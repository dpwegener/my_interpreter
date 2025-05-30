from abc import ABC, abstractmethod
from typing import Protocol, TypeVar

from plox import Token

R = TypeVar("R", covariant=True)


class Visitor(Protocol[R]):
    def visit_assign_expr(self, expr: "Assign") -> R: ...
    def visit_binary_expr(self, expr: "Binary") -> R: ...
    def visit_call_expr(self, expr: "Call") -> R: ...
    def visit_get_expr(self, expr: "Get") -> R: ...
    def visit_grouping_expr(self, expr: "Grouping") -> R: ...
    def visit_literal_expr(self, expr: "Literal") -> R: ...
    def visit_logical_expr(self, expr: "Logical") -> R: ...
    def visit_set_expr(self, expr: "Set") -> R: ...
    def visit_super_expr(self, expr: "Super") -> R: ...
    def visit_this_expr(self, expr: "This") -> R: ...
    def visit_unary_expr(self, expr: "Unary") -> R: ...
    def visit_variable_expr(self, expr: "Variable") -> R: ...


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor[R]) -> R:
        pass


class Assign(Expr):
    name: Token
    value: Expr

    def __init__(self, name: Token, value: Expr) -> None:
        self.name = name
        self.value = value

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_assign_expr(self)


class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_binary_expr(self)


class Call(Expr):
    callee: Expr
    paren: Token
    arguments: list[Expr]

    def __init__(self, callee: Expr, paren: Token, arguments: list[Expr]) -> None:
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_call_expr(self)


class Get(Expr):
    object: Expr
    name: Token

    def __init__(self, object: Expr, name: Token) -> None:
        self.object = object
        self.name = name

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_get_expr(self)


class Grouping(Expr):
    expression: Expr

    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_grouping_expr(self)


class Literal(Expr):
    value: object

    def __init__(self, value: object) -> None:
        self.value = value

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_literal_expr(self)


class Logical(Expr):
    left: Expr
    operator: Token
    right: Expr

    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_logical_expr(self)


class Set(Expr):
    object: Expr
    name: Token
    value: Expr

    def __init__(self, object: Expr, name: Token, value: Expr) -> None:
        self.object = object
        self.name = name
        self.value = value

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_set_expr(self)


class Super(Expr):
    keyword: Token
    method: Token

    def __init__(self, keyword: Token, method: Token) -> None:
        self.keyword = keyword
        self.method = method

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_super_expr(self)


class This(Expr):
    keyword: Token

    def __init__(self, keyword: Token) -> None:
        self.keyword = keyword

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_this_expr(self)


class Unary(Expr):
    operator: Token
    right: Expr

    def __init__(self, operator: Token, right: Expr) -> None:
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_unary_expr(self)


class Variable(Expr):
    name: Token

    def __init__(self, name: Token) -> None:
        self.name = name

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_variable_expr(self)
