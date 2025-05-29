from plox import Scanner, TokenType, error


def test_is_at_end() -> None:
    cut = Scanner("", error)
    assert cut.is_at_end()

    cut = Scanner("non_empty", error)
    assert not cut.is_at_end()


def test_advance() -> None:
    cut = Scanner("ab", error)
    assert "a" == cut.advance()
    assert "b" == cut.advance()


def test_add_token() -> None:
    cut = Scanner("", error)
    cut.add_token(TokenType.IDENTIFIER, "abc")
    actual = cut.tokens[0]
    assert TokenType.IDENTIFIER == actual.type
    assert "abc" == actual.literal

    cut = Scanner("", error)
    cut.add_token(TokenType.RIGHT_BRACE)
    actual = cut.tokens[0]
    assert TokenType.RIGHT_BRACE == actual.type
    assert actual.literal is None
