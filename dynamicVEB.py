from modVEB import ModVEB 
from modVEB import Node 
from VEB import VEB 
import time
import random

class DynamicVEB:
    def __init__(self,u):
        self.pointer = None
        self.base = ModVEB(u)
        self.node_set = {}
        #offsets are 2^2^1/2, 2^2^2/2, 2^2^4/2, ... 2^2^ lg lg U/2
        log_offset = 1
        self.offsets = [0]
        self.offset_copies = [self.base]
        while 2**2**log_offset < u:
            self.offsets.append(int(2**(2**log_offset)/2))
            self.offset_copies.append(ModVEB(u, k = self.offsets[-1]))
            log_offset *= 2

    def member(self,x):
        new_node = Node(x)
        if self.pointer == None:
            self.pointer = offset_copies[0].member(new_node,x)
            if self.pointer:
                return True
            else:
                self.pointer = None
                return False
        node = self.pointer
        base_pointer = node.references[0]
        base_answer = base_pointer.member(new_node,x)
        if base_answer:
            self.pointer = base_answer
            return True

        #use references and ancestor pointers to climb up the tree
        for i in range(1,len(self.offset_copies)):
            base_pointer = node.references[0]
            offset_pointer = node.references[self.offsets[int(i)]]
            for j in range(i):
                if base_pointer.ancestor == None or offset_pointer.ancestor == None:
                    break
                base_pointer = base_pointer.ancestor
                offset_pointer = offset_pointer.ancestor
                
            base_answer = base_pointer.member(new_node,x)
            if base_answer:
                self.pointer = base_answer
                return True
            offset_answer = offset_pointer.member(new_node,x+self.offsets[i])
            if offset_answer:
                self.pointer = offset_answer
                return True
        main_base_answer = self.base.member(new_node,x)
        if main_base_answer:
            self.pointer = main_base_answer
            return True
        else:
            return False

    def predecessor(self,x):
        new_node = Node(x)
        if self.pointer == None:
            self.pointer = offset_copies[0].predecessor(new_node,x)
            if self.pointer:
                #print("copies_checked = N/A")
                return self.pointer.value
            else:
                self.pointer = None
                return None
        node = self.pointer
        base_pointer = node.references[0]
        base_answer = base_pointer.predecessor(new_node,x)
        if base_answer and (self.node_set[base_answer.value].successor == None or self.node_set[base_answer.value].successor.value >= x) and base_answer.value < x:
            self.pointer = base_answer
            #print("copies_checked = ",0)
            return base_answer.value
        for i in range(1,len(self.offset_copies)):
            base_pointer = node.references[0]
            offset_pointer = node.references[self.offsets[int(i)]]
            for j in range(i):
                if base_pointer.ancestor == None or offset_pointer.ancestor == None:
                    break
                base_pointer = base_pointer.ancestor
                offset_pointer = offset_pointer.ancestor

            #print("offset universe:",offset_pointer.u, "offset:", self.offsets[int(i)], "i:",i)

            base_answer = base_pointer.predecessor(new_node,x)
            if base_answer and (self.node_set[base_answer.value].successor == None or self.node_set[base_answer.value].successor.value >= x) and base_answer.value < x:
                self.pointer = base_answer
                #print("copies_checked = ",i, " base version")
                return base_answer.value
            offset_answer = offset_pointer.predecessor(new_node,x+self.offsets[i])
            if offset_answer and (self.node_set[offset_answer.value].successor == None or self.node_set[offset_answer.value].successor.value >= x) and offset_answer.value < x:
                self.pointer = offset_answer
                #print("copies_checked = ",i, " offset verion")
                return offset_answer.value
        main_base_answer = self.base.predecessor(new_node,x)
        if main_base_answer:
            self.pointer = main_base_answer
            #print("copies_checked = all")
            return main_base_answer.value
        else:
            return None

    def successor(self,x):
        new_node = Node(x)
        if self.pointer == None:
            self.pointer = offset_copies[0].successor(new_node,x)
            if self.pointer:
                #print("copies_checked = N/A")
                return self.pointer.value
            else:
                self.pointer = None
                return None
        node = self.pointer
        base_pointer = node.references[0]
        base_answer = base_pointer.successor(new_node,x)
        if base_answer and (self.node_set[base_answer.value].predecessor == None or self.node_set[base_answer.value].predecessor.value <= x) and base_answer.value > x:
            self.pointer = base_answer
            #print("copies_checked = ",0)
            return base_answer.value
        for i in range(1,len(self.offset_copies)):
            base_pointer = node.references[0]
            offset_pointer = node.references[self.offsets[int(i)]]
            for j in range(i):
                if base_pointer.ancestor == None or offset_pointer.ancestor == None:
                    break
                base_pointer = base_pointer.ancestor
                offset_pointer = offset_pointer.ancestor

            #print("offset universe:",offset_pointer.u, "offset:", self.offsets[int(i)], "i:",i)

            base_answer = base_pointer.successor(new_node,x)
            if base_answer and (self.node_set[base_answer.value].predecessor == None or self.node_set[base_answer.value].predecessor.value <= x) and base_answer.value > x:
                self.pointer = base_answer
                #print("copies_checked = ",i, " base version")
                return base_answer.value
            offset_answer = offset_pointer.successor(new_node,x+self.offsets[i])
            if offset_answer and (self.node_set[offset_answer.value].predecessor == None or self.node_set[offset_answer.value].predecessor.value <= x) and offset_answer.value > x:
                self.pointer = offset_answer
                #print("copies_checked = ",i, " offset verion")
                return offset_answer.value
        main_base_answer = self.base.successor(new_node,x)
        if main_base_answer:
            self.pointer = main_base_answer
            #print("copies_checked = all")
            return main_base_answer.value
        else:
            return None

    def insert(self,x):
        node = Node(x)
        successor = self.base.successor(node,x)
        predecessor = self.base.predecessor(node,x)
        for i in range(len(self.offset_copies)):
            self.offset_copies[i].insert(node,x + self.offsets[i])
        if successor != None:
            self.node_set[successor.value].predecessor = node
            node.successor = successor
        if predecessor != None:
            self.node_set[predecessor.value].successor = node
            node.predecessor = predecessor
        
        self.node_set[x] = node
        self.pointer = node
        return node.value

