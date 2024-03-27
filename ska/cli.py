import shutil
import subprocess
import sys

import click
import rich

import ska
import ska.tools as skatools

import pandas as pd

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




@cli_ska.command()
@click.argument('file')
@click.argument('filter1')
@click.argument('filter2')
@click.option('--phot_sys', default='AB', help='Photometric system (Vega | ST | AB)')
def color(file, filter1, filter2, phot_sys):
    """Compute the color between two filters"""

    f_1 = ska.Filter( filter1 )
    f_2 = ska.Filter( filter2 )

    spectrum = pd.read_csv( file )
    color = skatools.compute_color( spectrum, f_1, f_2, phot_sys=phot_sys)
    #click.echo(f"{ file} {filter1} {filter2} {phot_sys}")
    click.echo(f"{color:4.2f}")
