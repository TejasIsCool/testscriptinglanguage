from src.Token import *
from src.helpers import Error, ErrorType, ComplexNum
# Can implement evaluation here!


# Create a joined output type of evaluate
# SO output of evaluate can be a ComplexNum, string, boolean, or an AST


class Expression():
    def evaluate(self) -> ComplexNum|str|bool|None:
        """Evaluates the given expression
        """
        pass
    
    # By default, for empty statements
    def __str__(self) -> str:
        return f"Empty Expression"
    pass

class BinaryExpression(Expression):
    def __init__(self, left: Expression, operator: Token, right: Expression) -> None:
        self.left = left
        self.operator = operator
        self.right = right
    
    def __str__(self) -> str:
        return f"({self.left} {self.operator} {self.right})"
    
    def evaluate(self) -> ComplexNum|str|bool|None:
        if self.operator.name == "+":
            expr_left_val = self.left.evaluate()
            valid_types: list[type] = [ComplexNum, str, bool]
            # For now only numeric addition, and string addition, and maybe bool with strings
            if not any(isinstance(expr_left_val, t) for t in valid_types): # type: ignore
                raise Error(ErrorType.TypeErr, self.operator.line_number, "Left side of '+' is not a plusable type!")
            expr_right_val = self.right.evaluate()
            if not any(isinstance(expr_right_val, t) for t in valid_types): # type: ignore
                raise Error(ErrorType.TypeErr, self.operator.line_number, "Right side of '+' is not a plusable type!")

            # if either is a string, convert both to string and concatenate
            if isinstance(expr_left_val, str) or isinstance(expr_right_val, str):
                return str(expr_left_val) + str(expr_right_val)
            if isinstance(expr_left_val, bool) or isinstance(expr_right_val, bool):
                raise Error(ErrorType.TypeErr, self.operator.line_number, "Cannot add boolean values!")
            return expr_left_val + expr_right_val # type: ignore
        if self.operator.name == "-":
            expr_left_val = self.left.evaluate()
            # For now, only numeric subtraction, will support other things later
            if not isinstance(expr_left_val, ComplexNum): # type: ignore
                raise Error(ErrorType.TypeErr, self.operator.line_number, "Left side of '-' is not a number!")
            expr_right_val = self.right.evaluate()
            if not isinstance(expr_right_val, ComplexNum): # type: ignore
                raise Error(ErrorType.TypeErr, self.operator.line_number, "Right side of '-' is not a number!")
            return expr_left_val - expr_right_val
        if self.operator.name == "*":
            expr_left_val = self.left.evaluate()
            if not isinstance(expr_left_val, ComplexNum): # type: ignore
                raise Error(ErrorType.TypeErr, self.operator.line_number, "Left side of '*' is not a number!")
            expr_right_val = self.right.evaluate()
            if not isinstance(expr_right_val, ComplexNum): # type: ignore
                raise Error(ErrorType.TypeErr, self.operator.line_number, "Right side of '*' is not a number!")
            return expr_left_val * expr_right_val
        if self.operator.name == "/":
            expr_left_val = self.left.evaluate()
            if not isinstance(expr_left_val, ComplexNum): # type: ignore
                raise Error(ErrorType.TypeErr, self.operator.line_number, "Left side of '/' is not a number!")
            expr_right_val = self.right.evaluate()
            if not isinstance(expr_right_val, ComplexNum): # type: ignore
                raise Error(ErrorType.TypeErr, self.operator.line_number, "Right side of '/' is not a number!")
            return expr_left_val / expr_right_val
        if self.operator.name == "^":
            expr_left_val = self.left.evaluate()
            if not isinstance(expr_left_val, ComplexNum): # type: ignore
                raise Error(ErrorType.TypeErr, self.operator.line_number, "Left side of '^' is not a number!")
            expr_right_val = self.right.evaluate()
            if not isinstance(expr_right_val, ComplexNum): # type: ignore
                raise Error(ErrorType.TypeErr, self.operator.line_number, "Right side of '^' is not a number!")
            return expr_left_val ** expr_right_val
        if self.operator.name == "%":
            expr_left_val = self.left.evaluate()
            if not isinstance(expr_left_val, ComplexNum): # type: ignore
                raise Error(ErrorType.TypeErr, self.operator.line_number, "Left side of '%' is not a number!")
            # Make sure left side is a purely real number
            if expr_left_val.imag != 0: # type: ignore
                raise Error(ErrorType.TypeErr, self.operator.line_number, "Left side of '%' is not a purely real number!")
            expr_right_val = self.right.evaluate()
            if not isinstance(expr_right_val, ComplexNum): # type: ignore
                raise Error(ErrorType.TypeErr, self.operator.line_number, "Right side of '%' is not a number!")
            # Make sure right side is a purely real number
            if expr_right_val.imag != 0: # type: ignore
                raise Error(ErrorType.TypeErr, self.operator.line_number, "Right side of '%' is not a purely real number!")
            return ComplexNum(expr_left_val.real % expr_right_val.real)
        
        
        
        if self.operator.name == "==":
            expr_left_val = self.left.evaluate()
            expr_right_val = self.right.evaluate()
            return expr_left_val == expr_right_val
        if self.operator.name == "!=":
            expr_left_val = self.left.evaluate()
            expr_right_val = self.right.evaluate()
            return expr_left_val != expr_right_val
        if self.operator.name == "<":
            # For strings, will compare lexicographically, for complex, only if both imaginary is 0
            expr_left_val = self.left.evaluate()
            expr_right_val = self.right.evaluate()
            if isinstance(expr_left_val, ComplexNum) and isinstance(expr_right_val, ComplexNum): # type: ignore
                if expr_left_val.imag != 0 or expr_right_val.imag != 0:
                    raise Error(ErrorType.TypeErr, self.operator.line_number, "Cannot compare numbers with non-zero imaginary parts!")
                return expr_left_val.real < expr_right_val.real
            if isinstance(expr_left_val, str) and isinstance(expr_right_val, str):
                return expr_left_val < expr_right_val
            raise Error(ErrorType.TypeErr, self.operator.line_number, "Cannot compare values of different types!")

        if self.operator.name == ">":
            # For strings, will compare lexicographically, for complex, only if both imaginary is 0
            expr_left_val = self.left.evaluate()
            expr_right_val = self.right.evaluate()
            if isinstance(expr_left_val, ComplexNum) and isinstance(expr_right_val, ComplexNum): # type: ignore
                if expr_left_val.imag != 0 or expr_right_val.imag != 0:
                    raise Error(ErrorType.TypeErr, self.operator.line_number, "Cannot compare numbers with non-zero imaginary parts!")
                return expr_left_val.real > expr_right_val.real
            if isinstance(expr_left_val, str) and isinstance(expr_right_val, str):
                return expr_left_val > expr_right_val
            raise Error(ErrorType.TypeErr, self.operator.line_number, "Cannot compare values of different types!")

        if self.operator.name == "<=":
            # For strings, will compare lexicographically, for complex, only if both imaginary is 0
            expr_left_val = self.left.evaluate()
            expr_right_val = self.right.evaluate()
            if isinstance(expr_left_val, ComplexNum) and isinstance(expr_right_val, ComplexNum): # type: ignore
                if expr_left_val.imag != 0 or expr_right_val.imag != 0:
                    raise Error(ErrorType.TypeErr, self.operator.line_number, "Cannot compare numbers with non-zero imaginary parts!")
                return expr_left_val.real <= expr_right_val.real
            if isinstance(expr_left_val, str) and isinstance(expr_right_val, str):
                return expr_left_val <= expr_right_val
            raise Error(ErrorType.TypeErr, self.operator.line_number, "Cannot compare values of different types!")

        if self.operator.name == ">=":
            # For strings, will compare lexicographically, for complex, only if both imaginary is 0
            expr_left_val = self.left.evaluate()
            expr_right_val = self.right.evaluate()
            if isinstance(expr_left_val, ComplexNum) and isinstance(expr_right_val, ComplexNum): # type: ignore
                if expr_left_val.imag != 0 or expr_right_val.imag != 0:
                    raise Error(ErrorType.TypeErr, self.operator.line_number, "Cannot compare numbers with non-zero imaginary parts!")
                return expr_left_val.real >= expr_right_val.real
            if isinstance(expr_left_val, str) and isinstance(expr_right_val, str):
                return expr_left_val >= expr_right_val
            raise Error(ErrorType.TypeErr, self.operator.line_number, "Cannot compare values of different types!")

        # Boolean ones too, what do we want to be truty and flasy, and do we even want conversion?
        # Screw it, no type conversion, only booleans allowed
        if self.operator.name == "&":
            expr_left_val = self.left.evaluate()
            expr_right_val = self.right.evaluate()
            if not isinstance(expr_left_val, bool) or not isinstance(expr_right_val, bool):
                raise Error(ErrorType.TypeErr, self.operator.line_number, "Both sides of '&' must be boolean!")
            return expr_left_val and expr_right_val
        if self.operator.name == "|":
            expr_left_val = self.left.evaluate()
            expr_right_val = self.right.evaluate()
            if not isinstance(expr_left_val, bool) or not isinstance(expr_right_val, bool):
                raise Error(ErrorType.TypeErr, self.operator.line_number, "Both sides of '|' must be boolean!")
            return expr_left_val or expr_right_val
        pass

