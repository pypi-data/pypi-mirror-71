"""
decomposition.py
================
The core class to define a decomposition.
"""


import logging
import numpy as np
import numpy.linalg as la
import pandas as pd

from sklearn.linear_model import LinearRegression

from .timeseries import TimeSeries
from ..datasets.atlas import Atlas, AtlasError


class Decomposition(TimeSeries):
    """
    Representation of a Decomposition.
    """

    def __init__(self, data=None, filenames=None, sampling_time=None):
        """
        Decomposition Constructor.

        Parameters
        ----------
        data : Array-like
            Preprocessed time-series fMRI data. Can be list of Array-like
        filenames : str
            filenames of :code:`.mat` files containing data. Can be list of :strong:`str`.
        sampling_time : float, optional
            Sampling time of time-series recording.

        Yields
        ------
        data : Array-like
            Time-series raw data
        X : Array-like
            Time-series data from t:1->T
        Y : Array-like
            Time-series data from t:0->T-1
        atlas : nidmd.Atlas
            Cortical Parcellation atlas used for this decomposition
        eig_val : Array-like
            Eigenvalues of the eigen-decomposition of the Auto-regressive matrix
        eig_vec : Array-like
            Eigenvectors of the eigen-decomposition of the Auto-regressive matrix
        eig_idx : Array-like
            Indices for descending order of the eigen-decomposition of the Auto-regressive matrix
        A : Array-like
            Auto-regressive matrix
        Z : Array-like
            Approximation of the activity versus time for each mode
        df : pd.DataFrame
            Pandas DataFrame containing the following columns: mode, value, intensity, damping_time, period, conjugate,
            strength_real, strength_imag, activity
        """
        # Call to super class
        super().__init__(data, filenames, sampling_time)

        self.X = None
        self.Y = None
        self.atlas = None
        self.eig_val = None
        self.eig_vec = None
        self.eig_idx = None
        self.A = None
        self.Z = None
        self.df = None

        if data is not None:
            if isinstance(data, np.ndarray):
                self.add(data)
            else:
                assert isinstance(data, list)
                for d in data:
                    self.add(d)
        elif filenames is not None:
            if isinstance(filenames, str):
                self.extract(filenames)
            else:
                assert isinstance(filenames, list)
                for f in filenames:
                    self.extract(f)

        self.run()

    def add(self, data):
        """
        Add data to Decomposition.

        Parameters
        ----------
        data : Array-like
            Time-series data.
            
        Yields
        ------
        atlas : nidmd.Atlas
            Cortical Parcellation atlas used for this decomposition

        Raises
        ------
        ImportError
            If the import fails.
        """

        # Verify that data is correctly formatted
        try:
            self.atlas = Atlas(data.shape[0])
        except AtlasError:
            raise ImportError('Data import attempt failed. No atlas was attributed.')

        super().add(data)

        logging.info('Data added to Decomposition using {} atlas.'.format(self.atlas))

    def run(self):
        """
        Run Decomposition.

        Returns
        -------
        df : pd.DataFrame
            Pandas DataFrame containing the following columns: mode, value, intensity, damping_time, period, conjugate,
            strength_real, strength_imag, activity
        """

        assert self.data is not None

        # Split data in X and Y
        self.X, self.Y = self.split(self.data)

        # Perform eigendecomposition
        self.eig_val, self.eig_vec, self.eig_idx, self.A = self.get_decomposition(self.X, self.Y)

        # Fetch time course for each mode
        self.Z = la.inv(self.eig_vec) @ self.X

        # Define general data frame
        self.df = self._compute(self.eig_val, self.eig_vec, self.eig_idx, self.Z)

        return self.df

    def _compute(self, val, vec, index, time):
        """
        Compute Decomposition to fetch DataFrame with all relevant info.

        Parameters
        ----------
        val : Array-like
            Eigenvalues of the eigen-decomposition of the AutoRegressive matrix
        vec : Array-like
            Eigenvectors of the eigen-decomposition of the AutoRegressive matrix
        index : Array-like
            Indices that sort the eigenvalues in descending order
        time : Array-like
            Approximation of the activity versus time for each mode

        Returns
        -------
        df : pd.DataFrame
            Pandas DataFrame containing the following columns: mode, value, intensity, damping_time, period, conjugate,
            strength_real, strength_imag, activity
        """

        modes = []

        assert val.shape[0] == vec.shape[0]
        assert vec.shape[0] == vec.shape[1]
        assert index.shape[0] == val.shape[0]
        assert time.shape[0] == val.shape[0]
        assert self.atlas is not None

        if self.sampling_time is None:
            self.sampling_time = 1.0

        order = 1
        idx = 0

        # Sort eigendecomposition and time course matrix
        val_sorted = val[index]
        vec_sorted = vec[:, index]
        time_sorted = time[index, :]

        # Fetch network labels
        labels = list(self.atlas.networks.keys())

        # Fetch indices of networks ROIs
        netidx = [self.atlas.networks[network]['index'] for network in
                  self.atlas.networks]

        # Global Variables contain MATLAB (1->) vs. Python (0->) indices
        netindex = [np.add(np.asarray(netidx[i]), -1) for i in range(len(netidx))]

        while idx < index.shape[0]:

            # Check if mode iterated on is a complex conjugate with the next
            conj = (idx < index.shape[0] - 1) and (val_sorted[idx] == val_sorted[idx + 1].conjugate())

            value = val_sorted[idx]

            strength_real = []
            strength_imag = []

            for n, network in enumerate(labels):
                strength_real.append(np.mean(np.abs(np.real(vec_sorted[netindex[n], idx]))))
                strength_imag.append(np.mean(np.abs(np.imag(vec_sorted[netindex[n], idx]))))

            modes.append(
                dict(
                    mode=order,
                    value=value,
                    intensity=vec_sorted[:, idx],
                    damping_time=(-1 / np.log(np.abs(value))) * self.sampling_time,
                    period=((2 * np.pi) / np.abs(np.angle(value))) * self.sampling_time if conj else np.inf,
                    conjugate=conj,
                    strength_real=strength_real,
                    strength_imag=strength_imag,
                    activity=np.real(time_sorted[idx, :])
                )
            )

            order += 1
            idx += 1 if not conj else 2

        return pd.DataFrame(modes)

    def compute_match(self, other, m):
        """
        Get approximated matched modes for match group with self as a reference.
        Predicts amplification of approximated modes using linear regression.

        Parameters
        ----------
        other : nidmd.Decomposition
            match group
        m : int
            number of modes analyzed for approximation

        Returns
        -------
        modes : pd.DataFrame
            Pandas DataFrame containing the following columns: mode, value, damping_time, period, conjudate
        x : Array-like
            Vector containing absolute value of top 10 approximated eigenvalues of self (by mode matching to self)
        y : Array-like
            Vector containing absolute value of top 10 real eigenvalues of self
        """

        # First the modes should be matched with myself to get regression params
        logging.info('Fetching reference mode matching for regression parameter estimation.')

        borderline = self.eig_val[self.eig_idx][m].conj() == self.eig_val[self.eig_idx][m + 1]
        mm = (m + 1) if borderline else m

        own = self.match_modes(self.X, self.eig_vec[:, self.eig_idx], mm)
        assert np.asarray(own).shape[0] == mm

        # Top 10 modes are used in the dashboard
        reg = LinearRegression().fit(np.abs(own).reshape(-1, 1), np.abs(self.eig_val[self.eig_idx][:mm]).reshape(-1, 1))

        logging.info('Regression parameters estimated.')
        logging.info('Fetching mode estimation for match group.')

        others = self.match_modes(other.X, self.eig_vec[:, self.eig_idx], (m + 1) if borderline else m)

        # complex prediction of top
        others = reg.intercept_ + reg.coef_ * others[:10]
        others = others.flatten()

        logging.info("Matching modes approximation predicted.")

        modes = []

        order = 1
        idx = 0

        while idx < others.shape[0]:

            conj = (idx < others.shape[0] - 1) and (others[idx] == others[idx + 1].conjugate())

            value = others[idx]

            modes.append(
                dict(
                    mode=order,
                    value=value,
                    damping_time=(-1 / np.log(np.abs(value))) * self.sampling_time,
                    period=((2 * np.pi) / np.abs(np.angle(value))) * self.sampling_time if conj else np.inf,
                    conjugate=conj
                )
            )

            order += 1
            idx += 1 if not conj else 2

        return pd.DataFrame(modes), np.abs(own.flatten()), np.abs(self.eig_val[self.eig_idx][:mm])
