import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sympy as sympy
import string 

# importing the omega function implemented as a method in the Vertex class
#from omega_vertex_class import *


import random
import string
import random as nonpseudo_random

global_wordsize=3 
global_alphabet_size=2

class Vertex:
    def __init__(self, string_value='', salt=0, 
    true_random = False, 
                 truncate_length = global_wordsize, # Truncating the output
                 father_agent = None):
        self.salt=salt  # salt is a number
        self.true_random=true_random
        self.truncate_length = truncate_length
        self.vertex_alphabet = string.ascii_lowercase[:global_alphabet_size]
        # if string_value is not provided, generate a random string
        if string_value == '':
            self.string_value = ''.join(nonpseudo_random.choice(self.vertex_alphabet) for _ in range(5))
        self.string_value = string_value
        
        #todo: choices
        if true_random: 
            self.seed = self.generate_random_word()  #(non-pseudo) random: each new vertex has a new seed 
        self.seed = "apple"  #initialised to the same seed. so the rules are uniform for vertices. 
        
        self.salt = self.pseudo_random_from_string() #pseudorandom number to be used in character updates
        self.max_size = 5
        # self.alphabet = 26  # 26 letters in the English alphabet
        self.alphabet = 3  # 26 letters in the English alphabet
        #  
        self.father_agent=father_agent




    def update_salt(self):
        #self.salt +=1
        self.salt = self.pseudo_random_from_string() #assigns a new pseudorandom number to salt
    

    
    # added truncation to the update_string method
    def update_string(self, new_string_value):
        self.string_value = new_string_value
        # truncate the string value up to truncate_length
        self.string_value= self.string_value[:self.truncate_length] 
        #!! will play to see the discrepancy !!
# uncomment ^^ later !!! !
        self.update_salt()
    # todo is not working properly, the module must be seeded with the same seed to generate the same random word
    def generate_random_word(self, length=5):  
        import random as nonpseudo_random
        return ''.join(nonpseudo_random.choice(self.vertex_alphabet) for _ in range(length))

    # 1. creates a pseudorandom number from the state of the vertex: seed+ string_value + salt
    # 2. seeds the random module random 
    def pseudo_random_from_string(self):  
        combined_seed = self.seed + self.string_value +str(self.salt)
        #seeds the random module
        if not self.true_random:
            random.seed(combined_seed)
            return round(random.random()*1000000)
        else: 
            return round(random.random()*1000000)
    
    
    # 1. use vertices' seed+salt+string_value to seed the random module
    # 2. update string_value to a pseudorandom string
    def update_to_random(self, length=None, max_size=5):
        #seeds the random module and gives a combined seed to be used in random.choice
        combined_seed = self.pseudo_random_from_string() 
        import random as pseudorandom   #!!! check to move it outside the method

        pseudorandom.seed(combined_seed) 
        # generate a pseudorandom string
        if length is None:
            # use random length
            length = combined_seed % max_size
        new_string_val = ''.join(pseudorandom.choice(self.vertex_alphabet) for _ in range(length))
        self.update_string(new_string_val)
        return new_string_val



    #omega acts on a vertex by updating the string_value of a vertex. 
        # details: 
        # 1.salt ->  seed the random function ->  generate pseudorandom characters. 

        # 2. on salt modulo n -> decisions. 
                # salt is updated after each action.


    # updates the  -- string.value -- of the vertex -- 
    def omega(self): 
        # constants
        rule = "None applied"  # default value
        
        # Appending a letter: with probability 1/5
        if len(self.string_value) < self.max_size and self.salt % 5 == 0:
            new_char = chr(97 + self.salt % self.alphabet)  # Generates a random lowercase letter
            self.update_string(self.string_value+new_char)  #this will update salt too. todo make it an explicit call
            rule = "Appended a letter: " + new_char

        # Deleting a letter: with probability 1/3
        elif len(self.string_value) > 0 and self.salt % 3 == 0:
            self.update_string(self.string_value[:-1]) #will update salt            
            rule = "Deleted a letter"
        
        # Update a letter
        elif self.salt % 2 == 0:
            for i in range(len(self.string_value)):
                if self.salt % 2 == 0:
                    new_char = chr(97 + self.salt % self.alphabet)
                    self.update_string(self.string_value[:i] + new_char + self.string_value[i+1:] ) #updates salt also
                    rule = f"Updated a letter at position {i} to: {new_char}"
                    break  # Break after one update for demonstration purposes. Remove this to update all characters.
        else: 
            # replaces string_val to a random rhs
            self.update_to_random(5)
            rule = f"Generated a random rhs"

        self.update_salt()
        father_agent = self.father_agent
        father_network = father_agent.father_network
        father_network.network_rules_history.append([ father_agent.name ,rule])  #!!! debug this, it is empty

