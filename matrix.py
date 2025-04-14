from typing import List
import numpy as np

class Matrix:
    
    def __init__(self, matrix: List):
        self._matrix = matrix
        self._rows = len(matrix)
        self._cols = len(matrix[0])

    def __len__(self):
        return (self._rows,self._cols)

    def __str__(self) -> str:
        return str(self._matrix)

    def __eq__(self, other) -> bool:
        return self._matrix == other._matrix

    def __ne__(self, other) -> bool:
        return self._matrix != other._matrix

    def __getitem__(self, index) -> float:   
        if isinstance(index, tuple):
            row, col = index
            return self._matrix[row][col]
         
        return self._matrix[index]
    
    def __setitem__(self, index, value):
        if isinstance(index, tuple):
            row, col = index
            self._matrix[row][col] = value
        return self

    def __add__(self, other):
        if isinstance(other, (int,float)):
            result = [
                [[other + elem for elem in row] for row in self._matrix]
            ]
            return Matrix(result)
        
        elif isinstance(other, Matrix): 
            if self._rows != other._rows or self._cols != other._cols:
                raise ValueError("Matrices must have the same dimensions for addition")
            result = [
                [self._matrix[i][j] + other._matrix[i][j] for j in range(self._cols)] for i in range(self._rows)
            ]
        
        else:
            raise TypeError("Unsupported operand type")
        
        return Matrix(result)
    
    def __sub__(self, other):
        if isinstance(other, (int,float)):
            result = [
                [[-other + elem for elem in row] for row in self._matrix]
            ]
            return Matrix(result)
        
        elif isinstance(other, Matrix):
            if self._rows != other._rows or self._cols != other._cols:
                raise ValueError("Matrices must have the same dimensions for subtraction")
            result = [
                [self._matrix[i][j] - other._matrix[i][j] for j in range(self._cols)] for i in range(self._rows)
            ]
        
        else:
            raise TypeError("Unsupported operand type")

        return Matrix(result)
    
    def __mul__(self,other):
        if isinstance(other, (int, float)):
            result = [
                [other * elem for elem in row] for row in self._matrix
            ]
            return Matrix(result)

        elif isinstance(other, Matrix):
            if self._rows != other._cols or self._cols != other._rows:
                raise ValueError("Matrices must have the correct shapes for multiplication")
            result = []
            row_result = []
            temp_res = []
            i,j,k = 0,0,0
            while i < self._rows:
                temp_res.append(self._matrix[i][j] * other._matrix[j][k])
                j += 1
                if j == self._cols:
                    row_result.append(sum(temp_res))
                    temp_res = []
                    k += 1
                    j = 0
                if k == other._cols:
                    result.append(row_result)
                    row_result = []
                    k = 0
                    i += 1
            # result = np.reshape(result, (self._rows,other._cols)).tolist()
            
            
            
            # i = 0
            # while i < self._rows:
            #     row_result = []
            #     k = 0
            #     while k < other._cols:
            #         temp_res = 0
            #         j = 0
            #         while j < self._cols:
            #             temp_res += self._matrix[i][j] * other._matrix[j][k]
            #             j += 1
            #         row_result.append(temp_res)
            #         k += 1
            #     result.append(row_result)
            #     i += 1

        else:
            raise TypeError("Unsupported operand type")

        return Matrix(result)

    def transpose(self):
        result = [
            [self._matrix[i][j] for i in range(self._rows)] for j in range(self._cols)
        ]
        return Matrix(result)

    def det(self) -> float:
        if self._rows != self._cols:
            raise ValueError("Determinant is only defined for square matrices")

        if self._rows == 1:
            return self._matrix[0][0]

        if self._rows == 2:
            return self._matrix[0][0] * self._matrix[1][1] - self._matrix[0][1] * self._matrix[1][0]

        determinant = 0
        for col in range(self._cols):
            minor = [row[:col] + row[col+1:] for row in self._matrix[1:]]
            minor_matrix = Matrix(minor)

            sign = (-1) ** col

            determinant += sign * self._matrix[0][col] * minor_matrix.det()

        return determinant
    
    def issingular(self) -> bool:
        if(self.det() == 0):
            return True    
        else:
            return False

    def inverse(self):
        newmatrix = []
        if(self.issingular()):
            raise ValueError("this matrix has not inverse!")
        else:
            det = self.det()
            for i in range(self._rows):
                tmplist = []
                for j in range(self._cols):
                    tmplist.append(1/det * self._matrix[i][j])
                newmatrix.append(tmplist)
        return Matrix(newmatrix)
    