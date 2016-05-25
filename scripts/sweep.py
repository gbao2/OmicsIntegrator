'''
parameter sweep
'''
import re, sys, os, SortSum, argparse
import CalcSummary as cs
import SortSum as ss
import numpy as np
import networkx as nx

def paramSweep(options):
    
    vals = {
        'w':None,
        'b':None,
        'D':None,
        'mu':None,
        'r':None,
        'g':None,
    }

    try:

        params = options.confFile    
        with open(params, 'r') as file:
            lines = file.readlines()
            for line in lines:
                mtch = re.match(r'([wbDrg]|[m][u])\s[=]\s[[](\d+\.?\d*)[:](\d+\.?\d*)[:](\d+\.?\d*)[]]\s',
                                line)        
                vals[mtch.group(1)] = [int(mtch.group(2)), int(mtch.group(3)), int(mtch.group(4))]    
    except AttributeError as e:
        print "Improper sweep config file formatting, exiting.", e
        sys.exit(e)        
    except re.error as e:
        print "Improper sweep config file formatting, exiting.", e
        sys.exit(e)

    if vals['w'] == None or vals['b'] == None or vals['D'] == None:
        print 'Missing a required config parameter for sweep. (w, b and D)'
        sys.exit(e)

    w_range = np.arange(vals['w'][0], vals['w'][1], vals['w'][2])
    b_range = np.arange(vals['b'][0], vals['b'][1], vals['b'][2])
    D_range = np.arange(vals['D'][0], vals['D'][1], vals['D'][2])
    
    sumFile = open(os.path.join(options.outputpath + "/summary_statistics"), "w+")
    sumList = []
    for w in w_range:
        for b in b_range:
            for D in D_range:
                dirname = 'w' + str(w) + '_' + 'b' + str(b) + '_' + 'D' + str(D)
                abs_path = os.path.join(options.outputpath, dirname)
                os.makedirs(abs_path)
                
                conf_path = os.path.join(abs_path, 'conf')
                with open(conf_path, 'w') as confFile:
                    confFile.write('w = {}\n'.format(w))
                    confFile.write('b = {}\n'.format(b))
                    confFile.write('D = {}\n'.format(D))
                    
                os.system("python forest.py --prize %s --edge %s --conf %s --msgpath %s --outpath %s" %(options.prizeFile,options.edgeFile, conf_path, options.msgpath, abs_path))
                
                sumListEntry = []
                sumListEntry.append(w)
                sumListEntry.append(b)
                sumListEntry.append(D)
                
                summaryObject = cs.CalcSummary(abs_path, options.outputlabel, options.sweep)
                sumListEntry.append(summaryObject.getSummary())

                sumList.append(sumListEntry)

    finalSumObject = ss.SortSum(sumList, options.sweep)
    toPrintList = finalSumObject.getSumList()

    sumFile.write('w\tb\tD\t{}\n'.format(options.sweep))
    for item in toPrintList:
        for x in range(len(item) - 1):
            sumFile.write(str(item[x]) + '\t')
        sumFile.write(str(item[len(item) - 1]) + '\n')
    
    sumFile.close()
    
def justSum(options):    
    
    runs = [x[0] for x in os.walk(options.outputpath)]
    sumList = []
    params = []
    first = True 
    runs = runs[1:]

    '''
    iterate through the folders in options.outputpath, parsing the 
    config file, and creating a CalcSummary object to calculate the desired
    topology for each run. Then creates a SortSum object to sort said list
    of forest runs.

    '''
    for run in runs:  
        sumListEntry = []
        with open(os.path.join(run, options.confFile)) as conf:                        
            for line in conf:
                ln = line.split()
                sumListEntry.append(float(ln[2].rstrip()))
                if first:
                    params.append(ln[0])
        summaryObject = cs.CalcSummary(run, options.outputlabel, options.sweep)
        sumListEntry.append(summaryObject.getSummary())
        sumList.append(sumListEntry)
        first = False

    finalSumObject = ss.SortSum(sumList, options.sweep)
    toPrintList = finalSumObject.getSumList()

    with open(os.path.join(options.outputpath + "/summary_statistics"), "w+") as sumFile:
        sumFile.write('w\tb\tD\t{}\n'.format(options.sweep))
        for item in toPrintList:
            for x in range(len(item) - 1):
                sumFile.write(str(item[x]) + '\t')
            sumFile.write(str(item[len(item) - 1]) + '\n')
            
            
    

if __name__ == "__main__":
    '''
    options.outputpath = the directory which contains the set of forest runs, each with
    their own folder
    options.sweep = what topology you want to sort on, currently only "nn" is supported 
    (number of nodes)
    options.confFile = name of your configuration file. must be the same for each forest
    run
    options.outputlabel = what you told forest to append to the front of the 
    result of a Forest run. Include the leading "_" that Forest appends
    to your outputlabel

    If you are running sweep.py independently, it is assumed that you are doing a 
    summarization over pre-ran Forest files. 

    '''
    parser = argparse.ArgumentParser(description='Standalone sweep')
    parser.add_argument("--sweep", dest='sweep', help='Attribute to sort Steiner Forests. Check Readme for full list.', 
                        default=None)
    parser.add_argument("--outpath", dest = 'outputpath', help='Path to the directory which '\
                        'holds the output folders.', default='.')
    parser.add_argument("--outlabel", dest = 'outputlabel', help='A string put at the beginning '\
                        'of the names of files output by the program. Default = "result"', default='result')
    parser.add_argument("-c", "--conf", dest='confFile', help='Path to the text file containing '\
                        'the parameters. Should be several lines that looks like: "ParameterName = '\
                        'ParameterValue". Must contain values for w, b, D.  May contain values for optional '\
                        'parameters mu, n, r, g. Default = "./conf.txt"', default='conf.txt')
    options = parser.parse_args()
    if options.sweep != None:
        justSum(options)
    else:
        print "Please provide a topology to summarize over."
    
