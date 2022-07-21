'''
Simple classes for probabilistic triple and probabilistic knowledge base.
Implementation of probabilistc updating algorithm.
'''
import numpy as np
import csv

import configs

class ProbabilisticTriple:
    '''
    The class for probabilistic triple in the form of p::<subj, pred, obj>
        where p ~ Beta(a, b)
    '''
    def __init__(self, subj, pred, obj, mu=0.5, v=2):
        self.subj = subj
        self.pred = pred
        self.obj = obj
        self.beta_a = 0
        self.beta_b = 0
        
        # initialize beta_a and beta_b by mean and sample size
        self._calculate_beta_by_mu_v(mu, v)
        
    def __str__(self):
        return f'{self.prob}::({self.subj}, {self.pred}, {self.obj})'
    
    def __repr__(self):
        return self.__str__()
    
    def _calculate_beta_by_mu_v(self, mu, v):
        '''Compute and set a and b of beta distribution by mean and sample size'''
        self.beta_a = mu * v
        self.beta_b = (1 - mu) * v
        return self.beta_a, self.beta_b

    # def _update_beta_a_b(self, evds_stream):
    #     num_ones = list(evds_stream).count(1)
    #     num_zeros = list(evds_stream).count(0)
    #     self.beta_a += num_ones
    #     self.beta_b += num_zeros
    #     return self.beta_a, self.beta_b
    
    def Jeffrey_update(self, evd_proba):
        """
        Update the probability by Jeffrey's rule

        TODO: relax tuple independence assumption
        """ 
        pos_proba, neg_proba = evd_proba, 1 - evd_proba
        
        # assuming Beta-Binomial distribution
        new_prob = pos_proba * (self.beta_a+1)/(self.beta_a+self.beta_b+1) \
            + neg_proba * (self.beta_a+0)/(self.beta_a+self.beta_b+1) 
       
        # compute and set new probability mean and sample size
        return self._calculate_beta_by_mu_v(
            new_prob, self.beta_a+self.beta_b+1)
        
    @property
    def prob(self):
        return self.beta_a / (self.beta_a + self.beta_b)
    
    @property
    def sample_size(self):
        return self.beta_a + self.beta_b

    def to_list(self):
        '''Return all probabilistic triples in list'''
        return [self.subj, self.pred, self.obj, self.prob, self.sample_size]

    def to_array(self):
        '''Return all probabilistic triples in np.ndarray'''
        return np.array(self.to_list())


class ProabilisticKnowledgeBase:
    '''
    A simple Proabilistic Knowledge Base that stores probabilistic triples.
    '''
    def __init__(self):
        self.data = {}

    def __len__(self) -> int:
        return len(self.data)
        
    def get_triple(self, subj, pred, obj) -> ProbabilisticTriple:
        '''Get the probabilistic triple by its subject, predicate, object'''
        return self.data.get(f'<{subj}, {pred}, {obj}>')

    def add_triple(self, probtrp: ProbabilisticTriple, update_exist=True):
        '''
        Add a probabilistic triple into the PKB. If the proposition part <s, p, o> 
        already exists, and set update_exist=True, then the probabilistic updating 
        procedure will be called automatically.
        '''
        trp = self.get_triple(probtrp.subj, probtrp.pred, probtrp.obj)
        if trp:
            if update_exist:
                trp.Jeffrey_update(probtrp.prob)
            else:
                raise Exception(f'Triple {probtrp} already exist!')
        else:
            self.data.setdefault(f'<{probtrp.subj}, {probtrp.pred}, {probtrp.obj}>', probtrp)

    def load(self, pkb_dir=configs.PKB_DIR):
        '''Load a PKB from the disk file'''
        with open(pkb_dir, 'r') as f:
            for line in f:
                s, p, o, m, v = line.split()
                m, v = float(m), float(v)
                self.add_triple(ProbabilisticTriple(s, p, o, m, v))
        return self
    
    def save(self, pkb_dir=configs.PKB_DIR):
        '''Save the PKB to the disk file'''
        with open(pkb_dir, 'w') as f:
            for v in self.data.values():
                line = f'{v.subj}\t{v.pred}\t{v.obj}\t' + \
                        str(round(v.prob, 3)) + '\t' + str(round(v.beta_a+v.beta_b, 3))
                f.write(line + '\n')


# class DeterministicRule:
#     '''
#     TODO: h <- b_1, b_2, ..., b_n
#     '''
#     pass


# class NegativeConstraint:
#     '''
#     TODO: False <- b_1, b_2, ..., b_n
#     '''
#     pass


if __name__ == "__main__":
    kb = ProabilisticKnowledgeBase()
    kb.add_triple('h1', 'r1', 't1')
    kb.add_triple('h1', 'r2', 't2', 0.8, 20)
    
    kb.get_triple('t1', 'r1', 't1').Jeffrey_update(0.9)

    kb.save()
