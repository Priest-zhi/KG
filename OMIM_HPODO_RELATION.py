import csv
from py2neo import Graph, Node, Relationship


def CreateOMIM_HPO_RELATIONSHIP(file='data/OMIM_HPO.csv'):
    RelCount=0
    OHgraph = Graph("http://localhost:7474")
    with open(file, 'r') as fr:
        reader = csv.DictReader(fr)
        for line in reader:
            if not line:
                break
            if line["DB"] == "OMIM" and "OMIM:" in line["DB_Reference"]:
                #get HPO node
                exitHPONodelist = list(OHgraph.nodes.match("HPO", id=line["HPO_ID"]))
                if len(exitHPONodelist) == 0:
                    continue
                else:
                    currentHPONode = exitHPONodelist[0]

                #get OMIM node
                exitOMIMNodelist = list(OHgraph.nodes.match("OMIM", id=line["DB_Reference"]))
                if len(exitOMIMNodelist) == 0:
                    OMIMNode = Node("OMIM",id=line["DB_Reference"],name=line["DB_Name"])
                    OHgraph.create(OMIMNode)
                    currentOMIMNode=OMIMNode
                else:
                    currentOMIMNode = exitOMIMNodelist[0]

                if currentHPONode and currentOMIMNode:
                    HPO_OMIM_relation = Relationship(currentHPONode, 'Association', currentOMIMNode)
                    OHgraph.create(HPO_OMIM_relation)

                RelCount+=1
                if RelCount%100==0:
                    print(RelCount)


def CreateOMIM_DO_RELATIONSHIP():
    RelCount = 0
    ODgraph = Graph("http://localhost:7474")
    resultDOs = ODgraph.run('MATCH (n:DO) RETURN n').data()
    for do in resultDOs:
        doNode = do["n"]
        if "xref" in doNode:
            xref = doNode["xref"]
            for ele in xref:
                if "OMIM" in ele:
                    #get OMIM node
                    exitOMIMNodelist = list(ODgraph.nodes.match("OMIM", id=ele))
                    if len(exitOMIMNodelist) == 0:
                        #no omim name, couldn't create node
                        continue
                    else:
                        currentOMIMNode = exitOMIMNodelist[0]
                    # get DO node
                    exitDONodelist = list(ODgraph.nodes.match("DO", id=doNode["id"]))
                    if len(exitDONodelist) == 0:
                        continue
                    else:
                        currentDONode = exitDONodelist[0]
                    #create relationship
                    if currentOMIMNode and currentDONode:
                        DO_OMIM_relation = Relationship(currentDONode, 'Association', currentOMIMNode)
                        ODgraph.create(DO_OMIM_relation)

                    RelCount += 1
                    if RelCount % 100 == 0:
                        print(RelCount)

if __name__ == '__main__':
    CreateOMIM_HPO_RELATIONSHIP()
    CreateOMIM_DO_RELATIONSHIP()
    print("All done!")