import pytest
from src.data_classes.NOAA import MagnetosphereDB

def test_clear():
    db = MagnetosphereDB(db='TEST', table='MAGNETOSPHERE')
    dummy_data = ('1/2/3 01:02', 0.1, 0.2, 0.3, 0.4, 0.5, 0.6)
    db.write_many_rows(dummy_data)
    assert db.get_num_rows() == 1
    db.clear_table()
    assert db.get_num_rows() == 0

def test_create_table():
    db = MagnetosphereDB(db='TEST', table='MAGNETOSPHERE')
    assert db.get_num_rows() == 0

def test_execute_write_one():
    db = MagnetosphereDB(db='TEST', table='MAGNETOSPHERE')
    dummy_data = ('1/2/3 01:02', 0.1, 0.2, 0.3, 0.4, 0.5, 0.6)
    db.write_many_rows(dummy_data)
    assert db.get_num_rows() == 1



