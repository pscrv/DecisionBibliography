class graphnode(object):

    def __init__(self, obj):
        self.__node = obj

    @property
    def Node(self):
        return self.__node


class graphedge(object):

    def __init__(self, node1: graphnode, node2: graphnode):
        self.__nodes = set()
        self.__nodes.add(node1)
        self.__nodes.add(node2)

    def Nodes(self):
        return self.__nodes



class graph(object):
    
    def __init__(self):
        self.__nodes = set()
        self.__edges = set()

    def AddNode(self, node: graphnode):
        self.__nodes.add(node)

    def DeleteNode(self, node: graphnode):
        self.__nodes.discard(node)

    def AddEdge(self, edge: graphedge):
            self.__edges.add(graphedge)

    def LinkNodes(self, node1: graphnode, node2: graphnode):
        if node1 in self.__nodes and node2 in self.__nodes:
            self.__edges.add(graphedge(node1, node2))
        else:
            raise ValueError('At least one of node1 and node2 is not in this graph.')

    def RemoveEdge(self, edge: graphedge):
        self.__edges.discard(edge)

    def SplitNodes(self, node1: graphnode, node2: graphnode):
        if node1 in self.__nodes and node2 in self.__nodes:
            edges_to_remove = [x for x in self.__edges if node1 in x.Nodes and node2 in x.Nodes]
            for edge in edges_to_remove:
                self.__edges.discard(edge)
        else:
            raise ValueError('At least one of node1 and node2 is not in this graph.')


