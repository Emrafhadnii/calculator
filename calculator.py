from parser import LatexParser
import math
from matrix import Matrix
from typing import List,Optional,Tuple,Union,Dict
import re
from settings import op_types, keys


class Calculator:
    
    parsed_expression: Dict

    @classmethod
    def result(cls) -> Optional[Union[str, float, Matrix]]:
        
        match cls.parsed_expression[keys.type.value]:
            case op_types.derivative.value:
                return cls.calculate_derivative(**cls.parsed_expression)   
            case op_types.integral.value:
                return cls.calculate_integral(**cls.parsed_expression)
            case op_types.matrix_op.value:
                return cls.matrix_calculations(**cls.parsed_expression)
            case op_types.de.value:
                return cls.calculate_de(**cls.parsed_expression)
        return None

    @staticmethod
    def _split_terms(function: str) -> List:
        s = function.replace(' ', '')
        terms, current_term = [], []
        brace_level, i, n = 0, 0, len(s)
        while i < n:
            char = s[i]
            if char == '\\':
                command_end = i + 1
                while command_end < n and s[command_end].isalpha():
                    command_end += 1
                current_term.append(s[i:command_end])
                i = command_end
                continue
                
            if char in '{(':
                brace_level += 1
            elif char in '})':
                brace_level -= 1
                
            if char in '+-*' and brace_level == 0:
                if current_term:
                    if current_term[0] == "(" and current_term[-1] == ')':
                        current_term = current_term[1:-1]
                    terms.append(''.join(current_term))
                    current_term = []
                current_term.append(char) if char == '-' else None
            else:
                current_term.append(char)
            i += 1
            
        if current_term:
            terms.append(''.join(current_term[1:-1] if current_term[0] == '(' and current_term[-1] == ')' else current_term))
        return terms

    @staticmethod
    def _polynomial_derivative(var: str, term: str) -> str:
        try:
            if term.find(var) == -1:
                term += "^0"
                index = term.find("^")
            else:
                index = term.find("^")
                if index != -1:
                    pass           
                else:
                    term += "^1"
                    index = term.find("^")
            
            power = float(term[index+1:].replace("{","").replace("}",""))
            if power == 0:
                new_power = 0
                new_base = 0
            else:
                new_power = float(power)-1
                index = term.find(var)
                if term[:index] == "":
                    term = "1" + term
                    index += 1
                new_base = float(term[:index])*power
            new_base = "" if new_base == 1 else new_base
            new_power = "" if new_power == 1 else new_power
            
            if new_base == 0:
                return ""
            if new_power == 0:
                derived = f"{new_base}"
            else:
                if new_power != "":
                    derived = f"{new_base}x^{new_power}"
                else:
                    derived = derived = f"{new_base}x"
        except:
            raise ValueError("Invalid expression")

        return derived

    @staticmethod
    def _polynominal_integral(var: str, term: str, lower: Optional[float], upper: Optional[float]) -> Tuple[float, str, float, float]:
        try:
            index = term.find("^")
            value_term = 0
            primary_term = ""
            if index == -1:
                term += "^1"
                index = term.find("^")
            else:
                pass

            if term[0] == var:
                term = "1" + term
                index += 1
            power = float(term[index+1:])
            base = float(term[:term.find(var)])
            new_power = power+1
            new_base = base/new_power

            if lower is None or upper is None:
                primary_term = f"({new_base})*{var}^({new_power})"

            else:
                value_term = (new_base*upper**new_power) - (new_base*lower**new_power)
        except:
            raise ValueError("Invalid expression")

        return value_term,primary_term,new_base,new_power

    @classmethod
    def _trigonometric_derivative(cls, var: str, term: str) -> str:
        try:
            exp = term.find("(")
            index = term.find("^") 
            derived_term = ""

            if index == -1 or index > exp:
                term = term[:exp] + "^1" + term[exp:]
                index = exp
                exp += 2

            index = term.find("^")
            start = term.find("{")
            end = term.find("}")
            if start != -1 and start < exp:
                power = float(term[start+1 : end])
            else:
                power = float(term[index+1 : exp])
            if power == 0:
                new_power = 0
            elif power == 1:
                new_power = 1
            else:
                new_power = power-1

            if term[:term.find("\\")] == "":
                term = "1" + term
            base = float(term[:term.find("\\")])
            new_base = base*power

            new_base = "" if new_base == 1 else new_base
            new_power = "" if new_power == 1 else new_power

            parenthesis_derived = cls.calculate_derivative(var=var
                ,function=term[term.find("(")+1 : term.rfind(")")])
            
            parenthesis_derived = "" if parenthesis_derived == "" else "" if parenthesis_derived == "0" else parenthesis_derived+")*"
           
            top = "1" if parenthesis_derived.replace("*","",1) == "" else parenthesis_derived.replace("*","",1)
            under_line = term.find("_")
            log_base = 10
            if under_line != -1:
                log_base = float(term[under_line+1 : term.find("^")])

            temp_dict = {"\\sin": "", "\\cos": "", "\\tan": "", "\\cot": ""}
            power_der = f"^{new_power}{term[term.find("(") : term.find(")")]})" if new_power != "" else f"^{new_power}{term[term.find("(") : term.find(")")]})".replace("^","",1)
            if power>1:
                temp_dict = {
                    "\\sin": "*sin"+power_der,
                    "\\cos": "*cos"+power_der,
                    "\\tan": "*tan"+power_der,
                    "\\cot": "cot"+power_der
                }
            func_map = {
                "\\sin": f"({parenthesis_derived}({new_base})*cos{term[term.find("(") : term.find(")")]})" + temp_dict['\\sin'],
                "\\cos": f"-({parenthesis_derived}({new_base})*sin{term[term.find("(") : term.find(")")]})" + temp_dict['\\cos'],
                "\\tan": f"({parenthesis_derived}({new_base})*(1+tan^2{term[term.find("(") : term.find(")")]}))" + temp_dict['\\tan'],
                "\\cot": f"-({parenthesis_derived}({new_base})*(1+cot^2{term[term.find("(") : term.find(")")]}))" + temp_dict['\\cot'],
                "\\log": f"({parenthesis_derived.replace("*","",1)}/{term[term.find("(") : term.rfind(")")]})*ln({log_base})",
                "\\ln": f"({top}/({term[term.find("(")+1 : term.rfind(")")]})"
            }
            funcs = re.findall(r'\\[a-zA-Z]+|\\.', term)
            derived_term = func_map[str(funcs[0])] if funcs[0] in func_map.keys() else ""

            if parenthesis_derived == "":
                derived_term = derived_term.replace("(","",1)
        except:
            raise ValueError("Invalid expression")

        return derived_term.replace("*()","").replace("()*","")

    @staticmethod
    def _trigonometric_integral(var: str, term: str, lower: Optional[float], upper: Optional[float]) -> Tuple[float, str, float, float]:
        try:
            if f"{var}^" in term:
                raise ValueError("Invalid expression")
            value_term = 0
            primary_term = ""
            if term[0] == "\\":
                term = "1" + term
            base = float(term[:term.find("\\")])
            power = 1
            
            new_power = power
            new_base = base

            under_line = term.find("_")
            log_base = 10
            if under_line != -1:
                log_base = float(term[under_line+1 : term.find("^")])

            func_map = {
                "\\sin": f"({-new_base})*cos({var})" if (lower is None or upper is None) else new_base*abs((math.cos(upper)) - (math.cos(lower))),
                "\\cos": f"({new_base})*sin({var})" if (lower is None or upper is None) else new_base*abs((math.sin(upper)) - (math.sin(lower))),
                "\\tan": f"({-new_base})*ln|cos({var})|" if (lower is None or upper is None) else new_base*abs((math.log(abs(math.cos(upper)),math.e)) - (math.log(abs(math.cos(lower)),math.e))),
                "\\cot": f"({new_base})*ln|sin({var})|" if (lower is None or upper is None) else new_base*abs((math.log(abs(math.sin(upper)),math.e)) - (math.log(abs(math.sin(lower)),math.e))),
                "\\log": f"({new_base})*({var}*(log_{log_base}({var})-(1/ln({log_base}))))" if (lower is None or upper is None) else (new_base*abs((upper*(math.log(upper,log_base)-(1/math.log(log_base,math.e)))) - (lower*(math.log(lower,log_base)-(1/math.log(log_base,math.e)))))),
                "\\ln": f"({new_base})*({var}*(ln({var})-1))" if (lower is None or upper is None) else new_base*abs((upper*(math.log(upper,math.e)-1)) - (lower*(math.log(lower,math.e)-1)))
            }

            funcs = re.findall(r'\\[a-zA-Z]+|\\.', term)
            term_result = func_map[str(funcs[0])]
            value_term = term_result if isinstance(term_result,float) else 0
            primary_term = term_result if isinstance(term_result,str) else ""
        except:
            raise ValueError("Invalid expression")

        return value_term,primary_term,new_base,new_power

    @classmethod
    def _exponential_derivative(cls, var: str, term: str) -> str:
        try:
            index = term.find("^")
            if index != -1:
                power = term[index+1:]
                if power[0] == "{" and power[-1] == "}":
                    power = power[1:-1]

                temp_der = cls.calculate_derivative(function=power, var=var)
                temp_der = "" if (temp_der == "" or temp_der =="0") else "("+temp_der+")*"
                base = term[:term.find("e")]
                new_power = power
                if base == "" or base == "1":
                    new_base = ""
                else:
                    new_base = f"(({base}))"

                derived = f"{temp_der}{new_base}e^{new_power}"
        except:
            raise ValueError("Invalid expression")
            
        return derived

    @classmethod
    def _exponential_integral(cls, var: str, term: str, lower: Optional[float], upper: Optional[float]) -> Tuple[float, str, float, float]:
        try:
            index = term.find("^")
            power = term[index+1 :].replace("{","",1).replace("}","",1)
            value_term = 0
            primary_term = ""
            try:
                base = float(term[:term.find("e")])
            except:
                base = 1

            power_der = cls.calculate_derivative(function=power, var=var)
            new_base = 1/float(power_der) * base
            new_power = power
            power_value = float(power[:power.find(var)])
            if lower is None or upper is None:
                primary_term = f"({new_base})*e^({new_power})"
            else:
                value_term = abs((new_base*math.e**(upper*power_value)) - (new_base*math.e**(lower*power_value)))
        except:
            raise ValueError("Invalid expression")

        return value_term,primary_term,new_base,new_power

    @classmethod
    def calculate_derivative(cls, function: str, var: str, **kwargs) -> str:
        derived = ""
        function = function.replace(" ","")
        terms = cls._split_terms(function)
        for term in terms:
            try:
                term = term.replace(f"-{var}",f"-1{var}")
                if function.find(f"{term}*") != -1 or function.find(f"({term})*") != -1:
                    second_term = terms[terms.index(term)+1]

                    terms.remove(second_term)
                    derived_term = "(" + cls.calculate_derivative(term, var) + f"*({second_term}))+"
                    derived_term += "(" + cls.calculate_derivative(second_term, var) + f"*({term}))"

                else:
                    operator_chars = str.maketrans('', '', '+-*')
                    if (len(term) != len(term.translate(operator_chars)) and term[0] != '-' 
                        and not term.startswith("\\") and not term.startswith("e^") 
                        and not term.startswith(f"{var}^")):
                        
                        derived_term = cls.calculate_derivative(function=term, var=var)
                    else:
                        if term.find("e^") != -1 and var != "e":
                            derived_term = cls._exponential_derivative(var, term)

                        elif term.find("\\") != -1:
                            var_index = term.find(var)
                            if var_index == -1:
                                new_power = 0
                                new_base = 0
                                derived_term = ""
                            else:
                                derived_term = cls._trigonometric_derivative(var=var, term=term)
                        else:
                            derived_term = cls._polynomial_derivative(term=term, var=var)
                        
                if derived_term != "":
                    derived += derived_term + "+"
                else:
                    derived += derived_term     
            except:
                raise ValueError("Invalid expression")
        derived = derived.replace("+-", "-").rstrip("+")
        if derived == "":
            return "0"
        if derived == "+":
            raise ValueError("unexpected function")
        return derived

    @classmethod
    def calculate_integral(cls, var: str, function: str,
                        lower: Optional[float] = None, upper: Optional[float] = None, **kwargs) -> Union[float,str]: 
        function = function.replace(" ","")
        terms = cls._split_terms(function)
        primary = ""
        value = 0
        for term in terms:
            try:
                primary_term = ""
                value_term = 0
                if term.find(var) == -1:
                    term = f"{term}{var}^0"
                
                term = term.replace(f"-{var}",f"-1{var}")

                operator_chars = str.maketrans('', '', '+-*')
                if len(term) != len(term.translate(operator_chars)) and term[0] != '-':
                    term_out = cls.calculate_integral(function=term, var=var,lower=lower,upper=upper)
                    primary_term = term_out.replace("+c","") if isinstance(term_out,str) else ""
                    value_term = term_out if isinstance(term_out,float) else 0                
                else:
                    if term.find("e^") != -1 and var != "e":
                        value_term,primary_term,new_base,new_power = cls._exponential_integral(var,term,lower,upper)
                    elif term.find("\\") != -1:
                        value_term,primary_term,new_base,new_power = cls._trigonometric_integral(var,term,lower,upper)
                    else:
                        value_term,primary_term,new_base,new_power = cls._polynominal_integral(var,term,lower,upper)
            
                    if new_base == 1:
                        primary_term = primary_term.replace(f"({new_base})*","",1)
                    if new_power == 1:
                        primary_term = primary_term.replace(f"^({new_power})","",1)
                    elif new_power == 0:
                        primary_term = primary_term.replace(f"*{var}^({new_power})","",1)        

                value += value_term
                primary += primary_term.replace("+-","-") + "+"
            except:
                raise ValueError("Invalid expression")
        if primary == "+" and value == 0:
            raise ValueError("unexpected function")
        return primary+"c" if lower is None or upper is None else round(value,2)

    @classmethod
    def calculate_de(cls, left_function: Dict, right_function: Dict, **kwargs) -> str:
        try:
            if right_function[keys.var.value] in left_function[keys.function.value]:
                raise ValueError("Invalid expression")
            left_int = cls.calculate_integral(**left_function)

            if left_function[keys.var.value] in right_function[keys.function.value]:
                raise ValueError("Invalid expression")
            right_int = cls.calculate_integral(**right_function)
        
        except:
            raise ValueError("Invalid expression")
        
        return left_int + " = " + right_int.replace("+c","")

    @classmethod
    def matrix_calculations(cls, first: List, second: List, op: str, **kwargs) -> Union[Matrix,float]:
        
        result = []
        first = Matrix(first)
        second = Matrix(second) if second != [] else second
        
        match op:
            case "*":
                result = first*second
            case "+":
                result = first+second
            case "-":
                result = first-second
            case "det":
                result = first.det()
            case "inverse":
                result = first.inverse()
            case "transpose":
                result = first.transpose()

        return result
    

