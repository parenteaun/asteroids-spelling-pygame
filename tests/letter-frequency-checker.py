# 1. Import & build frequency list
from main import build_frequency_list
lst = build_frequency_list()
print("Total letters:", len(lst))
print("Counts:", {l: lst.count(l) for l in sorted(set(lst))})
PY
