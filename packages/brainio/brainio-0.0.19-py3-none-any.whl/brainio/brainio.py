"""
brainio
========

A module to load and save 'brains' (image 3D volumes) as either nifty image
files, tiff stacks or sequences of tiffs either from the folder they are
stored in or a file containing a sorted list of file paths
"""

import os
import math
import nrrd
import logging
import tifffile
import warnings
import numpy as np

from skimage import transform
from tqdm import tqdm
from natsort import natsorted
from concurrent.futures import ProcessPoolExecutor

from imlib.general.system import get_sorted_file_paths, get_num_processes

from .utils import check_mem, scale_z

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import nibabel as nib


# ######################## INPUT METHODS ####################
def load_any(
    src_path,
    x_scaling_factor=1.0,
    y_scaling_factor=1.0,
    z_scaling_factor=1.0,
    anti_aliasing=True,
    load_parallel=False,
    sort_input_file=False,
    as_numpy=False,
    n_free_cpus=2,
):
    """
    This function will guess the type of data and hence call the appropriate
    function from this module to load the given brain.

    .. warning:: x and y scaling not used at the moment if loading a
        complete image

    :param str src_path: Can be the path of a nifty file, tiff file,
        tiff files folder or text file containing a list of paths
    :param float x_scaling_factor: The scaling of the brain along the x
        dimension (applied on loading before return)
    :param float y_scaling_factor: The scaling of the brain along the y
        dimension (applied on loading before return)
    :param float z_scaling_factor: The scaling of the brain along the z
        dimension (applied on loading before return)
    :param bool anti_aliasing: Whether to apply a Gaussian filter to smooth
        the image prior to down-scaling. It is crucial to filter when
        down-sampling the image to avoid aliasing artifacts.
    :param bool load_parallel: Load planes in parallel using multiprocessing
        for faster data loading
    :param bool sort_input_file: If set to true and the input is a filepaths
        file, it will be naturally sorted
    :param bool as_numpy: Whether to convert the image to a numpy array in
        memory (rather than a memmap). Only relevant for .nii files.
    :param bool verbose: Print more information about the process
    :param int n_free_cpus: Number of cpu cores to leave free.
    :return: The loaded brain
    :rtype: np.ndarray
    """
    src_path = str(src_path)

    if os.path.isdir(src_path):
        logging.debug("Data type is: directory of files")
        img = load_from_folder(
            src_path,
            x_scaling_factor,
            y_scaling_factor,
            z_scaling_factor,
            anti_aliasing=anti_aliasing,
            file_extension=".tif",
            load_parallel=load_parallel,
            n_free_cpus=n_free_cpus,
        )
    elif src_path.endswith(".txt"):
        logging.debug("Data type is: list of file paths")
        img = load_img_sequence(
            src_path,
            x_scaling_factor,
            y_scaling_factor,
            z_scaling_factor,
            anti_aliasing=anti_aliasing,
            load_parallel=load_parallel,
            sort=sort_input_file,
            n_free_cpus=n_free_cpus,
        )
    elif src_path.endswith((".tif", ".tiff")):
        logging.debug("Data type is: tif stack")
        img = load_img_stack(
            src_path,
            x_scaling_factor,
            y_scaling_factor,
            z_scaling_factor,
            anti_aliasing=anti_aliasing,
        )
    elif src_path.endswith(".nrrd"):
        logging.debug("Data type is: nrrd")
        img = load_nrrd(src_path)
    elif src_path.endswith((".nii", ".nii.gz")):
        logging.debug("Data type is: NifTI")
        img = load_nii(src_path, as_array=True, as_numpy=as_numpy)
    else:
        raise NotImplementedError(
            "Could not guess data type for path {}".format(src_path)
        )

    return img


def load_nrrd(src_path):
    """
    Load an .nrrd file as a numpy array

    :param str src_path: The path of the image to be loaded
    :return: The loaded brain array
    :rtype: np.ndarray
    """
    src_path = str(src_path)
    stack, _ = nrrd.read(src_path)
    return stack


