import forest_util as fut
import os
'''
Calculate forest summary topologies.
'''
    
class CalcSummary:

    def __init__(self, path, filePrefix, toBeSortedOn):
        # Can sometimes be a single number, for example, the node count
        self.returnList = []
        self.path = path
        self.graph = None
        self.fP = filePrefix
        self.attr = toBeSortedOn


    '''
    parses a optimizedForest.sif file. pp is undirected, pd directed.
    networkx currently does not support mixed graphs, so for all pp edges,
    a directed edge both to and from each node in the entry is created.
    '''
    def make_graph(self):
        self.graph = fut.loadGraph(os.path.join(self.path, self.fP + "optimalForest.sif"))

    # In the future, could also have keywords that compute and return
    # multiple statistics
    def calcStatistic(self):
        '''
        call appropriate test statistic function here, using toBeSortedOn

        store results in self.returnList
        '''        
        if self.attr == "nn":
            self.returnList = self.num_nodes()

    '''
    returns a single array containing the parameters and a list of 
    summary statistics for a particular --sweep option. 
    The idea being that this list can be formatted in any way that is most convenient,
    as long as the corresponding sorting function for the same --sweep option in 
    SortSum.py knows the format of the incoming data.
    '''
    def getSummary(self):
        self.make_graph()
        self.calcStatistic()
        return self.returnList
        
        
    '''
    Write test statistic calculating functions here

    '''
    def num_nodes(self):
        return self.graph.order()
