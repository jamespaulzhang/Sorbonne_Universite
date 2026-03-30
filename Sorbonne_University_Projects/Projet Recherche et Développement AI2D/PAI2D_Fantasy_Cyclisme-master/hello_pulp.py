import pulp as pl

pb = pl.LpProblem("z", pl.LpMaximize)

x = pl.LpVariable("x", lowBound=0)
y = pl.LpVariable("y", lowBound=0)

pb += 3*x + 2*y

pb += x + 2*y <= 14
pb += 3*x - y >= 0
pb += x - y <= 2

# status = pl.PULP_CBC_CMD(msg=0)
status = pb.solve()

print("Status:", pl.LpStatus[status])

print("x =", x.value())
print("y =", y.value())
print("opt =", pl.value(pb.objective))