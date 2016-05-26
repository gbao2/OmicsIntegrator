'''
Sort a sumList, based on the user attribute provided.
'''
from operator import itemgetter
class SortSum:
    
    def __init__(self, sumList, attribute):
        self.sumList = sumList
        self.attr = attribute

        '''
        ensure that this is a strictly a 2D array,
        each row should be a 1D list for the summary statistics of
        a Steiner Forest, including parameters, and all parameters
        should be listed in the same order    
        '''
        self.toPrintList = []
        

    def sort(self):
        '''
        sort the list here, by calling the appropriate function
        based on self.attr
        store results in self.toPrintList
        '''
        if self.attr == "nn":
            self.toPrintList = self.nnSort()
            
    # Could reuse some of the sorting functions, for example, if an
    # edge count was added it would be sorted the same way as the node count
    '''
    the return list in CalcStatistics.py is of a single value in an array, and
    therefore  the assumed structure of self.sumList is [params, x] for a run of
    sweep.py with --sweep="nn"
    '''    
    def nnSort(self):
        rList = []
        for x in range(len(self.sumList)):
            curr = []
            for y in range(len(self.sumList[x])):
                curr.append(self.sumList[x][y])
            rList.append(curr)
        rList = sorted(rList, key=itemgetter(len(rList[0]) - 1), reverse=True)
        return rList
        
    "returns the sorted list of network topologies"
    def getSumList(self):
        self.sort()
        return self.toPrintList

    '''
    write sorting functions here for each possible self.attr
    '''
