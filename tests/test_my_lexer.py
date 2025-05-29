from my_lexer import (
    TOKEN,
    get_tokens,
    is_alphanumeric,
    is_numeric,
    is_operation,
    is_whitespace,
)


def test_get_tokens_no_keywords() -> None:
    expectedTokens = [(TOKEN.IDENT, "a"), (TOKEN.IDENT, "b"), (TOKEN.IDENT, "c")]
    assert expectedTokens == get_tokens("a b c")

    assert [
        (TOKEN.IDENT, "a"),
        (TOKEN.OPERATOR, "+"),
        (TOKEN.IDENT, "b"),
    ] == get_tokens("a     +     b")


def test_is_whitespace() -> None:
    assert is_whitespace(" ")
    assert is_whitespace("\t")
    assert is_whitespace("\n")
    assert not is_whitespace("a")


def test_is_numeric() -> None:
    for i in range(ord("0"), ord("9") + 1):
        assert is_numeric(chr(i))

    for a in range(ord("a"), ord("z") + 1):
        assert not is_numeric(chr(a))


def test_is_alphanumeric() -> None:
    for i in range(ord("0"), ord("9") + 1):
        assert is_alphanumeric(chr(i))

    for a in range(ord("a"), ord("z") + 1):
        assert is_alphanumeric(chr(a))

    for a in range(ord("A"), ord("Z") + 1):
        assert is_alphanumeric(chr(a))

    for c in " +-=/=,.;:\"'":
        assert not is_alphanumeric(c)


def test_is_operation() -> None:
    for op in "+-*/=":
        assert is_operation(op)

    for op in "abc123":
        assert not is_operation(op)


def test_the_beautiful_white_moon() -> None:
    expected_tokens = [
        (TOKEN.IDENT, "the"),
        (TOKEN.IDENT, "beautiful"),
        (TOKEN.IDENT, "white"),
        (TOKEN.IDENT, "moon"),
    ]
    assert expected_tokens == get_tokens(" the beautiful   white\tmoon")


def test_get_tokens_with_keywords() -> None:
    sample_text = """
def a_function
    let a = 10 + 20
    let b = "string"
    return a"""

    expected_tokens = [
        (TOKEN.KEYWORD, "def"),
        (TOKEN.IDENT, "a_function"),
        (TOKEN.KEYWORD, "let"),
        (TOKEN.IDENT, "a"),
        (TOKEN.OPERATOR, "="),
        (TOKEN.LITERAL, "10"),
        (TOKEN.OPERATOR, "+"),
        (TOKEN.LITERAL, "20"),
        (TOKEN.KEYWORD, "let"),
        (TOKEN.IDENT, "b"),
        (TOKEN.OPERATOR, "="),
        (TOKEN.LITERAL, "string"),
        (TOKEN.KEYWORD, "return"),
        (TOKEN.IDENT, "a"),
    ]
    actual = get_tokens(sample_text)
    assert expected_tokens == actual
