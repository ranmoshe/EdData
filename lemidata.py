'''
Input: 
    - Dataframe. A row is user's activity in the course. Columns are different course metrics - categorized.
    - A list of Amenables (columns we can interfere with)
    - Goal name
Process:
    - Iterate on all 3-column combinations that have at least one Amenable, and don't include the Goal
    - Add Goal
    - Analyze with ic_graph
Output:
    - For each combo, log:
        - The relations that were found
        - Whether there is a causal relation from an Amenable to the Goal
Command line example:
    python lemidata.py lemidata.csv "bg_color,ttt" course_finished
'''
import itertools
import sys
import pandas as pd

from ic_graph import IC_Graph
from sample_set import SampleSet

def is_goal_influenced(ic_graph, directed_all, goal):
    influenced_columns = [t[2] for t in directed_all]
    return goal in influenced_columns

def get_influencer(t):
    if t[0] == t[2]:
        return t[1]
    return t[0]

def get_amenable_identified(ic_graph, directed_all, amenables_in_subset, goal):
    goal_direct_influencers = [get_influencer(t) for t in directed_all if t[2] == goal]
    amenables_identified = list(set(amenables_in_subset) & set(goal_direct_influencers))
    goal_indirect_influencers = [get_influencer(t) for t in directed_all if t[2] in goal_direct_influencers]
    amenables_identified += list(set(amenables_in_subset) & set(goal_indirect_influencers))
    return list(set(amenables_identified))

def print_combo_results(ic_graph, amenables_in_subset, goal):
    directed = [t for t in ic_graph.graph.edges.data('out') if t[2] is not None]
    directed_star = [t for t in ic_graph.graph.edges.data('out_star') if t[2] is not None]
    amenable_identified = []
    directed_all = directed + directed_star
    goal_influenced = is_goal_influenced(ic_graph, directed_all, goal)
    if goal_influenced:
        amenable_identified = get_amenable_identified(ic_graph, directed_all, amenables_in_subset, goal)

    print('===================================================')
    print(f'Columns: {ic_graph.graph.nodes}')
    print(f'Edges: {ic_graph.graph.edges}')
    print(f'Directed edges: {directed}')
    print(f'Star Directed edges: {directed_star}')
    if amenable_identified:
        print(f'Amenables Identified: {amenable_identified}')
    print('===================================================')

def main(df_file, amenables_string, goal):
    df = pd.read_csv(df_file)
    amenables = amenables_string.split(',')
    columns_wo_goal = [column for column in df.columns if column != goal]
    for subset in itertools.combinations(columns_wo_goal, 3):
        amenables_in_subset = list(set(subset) & set(amenables))
        if amenables_in_subset:  # the subset includes at least one amenable
            columns = list(subset) + [goal]
            sub_df = df[columns]
            ic_graph = IC_Graph(SampleSet(sub_df))
            ic_graph.build_graph()
            print_combo_results(ic_graph, amenables_in_subset, goal)


if __name__ == '__main__':
    df_file = sys.argv[1]
    amenables_string = sys.argv[2]
    goal = sys.argv[3]
    main(df_file, amenables_string, goal)

