# BinarySearch(A, Start, Finish)
# input: sorted list A, indice Start, indice Finish
# output: the singleton number
# 1. if finish < Start: return -1
# 2. if len(A) == 1: return element, if A[0] != A[1]: return A[0], if A[len - 1] != A[len - 2]: return A[len - 1]
# 3. mid = (start + finish) / 2
# 4. if A[middle_index] != A[middle_index - 1] and A[middle_index] != A[middle_index + 1]: return A[middle_index]
# 5. if A[middle_index] != A[middle_index - 1]: return BinarySearch(A, Start, Mid)
# 6. if A[middle_index] != A[middle_index + 1]: return BinarySearch(A, Mid, Finish)

import sys

filename = sys.argv[1]

try:
    with open(filename, 'r') as file:
        nums = list(map(int, file))
except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
    sys.exit(1)


def BinarySearch(A, start, finish):
    if finish < start:
        return None
    if len(A) == 1:
        return A[0]
    if A[0] != A[1]:
        return A[0]
    if A[len(A) - 1] != A[len(A) - 2]:
        return A[len(A) - 1]

    middle = (start + finish) // 2

    if A[middle] != A[middle - 1] and A[middle] != A[middle + 1]:
        return A[middle]
    
    if middle % 2 == 1:
        if A[middle] != A[middle - 1]:
            return BinarySearch(nums, start, middle - 1)
        else:
            return BinarySearch(nums, middle + 1, finish)
    else:
        if A[middle] != A[middle - 1]:
            return BinarySearch(nums, middle + 1, finish)
        else:
            return BinarySearch(nums, start, middle - 1)
            

print(BinarySearch(nums, 0, len(nums) - 1))