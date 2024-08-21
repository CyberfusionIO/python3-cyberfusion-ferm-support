import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from pytest_mock import MockerFixture

from cyberfusion.Common import get_tmp_file
from cyberfusion.FermSupport.configuration import Configuration


@pytest.fixture(autouse=True)
def systemd_restart_mock(mocker: MockerFixture) -> None:
    mocker.patch(
        "cyberfusion.SystemdSupport.units.Unit.restart", return_value=None
    )


@pytest.fixture
def configuration() -> Configuration:
    return Configuration(path=get_tmp_file())


def pytest_addoption(parser: Parser) -> None:
    parser.addoption("--ci", action="store_true", default=False)


def pytest_configure(config: Config) -> None:
    config.addinivalue_line("markers", "ci")


def pytest_collection_modifyitems(config: Config, items: list) -> None:
    if config.getoption("--ci"):
        return

    for item in items:
        if "ci" not in item.keywords:
            continue

        item.add_marker(
            pytest.mark.skip(reason="CI only. ferm is only available in CI.")
        )
