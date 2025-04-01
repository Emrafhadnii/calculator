import re

class LatexParser:

    def __init__(self, latex_input: str):
        self._expression = latex_input.replace(" ","")

    def derivative_parser(self):
        sorat = self._expression[self._expression.find("{")+1 : self._expression.rfind("dx")-2]
        makhraj = self._expression[self._expression.rfind("dx") : self._expression.rfind("}")]
        var = makhraj[1]

        index = sorat.find("d^")
        if index != -1:
            if sorat[index+2] == "{":
                order = int(sorat[index+3 : sorat.find("}")])
            else:
                order = int(sorat[index+2 : sorat.find("(")])
        else:
            order = 1
        function = sorat[sorat.find("(")+1 : sorat.rfind(")")]

        return{
            'type': 'derivative',
            'function': function,
            'variable': var,
            'order': order
        }

    def integral_parser(self):
        self._expression = self._expression.replace(" ","")
        if self._expression[self._expression.find("int") + 3] == "_":
            lindex = self._expression.find("_")
            if self._expression[lindex+1] != "{":
                lower = int(self._expression[lindex+1 : self._expression.find("^")])
            else:
                lower = int(self._expression[lindex+2 : self._expression.find("}")])
            
            uindex = self._expression.find("^")
            if self._expression[uindex+1] != "{":
                upper = int(self._expression[uindex+1 : self._expression.find("(")])
            else:
                upper = int(self._expression[uindex+2 : self._expression.find("(")-1])
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


    def matrix_parser(self):
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
            'first': matrix1,
            'second': matrix2,
            'op': operator
        }


    def parse(self):
        function = re.findall(r'\\[a-zA-Z]+|\\.', self._expression)
        if function[0] == "\\frac":
            return self.derivative_parser()
        elif function[0] == "\\int":
            return self.integral_parser()
        elif function[0] == "\\begin":
            return self.matrix_parser()

lp1 = LatexParser("\\frac{d(\cos(3x))}{dx}")
lp2 = LatexParser("\\frac{d^{10}(x^2+x+1)}{dx^{10}}")
lp3 = LatexParser("\\int (ax^2+bx+c) \, dx")
