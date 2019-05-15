import mpsquery


def main():
    file_name = 'QueryMPSPythonExample/solutions/TestSolution/models/Examples.mps'
    model = mpsquery.Model(file_name)
    for item in model.nodes_of_exactly_concept('TestLanguage.structure.SomeConcept'):
        print(model.get_property(item, 'name'))

main()