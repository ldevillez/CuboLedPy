

def Linear(Li, Le, i, n):
  L = [0, 0, 0]
  if n == 1:
    for j in range(3):
      L[j] = Li[j]
  else:
    for j in range(3):
      L[j] = Li[j] + (Le[j] - Li[j]) * i / (n - 1)
  return L

def Quadratic(Li, Le, i, n):
  L = [0, 0, 0]
  if n == 1:
    for j in range(3):
      L[j] = Li[j]
  else:
    A = [0, 0, 0]
    B = [0, 0, 0]
    C = [0, 0, 0]
    for j in range(3):
      C[j] = Li[j]
      A[j] = (C[j] - Le[j]) * 4 / (n -1)**2
      B[j] = - 2 * A[j] * (n-1)/2
      L = A[j] * i**2 + B[j] * i + C[j]
  return L

