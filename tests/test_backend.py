from cmuqiskit import *

print(Backend())
print(Backend(executor_seed=-42, transpiler_seed=42))
