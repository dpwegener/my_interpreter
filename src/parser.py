from typing import Callable

from expression import Binary, Expr, Grouping, Literal, Unary
from scanner import Token, TokenType


class Parser:
    __tokens: list[Token]
    __current: int
    __reporter: Callable[[int, str, str], None]

    def parse(self) -> Expr | None:
        try:
            return self.__expression()
        except Exception:
            return None

    def __init__(self, tokens: list[Token], reporter: Callable[[int, str, str], None]) -> None:
        self.__tokens = tokens
        self.__current = 0
        Parser.__reporter = reporter

    def __expression(self) -> Expr:
        return self.__equality()

    def __equality(self) -> Expr:
        expr = self.__comparison()

        while self.__match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.__previous()
            right = self.__comparison()
            expr = Binary(expr, operator, right)
        return expr

    def __match(self, *types: TokenType) -> bool:
        for type in types:
            if self.__check(type):
                self.__advance()
                return True
        return False

    def __check(self, type: TokenType) -> bool:
        return False if self.__is_at_end() else self.__peek().type == type

    def __advance(self) -> Token:
        if not self.__is_at_end():
            self.__current += 1
        return self.__previous()

    def __is_at_end(self) -> bool:
        return self.__peek().type == TokenType.EOF

    def __peek(self) -> Token:
        return self.__tokens[self.__current]

    def __previous(self) -> Token:
        return self.__tokens[self.__current - 1]

    def __comparison(self) -> Expr:
        expr = self.__term()

        while self.__match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.__previous()
            right = self.__term()
            expr = Binary(expr, operator, right)
        return expr

    def __term(self) -> Expr:
        expr = self.__factor()

        while self.__match(TokenType.MINUS, TokenType.PLUS):
            operator = self.__previous()
            right = self.__term()
            expr = Binary(expr, operator, right)

        return expr

    def __factor(self) -> Expr:
        expr = self.__unary()

        while self.__match(TokenType.SLASH, TokenType.STAR):
            operator = self.__previous()
            right = self.__unary()
            expr = Binary(expr, operator, right)

        return expr

    def __unary(self) -> Expr:
        if self.__match(TokenType.BANG, TokenType.MINUS):
            operator = self.__previous()
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
            return Literal(self.__previous().literal)
        if self.__match(TokenType.LEFT_PAREN):
            expr = self.__expression()
            self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        raise self.__error(self.__peek(), "Unexpected token.")

    def __consume(self, type: TokenType, message: str) -> Token:
        if self.__check(type):
            return self.__advance()
        raise self.__error(self.__peek(), message)

    def __error(self, token: Token, message: str) -> Exception:
        Parser.error(token, message)
        return Exception()

    def __synchronize(self) -> None:
        self.__advance()

        while not self.__is_at_end():
            if self.__previous().type == TokenType.SEMICOLON:
                return

            match self.__peek().type:
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
            self.__advance()

    @classmethod
    def error(cls, token: Token, message: str) -> None:
        if token.type == TokenType.EOF:
            Parser.__reporter(token.line, " at end", message)
        else:
            Parser.__reporter(token.line, f" at '{token.lexeme}'", message)
