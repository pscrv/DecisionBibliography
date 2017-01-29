
class dgraphnode(object):

    @property
    def Node(self):
        return self.__node

    @property
    def OutgoingLinks(self):
        return self.__links

    @property
    def AllLinks(self):
        links = self.__links.copy()
        for link in self.__links:
            childLinks = link.AllLinks
            links.extend(childLinks)
        return links

    @property
    def Depth(self):
        return self.__depth


    def __init__(self, nodeobj):
        self.__node = nodeobj
        self.__outgoingLinks = []
        self.__incomingLinks = []
        self.__depth = 0


    def AddOutgoingLink(self, node):
        if not isinstance(node, dgraphnode):
            node = dgraphnode(node)
        self.__outgoingLinks.append(node)
        node.__addIncomingLink(self)
        if node.Depth >= self.__depth:
            self.__depth = 1 + node.Depth
            for incoming in self.__incomingLinks:
                incoming.__updateDepth()

    def __addIncomingLink(self, node):
        self.__incomingLinks.append(node)


    def __updateDepth(self):
        self.__depth = 1 + max(x.Depth for x in self.__outgoingLinks)
        for incoming in self.__incomingLinks:
            incoming.__updateDepth()


    def __repr__(self):
        return self.__node.__repr__()