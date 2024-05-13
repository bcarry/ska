
import os
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
@click.option(
    "--clear",
    "-c",
    help="Clear cached filters and update the filter list.",
    is_flag=True,
)
@click.option(
    "--update", "-u", help="Update cached filters and filter list.", is_flag=True
)
def status(clear, update):
    """Echo the status of the cached filters."""
    from rich import prompt

    from ska import cache

    # ------
    # Check filter list
    if not os.path.isfile(ska.PATH_FILTER_LIST):
        ska.svo.download_filter_list()

    # ------
    # Echo inventory
    cached_ids, cached_xmls = cache.take_inventory()
    #date_index = index.get_modification_date()

    rich.print(
        f"""\nContents of {ska.PATH_CACHE}:

        {len(cached_xmls)} filters\n"""
    )
        #Index updated on:  {date_index}\n"""

    # Update or clear
    if cached_xmls:
        if not clear and not update:
            decision = prompt.Prompt.ask(
                "Update or clear the cached filters and filter list?\n"
                "[blue][0][/blue] No "
                "[blue][1][/blue] Clear cache "
                "[blue][2][/blue] Update data ",
                choices=["0", "1", "2"],
                show_choices=False,
                default="0",
            )
        else:
            decision = "none"


        if clear or decision == "1":
            rich.print("\nClearing the cached filters and filter list..")
            cache.clear()

        elif update or decision == "2":
            rich.print(cached_ids)
            rich.print("\nDownload filters from SVO Filter Service..")
            cache.update_filters(cached_ids)


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

    FILTERS = ska.svo.load_filter_list()
    for filter in FILTERS:
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
@click.argument("file")
@click.argument("filter1")
@click.argument("filter2")
@click.option("--phot_sys", default="AB", help="Photometric system (Vega | ST | AB)")
def color(file, filter1, filter2, phot_sys):
    """Compute the color between two filters"""


    # TBD: interactive selection filters with fzf

    f_1 = ska.Filter(filter1)
    f_2 = ska.Filter(filter2)

    spectrum = pd.read_csv(file)
    color = skatools.compute_color(spectrum, f_1, f_2, phot_sys=phot_sys)
    click.echo(f"{color:4.2f}")
