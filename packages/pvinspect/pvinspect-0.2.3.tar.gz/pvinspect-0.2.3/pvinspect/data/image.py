from __future__ import annotations


"""Provides classes to store and visualize images with metadata"""

import numpy as np
from skimage import io, img_as_uint, img_as_float64, img_as_int
from pvinspect.common.transform import Transform
from matplotlib import pyplot as plt
from pathlib import Path
from typing import List, Tuple, Union, Callable, Type, TypeVar, Any, Dict
from copy import deepcopy
import math
from functools import wraps
import logging
from pvinspect.common._ipy_exit import exit
import inspect
import sys
from enum import Enum
import re
import pandas as pd
from tqdm.autonotebook import tqdm

# this is a pointer to the module object instance itself
this = sys.modules[__name__]


# modality
class Modality(Enum):
    EL_IMAGE = (0,)
    PL_IMAGE = 1


EL_IMAGE = Modality.EL_IMAGE
"""Indicate an electroluminescense (EL) image"""
PL_IMAGE = Modality.PL_IMAGE
"""Indicate a photoluminescense (PL) image"""


# datatypes
DTYPE_INT = np.int32
DTYPE_UNSIGNED_INT = np.uint16
DTYPE_FLOAT = np.float64
img_as_float = img_as_float64


class DType(Enum):
    INT = 0
    UNSIGNED_INT = 1
    FLOAT = 2


# global list of plugins that are called on every .show()
this.show_plugins = list()


def register_show_plugin(callable, priority: int = 0):
    """Register a new plugin that is called on every .show()

    Args:
        callable: Callable that receives the image as a first argument and variable arguments to .show() next
        priority (int): Plugins are invoked in the order of increasing priority (highest priority is invoked
            last and hence appears on top)
    """
    this.show_plugins.append((priority, callable))
    this.show_plugins = sorted(this.show_plugins, key=lambda x: x[0])


def _invoke_show_plugins(image, **kwargs):
    for p in this.show_plugins:
        p[1](image, **kwargs)


