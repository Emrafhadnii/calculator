from parser import LatexParser
import math
from matrix import Matrix


class Calculator:
    def __init__(self, parsed_input):
        self.parsed_input = parsed_input
        self.type = parsed_input.get('type')
    

    def result(self):
        if self.type == 'derivative':
            return self.calculate_derivative()
        elif self.type == 'integral':
            return self.calculate_integral()
        elif self.type == 'matrix operation':
            return self.matrix_calculations()
        else:
            return None


    def polynomial_computation(self):
        pass


    def _split_terms(self, latex_str):
        s = latex_str.replace(' ', '')
        terms = []
        current_term = []
        brace_level = 0
        
        i = 0
        n = len(s)
        while i < n:
            char = s[i]
            
            if char == '\\':
                command_end = i + 1
                while command_end < n and s[command_end].isalpha():
                    command_end += 1
                command = s[i:command_end]
                current_term.append(command)
                i = command_end
                continue
            
            if char == '{' or char == '(':
                brace_level += 1
            elif char == '}' or char == ')':
                brace_level -= 1
            
            if (char == '+' or char == '-') and brace_level == 0:
                if current_term:
                    terms.append(''.join(current_term))
                    current_term = []
                if char == '-':
                    current_term.append(char)
            else:
                current_term.append(char)
            i += 1
        if current_term:
            terms.append(''.join(current_term))
        
        return terms


    def _polynomial_derivative(self, term: str):
        var = self.parsed_input['variable']
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

        return derived


    def _polynominal_integral(self, term: str, lower, upper):
        index = term.find("^")
        var = self.parsed_input['variable']
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

        return value_term,primary_term,new_base,new_power


    def _trigonometric_derivative(self, term: str):
        exp = term.find("(")
        index = term.find("^") 
        var = self.parsed_input['variable']
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

        obj = Calculator({
            'type': 'derivative',
            'function': term[term.find("(")+1 : term.rfind(")")],
            'variable': var,
            'order': 1
        })
        parenthesis_derived = obj.calculate_derivative()
        
        parenthesis_derived = "" if parenthesis_derived == "" else "" if parenthesis_derived == "0" else parenthesis_derived+")*"

        if term.find("\\sin") != -1:
            temp_der = ""
            if power > 1:
                temp_der = f"*sin^{new_power}{term[term.find("(") : term.find(")")]})"

            if new_power == "":
                temp_der = temp_der.replace("^","",1)

            derived_term = f"({parenthesis_derived}({new_base})*cos{term[term.find("(") : term.find(")")]})" + temp_der

        elif term.find("\\cos") != -1:
            temp_der = ""
            if power > 1:
                temp_der = f"*cos^{new_power}{term[term.find("(") : term.find(")")]})"

            if new_power == "":
                temp_der = temp_der.replace("^","",1)

            derived_term = f"-({parenthesis_derived}({new_base})*sin{term[term.find("(") : term.find(")")]})" + temp_der

        elif term.find("\\tan") != -1:
            temp_der = ""
            if power > 1:
                temp_der = f"*tan^{new_power}{term[term.find("(") : term.find(")")]})"
            
            if new_power == "":
                temp_der = temp_der.replace("^","",1)

            derived_term = f"({parenthesis_derived}({new_base})*(1+tan^2{term[term.find("(") : term.find(")")]}))" + temp_der

        elif term.find("\\cot") != -1:
            temp_der = ""
            if power > 1:
                temp_der = f"cot^{new_power}{term[term.find("(") : term.find(")")]})"
            
            if new_power == "":
                temp_der = temp_der.replace("^","",1)

            derived_term = f"-({parenthesis_derived}({new_base})*(1+cot^2{term[term.find("(") : term.find(")")]}))" + temp_der

        elif term.find("\\log") != -1:
            under_line = term.find("_")
            log_base = 10
            if under_line != -1:
                log_base = float(term[under_line+1 : term.find("^")])

            parenthesis_derived = parenthesis_derived.replace("*","",1)
            derived_term = f"({parenthesis_derived}/{term[term.find("(") : term.rfind(")")]})*ln({log_base})"
            

        elif term.find("\\ln") != -1:
            parenthesis_derived = parenthesis_derived.replace("*","",1)
            top = "1" if parenthesis_derived == "" else parenthesis_derived
            derived_term = f"({top}/({term[term.find("(")+1 : term.rfind(")")]})"

        if parenthesis_derived == "":
            derived_term = derived_term.replace("(","",1)

        return derived_term.replace("*()","").replace("()*","")


    def _trigonometric_integral(self, term: str, lower, upper):
        var = self.parsed_input['variable']
        value_term = 0
        primary_term = ""
        if term[0] == "\\":
            term = "1" + term
        base = float(term[:term.find("\\")])
        power = 1
        
        new_power = power
        new_base = base

        if term.find("\\sin") != -1:
            if lower is None or upper is None:
                primary_term = f"({-new_base})*(cos({var})"
            else:
                value_term = new_base*abs((math.cos(upper)) - (math.cos(lower)))

        elif term.find("\\cos") != -1:
            if lower is None or upper is None:
                primary_term = f"({new_base})*sin({var})"
            else:
                value_term = new_base*abs((math.sin(upper)) - (math.sin(lower)))

        elif term.find("\\tan") != -1:
            if lower is None or upper is None:
                primary_term = f"({-new_base})*ln|cos({var})|"
            else:
                value_term = new_base*abs((math.log(math.cos(upper),math.e)) - (math.log(math.cos(lower),math.e)))

        elif term.find("\\cot") != -1:
            if lower is None or upper is None:
                primary_term = f"({new_base})*ln|sin({var})|"
            else:
                value_term = new_base*abs((math.log(math.sin(upper),math.e)) - (math.log(math.sin(lower),math.e)))

        elif term.find("\\log") != -1:
            under_line = term.find("_")
            log_base = 10
            if under_line != -1:
                log_base = float(term[under_line+1 : term.find("^")])

            if lower is None or upper is None:
                primary_term = f"({new_base})*({var}*(log_{log_base}({var})-(1/ln({log_base}))))"
            else:
                
                value_term = new_base*abs((upper*(math.log(upper,log_base)-(1/math.log(log_base,math.e)))) 
                                          - 
                                          (lower*(math.log(lower,log_base)-(1/math.log(log_base,math.e)))))
            
        elif term.find("\\ln") != -1:
            if lower is None or upper is None:
                primary_term = f"({new_base})*({var}*(ln({var})-1))"
            else:
                value_term = new_base*abs((upper(math.log(upper,math.e)-1)) - (lower(math.log(lower,math.e)-1)))

        return value_term,primary_term,new_base,new_power


    def _exponential_derivative(self, term: str):
        index = term.find("^")
        if index != -1:
            power = term[index+1:]
            var = self.parsed_input['variable']
            if power[0] == "{" and power[-1] == "}":
                power = power[1:-1]
            obj = Calculator({
                        'type': 'derivative',
                        'function': power,
                        'variable': var,
                        'order': 1
                    })
            temp_der = obj.calculate_derivative()
            temp_der = "" if (temp_der == "" or temp_der =="0") else "("+temp_der+")*"
            base = term[:term.find("e")]
            new_power = power
            if base == "" or base == "1":
                new_base = ""
            else:
                new_base = f"(({base}))"


            derived = f"{temp_der}{new_base}e^{new_power}"
            return derived


    def _exponential_integral(self, term: str, lower, upper):
        index = term.find("^")
        power = term[index+1 :].replace("{","",1).replace("}","",1)
        var = self.parsed_input['variable']
        value_term = 0
        primary_term = ""
        try:
            base = float(term[:term.find("e")])
        except:
            base = 1
        obj = Calculator({
            'type': 'derivative',
            'function': power,
            'variable': var,
            'order': 1
        })
        power_der = obj.calculate_derivative()
        new_base = 1/float(power_der) * base
        new_power = power
        power_value = float(power[:power.find(var)])
        if lower is None or upper is None:
            primary_term = f"({new_base})*e^({new_power})"
        else:
            value_term = abs((new_base*math.e**(upper*power_value)) - (new_base*math.e**(lower*power_value)))

        return value_term,primary_term,new_base,new_power


    def calculate_derivative(self):
        derived = ""
        function = str(self.parsed_input['function'])    
        function = function.replace(" ","")
        terms = self._split_terms(function)
        var = self.parsed_input['variable']
        for term in terms:

            term = term.replace(f"-{var}",f"-1{var}")

            if term.find("e^") != -1 and var != "e":
                derived_term = self._exponential_derivative(term)

            elif term.find("\\") != -1:
                var_index = term.find(var)
                if var_index == -1:
                    new_power = 0
                    new_base = 0
                else:
                    derived_term = self._trigonometric_derivative(term)
            else:
                derived_term = self._polynomial_derivative(term)
                
            if derived_term != "":
                derived += derived_term + "+"
            else:
                derived += derived_term     

        derived = derived.replace("+-","-")
        if derived != "":
            if derived[-1] == "+":
                derived = derived[:-1]
        if derived == "":
            return "0"
        return derived


    def calculate_integral(self):
        function = str(self.parsed_input['function'])    
        function = function.replace(" ","")
        terms = self._split_terms(function)
        var = self.parsed_input['variable']
        lower = self.parsed_input['lower']
        upper = self.parsed_input['upper']
        primary = ""
        value = 0
        for term in terms:
            primary_term = ""
            value_term = 0
            if term.find(var) == -1:
                term = f"{term}{var}^0"
            
            term = term.replace(f"-{var}",f"-1{var}")

            if term.find("e^") != -1 and var != "e":
                value_term,primary_term,new_base,new_power = self._exponential_integral(term,lower,upper)
            elif term.find("\\") != -1:
                value_term,primary_term,new_base,new_power = self._trigonometric_integral(term,lower,upper)
            else:
                value_term,primary_term,new_base,new_power = self._polynominal_integral(term,lower,upper)
                

            if new_base == 1:
                primary_term = primary_term.replace(f"({new_base})*","",1)
            if new_power == 1:
                primary_term = primary_term.replace(f"^({new_power})","",1)
            if new_power == 0:
                primary_term = primary_term.replace(f"*{var}^({new_power})","",1)        

            value += value_term
            primary += primary_term + "+"
            primary = primary.replace("+-","-")

        return primary+"c" if lower is None or upper is None else value


    def matrix_calculations(self):
        matrix1 = Matrix(self.parsed_input['first'])
        matrix2 = Matrix(self.parsed_input['second'])
        op = self.parsed_input['op']
        
        result = []
        match op:
            case "*":
                result = matrix1*matrix2
            case "+":
                result = matrix1+matrix2
            case "-":
                result = matrix1-matrix2
            case "det":
                result = matrix1.det()
            case "inverse":
                result = matrix1.inverse()
            case "transpose":
                result = matrix1.transpose()

        return result
    

lp1 = LatexParser("\\frac{d(\\log(3x^{12}+12x) + x^2)}{dx}")
lp2 = LatexParser("\\frac{d(12x^2-2x+1)}{dx}")
lp3 = LatexParser("\\int_0^1(e^{2x} + 1) \, dx")
lp4 = LatexParser("\\frac{d(e^{x^2-x})}{dx}")
lp5 = LatexParser("\\int_5^10(\\log(x)) \, dx")

print(lp5.parse())
calc1 = Calculator(lp5.parse())
print(calc1.result())