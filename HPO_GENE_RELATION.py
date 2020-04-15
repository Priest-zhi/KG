import csv
from py2neo import Graph, Node, Relationship

def CreateHPOGeneAssociation(file='data/hpo_gene.csv'):
    RelCount=0
    HPOGENEgraph = Graph("http://localhost:7474")
    with open(file, 'r') as fr:
        reader = csv.DictReader(fr)
        for line in reader:
            if not line:
                break
            if line["HPO_Term_ID"] and line["entrez_gene_symbol"]:
                #search HPO node
                exitHPONodelist = list(HPOGENEgraph.nodes.match("HPO", id=line["HPO_Term_ID"]))
                # if len(exitHPONodelist) > 1:
                #     print("error, search more node ", line["HPO_Term_ID"])
                #     exit()
                if len(exitHPONodelist) >= 1:   #ignore duplicate hpo
                    currentHPONode=exitHPONodelist[0]
                else:   #create node
                    continue
                    # HPNode = Node("HPO",id=line["HPO_Term_ID"],name=line["HPO_Term_Name"])
                    # HPOGENEgraph.create(HPNode)
                    # currentHPONode=HPNode

                #search gene node
                exitGENENodelist = list(HPOGENEgraph.nodes.match("GENE", attribute_gene_name=line["entrez_gene_symbol"]))
                # if len(exitGENENodelist) > 1:
                #     print("error, search more node ", line["entrez_gene_symbol"])
                #     exit()
                if len(exitGENENodelist) >= 1:  #ignore duplicate gene
                    currentGENENode=exitGENENodelist[0]
                else:   #create node
                    continue
                    # GENENode = Node("GENE",attribute_gene_name=line["entrez_gene_symbol"])
                    # HPOGENEgraph.create(GENENode)
                    # currentGENENode=GENENode

                #create relationship
                if currentHPONode and currentGENENode:
                    #one relationship for two-way
                    HPO_GENE_relation = Relationship(currentHPONode, 'Association', currentGENENode)
                    HPOGENEgraph.create(HPO_GENE_relation)
                    #GENE_HPO_relation = Relationship(currentGENENode, 'Association', currentHPONode)
                    #HPOGENEgraph.create(GENE_HPO_relation)

                RelCount+=1
                if RelCount%100 ==0:
                    print(RelCount)


if __name__ == '__main__':
    CreateHPOGeneAssociation()
    print("ALL done!")