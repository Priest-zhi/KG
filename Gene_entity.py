import csv
from py2neo import Graph, Node, Relationship

def GTF2GENE_entity(file='/data/gtf.csv'):
    with open(file, 'r') as fr:
        reader = csv.DictReader(fr)
        for line in reader:
            if not line:
                break
            if line["feature"] == "gene":
            rcon2.lpush(line['Value'].strip(), line['SO ID']+'|'+ line['SO Term'])

if __name__ == '__main__':
    pass