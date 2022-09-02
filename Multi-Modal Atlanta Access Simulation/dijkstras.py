"""
This file handles the best route calculation for the respective transportation network. It also handles the reading of the network
data from the gml file. The global variables include the priority queue for the Dijkstra's algorithm, dictionaries that connect each
of the respective amenities (point or polygon) to their closest intersections for each network, and a dictionary that contains the
average speed limit for each road('highway') type. The file has three main functions, dijkstra which runs dijkstra's algo,
get_adjacent_nodes which retrieves the adjacent nodes given a node, and finally amenity_found which checks if the given
node(intersection) has the appropriate adjacent amenity.

"""
import time
import networkx as nx
import heapq as heap
from collections import defaultdict
import building_pointer_handler as build

global PRIORITY_QUEUE

PRIORITY_QUEUE = []
#road dict inilization
ROAD_POINT_AMENITY_DICT = build.make_point_amenity_dict_of_dict('r')
ROAD_POLY_AMENITY_DICT = build.make_poly_amenity_dict_of_dict('r')
#walk dict inilization
WALK_POINT_AMENITY_DICT = build.make_point_amenity_dict_of_dict('w')
WAlK_POLY_AMENITY_DICT = build.make_poly_amenity_dict_of_dict('w')
#bike dict inilization
BIKE_POINT_AMENITY_DICT = build.make_point_amenity_dict_of_dict('b')
BIKE_POLY_AMENITY_DICT = build.make_poly_amenity_dict_of_dict('b')
#Average Speed of road types in atlanta area
SPEED_DICT = {'residential': 25.634953897736796, 'tertiary': 34.12422839506173, 'secondary_link': 41.111111111111114, 'tertiary_link': 30.0, 'trunk_link': 30.0, 'motorway_link': 58.36134453781513, 'motorway': 60.460199004975124, 'secondary': 36.49489322191272, 'unclassified': 24.075949367088608, 'trunk': 39.379671150971596, 'primary': 38.09659090909091, 'primary_link': 31.0, 'disused': 30, 'living_street': 30}

"""
This function returns the network corresponding to the input type. The network is read
from a gml file into a networkx network, and then returned. The network
is a adjacency list of intersections to other intersections and the corresponding
connecting edges.

@args network kind
@return transportation network
"""
def read_network(kind):
    t0 = time.time()
    if kind == 'r':
        network_to_return = nx.read_gml("/Users/noahgans/Desktop/School/Honors/Semester 2 Work/All the Code and Shit/atlanta_road_network.gz", label='label', destringizer=None)
    elif kind == 'b':
        network_to_return = nx.read_gml("/Users/noahgans/Desktop/School/Honors/Semester 2 Work/All the Code and Shit/atlanta_bike_network.gz", label='label', destringizer=None)
    elif kind == 'w':
        network_to_return = nx.read_gml("/Users/noahgans/Desktop/School/Honors/Semester 2 Work/All the Code and Shit/atlanta_walk_network.gz", label='label', destringizer=None)
    else:
        print("Not Valid Network Type")
        return None
    t1 = time.time()
    print("Read time = ", end="")
    print(t1 -t0)
    print("Done with build")
    return network_to_return

 
"""
get_adjacent_nodes, given a node and a graph with kind, returns adjacent nodes
and dist to each adjacent node from the input node. First it goes through each adjacent node.
It then finds the shortest edge between the two nodes and appends the node and edge
length to a list and returns a list of all adjacent nodes and respective edges.
 
@args graph, node, kind of graph
@return adjacent nodes and respective edge lengths
"""
def get_adjacent_nodes(graph, node, kind):
    adjacent_nodes = []
    for adjacent_node in graph[node]:
        if adjacent_node in graph.keys():#running into error where node not in graph was added
            shortest_edge_to_node = float('inf')
            for edge in graph[node][adjacent_node]:
                edge_length_miles = graph[node][adjacent_node][edge]['length'] / 1609.34
                if kind == 'r':
                    if type(graph[node][adjacent_node][edge]['highway']) == list:
                        highway = graph[node][adjacent_node][edge]['highway'][0]
                    else:
                        highway = graph[node][adjacent_node][edge]['highway']
                    if edge_length_miles / SPEED_DICT[highway] < shortest_edge_to_node:
                        shortest_edge_to_node = edge_length_miles / SPEED_DICT[highway]
                elif kind == 'w' and edge_length_miles / 3.5 < shortest_edge_to_node: 
                    shortest_edge_to_node = edge_length_miles / 3.5 
                elif kind == 'b' and edge_length_miles / 10 < shortest_edge_to_node:
                    shortest_edge_to_node = edge_length_miles / 10
            if (adjacent_node not in graph.keys()):
                print(adjacent_node)
                print("adjacent node should always be in dict")
                input("wait")
            adjacent_nodes.append((adjacent_node, shortest_edge_to_node))
    return adjacent_nodes

