# LaTeX Input Guide

1. Integrals (∫): "\int_{<lower_>}^{<upper_>} (<argument_>) \, d<variable_>" 
    Notes:
    1. <lower_> and <upper_> can be left empty for indefinite integrals 
        (e.g., "\int(<argument_>) \, d<variable_>")
    2. The input argument to trigonometric and logarithmic functions should be simple (e.g., sin(x) or ln(x)), 
        while for exponential functions, it should be linear (e.g., e^{ax + b})

2. Derivatives (∂): "\frac{d^{<order_>}(<function_>)}{d<variable_>^{<order_>}}"
    Notes:
    1. <oreder_> can be left empty for first-order derivatives 
        (e.g., "\frac{d<function_>}{d<variable_>}" instead of "\frac{d^{1}<function_>}{d<variable_>^{1}}").
    2. <function_> can be any valid mathematical expression
        (e.g., polynomials, trigonometric functions, exponential functions, etc.).

3. Matrices : "\begin{<bracket_type>} <entry_11> & ... & <entry_1n> // ... // <entry_n1> & ... & <entry_nm> \end{<bracket_type>}"
    Notes:
    1. For simple matrix operations (+, -, *), place the operator between two matrices
    2. For matrix functions, use these syntaxes:
        `Determinant`: \det (<matrix_syntax>)
        `Transpose`: \transpose (<matrix_syntax>)
        `Inverse`: \inverse (<matrix_syntax>)
 

# How to Run the Calculator

1. `bash`
   python calculator.py