import csv
from py2neo import Graph, Node, Relationship



def CreateDiseasePathwayRelationship(file="data/CTD_diseases_pathways.csv"):
    relcount = 0
    head=["DiseaseName","DiseaseID","PathwayName","PathwayID","InferenceGeneSymbol"]
    graph = Graph("http://localhost:7474")
    lastDiseaseID=""
    lastDiseaseNode=""
    with open(file, mode='r',encoding='utf-8') as fr:
        reader = csv.reader(fr)
        for line in reader:
            if not line:
                break
            if not line[0].startswith("#"):
                line_dict = dict(zip(head, line))
                #find gene
                if lastDiseaseID != line_dict["DiseaseID"]:
                    DiseaseExitNode = graph.nodes.match("Disease", id=line_dict["DiseaseID"]).first()
                    if not DiseaseExitNode:
                        continue
                    else:
                        lastDiseaseNode=DiseaseExitNode
                else:
                    DiseaseExitNode=lastDiseaseNode

                #find pathway
                PathExitNode = graph.nodes.match("Pathway", id=line_dict["PathwayID"]).first()
                if not PathExitNode:
                    continue

                #create relationship
                if DiseaseExitNode and PathExitNode:
                    DiseasePathRelation = Relationship(DiseaseExitNode, 'DInteractionP', PathExitNode, **line_dict)
                    graph.create(DiseasePathRelation)

                relcount += 1
                if relcount % 500 == 0:
                    print(relcount)


if __name__ == '__main__':
    CreateDiseasePathwayRelationship()
    print("All done!")