def _register_default_plugins():
    def show_cell_crossings(
        image: ModuleImage, show_cell_crossings: bool = True, **kwargs
    ):
        if (
            show_cell_crossings
            and isinstance(image, ModuleImage)
            and image.has_meta("transform")
        ):
            grid = image.grid()
            coords = image.get_meta("transform").__call__(grid)
            plt.scatter(coords[:, 0], coords[:, 1], c="yellow", marker="+")

    register_show_plugin(show_cell_crossings)

    def multimodule_show_boxes(
        image: Image,
        multimodule_show_boxes: bool = True,
        multimodule_highlight_selection: bool = True,
        multimodule_boxes_linewidth: int = 2,
        **kwargs
    ):
        if (
            multimodule_show_boxes
            and isinstance(image, Image)
            and image.has_meta("multimodule_boxes")
        ):
            for i, box in enumerate(image.get_meta("multimodule_boxes")):
                color = (
                    "red"
                    if i == image.get_meta("multimodule_index")
                    and multimodule_highlight_selection
                    else "yellow"
                )
                plt.plot(
                    *box[1].exterior.xy,
                    linewidth=multimodule_boxes_linewidth,
                    color=color,
                )

    register_show_plugin(multimodule_show_boxes)

    def multimodule_show_numbers(
        image: Image,
        multimodule_show_numbers: bool = True,
        multimodule_highlight_selection: bool = True,
        multimodule_numbers_fontsize: int = 20,
        **kwargs
    ):
        if (
            multimodule_show_numbers
            and isinstance(image, Image)
            and image.has_meta("multimodule_boxes")
        ):
            for i, box in enumerate(image.get_meta("multimodule_boxes")):
                bgcolor = (
                    "red"
                    if i == image.get_meta("multimodule_index")
                    and multimodule_highlight_selection
                    else "white"
                )
                textcolor = (
                    "white"
                    if i == image.get_meta("multimodule_index")
                    and multimodule_highlight_selection
                    else "black"
                )
                plt.text(
                    box[1].centroid.x,
                    box[1].centroid.y,
                    s=str(i),
                    color=textcolor,
                    fontsize=multimodule_numbers_fontsize,
                    bbox=dict(facecolor=bgcolor, alpha=0.8),
                    ha="center",
                    va="center",
                )

    register_show_plugin(multimodule_show_numbers)

    def calibration_show_reference_box(
        image: Image,
        calibration_show_reference_box: bool = True,
        calibration_reference_box_color="red",
        **kwargs
    ):
        if (
            calibration_show_reference_box
            and isinstance(image, Image)
            and image.has_meta("calibration_reference_box")
        ):
            plt.plot(
                *image.get_meta("calibration_reference_box").exterior.xy,
                # linewidth=multimodule_boxes_linewidth,
                color=calibration_reference_box_color,
            )

    register_show_plugin(calibration_show_reference_box)

    def segment_module_show_box(
        image: Image,
        segment_module_show_box: bool = True,
        segment_module_show_box_color="red",
        **kwargs
    ):
        if (
            segment_module_show_box
            and isinstance(image, Image)
            and image.has_meta("segment_module_original_box")
        ):
            plt.plot(
                *image.get_meta("segment_module_original_box").exterior.xy,
                color=segment_module_show_box_color,
            )

    register_show_plugin(segment_module_show_box)

    def show_image(
        image: Image,
        clip_low: float = 0.001,
        clip_high: float = 99.999,
        colorbar: bool = True,
        **kwargs
    ):
        clip_low = clip_low if clip_low is not None else 0.0
        clip_high = clip_high if clip_high is not None else 100.0
        p = np.percentile(image._data, [clip_low, clip_high])
        d = np.clip(image._data, p[0], p[1])
        plt.imshow(d, cmap="gray")
        if colorbar:
            plt.colorbar()

    register_show_plugin(show_image, -100)

    def axis_options(
        image: Image,
        show_axis: bool = True,
        show_title: bool = True,
        max_title_length: bool = 30,
        **kwargs
    ):
        if not show_axis:
            plt.axis("off")
        if show_title:
            if isinstance(image, CellImage):
                t = "{} (r: {:d}, c: {:d})".format(
                    str(image.path.name), image.row, image.col
                )
            else:
                t = str(image.path.name)

            if len(t) > max_title_length:
                l1 = max_title_length // 2 - 2
                l2 = max_title_length - l1 - 2
                t = t[:l1] + ".." + t[len(t) - l2 :]

            plt.title(t)

    register_show_plugin(axis_options, -200)


class _Base:

    T = TypeVar("T")

    @classmethod
    def from_other(
        cls: Type[T], other: T, drop_meta_types: List[Type] = None, **kwargs
    ) -> T:
        """Create a new image by partially overwriting the properties of another

        Args:
            other (Image): The other image
            drop_meta_types (List[Type]): Drop any meta attributes that are insteanceof these types
            **kwargs: Arguments that should be overwritten
        """
        required = inspect.getfullargspec(cls.__init__)[0]

        other_args = dict()
        for name in required:
            if name == "meta" and "meta" in kwargs.keys():
                # joint meta dictionaries
                tmp = deepcopy(other._meta)
                if drop_meta_types is not None:
                    tmp = {
                        k: v
                        for k, v in tmp.items()
                        if not np.any([isinstance(v, x) for x in drop_meta_types])
                    }
                tmp.update(kwargs["meta"])
                kwargs["meta"] = tmp
            if name not in kwargs.keys() and name != "self":

                # first, try public property, then private property, then meta attribute
                if hasattr(other, name):
                    other_args[name] = getattr(other, name)
                elif hasattr(other, "_" + name):
                    other_args[name] = getattr(other, "_" + name)
                elif isinstance(other, Image) and other.has_meta(name):
                    other_args[name] = other.get_meta(name)

                if name == "meta" and drop_meta_types is not None:
                    other_args[name] = {
                        k: v
                        for k, v in other_args[name].items()
                        if not np.any([isinstance(v, x) for x in drop_meta_types])
                    }

        return cls(**kwargs, **other_args)


