# global x,y,z


# def proc(pid):
# 	while True:
# 1		x = pid
# 2		if (y != 0 and y != pid): continue
# 3		z = pid
# 4		if (x != pid): continue
# 5		y = pid
# 6		if (z != pid): continue
# 7		#critical section

		
# def main():
# 	proc(1) || proc(2)
	

from z3 import *

def bounded_model_checking(bound):
    # create K pc1 and pc2
    PC1 = [Int(f'PC1_{i}') for i in range(bound + 1)]
    PC2 = [Int(f'PC2_{i}') for i in range(bound + 1)]
    
    # create K x y z 
    x = [Int(f'x_{i}') for i in range(bound + 1)]
    y = [Int(f'y_{i}') for i in range(bound + 1)]
    z = [Int(f'z_{i}') for i in range(bound + 1)]

    # initialization
    init = [
        PC1[0] == 1, PC2[0] == 1,  
        x[0] == 0, y[0] == 0, z[0] == 0  
    ]

    # Transitions
    def transitions(PC, pid):
        trans = []
        for i in range(bound):
            trans.append(Implies(PC[i] == 1, And(PC[i+1] == 2, x[i+1] == pid, x[i] == x[i+1], y[i+1] == y[i], z[i+1] == z[i])))
            trans.append(Implies(PC[i] == 2, If(And(y[i] != 0, y[i] != pid), PC[i+1] == 3, PC[i+1] == 2)))
            trans.append(Implies(PC[i] == 3, And(PC[i+1] == 4, z[i+1] == pid, x[i+1] == x[i], y[i+1] == y[i])))
            trans.append(Implies(PC[i] == 4, If(x[i] != pid, PC[i+1] == 5, PC[i+1] == 4)))
            trans.append(Implies(PC[i] == 5, And(PC[i+1] == 6, y[i+1] == pid, x[i+1] == x[i], z[i+1] == z[i])))
            trans.append(Implies(PC[i] == 6, If(z[i] != pid, PC[i+1] == 7, PC[i+1] == 6)))
            trans.append(Implies(PC[i] == 7, PC[i+1] == 1))  # Exit critical section
        return trans

    # Collect all constraints
    constraints = (
        init +
        transitions(PC1, 1) +
        transitions(PC2, 2)
    )

    # never both processes in critical section
    # safety_property = And([Not(And(PC1[i] == 7, PC2[i] == 7)) for i in range(bound + 1)])
    safety_property = Not(And(PC1[bound] == 7, PC2[bound] == 7))

    # Solver setup
    s = Solver()
    s.add(constraints)
    s.add(Not(safety_property))  # Looking for a violation

    if s.check() == sat:
        print(f"Bound {bound}: Property violated! Counterexample found.")
        m = s.model()
        for i in range(bound + 1):
            print(f'time = {i}: PC1 = {m.evaluate(PC1[i])}, PC2 = {m.evaluate(PC2[i])}, x = {m.evaluate(x[i])}, y = {m.evaluate(y[i])}, z = {m.evaluate(z[i])}')


# Run bounded model
for k in range(0,20):
  bounded_model_checking(k)
# print("done")
	



# x = Bool("x")
# x = Const("x" , BoolSort())
# p, q, r = Bools("p q r") # convenience function for multiple definitions
# x = Real("x")
# y = Int("x") 
# v = BitVec("n", 32) # 32 bit bitvector
# f = FP("f", Float64()) #Floating point values
# a = Array("a", IntSort(), BoolSort()) # arrays

# print(And(p,q))
# print(And(p,q,r)) # some can accept more than one argument for convenience.
# print(Or(p,q))
# print(Implies(p,q))
# print(Xor(p,q))
# print(Not(p))

# def foo(x):
#     for i in range(3):
#         x = x*x
#     return x

# def foo(x):
#     x = x*x
#     x = x*x
#     x = x*x
#     return x

# x,x1,x2,x3 = Ints("x x1 x2 x3")
# prog = [
#     x1 == x*x,
#     x2 == x1*x1,
#     x3 == 