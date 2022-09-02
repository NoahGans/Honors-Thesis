# Project Title

Atlanta Probabilistic Citizen Demographic Assignment and Multi-Modal Access Simulation

## Authors

@ Noah Gans

## 🔗 Links

LinkedIn = https://www.linkedin.com/in/noah-gans-9536811a1/
Github - https://github.com/NoahGans
Honors Paper = https://digitalcommons.bowdoin.edu/honorsprojects/385/

##Example



## Dependencies

https://pypi.org/project/pyshp/
https://pypi.org/project/tqdm/ 
https://networkx.org/documentation/stable/install.html
https://pypi.org/project/Shapely/
https://matplotlib.org/stable/users/installing/index.html

## Environment Variables

All imports should be included in py files, and dependent data files are included.

## Running instructions

    Import all dependent libraries, navigate to appropriate directory, then use command:

    $ python3 access_simulation.py
    
    Follow directions, and make the final figure fullscreen for optimal viewing

##Description

This program calculates the travel access time to amenities in Atlanta along road, walk, and bike networks. The data used to 
represent Atlanta was retrieved from Open Street Maps using QGIS’s Quick OSM publicly available tool. This was one of two large 
programs run on the Atlanta data set I constructed. The other program partitioned the road network graph of Atlanta into subgraphs. 
My Honors Thesis describes the latter process and the implications on the social ecology of the city. Use the link above to read 
more about that process. The program given here however was not written up but allows for the calculation of access inequality for 
a given amenity for race, education attainment, and household income.
    
    At a high level, the program functions by initializing the city infrastructure, then sampling random homes, calculating the 
time required to reach the input amenity from the sampled home, and finally recording and displaying data. Initializing the 
city uses many of the functions from the Building_pointer_handler file to build pointer dictionaries from amenities to their 
closest intersection on all three travel networks. The same is done with all homes. After all infrastructure data has been read 
and organized into appropriate data structures, the program is ready to calculate access time.

    In order to calculate access time, the program first needs to know what network to use and therefore what person is being 
simulated. First a home is randomly selected from all homes in the city, and the census block it falls in is found. Next, the 
network is selected probabilistically  based on the percentages of the population in the respective census block that use the 
method of transport to commute to work. This same process is conducted to determine the person's race and education. The income 
of the person is assigned to the median household income of the census block. (See function descriptions for get_census_tract 
get_race_data get_education_data get_household_income_data get_transportation_data prob_race prob_education method_of_transport). 
    
    After the demographic variables have been assigned, the program calculates the time to reach the desired amenity by using 
dijkstra’s algorithm on the selected network. Dijkstra’s algorithm is used because it finds the solution to the shortest path 
from source to destination in an efficient nlg(n) time. The best route is calculated for the home to amenity, and the time taken 
to reach the amenity is returned to be stored.

    As the program samples homes and calculates the time needed to reach the amenity, the program saves this data to the 
Results_For_Amenity class. This class stores all racial, education, median household income, and transportation network data. 
After all the homes have been sampled, the program displays 6 graphs. The top three show the relationship between race, education 
attainment, and household income to access time. The bottom three show sample statistics from the process. Each shows what category 
of race, education attainment, and transportation network was selected at each iteration count. 

#Appendix 
Access_simulation
    get_all_networks
    get_demographic_data_for_homeAssign_person
    Run_dijkstras
    Find_valid_home
    Accessibility_simulation_for_amenity
    Assign_person
    Run_dijkstras
    Find_valid_home
    accessibility_simulation_for_amenity
Building_pointer_handler
    get_average_point_of_polygon
    make_point_amenity_dict_of_dict
    make_poly_amenity_dict_of_dict
    get_homes
    write_homes
    read_homes
    get_amenities
Census_data_handler.py
    read_acs_data
    write_demo_data_complete_to_new_file
    build_demograhic_data_ditionary
    get_census_tract
    get_race_data
    get_education_data
    get_household_income_data
    Get_transportation_data
    Prob_race
    Prob_education
    method_of_transport
Data_and_visualization.py
    Class Results_For_Amenity
Dikstras.py
    read_network
    get_adjacent_nodes
    get_point_and_poly_data
    amenity_found
    dijkstra
Demographic_data.csv
    Contains all demographic data for the Bounding Box
Homes.csv
    Contains all homes for bounding box
Block Groups
    Contains all block groups for bounding box
Pointer files
    Contains all needed pointer files.







