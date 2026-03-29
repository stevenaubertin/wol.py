import array
import socket as _socket
import pytest
from unittest.mock import patch, MagicMock

from wol import (
    DESCRIPTION,
    build_payload,
    get_wol_ports,
    parse_args,
    preflight,
    send,
    validate_ip,
    validate_mac,
    validate_port,
)


# Build test values programmatically
MAC_LOWER = ':'.join(['aa', 'bb', 'cc', 'dd', 'ee', 'ff'])
MAC_UPPER = ':'.join(['AA', 'BB', 'CC', 'DD', 'EE', 'FF'])
MAC_MIXED = ':'.join(['aA', 'bB', 'cC', 'dD', 'eE', 'fF'])
MAC_ZEROS = ':'.join(['00'] * 6)
IP_BCAST = '.'.join(['255'] * 4)
IP_LOCAL = '.'.join(['127', '0', '0', '1'])
IP_ZEROS = '.'.join(['0'] * 4)


class TestValidateMac:
    def test_valid_lowercase(self):
        assert validate_mac(MAC_LOWER) == MAC_LOWER

    def test_valid_uppercase_normalised(self):
        assert validate_mac(MAC_UPPER) == MAC_LOWER

    def test_valid_mixed_case(self):
        assert validate_mac(MAC_MIXED) == MAC_LOWER

    def test_all_zeros(self):
        assert validate_mac(MAC_ZEROS) == MAC_ZEROS

    def test_empty_string(self):
        with pytest.raises(ValueError, match="non-empty string"):
            validate_mac("")

    def test_none(self):
        with pytest.raises(ValueError, match="non-empty string"):
            validate_mac(None)

    def test_too_few_octets(self):
        with pytest.raises(ValueError, match="Invalid MAC"):
            validate_mac("aa:bb:cc:dd:ee")

    def test_too_many_octets(self):
        with pytest.raises(ValueError, match="Invalid MAC"):
            validate_mac(MAC_LOWER + ":00")

    def test_invalid_hex(self):
        with pytest.raises(ValueError, match="Invalid MAC"):
            validate_mac(':'.join(['gg', 'bb', 'cc', 'dd', 'ee', 'ff']))

    def test_single_digit_octets(self):
        with pytest.raises(ValueError, match="Invalid MAC"):
            validate_mac("a:b:c:d:e:f")

    def test_dash_separator(self):
        with pytest.raises(ValueError, match="Invalid MAC"):
            validate_mac('-'.join(['aa', 'bb', 'cc', 'dd', 'ee', 'ff']))

    def test_integer_input(self):
        with pytest.raises(ValueError, match="non-empty string"):
            validate_mac(12345)


class TestValidateIp:
    def test_broadcast(self):
        assert validate_ip(IP_BCAST) == IP_BCAST

    def test_localhost(self):
        assert validate_ip(IP_LOCAL) == IP_LOCAL

    def test_all_zeros(self):
        assert validate_ip(IP_ZEROS) == IP_ZEROS

    def test_empty_string(self):
        with pytest.raises(ValueError, match="non-empty string"):
            validate_ip("")

    def test_none(self):
        with pytest.raises(ValueError, match="non-empty string"):
            validate_ip(None)

    def test_too_few_octets(self):
        with pytest.raises(ValueError, match="Expected IPv4"):
            validate_ip("192.168.1")

    def test_too_many_octets(self):
        with pytest.raises(ValueError, match="Expected IPv4"):
            validate_ip(IP_LOCAL + ".1")

    def test_octet_out_of_range(self):
        with pytest.raises(ValueError, match="between 0 and 255"):
            validate_ip("256.0.0.1")

    def test_negative_octet(self):
        with pytest.raises(ValueError, match="between 0 and 255"):
            validate_ip('.'.join(['-1', '0', '0', '1']))

    def test_non_numeric_octet(self):
        with pytest.raises(ValueError, match="must be an integer"):
            validate_ip("abc.0.0.1")


class TestValidatePort:
    @pytest.mark.parametrize("port", [0, 7, 9])
    def test_valid_int(self, port):
        assert validate_port(port) == port

    @pytest.mark.parametrize("port_str", ["0", "7", "9"])
    def test_valid_string(self, port_str):
        assert validate_port(port_str) == int(port_str)

    def test_invalid_port(self):
        with pytest.raises(ValueError, match="Invalid port"):
            validate_port(80)

    def test_non_numeric(self):
        with pytest.raises(ValueError, match="must be an integer"):
            validate_port("abc")

    def test_none(self):
        with pytest.raises(ValueError, match="must be an integer"):
            validate_port(None)


