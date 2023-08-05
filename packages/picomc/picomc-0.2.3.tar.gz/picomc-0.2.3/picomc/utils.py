import collections
import hashlib
import json
import os
import subprocess
import sys
from functools import partial
from os.path import expanduser, join
from types import SimpleNamespace

from picomc.env import get_filepath
from picomc.javainfo import java_info, java_version
from picomc.logging import logger


class cached_property(object):
    def __init__(self, fn):
        self.fn = fn

    def __get__(self, inst, cls):
        if inst is None:
            return self
        r = self.fn(inst)
        setattr(inst, self.fn.__name__, r)
        return r


def join_classpath(*cp):
    return os.pathsep.join(cp)


def write_profiles_dummy():
    # This file makes the forge installer happy.
    fname = get_filepath("launcher_profiles.json")
    with open(fname, "w") as fd:
        fd.write(r'{"profiles":{}}')


def file_verify_relative(path, sha1):
    abspath = get_filepath(path)
    return os.path.isfile(abspath) and file_sha1(abspath) == sha1


def file_sha1(filename):
    h = hashlib.sha1()
    with open(filename, "rb", buffering=0) as f:
        for b in iter(partial(f.read, 128 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def die(mesg, code=1):
    logger.error(mesg)
    sys.exit(code)


def assert_java(java):
    try:
        jinfo = java_info(java)
        jver = java_version(java)
        badjv = False
        if jinfo:
            badjv = not jinfo["java.version"].startswith("1.8.0")
            bitness = jinfo.get("sun.arch.data.model", None)
            if bitness and bitness != "64":
                logger.warn(
                    "You are not using 64-bit java. Things will probably not work."
                )
        else:
            badjv = "1.8.0_" not in jver

        logger.info("Using java version: {}".format(jver))

        if badjv:
            logger.warn(
                "Minecraft uses java 1.8.0 by default."
                " You may experience issues, especially with older versions of Minecraft."
            )

        return jinfo

    except FileNotFoundError:
        die(
            "Could not execute java at: {}. Have you installed it? Is it in yout PATH?".format(
                java
            )
        )
