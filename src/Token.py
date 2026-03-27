# It is good to store the line numbers and stuff in the tokens
# For error reporting
# Maybe even store the character index?

class Token:
    """The Base class for all token types"""    
    def __init__(self, name: str, line_number: int) -> None:
        self.name = name
        self.line_number = line_number

    def __str__(self) -> str:
        return "["+self.name+"]"

    def __repr__(self) -> str:
        return self.__str__()

class IdentifierToken(Token):
    def __init__(self, id_name: str, line_number: int) -> None:
        super().__init__("Identifier", line_number)
        self.id_name = id_name
        
    def __str__(self) -> str:
        return f"[Identifier: {self.id_name}]"
        
class KeywordToken(Token):
    def __init__(self, name: str, line_number: int) -> None:
        super().__init__(name, line_number)

class LiteralToken(Token):
    def __init__(self, name: str, value: str|float|bool, line_number: int) -> None:
        super().__init__(name, line_number)
        self.value = value

    def __str__(self) -> str:
        val_str = str(self.value)
        if len(val_str) > 20:
            val_str = val_str[:17] + "..."
        return f"[{self.name}: {val_str}]"


class OperatorToken(Token):
    def __init__(self, name: str, tok_type: str,  line_number: int) -> None:
        """
        Args:
            name (str): Name of token, as in "+","-",...
            tok_type (str): "Bop" for binary operators, "Ass" for assignments, "Uop" for unary operators
            line_number (int): _description_
        """        
        super().__init__(name, line_number)
        self.tok_type = tok_type
    
    def __str__(self) -> str:
        return f"[Op: {self.name} Type: {self.tok_type}]"

class PunctuationToken(Token):
    def __init__(self, name: str, line_number: int) -> None:
        super().__init__(name, line_number)

# Is important punctuation
class SemicolonToken(PunctuationToken):
    def __init__(self, line_number: int) -> None:
        super().__init__("Semicolon", line_number)