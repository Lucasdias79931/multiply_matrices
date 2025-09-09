import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


from Utils import Utils
if __name__ == "__main__":
    MatrixA = [[1,2,3],
               [4,5,6],
               [7,8,9]]
    
    for i in range(len(MatrixA[0])):
        print(f"Column {i}:")
        column = Utils.getColumn(MatrixA, i)
        print(column)
    