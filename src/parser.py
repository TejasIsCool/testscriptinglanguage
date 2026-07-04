from src.Token import *
from src.AST import *
from src.scanner import source_to_tokens
from src.helpers import Error, ErrorType

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
            # Dont need name for semicolon token
            if isinstance(self.peek, SemicolonToken) :
                self.consume()
                return True
        return False
    
    def consume(self):
        self.current += 1
        self.peek = self.TOKENS[self.current] if self.current < len(self.TOKENS) else None
        pass
    
    def previous(self):
        return self.TOKENS[self.current-1]
    
    
    def parse(self) -> Expression:
        statement_list = self.parse_statement_list()
        # Check if we are at end of program
        if self.peek is not None:
            raise Error(ErrorType.SynErr, self.peek.line_number if self.peek else -1, f"Unexpected token after end of program: {self.peek}")
        
        return statement_list
    
    def parse_statement_list(self) -> Statement_List:
        statements: list[Expression] = []
        while self.peek is not None and self.peek.name != "}":
            statements.append(self.parse_statement())
        return Statement_List(statements)
    
    # Everything returns an expression! Thats the philosophy of this language!
    def parse_statement(self) -> Expression:
        if self.match(KeywordToken, "print"):
            # Instead of parse_expression, should i do parse_statement? GOing with the theme of language
            expr = self.parse_semicolonless_statement()
            if not self.match(SemicolonToken):
                raise Error(ErrorType.SynErr, self.peek.line_number if self.peek else -1, "Expected ';' after print statement")
            return PrintStatement(expr)
        # parse assignment?
        
        # Somehow, if we are already not in a statementlist, it should auto become a statementlist?
        # So probably should seperate parse_statement_list, and make the main parse evaluate that first
        # And in statement, thats where we consume the { and }
        
        # parse statement block
        if self.match(PunctuationToken, name="{"):
            statement_list = self.parse_statement_list()
            if not self.match(PunctuationToken, name="}"):
                raise Error(ErrorType.SynErr, self.peek.line_number if self.peek else -1, "Expected '}' after statement block")
            return statement_list
        
        # Should also just check if there is just a semi colon, so it becomes an empty statement
        if self.match(SemicolonToken):
            return Expression()
        
        # By default, we parse expressions i guess, followed by semi colon
        default_expression = self.parse_expression();
        
        # I actually dont want to check for semi colon,
        # cause i want to allow statements inside print or ifelse or while
        # and if i replace tham with parse_statement instead of parse_expression, 
        # then it will check for semi colons, which isint what i want.
        # so want a parse_semicolonless_statement, which will parse statements without checking for semi colons
        
        
        if not self.match(SemicolonToken):
            raise Error(ErrorType.SynErr, self.peek.line_number if self.peek else -1, "Expected ';' after statement")
        return default_expression
    
    
    def parse_semicolonless_statement(self) -> Expression:
        
        # parse statement block
        if self.match(PunctuationToken, name="{"):
            statement_list = self.parse_statement_list()
            if not self.match(PunctuationToken, name="}"):
                raise Error(ErrorType.SynErr, self.peek.line_number if self.peek else -1, "Expected '}' after statement block")
            return statement_list
        
        # parse if else, while?
        if self.match(SemicolonToken):
            return Expression()
        
        default_expression = self.parse_expression();
        return default_expression
    
    
    
    def parse_expression(self) -> Expression:
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
        while self.match(OperatorToken, names=["*", "/", "%"]):
            operator = self.previous()
            right = self.parse_unary()
            left = BinaryExpression(left, operator, right)
        return left
    
    def parse_unary(self) -> Expression:
        if self.match(OperatorToken, names=["!", "-"]):
            operator = self.previous()
            right = self.parse_unary()
            return UnaryExpression(operator, right)
        return self.parse_exponent()

    def parse_exponent(self) -> Expression:
        # Exponent is right associative, so we need to parse the right side first
        left = self.parse_primary()
        if self.match(OperatorToken, names=["^"]):
            operator = self.previous()
            # Instead of loop, we have a condition and recurse into itself
            right = self.parse_exponent()
            return BinaryExpression(left, operator, right)
        return left
    
    def parse_primary(self) -> Expression:
        if self.peek is None:
            raise Error(ErrorType.SynErr, self.peek.line_number if self.peek else -1, "Unexpected end of input")
        
        if isinstance(self.peek, LiteralToken):
            literal = self.peek
            self.consume()
            return LiteralExpression(literal)
        
        if isinstance(self.peek, IdentifierToken):
            identifier = self.peek
            self.consume()
            return IdentifierExpression(identifier)
        
        if self.match(PunctuationToken, name="("):
            # Every statement is expression
            expr = self.parse_semicolonless_statement()
            if not self.match(PunctuationToken, name=")"):
                print(f"DEBUG: {self.peek}")
                raise Error(ErrorType.SynErr, self.peek.line_number if self.peek else -1, "Expected ')' after expression")
            return expr
        
        # Do i want to permit 2+{4+4;}?
        # If so, the below wont work
        # Will have to do a parse_semicolonless_statement maybe
        # But then I am not sure how ill do unknown token thing
        # I suppose i can seperately do if peek { or smth
        # But what if I want 2+print(4)?? Do I even want that? Maybe, seems nice
        
        # BUT THEN WHERE DO I DO UNEXPECTED TOKEN HANDLING??
        # I think case by case is the only feasable way
        if self.match(PunctuationToken, name="{"):
            statement_list = self.parse_statement_list()
            if not self.match(PunctuationToken, name="}"):
                raise Error(ErrorType.SynErr, self.peek.line_number if self.peek else -1, "Expected '}' after statement block")
            return statement_list
        
        # We will only accept print with () in middle of expressions,
        # as otherwise we have ambiguity, like
        # is 2 + print 4 + 5 == 2 + (print 4) + 5 or 2 + print (4 + 5)??
        if self.match(KeywordToken, "print"):
            if not self.match(PunctuationToken, name="("):
                raise Error(ErrorType.SynErr, self.peek.line_number if self.peek else -1, "Expected '(' after 'print' used in expressions")
            expr = self.parse_semicolonless_statement()
            if not self.match(PunctuationToken, name=")"):
                raise Error(ErrorType.SynErr, self.peek.line_number if self.peek else -1, "Expected ')' after print expression")
            return PrintStatement(expr)
        
        raise Error(ErrorType.SynErr, self.peek.line_number if self.peek else -1, f"Unexpected token: {self.peek}")



if __name__ == "__main__":
    code = "1 * 5.21 + 2i * (3 - 4) & True | False"
    tokens = source_to_tokens(code)
    print(tokens)
    if tokens is not None:
        parser = Parser(tokens)
        ast = parser.parse_expression()
        print(ast)