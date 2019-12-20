import fileinput

def multiply(num1, num2, len1, len2):
    prod = [0] * (len1 + len2 - 1)

    for i in range(len1): 
        for j in range(len2): 
            prod[i + j] += int(num1[i])*int(num2[j])
  
    return prod;

# def karatsuba1(x, y, length, product):
#     # Base case
#     if x < 10 or y < 10:
#         return x * y
#     # Calculate the number of digits of the numbers
#     sx, sy = str(x), str(y)
#     m2 = int(max(len(sx), len(sy)) / 2)
#     # Split the digit sequences about the middle
#     ix, iy = len(sx) - m2, len(sy) - m2
#     ix = int(ix)
#     iy = int(iy)
#     a, b = int(sx[:ix]), int(sx[ix:])
#     c, d = int(sy[:iy]), int(sy[iy:])
#     print(a)
#     print(b)
#     print(c)
#     print(d)
#     # 3 products of numbers with half the size
#     A = karatsuba(a, c)
#     C = karatsuba(b, d)
#     D = karatsuba(a + b, c + d)
#     return A * 10**(2 * m2) + (D - A - C) * 10**m2 + C

def karatsuba(x, y, length):
    # Base case
    if len(x) < 20 or len(y) < 20:
        return multiply(x,y,len(x),len(y))
    # Calculate the number of digits of the numbers
    k = int(length/2)
    # Split the digit sequences about the middle
    ix, iy = len(x) - k, len(y) - k
    a, b = x[:ix], x[ix:]
    c, d = y[:iy], y[iy:]
    # print(a)
    # print(b)
    # print(c)
    # print(d)
    # 3 products of numbers with half the size
    aplusb=[x + y for x, y in zip(a, b)]
    cplusd=[x + y for x, y in zip(c, d)]
    V = karatsuba(a, c, k)
    U = karatsuba(b, d, k)
    W = karatsuba(aplusb, cplusd, k)
    #return U * 10**(2 * k) + (W - U - V) * 10**k + V
    V.append(0)
    V.extend(U)
    for i in reversed(range(2*k-1)):
        V[i+k]+=W[i]-U[i]-V[i]
    return V

inputlist = [] # original input list
for line in fileinput.input():
    inputlist.append(line.strip())

degree = int(inputlist[0])
first_poly = inputlist[1]
second_poly = inputlist[2]
first_poly = first_poly.split()
second_poly = second_poly.split()
first_poly_len = len(first_poly)
second_poly_len = len(second_poly)

first_poly = [int(i) for i in first_poly]
second_poly = [int(i) for i in second_poly]
#print(karatsuba(first_poly,second_poly,first_poly_len))
prod = karatsuba(first_poly,second_poly,first_poly_len)
for i in range(0, len(prod)): 
    prod[i] = str(prod[i])
prod = ' '.join(prod)
print(prod)
