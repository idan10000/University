import time


def first(num):
    # num = int(eval(input("Please enter a positive integer: ")))
    t0 = time.perf_counter()
    m = num
    cnt = 0
    while m > 0:
        if m % 10 == 0:
            cnt = cnt + 1
        m = m // 10
        print(num, "has", cnt, "zeros")
    t1 = time.perf_counter()
    print("Running time: ", t1 - t0, "sec")


def second(num):
    # num = int(eval(input("Please enter a positive integer: ")))
    t0 = time.perf_counter()
    cnt = 0
    snum = str(num)  # num as a string
    for digit in snum:
        if digit == "0":
            cnt = cnt + 1
    print(num, "has", cnt, "zeros")
    t1 = time.perf_counter()
    print("Running time: ", t1 - t0, "sec")

def third(num):
    # num = int(eval(input("Please enter a positive integer: ")))
    t0 = time.perf_counter()
    cnt = str.count(str(num), "0")
    print(num, "has", cnt, "zeros")
    t1 = time.perf_counter()
    print("Running time: ", t1 - t0, "sec")



l = {2**200, 2**400, 2**800, 2**1600}
print("")
for num in l:
     first(num)
print("")
for num in l:
     second(num)
print("")
for num in l:
     third(num)
