# from vertex_class import *
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



class Network: 
    def __init__(self, 
                 network_input_alphabet = input_alphabet, 
                 network_output_alphabet = output_alphabet, 
                 network_state_alphabet = state_alphabet,
                 network_action_alphabet = action_alphabet,
                 network_tag_alphabet = binary_alphabet,
                 output_file = 'queue.txt',
                                             # skew parameters
 ):
        
        self.population = []  # this will keep track of the vertices in the network
        # this will keep track of the number of vertices added and deleted
        self.network_input_alphabet = network_input_alphabet
        self.network_output_alphabet = network_output_alphabet
        self.network_state_alphabet = network_state_alphabet
        self.network_action_alphabet = network_action_alphabet
        self.network_tag_alphabet = network_tag_alphabet
            

        # queue is an importatnt parameter. we will include in the queue messages with vertex-tags and outputs
        # queue will be a dictionary of the form {vertex_destination_tag: output_values}
        # in case more than one output value is sent to the same tag, 
        # the values will be appended to the list of values, so output_values should be a list.

        self.queue = {}

        self.output_file = output_file
        # if it exists, remove the previous queue.txt file

        # if os.path.exists('queue.txt'):
        #     os.remove('queue.txt')
        self.prepare_output_file()
 

    # prepare a blank output file by removing the prev one. 
    def prepare_output_file(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        return
    

    # evaluate the network     
    def evaluation(self):
        # node that outputs to the environment will have a tag value of '00000'
        # search the queue for the output with destination tag '00000'
        # if it exists, return the output value
        for tag in self.queue:
            if tag == '00000':
                print('eoeo env output found', self.queue[tag])
                return self.queue[tag]
            
    # methods that take input from the environment and read output for the environment

    # input from the environment will be tagged with '11111'
    def environment_input(self, input_string):
        # first create a q-node that will contain input_string as its input and output value
       # todo (instead of referring to them as input vs output, just say value. )
        # qnodes value will be processed by vertex. 
        # we will use the tag '11111' for inputs from the environment
        q_node = Vertex() # all the attributes will be default. 
        q_node.input = input_string
        q_node.output_value = input_string
        self.queue_update('11111', q_node)
        return
    

    # network's output to the environment.
    # read the output value of the designated envorinment node
    # the two modes are 'queue' and 'tag'
    # when it's 'queue', we scan the queue for message with destination tag = source
    # when it's 'tag', we scan the population for the node with tag = source, and read its output value. or state value - to be decided
    def nw_output_to_env(self, source = '00000', source_mode = 'queue'):

        if source_mode == 'queue':
            # search the queue for the output with destination tag '00000'
            # if it exists, return the output value
            for tag in self.queue:
                if tag == source:
                    print('eoeo output for env found', self.queue[tag])
                    # use the first output value in the list and pop the queue of that value
                    output_value = self.queue[tag][0]
                    print('eoeo env tag has entries', self.queue[tag])

                    self.queue_pop(source, output_value)
                    # typechecking for binary string for output

                else:
                    return None
                
        elif source_mode == 'tag':
            #the source gives the node whose output we want to read
            for vertex in self.population:
                if vertex.tag_value == source:

                    return vertex.output_value
                # try instead the state of the output value
                    # return vertex.state

        return False
        


        
        

    

    # create vertices for the network                 
    def create_network(self, number_of_vertices):
        for _ in range(number_of_vertices):
            # remove stuff that's in the method below now. 

            # self.add_vertex() # this creates vertex and edges  # previously using add_vertex was responsible for edge accumulation at the head-end of
            self.create_vertex()  # this creates vertex but no edges. it logs fsm
        


    def create_vertex(self):
        state_value = self.network_state_alphabet[0]  
        # make a word of length 5 on the state alphabet
        state_value = ''.join(random.choices(self.network_state_alphabet, k=5))
        tag_value = ''.join(random.choices(self.network_tag_alphabet, k=5))
        # tag_value = '10000'

        action_value = random.choice(self.network_action_alphabet)  #!!!-!!! 
        action_value = '1'
        output_value = ''

        # set the rule-seeds
        # each rule can be a random string of size rrll on data_arithmetic_alphabet = ['r','l','t','a','d','i','p','c']
        rrll = 5 # rule-length
        output_rule = ''.join(random.choices(data_arithmetic_alphabet, k=rrll))
        state_rule = ''.join(random.choices(data_arithmetic_alphabet, k=rrll))
        action_rule = ''.join(random.choices(data_arithmetic_alphabet, k=rrll))
        rule_rule = ''.join(random.choices(data_arithmetic_alphabet, k=rrll))
        # create a new vertex


        new_vertex = Vertex(state_value = state_value, output_value = output_value, vertex_action = action_value, tag_value = tag_value,
                           vertex_input_alphabet = self.network_input_alphabet,
                            vertex_output_alphabet = self.network_output_alphabet,
                            vertex_action_alphabet=self.network_action_alphabet,
                            # pass the rule-seeds. recall the rules in the node class are generated from the seeds.
                            vertex_state_seed=state_rule, vertex_output_seed=output_rule, 
                            vertex_action_seed=action_rule, vertex_rule_seed=rule_rule,
                            father_network=None)
                            
        self.population.append(new_vertex)  # todo1. pop stays same when doing reseeding. 
        # create outgoing connections for the new vertex
        
        # log the addition by incrementing the vertex added count
        return new_vertex
    
    # next method will add a node to the network
    

    # now rewrite create vertex method, making all random values set to respective values of 010101 for testing 

    def create_vertex_fixed_vals(self):
        return 
    
        state_value = '01010'  
        tag_value = '01010'
        action_value = '1'
        output_value = ''
        rrll = 5 # rule-length
        output_rule = 'rrllr'
        state_rule = 'rrllr'
        action_rule = 'rrllr'
        rule_rule = 'rrllr'
        new_vertex = Vertex(state_value = state_value, output_value = output_value, vertex_action = action_value, tag_value = tag_value,
                           vertex_input_alphabet = self.network_input_alphabet,
                            vertex_output_alphabet = self.network_output_alphabet,
                            vertex_action_alphabet=self.network_action_alphabet,
                            # pass the rule-seeds. recall the rules in the node class are generated from the seeds.
                            vertex_state_seed=state_rule, vertex_output_seed=output_rule, vertex_action_seed=action_rule, vertex_rule_seed=rule_rule,
                            father_network=None)
        self.population.append(new_vertex)  # todo1. pop stays same when doing reseeding.
        return new_vertex



















    def add_vertex(self):
        new_vertex = self.create_vertex()
        return new_vertex


    # next method for deleting a vertex from the network
        
    # next we write a method for adding a particular vertex to the graph. similar to the method above, only with tha vertex parameter. 
        


    def delete_this_vertex(self, vertex, mode = 'hard_delete'):
        # check the vertex is in the population
        if vertex not in self.population:
            return
        # remove the vertex from network

        # if the vertex has envirjjonment tag, which for now is '11111', don't delete it.
        if vertex.tag_value == '11111': # tag for inputs from the environment
            return
        
        # similarly we have a tag for outputs to the environment
        if vertex.tag_value == '00000': # tag for outputs to the environment
            return
        
        self.population.remove(vertex)

    

    # method to add vertices to the network. 


    # next we define an edge-move method. move an edge 1-hop forward. this will take an edge, and point it toward a 1-hop neighbour of the sink vertex.
    
    # method to delete a random vertex from the network
    


# we write a queue based version of vertex_acts.
    

# we run a queue based evaluation now. the method below is an alternative to the method above. 
        
    # method for searching the queue for a tag value
    def queue_search(self, vertex_tag):
        match_length = 1
        kk = match_length
        for tag in self.queue:
            if tag == vertex_tag:
                return self.queue[tag]
            # loosen the match criterion to first kk characters
            elif tag[:kk] == vertex_tag[:kk]:
                return self.queue[tag]
        
        return False
        
# each node will check if it is in exectuion mode. 
        # if it is, itwill search the queue for the tag_value that matches its own tag_value.   
        # it will then use the queues output_value at the corresponding tag to use as nodes input
        # then it will process the input and put the corresponding output into the queue with a new tag value 

        # reminder: the rule-alphabet is ['r','l','t','a','d','i','p','c']

    def queue_node_evaluation(self, vertex = None):
        # search the queue 
        if vertex.ready == False:
            print('notready')
            # skip the vertex
            return
        vertex_tag = vertex.tag_value

        # will rewrite: instead of input_value we now want queue to be populated with q-nodes. 

        input_value = self.queue_search(vertex_tag)        # this is a list of values sent to vertex_tag



        if input_value == False or len(input_value) == 0:
            # the vertex is not in the queue
            return
       #                                 set the input as the first element of the list
        


        input_q_node = input_value[0] # input_value is now a list of q-nodes. 


        # remove the value from the queue
        self.queue_pop(vertex_tag, input_value)

        # now we have joint action. vertex, input_q_node --> vertex', output_q_node
        # for now use identity. 
        output_q_node = input_q_node
        new_vertex = vertex 
        # update the vertex to vertex' by substituting vertex' in the population
        self.population[self.population.index(vertex)] = new_vertex
        #update the queue
        new_tag = vertex.tag_value
        self.queue_update(new_tag, output_q_node)

        vertex.update_node()


        




# we write a queue based version of vertex_acts.

    def vertex_acts_queue(self, vertex):
        # we will rewrite the vertex_acts method to use the queue
        # first let's put the structure in. we go throug all the vertex-action values, and put a pass for now
        # then we will write the queue based version of the method.

    
        if vertex.action == None:
            return
        if vertex.action == '':
            return

        action_int = int(vertex.action)
        print('xxxva vertex action', vertex.action, 'from dictionary', action_dict)
        if action_int == action_dict['do_nothing']:
            return
        if not vertex_policy:
            return
        if action_int == action_dict['add_vertex']:
            if len(self.population) > network_upper_limit:
                for _ in range(1):
                    self.delete_vertex()
                    if verbose_action:
                        print('deleting a random vertex, verbose_action', verbose_action)
            else:
                self.add_vertex()
                if verbose_action:
                    print('adding a vertex, verbose_action', verbose_action)

        if action_int == action_dict['delete_vertex']:
            # delete instead of update
            # if not empty
            if len(self.population) > 5:
                self.delete_this_vertex(vertex)
        # update seeds
        if action_int == action_dict['update_seed']:
            #change all the seeds and data_dictionary_rules by applying a random rule
            random_rule = random.choice(data_arithmetic_alphabet)
            vertex.update_seed(data_arithmetic_rule = random_rule)
            # the method above chages rules for action, state and output.

        # adding a random vertex to the nw
        if action_int == action_dict['add_vertex']:
            self.add_vertex()






    def queue_network_evaluation(self, mode = 'synchronous', evaluation_order = 'sequential'):
        for vertex in self.population:
            self.queue_node_evaluation(vertex)
                    # let the vertex act on the graph given its action value 
            # self.vertex_acts(vertex)  # N.x based on vertex action. 


            
    # method to make a list of all distinct output values in the queue
    def queue_output_values(self):
        output_values = []
        for tag in self.queue:
            for value in self.queue[tag]:
                if value not in output_values:
                    output_values.append(value)

        # now each output values is a q-node. we need to extract its output value
        string_output_values = []
        for q_node in output_values:
            string_output_values.append(q_node.output_value)

        return string_output_values

    
    # rewrite this method keeping in mind that queue's tags have qnodes attached to them, not strings. 
    
    
    

    def queue_pop(self, vertex_tag, output_value='', pop_all = False):
        print('queue before popping vertex_tag', vertex_tag, 'output_value', output_value, 'pop_all', pop_all, 'queue \n', self.queue)
        # simple pop, without considering the input value, just pop the first value indexed by tag
        for tag in self.queue:
            if tag == vertex_tag:
                self.queue[tag].pop(0)
                # if the tag now has an empty list, remove the tag from the queue
                if len(self.queue[tag]) == 0:
                    del self.queue[tag]
                print('queue after popping vertex_tag', vertex_tag, 'output_value', output_value, 'pop_all', pop_all, 'queue \n', self.queue)
                return 

    # this is the Q push method
    def queue_update(self, new_destination_tag, q_node):
        max_length = 10
        if new_destination_tag in self.queue:
            # check that the list is nolonger than 5 elementsthen append
            if len(self.queue[new_destination_tag]) < max_length:
                self.queue[new_destination_tag].append(q_node)
            else:
                pass
        else:
            self.queue[new_destination_tag] = [q_node]
        return
    def instructions(self):
        instructions = []
        for vertex in self.population:
            instructions.append({
                                 'tag': vertex.tag_value,
 
                                #  'state-receive-mode': vertex.state_receive_mode,
 
                                 'rule_tag': vertex.data_arithmetic_rule_tag,
                                 'rule_output': vertex.data_arithmetic_rule_output, 
                                 'rule_state': vertex.data_arithmetic_rule_state,
                                 'rule_action': vertex.data_arithmetic_rule_action,
                                 'rule_rule': vertex.data_arithmetic_rule_rule,

                                    'state': vertex.state,

                                   })
        return instructions
    def queue_to_file(self, filename = ''):
        if filename == '':
            filename = self.output_file
        # append queue to an external file for later visualization
        # print queue to file
        # we want to add each printed queue to the file, so that we can display the queue updates in a separated method
        with open(filename, 'a') as file:
            file.write('\n queue \n')
            # file.write(json.dumps(self.queue))
            file.write('\n')
            # for each entry in queue, i want a separate line with that entry
            for tag in self.queue:
                # file.write(tag + ' : ' + str(self.queue[tag]) + '\n')
                # currently the queue has {tag:[q-nodes]}, we need to make a string of output_values from each q-node
                output_values = []
                for q_node in self.queue[tag]:
                    # check type: 
                    if type(q_node) == Vertex:
                        output_values.append(q_node.output_value)
                    else:
                        output_values.append('unknown type')
                file.write(tag + ' : vv ' + str(output_values) + '\n')



            file.write('--------------------\n')

            file.close()
            # print the queue to the console

        # additionally print all the distint output values, using existing method
        output_values = self.queue_output_values()
        with open(filename, 'a') as file:
            file.write('output_values ----------------------')
            file.write(json.dumps(output_values))
            file.write('--------------------\n')
            file.close()

        # now we want to also display network's node values e.g 
        for vv in self.population:
    # print state,output tag attributes of each vertex
    # tag values is coming up emputy because the tag value is not set in the vertex class
            print('state', vv.state, 'output', vv.output_value, 'tag', vv.tag_value, 'ready', vv.ready) 
        # let's put that into the same file
        with open(filename, 'a') as file:
            file.write('populationNN')

            # file.write(json.dumps(self.instructions()))

            # now for each entry in the NN.instructions() i want to print it to a separate line

            for instruction in self.instructions():
                file.write('\n')
                file.write(json.dumps(instruction))
            file.write('\n')
            file.write('--------------------\n')
            file.close()
  

                              
    # write a queue -based evaluation method
    def run_evaluation(self, number_of_evaluations = 10, mode = 'synchronous', evaluation_order = 'sequential'):
        for ii in range(number_of_evaluations):
            print('running evaluation')
            self.queue_network_evaluation(mode = mode, evaluation_order = evaluation_order)
            # display queue
            print('queue', self.queue)


            self.queue_to_file(self.output_file)


            # print the instruction set
            self.instructions()
        return self
 
   # number_of_evaluations = number of network-timesteps
 


########### end class Network defs #########



def queue_row_display(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            print(line)
            print('---------------------')

# queue_row_display('queue.txt')            


    

# pop the first tag


# test the methods environment_input and nw_output_to_env
# create a network
NN = Network()
NN.create_network(10)
# set the first two vertices to be from-env node, and to-env
NN.population[0].tag_value = '11111'
NN.population[1].tag_value = '00000'

# test the environment_input method
NN.environment_input('10101')
# artificially set the to-env node to contain a value
# test the nw_output_to_env method
NN.population[1].output_value = '10101'
print('output to env', NN.nw_output_to_env(source = '00000', source_mode = 'tag'))  # should be '10101'



# updated the queue to contain q-nodes. these are just like network nodes. 
# when an n-node (network node from population) is matched up with q-node, they will mutually change each other 
# and update the queue with the new q-node and the network population with the new n-node.

# test the changes

NN = Network()
NN.create_network(10)
NN.output_file = 'queue.txt'
# create a node for the queue. 

rrll=5
output_rule = ''.join(random.choices(data_arithmetic_alphabet, k=rrll))
rule_rule = ''.join(random.choices(data_arithmetic_alphabet, k=rrll))
state_rule = ''
action_rule = ''
q_node = Vertex(state_value = '10101', 
                output_value = '10101', vertex_action = '1', tag_value = '00000',
                # seeds are rules
                vertex_tag_seed = 'rt', #tag*
                vertex_output_seed =  output_rule, #val*
                vertex_rule_seed = 't' #tag** , val**. 
)

# add the q-node to the queue
NN.queue_update('00000',  q_node)
# evaluate network
# NN.queue_to_file()
NN.run_evaluation(10)

