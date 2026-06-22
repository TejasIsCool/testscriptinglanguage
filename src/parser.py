from src.Token import *
from src.AST import *
from src.scanner import source_to_tokens



class Parser:
    current: int = 0
    
    def __init__(self, tokens: list[Token]) -> None:
        self.TOKENS: list[Token] = tokens
        self.current = 0
        self.peek = self.TOKENS[self.current] if len(self.TOKENS) > 0 else None
    
    def check_type(self, token_type: type) -> bool:
        if (isinstance(self.TOKENS[self.current], token_type)):
            return True
        return False
    
    def match(self, token_type: type, name: str | None = None, names: list[str] | None= None) -> bool:
        if (self.peek is not None and isinstance(self.peek, token_type)):
            if name is not None and self.peek.name == name:
                self.consume()
                return True
            if names is not None and self.peek.name in names:
                self.consume()
                return True
        return False
    
    def consume(self):
        self.current += 1
        self.peek = self.TOKENS[self.current] if self.current < len(self.TOKENS) else None
        pass
    
    def previous(self):
        return self.TOKENS[self.current-1]
    
    def parse_expression(self):
        return self.parse_connectors()
    
    def parse_connectors(self) -> Expression:
        left = self.parse_equality()
        while self.match(OperatorToken, names=["&", "|"]):
            operator = self.previous()
            right = self.parse_equality()
            left = BinaryExpression(left, operator, right)
        return left

    def parse_equality(self) -> Expression:
        left = self.parse_comparison()
        while self.match(OperatorToken, names=["==", "!="]):
            operator = self.previous()
            right = self.parse_comparison()
            left = BinaryExpression(left, operator, right)
        return left
    
    def parse_comparison(self) -> Expression:
        left = self.parse_term()
        while self.match(OperatorToken, names=["<", ">", "<=", ">="]):
            operator = self.previous()
            right = self.parse_term()
            left = BinaryExpression(left, operator, right)
        return left
    
    def parse_term(self) -> Expression:
        left = self.parse_factor()
        while self.match(OperatorToken, names=["+", "-"]):
            operator = self.previous()
            right = self.parse_factor()
            left = BinaryExpression(left, operator, right)
        return left
    
    def parse_factor(self) -> Expression:
        left = self.parse_unary()
        while self.match(OperatorToken, names=["*", "/"]):
            operator = self.previous()
            right = self.parse_unary()
            left = BinaryExpression(left, operator, right)
        return left
    
    def parse_unary(self) -> Expression:
        if self.match(OperatorToken, names=["!", "-"]):
            operator = self.previous()
            right = self.parse_unary()
            return UnaryExpression(operator, right)
        return self.parse_primary()
    
    def parse_primary(self) -> Expression:
        if self.peek is None:
            raise Exception("Unexpected end of input")
        
        if isinstance(self.peek, LiteralToken):
            literal = self.peek
            self.consume()
            return LiteralExpression(literal)
        
        if isinstance(self.peek, IdentifierToken):
            identifier = self.peek
            self.consume()
            return IdentifierExpression(identifier)
        
        if self.match(PunctuationToken, name="("):
            expr = self.parse_expression()
            if not self.match(PunctuationToken, name=")"):
                raise Exception("Expected ')' after expression")
            return expr
        
        raise Exception(f"Unexpected token: {self.peek}")



if __name__ == "__main__":
    code = "1 * 5.21 + 2i * (3 - 4) & True | False"
    tokens = source_to_tokens(code)
    print(tokens)
    parser = Parser(tokens)
    ast = parser.parse_expression()
    print(ast)