# print("Testing")
# VEB = VEB(1000000000)
# dVEB = DynamicVEB(1000000000)

# print("Constructing keyset")
# key_set = []
# for i in range(100000):
#     #key_set.append(i)
#     if random.random() < 0.8:
#         key_set.append(i)
# #random.shuffle(key_set)
# sorted_copy = sorted(key_set)

# print("Testing insert for VEB")
# start_time = time.time()
# for item in key_set:
#     VEB.insert(item)
# end_time = time.time()
# print("result:", end_time - start_time)
# print()

# print("Testing insert for dVEB")
# start_time = time.time()
# for item in key_set:
#     dVEB.insert(item)
# end_time = time.time()
# print("result:", end_time - start_time)
# print()



# # print("Testing member for VEB")
# # start_time = time.time()
# # for item in key_set:
# #     assert(VEB.member(item))
# # end_time = time.time()
# # print("result:", end_time - start_time)
# # print()

# # print("Testing member for dVEB")
# # start_time = time.time()
# # for item in key_set:
# #     assert(dVEB.member(item))
# # end_time = time.time()
# # print("result:", end_time - start_time)
# # print()

# # print("Testing predecessor for VEB")
# # start_time = time.time()
# # for i in range(1,len(sorted_copy)):
# #     assert(VEB.predecessor(sorted_copy[i]) == sorted_copy[i-1])
# # end_time = time.time()
# # print("result:", end_time - start_time)
# # print()

# # print("Testing predecessor for dVEB")
# # start_time = time.time()
# # for i in range(1,len(sorted_copy)):
# #     assert(dVEB.predecessor(sorted_copy[i]) == sorted_copy[i-1])
# # end_time = time.time()
# # print("result:", end_time - start_time)
# # print()

# print("Testing successor for VEB")
# start_time = time.time()
# for i in range(len(sorted_copy)-1):
#     assert(VEB.successor(sorted_copy[i]) == sorted_copy[i+1])
# end_time = time.time()
# print("result:", end_time - start_time)
# print()

# print("Testing successor for dVEB")
# start_time = time.time()
# for i in range(len(sorted_copy)-1):
#     assert(dVEB.successor(sorted_copy[i]) == sorted_copy[i+1])
# end_time = time.time()
# print("result:", end_time - start_time)
# print()
                
# # print("before construction")
# dVEB = DynamicVEB(1000000000)
# print("before insert")
# dVEB.insert(1)
# dVEB.insert(2)
# dVEB.insert(3)
# dVEB.insert(4)
# dVEB.insert(5)
# dVEB.insert(100000)
# print("running")
# print(len(dVEB.offset_copies))

# print(100, dVEB.successor(100))
# print(1, dVEB.successor(1))
# print(2, dVEB.successor(2))
# print(3,dVEB.successor(3))
# print(10,dVEB.successor(10))
# print(5,dVEB.successor(5))

# print(100, dVEB.predecessor(100))
# print(1, dVEB.predecessor(1))
# print(2, dVEB.predecessor(2))
# print(dVEB.pointer.value)
# print(10, dVEB.predecessor(10))
# print(3, dVEB.predecessor(3))
# print(4, dVEB.predecessor(4))
# print(5, dVEB.predecessor(5))

# print(100001, dVEB.predecessor(100001))
# print(1000, dVEB.predecessor(1000))

# pointer = dVEB.pointer.references[0]
# while True:
#     if pointer != None:
#         print (pointer.u)
#         pointer = pointer.ancestor
#     else:
#         break

print("Starting")
veb= VEB(100000000000)
veb.insert(1)
print(veb.member(1))
            
