from cmuqiskit import *

print(Backend())
print(Backend(simulator_seed=-42, transpiler_seed=42))
