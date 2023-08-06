# systemctl-mqtt - MQTT client triggering & reporting shutdown on systemd-based systems
#
# Copyright (C) 2020 Fabian Peter Hammerle <fabian@hammerle.me>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import typing
import unittest.mock

import pytest

import systemctl_mqtt


@pytest.mark.parametrize(
    (
        "argv",
        "expected_mqtt_host",
        "expected_mqtt_port",
        "expected_username",
        "expected_password",
        "expected_topic_prefix",
    ),
    [
        (
            ["", "--mqtt-host", "mqtt-broker.local"],
            "mqtt-broker.local",
            8883,
            None,
            None,
            None,
        ),
        (
            ["", "--mqtt-host", "mqtt-broker.local", "--mqtt-port", "8883"],
            "mqtt-broker.local",
            8883,
            None,
            None,
            None,
        ),
        (
            ["", "--mqtt-host", "mqtt-broker.local", "--mqtt-username", "me"],
            "mqtt-broker.local",
            8883,
            "me",
            None,
            None,
        ),
        (
            [
                "",
                "--mqtt-host",
                "mqtt-broker.local",
                "--mqtt-username",
                "me",
                "--mqtt-password",
                "secret",
            ],
            "mqtt-broker.local",
            8883,
            "me",
            "secret",
            None,
        ),
        (
            [
                "",
                "--mqtt-host",
                "mqtt-broker.local",
                "--mqtt-topic-prefix",
                "system/command",
            ],
            "mqtt-broker.local",
            8883,
            None,
            None,
            "system/command",
        ),
    ],
)
def test__main(
    argv,
    expected_mqtt_host,
    expected_mqtt_port,
    expected_username,
    expected_password,
    expected_topic_prefix: typing.Optional[str],
):
    # pylint: disable=too-many-arguments
    with unittest.mock.patch("systemctl_mqtt._run") as run_mock, unittest.mock.patch(
        "sys.argv", argv
    ), unittest.mock.patch("systemctl_mqtt._get_hostname", return_value="hostname"):
        # pylint: disable=protected-access
        systemctl_mqtt._main()
    run_mock.assert_called_once_with(
        mqtt_host=expected_mqtt_host,
        mqtt_port=expected_mqtt_port,
        mqtt_username=expected_username,
        mqtt_password=expected_password,
        mqtt_topic_prefix=expected_topic_prefix or "systemctl/hostname",
    )


@pytest.mark.parametrize(
    ("password_file_content", "expected_password",),
    [
        ("secret", "secret"),
        ("secret space", "secret space"),
        ("secret   ", "secret   "),
        ("  secret ", "  secret "),
        ("secret\n", "secret"),
        ("secret\n\n", "secret\n"),
        ("secret\r\n", "secret"),
        ("secret\n\r\n", "secret\n"),
        ("你好\n", "你好"),
    ],
)
def test__main_password_file(tmpdir, password_file_content, expected_password):
    mqtt_password_path = tmpdir.join("mqtt-password")
    with mqtt_password_path.open("w") as mqtt_password_file:
        mqtt_password_file.write(password_file_content)
    with unittest.mock.patch("systemctl_mqtt._run") as run_mock, unittest.mock.patch(
        "sys.argv",
        [
            "",
            "--mqtt-host",
            "localhost",
            "--mqtt-username",
            "me",
            "--mqtt-password-file",
            str(mqtt_password_path),
        ],
    ), unittest.mock.patch("systemctl_mqtt._get_hostname", return_value="hostname"):
        # pylint: disable=protected-access
        systemctl_mqtt._main()
    run_mock.assert_called_once_with(
        mqtt_host="localhost",
        mqtt_port=8883,
        mqtt_username="me",
        mqtt_password=expected_password,
        mqtt_topic_prefix="systemctl/hostname",
    )


def test__main_password_file_collision(capsys):
    with unittest.mock.patch(
        "sys.argv",
        [
            "",
            "--mqtt-host",
            "localhost",
            "--mqtt-username",
            "me",
            "--mqtt-password",
            "secret",
            "--mqtt-password-file",
            "/var/lib/secrets/mqtt/password",
        ],
    ):
        with pytest.raises(SystemExit):
            # pylint: disable=protected-access
            systemctl_mqtt._main()
    out, err = capsys.readouterr()
    assert not out
    assert (
        "argument --mqtt-password-file: not allowed with argument --mqtt-password\n"
        in err
    )


@pytest.mark.parametrize("hostname", ["test"])
def test__get_hostname(hostname):
    with unittest.mock.patch("socket.gethostname", return_value=hostname):
        # pylint: disable=protected-access
        assert systemctl_mqtt._get_hostname() == hostname
