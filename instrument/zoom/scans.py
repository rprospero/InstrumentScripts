"""Default class and utilities for Zoom

All the scanning code specific to the Zoom instrument is
contained in this module

"""
from __future__ import print_function
from genie.scans.scans.defaults import Defaults
from genie.scans.scans.detector import dae_periods
from general.scans.scans.genie import g
from genie.scans.scans.motion import populate
from genie.scans.scans.monoid import Sum
from genie.scans.scans.util import make_scan

def _trans_mode():
    """Setup the instrument for a simple transmission measurement."""
    setup_dae_transmission()
    g.set_pv("IN:ZOOM:VACUUM:MONITOR:4:INSERT","INSERT")
    g.waitfor_move()


def zoom_monitor(spectrum):
    """A generating function for detectors for monitor spectra"""
    @dae_periods(_trans_mode)
    def monitor(**kwargs):
        """A simple detector for monitor number {}""".format(spectrum)
        local_kwargs = {}
        if "frames" in kwargs:
            local_kwargs["frames"] = kwargs["frames"] + g.get_frames()
        if "uamps" in kwargs:
            local_kwargs["uamps"] = kwargs["uamps"] + g.get_uamps()
        g.resume()

        g.waitfor(**local_kwargs)
        g.pause()
        temp = sum(g.get_spectrum(spectrum, period=g.get_period())["signal"])*100
        base = sum(g.get_spectrum(1, period=g.get_period())["signal"])*100
        if spectrum == 1:
            return Average(base)
        return Average(temp, count=base)
    return monitor


class Zoom(Defaults):
    """
    This class represents the default functions for the Zoom instrument.
    """

    detector = zoom_monitor(4)

    @staticmethod
    def log_file():
        from datetime import datetime
        now = datetime.now()
        return "U:/zoom_scan_{}_{}_{}_{}_{}_{}.dat".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second)

    def __repr__(self):
        return "Zoom()"


_zm = Zoom()
scan = local_wrapper(_lm, "scan")
ascan = local_wrapper(_lm, "ascan")
dscan = local_wrapper(_lm, "dscan")
rscan = local_wrapper(_lm, "rscan")
populate()
monitor1 = zoom_monitor(1)
monitor2 = zoom_monitor(2)
monitor3 = zoom_monitor(3)
monitor4 = zoom_monitor(4)
