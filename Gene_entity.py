import csv
from py2neo import Graph, Node, Relationship

def GTF2GENE_entity(file='data/gtf.csv'):
    nodecount=0
    GENEgraph = Graph("http://localhost:7474")
    with open(file, 'r') as fr:
        reader = csv.DictReader(fr)
        for line in reader:
            if not line:
                break
            if line["feature"] == "gene":
                node={}
                for ele in line:
                    if "." in ele:
                        newele = ele.replace('.', '_')
                        node[newele]=line[ele]
                    else:
                        node[ele] = line[ele]
                GeneNode = Node("GENE", **node)
                GENEgraph.create(GeneNode)

                nodecount+=1
                if nodecount%100 ==0:
                    print(nodecount)


if __name__ == '__main__':
    GTF2GENE_entity()
    print("ALL done!")