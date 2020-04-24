import csv
from py2neo import Graph, Node, Relationship

def CreateChemicalGeneRelationship(file="data/CTD_chem_gene_ixns.csv"):
    relcount = 0
    head=["ChemicalName","ChemicalID","CasRN","GeneSymbol","GeneID","GeneForms","Organism","OrganismID","Interaction","InteractionActions","PubMedIDs"]
    harray = ["GeneForms", "InteractionActions", "PubMedIDs"]
    type="Chemical"
    Cgraph = Graph("http://localhost:7474")
    lastChemiName=lastGeneSymbol=""
    with open(file, mode='r',encoding='utf-8') as fr:
        reader = csv.reader(fr)
        for line in reader:
            if not line:
                break
            if not line[0].startswith("#"):
                if line[6] == "Homo sapiens" and not (line[0] == lastChemiName and line[3] == lastGeneSymbol):
                    line_dict = dict(zip(head, line))
                    line_dict["ChemicalID"] = "MESH:"+line_dict["ChemicalID"]
                    for elearray in harray:
                        line_dict[elearray]=line_dict[elearray].strip().split('|')
                    lastChemiName=line_dict["ChemicalName"]
                    lastGeneSymbol=line_dict["GeneSymbol"]
                    #find chemical
                    ChemiExitNode = Cgraph.nodes.match("Chemical", id=line_dict["ChemicalID"]).first()
                    if not ChemiExitNode:
                        continue

                    #find gene symbol
                    GeneExitNode = Cgraph.nodes.match("GENE", attribute_gene_name=line_dict["GeneSymbol"]).first()
                    if not GeneExitNode:
                        continue

                    #create relationship
                    ChemiRelation = Relationship(ChemiExitNode, 'CInteractionG', GeneExitNode, **line_dict)
                    Cgraph.create(ChemiRelation)

                    relcount+=1
                    if relcount%100==0:
                        print(relcount)


def CreateChemicalDiseaseRelationship(file="data/CTD_chemicals_diseases.csv"):
    head=["ChemicalName","ChemicalID","CasRN","DiseaseName","DiseaseID","DirectEvidence","InferenceGeneSymbol","InferenceScore","OmimIDs","PubMedIDs"]
    headarray=["DirectEvidence","OmimIDs","PubMedIDs"]
    relcount = 0
    graph = Graph("http://localhost:7474")
    with open(file, mode='r',encoding='utf-8') as fr:
        reader = csv.reader(fr)
        for line in reader:
            if not line:
                break
            if not line[0].startswith("#") and line[7]!="" and float(line[7])>=8:
                line_dict = dict(zip(head, line))
                line_dict["ChemicalID"] = "MESH:" + line_dict["ChemicalID"]
                for elearray in headarray:
                    line_dict[elearray] = line_dict[elearray].strip().split('|')
                # find chemical
                ChemiExitNode = graph.nodes.match("Chemical", id=line_dict["ChemicalID"]).first()
                if not ChemiExitNode:
                    continue

                # find disease
                DiseaseExitNode = graph.nodes.match("Disease", id=line_dict["DiseaseID"]).first()
                if not DiseaseExitNode:
                    continue

                # create relationship
                ChemiRelation = Relationship(ChemiExitNode, 'CInteractionD', DiseaseExitNode, **line_dict)
                graph.create(ChemiRelation)

                relcount += 1
                if relcount % 100 == 0:
                    print(relcount)

def CreateChemicalPathwayRelationship(file="data/CTD_chem_pathways_enriched.csv"):
    head=["ChemicalName","ChemicalID","CasRN","PathwayName","PathwayID","PValue","CorrectedPValue","TargetMatchQty","TargetTotalQty","BackgroundMatchQty","BackgroundTotalQty"]
    relcount = 0
    graph = Graph("http://localhost:7474")
    with open(file, mode='r',encoding='utf-8') as fr:
        reader = csv.reader(fr)
        for line in reader:
            if not line:
                break
            if not line[0].startswith("#"):
                line_dict = dict(zip(head, line))
                line_dict["ChemicalID"] = "MESH:" + line_dict["ChemicalID"]
                # find chemical
                ChemiExitNode = graph.nodes.match("Chemical", id=line_dict["ChemicalID"]).first()
                if not ChemiExitNode:
                    continue

                # find pathway
                PathwayExitNode = graph.nodes.match("Pathway", id=line_dict["PathwayID"]).first()
                if not PathwayExitNode:
                    continue

                # create relationship
                ChemiRelation = Relationship(ChemiExitNode, 'CInteractionP', PathwayExitNode, **line_dict)
                graph.create(ChemiRelation)

                relcount += 1
                if relcount % 100 == 0:
                    print(relcount)

#file too large, only pick three relationship from one chemical
def CreateChemicalGORelationship(file="data/CTD_chem_go_enriched.csv"):
    head=["ChemicalName","ChemicalID","CasRN","Ontology","GOTermName","GOTermID","HighestGOLevel","PValue","CorrectedPValue","TargetMatchQty","TargetTotalQty","BackgroundMatchQty","BackgroundTotalQty"]
    relcount = 0
    graph = Graph("http://localhost:7474")
    lastChemiID=""
    lastChemiNode=0
    ChemiLimit=0
    with open(file, mode='r',encoding='utf-8') as fr:
        reader = csv.reader(fr)
        for line in reader:
            if not line:
                break
            if not line[0].startswith("#"):
                line_dict = dict(zip(head, line))
                line_dict["ChemicalID"] = "MESH:" + line_dict["ChemicalID"]
                if line_dict["ChemicalID"] != lastChemiID:
                    ChemiLimit=0
                if ChemiLimit >=100:
                    continue
                # find chemical
                if ChemiLimit==0:
                    ChemiExitNode = graph.nodes.match("Chemical", id=line_dict["ChemicalID"]).first()
                    if not ChemiExitNode:
                        continue
                    else:
                        lastChemiNode = ChemiExitNode
                        lastChemiID=line_dict["ChemicalID"]
                else:
                    ChemiExitNode = lastChemiNode
                ChemiLimit += 1

                # find GO
                GOExitNode = graph.nodes.match("GO", id=line_dict["GOTermID"]).first()
                if not GOExitNode:
                    continue

                # create relationship
                if ChemiExitNode and GOExitNode:
                    ChemiRelation = Relationship(ChemiExitNode, 'CInteractionGO', GOExitNode, **line_dict)
                    graph.create(ChemiRelation)

                relcount += 1
                if relcount % 500 == 0:
                    print(relcount)


if __name__ == '__main__':
    #CreateChemicalGeneRelationship()

    # CreateChemicalPathwayRelationship()
    # print("C-P association done!")
    # CreateChemicalDiseaseRelationship()
    # print("C-D association done!")
    CreateChemicalGORelationship()
    print("ALL done!")