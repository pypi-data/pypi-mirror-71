"""
===============================================
vidgear library source-code is deployed under the Apache 2.0 License:

Copyright (c) 2019-2020 Abhishek Thakur(@abhiTronix) <abhi.una12@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
===============================================
"""

# Contains all the support functions/modules required by Vidgear packages

# import the necessary packages
import errno
import logging as log
import os
import platform
import sys

import numpy as np
import requests
from colorlog import ColoredFormatter
from pkg_resources import parse_version
from tqdm import tqdm

try:
    # import OpenCV Binaries
    import cv2

    # check whether OpenCV Binaries are 3.x+
    if parse_version(cv2.__version__) < parse_version("3"):
        raise ImportError(
            "[Vidgear:ERROR] :: Installed OpenCV API version(< 3.0) is not supported!"
        )
except ImportError:
    raise ImportError(
        "[Vidgear:ERROR] :: Failed to detect correct OpenCV executables, install it with `pip3 install opencv-python` command."
    )


def logger_handler():
    """
    ### logger_handler

    Returns a color formatted logger handler

    **Returns:** A logger handler
    """
    # logging formatter
    formatter = ColoredFormatter(
        "%(bold_blue)s%(name)s%(reset)s :: %(log_color)s%(levelname)s%(reset)s :: %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            "INFO": "bold_green",
            "DEBUG": "bold_yellow",
            "WARNING": "bold_purple",
            "ERROR": "bold_red",
            "CRITICAL": "bold_red,bg_white",
        },
    )
    # define handler
    handler = log.StreamHandler()
    handler.setFormatter(formatter)
    return handler


# define logger
logger = log.getLogger("Helper")
logger.addHandler(logger_handler())
logger.setLevel(log.DEBUG)


def check_CV_version():
    """
    ### check_CV_version

    Returns OpenCV binary in-use, version's first bit 
    """
    if parse_version(cv2.__version__) >= parse_version("4"):
        return 4
    else:
        return 3


def mkdir_safe(dir, logging=False):
    """
    ### mkdir_safe

    Safely creates directory at given path.

    Parameters:
        logging (bool): enables logging for its operations

    """
    try:
        os.makedirs(dir)
        if logging:
            logger.debug("Created directory at `{}`".format(dir))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        if logging:
            logger.debug("Directory already exists at `{}`".format(dir))


def capPropId(property):
    """
    ### capPropId

    Retrieves the OpenCV property's Integer(Actual) value from string.

    Parameters:
        property (string): inputs OpenCV property as string.

    **Returns:** Resultant integer value.
    """
    integer_value = 0
    try:
        integer_value = getattr(cv2, property)
    except Exception as e:
        logger.exception(str(e))
        logger.critical("`{}` is not a valid OpenCV property!".format(property))
        return None
    return integer_value


def reducer(frame=None, percentage=0):
    """
    ### reducer

    Reduces frame size by given percentage

    Parameters:
        frame (numpy.ndarray): inputs numpy array(frame).
        percentage (int/float): inputs size-reduction percentage.

    **Returns:**  A reduced numpy ndarray array.
    """
    # check if frame is valid
    if frame is None:
        raise ValueError("[Helper:ERROR] :: Input frame cannot be NoneType!")

    # check if valid reduction percentage is given
    if not (percentage > 0 and percentage < 90):
        raise ValueError(
            "[Helper:ERROR] :: Given frame-size reduction percentage is invalid, Kindly refer docs."
        )

    # grab the frame size
    (height, width) = frame.shape[:2]

    # calculate the ratio of the width from percentage
    reduction = ((100 - percentage) / 100) * width
    ratio = reduction / float(width)
    # construct the dimensions
    dimensions = (int(reduction), int(height * ratio))

    # return the resized frame
    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_LANCZOS4)


def dict2Args(param_dict):
    """
    ### dict2Args

    Converts dictionary attributes to list(args)
    
    Parameters:
        param_dict (dict): Parameters dictionary

    **Returns:** Arguments list
    """
    args = []
    for key in param_dict.keys():
        args.append(key)
        args.append(param_dict[key])
    return args


