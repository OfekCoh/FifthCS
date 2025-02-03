from z3 import *

def bmc(k):
    s = Solver()
    PC1 = [Int(f'PC1_{i}') for i in range(k+1)]
    PC2 = [Int(f'PC2_{i}') for i in range(k+1)]
    x = [Int(f'x_{i}') for i in range(k+1)]
    y = [Int(f'y_{i}') for i in range(k+1)]
    z = [Int(f'z_{i}') for i in range(k+1)]

    s.add(PC1[0] == 1, PC2[0] == 1)
    s.add(x[0] == 0, y[0] == 0, z[0] == 0)

    for i in range(k):
        # Transitions for Process 1
        s.add(Or(
            And(PC1[i] == 1, x[i+1] == 1, PC1[i+1] == 2, PC2[i+1] == PC2[i], y[i+1] == y[i], z[i+1] == z[i]),
            And(PC1[i] == 2, Or(y[i] != 0, y[i] == 1), PC1[i+1] == 2, PC2[i+1] == PC2[i], x[i+1] == x[i], y[i+1] == y[i], z[i+1] == z[i]),
            And(PC1[i] == 2, y[i] == 0, PC1[i+1] == 3, PC2[i+1] == PC2[i], x[i+1] == x[i], y[i+1] == y[i], z[i+1] == z[i]),
            And(PC1[i] == 3, z[i+1] == 1, PC1[i+1] == 4, PC2[i+1] == PC2[i], x[i+1] == x[i], y[i+1] == y[i]),
            And(PC1[i] == 4, x[i] != 1, PC1[i+1] == 4, PC2[i+1] == PC2[i], x[i+1] == x[i], y[i+1] == y[i], z[i+1] == z[i]),
            And(PC1[i] == 4, x[i] == 1, PC1[i+1] == 5, PC2[i+1] == PC2[i], x[i+1] == x[i], y[i+1] == y[i], z[i+1] == z[i]),
            And(PC1[i] == 5, y[i+1] == 1, PC1[i+1] == 6, PC2[i+1] == PC2[i], x[i+1] == x[i], z[i+1] == z[i]),
            And(PC1[i] == 6, z[i] != 1, PC1[i+1] == 6, PC2[i+1] == PC2[i], x[i+1] == x[i], y[i+1] == y[i], z[i+1] == z[i]),
            And(PC1[i] == 6, z[i] == 1, PC1[i+1] == 7, PC2[i+1] == PC2[i], x[i+1] == x[i], y[i+1] == y[i], z[i+1] == z[i]),
            And(PC1[i] == 7, PC1[i+1] == 1, PC2[i+1] == PC2[i], x[i+1] == x[i], y[i+1] == y[i], z[i+1] == z[i]),
            PC1[i+1] == PC1[i]
        ))
        # Transitions for Process 2
        s.add(Or(
            And(PC2[i] == 1, x[i+1] == 2, PC2[i+1] == 2, PC1[i+1] == PC1[i], y[i+1] == y[i], z[i+1] == z[i]),
            And(PC2[i] == 2, Or(y[i] != 0, y[i] == 2), PC2[i+1] == 2, PC1[i+1] == PC1[i], x[i+1] == x[i], y[i+1] == y[i], z[i+1] == z[i]),
            And(PC2[i] == 2, y[i] == 0, PC2[i+1] == 3, PC1[i+1] == PC1[i], x[i+1] == x[i], y[i+1] == y[i], z[i+1] == z[i]),
            And(PC2[i] == 3, z[i+1] == 2, PC2[i+1] == 4, PC1[i+1] == PC1[i], x[i+1] == x[i], y[i+1] == y[i]),
            And(PC2[i] == 4, x[i] != 2, PC2[i+1] == 4, PC1[i+1] == PC1[i], x[i+1] == x[i], y[i+1] == y[i], z[i+1] == z[i]),
            And(PC2[i] == 4, x[i] == 2, PC2[i+1] == 5, PC1[i+1] == PC1[i], x[i+1] == x[i], y[i+1] == y[i], z[i+1] == z[i]),
            And(PC2[i] == 5, y[i+1] == 2, PC2[i+1] == 6, PC1[i+1] == PC1[i], x[i+1] == x[i], z[i+1] == z[i]),
            And(PC2[i] == 6, z[i] != 2, PC2[i+1] == 6, PC1[i+1] == PC1[i], x[i+1] == x[i], y[i+1] == y[i], z[i+1] == z[i]),
            And(PC2[i] == 6, z[i] == 2, PC2[i+1] == 7, PC1[i+1] == PC1[i], x[i+1] == x[i], y[i+1] == y[i], z[i+1] == z[i]),
            And(PC2[i] == 7, PC2[i+1] == 1, PC1[i+1] == PC1[i], x[i+1] == x[i], y[i+1] == y[i], z[i+1] == z[i]),
            PC2[i+1] == PC2[i]
        ))
    # Check for violation of the specification
    s.add(Or([And(PC1[i] == 7, PC2[i] == 7) for i in range(k+1)]))

    if s.check() == sat:
        m = s.model()
        print("Bug found! Trace:")
        for i in range(k+1):
            print(f"time = {i}: PC1 = {m[PC1[i]]}, PC2 = {m[PC2[i]]}, x = {m[x[i]]}, y = {m[y[i]]}, z = {m[z[i]]}")
        return True
    else:
        print(f"No bug found within bound {k}")
        return False
# Run BMC with increasing bounds until a bug is found
k = 1
while not bmc(k):
    k += 1