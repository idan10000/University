import time
import math

# print(math.log(11**2020, 2))
# print(len(bin(11**2020)))
#
# def build_dict(keys, vals):
#     d = {}
#     for key in keys:
#         for val in vals:
#             if keys.index(key) == vals.index(val):
#                 d[key] = val
#     return d
#
#
# def build_dict2(keys, vals):
#     d = {}
#     for i in range(len(keys)):
#         d[keys[i]] = vals[i]
#     return d
#
#
# keys = [i for i in range(1000)]
# vals = [i for i in range(1000)]
# start = time.perf_counter()
# build_dict(keys, vals)
# end = time.perf_counter()
# print("build_dict time: ", end - start)
# start = time.perf_counter()
# build_dict2(keys, vals)
# end = time.perf_counter()
# print("build_dict2 time: ", end - start)

n = 999
result = n
for i in range(1,10):
    t = (3*(result-1))/(result+3)
    result = t
    print (result)