class UnaryExpression(Expression):
    def __init__(self, operator: Token, right: Expression) -> None:
        self.operator = operator
        self.right = right

    def evaluate(self) -> ComplexNum|str|bool|None:
        if self.operator.name == "-":
            expr_right_val = self.right.evaluate()
            if not isinstance(expr_right_val, ComplexNum): # type: ignore
                raise Error(ErrorType.TypeErr, self.operator.line_number, "Right side of unary '-' is not a number!")
            return -expr_right_val
        if self.operator.name == "!":
            expr_right_val = self.right.evaluate()
            if not isinstance(expr_right_val, bool):
                raise Error(ErrorType.TypeErr, self.operator.line_number, "Right side of '!' must be boolean!")
            return not expr_right_val
        pass
    
    def __str__(self) -> str:
        return f"({self.operator} {self.right})"

class LiteralExpression(Expression):
    def __init__(self, literal: LiteralToken) -> None:
        self.literal = literal

    def evaluate(self) -> ComplexNum|str|bool|None:
        return self.literal.value
    
    def __str__(self) -> str:
        return f"({self.literal})"

class IdentifierExpression(Expression):
    def __init__(self, identifier: IdentifierToken) -> None:
        self.identifier = identifier

    def evaluate(self) -> ComplexNum|str|bool|None:
        # This is a placeholder - in a real implementation, this would look up the identifier in the symbol table
        pass
    
    def __str__(self) -> str:
        return f"({self.identifier})"



