import os
import sys

import click
import rich

import ska


# --------------------------------------------------------------------------------
@click.group()
@click.version_option(version=ska.__version__, message="%(version)s")
def cli_ska():
    """CLI for Spectral-Kit for Asteroids."""
    pass


# --------------------------------------------------------------------------------
# Open documentation in the browser
@cli_ska.command()
def docs():
    """Open the ska documentation in browser."""
    import webbrowser

    webbrowser.open("https://space-ska.readthedocs.io/en/latest/", new=2)


# --------------------------------------------------------------------------------
# Status
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
    # Inventory of filters
    if not os.path.isfile(ska.PATH_FILTER_LIST):
        ska.svo.download_filter_list()
    cached_filter_ids, cached_filter_xmls = cache.filter_inventory()

    # ------
    # Inventory of spectra
    cached_spectra, cached_templates = cache.spectra_inventory()

    rich.print(
        f"""\nContents of {ska.PATH_CACHE}:

        {len(cached_filter_xmls)} filters
        {len(cached_spectra)} spectra
        {len(cached_templates)} spectral template files"""
    )

    # Filters: Update or clear
    if cached_filter_xmls:
        if not clear and not update:
            decision = prompt.Prompt.ask(
                "\nUpdate or clear the cached [bright_cyan]filters and filter list[/bright_cyan]?\n"
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
            cache.clear_filters()

        elif update or decision == "2":
            rich.print(cached_filter_ids)
            rich.print("\nDownload filters from SVO Filter Service..")
            cache.update_filters(cached_filter_ids, force=True)

    # Spectra: Update or clear
    if cached_spectra or cached_templates:
        if not clear and not update:
            decision = prompt.Prompt.ask(
                "\nUpdate or clear the cached [bright_cyan]spectra and templates[/bright_cyan]?\n"
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
            rich.print("\nClearing the cached spectra and templates..")
            cache.clear_spectra()

        elif update or decision == "2":
            rich.print("\nUpdate spectra and templates..")
            cache.download_sun_and_vega()
            cache.download_mahlke_taxonomy()


# --------------------------------------------------------------------------------
# Fuzzy search among filters ID
@cli_ska.command()
def id():
    """Fuzzy-search SVO filter index."""

    import shutil
    import subprocess

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
        filt = ska.Filter(choice.strip())
        filt.display_summary()

    except IndexError:  # no choice was made, c-c c-c
        sys.exit()
    return choice


# --------------------------------------------------------------------------------
# Color computation
@cli_ska.command()
@click.argument("file")
@click.argument("filter1")
@click.argument("filter2")
@click.option(
    "--phot_sys", default="Vega", help="Photometric system: Vega (default) | ST | AB"
)
@click.option(
    "--reflectance",
    "-r",
    is_flag=True,
    default=False,
    help="Multiply the input reflectance by Solar spectrum.",
)
def color(file, filter1, filter2, phot_sys, reflectance):
    """Compute the color between two filters"""

    import pandas as pd

    # TBD: interactive selection filters with fzf

    # Load filters
    f_1 = ska.Filter(filter1)
    f_2 = ska.Filter(filter2)

    # Read spectrum
    spectrum = ska.Spectrum(file)

    # Compute color
    if reflectance:
        color = spectrum.reflectance_to_color(f_1, f_2, phot_sys=phot_sys)
        # color = skatools.reflectance_to_color(spectrum, f_1, f_2, phot_sys=phot_sys)
    else:
        color = spectrum.compute_color(f_1, f_2, phot_sys=phot_sys)
        # color = skatools.compute_color(spectrum, f_1, f_2, phot_sys=phot_sys)
    click.echo(f"{color:4.2f}")


# --------------------------------------------------------------------------------
# Solar Colors
@cli_ska.command()
@click.argument("filter1")
@click.argument("filter2")
@click.option(
    "--phot_sys",
    default="Vega",
    help="Photometric system ([green]Vega[/green] | ST | AB)",
)
def solarcolor(filter1, filter2, phot_sys):
    """Compute the color of the Sun between two filters"""

    # Load filters
    f_1 = ska.Filter(filter1)
    f_2 = ska.Filter(filter2)

    # Compute color
    color = f_1.solar_color(f_2, phot_sys=phot_sys)
    click.echo(f"{color:4.2f}")


# --------------------------------------------------------------------------------
# Filter basic information
@cli_ska.command()
@click.argument("filter")
def filter(filter):
    """Display the basic properties of the filter"""

    f = ska.Filter(filter)
    f.display_summary()


# --------------------------------------------------------------------------------
# Plot filter transmission
@cli_ska.command()
@click.argument("filter")
@click.option("--figure", default=None, help="Name of the figure")
@click.option(
    "--black", default=False, is_flag=True, help="Figure with a dark background"
)
def plot_filter(filter, figure, black):
    """Display a simple figure of the transmission of the filter"""

    f = ska.Filter(filter)

    import matplotlib.pyplot as plt

    fig, ax = f.plot_transmission(figure=figure, black=black)

    if not "figure" in locals():
        plt.show()
    elif figure is None:
        plt.show()


# --------------------------------------------------------------------------------
# Plot filter transmission or spectrum (with filters)
@cli_ska.command()
@click.argument("spectrum")
@click.option("--figure", default=None, help="Name of the figure")
@click.option("--filter", "-f", default=None, help="Filter to overplot", multiple=True)
@click.option(
    "--black", default=False, is_flag=True, help="Figure with a dark background"
)
def plot_spectrum(spectrum, filter, figure, black):
    """Display a simple figure of the spectrum"""

    s = ska.Spectrum(spectrum)

    import matplotlib.pyplot as plt

    fig, ax = s.plot(filters=list(filter), figure=figure, black=black)

    if not "figure" in locals():
        plt.show()
    elif figure is None:
        plt.show()
