import os

import pytest
from pytest_mock import MockerFixture

from cyberfusion.FermSupport.configuration import Configuration
from cyberfusion.FermSupport.exceptions import ConfigInvalidError
from cyberfusion.SystemdSupport.units import Unit


def test_configuration_save_not_exists_creates(
    mocker: MockerFixture, configuration: Configuration
):
    mocker.patch(
        "cyberfusion.FermSupport.configuration.Configuration.is_valid",
        new=mocker.PropertyMock(return_value=True),
    )

    os.unlink(configuration.path)

    configuration.save()

    assert os.path.isfile(configuration.path)


def test_configuration_save_not_changed_result(
    mocker: MockerFixture,
    configuration: Configuration,
) -> None:
    mocker.patch(
        "cyberfusion.FermSupport.configuration.Configuration.is_valid",
        new=mocker.PropertyMock(return_value=True),
    )

    with open(configuration.path, "w") as f:
        f.write(str(configuration))

    assert configuration.save() is False


def test_configuration_save_changed_result(
    mocker: MockerFixture,
    configuration: Configuration,
) -> None:
    mocker.patch(
        "cyberfusion.FermSupport.configuration.Configuration.is_valid",
        new=mocker.PropertyMock(return_value=True),
    )

    assert open(configuration.path, "r").read() != str(configuration)

    assert configuration.save() is True


def test_configuration_save_changed_calls_restart(
    mocker: MockerFixture, configuration: Configuration
) -> None:
    mocker.patch(
        "cyberfusion.FermSupport.configuration.Configuration.is_valid",
        new=mocker.PropertyMock(return_value=True),
    )

    spy_unit_init = mocker.spy(Unit, "__init__")
    spy_unit_restart = mocker.spy(Unit, "restart")

    assert configuration.save() is True

    spy_unit_init.assert_called_once_with(mocker.ANY, f"ferm.{Unit.SUFFIX_SERVICE}")
    spy_unit_restart.assert_called_once_with()


def test_configuration_save_changed_not_valid_raises(
    mocker: MockerFixture, configuration: Configuration
) -> None:
    mocker.patch(
        "cyberfusion.FermSupport.configuration.Configuration.is_valid",
        new=mocker.PropertyMock(return_value=False),
    )

    with pytest.raises(ConfigInvalidError):
        configuration.save()


@pytest.mark.ci
def test_configuration_not_valid(configuration: Configuration) -> None:
    with open(configuration.path, "w") as f:
        f.write("bogus")

    assert configuration.is_valid is False


@pytest.mark.ci
def test_configuration_valid(configuration: Configuration) -> None:
    with open(configuration.path, "w") as f:
        f.write("")

    assert configuration.is_valid is True
