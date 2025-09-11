from abc import ABC, abstractmethod
class Utils(ABC):
    
    """
        This class provides basic methods to split a column from a matrix
        and to multiply a line by a column.

        Other classes should implement methods to multiply two or more matrices.
    """


    def __init__(self):
        
        pass


    @staticmethod
    def scalarMultiply(line: list, column:list) -> int:
        sum = 0

        for i in range(len(line)):
            sum += line[i] * column[i]
        return sum
    

    @staticmethod
    def getColumn(Matrix: list, colIndex: int) -> list:
        if not Matrix:
            raise ValueError("Empty matrix")
        
        column = []
        for i, row in enumerate(Matrix):
            if colIndex >= len(row):
                raise IndexError(f"Column index {colIndex} out of range for row {i}")
            column.append(row[colIndex])
        
        return column

        
    
if __name__ == "__main__":
    MatrixA = [[1,2,3],
               [4,5,6],
               [7,8,9]]
    
    for i in range(len(MatrixA[0])):
        print(f"Column {i}:")
        column = Utils.getColumn(MatrixA, i)
        print(column)
    