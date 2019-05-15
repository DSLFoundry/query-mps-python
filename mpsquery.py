import lxml
from lxml import etree

def one_xpath(node, xpath, default_value=None):
    retval = default_value
    query_result = node.xpath(xpath)
    if default_value is not None:
        assert len(query_result) <= 1, 'Expected at most one element for xpath "{}", found {}: {}'.format(xpath, len(
            query_result), query_result)
    else:
        assert len(query_result) == 1, 'Expected exactly one element for xpath "{}", found {}, {}'.format(xpath,
                                                                                                      query_result,
                                                                                                      etree.tostring(node))

    if len(query_result) == 1:
        retval = query_result[0]
    return retval

class Model:
    def __init__(self, file_name):
        self.doc = etree.parse(file_name)
        self.root = self.doc.getroot()
        self.concepts = {} # index -> concept
        self.concept_names = {} # name -> concept

        # Read concepts
        for concept in self.root.xpath('/model/registry//concept'):
            concept_index = concept.get('index')
            concept_name = concept.get('name')

            # index -> name resolve
            if concept_index in self.concepts:
                raise Exception(f'Duplicate index for concept: {concept_index}')
            self.concepts[concept_index] = concept

            # Build name -> index resolve
            if concept_name in self.concept_names:
                raise Exception(f'Duplicate name for concept: {concept_name}')
            self.concept_names[concept_name] = concept

    # Helpers
    def index_of_concept(self, name):
        concept = self.concept_names.get(name)
        if concept is None:
            raise Exception(f'Concept with name {name} not found')
        return concept.get('index')

    def name_of_concept(self, index):
        concept = self.concepts.get(index)
        if concept is None:
            raise Exception(f'Concept with index {index} not found')
        return concept.get('name')

    # Model level
    def nodes_of_exactly_concept(self, concept_name):
        """Returns nodes of exactly the given concept (no inheritance)"""
        index = self.index_of_concept(concept_name)
        return self.root.xpath(f"/model/node[@concept='{index}']")

    # Node level
    def get_property(self, node, propname):
        concept_index = node.get('concept')
        concept = self.concepts.get(concept_index)
        prop_definition = one_xpath(concept, f"./property[@name='{propname}']")
        prop_index = prop_definition.get('index')
        prop_instance = one_xpath(node, f"./property[@role='{prop_index}']")
        return prop_instance.get('value')
