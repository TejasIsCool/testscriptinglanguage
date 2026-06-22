
# Should i use pythons own complex or my own?
# BTOH!
class Complex(complex):
    # Instead of 1+2j, want 1+2i
    def __str__(self) -> str:
        real_str = str(self.real)
        
        imag_str = str(self.imag) + "i"
        
        if self.real == 0 and self.imag != 0:
            return imag_str
        
        if self.imag == 0:
            return real_str
        
        if self.imag >= 0:
            return f"{real_str}+{imag_str}"
        else:
            return f"{real_str}{imag_str}"

