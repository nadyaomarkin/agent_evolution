import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sympy as sympy
from concurrent.futures import ProcessPoolExecutor

import set_parameters as params
from nq_class import Network
from nq_class import *
from rubikkubik import RubikCube

from nqplayer_class_both import *

parallel_mode = True

# Helper function outside the Evolution class
def run_evaluation_wrapper(player, network_timesteps, evaluation_mode, evaluation_order):
    player.network_play(network_timesteps)
    return player

class Evolution:
    def __init__(self, number_of_trials=0, epoch=0, network_timesteps=0, network_size=0, params=params):
        self.number_of_trials = number_of_trials
        self.epoch = epoch
        self.network_timesteps = network_timesteps
        self.trials = []

        # Import all parameters from set_parameters.py
        self.params = params
        self.prepare_output_files()

    # Create networks for trials
    def prepare_output_files(self):
        if os.path.exists('memory.txt'):
            os.remove('memory.txt')
    def create_trials(self):
        trials = []
        for ii in range(self.number_of_trials):
            # for each player we define an output file, nqrk_ii.txt
            output_file_name = f'nqrk_{ii}.txt'
            player = NQPlayer(game = 'pacman', output_file=output_file_name)
            
            player.create_network(self.params.network_size)
            trials.append(player)
        self.trials = trials
        return trials

    def run_trials_parallel(self):
        # Prepare arguments for the helper function
        args = [(player, self.network_timesteps, self.params.evaluation_mode, self.params.evaluation_order) for player in self.trials]

        # Use ProcessPoolExecutor to execute run_evaluation in parallel
        with ProcessPoolExecutor() as executor:
            results = executor.map(run_evaluation_wrapper, *zip(*args))
            results = list(results)

        self.trials = results
        return self

    def run_trials(self, parallel_mode=parallel_mode):
        # evaluate each network network_timesteps times
        if parallel_mode:
            #args = [(player, self.network_timesteps, self.params.evaluation_mode, self.params.evaluation_order) for player in self.trials]
            self.run_trials_parallel()
        else:
            for player in self.trials:
                player.network_play(self.network_timesteps)

        # Evaluate each network
        # make a distance-list to be used for memory adjustment
        # evaluation gives 0 when there are 0 stars remaining. 
        distance_list = [player.evaluation() for player in self.trials]
        avg_distance = sum(distance_list) / len(distance_list)
        distance_from_avg = [ avg_distance - distance for distance in distance_list]
        # make a memory adjustment using distance_from_avg. will be adding memory with lower-than-avg scores (optimising for min)
        for ii, player in enumerate(self.trials):
            player.memory_adjustment(distance_from_avg[ii])
        
        print('memory lists', [player.memory for player in self.trials], file=open('memory.txt', 'a'))
        # print each players stars collected
        print('stars collected', [player.pacman.star_num - len(player.pacman.stars) for player in self.trials], file=open('memory.txt', 'a'))

        return self

if __name__ == '__main__':
    import time
    start_time = time.time()

    evolution = Evolution(number_of_trials=4, epoch=100, network_timesteps=10, network_size=10, params=params)
    evolution.create_trials()

    for ii in range(evolution.epoch):
        evolution.run_trials()

    print('parallel mode', parallel_mode, 'time eoeo', time.time() - start_time)