def load_img_stack(
    stack_path,
    x_scaling_factor,
    y_scaling_factor,
    z_scaling_factor,
    anti_aliasing=True,
):
    """
    Load a tiff stack as a numpy array

    :param str stack_path: The path of the image to be loaded
    :param float x_scaling_factor: The scaling of the brain along the x
        dimension (applied on loading before return)
    :param float y_scaling_factor: The scaling of the brain along the y
        dimension (applied on loading before return)
    :param float z_scaling_factor: The scaling of the brain along the z
        dimension (applied on loading before return)
    :param bool anti_aliasing: Whether to apply a Gaussian filter to smooth
        the image prior to down-scaling. It is crucial to filter when
        down-sampling the image to avoid aliasing artifacts.
    :return: The loaded brain array
    :rtype: np.ndarray
    """
    stack_path = str(stack_path)
    logging.debug(f"Loading: {stack_path}")
    stack = tifffile.imread(stack_path)

    # Downsampled plane by plane because the 3D downsampling in scipy etc
    # uses too much RAM

    if not (x_scaling_factor == y_scaling_factor == 1):
        downsampled_stack = []
        logging.debug("Downsampling stack in X/Y")
        for plane in tqdm(range(0, len(stack))):
            downsampled_stack.append(
                transform.rescale(
                    stack[plane],
                    (y_scaling_factor, x_scaling_factor),
                    mode="constant",
                    preserve_range=True,
                    anti_aliasing=anti_aliasing,
                )
            )

        logging.debug("Converting downsampled stack to array")
        stack = np.array(downsampled_stack)

    if stack.ndim == 3:
        stack = np.rollaxis(stack, 0, 3)
        if z_scaling_factor != 1:
            logging.debug("Downsampling stack in Z")
            stack = scale_z(stack, z_scaling_factor)
    return stack


def load_nii(src_path, as_array=False, as_numpy=False):
    """
    Load a brain from a nifti file

    :param str src_path: The path to the nifty file on the filesystem
    :param bool as_array: Whether to convert the brain to a numpy array of
        keep it as nifty object
    :param bool as_numpy: Whether to convert the image to a numpy array in
        memory (rather than a memmap)
    :return: The loaded brain (format depends on the above flag)
    """
    src_path = str(src_path)
    nii_img = nib.load(src_path)
    if as_array:
        image = nii_img.get_data()
        if as_numpy:
            image = np.array(image)

        return image
    else:
        return nii_img


def load_from_folder(
    src_folder,
    x_scaling_factor,
    y_scaling_factor,
    z_scaling_factor,
    anti_aliasing=True,
    file_extension="",
    load_parallel=False,
    n_free_cpus=2,
):
    """
    Load a brain from a folder. All tiff files will be read sorted and assumed
    to belong to the same sample.
    Optionally a name_filter string can be supplied which will have to be
    present in the file names for them
    to be considered part of the sample

    :param str src_folder:
    :param float x_scaling_factor: The scaling of the brain along the x
        dimension (applied on loading before return)
    :param float y_scaling_factor: The scaling of the brain along the y
        dimension (applied on loading before return)
    :param float z_scaling_factor: The scaling of the brain along the z
        dimension
    :param bool anti_aliasing: Whether to apply a Gaussian filter to smooth
        the image prior to down-scaling. It is crucial to filter when
        down-sampling the image to avoid aliasing artifacts.
    :param str file_extension: will have to be present in the file names for them\
        to be considered part of the sample
    :param bool load_parallel: Use multiprocessing to speedup image loading
    :param int n_free_cpus: Number of cpu cores to leave free.
    :return: The loaded and scaled brain
    :rtype: np.ndarray
    """
    paths = get_sorted_file_paths(src_folder, file_extension=file_extension)

    return load_image_series(
        paths,
        x_scaling_factor,
        y_scaling_factor,
        z_scaling_factor,
        load_parallel=load_parallel,
        n_free_cpus=n_free_cpus,
        anti_aliasing=anti_aliasing,
    )


def load_img_sequence(
    img_sequence_file_path,
    x_scaling_factor,
    y_scaling_factor,
    z_scaling_factor,
    anti_aliasing=True,
    load_parallel=False,
    sort=False,
    n_free_cpus=2,
):
    """
    Load a brain from a sequence of files specified in a text file containing
    an ordered list of paths

    :param str img_sequence_file_path: The path to the file containing the
        ordered list of image paths (one per line)
    :param float x_scaling_factor: The scaling of the brain along the x
        dimension (applied on loading before return)
    :param float y_scaling_factor: The scaling of the brain along the y
        dimension (applied on loading before return)
    :param float z_scaling_factor: The scaling of the brain along the z
        dimension
    :param bool anti_aliasing: Whether to apply a Gaussian filter to smooth
        the image prior to down-scaling. It is crucial to filter when
        down-sampling the image to avoid aliasing artifacts.
    :param bool load_parallel: Use multiprocessing to speedup image loading
    :param bool sort: If set to true will perform a natural sort of the
        file paths in the list
    :param int n_free_cpus: Number of cpu cores to leave free.
    :return: The loaded and scaled brain
    :rtype: np.ndarray
    """
    img_sequence_file_path = str(img_sequence_file_path)
    with open(img_sequence_file_path, "r") as in_file:
        paths = in_file.readlines()
        paths = [p.strip() for p in paths]
    if sort:
        paths = natsorted(paths)

    return load_image_series(
        paths,
        x_scaling_factor,
        y_scaling_factor,
        z_scaling_factor,
        load_parallel=load_parallel,
        n_free_cpus=n_free_cpus,
        anti_aliasing=anti_aliasing,
    )


