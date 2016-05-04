'''
Sort a sumList, based on the user attribute provided.
'''

class SortSum:
    
    def __init__(self, sumList, attribute):
        self.sumList = sumList
        self.attr = attribute

        '''
        ensure that this is a 2D array,
        each row should be a 1D list for the summary statistics of
        a Steiner Forest
        '''
        self.toPrintList = []
        
        self.sort()

    def sort(self):
        '''
        sort the list here, by calling the appropriate function
        based on self.attr
        store results in self.toPrintList
        '''

    def getSumList(self):
        return self.toPrintList

    '''
    write sorting functions here for each possible self.attr
    '''
