from my_lexer import TOKEN, get_tokens, is_whitespace


def test_get_tokens_no_keywords() -> None:
    expectedTokens = [(TOKEN.IDENT, "a"), (TOKEN.IDENT, "b"), (TOKEN.IDENT, "c")]
    assert expectedTokens == get_tokens("a b c")

    assert [
        (TOKEN.IDENT, "a"),
        (TOKEN.IDENT, "+"),
        (TOKEN.IDENT, "b"),
    ] == get_tokens("a     +     b")


def test_is_whitespace() -> None:
    assert is_whitespace(" ")
    assert is_whitespace("\t")
    assert is_whitespace("\n")
    assert not is_whitespace("a")


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
    let a = 10
    return a"""
    keywords = ["def", "let"]

    expected_tokens = [
        (TOKEN.KEYWORD, "def"),
        (TOKEN.IDENT, "a_function"),
        (TOKEN.KEYWORD, "let"),
        (TOKEN.IDENT, "a"),
        (TOKEN.IDENT, "="),
        (TOKEN.IDENT, "10"),
        (TOKEN.IDENT, "return"),
        (TOKEN.IDENT, "a"),
    ]
    assert expected_tokens == get_tokens(sample_text, keywords=keywords)
