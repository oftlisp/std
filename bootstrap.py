#!/usr/bin/env python3

from argparse import ArgumentParser
import filecmp
from os import chdir, makedirs, remove
from os.path import abspath, isdir, join, realpath
import shutil
import subprocess
import tarfile
from tempfile import NamedTemporaryFile


def command(*cmd, redirect=None):
    if redirect is None:
        subprocess.check_call(cmd)
    else:
        with NamedTemporaryFile() as f:
            subprocess.check_call(cmd, stdout=f)
            d = realpath(abspath(join(redirect, "..")))
            if not isdir(d):
                makedirs(d)
            shutil.copy(f.name, redirect)


def print_cyan(fmt, *args, indent=0):
    from sys import stdout
    stdout.write(" " * indent)
    stdout.write("\x1b[1;36m")
    print(fmt.format(*args), end="")
    stdout.write("\x1b[0m\n")



# These get filled in below
oftb_exec = None
oftb_dir = None
std_dir = None


def bootstrap():
    print_cyan("oftb-macro-expander oftc")
    macro_expander_path = join(oftb_dir,
                               "macro-expander/build/oftb-macro-expander.ofta")
    command(oftb_exec, "-v", "interpret", macro_expander_path, std_dir, ".",
            "oftc", redirect="build/oftc.ofta")

    print_cyan("oftc oftc")
    command(oftb_exec, "-v", "interpret", "build/oftc.ofta", "--", "--std",
            std_dir, ".", "oftc")

    print_cyan("oftc oftc")
    command("build/oftc", "--std", std_dir, ".", "oftc", "-o", "build/oftc-2")

    if not filecmp.cmp("build/oftc", "build/oftc-2"):
        raise Exception("oftc is not idempotent")
    remove("build/oftc-2")


def make_archive():
    with tarfile.open("oftc.tar.gz", "w:gz") as tar:
        tar.add("build/oftc", arcname="oftc")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--oftb-dir", default="../oftb")
    parser.add_argument("--std-dir", default=".")
    parser.add_argument("--use-system-oftb", action="store_true")
    args = parser.parse_args()

    if args.use_system_oftb:
        oftb_exec = "oftb"
    else:
        oftb_exec = join(args.oftb_dir, "target/release/oftb")
    oftb_dir = abspath(args.oftb_dir)
    std_dir = abspath(args.std_dir)

    chdir(abspath(join(__file__, "..")))

    bootstrap()
    make_archive()
