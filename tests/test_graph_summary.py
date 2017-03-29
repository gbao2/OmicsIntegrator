import os, sys, pytest, copy
from numpy import isclose

# import repo's tests utilities
cur_dir = os.path.dirname(__file__)
path = os.path.abspath(os.path.join(cur_dir, '..', 'tests'))
if not path in sys.path:
    sys.path.insert(1, path)
del path
import test_util

# Set arguments used in all forest tests:
# Define all but the b (beta) parameter here; vary beta for the tests
conf_params = {
    'w': 1,
    'D': 5,
    'mu': 2,
    'g': 0
}
# Location of the prize, network, and root node files
forest_opts = {
  'prize': os.path.join(cur_dir, 'small_forest_tests', 'beta_mu_test_prizes.txt'),
  'edge': os.path.join(cur_dir, 'small_forest_tests', 'beta_mu_test_network.txt'),
  'dummyMode': os.path.join(cur_dir, 'small_forest_tests', 'beta_mu_test_roots.txt')
}

class TestGraphSummary:
    '''
    Simulate a parameter sweep and test summarizing multiple optimal forests
    obtained under different parameters.    
    
    The forests are generated by testing various values of the beta parameter
    with respect to its interaction with a non-zero mu
    p'(v) = beta * p(v) - mu * deg(v)
    min f'(F) = sum_{v not in V_F} p'(v) + sum_{e in E_F} c(e) + w * K
    c(e) = 1 - c'(e) [c' is "confidence" while c is "cost"]

    The mu parameter is typically used in practice to exclude well-studied proteins
    that appear as high-confidence hubs in bioinformatics databases.

    Use the following test network (with directed edges as mentioned in c' below):

      B - A - D
       \ / \ /
        C   E

    p(A) = 5
    p(B) = 6
    p(C) = 6
    p(D) = 6
    p(E) = 6
    c'(AB) = 0.9
    c'(AC) = 0.9
    c'(AD) = 0.9
    c'(AE) = 0.9
    c'(BC) = 0.1
    c'(DE) = 0.1
    '''
    def test_graph_summary_beta(self, msgsteiner):
        '''
        In p'(v) = beta * p(v) - mu * deg(v), beta = 1 is too small to overcome the hub penalty with mu = 2:
          p'(A) = 1*5 - 2*4 = -3
        We expect forest to use the more costly edges BC and CD in its network instead.
        The graph will have 4 nodes and 2 edges.
        
        beta = 2 is enough to overcome the hub penalty so that the hub at A is chosen:
          p'(A) = 2*5 - 2*4 = 2
        The graph will have 5 nodes and 4 edges.
        
        beta = 0.001 is too small to connect any prizes.
        The graph will have 0 nodes and 0 edges.
        '''
        ### TODO verify the beta = 0.001 behavior
        beta_sweep = [1, 2, 0.001]
        for beta in beta_sweep:
            params = copy.deepcopy(conf_params)
            params['b'] = beta_sweep
            ### TODO add outpath to forest_opts before running
            ### TODO need to make sure the output files are not overwritten
            # by adding outlabel to run_forest and making the outlabel contain
            # beta
            test_util.run_forest(msgsteiner, params, forest_opts)
        
        ### TODO run forest_util.summaryGraphs
        ### TODO modify path to import forest_util
        
        ### TODO test that the dataframe for the three graphs contains the expected
        # nodes and edges
        assert True