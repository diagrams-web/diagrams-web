import unittest
import helpers


class HelpersTest(unittest.TestCase):
    """"""

    def test_providers(self):
        """"""
        providers = helpers.providers()
        # Check that it return correct structure i.e list of dict
        self.assertTrue(providers[0])
        self.assertTrue(providers[0]['name'])
        self.assertTrue(providers[0]['icon'])
        # we have the nodes key but it empty as by default we don't want the nodes.
        self.assertFalse(providers[0]['nodes'])

    def test_providers_with_nodes(self):
        """"""
        providers = helpers.providers(with_nodes=True)
        # we have the nodes and there's data inside
        self.assertTrue(providers[0]['nodes'])
        nodes_content = providers[0]['nodes']
        self.assertTrue(nodes_content[0]['path'])
        self.assertTrue(nodes_content[0]['title'])
        self.assertTrue(nodes_content[0]['nodes'])

    def test_nodes(self):
        """"""
        import config

        nodes = helpers.nodes('elastic', config.RESOURCE_PATH)
        # Check that it return correct structure i.e list of dict
        self.assertTrue(nodes[0])
        self.assertTrue(nodes[0]['path'])
        self.assertTrue(nodes[0]['title'])
        self.assertTrue(nodes[0]['nodes'])
        # sub-nodes are list of dict
        sub_nodes = nodes[0]['nodes']
        # key should exist but can be empty or not
        self.assertIn('alias', sub_nodes[0])
        self.assertTrue(sub_nodes[0]['icon'])
        self.assertTrue(sub_nodes[0]['name'])

        