import csv
from py2neo import Graph, Node, Relationship

def CreateExposureEntityAndRelationship(file="data/CTD_exposure_studies.csv"):
    nodecount = 0
    head=["id","studyfactors","exposurestressors","receptors","studycountries","mediums","exposuremarkers","diseases","phenotypes","authorsummary"]
    harray = ["studyfactors", "exposurestressors", "receptors", "studycountries", "mediums","exposuremarkers", "diseases", "phenotypes"]
    type="Exposure"
    Egraph = Graph("http://localhost:7474")
    with open(file, mode='r',encoding='utf-8') as fr:
        reader = csv.reader(fr)
        for line in reader:
            if not line:
                break
            if not line[0].startswith("#"):
                #line_list = line.strip('\n').split(',')
                line_dict = dict(zip(head, line))
                for elearray in harray:
                    line_dict[elearray]=line_dict[elearray].strip().split('|')
                #create node
                NewNode = Node(type, **line_dict)
                Egraph.create(NewNode)

                #create relationship
                #chemical
                for chemi in line_dict["exposurestressors"]:
                    if chemi == '':
                        break
                    chemiID = chemi.split('^')[2]+":"+chemi.split('^')[1]
                    ChemiExitNode = Egraph.nodes.match("Chemical", id=chemiID).first()
                    if ChemiExitNode:
                        ChemiRelation = Relationship(ChemiExitNode, 'in', NewNode)
                        Egraph.create(ChemiRelation)
                #Diseases
                for dises in line_dict["diseases"]:
                    if dises == '':
                        break
                    diseID = dises.split('^')[2]+":"+dises.split('^')[1]
                    DiseExitNode = Egraph.nodes.match("Disease", id=diseID).first()
                    if DiseExitNode:
                        DiseRelation = Relationship(NewNode, 'leadtoD', DiseExitNode)
                        Egraph.create(DiseRelation)
                #Phenotypes
                for pht in line_dict["phenotypes"]:
                    if pht == '':
                        break
                    phtID=pht.split('^')[1]
                    GOExitNode = Egraph.nodes.match("GO", id=phtID).first()
                    if GOExitNode:
                        GORelation = Relationship(NewNode, 'leadtoG', GOExitNode)
                        Egraph.create(GORelation)

                nodecount += 1
                if nodecount % 100 == 0:
                    print(nodecount)

if __name__ == '__main__':
    CreateExposureEntityAndRelationship()
    print("ALL done!")