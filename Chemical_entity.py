import csv
from py2neo import Graph, Node, Relationship

#drop, this function is too slow
def CreateChemicalEntityAndRelationship(file='data/CTD_chemicals.csv'):
    nodecount=0
    head=["name","id","CasRN","Definition","ParentIDs","TreeNumbers","ParentTreeNumbers","Synonyms","DrugBankIDs"]
    type="Chemical"
    Cgraph = Graph("http://localhost:7474")
    with open(file, mode='r',encoding='utf-8') as fr:
        while True:
            line = fr.readline()
            if not line:
                break
            if not line.startswith("#"):
                line_list = line.strip('\n').split(',')
                line_dict = dict(zip(head, line_list))
                Parentslist= line_dict["ParentIDs"].strip().split('|')
                line_dict["ParentIDs"] = Parentslist
                #create node
                exitNodelist = list(Cgraph.nodes.match(type, id=line_dict['id']))
                if len(exitNodelist) >= 1:
                    exitNode=exitNodelist[0]
                    for ele in line_dict:
                        exitNode[ele]=line_dict[ele]
                    Cgraph.push(exitNode)
                    currentNode=exitNode
                else:
                    NewNode = Node(type,**line_dict)
                    Cgraph.create(NewNode)
                    currentNode=NewNode

                #create relationship
                if line_dict["ParentIDs"]:
                    for ParentEle in line_dict["ParentIDs"]:
                        ParentExitNode = Cgraph.nodes.match(type, id=ParentEle).first()
                        if ParentExitNode:
                            childrelation = Relationship(currentNode, 'father', ParentExitNode)
                        else:
                            NewNodeEnd = Node(type, id=ParentEle)
                            childrelation = Relationship(currentNode,'father',NewNodeEnd)
                        Cgraph.create(childrelation)

                nodecount+=1
                if nodecount%100==0:
                    print(nodecount)


def CreateChemicalEntity(file='data/CTD_chemicals.csv'):
    nodecount=0
    head=["name","id","CasRN","Definition","ParentIDs","TreeNumbers","ParentTreeNumbers","Synonyms","DrugBankIDs"]
    type="Chemical"
    Cgraph = Graph("http://localhost:7474")
    with open(file, mode='r',encoding='utf-8') as fr:
        while True:
            line = fr.readline()
            if not line:
                break
            if not line.startswith("#"):
                line_list = line.strip('\n').split(',')
                line_dict = dict(zip(head, line_list))
                Parentslist= line_dict["ParentIDs"].strip().split('|')
                line_dict["ParentIDs"] = Parentslist
                #create node
                NewNode = Node(type, **line_dict)
                Cgraph.create(NewNode)

                nodecount+=1
                if nodecount%100==0:
                    print(nodecount)


def CreateChemicalRelationship():
    nodecount = 0
    Cgraph = Graph("http://localhost:7474")
    resultChemicals = Cgraph.run('MATCH (n:Chemical) RETURN n').data()
    for node in resultChemicals:
        ChemicalNode = node["n"]
        if ChemicalNode["ParentIDs"]:
            for ParentEle in ChemicalNode["ParentIDs"]:
                if ParentEle=='':
                    break
                ParentExitNode = Cgraph.nodes.match("Chemical", id=ParentEle).first()
                if ParentExitNode:
                    childrelation = Relationship(ChemicalNode, 'father', ParentExitNode)
                    Cgraph.create(childrelation)

            nodecount += 1
            if nodecount % 100 == 0:
                print(nodecount)

if __name__ == '__main__':
    #CreateChemicalEntity()
    CreateChemicalRelationship()
    print("ALL done!")