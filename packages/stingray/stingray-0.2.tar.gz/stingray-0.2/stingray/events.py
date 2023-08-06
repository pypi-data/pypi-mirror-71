"""
Definition of :class:`EventList`.

:class:`EventList` is used to handle photon arrival times.
"""

import copy

import numpy as np
import numpy.random as ra

from .io import read, write
from .utils import simon, assign_value_if_none
from .filters import get_deadtime_mask
from .gti import cross_gtis, append_gtis, check_separate

from .lightcurve import Lightcurve
from stingray.simulator.base import simulate_times

__all__ = ['EventList']


class EventList(object):
    """
    Basic class for event list data. Event lists generally correspond to individual events (e.g. photons)
    recorded by the detector, and their associated properties. For X-ray data where this type commonly occurs,
    events are time stamps of when a photon arrived in the detector, and (optionally) the photon energy associated
    with the event.

    Parameters
    ----------
    time: iterable
        A list or array of time stamps

    Other Parameters
    ----------------
    dt: float
        The time resolution of the events. Only relevant when using events
        to produce light curves with similar bin time.

    energy: iterable
        A list of array of photon energy values

    mjdref : float
        The MJD used as a reference for the time array.

    ncounts: int
        Number of desired data points in event list.

    gtis: ``[[gti0_0, gti0_1], [gti1_0, gti1_1], ...]``
        Good Time Intervals

    pi : integer, numpy.ndarray
        PI channels

    notes : str
        Any useful annotations

    Attributes
    ----------
    time: numpy.ndarray
        The array of event arrival times, in seconds from the reference
        MJD defined in ``mjdref``

    energy: numpy.ndarray
        The array of photon energy values

    ncounts: int
        The number of data points in the event list

    dt: float
        The time resolution of the events. Only relevant when using events
        to produce light curves with similar bin time.

    mjdref : float
        The MJD used as a reference for the time array.

    gtis: ``[[gti0_0, gti0_1], [gti1_0, gti1_1], ...]``
        Good Time Intervals

    pi : integer, numpy.ndarray
        PI channels

    """
    def __init__(self, time=None, energy=None, ncounts=None, mjdref=0, dt=0,
                 notes="", gti=None, pi=None):

        self.energy = None if energy is None else np.array(energy)
        self.notes = notes
        self.dt = dt
        self.mjdref = mjdref
        self.gti = gti
        self.pi = pi
        self.ncounts = ncounts

        if time is not None:
            self.time = np.array(time, dtype=np.longdouble)
            self.ncounts = len(time)
        else:
            self.time = None

        if (time is not None) and (energy is not None):
            if len(time) != len(energy):
                raise ValueError('Lengths of time and energy must be equal.')

    def to_lc(self, dt, tstart=None, tseg=None):
        """
        Convert event list to a :class:`stingray.Lightcurve` object.

        Parameters
        ----------
        dt: float
            Binning time of the light curve

        Other Parameters
        ----------------
        tstart : float
            Start time of the light curve

        tseg: float
            Total duration of light curve

        Returns
        -------
        lc: :class:`stingray.Lightcurve` object
        """

        if tstart is None and self.gti is not None:
            tstart = self.gti[0][0]
            tseg = self.gti[-1][1] - tstart

        return Lightcurve.make_lightcurve(self.time, dt, tstart=tstart,
                                          gti=self.gti, tseg=tseg,
                                          mjdref=self.mjdref)


    def to_lc_list(self, dt):
        """Convert event list to a generator of Lightcurves.

        Parameters
        ----------
        dt: float
            Binning time of the light curves

        Returns
        -------
        lc_gen: generator
            Generates one :class:`stingray.Lightcurve` object for each GTI
        """
        start_times = self.gti[:, 0]
        end_times = self.gti[:, 1]
        tsegs = end_times - start_times

        for st, end, tseg in zip(start_times, end_times, tsegs):
            idx_st = np.searchsorted(self.time, st, side='right')
            idx_end = np.searchsorted(self.time, end, side='left')
            lc = Lightcurve.make_lightcurve(self.time[idx_st:idx_end], dt,
                                            tstart=st,
                                            gti=np.array([[st, end]]),
                                            tseg=tseg,
                                            mjdref=self.mjdref)
            yield lc

    @staticmethod
    def from_lc(lc):
        """
        Create an :class:`EventList` from a :class:`stingray.Lightcurve` object. Note that all
        events in a given time bin will have the same time stamp.

        Parameters
        ----------
        lc: :class:`stingray.Lightcurve` object
            Light curve to use for creation of the event list.

        Returns
        -------
        ev: :class:`EventList` object
            The resulting list of photon arrival times generated from the light curve.
        """

        # Multiply times by number of counts
        times = [[i] * int(j) for i, j in zip(lc.time, lc.counts)]
        # Concatenate all lists
        times = [i for j in times for i in j]

        return EventList(time=times, gti=lc.gti)

    def simulate_times(self, lc, use_spline=False, bin_time=None):
        """
        Randomly assign (simulate) photon arrival times to an :class:`EventList` from a
        :class:`stingray.Lightcurve` object, using the acceptance-rejection method.

        Parameters
        ----------
        lc: :class:`stingray.Lightcurve` object

        Other Parameters
        ----------------
        use_spline : bool
            Approximate the light curve with a spline to avoid binning effects

        bin_time : float
            The bin time of the light curve, if it needs to be specified for
            improved precision

        Returns
        -------
        times : array-like
            Simulated photon arrival times
        """
        self.time = simulate_times(lc, use_spline=use_spline,
                                   bin_time=bin_time)
        self.gti = lc.gti
        self.ncounts = len(self.time)

    def simulate_energies(self, spectrum):
        """
        Assign (simulate) energies to event list from a spectrum.

        Parameters
        ----------
        spectrum: 2-d array or list
            Energies versus corresponding fluxes. The 2-d array or list must
            have energies across the first dimension and fluxes across the
            second one.
        """

        if self.ncounts is None:
            simon("Either set time values or explicity provide counts.")
            return

        if isinstance(spectrum, list) or isinstance(spectrum, np.ndarray):

            energy = np.array(spectrum)[0]
            fluxes = np.array(spectrum)[1]

            if not isinstance(energy, np.ndarray):
                raise IndexError("Spectrum must be a 2-d array or list")

        else:
            raise TypeError("Spectrum must be a 2-d array or list")

        # Create a set of probability values
        prob = fluxes / float(sum(fluxes))

        # Calculate cumulative probability
        cum_prob = np.cumsum(prob)

        # Draw N random numbers between 0 and 1, where N is the size of event
        # list
        R = ra.uniform(0, 1, self.ncounts)

        # Assign energies to events corresponding to the random numbers drawn
        self.energy = \
            np.array([energy[
                np.argwhere(cum_prob == np.min(cum_prob[(cum_prob - r) > 0]))]
                      for r in R])

    def join(self, other):
        """
        Join two :class:`EventList` objects into one.

        If both are empty, an empty :class:`EventList` is returned.

        GTIs are crossed if the event lists are over a common time interval,
        and appended otherwise.

        ``pi`` and ``pha`` remain ``None`` if they are ``None`` in both. Otherwise, 0 is used
        as a default value for the :class:`EventList` where they were None.

        Parameters
        ----------
        other : :class:`EventList` object
            The other :class:`EventList` object which is supposed to be joined with.

        Returns
        -------
        `ev_new` : :class:`EventList` object
            The resulting :class:`EventList` object.
        """

        ev_new = EventList()

        if self.dt != other.dt:
            simon("The time resolution is different."
                  " Using the rougher by default")
            ev_new.dt = np.max([self.dt, other.dt])

        if self.time is None and other.time is None:
            return ev_new

        if (self.time is None):
            simon("One of the event lists you are concatenating is empty.")
            self.time = np.asarray([])

        elif (other.time is None):
            simon("One of the event lists you are concatenating is empty.")
            other.time = np.asarray([])

        # Tolerance for MJDREF:1 microsecond
        if not np.isclose(self.mjdref, other.mjdref, atol=1e-6 / 86400):
            other = other.change_mjdref(self.mjdref)

        ev_new.time = np.concatenate([self.time, other.time])
        order = np.argsort(ev_new.time)
        ev_new.time = ev_new.time[order]

        if (self.pi is None) and (other.pi is None):
            ev_new.pi = None
        elif (self.pi is None) or (other.pi is None):
            self.pi = assign_value_if_none(self.pi, np.zeros_like(self.time))
            other.pi = assign_value_if_none(other.pi,
                                            np.zeros_like(other.time))

        if (self.pi is not None) and (other.pi is not None):
            ev_new.pi = np.concatenate([self.pi, other.pi])
            ev_new.pi = ev_new.pi[order]

        if (self.energy is None) and (other.energy is None):
            ev_new.energy = None
        elif (self.energy is None) or (other.energy is None):
            self.energy = assign_value_if_none(self.energy,
                                               np.zeros_like(self.time))
            other.energy = assign_value_if_none(other.energy,
                                                np.zeros_like(other.time))

        if (self.energy is not None) and (other.energy is not None):
            ev_new.energy = np.concatenate([self.energy, other.energy])
            ev_new.energy = ev_new.energy[order]

        if self.gti is None and other.gti is not None and len(self.time) > 0:
            self.gti = \
                assign_value_if_none(
                    self.gti, np.asarray([[self.time[0] - self.dt / 2,
                                           self.time[-1] + self.dt / 2]]))
        if other.gti is None and self.gti is not None and len(other.time) > 0:
            other.gti = \
                assign_value_if_none(
                    other.gti, np.asarray([[other.time[0] - other.dt / 2,
                                            other.time[-1] + other.dt / 2]]))

        if (self.gti is None) and (other.gti is None):
            ev_new.gti = None

        elif (self.gti is not None) and (other.gti is not None):
            if check_separate(self.gti, other.gti):
                ev_new.gti = append_gtis(self.gti, other.gti)
                simon('GTIs in these two event lists do not overlap at all.'
                      'Merging instead of returning an overlap.')
            else:
                ev_new.gti = cross_gtis([self.gti, other.gti])

        ev_new.mjdref = self.mjdref

        return ev_new

    @staticmethod
    def read(filename, format_='pickle'):
        """
        Read an event list from a file on disk. The file must be either a Python pickle file (not recommended
        for long-term storage), an HDF5 file, an ASCII or a FITS file. The file can have the following
        attributes in the data or meta-data:

        * ``time``:  the time stamps of the photon arrivals
        * ``energy``: the photon energy corresponding to each time stamp
        * ``ncounts``: the total number of photon counts recorded
        * ``mjdref``: a reference time in Modified Julian Date
        * ``dt``: the time resolution of the data
        * ``notes``: other possible meta-data
        * ``gti``: Good Time Intervals
        * ``pi``: some instruments record energies as "Pulse Invariant", an integer number recorded from
          the Pulse Height Amplitude

        Parameters
        ----------
        filename: str
            Name of the :class:`EventList` object to be read.

        format_: str
            Available options are ``pickle``, ``hdf5``, ``ascii`` and `fits``.

        Returns
        -------
        ev: :class:`EventList` object
            The :class:`EventList` object reconstructed from file
        """

        attributes = ['time', 'energy', 'ncounts', 'mjdref', 'dt',
                      'notes', 'gti', 'pi']
        data = read(filename, format_, cols=attributes)

        if format_ == 'ascii':
            time = np.array(data.columns[0])
            return EventList(time=time)

        elif format_ == 'hdf5' or format_ == 'fits':
            keys = data.keys()
            values = []

            if format_ == 'fits':
                attributes = [a.upper() for a in attributes]

            for attribute in attributes:
                if attribute in keys:
                    values.append(data[attribute])

                else:
                    values.append(None)

            return EventList(time=values[0], energy=values[1],
                             ncounts=values[2], mjdref=values[3], dt=values[4],
                             notes=values[5], gti=values[6], pi=values[7])

        elif format_ == 'pickle':
            return data

        else:
            raise KeyError("Format not understood.")

    def write(self, filename, format_='pickle'):
        """
        Write an :class:`EventList` object to file. Possible file formats are ``pickle``, ``hdf5``, ``ascii``
        or ``fits``.

        Parameters
        ----------
        filename: str
            Name and path of the file to save the event list to..

        format_: str
            The file format to store the data in.
            Available options are ``pickle``, ``hdf5``, ``ascii``, ``fits``
        """

        if format_ == 'ascii':
            write(np.array([self.time]).T, filename, format_, fmt=["%s"])

        elif format_ == 'pickle':
            write(self, filename, format_)

        elif format_ == 'hdf5':
            write(self, filename, format_)

        elif format_ == 'fits':
            write(self, filename, format_, tnames=['EVENTS', 'GTI'],
                  colsassign={'gti': 'GTI'})

        else:
            raise KeyError("Format not understood.")

    def apply_deadtime(self, deadtime, inplace=False, **kwargs):
        """Apply deadtime filter to this event list.

        Additional arguments in ``kwargs`` are passed to `get_deadtime_mask`

        Parameters
        ----------
        deadtime : float
            Value of dead time to apply to data
        inplace : bool, default False
            If True, apply the deadtime to the current event list. Otherwise,
            return a new event list.

        Returns
        -------
        new_event_list : `EventList` object
            Filtered event list. if `inplace` is True, this is the input object
            filtered for deadtime, otherwise this is a new object.
        additional_output : object
            Only returned if `return_all` is True. See `get_deadtime_mask` for
            more details.

        Examples
        --------
        >>> events = np.array([1, 1.05, 1.07, 1.08, 1.1, 2, 2.2, 3, 3.1, 3.2])
        >>> events = EventList(events)
        >>> events.pi=np.array([1, 2, 2, 2, 2, 1, 1, 1, 2, 1])
        >>> events.energy=np.array([1, 2, 2, 2, 2, 1, 1, 1, 2, 1])
        >>> events.mjdref = 10
        >>> filt_events, retval = events.apply_deadtime(0.11, inplace=False,
        ...                                             verbose=False,
        ...                                             return_all=True)
        >>> filt_events is events
        False
        >>> expected = np.array([1, 2, 2.2, 3, 3.2])
        >>> np.all(filt_events.time == expected)
        True
        >>> np.all(filt_events.pi == 1)
        True
        >>> np.all(filt_events.energy == 1)
        True
        >>> np.all(events.pi == 1)
        False
        >>> filt_events = events.apply_deadtime(0.11, inplace=True,
        ...                                     verbose=False)
        >>> filt_events is events
        True
        """
        if inplace:
            new_ev = self
        else:
            new_ev = copy.deepcopy(self)

        local_retall = kwargs.pop('return_all', False)

        mask, retall = get_deadtime_mask(new_ev.time, deadtime,
                                         return_all=True,
                                         **kwargs)

        for attr in 'time', 'energy', 'pi':
            if hasattr(new_ev, attr):
                setattr(new_ev, attr, getattr(new_ev, attr)[mask])

        if local_retall:
            new_ev = [new_ev, retall]

        return new_ev

    def change_mjdref(self, new_mjdref):
        """Change the MJD reference time (MJDREF) of the light curve.

        Times will be now referred to this new MJDREF

        Parameters
        ----------
        new_mjdref : float
            New MJDREF

        Returns
        -------
        new_lc : :class:`EventList` object
            The new LC shifted by MJDREF
        """
        time_shift = (self.mjdref - new_mjdref) * 86400

        new_ev = self.shift(time_shift)
        new_ev.mjdref = new_mjdref
        return new_ev

    def shift(self, time_shift):
        """
        Shift the events and the GTIs in time.

        Parameters
        ----------
        time_shift: float
            The time interval by which the light curve will be shifted (in
            the same units as the time array in :class:`Lightcurve`

        Returns
        -------
        new_ev : lightcurve.Lightcurve object
            The new event list shifted by ``time_shift``

        """
        new_ev = copy.deepcopy(self)
        new_ev.time = new_ev.time + time_shift
        new_ev.gti = new_ev.gti + time_shift

        return new_ev
