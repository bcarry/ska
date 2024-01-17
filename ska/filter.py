from pathlib import Path

from astropy.io.votable import parse
import pandas as pd

import ska


class Filter:
    def __init__(self, id):
        """Load a filter.

        Parameters
        ----------
        id : str
            The filter unique ID (see SVO filter service)
        """

        self.id = id
        self.path = Path(ska.PATH_CACHE) / f"{self.id}.xml"

        if not self.path.is_file():
            ska.svo.download_filter(self.id)

        # Read, parse, return VOTable
        VOFilter = parse(self.path)
        data = pd.DataFrame(data=VOFilter.get_first_table().array.data)

        self.wave = data.Wavelength
        self.trans = data.Transmission
