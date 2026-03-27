# It is good to store the line numbers and stuff in the tokens
# For error reporting
# Maybe even store the character index?

class Token:
    """The Base class for all token types"""    
    def __init__(self, name: str, line_number: int) -> None:
        self.name = name
        self.line_number = line_number

class IdentifierToken(Token):
    def __init__(self, id_name: str, line_number: int) -> None:
        super().__init__("Identifier", line_number)
        self.id_name = id_name
        
class KeywordToken(Token):
    def __init__(self, name: str, line_number: int) -> None:
        super().__init__(name, line_number)

class LiteralToken(Token):
    def __init__(self, name: str, value: str|float|bool, line_number: int) -> None:
        super().__init__(name, line_number)
        self.value = value

class OperatorToken(Token):
    def __init__(self, name: str, line_number: int) -> None:
        super().__init__(name, line_number)

class PunctuationToken(Token):
    def __init__(self, name: str, line_number: int) -> None:
        super().__init__(name, line_number)

# Is important punctuation
class SemicolonToken(PunctuationToken):
    def __init__(self, line_number: int) -> None:
        super().__init__("Semicolon", line_number)