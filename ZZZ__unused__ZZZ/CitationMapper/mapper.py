

class citationMapper(object):

    @property
    def Nodes(self):
        return self.__nodes

    def NodesAtDepth(self, depth):
        list = []
        for node in self.__nodes:
            if node.Depth == depth:
                list.append(node)
        depthlist = [x for x in self.__nodes if x.Depth == depth]
        depthnodes = set(depthlist)
        return depthnodes


    def __init__(self, casenumber):
        from app.DBProxy import DecisionModelProxy
        decision = DecisionModelProxy.GetRepresentativeForCaseNumber(casenumber)

        citing_casenumbers = [x.CaseNumber for x in DecisionModelProxy.GetCitingCasesFromCaseNumber(casenumber)]
        cited_casenumbers = [x.strip() for x in decision.CitedCases.split(',')]
        all_casenumbers = citing_casenumbers + cited_casenumbers + [casenumber]

        from CitationMapper.dgraph import dgraphnode
        nodes = {x: dgraphnode(x) for x in all_casenumbers}
        decisions = {x: DecisionModelProxy.GetRepresentativeForCaseNumber(x) for x in all_casenumbers}
       
        for cn, node in nodes.items():
            thisdecision = decisions[cn]
            if not thisdecision:
                # cn is not in the DB, so cn is in the list because it is
                # cited by casenumber
                # which will be dealt with when cn = casenumber
                continue

            caseNumbersCitedByThisDecision = [x.strip() for x in thisdecision.CitedCases.split(',') if x.strip() in all_casenumbers]
            
            for othercasenumber in caseNumbersCitedByThisDecision:
                othernode = nodes[othercasenumber]
                node.AddOutgoingLink(othernode)
                
        self.__nodes = set(node for x, node in nodes.items())