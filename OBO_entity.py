import csv
from py2neo import Graph, Node, Relationship

OBOArrayField=['xref','synonym','is_a','alt_id','intersection_of','relationship','property_value']
#input file: xxx.obo
#input type: HPO, DO, SO, GO
def CreateOBOEntity(file, type):
    OBOgraph = Graph("http://localhost:7474")
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
                    if strtmp[0] in OBOArrayField:
                    #if strtmp[0] == 'xref' or strtmp[0] == 'synonym' or strtmp[0] == 'is_a' or strtmp[0] == 'alt_id': #array
                        if strtmp[0].strip() in node:
                            node[strtmp[0].strip()].append(strtmp[1].strip())
                        else:
                            node[strtmp[0].strip()] = [strtmp[1].strip()]
                    else:
                        node[strtmp[0].strip()] = strtmp[1].strip()
                #create node
                exitNodelist = list(OBOgraph.nodes.match(type, id=node['id']))
                # if len(exitNodelist) > 1:
                #     print("error, search more node ", node['id'])
                #     exit()
                if len(exitNodelist) >= 1:
                    exitNode=exitNodelist[0]
                    for ele in node:
                        exitNode[ele]=node[ele]
                    OBOgraph.push(exitNode)
                    currentNode=exitNode
                else:
                    NewNode = Node(type,**node)
                    OBOgraph.create(NewNode)
                    currentNode=NewNode
                #create relationship
                if 'is_a' in node:
                    for Parentele in node['is_a']:
                        Parentid = Parentele.split(' ! ')[0].strip()
                        ParentExitNode = OBOgraph.nodes.match(type, id=Parentid).first()
                        if ParentExitNode:
                            childrelation = Relationship(currentNode, 'father', ParentExitNode)
                        else:
                            NewNodeEnd = Node(type, id=Parentid)
                            childrelation = Relationship(currentNode,'father',NewNodeEnd)
                        OBOgraph.create(childrelation)
                if type=='Disease':
                    if 'alt_id' in node:
                        for altele in node['alt_id']:
                            if "DO" in altele:
                                DOID = altele.strip()[3:] #DOID:xxxx
                                AltExitNode = OBOgraph.nodes.match('DO', id=DOID).first()
                                if AltExitNode:
                                    childrelation = Relationship(currentNode, 'alt', AltExitNode)
                                    OBOgraph.create(childrelation)
                            elif "OMIM" in altele:
                                OMIMID = altele.strip()
                                AltExitNode = OBOgraph.nodes.match('OMIM', id=OMIMID).first()
                                if AltExitNode:
                                    childrelation = Relationship(currentNode, 'alt', AltExitNode)
                                    OBOgraph.create(childrelation)
                            else:
                                continue


                nodecount+=1
                if nodecount%100==0:
                    print(nodecount)



if __name__ == '__main__':
    #CreateOBOEntity("data/hp.obo","HPO")
    #CreateOBOEntity("data/so.obo","SO")
    #CreateOBOEntity("data/doid.obo", "DO")
    #CreateOBOEntity("data/go.obo", "GO")
    #CreateOBOEntity("data/CTD_diseases.obo", "Disease")
    CreateOBOEntity("data/CTD_exposure_ontology.obo", "ExO")
    print("ALL done!")