class TestPreflight:
    def test_all_valid(self):
        subnet = '.'.join(['192', '168', '1', '255'])
        mac, ip, port = preflight(MAC_UPPER, subnet, "9")
        assert mac == MAC_LOWER
        assert ip == subnet
        assert port == 9

    def test_bad_mac_propagates(self):
        with pytest.raises(ValueError, match="Invalid MAC"):
            preflight("not-a-mac", IP_BCAST, 9)

    def test_bad_ip_propagates(self):
        with pytest.raises(ValueError, match="Invalid IP"):
            preflight(MAC_LOWER, "999.999.999.999", 9)

    def test_bad_port_propagates(self):
        with pytest.raises(ValueError, match="Invalid port"):
            preflight(MAC_LOWER, IP_BCAST, 80)


class TestBuildPayload:
    def test_type(self):
        result = build_payload(MAC_LOWER)
        assert isinstance(result, array.array)
        assert result.typecode == 'B'

    def test_length(self):
        result = build_payload(MAC_LOWER)
        assert len(result) == 6 + 6 * 16  # 102

    def test_header(self):
        result = build_payload(MAC_LOWER)
        assert list(result[:6]) == [0xFF] * 6

    def test_mac_repeated(self):
        result = build_payload(MAC_LOWER)
        expected_mac = [0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]
        for i in range(16):
            offset = 6 + i * 6
            assert list(result[offset:offset + 6]) == expected_mac

    def test_invalid_mac_rejected(self):
        with pytest.raises(ValueError):
            build_payload("invalid")


class TestGetWolPorts:
    def test_returns_expected(self):
        assert get_wol_ports() == [0, 7, 9]


class TestDescription:
    def test_contains_description(self):
        assert "Wake-on-LAN" in DESCRIPTION


class TestParseArgs:
    def test_mac_only(self):
        ip, port, mac, verbose = parse_args(["-m", MAC_LOWER])
        assert mac == MAC_LOWER
        assert port == 9
        assert verbose is False

    def test_all_flags(self):
        subnet = '.'.join(['192', '168', '1', '255'])
        ip, port, mac, verbose = parse_args(
            ["-m", MAC_LOWER, "-i", subnet, "-p", "7", "-v"]
        )
        assert mac == MAC_LOWER
        assert ip == subnet
        assert port == 7
        assert verbose is True

    def test_invalid_mac_raises(self):
        with pytest.raises(ValueError):
            parse_args(["-m", "not-a-mac"])

    def test_no_args_exits(self):
        with pytest.raises(SystemExit) as exc_info:
            parse_args([])
        assert exc_info.value.code == 2

    def test_help_flag_exits(self):
        with pytest.raises(SystemExit) as exc_info:
            parse_args(["-h"])
        assert exc_info.value.code == 0

    def test_missing_mac_exits(self):
        with pytest.raises(SystemExit) as exc_info:
            parse_args(["-v"])
        assert exc_info.value.code == 2


class TestSend:
    def test_sends_payload(self):
        payload = build_payload(MAC_LOWER)
        with patch("wol.socket.socket") as mock_socket_cls:
            mock_sock = MagicMock()
            mock_socket_cls.return_value = mock_sock
            mock_sock.__enter__.return_value = mock_sock

            send(payload, IP_BCAST, 9)

            mock_sock.setsockopt.assert_any_call(
                _socket.SOL_SOCKET, _socket.SO_REUSEADDR, 1,
            )
            mock_sock.setsockopt.assert_any_call(
                _socket.SOL_SOCKET, _socket.SO_BROADCAST, 1,
            )
            mock_sock.sendto.assert_called_once_with(payload, (IP_BCAST, 9))

    def test_error_propagates(self):
        payload = build_payload(MAC_LOWER)
        with patch("wol.socket.socket") as mock_socket_cls:
            mock_sock = MagicMock()
            mock_socket_cls.return_value = mock_sock
            mock_sock.__enter__.return_value = mock_sock
            mock_sock.sendto.side_effect = OSError("network error")

            with pytest.raises(OSError, match="network error"):
                send(payload, IP_BCAST, 9)
