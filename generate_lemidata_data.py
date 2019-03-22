import numpy as np
import pandas as pd
import random
import unittest

from ic_graph import IC_Graph
from sample_set import SampleSet
from utils import generate_random_a_b, generate_random_series

class TestGraph(unittest.TestCase):

    @staticmethod
    def course_finished(row):
        if row['initial_engagement'] == 'yes':
            choice = random.choices(
                    population=['yes', 'no'],
                    weights = [0.5, 0.5],
                    k = 1)[0]
        else:
            choice = random.choices(
                    population=['yes', 'no'],
                    weights = [0.1, 0.9],
                    k = 1)[0]

        return choice

    @staticmethod
    def initial_engagement(row):
        if row['gender'] == 'female':
            if row['bg_color'] == 'green':
                choice = random.choices(
                        population=['yes', 'no'],
                        weights = [0.8, 0.2],
                        k = 1)[0]
            else:
                choice = random.choices(
                        population=['yes', 'no'],
                        weights = [0.4, 0.6],
                        k = 1)[0]
        else:
            if row['bg_color'] == 'green':
                choice = random.choices(
                        population=['yes', 'no'],
                        weights = [0.4, 0.6],
                        k = 1)[0]
            else:
                choice = random.choices(
                        population=['yes', 'no'],
                        weights = [0.7, 0.3],
                        k = 1)[0]

        return choice

    def test_structure(self):
        '''
        '''
        df = generate_random_a_b(100000, [0.5], [0.5], a_name='gender', b_name='bg_color')
        df['gender'] = df['gender'].map({'gender_0': 'female', 'gender_1': 'male'})
        df['bg_color'] = df['bg_color'].map({'bg_color_0': 'red', 'bg_color_1': 'green'})
        df['initial_engagement'] = df.apply(lambda row: self.initial_engagement(row), axis=1)
        df['course_finished'] = df.apply(lambda row: self.course_finished(row), axis=1)
        ic_graph = IC_Graph(SampleSet(df))
        ic_graph.build_graph()
        directed = [t for t in ic_graph.graph.edges.data('out') if t[2] is not None]
        directed_star = [t for t in ic_graph.graph.edges.data('out_star') if t[2] is not None]
        df.to_csv('lemidata.csv', index=False)


                
if __name__ == '__main__':
    unittest.main()

