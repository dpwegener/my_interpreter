from collections.abc import Iterable
from enum import IntEnum
from typing import Tuple


class TOKEN(IntEnum):
    KEYWORD = 1
    OPERATOR = 2
    IDENT = 3
    LITERAL = 4
    PUNCT = 5


def is_whitespace(c: str) -> bool:
    return c in " \t\n"


def get_tokens(text: str, keywords: Iterable[str] = ()) -> list[Tuple[TOKEN, str]]:
    tokens = []
    lexeme = ""
    for c in text:
        if is_whitespace(c):
            if lexeme != "":
                tokens.append((categorize(lexeme, keywords=keywords), lexeme))
                lexeme = ""
        else:
            lexeme += c
    if lexeme != "":
        tokens.append((categorize(lexeme, keywords=keywords), lexeme))
    return tokens


def categorize(lexeme: str, keywords: Iterable[str]) -> TOKEN:
    if lexeme in keywords:
        return TOKEN.KEYWORD
    return TOKEN.IDENT