#
# 
        global_network_rules_history.append([ father_agent.name ,rule])
# !!!! fix this by defining network before modified agent, 
#         father_network.network_rules_history.append([ father_agent.name ,rule])
# for now use global variable
    
        return {"salt": self.salt, "seed": self.seed, "rule": rule, "updated string": self.string_value}
    



#todo - test the omega functioions generate_random_word and update_to_random


import random as nonpseudo_random

# end of omega_vertex_class.py

###
###
###
###
###
###
###
###
###
###
###
###
###
###
###




# Modifying the Agent class: vertex update rule uses omega 
#from ModifiedAgent_class import *

# ModifiedAgent class uses omega to update the output of the agent.
# importing the Vertex class

from omega_vertex_class import * #empty now.


class ModifiedAgent:
    def __init__(self,
            name='', 
            policy=None, 
            state_vertex=None, 
            output = None, type="", 
            use_omega=True, class_type="ModifiedAgent", 
            father_network = None):
        self.class_type = 'ModifiedAgent'
        self.name = name
        self.policy = policy
        self.rules = []
        self.connections = []

        agent_alphabet = string.ascii_lowercase[:global_wordsize]

        self.father_network = father_network
        # todo: !!! implement type: decision tree
        # type abcdefg 
        # type decision tree: if ab etc..

        self.state_vertex = Vertex(string_value = ''.join(random.choice(agent_alphabet) for _ in range(5)))
       

        self.subcomponents = []
        self.use_omega = use_omega
        self.type = type

        # setting the initial policy, state and output
        random_length = 5
        random_policy = ''.join(random.choice(string.ascii_lowercase) for _ in range(random_length))

        self.policy = Vertex(string_value=random_policy)   #todo !!! discuss policy options in terms of decisions

        
        self.output_vertex = Vertex(string_value = ''.join(random.choice(string.ascii_lowercase) for _ in range(random_length)))
        self.output = self.output_vertex.generate_random_word()  # Setting the initial output to a random string    

        #set the father_agent: 
        self.policy.father_agent = self
        self.output_vertex.father_agent = self
        self.state_vertex.father_agent = self


        #I want to clean up the code below so that the output is just a vertex, rather than a string.
        # step 1. identify the methods that use the output string.
        # these methods are: update_agent_node, connect, update_to_random, update_string 
  
    def disassociate(self):  
        pass  
    def connect(self, other_agent):
        self.connections.append(other_agent)
    
    # this method   uses omega to update the output of the agent.
    # function: add neighbours' outputs to the agent's state string, and then apply omega to the agent's state string.
    # the flow: update_agent_node calls omega, 
    # omega calls update_string 
    def update_agent_node(self, i=0):
    
        neighbours_string = ''.join([
            agent.output_vertex.string_value for agent in self.connections])

        
        new_string_value = self.state_vertex.string_value + neighbours_string # no truncation yet.

        #new_string_value = new_string_value+ policy.string_value todo: !!! implement and check.!!!

        # update the state
        self.state_vertex.string_value = new_string_value   # untruncated string value
        #!!! todo check truncation ----!!!
        self.state_vertex.omega()  # apply omega on the state_vertex
        #inside it calls update_string which truncates the string value

        # update the output 
        self.output_vertex.string_value = self.state_vertex.string_value # pass state to the output


# Displaying the modified Agent class
ModifiedAgent

#from agent_class import Agent  # If you want to use the original Agent class
# !!! uncomment the above and address all the differences. 
Agent = ModifiedAgent # for now we will only use ModifiedAgent to test omega. 


agent=ModifiedAgent()

# end of ModifiedAgent_class.py 



###
###
###
###
###
###
###
###
###
###
###
###
###
###

# this network now has the option to use either rules or omega for agents. 

#from                 network_class import    Network
# Modifying the Network class as per the given requirements

# this network now has the option to use either rules or omega for agents. 
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sympy as sympy

# from network_class import Network 
# from network_class import * #   ------------- empty now.

# with open('network_class.py', 'r') as file:
#     file_content = file.read()

# exec(file_content)
#from agent_class import Agent  # If you want to use the original Agent class



