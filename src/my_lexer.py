from collections.abc import Iterable
from enum import IntEnum
from typing import Tuple


class TOKEN(IntEnum):
    """
    Enum of the lexer token categories
    Values:
    KEYWORD:  token is a keyword
    OPERATOR: token is an operator
    IDENT:    token is an identifier
    LITERAL:  token is a numer or string literal
    PUNCT:    token is a punctuation symbol
    """

    KEYWORD = 1
    OPERATOR = 2
    IDENT = 3
    LITERAL = 4
    PUNCT = 5


keywords = ("def", "let", "return")


def is_whitespace(c: str) -> bool:
    """
    Returns whether or not 'c' is a whitespace character.

    Parameters:
    c (str): The character to check for being a white space.  Should be a single character string

    Returns:
    True: c is a whitespace character
    False: c is not a whitespace character
    """
    return c in " \r\t\n"


def is_numeric(c: str) -> bool:
    """
    Returns whether or not 'c' is an ascii digit.

    Parameters:
    c (str): The character to check.  Should be a single character string

    Returns:
    True: c is a digit
    False: c is not a digit
    """
    return c.isdigit()


def is_alphanumeric(c: str) -> bool:
    """
    Returns whether or not 'c' is an ascii alphanumeric character.

    Parameters:
    c (str): The character to check.  Should be a single character string

    Returns:
    True: c is alphanumeric
    False: c is not alphanumeric
    """
    return is_numeric(c) or c.isalpha() or c == "_"


def is_operation(c: str) -> bool:
    """
    Returns whether or not 'c' is an operation character.

    Parameters:
    c (str): The character to check.  Should be a single character string

    Returns:
    True: c is an operation character
    False: c is not an operation character
    """
    return c in "+-*/="


def handle_numeric(cursor: int, start_index: int, text: str) -> Tuple[str, int]:
    """
    Creates a number Literal token from start_index till the first non-numeric character.

    Parameters:
    cursor (int): the index of the next text character to check for numeric
    start_index (int): the text index of the first digit of the token
    text (str): the text stream being lexed

    Returns:
    str: the lexeme of the number literal
    int: the next cursor location after the end of the literal
    """
    if cursor < len(text):
        char = text[cursor]
        if is_numeric(char):
            return handle_numeric(cursor + 1, start_index, text)
    return (text[start_index:cursor], cursor)


def handle_alpha(cursor: int, start_index: int, text: str) -> Tuple[str, int]:
    if cursor < len(text):
        char = text[cursor]
        if is_alphanumeric(char):
            return handle_alpha(cursor + 1, start_index, text)
    return (text[start_index:cursor], cursor)


def handle_string(cursor: int, start_index: int, text: str) -> Tuple[str, int]:
    if cursor < len(text):
        char = text[cursor]
        if char != '"':
            return handle_string(cursor + 1, start_index, text)
    return (text[start_index + 1 : cursor], cursor + 1)


def get_tokens(text: str, keywords: Iterable[str] = ()) -> list[Tuple[TOKEN, str]]:
    return lex_tokens(0, [], text)


def lex_tokens(
    index: int, tokens: list[Tuple[TOKEN, str]], text: str, k: Iterable[str] = ()
) -> list[Tuple[TOKEN, str]]:
    lexeme = ""
    for i in range(index, len(text)):
        c = text[i]
        if c == '"':
            (lexeme, cursor) = handle_string(i + 1, i, text)
            tokens.append((TOKEN.LITERAL, lexeme))
            return lex_tokens(cursor, tokens, text)

        if is_numeric(c):
            (lexeme, cursor) = handle_numeric(i + 1, i, text)
            tokens.append((TOKEN.LITERAL, lexeme))
            return lex_tokens(cursor, tokens, text)

        if is_alphanumeric(c):
            (lexeme, cursor) = handle_alpha(i + 1, i, text)
            tokens.append((categorize(lexeme), lexeme))
            return lex_tokens(cursor, tokens, text)

        if is_operation(c):
            tokens.append((TOKEN.OPERATOR, c))
            return lex_tokens(i + 1, tokens, text)

    return tokens


def categorize(lexeme: str) -> TOKEN:
    if lexeme in keywords:
        return TOKEN.KEYWORD
    return TOKEN.IDENT
