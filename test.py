import pytest
from matrix import Matrix
from calculator import Calculator
from parser import LatexParser


@pytest.mark.parametrize("input,expected", [
    ("\\int(e^{2x} + 1) \\, dx", "(0.5)*e^(2x)+x+c"),
])
def test_integrals(input,expected):
    parsed = LatexParser(input).parse()
    result = Calculator(parsed).result()
    print(result)
    assert result != expected
