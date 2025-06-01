from enum import IntEnum
from types import MappingProxyType
from typing import Callable


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


__keywords = MappingProxyType(
    {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }
)


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

    def scan_tokens(self) -> list[Token]:
        while not self.__is_at_end():
            self.start = self.current
            self.__scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def __is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def __scan_token(self) -> None:
        c = self.__advance()
        match c:
            case "(":
                self.__add_token(TokenType.LEFT_PAREN)
            case ")":
                self.__add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.__add_token(TokenType.LEFT_BRACE)
            case "}":
                self.__add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.__add_token(TokenType.COMMA)
            case ".":
                self.__add_token(TokenType.DOT)
            case "-":
                self.__add_token(TokenType.MINUS)
            case "+":
                self.__add_token(TokenType.PLUS)
            case ";":
                self.__add_token(TokenType.SEMICOLON)
            case "*":
                self.__add_token(TokenType.STAR)
            case "!":
                self.__add_token(TokenType.BANG_EQUAL if self.__match("=") else TokenType.BANG)
            case "=":
                self.__add_token(TokenType.EQUAL_EQUAL if self.__match("=") else TokenType.EQUAL)
            case "<":
                self.__add_token(TokenType.LESS_EQUAL if self.__match("=") else TokenType.LESS)
            case ">":
                self.__add_token(TokenType.GREATER_EQUAL if self.__match("=") else TokenType.GREATER)
            case "/":
                if self.__match("/"):
                    while self.__peek() != "\n" and not self.__is_at_end():
                        self.__advance()
                else:
                    self.__add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                pass  # ignore white space
            case "\n":
                self.line += 1
            case '"':
                self.__string()
            case _:
                if c.isdigit():
                    self.__number()
                elif c.isalpha():
                    self.__identifier()
                else:
                    self.reporter(self.line, "Unexpected character.")

    def __add_token(self, type: TokenType, literal: None | str | float = None) -> None:
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def __advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        return c

    def __match(self, expected: str) -> bool:
        if self.__is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def __peek(self) -> str:
        return "\0" if self.__is_at_end() else self.source[self.current]

    def __string(self) -> None:
        while self.__peek() != '"' and not self.__is_at_end():
            if self.__peek() == "\n":
                self.line += 1
            self.__advance()
        if self.__is_at_end():
            self.reporter(self.line, "Unterminated string.")
            return
        self.__advance()
        value = self.source[self.start + 1 : self.current - 1]
        self.__add_token(TokenType.STRING, value)

    def __number(self) -> None:
        while self.__peek().isdigit():
            self.__advance()

        if self.__peek() == "." and self.__peek_next().isdigit():
            self.__advance()
            while self.__peek().isdigit():
                self.__advance()
        self.__add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def __identifier(self) -> None:
        while self.__peek().isalnum():
            self.__advance()
        text = self.source[self.start : self.current]
        type = __keywords.get(text)
        type = type if type else TokenType.IDENTIFIER
        self.__add_token(type)

    def __peek_next(self) -> str:
        if self.current + 1 > len(self.source):
            return "\0"
        return self.source[self.current + 1]
