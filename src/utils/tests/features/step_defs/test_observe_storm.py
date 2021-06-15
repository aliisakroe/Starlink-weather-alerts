'''This file is a WIP and is not expected to run in this state'''

from pytest_bdd import scenario, given, when, then
from src.data_classes.NOAA import MagnetosphereData, MagnetosphereDB, PlasmaData, Storm
from src.data_classes.Starlink import Constellation

@scenario('Magnetosphere Storm Event')
def test_storm():
    pass

@given('Given the Intensity of solar wind has been logged')
def negative_bx_gsm():
    assert MagnetosphereData().possible_storm(-2.5) == True

@given('And Given the Magnetosphere bx_gsm coordinate has been negative')
def negative_bx_gsm():
    assert MagnetosphereData().possible_storm(-2.5) == True

@then('At least 1 storm existed in the last interval')
def register_storm():
     Storm()

@then('Then the storm database is not empty')
def check_storm_database():
    db = MagnetosphereDB(db='TEST', table='OBSERVE_STORM')
    assert db.get_num_rows() > 0

@then('And I log the intensity of the storm for future research')
def log_storm_intensity():
    PlasmaData().get_radiation_drag()

@then('And I alert all satellites to engage their thrusters')
def alert_constellation():
    Constellation().broadcast_alert()
