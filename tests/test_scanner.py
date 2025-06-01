from typing import Callable

import pytest

from scanner import Scanner, TokenType


class TestScanner:
    reported_errors = []

    @pytest.fixture
    def setup_reporter(self) -> Callable[[int, str], None]:
        def capture_error(line: int, message: str) -> None:
            self.reported_errors.append((line, message))

        return capture_error

    def test_scan_tokens_simple_add(self, setup_reporter: Callable[[int, str], None]) -> None:
        source = "3 + 4"
        out = Scanner(source, setup_reporter)
        tokens = list(out.scan_tokens())
        expected_values = [
            (TokenType.NUMBER, 3.0),
            (TokenType.PLUS, None),
            (TokenType.NUMBER, 4.0),
            (TokenType.EOF, None),
        ]
        for expected, actual in zip(expected_values, tokens, strict=True):
            assert expected[0] == actual.type
            assert expected[1] == actual.literal

        assert len(self.reported_errors) == 0

    def test_scan_tokens_punctuation(self, setup_reporter: Callable[[int, str], None]) -> None:
        source = "({,.;})"
        out = Scanner(source, setup_reporter)
        tokens = list(out.scan_tokens())
        expected_types = [
            TokenType.LEFT_PAREN,
            TokenType.LEFT_BRACE,
            TokenType.COMMA,
            TokenType.DOT,
            TokenType.SEMICOLON,
            TokenType.RIGHT_BRACE,
            TokenType.RIGHT_PAREN,
            TokenType.EOF,
        ]
        for expected, actual in zip(expected_types, tokens, strict=True):
            assert expected == actual.type

        assert len(self.reported_errors) == 0

    def test_unexpected_character(self, setup_reporter: Callable[[int, str], None]) -> None:
        source = "[]"
        out = Scanner(source, setup_reporter)
        tokens = list(out.scan_tokens())
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF
        assert len(self.reported_errors) == 2
        assert self.reported_errors[0][1] == "Unexpected character."
        assert self.reported_errors[1][1] == "Unexpected character."
