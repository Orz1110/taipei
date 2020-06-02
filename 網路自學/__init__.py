# def pattern(n):
#     k = 2*n-2
#     for i in range(0, n):
#         for j in range(0, k):
#             print(end=" ")
#         k = k-2
#         for j in range(0, i+n):
#             print("* ", end="")
#         print("\r")
# n = 5
# pattern(n)

def pattern(n):
    k = 2 * n - 2
    for i in range(0, n):
        for j in range(0, k):
            print(end=" ")
        for j in range(0, i+1):
            print("* ", end="")
        for j in range(0, i):
            print("* ", end="")
        print("\r")
        k -= 2

n = input("請輸入: ")
pattern(int(n))