#from ModifiedAgent_class import *  # empty now. 

# this network now has the option to use either rules or omega for agents. 
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sympy as sympy

# to set the number of edges in the network, change the variable connectivity 



global_network_rules_history = [] #todo: !!! implement this in the network class. !!!
global_wordsize = 1
global_alphabet_size = 2

class Network:
    def __init__(self, use_omega=True, show_animation=False, network_rules_history = [],
                 gl_alphabet_size = 3,
                 gl_wordsize=3):
        
        global global_alphabet_size
        global global_wordsize
        global_alphabet_size = gl_alphabet_size # update global
        global_wordsize = gl_wordsize # update global
        print("global_alphabet_size", global_alphabet_size)
        global_wordsize = gl_wordsize

        self.graph = nx.DiGraph()
        self.random_agents = []
        self.population = []
        self.network_outputs = []
        self.network_states=[]
        
        self.network_states_history = []
        self.network_outputs_history = []

        self.network_rules_history = []

        self.show_animation_nw = show_animation

        self.use_omega = use_omega
        self.connectivity = 7  # number of edges per node in method create_network
        # to add !!! preferences for network decisions

    # methods in class: 
    def plot(self, show_edges=True):
        pass 
    def create(self,N):
        pass
    def make_a_connection(self, agent):
        pass
    def create_network(self, iteration):
        pass
    def evaluate_network(self, mode="non-random", network_runs=20, show_edges=True, show_animation=False):
        pass

    
    # the code below plots the graph for agents that do not use omega.
    # more specifically, it sets the color of the nodes to red if the output is 'a', and blue if the output is 'b'.
    def plot_normal(self, show_edges=True, show_animation=False, show_plot=True):
        colors = ['red' if agent.output == 'a' else 'blue' for agent in self.population]
        label_map = {agent: agent.name + str(agent.output) for agent in self.population}
        pos = nx.circular_layout(self.graph)
        plt.figure(figsize=(8, 8))
        nx.draw_networkx_nodes(self.graph, pos, node_color=colors, node_size=800)
        nx.draw_networkx_labels(self.graph, pos, labels=label_map, font_size=12)
        if show_edges:
            nx.draw_networkx_edges(self.graph, pos)
        plt.title("Agents' Graph")
        plt.axis('off')
        plt.show(block=False)



    # the code below plots the graph for agents that use omega.
  
    # the method plot_omega is used by the method plot, and not by the method evaluate_network.
    # the method plot_omega -> method plot -> method evaluate_network.
    # method update -> method evaluate_network.

    def plot_omega(self, show_edges=True, show_animation=False, show_plot=False):
        label_map = {agent: agent.name[-1] + str(agent.state_vertex.string_value) for agent in self.population}
        pos = nx.circular_layout(self.graph)
        plt.figure(figsize=(8, 8))
        nx.draw_networkx_nodes(self.graph, pos, node_size=800)
        nx.draw_networkx_labels(self.graph, pos, labels=label_map, font_size=20)
        if show_edges:
            nx.draw_networkx_edges(self.graph, pos)
        plt.title("Agents' Graph (using omega)")
        plt.axis('off')
        print("----------- plotting omega network --------------", show_plot)
        # #print the string values of the agents in the network
        #print([self.population[i].output[:10] for i in range(len(self.population)) ])
        
        if show_plot:    
            plt.show(block=False)
        else:
            plt.show(block=False)
            plt.pause(0.1)
