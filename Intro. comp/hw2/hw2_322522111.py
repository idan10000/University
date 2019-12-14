import time


############
# QUESTION 1
############

# 1d
def reverse_dict_in_place(d):
    items = list(d.keys())
    for item in items:
        d[d[item]] = item
        d.pop(item)
    return d


############
# QUESTION 2
############

# 2b
def power_new(a, b):
    """ computes a**b using iterated squaring """
    result = 1
    b_bin = bin(b)[2:]
    reverse_b_bin = b_bin[::-1]
    for bit in reverse_b_bin:
        if bit == "1":
            result *= a
        a *= a
    return result


# 2c
def modpower_new(a, b, c):
    """ computes a**b mod c using iterated squaring
        assumes b is nonnegative integer  """

    result = 1  # a**0
    while b > 0:
        if b % 4 == 0:
            result = (result) % c
            a = (a ** 4) % c
        if b % 4 == 1:
            result = (a * result) % c
            a = (a ** 4) % c
        if b % 4 == 2:
            result = (a ** 2 * result) % c
            a = (a ** 4) % c
        if b % 4 == 3:
            result = (a ** 3 * result) % c
            a = (a ** 4) % c
        b = b // 4
    return result


############
# QUESTION 3
############

# 3b
def inc(binary):
    carry = 0
    newNum = list()  # I use a list for memory efficiency, as to not create new strings in a loop.
    if len(binary) == 1:
        return "1" if binary == "0" else "10"
    if binary[-1] == "0":
        return binary[:-1] + "1"
    else:
        newNum.append("0")
        carry = 1
    for pos in range(2, len(binary) + 1, 1):
        if carry == 0:
            newNum.append(binary[: len(binary) - pos + 1])
            break
        if binary[-pos] == "0":
            newNum.append("1")
            carry = 0
        else:
            newNum.append("0")
    if carry == 1:
        newNum.append("1")
    return ("".join(newNum))[::-1]


# 3c
def dec(binary):
    newNum = list()  # I use a list for memory efficiency, as to not create new strings in a loop.
    if len(binary) == 1:
        return binary[:-1] + "0"
    elif binary[-1] == "1":
        return binary[:-1] + "0"
    else:
        newNum.append("1")
    for pos in range(2, len(binary) + 1, 1):
        if binary[-pos] == "1":
            newNum.append("0")
            newNum.append(binary[: len(binary) - pos][::-1])
            break
        newNum.append("1")
    newNumString = "".join(newNum)[::-1]
    return newNumString[1:] if newNumString[0] == "0" else newNumString


# 3d
def sub(bin1, bin2):
    newNum = list()
    if len(bin2) == 1:
        if bin2 == "1":
            return dec(bin1)
        else:
            return bin1
    curString = bin1
    for bit2 in range(1, len(bin2) + 1):
        if bin2[-bit2] == "1":
            curString = dec(curString)
            newNum.append(curString[-1])
            curString = curString[:-1]
        else:
            newNum.append(curString[-1])
            curString = curString[:-1]
    return str(int("".join(newNum[::-1])))


############
# QUESTION 4
############

# 4a
def has_repeat1(s, k):  # need to edit
    dict = {}
    for i in range(len(s) - k + 1):
        str = s[i:i + k]
        if str in dict:
            return True
        else:
            dict[str] = 1
    return False


# 4b
def has_repeat2(s, k):
    for i in range(len(s) - k):
        for j in range(i + 1, len(s) - k + 1):
            if s[i:i+k] == s[j:j+k]:
                return True
    return False


############
# QUESTION 5
############

# 5a
def sum_divisors(n):
    sum = 1
    for i in range(2, int(n ** (1 / 2)) + 1):
        if n % i == 0:
            sum += i
        if n % (n // i) == 0:
            if i != n // i:
                sum += n // i
    return sum


############
# QUESTION 6
############

# 6a
def parse_primes(filename):
    primesFile = open(filename, "r")
    primes = set(map(int, primesFile.read().split()))
    primesFile.close()
    return primes


# 6b
def check_goldbach_for_num(n, primes_set):
    for num in primes_set:
        if num < n:
            if n - num in primes_set:
                return True
    return False


# 6c
def check_goldbach_for_range(limit, primes_set):
    for num in range(4, int(limit), 2):
        if not check_goldbach_for_num(num, primes_set):
            return False
    return True


# 6d1
def check_goldbach_for_num_stats(n, primes_set):
    counter = 0
    for num in primes_set:
        if (int(n) - num) in primes_set:
            if (int(n) - num) == num:
                counter += 2
            else:
                counter += 1
    return counter // 2  # it find every pair twice, so we return half of it (5 + 3 or 3 + 5 which are the same pair)


# 6d2
def check_goldbach_stats(limit, primes_set):
    dict = {}
    for num in range(4, int(limit) + 1, 2):
        curPlace = check_goldbach_for_num_stats(num, primes_set)
        if curPlace not in dict:
            dict[curPlace] = 0
        dict[curPlace] += 1
    return dict


########
# Tester
########

def test():
    d = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    d_ans = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}

    d_id = id(d)
    reverse_dict_in_place(d)
    if d != d_ans or id(d) != d_id:
        print("error in reverse_dict_in_place()")

    if power_new(2, 3) != 8:
        print("error in power_new()")

    if modpower_new(3, 4, 5) != pow(3, 4, 5) or \
            modpower_new(5, 4, 2) != pow(5, 4, 2):
        print("error in modpower_new()")

    if inc("0") != "1" or \
            inc("1") != "10" or \
            inc("101") != "110" or \
            inc("111") != "1000" or \
            inc(inc("111")) != "1001":
        print("error in inc()")

    if dec("1") != "0" or \
            dec("10") != "1" or \
            dec("110") != "101" or \
            dec("1000") != "111" or \
            dec(dec("1001")) != "111":
        print("error in dec()")

    if sub("0", "0") != "0" or \
            sub("1000", "0") != "1000" or \
            sub("1000", "1000") != "0" or \
            sub("1000", "1") != "111" or \
            sub("101", "100") != "1":
        print("error in sub()")

    if not has_repeat1("ababa", 3) or \
            has_repeat1("ababa", 4) or \
            not has_repeat1("aba", 1):
        print("error in has_repeat1()")

    if not has_repeat2("ababa", 3) or \
            has_repeat2("ababa", 4) or \
            not has_repeat2("aba", 1):
        print("error in has_repeat2()")

    if sum_divisors(6) != 6 or \
            sum_divisors(4) != 3:
        print("error in sum_divisors()")

    primes_set = parse_primes("primes.txt")
    if primes_set == None or 104729 not in primes_set or 6 in primes_set:
        print("error in parse_primes()")

    if not check_goldbach_for_num(10, {2, 3, 5, 7}):
        print("error in check_goldbach_for_num()")

    if check_goldbach_for_num(10, {2, 3}):
        print("error in check_goldbach_for_num()")

    if not check_goldbach_for_range(20, {2, 3, 5, 7, 11}):
        print("error in check_goldbach_for_range()")

    if check_goldbach_for_range(21, {2, 3, 5, 7, 11}):
        print("error in check_goldbach_for_range()")

    if check_goldbach_for_num_stats(20, primes_set) != 2:
        print("error in check_goldbach_for_num_stats()")

    if check_goldbach_for_num_stats(10, primes_set) != 2:
        print("error in check_goldbach_for_num_stats()")

    if check_goldbach_stats(11, primes_set) != {1: 3, 2: 1}:
        print("error in check_goldbach_stats()")

print(inc("10001111 "))
