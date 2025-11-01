import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Characters.Character import Character
from Relationships.Relationship import Relationship
import networkx as nx

class Graph :
    """
    Classe représantant le graphe de relation
    """

    def __init__(self):
        
        self.listNode = []
        self.listEdge = []
        self.nxGraph = nx.DiGraph()

    def addNode(self, name, caractere, personality):
        newCharacter = Character(name, caractere, personality)
        self.listNode.append(newCharacter)

        info = {'caractere':caractere, 'personality':personality}
        self.nxGraph.add_node(name, **info)

    def removeNode(self, character):
        self.listNode = [node for node in self.listNode if node != character]
        self.listEdge = [edge for edge in self.listEdge if edge.source != character and edge.target != character]
        self.nxGraph.remove_node(character)

    def updateNode(self, oldName, newName, caractere, personality):
        if oldName != newName :
            self.addNode(newName, caractere, personality)
            for edge in self.listEdge:
                if edge.source == oldName:
                    self.addEdge(newName, edge.target, edge.typeRelationship)
                    self.removeEdge(edge.source, edge.target)
                elif edge.target == oldName:
                    self.addEdge(edge.source, newName, edge.typeRelationship)
                    self.removeEdge(edge.source, edge.target)
            self.removeNode(self.getNode(oldName))
            return
        
        node = self.getNode(oldName)
        node.caractere = caractere
        node.personality = personality

    def getNode(self, name):
        for node in self.listNode:
            if node.name == name:
                return node
        return None
    
    def getNodeNames(self):
        return [node.name for node in self.listNode]

    def addEdge(self, source, target, typeRelationship):
        newRelationship = Relationship(source, target, typeRelationship)
        self.listEdge.append(newRelationship)

        info = {'typeRelationship':typeRelationship}
        self.nxGraph.add_edge(source, target, **info)

    def removeEdge(self, source, target):
        self.listEdge = [edge for edge in self.listEdge if not (edge.source == source and edge.target == target)]
        self.nxGraph.remove_edge(source, target)

    def updateEdge(self, source, target, typeRelationship):
        self.removeEdge(source, target)
        self.addEdge(source, target, typeRelationship)

    def getEdge(self, source, target):
        for edge in self.listEdge :
            if edge.source == source and edge.target == target:
                return edge
        return None
    
    def toNetworkx(self):
        return self.nxGraph
    