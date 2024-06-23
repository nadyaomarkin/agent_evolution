import random
import networkx as nx
import os
import json
import matplotlib.pyplot as plt
import set_parameters as params
from rubikkubik import RubikCube

from pacman import Pacman
from nq_class import Network
from node_class import *
import set_parameters as params


class NQPlayer(Network):
    def __init__(self, game='rubikscube', **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.prepare_output_files()
        if self.game == 'rubikscube':
            self.cube = RubikCube()
            self.cube.apply_operations('xx')
        elif self.game == 'pacman':
            self.pacman = Pacman(rows=10, cols=10, star_num=10, boundary_mode='torus')

    # def prepare some output files by deleting the old ones. 
    def prepare_output_files(self):
        if os.path.exists('move.txt'):
            os.remove('move.txt')

    def evaluation(self):
        if self.game == 'rubikscube':
            cube_state = self.cube.state_string()
            solved_state = self.cube.solved_state_string()
            distance = sum([1 for i in range(8) if cube_state[i] != solved_state[i]])
            print(f"Distance from solved state: {distance}")
            return distance
        elif self.game == 'pacman':
            stars_collected = self.pacman.star_num - len(self.pacman.stars)
            print(f"Stars collected: {stars_collected}")
            # instead of stars_collected, return the distance from the solved state, so the number of stars to be collected
            # print(f"Stars remaining: {len(self.pacman.stars)}")
            return len(self.pacman.stars)
        

    def memory_adjustment(self, delta):
        self.memory = self.memory + delta
        self.network_upper_limit = self.memory #todo. make more refined memory allocation: use queue and wordlength. 


    def network_play_cube(self, steps):
        input_string = self.cube.state_to_binary()
        self.environment_input(input_string)

        gamefile = open('rk-evaluation-output.txt', 'w')
        cube_states = {self.cube.state_string(): 1}

        for _ in range(steps):
            state = self.cube.state_string()
            if state in cube_states:
                cube_states[state] += 1
            else:
                cube_states[state] = 1

            print('cube_states visited', cube_states, file=gamefile)

            if self.cube.is_solved():
                print('cube solved!!', file=gamefile)
                break

            self.run_evaluation(1)
            nw_output = self.nw_output_to_env(source= nw_output_tag, source_mode='queue')

            print('rkoutput1', nw_output, file=gamefile)
            print('got output from network oonn', nw_output, file=gamefile)

            self.cube.apply_binary_operations(nw_output)
            self.cube.apply_binary_operations(nw_output)

            new_state = self.cube.state
            print('new-state', new_state, file=gamefile)

            input_string = self.cube.state_to_binary()
            self.environment_input(input_string, destination='network')

        print('cube_states visited', cube_states, file=gamefile)
        gamefile.close()
        return self.evaluation()

    def network_play_pacman(self, steps):
        # assume initial position. 
        for _ in range(steps):
            # Get Pacman's state as a binary string
            pacman_state = self.pacman_state_to_binary()
            self.environment_input(pacman_state) # input from pacman-game to nq-network
            print('pacman state was sent to the nq-network', pacman_state, file = open('move.txt', 'a'))

            # Run network evaluation
            self.run_evaluation(1)

            # get the output from the queue computed by the network
            nw_output = self.nw_output_to_env(source=nw_output_tag, source_mode='queue')

            # nw_output = self.nw_output_to_env(source=nw_output_tag, source_mode='network')
            # Decode the network's output to represent Pacman's move
            dxdy = self.binary_to_move(nw_output)
            # ratrat remove after testing, test a random dxdy move
            # dxdy = (random.randint(0, 1), random.randint(0, 1)) # ok. it works. 
            # debug: why is it always 0000? 

            # apply the move to the pacman
            self.pacman.move(dxdy[0], dxdy[1])
            # record the move in a 'move.txt' file
            print('pacman move', dxdy, file = open('move.txt', 'a'))
            print('from the nq-output', nw_output, file = open('move.txt', 'a'))
            self.pacman.visualize_grid()
        return self.evaluation()

    def network_play(self, steps):
        if self.game == 'rubikscube':
            return self.network_play_cube(steps)
        elif self.game == 'pacman':
            return self.network_play_pacman(steps)

    def pacman_state_to_binary(self):
        return self.pacman.state_to_binary()
    


    def binary_to_move(self, binary_string):
        # Assuming binary_string is a binary representation of dx and dy
        if binary_string == '':
            return (0, 0)
        move_int = int(binary_string, 2)
        dx = (move_int >> 1) & 1
        dy = move_int & 1
        return (dx, dy)

if __name__ == "__main__":
    import time
    start_time = time.time()

    # Initialize for Rubik's Cube
    player_rubik = NQPlayer(game='rubikscube', output_file='nqrk.txt')
    player_rubik.create_network(3)


    # Initialize for Pacman
    player_pacman = NQPlayer(game='pacman', output_file='nqrk.txt')
    player_pacman.create_network(3)
    for _ in range(2):
        player_pacman.add_vertex()

    # player_pacman.population[0].tag_value = '11111'  # Inputs from environment
    # player_pacman.population[1].tag_value = '00000'  # Outputs to the environment


    
    player_rubik.population[0].tag_value = env_tag  # Inputs from environment
    player_rubik.population[1].tag_value = nw_output_tag  # Outputs to the environment



    player_rubik.queue_to_file(filename='qonly.txt')

    # player_pacman.queue_update('20000000000000000000010111111111111111111112', Vertex())
    # player_pacman.environment_input(input_string='11111100000', destination='queue')
    # player_pacman.queue_to_file(filename='qonly.txt', nw_print=True)

    # change the pacman's position to a random position on the grid
    player_pacman.pacman.position = [random.randint(0, 9), random.randint(0, 9)]
    # send the environment's (pacman's) state to the network
    pacman_state = player_pacman.pacman_state_to_binary()
    # update the nq-network with the pacman's state as a q-node
    player_pacman.environment_input(pacman_state)

    # add a few q-nodes for activity. make them random valued
    for _ in range(20):
        qnode = Vertex()
        qnode.tag_value = ''.join([str(random.randint(0, 1)) for _ in range(10)])
        qnode.value = ''.join([str(random.randint(0, 1)) for _ in range(10)])
        player_pacman.queue_update(qnode.tag_value, qnode)


    player_pacman.network_play(200)

    player_pacman.evaluation()

    print('time eoeo', time.time() - start_time)