def get_valid_ffmpeg_path(
    custom_ffmpeg="", is_windows=False, ffmpeg_download_path="", logging=False
):
    """
    ### get_valid_ffmpeg_path

    Validate the given FFmpeg path/binaries, and returns a valid FFmpeg executable path.

    Parameters:
        custom_ffmpeg (string): path to custom FFmpeg executables
        is_windows (boolean): is running on Windows OS?
        ffmpeg_download_path (string): FFmpeg static binaries download location _(Windows only)_
        logging (bool): enables logging for its operations

    **Returns:** A  valid FFmpeg executable path string.
    """
    final_path = ""
    if is_windows:
        # checks if current os is windows
        if custom_ffmpeg:
            # if custom FFmpeg path is given assign to local variable
            final_path += custom_ffmpeg
        else:
            # otherwise auto-download them
            try:
                if not (ffmpeg_download_path):
                    # otherwise save to Temp Directory
                    import tempfile

                    ffmpeg_download_path = tempfile.gettempdir()

                if logging:
                    logger.debug(
                        "FFmpeg Windows Download Path: {}".format(ffmpeg_download_path)
                    )

                # download Binaries
                os_bit = (
                    ("win64" if platform.machine().endswith("64") else "win32")
                    if is_windows
                    else ""
                )
                _path = download_ffmpeg_binaries(
                    path=ffmpeg_download_path, os_windows=is_windows, os_bit=os_bit
                )
                # assign to local variable
                final_path += _path

            except Exception as e:
                # log if any error occurred
                if logging:
                    logger.exception(str(e))
                    logger.debug(
                        "Error in downloading FFmpeg binaries, Check your network and Try again!"
                    )
                return False

        if os.path.isfile(final_path):
            # check if valid FFmpeg file exist
            pass
        elif os.path.isfile(os.path.join(final_path, "ffmpeg.exe")):
            # check if FFmpeg directory exists, if does, then check for valid file
            final_path = os.path.join(final_path, "ffmpeg.exe")
        else:
            # else return False
            if logging:
                logger.debug("No valid FFmpeg executables found at Custom FFmpeg path!")
            return False
    else:
        # otherwise perform test for Unix
        if custom_ffmpeg:
            # if custom FFmpeg path is given assign to local variable
            if os.path.isfile(custom_ffmpeg):
                # check if valid FFmpeg file exist
                final_path += custom_ffmpeg
            elif os.path.isfile(os.path.join(custom_ffmpeg, "ffmpeg")):
                # check if FFmpeg directory exists, if does, then check for valid file
                final_path = os.path.join(custom_ffmpeg, "ffmpeg")
            else:
                # else return False
                if logging:
                    logger.debug(
                        "No valid FFmpeg executables found at Custom FFmpeg path!"
                    )
                return False
        else:
            # otherwise assign ffmpeg binaries from system
            final_path += "ffmpeg"

    if logging:
        logger.debug("Final FFmpeg Path: {}".format(final_path))

    # Final Auto-Validation for FFmeg Binaries. returns final path if test is passed
    if validate_ffmpeg(final_path, logging=logging):
        return final_path
    else:
        return False