while True:
    user_input = str(input("Enter LaTeX expression: "))
    if user_input == "exit":
        break
    LatexParser.latex_expression = user_input
    parsed = LatexParser.parse()
    Calculator.parsed_expression = parsed
    result = Calculator.result()
    print(f"type: {parsed['type']} \nresult: {result}")


"""
sample inputs:
1.\frac{d(\ln(3x^{12}+12x) + x^2)}{dx}
2.\frac{d((12x^2-2x+1)+(3x^2))}{dx}
3.\int_5^10((12x^2-2x+1)+(3x^2)) \, dx
4.\frac{d(e^{x^2-x})}{dx}
5.\int_5^10(\log(y)) \, dy
6.\frac{d(2y*3y)}{dy}
7.(3x)dx=(3y)dy
\frac(log(3x) + y^2))
\int(e^{2x} + 1) \, dx
\frac{d(\log(3x^{12}+12x) + x^2)}{dx}
\begin{brackets} 2 & 2 & 3 \ 5 & -1 & 6 \end{brackets}*\begin{brackets} 2 & 3 \ 3 & 7 \ 2 & 5 \end{brackets}
\begin{brackets} 2 & 2 & 3 \ 5 & -1 & 6 \ 4 & 0 & 8 \end{brackets}+\begin{brackets} 2 & 2 & 3 \ 5 & -1 & 6 \ 4 & 0 & 8 \end{brackets}
\inverse(\begin{brackets} 2 & 2 & 3 \ 5 & -1 & 6 \ 4 & 0 & 8 \end{brackets})
\int_5^10(\log(y)) \, dy
"""