def load_image_series(
    paths,
    x_scaling_factor,
    y_scaling_factor,
    z_scaling_factor,
    anti_aliasing=True,
    load_parallel=False,
    n_free_cpus=2,
):
    """
    Load a brain from a sequence of files specified in a text file containing
    an ordered list of paths

    :param lost paths: Ordered list of image paths
    :param float x_scaling_factor: The scaling of the brain along the x
        dimension (applied on loading before return)
    :param float y_scaling_factor: The scaling of the brain along the y
        dimension (applied on loading before return)
    :param float z_scaling_factor: The scaling of the brain along the z
        dimension
    :param bool anti_aliasing: Whether to apply a Gaussian filter to smooth
        the image prior to down-scaling. It is crucial to filter when
        down-sampling the image to avoid aliasing artifacts.
    :param bool load_parallel: Use multiprocessing to speedup image loading
    :param int n_free_cpus: Number of cpu cores to leave free.
    :return: The loaded and scaled brain
    :rtype: np.ndarray
    """

    if load_parallel:
        img = threaded_load_from_sequence(
            paths,
            x_scaling_factor,
            y_scaling_factor,
            n_free_cpus=n_free_cpus,
            anti_aliasing=anti_aliasing,
        )
    else:
        img = load_from_paths_sequence(
            paths,
            x_scaling_factor,
            y_scaling_factor,
            anti_aliasing=anti_aliasing,
        )
    if z_scaling_factor != 1:
        img = scale_z(img, z_scaling_factor)

    return img


def threaded_load_from_sequence(
    paths_sequence,
    x_scaling_factor=1.0,
    y_scaling_factor=1.0,
    anti_aliasing=True,
    n_free_cpus=2,
):
    """
    Use multiprocessing to load a brain from a sequence of image paths.

    :param list paths_sequence: The sorted list of the planes paths on the
        filesystem
    :param float x_scaling_factor: The scaling of the brain along the x
        dimension (applied on loading before return)
    :param float y_scaling_factor: The scaling of the brain along the y
        dimension (applied on loading before return)
    :param bool anti_aliasing: Whether to apply a Gaussian filter to smooth
        the image prior to down-scaling. It is crucial to filter when
        down-sampling the image to avoid aliasing artifacts.
    :param int n_free_cpus: Number of cpu cores to leave free.
    :return: The loaded and scaled brain
    :rtype: np.ndarray
    """

    stacks = []
    n_processes = get_num_processes(min_free_cpu_cores=n_free_cpus)

    # WARNING: will not work with interactive interpreter.
    pool = ProcessPoolExecutor(max_workers=n_processes)
    # FIXME: should detect and switch to other method

    n_paths_per_subsequence = math.ceil(len(paths_sequence) / n_processes)
    for i in range(n_processes):
        start_idx = i * n_paths_per_subsequence
        if start_idx >= len(paths_sequence):
            break
        else:
            end_idx = start_idx + n_paths_per_subsequence
            end_idx = end_idx if end_idx < len(paths_sequence) else -1
            sub_paths = paths_sequence[start_idx:end_idx]

        process = pool.submit(
            load_from_paths_sequence,
            sub_paths,
            x_scaling_factor,
            y_scaling_factor,
            anti_aliasing=anti_aliasing,
        )
        stacks.append(process)
    stack = np.dstack([s.result() for s in stacks])
    return stack


def load_from_paths_sequence(
    paths_sequence,
    x_scaling_factor=1.0,
    y_scaling_factor=1.0,
    anti_aliasing=True,
):
    # TODO: Optimise -  load threaded and process by batch
    """
    A single core version of the function to load a brain from a sequence of
    image paths.

    :param list paths_sequence: The sorted list of the planes paths on the
        filesystem
    :param float x_scaling_factor: The scaling of the brain along the x
        dimension (applied on loading before return)
    :param float y_scaling_factor: The scaling of the brain along the y
        dimension (applied on loading before return)
    :param bool anti_aliasing: Whether to apply a Gaussian filter to smooth
        the image prior to down-scaling. It is crucial to filter when
        down-sampling the image to avoid aliasing artifacts.
    :return: The loaded and scaled brain
    :rtype: np.ndarray
    """
    for i, p in enumerate(
        tqdm(paths_sequence, desc="Loading images", unit="plane")
    ):
        img = tifffile.imread(p)
        if i == 0:
            check_mem(
                img.nbytes * x_scaling_factor * y_scaling_factor,
                len(paths_sequence),
            )
            # TEST: add test case for shape rounding
            volume = np.empty(
                (
                    int(round(img.shape[0] * x_scaling_factor)),
                    int(round(img.shape[1] * y_scaling_factor)),
                    len(paths_sequence),
                ),
                dtype=img.dtype,
            )
        if x_scaling_factor != 1 and y_scaling_factor != 1:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                img = transform.rescale(
                    img,
                    (x_scaling_factor, y_scaling_factor),
                    mode="constant",
                    preserve_range=True,
                    anti_aliasing=anti_aliasing,
                )
        volume[:, :, i] = img
    return volume


