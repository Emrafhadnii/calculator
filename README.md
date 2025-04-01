# LaTeX Input Guide

1. Integrals (∫): "\int_{<lower>}^{<upper>} (<argument>) \, d<variable>" 
    # Notes:
    1. <lower> and <upper> can be left empty for indefinite integrals 
        (e.g., "\int(<argument>) \, d<variable>")
    2. The input <argument> to trigonometric and logarithmic functions should be linear 
        (e.g., sin(ax + b) or ln(cx + d))

2. Derivatives (∂): "\frac{d^{<order>}(<function>)}{d<variable>^{<order>}}"
    # Notes:
    1. <oreder> can be left empty for first-order derivatives 
        (e.g., "\frac{d<function>}{d<variable>}" instead of "\frac{d^{1}<function>}{d<variable>^{1}}").
    2. <function> can be any valid mathematical expression
        (e.g., polynomials, trigonometric functions, exponential functions, etc.).

3. Matrices : "\begin{<bracket_type>} <entry_11> & ... & <entry_1n> // ... // <entry_n1> & ... & <entry_nm> \end{<bracket_type>}"
    # Notes:
    1. For simple matrix operations (+, -, *), place the operator between two matrices
    2. For matrix functions, use these syntaxes:
        `Determinant`: \det (<matrix syntax>)
        `Transpose`: \transpose (<matrix syntax>)
        `Inverse`: \inverse (<matrix syntax>)
 


