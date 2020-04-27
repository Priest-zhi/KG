import csv
from py2neo import Graph, Node, Relationship

def CreateGeneDiseaseRelationship(file="E:\DOWNLOAD\CTD_genes_diseases.csv"):
    relcount = 0
    head=["GeneSymbol","GeneID","DiseaseName","DiseaseID","DirectEvidence","InferenceChemicalName","InferenceScore","OmimIDs","PubMedIDs"]
    harray = ["DirectEvidence", "OmimIDs", "PubMedIDs"]
    graph = Graph("http://localhost:7474")
    lastgeneSymbol=""
    lastGeneNode=""
    precoount=0
    with open(file, mode='r',encoding='utf-8') as fr:
        reader = csv.reader(fr)
        for line in reader:
            precoount+=1
            if not line:
                break
            if not line[0].startswith("#") and line[6]!="" and float(line[6])>200 and precoount>3285000:
                line_dict = dict(zip(head, line))
                #find gene
                if lastgeneSymbol != line_dict["GeneSymbol"]:
                    GeneExitNode = graph.nodes.match("GENE", attribute_gene_name=line_dict["GeneSymbol"]).first()
                    if not GeneExitNode:
                        continue
                    else:
                        lastGeneNode=GeneExitNode
                else:
                    GeneExitNode=lastGeneNode

                #find disease
                DiseaseExitNode = graph.nodes.match("Disease", id=line_dict["DiseaseID"]).first()
                if not DiseaseExitNode:
                    continue

                if GeneExitNode and DiseaseExitNode:
                    GeneDRelation = Relationship(GeneExitNode, 'GeInteractionD', DiseaseExitNode, **line_dict)
                    graph.create(GeneDRelation)

                relcount += 1
                if relcount % 500 == 0:
                    print(relcount)


def CreateGenePathwayRelationship(file="data/CTD_genes_pathways.csv"):
    relcount = 0
    head=["GeneSymbol","GeneID","PathwayName","PathwayID"]
    graph = Graph("http://localhost:7474")
    lastgeneSymbol=""
    lastGeneNode=""
    with open(file, mode='r',encoding='utf-8') as fr:
        reader = csv.reader(fr)
        for line in reader:
            if not line:
                break
            if not line[0].startswith("#"):
                line_dict = dict(zip(head, line))
                #find gene
                if lastgeneSymbol != line_dict["GeneSymbol"]:
                    GeneExitNode = graph.nodes.match("GENE", attribute_gene_name=line_dict["GeneSymbol"]).first()
                    if not GeneExitNode:
                        continue
                    else:
                        lastGeneNode=GeneExitNode
                else:
                    GeneExitNode=lastGeneNode

                #find pathway
                PathExitNode = graph.nodes.match("Pathway", id=line_dict["PathwayID"]).first()
                if not PathExitNode:
                    continue

                #create relationship
                if GeneExitNode and PathExitNode:
                    GeneDRelation = Relationship(GeneExitNode, 'GeInteractionP', PathExitNode, **line_dict)
                    graph.create(GeneDRelation)

                relcount += 1
                if relcount % 500 == 0:
                    print(relcount)


if __name__ == '__main__':
    #CreateGeneDiseaseRelationship()
    CreateGenePathwayRelationship()
    print("All done!")