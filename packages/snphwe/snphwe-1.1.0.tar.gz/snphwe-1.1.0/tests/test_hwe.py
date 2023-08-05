
import unittest

from snphwe import snphwe

class TestHWE(unittest.TestCase):
    def test_snphwe(self):
        ''' check snphwe gives expected p-values
        '''
        self.assertAlmostEqual(snphwe(500, 10, 5000), 0.65157189991)
        self.assertAlmostEqual(snphwe(1000, 20, 5000), 1.26598491e-5)
    
    def test_snphwe_odd_inputs(self):
        ''' check snphwe with odd inputs
        '''
        # should raise errors with odd inputs
        with self.assertRaises(ValueError):
            snphwe(0, 0, 0)
        with self.assertRaises(ValueError):
            snphwe(-5, 10, 1000)
    
    def test_snphwe_large_input(self):
        ''' check snphwe doesn't give errors with large sample sizes
        '''
        self.assertEqual(snphwe(200000, 200000, 200000), 0.0)
    
    def test_snphwe_uncertain_genotypes(self):
        ''' check uncertain genotypes give correct p-values
        
        Imputed genotypes need HWE checks too. I checked this against the method
        from:
        Shriner D. (2011) Genet Epidemiol. 35:632‐637. doi:10.1002/gepi.20612
        Approximate and exact tests of Hardy-Weinberg equilibrium using uncertain genotypes.
        
        Instead of running the full exact test from that, I simply round the
        genotype totals before calling the underlying c++ function. This should
        still be reasonably accurate and fast.
        '''
        self.assertAlmostEqual(snphwe(4989.99999, 494999.999, 9.9999999), 0.570223198305)
