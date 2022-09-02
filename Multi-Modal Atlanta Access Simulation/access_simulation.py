"""
This file is the driver for the whole program. The main function is accessability_simulation_for_amenity
which initializes all needed data structures, and then starts simulating the access time from homes to amenities
and records the time using the data_and_visulization file.
"""

from tqdm import tqdm
from numpy import inf
import census_data_handler as cd
import dijkstras as gp
import networkx as nx
import building_pointer_handler as build
import random
from data_and_visualization import Results_For_Amenity

AMENITIES = ['theatre', 'tutor', 'fuel', 'bank', 'public_bookcase', 'cafe;animal_shelter', 'gazebo', 'veterinary', 'financial_advice', 'vending_machine', 'dentist', 'vending_machine;waste_basket', 'taxi', 'social_center', 'public_building', 'fast_food', 'vehicle_inspection', 'food_court', 'shelter', 'courthouse', 'car_sharing', 'Dry Cleaner', 'hospital', 'social_facility', 'car_rental', 'planetarium', 'grave_yard', 'restaurant', 'arts_centre', 'toilets', 'cinema', 'fountain', 'bar', 'animal_shelter', 'pharmacy', 'studio', 'doctors', 'waste_basket', 'biergarten', 'police', 'parking_space', 'vacuum_cleaner', 'cafe', 'stripclub', 'bicycle_repair_station', 'animal_boarding', 'mailroom', 'college', 'car_wash', 'bicycle_parking', 'jobcentre', 'fire_station', 'clinic', 'dojo', 'auditorium', 'shower', 'bench', 'manhole', 'nursing_home', 'events_venue', 'post_office', 'bus_station', 'swimming_pool', 'letter_box', 'parking_entrance', 'clock', 'hospital:historical', 'bbq', 'disused', 'community_centre', 'university', 'driving_school', 'townhall', 'recycling', 'place_of_worship', 'smoking_area', 'nightclub', 'kindergarten', 'telephone', 'ice_cream', 'office', 'social_centre', 'childcare', 'language_school', 'parking', 'bureau_de_change', 'atm', 'prison', 'waste_disposal', 'conference_centre', 'Paint Supplies', 'pub', 'drinking_water', 'charging_station', 'library', 'waste_container', 'car_wash;fuel', 'waste_transfer_station', 'bench;waste_basket', 'school', 'marketplace', 'post_box', 'Recycle glass vases']

"""
get all networks returns the three network types converted into the form of a dictionary of dictionaries.
The three networks are initially returned as network x graphs from the dijkstra's file, and are then converted
and returned.

@ars none
@return road graph, walk graph, and bike graph --> dictionary of dictionarys 

"""
def get_all_networks():
        road_network = gp.read_network('r')
        walk_network = gp.read_network('w')
        bike_network = gp.read_network('b')
        road_graph = nx.to_dict_of_dicts(road_network, nodelist=None, edge_data=None)
        print("Done Reading Road Network")
        walk_graph = nx.to_dict_of_dicts(walk_network, nodelist=None, edge_data=None)
        print("Done Reading Walk Network")
        bike_graph = nx.to_dict_of_dicts(bike_network, nodelist=None, edge_data=None)
        print("Done Reading Bike Network")
        
        return road_graph, walk_graph, bike_graph


"""
get_demographic_data_for_home actually returns the demographic data for a census block from the
getter methods in census_data_handaler. Given a block_id the funtion returns he racial
education, income, and transportation data which are all lists of percents.
 
@args bloc_id

@return racial_data, edu_data, household_income, transportation_data
"""
def get_demographic_data_for_home(block_id):
        racial_data = cd.get_race_data(block_id)
        edu_data = cd.get_education_data(block_id)
        household_income = cd.get_household_income_data(block_id)
        transportation_data = cd.get_transportation_data(block_id)
        return racial_data, edu_data, household_income, transportation_data


"""
assign_person selects a race, education attainment, household income, and method of transport for
a given set of demographic data inputs. It selects the attributes based off of the percentages
included in the data lists, and uses functions from the census data handaler to retrieve the assignments.
All four assignments are returned as ints that represent indexes to the respective lists.
 

@args all four data types
@return attribute assignments for the four types of demographic data types. 
"""
def assign_person(demographic_data, edu_data, household_income, transportation_data):
        race = cd.prob_race(demographic_data)
        edu = cd.prob_education(edu_data)
        wealth = household_income
        network_type = cd.method_of_transport(transportation_data)
        return race, edu, wealth, network_type

"""

run dijstras passes the home, graph, kind of grah, and goal amenity into
the dijkstra's function from the dijkstra's file. The function returns the
values returned from the dijkstra's function, and if for some reason this function
fails, it returns an inf distance indicating a fail.
 

@args home(start node), graph (dict of dicts), kind of graph(r,w,b), amenity goal name
@return  parents(dict's pointing to parennts), amenity name, goal_node, time to amenity
"""
def run_dijkstras(home, graph, kind, amenity_name):
        distace = inf
        parents, amenity, goal_node, distace = gp.dijkstra(graph, str(home[1]), amenity_name, kind)
        return parents, amenity, goal_node, distace


