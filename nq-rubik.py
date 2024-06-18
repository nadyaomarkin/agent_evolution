from nq_class import Network

# from nq_class_qnodes import Network


from node_class import *

import networkx as nx
import os

import json
import matplotlib.pyplot as plt
import networkx as nx

                
# removed testing. check previous commits. 
import set_parameters as params
if True:

    # set the biggest seed to work around inaccurate seeding if neeeded
    # calculate the largest seed, if the biggest alphabet in use is of size bbaass

    action_dict = params.action_dict
    

    vertex_policy = params.vertex_policy
    total_number_of_trials = params.total_number_of_trials
    evaluation_runs = params.evaluation_runs
    network_timesteps = params.network_timesteps

    network_size = params.network_size

    state_alphabet = params.state_alphabet
    binary_alphabet = params.binary_alphabet    

    input_alphabet = params.input_alphabet
    output_alphabet = params.output_alphabet
    action_alphabet = params.action_alphabet

    evaluation_mode = params.evaluation_mode
    evaluation_order = params.evaluation_order

    list_of_networks = params.list_of_networks

    verbose_trials = params.verbose_trials
    margin = params.margin

    number_of_perturbations = params.number_of_perturbations
    pert_times = params.pert_times
    topology_action = params.topology_action

    # delete_skew = params.delete_skew
    do_nothing_skew = params.do_nothing_skew
    # skew = params.skew



# test the new queue network
    
# we define a simple shift program. that shifts the input, updating the queue. destination doesn't change, so just keeps shifting.
    
        
NN = Network(network_input_alphabet=binary_alphabet, 
             network_output_alphabet=binary_alphabet, 
             network_state_alphabet=binary_alphabet, 
             network_action_alphabet=binary_alphabet, 
             network_tag_alphabet=binary_alphabet)
NN = Network(output_file='nqrk.txt')
# create a network with 10 vertices
NN.create_network(2)
#print the population
# add entries to the queue, using the first vertexto create the first entry, i.e. destination tag and output




# now we create an environment node
# modify the first node to be an environment node by giving it a special tag value '11111'
NN.population[0].tag_value = '11111' # inputs from environment will go to this node
# outputs to the environment will come from this node
NN.population[1].tag_value = '00000' # outputs to the environment will come from this node
NN.population[1].input = '0111'
NN.population[1].output = '0111'



# we need to make sure these tags cannot be updated. 
# add a few random nodes to the network

for ii in range(10):
    NN.add_vertex()



# now that we have environment input output set up, let's have the network play rubik's cube.
# first create a rubik's cube object
from rubikkubik import RubikCube
from rubikkubik import *

cube = RubikCube()
# cube.apply_operations('xx')
# cube.apply_operations('yy')
cube.apply_operations('zz')

# feed the environment input to the network
input_string = cube.state_to_binary()
# create a node whose input and output values correspond to this input
NN.environment_input(input_string)

# note that the state of the rubik's cube is expressed as a list of 8 vertices.

# create an rk_evaluation_output.txt file for the printout messages directly in the evaluation below
# open the file for writing
# first make sure the gamefile is empty
gamefile = open('rk_evaluation_output.txt', 'w')

cube_state = {}
# the above dictionary will keep track of the states that the cube visits in the course of the game
# add the current state to dictionary
cube_state[cube.state_to_binary()] = 1

NN.population[1].output = '0111'

def network_play(steps):
    for ii in range(steps):
        NN.run_evaluation(1)
        # check the output of the network

        # let's look directly into the 'environment' node, not in the queue
        output = NN.nw_output_to_env(source = '00000', source_mode='tag')

        # extract the value
        output = output
        # for now, try a different way of applying output. rather than from the queue, let's read it directly from the output
        print('rkoutput1', output, file=gamefile)
        output1 = output 
        # check the length of the string output, and print it. also if it's not 24 print it
        if len(output) != 24:
            print('output lengthxx', len(output), file=gamefile)
        # print the state of the cube to the gamefile

        cube.apply_binary_operations(output)
        #if cube is solved, print and break

        if cube.is_solved():
            print('cube solved!!', file=gamefile)
            #print the states of the cube visited
            # add the final state to the dictionary
            if input in cube_state:
                cube_state[input] += 1
            else:
                cube_state[input] = 1
            print('cube_states visited', cube_state, file=gamefile)
            break

        # now we feed the new state of the cube back to the network as input, using the environment method

        # # for debugging make a random cube op
        # cube.apply_operations(random.choice(['x', 'y', 'z' ]))


        input = cube.state_to_binary()
        output2 = output
        print('rkoutput2', output, output1== output2, len(output), file=gamefile)

        # append the cube state to the dictionary
        if input in cube_state:
            cube_state[input] += 1
        else:
            cube_state[input] = 1

        
        NN.environment_input(input)

        print('cube state', cube.state, file=gamefile)
        if cube.is_solved():
            print('cube solved xx', file=gamefile)
            break
        # each output is enterpreted as a cube action, e.g.  x,y,z. so we convert the first 2 bits of the output to a cube action

        NN.evaluation()

network_play(100)
# write the cube_state to gamefile
    
print('cube_states visited', cube_state, file=gamefile)


''' x, y, z . xx yy zz '''
# print the queue to the console
    
# write a method for displaying the queue in a nicer way. {tag, output_values} 
#should be displayed with each tag being a row, and the values in a list
# we print it to a separate file called 'queue_rows_display.txt'

NN.evaluation()