class Image(_Base):
    """A general image"""

    def __init__(
        self,
        data: np.ndarray,
        path: Path,
        modality: Modality = None,
        meta: Dict[str, Any] = None,
    ):
        """Create a new image. All non-float images as automatically converted to uint.

        Args:
            data (np.ndarray): The image data
            path (Path): Path to the image
            modality (Modality): The imaging modality
            meta (Dict[str, Any]): Meta attributes of this image
        """
        self._data = data
        self._meta = meta if meta is not None else dict()
        self._meta["modality"] = modality
        self._meta["path"] = path

        # unify datatypes
        if self.dtype == DType.UNSIGNED_INT and self._data.dtype != DTYPE_UNSIGNED_INT:
            if (
                self._data.max() > np.iinfo(DTYPE_UNSIGNED_INT).max
                or self._data.min() < np.iinfo(DTYPE_UNSIGNED_INT).min
            ):
                raise RuntimeError(
                    "Datatype conversion to {} failed, since original data exceeds dtype limits.".format(
                        DTYPE_UNSIGNED_INT
                    )
                )
            self._data = self._data.astype(DTYPE_UNSIGNED_INT)
        if self.dtype == DType.INT and self._data.dtype != DTYPE_INT:
            if (
                self._data.max() > np.iinfo(DTYPE_INT).max
                or self._data.min() < np.iinfo(DTYPE_INT).min
            ):
                raise RuntimeError(
                    "Datatype conversion to {} failed, since original data exceeds dtype limits.".format(
                        DTYPE_INT
                    )
                )
            self._data = self._data.astype(DTYPE_INT)
        if self.dtype == DType.FLOAT and self._data.dtype != DTYPE_FLOAT:
            self._data = self._data.astype(DTYPE_FLOAT)

    def show(self, **kwargs):
        """Show this image"""
        _invoke_show_plugins(self, **kwargs)

    _T = TypeVar("T")

    def as_type(self: _T, dtype: DType) -> _T:
        if dtype == DType.FLOAT:
            return type(self).from_other(self, data=img_as_float(self._data))
        elif dtype == DType.UNSIGNED_INT:
            return type(self).from_other(self, data=img_as_uint(self._data))
        elif dtype == DType.INT:
            return type(self).from_other(self, data=img_as_int(self._data))

    def __add__(self: _T, other: _T) -> _T:
        if self.dtype != other.dtype:
            raise RuntimeError("Images must have the same datatype")
        return type(self).from_other(self, data=self._data + other._data)

    def __sub__(self: _T, other: _T) -> _T:
        if self.dtype != other.dtype:
            raise RuntimeError("Images must have the same datatype")
        if self.dtype == DType.UNSIGNED_INT:
            res = self._data.astype(DTYPE_INT) - other._data.astype(DTYPE_INT)
            iinfo = np.iinfo(DTYPE_UNSIGNED_INT)
            res = np.clip(res, 0, iinfo.max)
            return type(self).from_other(self, data=res)
        else:
            return type(self).from_other(self, data=self._data - other._data)

    def __mul__(self: _T, other: _T) -> _T:
        if self.dtype != other.dtype:
            raise RuntimeError("Images must have the same datatype")
        return type(self).from_other(self, data=self._data * other._data)

    def __truediv__(self: _T, other: _T) -> _T:
        if self.dtype != DType.FLOAT or other.dtype != DType.FLOAT:
            raise RuntimeError("Images must be of type float")
        return type(self).from_other(self, data=self._data / other._data)

    def __floordiv__(self: _T, other: _T) -> _T:
        if self.dtype != other.dtype:
            raise RuntimeError("Images must have the same datatype")
        return type(self).from_other(self, data=self._data // other._data)

    def __mod__(self: _T, other: _T) -> _T:
        if self.dtype != other.dtype:
            raise RuntimeError("Images must have the same datatype")
        return type(self).from_other(self, data=self._data % other._data)

    def __pow__(self: _T, other: _T) -> _T:
        if self.dtype != other.dtype:
            raise RuntimeError("Images must have the same datatype")
        return type(self).from_other(self, data=self._data ** other._data)

    @property
    def data(self) -> np.ndarray:
        """The underlying image data"""
        v = self._data.view()
        v.setflags(write=False)
        return v

    @property
    def path(self) -> Path:
        """Path to the original image"""
        return self.get_meta("path")

    @property
    def dtype(self) -> DType:
        """Datatype of the image"""
        if self.data.dtype == np.float32 or self.data.dtype == np.float64:
            return DType.FLOAT
        elif (
            self.data.dtype == np.uint8
            or self.data.dtype == np.uint16
            or self.data.dtype == np.uint32
            or self.data.dtype == np.uint64
        ):
            return DType.UNSIGNED_INT
        elif (
            self.data.dtype == np.int8
            or self.data.dtype == np.int16
            or self.data.dtype == np.int32
            or self.data.dtype == np.int64
        ):
            return DType.INT

    @property
    def shape(self) -> Tuple[int, int]:
        """Shape of the image"""
        return deepcopy(self.data.shape)

    @property
    def modality(self) -> Modality:
        """The imaging modality"""
        return self.get_meta("modality")

    def get_meta(self, key: str) -> Any:
        """Access a meta attribute"""
        if isinstance(self._meta[key], np.ndarray):
            v = self._meta[key].view()
            v.setflags(write=False)
            return v
        else:
            return deepcopy(self._meta[key])

    def has_meta(self, key: str) -> bool:
        """Check if a meta attribute is set"""
        return key in self._meta.keys()

    def list_meta(self) -> List[str]:
        """List avaliable meta keys"""
        return list(self._meta.keys())

    def meta_from_path(
        self,
        pattern: str,
        key: str,
        target_type: Type,
        group_n: int = 0,
        transform: Callable[[Any], Any] = None,
    ) -> Image:
        """Extract meta information from path. The group_n'th matching group
        from pattern is used as meta value

        Args:
            pattern (str): Regular expression used to parse meta
            key (str): Key of the meta attribute
            target_type (Type): Result is converted to this datatype
            group_n (int): Index of matching group
            transform (Callable[[Any], Any]): Optional function that is applied on the value
                before datatype conversion

        Returns:
            image (Image): Resulting Image
        """
        s = str(self.path.absolute())
        res = re.search(pattern, s)
        v = res.group(group_n)
        if transform is not None:
            v = transform(v)
        v = target_type(v)
        return type(self).from_other(self, meta={key: v})

    def meta_from_fn(self, fn: Callable[[Image], Dict[str, Any]]) -> Image:
        """Extract meta data using given callable

        Args:
            fn (Callable[[Image], Dict[str, Any]]): Function used to extract meta data
        
        Returns
            image (Image): Resulting Image
        """
        return self.from_other(self, meta=fn(self))

    def meta_to_pandas(self) -> pd.Series:
        """Convert (compatible) meta data to pandas series"""
        data = pd.Series(self._meta, copy=True)
        data["shape"] = self.shape
        data["dtype"] = self.dtype
        return data


class ImageSequence(_Base):
    """An immutable sequence of images, allowing for access to single images as well as analysis of the sequence"""

    def _show(self, imgs: List[Image], cols: int, *args, **kwargs):
        N = len(imgs)
        rows = math.ceil(N / cols)

        # adjust the figure size
        if self.shape is not None:
            aspect = self.shape[0] / self.shape[1]
        else:
            aspect = 1.0
        plt.figure(figsize=(6 * cols, 6 * rows * aspect))

        for i, img in enumerate(imgs):
            plt.subplot(rows, cols, i + 1)
            img.show(*args, **kwargs)

    def __init__(
        self, images: List[Image], same_camera: bool, allow_different_dtypes=False
    ):
        """Initialize a module image sequence
        
        Args:
            images (List[Image]): The list of images
            came_camera (bool): Indicates, if all images are from the same camera and hence share the same intrinsic parameters
            allow_different_dtypes (bool): Allow images to have different datatypes?
        """

        self._images = images
        self._same_camera = same_camera
        self._allow_different_dtypes = allow_different_dtypes
        self._meta_df = None
        if len(self.images) == 0:
            logging.error("Creation of an empty sequence is not supported")
            exit()

        # check that all have the same modality, dimension, dtype and module configuration
        shape = self.images[0].shape
        dtype = self.images[0].dtype
        modality = self.images[0].modality
        for img in self.images:
            if img.dtype != dtype and not allow_different_dtypes:
                logging.error(
                    'Cannot create sequence from mixed dtypes. Consider using the "allow_different_dtypes" argument, when reading images.'
                )
                exit()
            if img.shape != shape and same_camera:
                logging.error(
                    'Cannot create sequence from mixed shapes. Consider using the "same_camera" argument, when reading images.'
                )
                exit()
            if img.modality != modality:
                logging.error("Cannot create a sequence from mixed modalities.")
                exit()

    def head(self, N: int = 4, cols: int = 2, *args, **kwargs):
        """Show the first N images

        Args:
            N (int): Number of images to show
            cols (int): How many images to show in a column
        """
        self._show(self.images[:N], cols, *args, **kwargs)

    def tail(self, N: int = 4, cols: int = 2, *args, **kwargs):
        """Show the last N images

        Args:
            N (int): Number of images to show
            cols (int): How many images to show in a column
        """
        self._show(self.images[-N:], cols, *args, **kwargs)

    _T = TypeVar("T")

    def apply(
        self, fn: Callable[[Image], Image], *argv, progress_bar: bool = True, **kwargs
    ) -> ImageSequence:
        """Apply the given callable on every image. Returns a copy of the
        original sequence

        Args:
            fn (Callable[[Image], Image]): Callable that receives and returns an Image
            progress_bar (bool): Show progress bar?
        
        Returns:
            sequence (ImageSequence): The copy with modified images
        """
        result = []
        p = tqdm if progress_bar else lambda x: x
        for img in p(self._images):
            result.append(fn(img, *argv, **kwargs))
        return type(self).from_other(self, images=result)

    def apply_image_data(
        self: _T,
        fn: Callable[[np.ndarray], np.ndarray],
        *argv,
        progress_bar: bool = True,
        **kwargs
    ) -> _T:
        """Apply the given callable on every image data. Returns a copy of the
        original sequence with modified data

        Args:
            fn (Callable[[np.ndarray], np.ndarray]): Callable that receives a np.ndarray
                and returns a np.ndarray. Note that the argument is immutable.
            progress_bar (bool): Show progress bar?
        
        Returns:
            sequence (ImageSequence): The copy with modified data
        """
        result = []
        p = tqdm if progress_bar else lambda x: x
        for img in p(self._images):
            data = img.data
            res = fn(data, *argv, **kwargs)
            result.append(type(img).from_other(img, data=res))
        return type(self).from_other(self, images=result)

    def meta_from_path(
        self,
        pattern: str,
        key: str,
        target_type: Type,
        group_n: int = 1,
        transform: Callable[[Any], Any] = None,
    ) -> ImageSequence:
        """Extract meta information from path of individual aimges. The group_n'th matching group
        from pattern is used as meta value

        Args:
            pattern (str): Regular expression used to parse meta
            key (str): Key of the meta attribute
            target_type (Type): Result is converted to this datatype
            group_n (int): Index of matching group
            transform (Callable[[Any], Any]): Optional function that is applied on the value
                before datatype conversion

        Returns:
            images (ImageSequence): Resulting ImageSequence
        """
        result = []
        for img in self._images:
            result.append(
                img.meta_from_path(
                    pattern=pattern,
                    key=key,
                    target_type=target_type,
                    group_n=group_n,
                    transform=transform,
                )
            )
        return type(self).from_other(self, images=result)

    def meta_from_fn(self, fn: Callable[[Image], Dict[str, Any]]) -> ImageSequence:
        """Extract meta information using given function

        Args:
            fn (Callable[[Image], Dict[str, Any]]): Function that is applied on every element of the sequence
        """
        return self.from_other(
            self, images=[img.meta_from_fn(fn) for img in self._images]
        )

    def meta_to_pandas(self) -> pd.DataFrame:
        """Convert meta from images to pandas DataFrame"""
        if self._meta_df is None:
            series = [img.meta_to_pandas() for img in self._images]
            self._meta_df = pd.DataFrame(data=series)
            self._meta_df = self._meta_df.astype(
                {"modality": str}
            )  # allow for easy comparison
        return self._meta_df.copy()  # pd.DataFrame has no writable flag :(

    def drop_duplicates(
        self, subset: List[str] = None, keep: str = "first"
    ) -> ImageSequence:
        """Drop duplicates based on meta attributes. For further reference, please
            refer to the corresponding pandas method

        Args:
            subset (List[str]): Meta keys
            keep (str): Same as pandas method

        Returns:
            result (ImageSequence): The images with duplicates dropped
        """
        idx = (
            self.meta_to_pandas()
            .drop_duplicates(subset=subset, keep=keep)
            .index.to_list()
        )
        result = [self._images[i] for i in idx]
        return type(self).from_other(self, images=result)

    def query(self, query: str) -> ImageSequence:
        """Query image sequence using image meta attributes

        Args:
            query (str): The query string using the query syntax of pandas library

        Returns:
            result (ImageSequence): The images, where query evaluated true
        """
        idx = self.meta_to_pandas().query(query).index.to_list()
        result = [self._images[i] for i in idx]
        return type(self).from_other(self, images=result)

    def as_type(self: _T, dtype: DType) -> _T:
        """Convert sequence to specified dtype"""
        result = [img.as_type(dtype) for img in self._images]
        return type(self).from_other(self, images=result)

    def __add__(self: _T, other: _T) -> _T:
        res = [x + y for x, y in zip(self.images, other.images)]
        return type(self).from_other(self, images=res)

    def __sub__(self: _T, other: _T) -> _T:
        res = [x - y for x, y in zip(self.images, other.images)]
        return type(self).from_other(self, images=res)

    def __mul__(self: _T, other: _T) -> _T:
        res = [x * y for x, y in zip(self.images, other.images)]
        return type(self).from_other(self, images=res)

    def __truediv__(self: _T, other: _T) -> _T:
        res = [x / y for x, y in zip(self.images, other.images)]
        return type(self).from_other(self, images=res)

    def __floordiv__(self: _T, other: _T) -> _T:
        res = [x // y for x, y in zip(self.images, other.images)]
        return type(self).from_other(self, images=res)

    def __mod__(self: _T, other: _T) -> _T:
        res = [x % y for x, y in zip(self.images, other.images)]
        return type(self).from_other(self, images=res)

    def __pow__(self: _T, other: _T) -> _T:
        res = [x ** y for x, y in zip(self.images, other.images)]
        return type(self).from_other(self, images=res)

    @property
    def images(self) -> List[Image]:
        """Access the list of images"""
        return self._images

    @property
    def dtype(self) -> DType:
        """Access the image datatype"""
        return self.images[0].dtype if not self._allow_different_dtypes else None

    @property
    def shape(self) -> Tuple[int, int]:
        """Access the image shape"""
        return self.images[0].shape if self._same_camera else None

    @property
    def modality(self) -> Modality:
        """Access the imaging modaility"""
        return self.images[0].modality

    @property
    def same_camera(self) -> bool:
        """Indicate, if the images originate from the same camera"""
        return self._same_camera

    def __len__(self) -> int:
        return len(self.images)

    def __getitem__(self, i: int) -> Image:
        return self.images[i]


ImageOrSequence = Union[Image, ImageSequence]


class CellImage(Image):
    """An image of a solar cell with additional meta data"""

    def __init__(
        self,
        data: np.ndarray,
        modality: Modality,
        path: Path,
        row: int,
        col: int,
        meta: Dict[str, Any] = None,
    ):
        """Initialize a cell image

        Args:
            data (np.ndarray): The image data
            modality (Modality): The imaging modality
            path (Path): Path to the image
            row (int): Row index (zero-based)
            col (int): Cell index (zero-based)
            meta (Dict[str, Any]): Meta data
        """

        super().__init__(data, path=path, modality=modality, meta=meta)
        self._meta["row"] = row
        self._meta["col"] = col

    @property
    def row(self) -> int:
        """0-based row index of the cell in the original module"""
        return self.get_meta("row")

    @property
    def col(self) -> int:
        """0-based column index of the cell in the original module"""
        return self.get_meta("col")

    def show(self, *argv, **kwargs):
        """Show this image"""
        super().show(*argv, **kwargs)


class CellImageSequence(ImageSequence):
    """An immutable sequence of cell images, allowing for access to single images as well as analysis of the sequence"""

    def __init__(self, images: List[CellImage]):
        """Initialize a module image sequence
        
        Args:
            images (List[CellImage]): The list of images
        """

        super().__init__(images, False)


class ModuleImage(Image):
    """An image of a solar module with additional meta data"""

    def __init__(
        self,
        data: np.ndarray,
        modality: Modality,
        path: Path,
        cols: int = None,
        rows: int = None,
        meta: dict = None,
    ):
        """Initialize a module image

        Args:
            data (np.ndarray): The image data
            modality (Modality): The imaging modality
            path (Path): Path to the image
            cols (int): Number of cells in a column
            rows (int): Number of cells in a row
        """

        super().__init__(data, path, modality, meta)
        self._meta["cols"] = cols
        self._meta["rows"] = rows

    def grid(self) -> np.ndarray:
        """Create a grid of corners according to the module geometry
        
        Returns:
            grid: (cols*rows, 2)-array of coordinates on a regular grid
        """

        if self.cols is not None and self.rows is not None:
            x, y = np.mgrid[0 : self.cols + 1 : 1, 0 : self.rows + 1 : 1]
            grid = np.stack([x.flatten(), y.flatten()], axis=1)
            return grid
        else:
            logging.error("Module geometry is not initialized")
            exit()

    @property
    def cols(self):
        """Number of cell-columns"""
        return self.get_meta("cols")

    @property
    def rows(self):
        """Number of row-columns"""
        return self.get_meta("rows")


class PartialModuleImage(ModuleImage):
    """An image of a solar module with additional meta data"""

    def __init__(
        self,
        data: np.ndarray,
        modality: Modality,
        path: Path,
        cols: int = None,
        rows: int = None,
        first_col: int = None,
        first_row: int = None,
        meta: dict = None,
    ):
        """Initialize a module image

        Args:
            data (np.ndarray): The image data
            modality (Modality): The imaging modality
            path (Path): Path to the image
            cols (int): Number of completely visible cells in a column
            rows (int): Number of completely visible cells in a row
            first_col (int): Index of the first complete column shown
            first_row (int): Index of the first complete row shown
        """

        super().__init__(data, modality, path, cols, rows, meta)

        self._meta["first_col"] = first_col
        self._meta["first_row"] = first_row


ModuleOrPartialModuleImage = Union[ModuleImage, PartialModuleImage]


class ModuleImageSequence(ImageSequence):
    """An immutable sequence of module images, allowing for access to single images as well as analysis of the sequence"""

    def __init__(
        self,
        images: List[ModuleOrPartialModuleImage],
        same_camera: bool,
        allow_different_dtypes=False,
    ):
        """Initialize a module image sequence
        
        Args:
            images (List[ModuleImage]): The list of images
            same_camera (bool): Indicates if all images are from the same camera
            allow_different_dtypes (bool): Allow images to have different datatypes?
        """

        cols = images[0].cols
        rows = images[0].rows
        for img in images:
            if img.cols != cols:
                logging.error(
                    "Cannot create sequence from different module configurations"
                )
                exit()
            if img.rows != rows:
                logging.error(
                    "Cannot create sequence from different module configurations"
                )
                exit()

        super().__init__(images, same_camera, allow_different_dtypes)


ModuleImageOrSequence = Union[
    ModuleImageSequence, ModuleImage, PartialModuleImage, Image
]


def _sequence(*args):
    """Assure that the first argument is a sequence and handle the first return value accordingly"""

    def decorator_sequence(func):
        @wraps(func)
        def wrapper_sequence(*args, **kwargs):
            if not isinstance(args[0], ImageSequence):
                args = list(args)
                args[0] = (
                    ModuleImageSequence([args[0]], same_camera=False)
                    if type(args[0]) == ModuleImage
                    else ImageSequence([args[0]], same_camera=False)
                )
                unwrap = True
            else:
                unwrap = False
            res = func(*tuple(args), **kwargs)
            if unwrap and not disable_unwrap:
                if isinstance(res, tuple) and isinstance(res[0], ImageSequence):
                    res[0] = res[0].images[0]
                elif isinstance(res, ImageSequence):
                    res = res.images[0]
            return res

        return wrapper_sequence

    if len(args) == 1 and callable(args[0]):
        disable_unwrap = False
        return decorator_sequence(args[0])
    else:
        disable_unwrap = args[0] if len(args) == 1 else False
        return decorator_sequence