class Statement(Expression):
    def __init__(self, statement: Statement) -> None:
        self.statement = statement
        pass
    
    def evaluate(self) -> ComplexNum|str|bool|None:
        return self.statement.evaluate()
    
    
    
    
class PrintStatement(Statement):
    def __init__(self, expression: Expression) -> None:
        self.expression = expression
        pass
    
    # Result of the print statement is whatever value it printed
    def evaluate(self) -> ComplexNum|str|bool|None:
        value = self.expression.evaluate()
        print(value)
        return value
    
    
    # This is the debugging str! not the actual thing thats printed
    def __str__(self) -> str:
        return f"Print ({self.expression})"


# The philosophy that every statement and statement block is an expression, that returns a AST
class Statement_List(Statement):
    def __init__(self, statements: list[Expression]) -> None:
        self.statements = statements
        pass
    
    
    # I do want an assignable evaluate? Not 100% sure.
    
    def evaluate(self) -> ComplexNum|str|bool|None:
        result = None
        for statement in self.statements:
            result = statement.evaluate()
        # We return the result of the last statement ig.
        # I can get an idea of how monads work here, we pass the result to the next evaluate essentially.
        return result
    
    def __str__(self) -> str:
        # Each statement is printed on a new line, with indentation, including the scope
        output = "Statement_List [\n"
        for statement in self.statements:
            output +=  "\t"+str(statement).replace('\n', '\n\t')+"\n"
        output += "]"
        return output