def generate_paths_sequence_file(
    input_folder,
    output_file_path,
    sort=True,
    prefix=None,
    suffix=None,
    match_string=None,
):
    input_folder = str(input_folder)
    paths = []
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if prefix is not None and not filename.startswith(prefix):
                continue
            if suffix is not None and not filename.endswith(suffix):
                continue
            if match_string is not None and match_string not in filename:
                continue
            paths.append(os.path.join(root, filename))

    if sort:
        paths = natsorted(paths)

    with open(output_file_path, "w") as out_file:
        out_file.writelines(paths)


def get_size_image_from_file_paths(file_path, file_extension="tif"):
    """
    Returns the size of an image (which is a list of 2D files), without loading
    the whole image
    :param str file_path: File containing file_paths in a text file,
    or as a list.
    :param str file_extension: Optional file extension (if a directory
     is passed)
    :return: Dict of image sizes
    """
    file_path = str(file_path)

    img_paths = get_sorted_file_paths(file_path, file_extension=file_extension)
    z_shape = len(img_paths)

    logging.debug(
        "Loading file: {} to check raw image size" "".format(img_paths[0])
    )
    image_0 = load_any(img_paths[0])
    y_shape, x_shape = image_0.shape

    image_shape = {"x": x_shape, "y": y_shape, "z": z_shape}
    return image_shape


# ######################## OUTPUT METHODS ########################
def to_nii(img, dest_path, scale=None, affine_transform=None):
    # TODO: see if we want also real units scale

    """
    Write the brain volume to disk as nifty image.

    :param img: A nifty image object or numpy array brain
    :param str dest_path: The path where to save the brain.
    :param tuple scale: A tuple of floats to indicate the 'zooms' of the nifty
        image
    :param np.ndarray affine_transform: A 4x4 matrix indicating the transform
        to save in the metadata of the image (required only if not nibabel input)
    :return:
    """
    dest_path = str(dest_path)
    if affine_transform is None:
        affine_transform = np.eye(4)
    if not isinstance(img, nib.Nifti1Image):
        img = nib.Nifti1Image(img, affine_transform)
    if scale is not None:
        img.header.set_zooms(scale)
    nib.save(img, dest_path)


def tiff_to_nii(src_path, dest_path, affine_transform=None):
    """
    Load the tiff image and save it as a nifty image.

    :param str src_path: The path of the tiff image (can be multiple plains
        (folder of files list) or a single stack
    :param str dest_path: The path to save the nifty image to.
    :param np.array affine_transform: a 4x4 matrix specifying the affine
        transformation to be associated with the nii
    :return:
    """
    src_path = str(src_path)
    dest_path = str(dest_path)

    if not dest_path.endswith(".nii.gz"):
        raise ValueError(
            'Path is expected to end in "nii.gz", got {} '
            "instead.".format(dest_path)
        )

    img = load_any(src_path)
    if affine_transform is None:
        affine_transform = np.eye(4)
    if not isinstance(img, nib.Nifti1Image):
        img = nib.Nifti1Image(img, affine_transform)
    nib.save(img, os.path.normpath(dest_path))


def to_tiff(img_volume, dest_path):
    """
    Saves the image volume (numpy array) to a tiff stack

    :param np.ndarray img_volume: The image to be saved
    :param dest_path: Where to save the tiff stack
    :return:
    """
    dest_path = str(dest_path)
    tifffile.imsave(dest_path, img_volume)


def to_tiffs(img_volume, path_prefix, path_suffix="", pad_width=4):
    """
    Save the image volume (numpy array) as a sequence of tiff planes.
    Each plane will have a filepath of the following for:
    pathprefix_zeroPaddedIndex_suffix.tif

    :param np.ndarray img_volume: The image to be saved
    :param str path_prefix:  The prefix for each plane
    :param str path_suffix: The suffix for each plane
    :param int pad_width: The number of digits on which the index of the
        image (z plane number) will be padded
    :return:
    """
    z_size = img_volume.shape[-1]
    if z_size > 10 ** pad_width:
        raise ValueError(
            "Not enough padding digits {} for value"
            " {}".format(pad_width, z_size)
        )
    for i in range(z_size):
        img = img_volume[:, :, i]
        dest_path = "{}_{}{}.tif".format(
            path_prefix, str(i).zfill(pad_width), path_suffix
        )
        tifffile.imsave(dest_path, img)