def download_ffmpeg_binaries(path, os_windows=False, os_bit=""):
    """
    ### download_ffmpeg_binaries

    Generates FFmpeg Static Binaries for windows(if not available)

    Parameters:
        path (string): path for downloading custom FFmpeg executables
        os_windows (boolean): is running on Windows OS?
        os_bit (string): 32-bit or 64-bit OS?

    **Returns:** A  valid FFmpeg executable path string.
    """
    final_path = ""
    if os_windows and os_bit:
        # initialize variables
        file_url = "https://ffmpeg.zeranoe.com/builds/{}/static/ffmpeg-latest-{}-static.zip".format(
            os_bit, os_bit
        )
        file_name = os.path.join(
            os.path.abspath(path), "ffmpeg-latest-{}-static.zip".format(os_bit)
        )
        file_path = os.path.join(
            os.path.abspath(path),
            "ffmpeg-latest-{}-static/bin/ffmpeg.exe".format(os_bit),
        )
        base_path, _ = os.path.split(file_name)  # extract file base path
        # check if file already exists
        if os.path.isfile(file_path):
            final_path += file_path  # skip download if does
        else:
            # import libs
            import zipfile

            # check if given path has write access
            assert os.access(path, os.W_OK), (
                "[Helper:ERROR] :: Permission Denied, Cannot write binaries to directory = "
                + path
            )
            # remove leftovers if exists
            if os.path.isfile(file_name):
                os.remove(file_name)
            # download and write file to the given path
            with open(file_name, "wb") as f:
                logger.debug(
                    "No Custom FFmpeg path provided. Auto-Installing FFmpeg static binaries now. Please wait..."
                )
                try:
                    response = requests.get(file_url, stream=True, timeout=2)
                    response.raise_for_status()
                except Exception as e:
                    logger.exception(str(e))
                    logger.warning("Downloading Failed. Trying GitHub mirror now!")
                    file_url = "https://raw.githubusercontent.com/abhiTronix/ffmpeg-static-builds/master/windows/ffmpeg-latest-{}-static.zip".format(
                        os_bit, os_bit
                    )
                    response = requests.get(file_url, stream=True, timeout=2)
                    response.raise_for_status()
                total_length = response.headers.get("content-length")
                assert not (
                    total_length is None
                ), "[Helper:ERROR] :: Failed to retrieve files, check your Internet connectivity!"
                bar = tqdm(total=int(total_length), unit="B", unit_scale=True)
                for data in response.iter_content(chunk_size=4096):
                    f.write(data)
                    if len(data) > 0:
                        bar.update(len(data))
                bar.close()
            logger.debug("Extracting executables.")
            with zipfile.ZipFile(file_name, "r") as zip_ref:
                zip_ref.extractall(base_path)
            # perform cleaning
            os.remove(file_name)
            logger.debug("FFmpeg binaries for Windows configured successfully!")
            final_path += file_path
    # return final path
    return final_path


def validate_ffmpeg(path, logging=False):
    """
    ### validate_ffmpeg

    Validate FFmeg Binaries. returns `True` if tests are passed.

    Parameters:
        logging (bool): enables logging for its operations

    **Returns:** A  boolean value, confirming whether tests passed, or not?.
    """
    try:
        # get the FFmpeg version
        version = check_output([path, "-version"])
        firstline = version.split(b"\n")[0]
        version = firstline.split(b" ")[2].strip()
        if logging:
            # log if test are passed
            logger.debug("FFmpeg validity Test Passed!")
            logger.debug(
                "Found valid FFmpeg Version: `{}` installed on this system".format(
                    version
                )
            )
    except Exception as e:
        # log if test are failed
        if logging:
            logger.exception(str(e))
            logger.warning("FFmpeg validity Test Failed!")
        return False
    return True


