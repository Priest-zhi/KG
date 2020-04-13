import csv
from py2neo import Graph, Node, Relationship

def CreateHPOEntity(file = "data/hp.obo"):
    HPgraph = Graph("http://localhost:7474")
    nodecount = 0
    with open(file, 'r') as fr:
        while True:
            line = fr.readline()
            if not line:
                break
            if line.startswith("[Term]"):
                #read line
                node = {}
                while line:
                    line = fr.readline().strip('\n')
                    if line == '':
                        break
                    strtmp = line.split(": ")

                    if strtmp[1].strip().startswith('"'):
                        strtmp[1]=strtmp[1].strip().split('"')[1]
                    if strtmp[0] == 'xref' or strtmp[0] == 'synonym' or strtmp[0] == 'is_a' or strtmp[0] == 'alt_id': #array
                        if strtmp[0].strip() in node:
                            node[strtmp[0].strip()].append(strtmp[1].strip())
                        else:
                            node[strtmp[0].strip()] = [strtmp[1].strip()]
                    else:
                        node[strtmp[0].strip()] = strtmp[1].strip()
                #create node
                exitNodelist = list(HPgraph.nodes.match("HPO", id=node['id']))
                if len(exitNodelist) > 1:
                    print("error, search more node ", node['id'])
                    exit()
                if len(exitNodelist) == 1:
                    exitNode=exitNodelist[0]
                    for ele in node:
                        exitNode[ele]=node[ele]
                    HPgraph.push(exitNode)
                    currentNode=exitNode
                else:
                    HPNode = Node("HPO",**node)
                    HPgraph.create(HPNode)
                    currentNode=HPNode
                #create relationship
                if 'is_a' in node:
                    for childele in node['is_a']:
                        childid = childele.split(' ! ')[0].strip()
                        childExitNode = HPgraph.nodes.match("HPO", id=childid).first()
                        if childExitNode:
                            childrelation = Relationship(currentNode, 'father', childExitNode)
                        else:
                            HPNodeEnd = Node("HPO", id=childid)
                            childrelation = Relationship(currentNode,'father',HPNodeEnd)
                        HPgraph.create(childrelation)

                nodecount+=1
                if nodecount%100==0:
                    print(nodecount)

if __name__ == '__main__':
    #CreateHPOEntity("data/hptext")
    CreateHPOEntity()
    print("ALL done!")