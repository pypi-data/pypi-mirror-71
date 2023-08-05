#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the importer functions and classes."""

import os
import yaml
import xarray as xr
import numpy as np
import dask.array as da
from datetime import datetime
from satpy import DatasetID, Scene
from pyresample.geometry import AreaDefinition
from uwsift.workspace.importer import available_satpy_readers, SatpyImporter
from uwsift.common import Info


def test_available_satpy_readers_defaults():
    """Test default behavior of the satpy reader function."""
    readers = available_satpy_readers()
    assert isinstance(readers, list)
    assert len(readers) != 0
    assert isinstance(readers[0], str)  # names


def test_available_satpy_readers_as_dict():
    """Test asking for reader info as dictionaries."""
    readers = available_satpy_readers(as_dict=True)
    assert isinstance(readers, list)
    assert len(readers) != 0
    assert isinstance(readers[0], dict)


def test_available_satpy_readers_no_cache(tmpdir, monkeypatch):
    """Test loading the satpy readers when we know the cache is missing."""
    p = tmpdir.join('satpy_available_readers.yaml')
    monkeypatch.setattr('uwsift.workspace.importer.SATPY_READER_CACHE_FILE', str(p))
    readers = available_satpy_readers()
    assert isinstance(readers, list)
    assert len(readers) != 0
    assert isinstance(readers[0], str)


def test_available_satpy_readers_empty_cache(tmpdir, monkeypatch):
    """Test loading the satpy readers when the cache exists but is empty."""
    p = tmpdir.join('satpy_available_readers.yaml')
    with open(p, 'w') as cfile:
        yaml.dump({}, cfile)
    monkeypatch.setattr('uwsift.workspace.importer.SATPY_READER_CACHE_FILE', str(p))
    readers = available_satpy_readers()
    assert isinstance(readers, list)
    assert len(readers) != 0
    assert isinstance(readers[0], str)


def test_available_satpy_readers_known_cache(tmpdir, monkeypatch):
    """Test loading the satpy readers when the cache exists."""
    p = tmpdir.join('satpy_available_readers.yaml')
    with open(p, 'w') as cfile:
        yaml.dump({}, cfile)
    monkeypatch.setattr('uwsift.workspace.importer.SATPY_READER_CACHE_FILE', str(p))
    monkeypatch.setattr('uwsift.workspace.importer._SATPY_READERS', None)
    # create the cache
    _ = available_satpy_readers()
    mod_time1 = os.stat(p).st_mtime

    # load from the cache
    monkeypatch.setattr('uwsift.workspace.importer._SATPY_READERS', None)
    _ = available_satpy_readers()
    mod_time2 = os.stat(p).st_mtime
    assert mod_time1 == mod_time2, "Cache was not reused"

    # force recreation of the cache
    readers = available_satpy_readers(force_cache_refresh=True)
    mod_time3 = os.stat(p).st_mtime
    assert mod_time3 != mod_time1, "Cache was reused when it should have been recreated"
    assert isinstance(readers, list)
    assert len(readers) != 0
    assert isinstance(readers[0], str)


def _get_data_array_generator(data_arrs):
    """Help mimic what a real Satpy Scene would do."""
    yield from data_arrs


def test_satpy_importer_basic(tmpdir, monkeypatch, mocker):
    """Basic import test using Satpy."""
    db_sess = mocker.MagicMock()
    attrs = {
        'name': 'C01',
        'wavelength': (1.0, 2.0, 3.0),
        'area': AreaDefinition(
            'test', 'test', 'test',
            {
                'proj': 'geos',
                'sweep': 'x',
                'lon_0': -75,
                'h': 35786023,
                'ellps': 'GRS80',
                'units': 'm',
            }, 5, 5,
            (-5434894.885056, -5434894.885056, 5434894.885056, 5434894.885056)
        ),
        'start_time': datetime(2018, 9, 10, 17, 0, 31, 100000),
        'end_time': datetime(2018, 9, 10, 17, 11, 7, 800000),
        'standard_name': 'toa_bidirectional_reflectance',
    }
    data_arr = xr.DataArray(da.from_array(np.empty((5, 5), dtype=np.float64), chunks='auto'),
                            attrs=attrs)
    scn = Scene()
    scn['C01'] = data_arr
    scn.load = mocker.MagicMock()  # don't do anything on load

    imp = SatpyImporter(['/test/file.nc'], tmpdir, db_sess,
                        scene=scn,
                        reader='abi_l1b',
                        dataset_ids=[DatasetID(name='C01')])
    imp.merge_resources()
    assert imp.num_products == 1
    products = list(imp.merge_products())
    assert len(products) == 1
    assert products[0].info[Info.CENTRAL_WAVELENGTH] == 2.0
    assert products[0].info[Info.STANDARD_NAME] == 'toa_bidirectional_reflectance'
