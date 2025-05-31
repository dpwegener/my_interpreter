from expression import (
    Assign,
    Binary,
    Call,
    Expr,
    Get,
    Grouping,
    Literal,
    Logical,
    Set,
    Super,
    This,
    Unary,
    Variable,
    Visitor,
)
from scanner import Token, TokenType


class AstPrinter(Visitor[str]):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_binary_expr(self, expr: Binary) -> str:
        return self.parenthasize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self.parenthasize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal) -> str:
        return "nil" if not expr.value else f"{expr.value}"

    def visit_unary_expr(self, expr: Unary) -> str:
        return self.parenthasize(expr.operator.lexeme, expr.right)

    def visit_assign_expr(self, expr: Assign) -> str:
        raise NotImplementedError

    def visit_call_expr(self, expr: Call) -> str:
        raise NotImplementedError

    def visit_get_expr(self, expr: Get) -> str:
        raise NotImplementedError

    def visit_logical_expr(self, expr: Logical) -> str:
        raise NotImplementedError

    def visit_set_expr(self, expr: Set) -> str:
        raise NotImplementedError

    def visit_super_expr(self, expr: Super) -> str:
        raise NotImplementedError

    def visit_this_expr(self, expr: This) -> str:
        raise NotImplementedError

    def visit_variable_expr(self, expr: Variable) -> str:
        raise NotImplementedError

    def parenthasize(self, name: str, *exprs: Expr) -> str:
        return f"({name}{''.join(map(lambda expr: f' {expr.accept(self)}', exprs))})"


if __name__ == "__main__":
    expression = Binary(
        Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67)),
    )
    print(AstPrinter().print(expression))
