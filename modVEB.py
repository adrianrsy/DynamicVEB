from VEB import VEB 
import numpy as np

#stores the entire value of an inserted value into relevant positions in the vEB
#also stores its locations across vEBs and its predecessor and successors within the vEB 
class Node:
    def __init__(self,v):
        self.value = v
        #stores references to the low-level vEBs containing this node (so as to be able to point to other copies)
        self.references = {}
        #pointers to its predecessor and successor within the vEB for verifying purposes
        self.predecessor = None
        self.successor = None

class ModVEB(VEB):
    #initialized based on parent to generate ancestor list
    def __init__(self, u, k=0, parent = None):
        self.offset = k
        if u < 0:
            raise Exception("u cannot be less than 0 --- u = " + str(u))
        self.u = 2
        while self.u < u:
            self.u *= self.u
        self.min = (None,None) #(Node, x)
        self.max = (None,None) #(Node, x)
        if (u > 2):
            self.clusters = [None for i in range(self.high(self.u))] #modVEB trees
            self.summary = None #standard VEB tree
        self.parent = parent 

        #ancestor of 2^2^i bit universe is 2^2^{i+1} bit universe (jumping 2^i levels)
        self.ancestor = parent
        bitsize = np.log2(u)
        for i in range(int(np.log2(bitsize)/2)):
            if self.ancestor == None:
                break
            self.ancestor = self.ancestor.parent

    #returns a value node/false
    def member(self,node,x):
        x = x%self.u
        if x == self.min[1] and node.value == self.min[0].value:
            return self.min[0]
        elif x == self.max[1] and node.value == self.max[0].value:
            return self.max[0]
        elif self.u <=2:
            return False
        else:
            cluster = self.clusters[self.high(x)]
            if cluster != None:
                return cluster.member(node,self.low(x))
            else:
                return False

    #assumes x is of the same bitorder as u, finds successor in overall vEB
    #e.g. when in vEB corresponding to high order bits 1101 and 11010100 is in the vEB
    #   returns the node containing the value 11010100 for successor(0100)
    def successor(self,node, x):
        x = x%self.u
        if self.min[0] == None:
            return None
        if self.u <= 2:
            if x==0 and self.max[1] ==1 and self.max[0].value > node.value:
                return self.max[0]
            else:
                return None
        elif self.min[1] != None and x < self.min[1] and self.max[0].value > node.value:
            return self.min[0]
        else:
            h = self.high(x)
            l = self.low(x)
            maxlow = None
            cluster = self.clusters[h]
            if cluster != None:
                maxlow = cluster.max[1]
            if maxlow != None and l < maxlow:
                return cluster.successor(node,l)
            else:
                succcluster = None
                if self.summary != None:
                    succcluster = self.summary.successor(h)
                if succcluster == None:
                    return None
                else:
                    cluster2 = self.clusters[succcluster]
                    return cluster2.min[0]

    def predecessor(self, node, x):
        if self.min[0] == None:
            return None
        x = x%self.u
        if self.u <= 2:
            if x==1 and self.min[1] ==0 and self.min[0].value < node.value:
                return self.min[0]
            else:
                return None
        elif self.max[1] != None and x > self.max[1] and self.max[0].value < node.value:
            return self.max[0]
        else:
            h = self.high(x)
            l = self.low(x)
            minlow = None
            cluster = self.clusters[h]
            if cluster != None:
                minlow = cluster.min[1]
            if minlow != None and l > minlow:
                return cluster.predecessor(node,l)
            else:
                predcluster = None
                if self.summary != None:
                    predcluster = self.summary.predecessor(h)
                if predcluster == None:
                    return None
                else:
                    cluster2 = self.clusters[predcluster]
                    return cluster2.max[0]

    def emptyInsert(self,node,x):
        x = x%self.u
        self.min = (node,x)
        self.max = (node,x)

    def insert(self,node,x):
        x = x%self.u
        if (self.u <= 2):
            node.references[self.offset] = self
        if self.min[1] == None or self.min[0] == None:
            self.emptyInsert(node,x)
            self.insert(node,x)
        else:
            if x < self.min[1]:
                self.min = (self.min[0],x)
            if node.value < self.min[0].value:
                self.min = (node,self.min[1])
            if x > self.max[1]:
                self.max = (self.max[0],x)
            if node.value > self.max[0].value:
                self.max = (node,self.max[1])
            if self.u > 2:
                h = self.high(x)
                if self.clusters[h] == None:
                    self.clusters[h] = ModVEB(self.high(self.u), k = self.offset, parent = self)
                if self.summary == None:
                    self.summary = VEB(self.high(self.u))
                if self.clusters[h].min[1] == None:
                    self.summary.insert(h)
                    self.clusters[h].emptyInsert(node,self.low(x))
                self.clusters[h].insert(node,self.low(x))
        return self.member(node,x)

          
            
        
            
