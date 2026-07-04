from enum import Enum
# Should i use pythons own complex or my own?
# BTOH!
from typing import Union

# Complex numbers can do math with other complex numbers, floats, and ints
ComplexLike = Union[complex, float, int]

class ComplexNum(complex):
    def __str__(self) -> str:
        real_str = str(self.real)
        imag_str = str(self.imag) + "i"
        
        if self.real == 0 and self.imag != 0:
            return imag_str
        if self.imag == 0:
            return real_str
        
        if self.imag >= 0:
            return f"{real_str}+{imag_str}"
        return f"{real_str}{imag_str}"

    # --- Pyright-Friendly Boilerplate ---
    # We explicitly define the signatures, but let the C-optimized 
    # base class handle the actual math via super()
    
    def __add__(self, other: ComplexLike) -> "ComplexNum":
        return ComplexNum(super().__add__(other))
        
    def __radd__(self, other: ComplexLike) -> "ComplexNum":
        return ComplexNum(super().__radd__(other))
        
    def __sub__(self, other: ComplexLike) -> "ComplexNum":
        return ComplexNum(super().__sub__(other))
        
    def __rsub__(self, other: ComplexLike) -> "ComplexNum":
        return ComplexNum(super().__rsub__(other))
        
    def __mul__(self, other: ComplexLike) -> "ComplexNum":
        return ComplexNum(super().__mul__(other))
        
    def __rmul__(self, other: ComplexLike) -> "ComplexNum":
        return ComplexNum(super().__rmul__(other))
        
    def __truediv__(self, other: ComplexLike) -> "ComplexNum":
        return ComplexNum(super().__truediv__(other))
        
    def __rtruediv__(self, other: ComplexLike) -> "ComplexNum":
        return ComplexNum(super().__rtruediv__(other))
        
    def __pow__(self, other: ComplexLike, mod: None = None) -> "ComplexNum":
        return ComplexNum(super().__pow__(other, mod))
        
    def __rpow__(self, other: ComplexLike, mod: None = None) -> "ComplexNum":
        return ComplexNum(super().__rpow__(other, mod))
        
    def __neg__(self) -> "ComplexNum":
        return ComplexNum(super().__neg__())
        
    def __pos__(self) -> "ComplexNum":
        return ComplexNum(super().__pos__())
    

class ErrorType(Enum):
    SynErr = 1
    TypeErr = 2



class ErrorManager:

    errors: list[Error] = []
    code_lines: list[str] = []
    
    
    @staticmethod
    def add_error(error: Error):
        ErrorManager.errors.append(error)
    
    @staticmethod
    def has_errors() -> bool:
        return len(ErrorManager.errors) > 0
    
    @staticmethod
    def print_errors():
        for error in ErrorManager.errors:
            print(f"Error: {error.message}")
            print(f"Error Line: {ErrorManager.code_lines[error.line_number-1] if error.line_number-1 < len(ErrorManager.code_lines) else 'Unknown line'}")


class Error(Exception):
    
    def __init__(self, error_type: ErrorType, line_number: int, message: str, *args: object) -> None:
        self.error_type = error_type
        self.line_number = line_number if line_number != -1 else len(ErrorManager.code_lines)-1 # THe last line!
        self.message = message +f" [At line {self.line_number}: {ErrorManager.code_lines[line_number-1] if line_number-1 < len(ErrorManager.code_lines) else 'Unknown line'}]"
        ErrorManager.add_error(self)
        super().__init__(self.message, *args)
    pass



# Truthyness
# Empty things(array, string, sets, dictionary), False, None are Falsy
# Else truthy
# Actually, do i want that?
# Ig no, enforce types ig
# So only falsy: False and None? Or only False?
# Orrrrrrrrrrrrr
# Maybe make it worse than js, ocnvert EVERYTHING!
# nah, lets enforce type strictness
# one exception? string with + operator should convert right? ALl to toStr? welp idk
# maybe toStr is a function
# ok nvm will allow str+num things

