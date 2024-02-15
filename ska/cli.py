import shutil
import subprocess
import sys

import click
import rich

import ska


@click.group()
@click.version_option(version=ska.__version__, message="%(version)s")
def cli_ska():
    """CLI for Spectral-Kit for Asteroids."""
    pass


@cli_ska.command()
def filter():
    """Fuzzy-search SVO filter index."""

    PATH_EXECUTABLE = shutil.which("fzf")

    if PATH_EXECUTABLE is None:
        rich.print(
            "Interactive selection is not possible as the fzf tool is not installed.\n"
        )
        sys.exit()

    FZF_OPTIONS = []

    # Open fzf subprocess
    process = subprocess.Popen(
        [shutil.which("fzf"), *FZF_OPTIONS],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=None,
    )

    for filter in ska.svo.FILTERS:
        line = filter.encode(sys.getdefaultencoding()) + b"\n"
        process.stdin.write(line)
        process.stdin.flush()

    # Run process and wait for user selection
    process.stdin.close()
    process.wait()

    # Extract selected line
    try:
        choice = [line for line in process.stdout][0].decode()
    except IndexError:  # no choice was made, c-c c-c
        sys.exit()
    return choice