#            plt.close()   ˙#!!! fix this plot and check the labels

    def plot_omega(self, show_edges=True, show_animation=False, show_plot=False):
        pass  # !!! fix this plot and check the labels



    # lets set the plot to plot_omega when necessary 
    def plot(self, show_edges=True, show_plot=False):
        if self.use_omega:
            self.plot_omega(show_edges=show_edges, show_plot=show_plot)
        else:
            self.plot_normal(show_edges=show_edges)
        #print(self.network_outputs)


    def create(self, N):
        self.create_network(N)

    def make_a_connection(self, agent):
        agent_to_connect = random.choice(self.population)
        agent_to_connect.connect(agent)
        self.graph.add_node(agent)
        self.graph.add_edge(agent_to_connect, agent)

    def create_network(self, iteration):
        policy = "policy"
        
        # Determine which Agent class to use based on use_omega
        AgentClass = ModifiedAgent if self.use_omega != "rules" else Agent
        AgentClass = ModifiedAgent if self.use_omega else Agent

        
        agent1 = AgentClass("RA1", policy, father_network=self)
        agent2 = AgentClass("RA2", policy, father_network=self)


        # todo: this sets it to the same value? 
        # agent3 = AgentClass("RA1", policy,.state_vertex = Vertex().generate_random_word(), output = Vertex().generate_random_word())
        
        
        agent3 = AgentClass("RA3", policy, father_network=self) 
        self.random_agents = [AgentClass("RA " + str(i + 4), policy, father_network=self) for i in range(iteration)]
        self.population = [agent1, agent2, agent3] + self.random_agents
        
        for random_agent in self.population:
            for _ in range(self.connectivity):
                self.make_a_connection(random_agent)

    # in evaluate network, the nodes are coloured based on their output. Color blue for output 'b' and red for output 'a'
    # if the output consists of more than one character, only the first character is considered for colouring.
    # to make more sophisticated colouring scheme, we could use a dictionary to map the output to a colour.
    # for example, we could have a numerical representation of the output and map it to a colour.

    def make_outputs(self):
        self.network_outputs = [agent.output_vertex.string_value for agent in self.population]
        print(self.network_outputs)
        self.network_outputs_history.append(self.network_outputs)
        return(self.network_outputs)

    def make_states(self):
        self.network_states = [agent.state_vertex.string_value for agent in self.population]
        print(self.network_states)
        self.network_states_history.append(self.network_states)
        return(self.network_states)
    
    def print_history(self, which = "outputs"):
        if which == "outputs":
            for i in range(len(self.network_outputs_history)):
                print(i, " : ", self.network_outputs_history[i])
        elif which == "states":
            for i in range(len(self.network_states_history)):
                print(i, " : ", self.network_states_history[i])
        


# !!! todo. why is the first agent not truncated? and why 
# !!! fix the animation. the update function is not getting the ax from the plot function.

    # update arguments explained: num is an iterator, used by the animation function.
    # mode is either random or non-random.
    # network_runs is the number of times the network is evaluated. 
    
    def update(self, num, ax=None, mode="non-random", 
               network_runs=4, show_edges=True, show_animation=False):
        if mode == "random":
            order_agents = random.sample(self.population, len(self.population))
        else: 
            order_agents = self.population

        for agent in order_agents:
            agent.update_agent_node() 

        self.make_outputs() 
        self.make_states()

        if ax:
            ax.clear()
            ax.text(0.05, 1.02, f"Iteration: {num}", transform=ax.transAxes)
            colors = ['red' if agent.state_vertex.string_value == 'a' else 'blue' for agent in self.population]
            label_map = {agent: str(agent.state_vertex.string_value[0:7]) for agent in self.population}
            pos = nx.circular_layout(self.graph)
            nx.draw_networkx_nodes(self.graph, pos, node_color=colors, node_size=30, ax=ax)
            nx.draw_networkx_labels(self.graph, pos, labels=label_map, font_size=12, ax=ax)
            if show_edges:
                nx.draw_networkx_edges(self.graph, pos, ax=ax)

    def evaluate_network(self, mode="non-random", network_runs=4, 
                         show_edges=True, show_animation=False):
        if show_animation:
            fig, ax = plt.subplots()

            def update_with_ax(num):
                self.update(num, ax=ax)

            ani = animation.FuncAnimation(fig, update_with_ax, 
                                          frames=range(network_runs), repeat=False)
            plt.show()
        else:
            for num in range(network_runs):
                self.update(num)
        
        self.network_outputs = [agent.state_vertex.string_value for agent in self.population]
        self.plot(show_edges=show_edges)  # 
        self.make_outputs()  
        self.make_states()  
        self.plot(show_edges=show_edges)  
# end of network_class.py

# Displaying the modified Network class


#todo agents have empty connections on their own!!!!

#print("-----------------", "ModifiedAgent class", "-----------------")
agent=ModifiedAgent()
print(agent.output, " agent.output", agent.policy.string_value, "agent's policy ", agent.state_vertex.string_value, "agents state")

# end of network_class.py -------------------------


# nw=Network(use_omega=True, show_animation=True)  # use_omega can be set to True or False
# nw.create(1)
# nw.plot(show_plot=True)

# #plot the network with omega, setting the variables to display plot
# nw.plot(show_plot=True, show_edges=True)
# nw.evaluate_network(show_animation=True, network_runs=10)
# print(nw.network_states_history)
# print(nw.network_outputs_history)


