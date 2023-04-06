import itertools
import timeit

cases = []

n = 2
id = 1
for i in range(1, n + 1):
    for j in range(1, n + 1):
        cases.append(id)
        id += 1


def test1():
    for case1 in cases:
        for case2 in cases:
            if case1 != case2:
                for case3 in cases:
                    if case3 != case1 and case3 != case2:
                        print(f"{case1} ; {case2} ; {case3}")


def test2():
    for case1, case2, case3 in itertools.combinations(cases, 3):
        print(f"{case1} ; {case2} ; {case3}")


starttime = timeit.default_timer()
print("The start time is :", starttime)
test1()
print("The time difference is :", timeit.default_timer() - starttime)

starttime = timeit.default_timer()
print("The start time is :", starttime)
test2()
print("The time difference is :", timeit.default_timer() - starttime)
