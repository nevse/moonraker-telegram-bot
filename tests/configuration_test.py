import pathlib

import pytest

from bot.configuration import ConfigWrapper  # type: ignore

CONFIG_PATH = "tests/resources/telegram.conf"
CONFIG_MINIMAL_PATH = "tests/resources/telegram_minimal.conf"
CONFIG_TEMPLATE_PATH = "scripts/base_install_template"
CONFIG_WITH_SECRETS_PATH = "tests/resources/telegram_secrets.conf"
CONFIG_STARTUP_PATH = "tests/resources/telegram_startup.conf"


def test_template_config_has_no_errors():
    config_path = pathlib.Path(CONFIG_TEMPLATE_PATH).absolute().as_posix()
    assert ConfigWrapper(config_path).configuration_errors == ""


def test_minimal_config_has_no_errors():
    config_path = pathlib.Path(CONFIG_MINIMAL_PATH).absolute().as_posix()
    assert ConfigWrapper(config_path).configuration_errors == ""


@pytest.fixture
def config_secrets_helper():
    config_path = pathlib.Path(CONFIG_WITH_SECRETS_PATH).absolute().as_posix()
    return ConfigWrapper(config_path)


def test_config_with_secrets_has_no_errors(config_secrets_helper):
    assert config_secrets_helper.configuration_errors == ""


def test_config_with_secrets_is_valid(config_secrets_helper):
    assert config_secrets_helper.secrets.chat_id == 1661233333 and config_secrets_helper.secrets.token == "23423423334:sdfgsdfg-doroasd"


@pytest.fixture
def config_helper():
    config_path = pathlib.Path(CONFIG_PATH).absolute().as_posix()
    return ConfigWrapper(config_path)


def test_config_has_no_errors(config_helper):
    assert config_helper.configuration_errors == ""


def test_config_bot_is_valid(config_helper):
    assert config_helper.secrets.chat_id == 16612341234 and config_helper.secrets.token == "23423423334:sdfgsdfg-dfgdfgsdfg"


# --- greeting_message_extra ---

def test_greeting_message_extra_default(config_helper):
    assert config_helper.telegram_ui.greeting_message_extra == ""


def test_send_startup_photo_default(config_helper):
    assert config_helper.telegram_ui.send_startup_photo is False


# --- camera_snapshot_urls ---

def test_camera_snapshot_url_derived_from_stream(config_helper):
    urls = config_helper.camera_snapshot_urls
    assert len(urls) == 1
    assert urls[0] == "http://192.168.1.56::8110/?action=snapshot"


def test_camera_snapshot_urls_empty_when_no_camera_section():
    config_path = pathlib.Path(CONFIG_MINIMAL_PATH).absolute().as_posix()
    config = ConfigWrapper(config_path)
    assert config.camera_snapshot_urls == []


# --- startup config fixture ---

@pytest.fixture
def startup_config():
    config_path = pathlib.Path(CONFIG_STARTUP_PATH).absolute().as_posix()
    return ConfigWrapper(config_path)


def test_startup_config_has_no_errors(startup_config):
    assert startup_config.configuration_errors == ""


def test_send_startup_photo_enabled(startup_config):
    assert startup_config.telegram_ui.send_startup_photo is True


def test_greeting_message_extra_value(startup_config):
    extra = startup_config.telegram_ui.greeting_message_extra
    assert extra.startswith("<b>Printer access:</b>")
    assert "Local network" in extra
    assert "VPN" in extra


def test_greeting_message_extra_no_leading_whitespace(startup_config):
    for line in startup_config.telegram_ui.greeting_message_extra.splitlines():
        assert line == line.strip()


def test_camera_snapshot_urls_multiple_cameras(startup_config):
    urls = startup_config.camera_snapshot_urls
    assert len(urls) == 2


def test_camera_snapshot_url_derived_from_host(startup_config):
    urls = startup_config.camera_snapshot_urls
    assert "http://192.168.1.56:8080/?action=snapshot" in urls


def test_camera_snapshot_url_explicit_host_snapshot(startup_config):
    urls = startup_config.camera_snapshot_urls
    assert "http://192.168.1.56:8081/?action=snapshot" in urls
