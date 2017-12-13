from dynamicVEB import *
import time
import random

print("Testing")
VEB = VEB(1000000000)
dVEB = DynamicVEB(1000000000)

print("Constructing keyset")
key_set = []
for i in range(100000):
    #key_set.append(i)
    if random.random() < 0.8:
        key_set.append(i)
#random.shuffle(key_set)
sorted_copy = sorted(key_set)

print("Testing insert for VEB")
start_time = time.time()
for item in key_set:
    VEB.insert(item)
end_time = time.time()
print("result:", end_time - start_time)
print()

print("Testing insert for dVEB")
start_time = time.time()
for item in key_set:
    dVEB.insert(item)
end_time = time.time()
print("result:", end_time - start_time)
print()


print("Testing member for VEB")
start_time = time.time()
for item in key_set:
    assert(VEB.member(item))
end_time = time.time()
print("result:", end_time - start_time)
print()

print("Testing member for dVEB")
start_time = time.time()
for item in key_set:
    assert(dVEB.member(item))
end_time = time.time()
print("result:", end_time - start_time)
print()

print("Testing predecessor for VEB")
start_time = time.time()
for i in range(1,len(sorted_copy)):
    assert(VEB.predecessor(sorted_copy[i]) == sorted_copy[i-1])
end_time = time.time()
print("result:", end_time - start_time)
print()

print("Testing predecessor for dVEB")
start_time = time.time()
for i in range(1,len(sorted_copy)):
    assert(dVEB.predecessor(sorted_copy[i]) == sorted_copy[i-1])
end_time = time.time()
print("result:", end_time - start_time)
print()

print("Testing successor for VEB")
start_time = time.time()
for i in range(len(sorted_copy)-1):
    assert(VEB.successor(sorted_copy[i]) == sorted_copy[i+1])
end_time = time.time()
print("result:", end_time - start_time)
print()

print("Testing successor for dVEB")
start_time = time.time()
for i in range(len(sorted_copy)-1):
    assert(dVEB.successor(sorted_copy[i]) == sorted_copy[i+1])
end_time = time.time()
print("result:", end_time - start_time)
print()
