import csv
from py2neo import Graph, Node, Relationship

def CreatePathwayEntity(file='data/CTD_pathways.csv'):
    nodecount=0
    Pgraph = Graph("http://localhost:7474")
    with open(file, 'r') as fr:
        while True:
            line = fr.readline()
            if not line:
                break
            if not line.startswith("#"):
                lineP = line.strip('\n').split(',')
                node = {'id':lineP[1], 'name':lineP[0]}
                PNode = Node("Pathway", **node)
                Pgraph.create(PNode)


if __name__ == '__main__':
    CreatePathwayEntity()
    print("ALL done!")