def check_output(*args, **kwargs):
    """
    ### check_output

    Returns stdin output from subprocess module
    """
    # import libs
    import subprocess as sp
    from subprocess import DEVNULL

    # execute command in subprocess
    process = sp.Popen(stdout=sp.PIPE, stderr=DEVNULL, *args, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()

    # if error occurred raise error
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = args[0]
        error = sp.CalledProcessError(retcode, cmd)
        error.output = output
        raise error
    return output


def generate_auth_certificates(path, overwrite=False, logging=False):
    """ 
    ### generate_auth_certificates

    Auto-Generates, and Auto-validates CURVE ZMQ key-pairs for NetGear API's Secure Mode.
    
    Parameters:
        path (string): path for generating CURVE key-pairs
        overwrite (boolean): overwrite existing key-pairs or not?
        logging (bool): enables logging for its operations

    **Returns:** A valid CURVE key-pairs path as string.
    """
    # import necessary libs
    import shutil
    import zmq.auth

    # check if path corresponds to vidgear only
    if os.path.basename(path) != ".vidgear":
        path = os.path.join(path, ".vidgear")

    # generate keys dir
    keys_dir = os.path.join(path, "keys")
    mkdir_safe(keys_dir, logging=logging)

    # generate separate public and private key dirs
    public_keys_dir = os.path.join(keys_dir, "public_keys")
    secret_keys_dir = os.path.join(keys_dir, "private_keys")

    # check if overwriting is allowed
    if overwrite:
        # delete previous certificates
        for dirs in [public_keys_dir, secret_keys_dir]:
            if os.path.exists(dirs):
                shutil.rmtree(dirs)
            mkdir_safe(dirs, logging=logging)

        # generate new keys
        server_public_file, server_secret_file = zmq.auth.create_certificates(
            keys_dir, "server"
        )
        client_public_file, client_secret_file = zmq.auth.create_certificates(
            keys_dir, "client"
        )

        # move keys to their appropriate directory respectively
        for key_file in os.listdir(keys_dir):
            if key_file.endswith(".key"):
                shutil.move(os.path.join(keys_dir, key_file), public_keys_dir)
            elif key_file.endswith(".key_secret"):
                shutil.move(os.path.join(keys_dir, key_file), secret_keys_dir)
            else:
                # clean redundant keys if present
                redundant_key = os.path.join(keys_dir, key_file)
                if os.path.isfile(redundant_key):
                    os.remove(redundant_key)
    else:
        # otherwise validate available keys
        status_public_keys = validate_auth_keys(public_keys_dir, ".key")
        status_private_keys = validate_auth_keys(secret_keys_dir, ".key_secret")

        # check if all valid keys are found
        if status_private_keys and status_public_keys:
            return (keys_dir, secret_keys_dir, public_keys_dir)

        # check if valid public keys are found
        if not (status_public_keys):
            mkdir_safe(public_keys_dir, logging=logging)

        # check if valid private keys are found
        if not (status_private_keys):
            mkdir_safe(secret_keys_dir, logging=logging)

        # generate new keys
        server_public_file, server_secret_file = zmq.auth.create_certificates(
            keys_dir, "server"
        )
        client_public_file, client_secret_file = zmq.auth.create_certificates(
            keys_dir, "client"
        )

        # move keys to their appropriate directory respectively
        for key_file in os.listdir(keys_dir):
            if key_file.endswith(".key") and not (status_public_keys):
                shutil.move(
                    os.path.join(keys_dir, key_file), os.path.join(public_keys_dir, ".")
                )
            elif key_file.endswith(".key_secret") and not (status_private_keys):
                shutil.move(
                    os.path.join(keys_dir, key_file), os.path.join(secret_keys_dir, ".")
                )
            else:
                # clean redundant keys if present
                redundant_key = os.path.join(keys_dir, key_file)
                if os.path.isfile(redundant_key):
                    os.remove(redundant_key)

    # validate newly generated keys
    status_public_keys = validate_auth_keys(public_keys_dir, ".key")
    status_private_keys = validate_auth_keys(secret_keys_dir, ".key_secret")

    # raise error is validation test fails
    if not (status_private_keys) or not (status_public_keys):
        raise RuntimeError(
            "[Helper:ERROR] :: Unable to generate valid ZMQ authentication certificates at `{}`!".format(
                keys_dir
            )
        )

    # finally return valid key paths
    return (keys_dir, secret_keys_dir, public_keys_dir)


def validate_auth_keys(path, extension):
    """
    ### validate_auth_keys

    Validates, and also maintains generated ZMQ CURVE Key-pairs.

    Parameters:
        path (string): path of generated CURVE key-pairs
        extension (string): type of key-pair to be validated

    **Returns:** A  boolean value, confirming whether tests passed, or not?.
    """
    # check for valid path
    if not (os.path.exists(path)):
        return False

    # check if directory empty
    if not (os.listdir(path)):
        return False

    keys_buffer = []  # stores auth-keys

    # loop over auth-keys
    for key_file in os.listdir(path):
        key = os.path.splitext(key_file)
        # check if valid key is generated
        if key and (key[0] in ["server", "client"]) and (key[1] == extension):
            keys_buffer.append(key_file)  # store it

    # remove invalid keys if found
    if len(keys_buffer) == 1:
        os.remove(os.path.join(path, keys_buffer[0]))

    # return results
    return True if (len(keys_buffer) == 2) else False
