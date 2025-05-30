"""
Python Interpretor based on https://craftinginterpreters.com/
"""

import sys
from enum import IntEnum
from typing import Callable, Iterable


class TokenType(IntEnum):
    # Single Character Tokens
    LEFT_PAREN = 1
    RIGHT_PAREN = 2
    LEFT_BRACE = 3
    RIGHT_BRACE = 4
    COMMA = 5
    DOT = 6
    MINUS = 7
    PLUS = 8
    SEMICOLON = 9
    SLASH = 10
    STAR = 11
    # One or two character tokens
    BANG = 12
    BANG_EQUAL = 13
    EQUAL = 14
    EQUAL_EQUAL = 15
    GREATER = 16
    GREATER_EQUAL = 17
    LESS = 18
    LESS_EQUAL = 19
    # Literals
    IDENTIFIER = 20
    STRING = 21
    NUMBER = 22
    # Keywords
    AND = 23
    CLASS = 24
    ELSE = 25
    FALSE = 26
    FUN = 27
    FOR = 28
    IF = 29
    NIL = 30
    OR = 31
    PRINT = 32
    RETURN = 33
    SUPER = 34
    THIS = 35
    TRUE = 36
    VAR = 37
    WHILE = 38
    EOF = 39


class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: None | str | float, line: int) -> None:
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self) -> str:
        return f"({self.type.name} {self.lexeme} {self.literal})"


class Scanner:
    def __init__(self, source: str, reporter: Callable[[int, str], None]) -> None:
        self.source = source
        self.start = 0
        self.reporter = reporter
        self.current = 0
        self.line = 1
        self.tokens = []

    def scan_tokens(self) -> Iterable[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self) -> None:
        c = self.advance()
        match c:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case _:
                self.reporter(self.line, "Unexpected character.")

    def add_token(
        self,
        type: TokenType,
        literal: None | str | float = None,
    ) -> None:
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        return c


def main() -> None:
    if len(sys.argv) > 2:
        print("Usage: plox [script]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_prompt()


class ErrorReporter:
    had_error: bool

    @classmethod
    def report_error(cls, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}")
        ErrorReporter.had_error = True


def run_file(path: str) -> None:
    with open(path, "r") as file:
        content = file.read()
        run(content)
        if ErrorReporter.had_error:
            sys.exit(65)


def run_prompt() -> None:
    while True:
        try:
            line = input("> ")
            run(line)
            ErrorReporter.had_error = False
        except EOFError:
            break


def run(source: str) -> None:
    tokens = Scanner(source, error).scan_tokens()

    print(tokens)


def error(line: int, message: str) -> None:
    report(line, "", message)


def report(line: int, where: str, message: str) -> None:
    ErrorReporter.report_error(line, where, message)


if __name__ == "__main__":
    main()
