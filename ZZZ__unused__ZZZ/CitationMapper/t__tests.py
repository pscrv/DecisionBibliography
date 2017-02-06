import django
from django.test import TestCase


class dgraphtests(TestCase):

    def test_CanMakeNode(self):
        from CitationMapper import dgraph
        string = 'Test string'
        node = dgraph.dgraphnode(string)
        self.assertEqual(node.Node, string)

    def test_CanAddLink(self):
        from CitationMapper import dgraph
        string = 'Base node'
        basenode = dgraph.dgraphnode(string)
        othernode = dgraph.dgraphnode("other node")
        basenode.AddLink(othernode)
        self.assertEqual(len(basenode.OutgoingLinks), 1)
        self.assertEqual(basenode.OutgoingLinks[0], othernode)

    def test_CanAddNon_nodeLink(self):
        from CitationMapper import dgraph
        string = 'Base node'
        basenode = dgraph.dgraphnode(string)
        othernode = 7
        basenode.AddLink(othernode)
        self.assertEqual(len(basenode.OutgoingLinks), 1)
        self.assertEqual(basenode.OutgoingLinks[0].Node, othernode)

    def test_CanAddTwoLinks(self):
        from CitationMapper import dgraph
        string = 'Base node'
        basenode = dgraph.dgraphnode(string)
        othernode1 = dgraph.dgraphnode("other node")
        othernode2 = 7
        basenode.AddLink(othernode1)
        basenode.AddLink(othernode2)
        self.assertEqual(len(basenode.OutgoingLinks), 2)

    def test_AllLinks_depth1(self):
        from CitationMapper import dgraph
        string = 'Base node'
        basenode = dgraph.dgraphnode(string)
        link1 = dgraph.dgraphnode('1_1')
        link2 = dgraph.dgraphnode('1_2')
        basenode.AddLink(link1)
        basenode.AddLink(link2)
        alllinks = basenode.AllLinks
        self._baseAssertEqual(len(alllinks), 2)
        
    def test_AllLinks_depth2(self):
        from CitationMapper import dgraph
        string = 'Base node'
        basenode = dgraph.dgraphnode(string)
        link1 = dgraph.dgraphnode('1_1')
        link2 = dgraph.dgraphnode('1_2')
        link3 = dgraph.dgraphnode('2_1')
        basenode.AddLink(link1)
        basenode.AddLink(link2)
        link1.AddLink(link3)
        alllinks = basenode.AllLinks
        self._baseAssertEqual(len(alllinks), 3)
        
    def test_AllLinks_depth3(self):
        from CitationMapper import dgraph
        string = 'Base node'
        basenode = dgraph.dgraphnode(string)
        link1 = dgraph.dgraphnode('1_1')
        link2 = dgraph.dgraphnode('2_1')
        link3 = dgraph.dgraphnode('3_1')
        basenode.AddLink(link1)
        link1.AddLink(link2)
        link2.AddLink(link3)
        alllinks = basenode.AllLinks
        self._baseAssertEqual(len(alllinks), 3)





class CitationMapperTests(TestCase):

    if django.VERSION[:2] >= (1, 7):
        # Django 1.7 requires an explicit setup() when running tests in PTVS
        @classmethod
        def setUpClass(cls):
            super(CitationMapperTests, cls).setUpClass()
            django.setup()

    def test_mapper(self):
        from app.DBProxy import DecisionModelProxy
        from CitationMapper import mapper

        decision = DecisionModelProxy.GetRepresentativeForCaseNumber('G 0002/88')
        mpr = mapper.citationMapper(decision.CaseNumber)
        d1 = mpr.NodesAtDepth(0)
        #d2 = mpr.NodesAtDepth(1)
        #d3 = mpr.NodesAtDepth(333)
        x = 1
