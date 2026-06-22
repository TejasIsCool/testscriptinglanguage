from src.Token import *


class Expression:
    pass

class BinaryExpression(Expression):
    def __init__(self, left: Expression, operator: Token, right: Expression) -> None:
        self.left = left
        self.operator = operator
        self.right = right
    
    def __str__(self) -> str:
        return f"({self.left} {self.operator} {self.right})"

class UnaryExpression(Expression):
    def __init__(self, operator: Token, right: Expression) -> None:
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return f"({self.operator} {self.right})"

class LiteralExpression(Expression):
    def __init__(self, literal: LiteralToken) -> None:
        self.literal = literal

    def __str__(self) -> str:
        return f"({self.literal})"

class IdentifierExpression(Expression):
    def __init__(self, identifier: IdentifierToken) -> None:
        self.identifier = identifier

    def __str__(self) -> str:
        return f"({self.identifier})"