"""
This function gets the home that falls within the studied census tracts. It fails when home is outside included census tracts
which means it's on the perimeter of the bounding box. Occurs 3-5% of homes selected for homes barley close
to atlanta. It keeps random indexing the home list until it finds a valed home, and returns the census block
the home falls in and its information.
 

@args homes list of all homes
@return block id the home was in and home information
"""
def find_valid_home(homes):
    home_found = False
    while(not home_found):    
            i = random.randint(0, len(homes) - 1)
            home = homes[i]
            #put cords of the home into get_census_tract
            block_id = cd.get_census_tract(home[0][0], home[0][1])
            if(block_id != None):
                return block_id, home
    

"""
accessability_simulation_for_amenity is the driver for the entire program. It funtions in three steps.
   1.) Initialize city
   2.) Calculate time to get from home to amenity for input home sample iterations
   3.) Show Data (mostly handled by data_and_visulization)
 
1.)
In the first stage of this process the function builds the fist builds the homes. It does this by
using the read_homes() method from the building_pointer_handaler which returns a list of all the homes
and their respective spatial data. Next the function reads all the networks from the and saves them as
dictionaries of dictionaries. Finally it creates an instance of the Results_For_Amenity class from the
data_and_visulization file which will handle the storing of collected data. This process takes a while
because reading the network's files is not fast. Roughly 11 secs for the road and >30 for the other two.
Print statements show read time and inform the user of progress.
 
2.)
After building the city of atlanta, the function starts to sample homes and calculate
their access time to the given amenity. First the program choses a random home, then
it gathers the demographic data for the census block of that home, after that, it assigns
the attributes for that home through probability, and finally, using the network type
that the person who's travel is being simulated, the distance(time) to the amenity is found.
This means that the travel time simulation is multi-modal and accounts for the three transportation
networks. The network type is used to select which network is used to calculate the travel time.
Sometimes the time to travel calculation fails which happens when the network bounding box does not
include the node pointed to by the home. In this case an error is recorded, and the error percent is
printed at the end. If there is no error, the relevant data is passed to the Results_For_Amenity
instance called amenity_data_handaler and saved for presentation there.
 
3.)
After all input sample iterations have been completed (default = 1000), the program outputs
some of the possible results with amenity_data_handaler instance.
 
 


@args desired home samples (default = 1000) & desired amenity to caculate access to (dafult = 'financial_advice')
@return none

"""
def accessibility_simulation_for_amenity(home_iterations = 1000, amenity_name = 'financial_advice'):
        print("Building Homes")
        homes = build.read_homes()
        print("Homes built")
        print("Reading Networks")
        road_graph, walk_graph, bike_graph = get_all_networks()
        amenity_data_handaler = Results_For_Amenity(amenity_name)
        error_count = 0
        print("====== Starting to simulate movement from homes to the " + amenity_name + " amenity ======")
        for i in tqdm(range(home_iterations)):        
            block_id, home = find_valid_home(homes)
            racial_data, edu_data, poverty_data, transportation_data = get_demographic_data_for_home(block_id)
            race, edu, wealth, network_type = assign_person(racial_data, edu_data, poverty_data, transportation_data)
            try:
                if(network_type == 0):
                        parents, amenity, goal_node, distace = run_dijkstras(home, road_graph, 'r', amenity_name)
                        dist_to_node = (float(home[4]) /1609.34) / 3.5 #distance from home to intersecion divided by walk rate
                elif(network_type == 1):
                        parents, amenity, goal_node, distace = run_dijkstras(home, walk_graph, 'w', amenity_name)
                        dist_to_node = (float(home[5]) /1609.34) / 3.5  #distance from home to intersecion divided by walk rate
                else:
                        parents, amenity, goal_node, distace = run_dijkstras(home, bike_graph, 'b', amenity_name)
                        dist_to_node = (float(home[6]) /1609.34) / 3.5  #distance from home to intersecion divided by walk rate
                total_time = dist_to_node + distace
                amenity_data_handaler.add_data(race, edu, wealth, network_type, total_time)
            except Exception as e:
                error_count += 1
        print("Errors percentage : " + str(1 / home_iterations))
        amenity_data_handaler.multi_plot()
        
        
                    
                        

            


if __name__ == "__main__":
        ready = 'n'
        while(ready == 'n'):
            iteration = int(input("Enter Number of iterations/samples   "))
            for amenity in AMENITIES:
                print(amenity)
            print()
            amenity = input("Enter amenity from amenity list    ")
            print("You've selected " + str(iteration) + " iterations for " + amenity + " amenity")
            ready = input("Ready to run simulation y/n  ")
        accessibility_simulation_for_amenity(iteration, amenity)
        