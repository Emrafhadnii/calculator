import pytest
from matrix import Matrix
from calculator import Calculator
from parser import LatexParser
from enums import keys

@pytest.mark.parametrize("input,expected", [
    ("\\int(e^{2x} + 1) \\, dx","(0.5)*e^(2x)+x+c"),
    ("\\int_5^10(\\log(y)) \\, dy",4.33),
    ("\\int(\\sin(x)) \\, dx","(-1.0)*cos(x)+c"),
    ("\\int(e2x + 1) \\, dx",ValueError),
    ("\\int_5^0(\\log(y)) \\, dy",ValueError),
    ("\\int(\\sec(x)) \\, dx",ValueError),
    ("\\int(\\cos(x^{12})) \\, dx",ValueError),
])
def test_integrals_calc(input, expected):
    LatexParser.latex_expression = input
    parsed = LatexParser.parse()
    Calculator.parsed_expression = parsed
    if expected == ValueError:
        with pytest.raises(ValueError):
            Calculator.result()
    else:
        result = Calculator.result()
        assert result == expected

@pytest.mark.parametrize("input,expected", [
    ("\\frac{d(\\log(3x^{12}+12x) + x^2)}{dx}","(36.0x^11.0+12.0)/(3x^{12}+12x)*ln(10)+2.0x"),
    ("\\frac{d(2y*3y)}{dy}","(2.0*(3y))+(3.0*(2y))"),
    ("\\frac{d(e^{x^2-x})}{dx}","(2.0x-1.0)*e^x^2-1x"),
    ("\\frac{d((12x^2-2x+1)+(3x^2))}{dx}","24.0x-2.0+6.0x"),
    ("\\frac{d(\\log(3x) + y^2)}{dx}",ValueError),
    ("\\frac{d(2y^3y)}{dy}",ValueError),
    ("\\frac{d(x^{x^2-x})}{dx}",ValueError),
])
def test_derivatives_calc(input, expected):
    LatexParser.latex_expression = input
    parsed = LatexParser.parse()
    Calculator.parsed_expression = parsed
    if expected == ValueError:
        with pytest.raises(ValueError):
            Calculator.result()
    else:
        result = Calculator.result()
        assert result == expected


@pytest.mark.parametrize("input,expected", [
    ("(3x)dx=(3y)dy","(1.5)*x^(2.0)+c = (1.5)*y^(2.0)"),
    ("\\frac{d(2y*3y)}{dy}","(2.0*(3y))+(3.0*(2y))"),
    ("\\int(\\cos(x^{12})) \\, dx=\\log(3y)dy",ValueError),
    ("(3y)(7x)dx=(3y)dy",ValueError),
])
def test_de_calc(input, expected):
    LatexParser.latex_expression = input
    parsed = LatexParser.parse()
    Calculator.parsed_expression = parsed
    if expected == ValueError:
        with pytest.raises(ValueError):
            Calculator.result()
    else:
        result = Calculator.result()
        assert result == expected


@pytest.mark.parametrize("input,expected", [
    ("\\int(e^{2x} + 1) \\, dx","e^{2x}+1"),
    ("\\int_5^10(\\log(y)) \\, dy","\\log(y)"),
    ("\\int(\\sin(x)) \\, dx","\\sin(x)"),
    ("\\frac(e^{2x} + 1) \\, dx",ValueError),
    ("\\int_^(\\log(y)) \\, dy",ValueError),
    ("\\int(\\sec(y)) \\, dx",ValueError),
    ("\\frac(log(3x) + y^2))",ValueError),
    ("\\frac{d(2y^3y)}{dx}",ValueError),
    ("\\frac{d(x^{2^x-x})}{dx}","x^{2^x-x}"),
    ("(3x)dy=(3y)dx",ValueError),
])
def test_parser(input, expected):   
    LatexParser.latex_expression = input
    if expected == ValueError:
        with pytest.raises(ValueError):
                LatexParser.parse()
    else:
        parsed = LatexParser.parse()
        assert parsed[keys.function.value] == expected