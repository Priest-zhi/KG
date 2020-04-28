import csv
from py2neo import Graph, Node, Relationship



def CreateGODiseaseRelationship(file):
    relcount = 0
    head=["GOName","GOID","DiseaseName","DiseaseID","InferenceChemicalQty","InferenceChemicalNames","InferenceGeneQty","InferenceGeneSymbols"]
    graph = Graph("http://localhost:7474")
    lastGOID=""
    lastGONode=""
    with open(file, mode='r',encoding='utf-8') as fr:
        reader = csv.reader(fr)
        for line in reader:
            if not line:
                break
            if not line[0].startswith("#"):
                line_dict = dict(zip(head, line))
                #find GO
                if lastGOID != line_dict["GOID"]:
                    GOExitNode = graph.nodes.match("GO", id=line_dict["GOID"]).first()
                    if not GOExitNode:
                        continue
                    else:
                        lastGONode=GOExitNode
                else:
                    GOExitNode=lastGONode

                #find disease
                DiseaseExitNode = graph.nodes.match("Disease", id=line_dict["DiseaseID"]).first()
                if not DiseaseExitNode:
                    continue

                #create relationship
                if GOExitNode and DiseaseExitNode:
                    DiseasePathRelation = Relationship(GOExitNode, 'GOInteractionD', DiseaseExitNode, **line_dict)
                    graph.create(DiseasePathRelation)

                relcount += 1
                if relcount % 500 == 0:
                    print(relcount)


if __name__ == '__main__':
    files=["data/CTD_Phenotype-Disease_cellular_component_associations.csv","data/CTD_Phenotype-Disease_molecular_function_associations.csv","data/CTD_Phenotype-Disease_biological_process_associations.csv"]
    for fileEle in files:
        print("file begin: ", fileEle)
        CreateGODiseaseRelationship(fileEle)
        print("file complete: ", fileEle)
    print("All done!")