import re
from typing import Optional,Union,Dict
from matrix import Matrix

class LatexParser:

    def __init__(self, latex_input: str):
        self._expression = latex_input.replace(" ","")

    def derivative_parser(self) -> Dict[str, str, str, int]:
        numerator = self._expression[self._expression.find("{")+1 : self._expression.rfind("dx")-2]
        denominator = self._expression[self._expression.rfind("dx") : self._expression.rfind("}")]
        var = denominator[1]

        index = numerator.find("d^")
        if index != -1:
            if numerator[index+2] == "{":
                order = int(numerator[index+3 : numerator.find("}")])
            else:
                order = int(numerator[index+2 : numerator.find("(")])
        else:
            order = 1
        function = numerator[numerator.find("(")+1 : numerator.rfind(")")]

        return{
            'type': 'derivative',
            'function': function,
            'variable': var,
            'order': order
        }


    def integral_parser(self) -> Dict[str, str, str, float, float]:
        self._expression = self._expression.replace(" ","")
        if self._expression[self._expression.find("int") + 3] == "_":
            lindex = self._expression.find("_")
            if self._expression[lindex+1] != "{":
                lower = float(self._expression[lindex+1 : self._expression.find("^")])
            else:
                lower = float(self._expression[lindex+2 : self._expression.find("}")])
            
            uindex = self._expression.find("^")
            if self._expression[uindex+1] != "{":
                upper = float(self._expression[uindex+1 : self._expression.find("(")])
            else:
                upper = float(self._expression[uindex+2 : self._expression.find("(")-1])
        else:
            lower,upper = None,None

        var = self._expression[self._expression.rfind("d")+1:]
        function = self._expression[self._expression.find("(")+1 : self._expression.rfind(")")]

        return {
            'type': 'integral',
            'function': function,
            'variable': var,
            'lower': lower,
            'upper': upper
        }


    def matrix_parser(self) -> Dict[str, Matrix, Matrix, str]:
        self._expression = self._expression.replace(" ","")
        
        start = self._expression.find("}")
        end = self._expression.find("\\end")
        matrix_bound = self._expression[start+1 : end]
        matrix1 = [list(map(int, line.split("&"))) for line in matrix_bound.split("\\")]

        if self._expression.count("\\begin") == 1:
            matrix2 = None
            operator = self._expression[:self._expression.find("(")].replace("\\","")
        else:
            start = self._expression.find("}",self._expression.rfind("\\begin"))
            end = self._expression.rfind("\\end")
            matrix_bound = self._expression[start+1 : end]
            matrix2 = [list(map(int, line.split("&"))) for line in matrix_bound.split("\\")]

            operator = self._expression[self._expression.rfind("\\begin")-1]

        return{
            'type': 'matrix operation',
            'first': Matrix(matrix1),
            'second': Matrix(matrix2),
            'op': operator
        }


    def parse(self) -> Optional[
                            Union[
                                Dict[str, str, str, int],
                                Dict[str, str, str, float, float],
                                Dict[str, Matrix, Matrix, str]]]:
        
        function = re.findall(r'\\[a-zA-Z]+|\\.', self._expression)
        if function[0] == "\\frac":
            return self.derivative_parser()
        elif function[0] == "\\int":
            return self.integral_parser()
        elif function[0] == "\\begin":
            return self.matrix_parser()
        else:
            return None