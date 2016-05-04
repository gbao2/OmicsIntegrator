'''
Calculate forest summary topologies.
'''

class CalcSummary:
    
    def __init__(self, path, filePrefix, toBeSortedOn):
        self.returnList = []
        self.path = path
        self.filePrefix = filePrefix
        self.attr = toBeSortedOn
        self.calcStatistic(toBeSortedOn)


    def calcStatistic(self, attribute):
        '''
        call appropriate test statistic function here, using toBeSortedOn
        store results in self.returnList
        '''        

    def getSummary(self):
        return self.returnList
        

    '''
    Write test statistic calculating functions here

    '''


    
