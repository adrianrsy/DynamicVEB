from modVEB import ModVEB 
from modVEB import Node 
from VEB import VEB 

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

            
