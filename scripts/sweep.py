'''
parameter sweep
'''
import re, sys, os, CalcSummary, SortSum
import numpy as np

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
    
    sumFile = open(options.outputpath + "/summary_statistics", w+)
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
                
                summaryObject = CalcSummary(abs_path, options.outputlabel, options.toSweepOn)
                sumListEntry.append(summaryObject.getSummary())

                sumList.append(sumListEntry)

    finalSumObject = SortSum(sumList, options.toSweepOn)
    toPrintList = finalSumObject.getSumList()

    sumFile.write('w\tb\tD\t{}\n'.format(toSweepOn))
    for item in toPrintList:
        for x in range(len(item) - 1):
            sumFile.write(item[x] + '\t')
        sumFile.write(item[len(item) - 1] + '\n')
    
    sumFile.close()
    
                
                
                
                
                 