"""
get_point_and_poly_data is a helper function that returns the appropriate
point_network_dict and poly_network_dict for the type of transportation
network.
 
@args network_kind
@return point_network_dict and poly_network_dict
"""
def get_point_and_poly_data(network_kind):
    if network_kind == 'r':
        point_network_dict = ROAD_POINT_AMENITY_DICT
        poly_network_dict = ROAD_POLY_AMENITY_DICT
    elif network_kind == 'w':
        point_network_dict = WALK_POINT_AMENITY_DICT
        poly_network_dict = WAlK_POLY_AMENITY_DICT
    elif network_kind == 'b':
        point_network_dict = BIKE_POINT_AMENITY_DICT
        poly_network_dict = BIKE_POLY_AMENITY_DICT
    else:
        print("Not valid pointer dict type")
    return point_network_dict, poly_network_dict

"""
Amenity_found checks whether the input node contains the searched for
adjacent amenity. If it does it returns done as true, the amenity name,
and the distance to the amenity from the intersection. First it retrieves
the point and poly dictionaries for the network type. Then it checks if
the node is in the point dict. If it is, it checks if the amenity is in the
dict associated with the node, and if so the amenity is found. The same logic
applies for the poly_amenity dict. If both fail to find the matching amenity
then done is returned false.
 
 
@args node, goal_amenity, network kind
 
@return done(amenity found), amenity name, distance from node to amenity
"""   
def amenity_found(node, input_amenity, network_kind):
    point_network_dict, poly_network_dict = get_point_and_poly_data(network_kind)
    done = False
    amenities = []
    distances = []
    amenity = None 
    if(node in point_network_dict):
        dict_of_amenities = point_network_dict[node]
        if (input_amenity in dict_of_amenities):
            amenity = dict_of_amenities[input_amenity][0]
            amenities.append(amenity)
            distances.append((amenity[-1] / 1600) / 3.5)
            done = True
    if(node in poly_network_dict):
        dict_of_amenities = poly_network_dict[node]
        if(input_amenity in dict_of_amenities):
            amenity = dict_of_amenities[input_amenity][0]
            amenities.append(amenity)
            distances.append((amenity[-1] / 1600) / 3.5)
            done = True
    return done, amenity, distances

"""
dijkstra runs dijkstra's algorithm for the given network G starting at startingNode and
returning once finding amenity_name. First it clears the priority_queue then pushes
the priority queue onto the heap with the starting node cost set to 0. Then it builds a
set of visited nodes, a parents pointer dict, and a node cost dict with every value
initially set to inf, so that when nodes are discovered their cost will be updated.
The cost of the starting node is set to 0, and then the function starts popping out a node
from the Priority Queue that has the lowest cost. It then checks if that node has the goal
amenity adjacent to it. If it does than it returns the parents pointer, the amenity,
the cheapest node id, and the total distance(which is time throughout this whole process).
If the goal amenity is not adjacent to the cheapest node, than the adjacent nodes to it
are iterated through. If the new cost to reach the adjacent node from the parent node
is cheaper then the value stored in the node_cost dict, then the value is reset. If the
value is reset then they need to be pushed to the priority queue with the lower values.
 
@args = G(network dict of dicts) goal amenity, kind of network
 
@return parents, amenity name, goal node id, time to get to amenity
"""
def dijkstra(G, startingNode, amenity_name, kind):
    PRIORITY_QUEUE.clear()
    heap.heappush(PRIORITY_QUEUE, (0, startingNode))
    parents = {}
    parents[startingNode] = None    
    node_cost = defaultdict(lambda: float('inf'))
    node_cost[startingNode] = 0
    while PRIORITY_QUEUE:
        cheapest_node = heap.heappop(PRIORITY_QUEUE)
        done, amenity, distance = amenity_found(int(cheapest_node[1]), amenity_name, kind)
        if done:
            PRIORITY_QUEUE.clear()
            return parents, amenity, cheapest_node[1], node_cost[cheapest_node[1]] + distance[0]
        for adj_node in get_adjacent_nodes(G, cheapest_node[1], kind):
                new_cost = node_cost[cheapest_node[1]] + adj_node[1]
                if new_cost < node_cost[adj_node[0]]:
                    parents[adj_node[0]] = cheapest_node[1]
                    node_cost[adj_node[0]] = new_cost
                    if adj_node[0] in G.keys():
                        heap.heappush(PRIORITY_QUEUE, (cheapest_node[0] + adj_node[1], adj_node[0]))


        

                

