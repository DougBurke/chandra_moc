"""View a Chandra MOC

(technically any MOC but ...)

Based on code from

https://cds-astro.github.io/mocpy/examples/user_documentation.html#smoc-a-k-a-moc-spatial-coverages

"""

import numpy as np

from matplotlib import pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch

import pycrates

import astropy.units as u
from astropy.coordinates import Angle, SkyCoord
from astropy.wcs.utils import skycoord_to_pixel

from mocpy import MOC, WCS


def view_moc(infile: str,
             ra0: float = 83.86661458,
             dec0: float = -69.26975194,
             fov0: float = 2,
             color: str = "red",
             gcolor: str = "black",
             ) -> None:

    moc = MOC.load(infile, format="fits")

    center = SkyCoord(ra0, dec0, unit="deg", frame="icrs")
    fov = fov0 * u.deg
    rot = Angle(0, u.deg)

    fig = plt.figure(figsize=(8, 8))
    with WCS(
            fig,
            fov=fov,
            center=center,
            rotation=rot,
            projection="TAN"
            ) as wcs:

        ax = fig.add_subplot(1, 1, 1, projection=wcs)
        moc.fill(ax=ax, wcs=wcs, alpha=0.5, fill=True, color=color,
                 linewidth=1)
        moc.border(ax=ax, wcs=wcs, alpha=1, color=color)

    plt.xlabel("RA")
    plt.ylabel("Dec")
    plt.grid(color=gcolor, linestyle="dotted", alpha=0.5)
    plt.show()


def view_single(infile: str,
                fovfile: str,
                ra0: float = 83.86661458,
                dec0: float = -69.26975194,
                fov0: float = 2,
                color: str = "red",
                gcolor: str = "black",
                ) -> None:

    moc = MOC.load(infile, format="fits")

    cr = pycrates.read_file(f"{fovfile}[cols eqpos]")
    coords = []
    for pos in cr.get_column("EQPOS").values:
        idx = np.isfinite(pos[0])
        coords.append(pos[:, idx])

    center = SkyCoord(ra0, dec0, unit="deg", frame="icrs")
    fov = fov0 * u.deg
    rot = Angle(0, u.deg)

    fig = plt.figure(figsize=(8, 8))
    with WCS(
            fig,
            fov=fov,
            center=center,
            rotation=rot,
            projection="TAN"
            ) as wcs:

        ax = fig.add_subplot(1, 1, 1, projection=wcs)
        moc.fill(ax=ax, wcs=wcs, alpha=0.5, fill=True, color=color,
                 linewidth=1)
        moc.border(ax=ax, wcs=wcs, alpha=1, color=color)

        # What is the best way to do this?
        for coord in coords:
            skycoord = SkyCoord(coord.T, unit="deg", frame="icrs")
            x, y = skycoord_to_pixel(skycoord, wcs=wcs)
            p = Path(np.vstack((x, y)).T)
            patch = PathPatch(p, color="black", fill=False, alpha=0.75, lw=2)
            ax.add_patch(patch)

    plt.xlabel("RA")
    plt.ylabel("Dec")
    plt.grid(color=gcolor, linestyle="dotted", alpha=0.5)
    plt.show()


"""
if __name__ == "__main__":

    import sys
    if len(sys.argv) != 2:
        sys.stderr.write(f"Usage: {sys.argv[0]} moc\n")
        sys.exit(1)

    view_moc(sys.argv[1])
"""
