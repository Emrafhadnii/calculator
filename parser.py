import re
from typing import Optional,Union,Dict
from matrix import Matrix
from settings import op_types, keys

class LatexParser:

    latex_expression: str

    @classmethod
    def dif_eq(cls):
        try:
            index = cls.latex_expression.find("=")
            left_side = cls.latex_expression[:index]
            right_side = cls.latex_expression[index+1:]
            if left_side.find("dx") != -1:
                left_side = left_side.replace("dx","")
                right_side = right_side.replace("dy","")
                left_int = cls.integral_parser("\\int"+left_side+ " \, dx")
                right_int = cls.integral_parser("\\int"+right_side+" \, dy")
            elif left_side.find("dy") != -1:
                left_side = left_side.replace("dy","")
                right_side = right_side.replace("dx","")
                left_int = cls.integral_parser("\\int"+left_side+ " \, dy")
                right_int = cls.integral_parser("\\int"+right_side+" \, dx")
            else:
                raise ValueError("Invalid input")
        except:
            raise ValueError("Invalid input")
        return {
            keys.type.value: op_types.de.value,
            keys.left_function.value: left_int,
            keys.right_function.value: right_int,
        }

    @staticmethod
    def derivative_parser(expression: str) -> Dict[str, Union[str, int]]:
        try:
            numerator = expression[expression.find("{")+1 : expression.rfind("d")-2]
            denominator = expression[expression.rfind(f"d") : expression.rfind("}")]
            var = denominator[1]

            index = numerator.find("d^")
            if index != -1:
                if numerator[index+2] == "{":
                    order = int(numerator[index+3 : numerator.find("}")])
                else:
                    order = int(numerator[index+2 : numerator.find("(")])
            elif numerator.find("d") != -1:
                order = 1
            else:
                raise ValueError("Invalid input")
            function = numerator[numerator.find("(")+1 : numerator.rfind(")")]
        except:
            raise ValueError("Invalid input")
        if var not in function:
            raise ValueError("Invalid dif")
        
        return{
            keys.type.value: op_types.derivative.value,
            keys.function.value: function,
            keys.var.value: var,
            keys.order.value: order
        }

    @staticmethod
    def integral_parser(expression: str) -> Dict[str, Union[str, float]]:
        try:
            expression = expression.replace(" ","")
            if expression[expression.find("int") + 3] == "_":
                lindex = expression.find("_")
                if expression[lindex+1] != "{":
                    lower = float(expression[lindex+1 : expression.find("^")])
                else:
                    lower = float(expression[lindex+2 : expression.find("}")])
                
                uindex = expression.find("^")
                if expression[uindex+1] != "{":
                    upper = float(expression[uindex+1 : expression.find("(")])
                else:
                    upper = float(expression[uindex+2 : expression.find("(")-1])
            else:
                lower,upper = None,None

            var = expression[expression.rfind("d")+1:]
            function = expression[expression.find("(")+1 : expression.rfind(")")]
        except:
            raise ValueError("Invalid input")

        if var not in function:
            raise ValueError("Invalid dif")

        return {
            keys.type.value: op_types.integral.value,
            keys.function.value: function,
            keys.var.value: var,
            keys.lower.value: lower,
            keys.upper.value: upper
        }

    @staticmethod
    def matrix_parser(expression: str) -> Dict[str, Union[str, Matrix]]:
        expression = expression.replace(" ","")
        
        start = expression.find("}")
        end = expression.find("\\end")
        matrix_bound = expression[start+1 : end]
        matrix1 = [list(map(int, line.split("&"))) for line in matrix_bound.split("\\")]

        if expression.count("\\begin") == 1:
            matrix2 = None
            operator = expression[:expression.find("(")].replace("\\","")
        elif expression.count("\\begin") == 2:
            start = expression.find("}",expression.rfind("\\begin"))
            end = expression.rfind("\\end")
            matrix_bound = expression[start+1 : end]
            matrix2 = [list(map(int, line.split("&"))) for line in matrix_bound.split("\\")]

            operator = expression[expression.rfind("\\begin")-1]
        else:
            raise ValueError("Invalid input")
        
        return{
            keys.type.value: op_types.matrix_op.value,
            keys.first.value: Matrix(matrix1),
            keys.second.value: Matrix(matrix2),
            keys.op.value: operator
        }

    @classmethod
    def parse(cls) -> Optional[
                            Union[
                                Dict[str, Union[str, int]],
                                Dict[str, Union[str, float]],
                                Dict[str, Union[str, Matrix]]]]:
        
        cls.latex_expression = cls.latex_expression.replace(" ","")
        
        if cls.latex_expression.find("=") != -1:
            return cls.dif_eq()
        
        function = re.findall(r'\\[a-zA-Z]+|\\.', cls.latex_expression)       
        match function[0]:
            case "\\frac":
                return cls.derivative_parser(cls.latex_expression)
            case "\\int":
                return cls.integral_parser(cls.latex_expression)
            case "\\begin":
                return cls.matrix_parser(cls.latex_expression)
            
        return None
    
