from typing import Union
import math

NumberType = float | int
ReturnType = Union["ComplexNumber", NumberType]


class ComplexNumber:
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary
        self.default_exponent = 2
        self.T = self.real, self.imaginary

    def flip_neg_pos(self) -> None:
        real = self.real - (self.real * 2)
        imaginary = self.imaginary - (self.imaginary * 2)
        self.real = real
        self.imaginary = imaginary
        self.T = self.real, self.imaginary

    def __rtruediv__(self, other: ReturnType) -> ReturnType:
        total = other / sum(self.T)
        imaginary = total - (total * 2)
        return ComplexNumber(real=total, imaginary=imaginary)

    def __rsub__(self, other: ReturnType) -> ReturnType:
        complex_number = self.__sub__(other)
        complex_number.flip_neg_pos()
        return complex_number

    def __radd__(self, other: ReturnType) -> ReturnType:
        return self.__add__(other)

    def __rmul__(self, other: ReturnType) -> ReturnType:
        return self.__mul__(other)

    def __add__(self, other: ReturnType) -> ReturnType:
        if isinstance(other, ComplexNumber):
            real_sum = self.real + other.real
            imaginary = self.imaginary + other.imaginary
            return ComplexNumber(real_sum, imaginary)
        if isinstance(other, NumberType):
            return ComplexNumber(self.real + other, self.imaginary)

    def __eq__(self, other: ReturnType) -> bool:
        if isinstance(other, ComplexNumber):
            real_sum = self.real == other.real
            imaginary = self.imaginary == other.imaginary
            return real_sum is imaginary

        return False

    def __mul__(self, other: ReturnType) -> ReturnType:
        if isinstance(other, ComplexNumber):
            real_sum = self.real * other.real
            imaginary = self.imaginary * other.imaginary
            return ComplexNumber(real_sum, imaginary)
        if isinstance(other, NumberType):
            real_sum = self.real * other
            imaginary = self.imaginary * other
            return ComplexNumber(real_sum, imaginary)

    def __sub__(self, other: ReturnType) -> ReturnType:
        if isinstance(other, ComplexNumber):
            real_sum = self.real - other.real
            imaginary = self.imaginary - other.imaginary
            return ComplexNumber(real_sum, imaginary)
        if isinstance(other, NumberType):
            return ComplexNumber(self.real - other, self.imaginary)

    def __truediv__(self, other: ReturnType) -> ReturnType:
        if isinstance(other, ComplexNumber):
            real = 0
            imaginary = 0

            real_t = self.real, other.real
            imaginary_t = self.imaginary, other.imaginary

            if not any(e == 0 for e in real_t):
                l, r = real_t
                real = l / r

            if not any(e == 0 for e in imaginary_t):
                l, r = imaginary_t
                imaginary = l / r

            elif not real and imaginary:
                return ComplexNumber(imaginary, real)

            return ComplexNumber(real, imaginary)

        if isinstance(other, NumberType):
            r = self.real / other if other > 0 else 0
            l = self.imaginary / other if other > 0 else 0
            return ComplexNumber(r, l)

    def __abs__(self) -> NumberType:
        square_real = self.real**2
        imaginary_real = self.imaginary**2
        summed_squares = square_real + imaginary_real
        sum_sqr_root = math.sqrt(summed_squares)
        return sum_sqr_root

    def conjugate(self) -> "ComplexNumber":
        imaginary = self.imaginary
        if imaginary == 0:
            return self

        imaginary = imaginary - (imaginary * 2)
        self.imaginary = imaginary
        return self

    def polar_form(self):
        magnitude = self.__abs__()
        angle = math.atan2(self.imaginary, self.real)
        polar_form = (magnitude, angle)
        return polar_form

    def exp(self, n: Union[None, NumberType] = None):

        if all(elem == 0 for elem in (self.real, self.imaginary)):
            return ComplexNumber(1, 0)

        if self.real == 1 and self.imaginary == 0:
            return ComplexNumber(math.e, 0)

        if n is None:
            n = self.default_exponent

        polar_form = self.polar_form()
        magnitude, angle = polar_form
        raised_magnitude = magnitude**n
        raised_angle = angle * n
        real_part = raised_magnitude * math.cos(raised_angle)
        imaginary_part = raised_magnitude * math.sin(raised_angle)
        return ComplexNumber(real=real_part, imaginary=imaginary_part)

    def __str__(self):
        return f"{self.real} + {self.imaginary}i"


if __name__ == "__main__":
    inst = 5 / ComplexNumber(1, 1)
    print(str(inst))
