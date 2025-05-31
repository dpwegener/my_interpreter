from typing import Callable

from expression import Binary, Expr, Grouping, Literal, Unary
from scanner import Token, TokenType


class Parser:
    tokens: list[Token]
    current: int
    reporter: Callable[[int, str, str], None]

    def parse(self) -> Expr | None:
        try:
            return self.__expression()
        except Exception:
            return None

    def __init__(self, tokens: list[Token], reporter: Callable[[int, str, str], None]) -> None:
        self.tokens = tokens
        self.current = 0
        Parser.reporter = reporter

    def __expression(self) -> Expr:
        return self.__equality()

    def __equality(self) -> Expr:
        expr = self.__comparison()

        while self.__match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.__comparison()
            expr = Binary(expr, operator, right)
        return expr

    def __match(self, *types: TokenType) -> bool:
        for type in types:
            if self.__check(type):
                self.advance()
                return True
        return False

    def __check(self, type: TokenType) -> bool:
        return False if self.is_at_end() else self.peek().type == type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def __comparison(self) -> Expr:
        expr = self.__term()

        while self.__match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.__term()
            expr = Binary(expr, operator, right)
        return expr

    def __term(self) -> Expr:
        expr = self.__factor()

        while self.__match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.__term()
            expr = Binary(expr, operator, right)

        return expr

    def __factor(self) -> Expr:
        expr = self.__unary()

        while self.__match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.__unary()
            expr = Binary(expr, operator, right)

        return expr

    def __unary(self) -> Expr:
        if self.__match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.__unary()
            return Unary(operator, right)

        return self.__primary()

    def __primary(self) -> Expr:
        if self.__match(TokenType.FALSE):
            return Literal(False)
        if self.__match(TokenType.TRUE):
            return Literal(True)
        if self.__match(TokenType.NIL):
            return Literal(None)
        if self.__match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        if self.__match(TokenType.LEFT_PAREN):
            expr = self.__expression()
            self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        raise self.__error(self.peek(), "Unexpected token.")

    def __consume(self, type: TokenType, message: str) -> Token:
        if self.__check(type):
            return self.advance()
        raise self.__error(self.peek(), message)

    def __error(self, token: Token, message: str) -> Exception:
        Parser.error(token, message)
        return Exception()

    def __synchronize(self) -> None:
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return

            match self.peek().type:
                case (
                    TokenType.CLASS
                    | TokenType.FUN
                    | TokenType.VAR
                    | TokenType.FOR
                    | TokenType.IF
                    | TokenType.WHILE
                    | TokenType.PRINT
                    | TokenType.RETURN
                ):
                    return
            self.advance()

    @classmethod
    def error(cls, token: Token, message: str) -> None:
        if token.type == TokenType.EOF:
            Parser.reporter(token.line, " at end", message)
        else:
            Parser.reporter(token.line, f" at '{token.lexeme}'", message)
