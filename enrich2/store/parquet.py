#  Copyright 2016-2017 Alan F Rubin, Daniel C Esposito
#
#  This file is part of Enrich2.
#
#  Enrich2 is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Enrich2 is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Enrich2.  If not, see <http://www.gnu.org/licenses/>.

import pandas as pd
import dask.dataframe as dd
import numpy as np
import json
from typing import Union, Sequence, Mapping, Any, Dict
from os import PathLike
from enrich2.store.interface import StoreInterface


class ParquetStore(StoreInterface):
    """
    Implementation for using Apache Parquet as the storage backend.

    Parameters
    ----------
    path: str
        Path to a new or existing directory for the parquet files.

    Attributes
    ----------

    See Also
    --------

    """

    file_extensions = ("",)

    def __init__(self, path: Union[PathLike, str]) -> None:
        super().__init__(path)

        self._key_file = self.path.joinpath("dataset_keys.json")
        if self.path.is_dir():
            if self._key_file.exists():
                with self._key_file.open() as handle:
                    # TODO: validation for the json key file
                    self._keys.extend(json.load(handle))
            else:
                raise ValueError(f"unable to read keys for {self.__class__.__name__}")
        else:
            # will raise a FileExistsError if the path exists
            self.path.mkdir(parents=True)

    def _write_key_file(self) -> None:
        """Writes the contents of self.keys() to the key file.

        This is required after put() and drop() operations to keep the keys in
        the file in sync with what's in the data structure.

        Returns
        -------
        None

        """
        with self._key_file.open(mode="w") as handle:
            json.dump(self.keys(), handle)

    def put(self, key: str, value: Union[dd.DataFrame, pd.DataFrame]) -> None:
        """
        Stores a data frame in the HDF file under the given key.

        Parameters
        ----------
        key:  str
            Name of the data frame in the store.
        value : Union[dd.DataFrame, pd.DataFrame]
            The data frame to store.

        """
        if key not in self.keys():
            self._keys.append(key)
            self._write_key_file()
        value.to_parquet(self.path.joinpath(key))

    def drop(self, key: str) -> None:
        """
        Remove a table and its data from the store.

        Note that this operation may not reduce the HDF5 file size on disk
        until the file is repacked using ptrepack or a similar utility.  # TODO check ptrepack reference

        Parameters
        ----------
        key: str
            Name of the table to remove.

        Raises
        ------
        KeyError
            If the key is not in the store.

        """
        if key not in self.keys():
            raise KeyError(f"{self.__class__.__name__} does not contain key '{key}'")
        else:
            with pd.HDFStore(self.path) as store:
                del store[key]
            self._keys.remove(key)
            self._write_key_file()

    def get(self, key: str) -> dd.DataFrame:
        """
        Returns the data at key as a dask DataFrame.

        Parameters
        ----------
        key: str
            The key to access.

        Returns
        -------
        :py:class:`~dask.dataframe.DataFrame`
            The data frame stored under key.

        Raises
        ------
        KeyError
            If the key is not in the store.

        """
        if key not in self.keys():
            raise KeyError(f"{self.__class__.__name__} does not contain key '{key}'")
        else:
            return dd.read_parquet(self.path.joinpath(key))

    def get_column(self, key: str, column: str) -> np.ndarray:
        """
        Returns the values of a single column of the data frame stored under key.

        Parameters
        ----------
        key: str
            The key to access.
        column: name
            The name of a single column in the data

        Returns
        -------
        :py:class:`~numpy.ndarray`
            The column's values.

        Raises
        ------
        KeyError
            If the key is not in the store.

        """
        if key not in self.keys():
            raise KeyError(f"{self.__class__.__name__} does not contain key '{key}'")
        else:
            return (
                dd.read_parquet(self.path.joinpath(key), columns=[column]).compute().values.flatten()
            )

    def get_with_merge(self, keys: Sequence[str]) -> dd.DataFrame:
        """
        Returns a single data frame that is the result of merging multiple keys
        on the data frame indices.

        This performs an inner join, meaning that the index will contain only
        those values that are shared across all keys. The order of items in the
        index will be the same as in the first of the keys.

        Passing in keys that share column names will result in columns
        being re-labeled in the result.

        Parameters
        ----------
        keys: Sequence[str]
            The keys to access and merge.

        Returns
        -------
        dd.DataFrame
            Result of combining the data frames.

        Raises
        ------
        KeyError
            If any key is not in the store.
        ValueError
            If the resulting data frame is empty (no shared index values).

        """
        for key in keys:
            if key not in self.keys():
                raise KeyError(
                    f"{self.__class__.__name__} does not contain key '{key}'"
                )
        result = None
        for key in keys:
            if result is None:
                result = self.get(key)
            else:
                result = result.merge(
                    self.get(key), how="inner", left_index=True, right_index=True
                )
        if result.shape[0].compute() == 0:
            raise ValueError(f"{self.__class__.__name__} merge result is empty")
        return result

    def set_metadata(
        self, key: str, metadata: Mapping[str, Any], update: bool = False
    ) -> None:
        """
        Sets the metadata of the data frame located at key with the supplied
        key-value pairs.

        Parameters
        ----------
        key: str
            The key to access.
        metadata : Mapping[str, Any]
            The metadata to store.
        update : bool
            Update the metadata instead of replacing it. Default False.

        Raises
        ------
        KeyError
            If any key is not in the store.
        TypeError
            If the metadata is not a Mapping.

        """
        if key not in self.keys():
            raise KeyError(f"{self.__class__.__name__} does not contain key '{key}'")
        if not isinstance(metadata, Mapping):
            raise TypeError(f"{self.__class__.__name__} must be a Mapping")

        if update:
            existing = self.get_metadata(key)
            metadata.update(existing)
        with pd.HDFStore(self.path) as store:
            store.get_storer(key).attrs[self.metadata_key] = metadata

    def get_metadata(self, key: str) -> Dict[str, Any]:
        """
        Returns the metadata of the data frame located at key.
        
        Parameters
        ----------
        key: str
            The key to access.

        Returns
        -------
        Dict[str, Any]
            The metadata.

        Raises
        ------
        KeyError
            If the key is not in the store.

        """
        if key not in self.keys():
            raise KeyError(f"{self.__class__.__name__} does not contain key '{key}'")

        with pd.HDFStore(self.path) as store:
            try:
                metadata = store.get_storer(key).attrs[self.metadata_key]
            except KeyError as e:
                if str(e).startswith(
                    f"\"Attribute ('{self.metadata_key}') does not exist in node"
                ):
                    metadata = {}
                else:
                    raise e
        return metadata