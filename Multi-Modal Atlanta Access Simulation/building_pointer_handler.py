
"""
This file contains functions that handle the infrastructure of atlanta. Many of them are not used
when the main function of the program is run. Most are Legacy functions that were used to create
efficient files that are now just read. The functions used for the access simulation are the
make_point_amenity_dict_of_dict, make_poly_amenity_dict_of_dict, and read homes. All others were
used to prepare data for efficient reading. Many function are heavily dependent on reading shapefiles
and the shapefile library.
"""
import shapefile as shp


"""
This function gets the average point given a set of points. It was used in the creation of the
homes csv, where the location of a home is abstracted to the average point of its geometry.
 
@args list of points representing home shape
@returnaverage point representing home location
"""
def get_average_point_of_polygon(points):
    x_sum = 0
    y_sum = 0
    num_points = len(points)
    for point in points:
        x_sum += point[0]
        y_sum += point[1]
    return(x_sum/num_points, y_sum/num_points)


'''
This function and following function create dictionaries that store the amenities
at each node in a selected network. The take a network type and read in the
respective shape file of the pointer shapefiles. This shapefile has every
point amenity and the intersection they are closest to. After reading the
shapefile, it iterates through the shapefile, and creates a key value
pair for every network node, and adds any amenity dictionary attached value of
the node key. The amenity dictionary is a dict of amenity names to
data describing the amenity. If two of the same amenity are at the same
network node, then the data is appended to the existing amenity.
 
Example
node_dicct = {network node: {"library": [name, location, ect], "cafe": [name, location, ect]}
 
@args kind of network
@return point amenity dict
 
'''

def make_point_amenity_dict_of_dict(kind):
    point_amenity_dict_of_dicts = {}
    shp_path = ""
    if kind == 'r':
        shp_path = "pointer_files/Road/point_amenities_to_road_intersections.shp"#file to read
    elif kind == 'w':
        shp_path = "pointer_files/Walk/point_amenities_to_walk_intersections.shp"#file to read
    elif kind == 'b':
        shp_path = "pointer_files/Bike/point_amenitites_to_point_amenitites.shp"#file to read
    else:
        print("Not valid pointer dict type")
        return
    sf = shp.Reader(shp_path)#read file
    length = len(sf.shapes())#number of records
    for i in range(0, length):
        shapeRec = sf.shapeRecord(i)
        data = shapeRec.record
        node = int(data[194])#network node
        amenity = data[2]#amenity name
        try:#if node in dict already
            point_amenity_dict_of_dicts[node]
            if amenity in point_amenity_dict_of_dicts[node].keys():
                point_amenity_dict_of_dicts[node][amenity].append(list(filter(('').__ne__, data[0:])))
            else:
                point_amenity_dict_of_dicts[node][amenity] = [list(filter(('').__ne__, data[0:]))]
        #if node not in dict already
        except Exception as e:
            point_amenity_dict_of_dicts[node] = {amenity : [list(filter(('').__ne__, data[0:]))]}
    return point_amenity_dict_of_dicts


"""
This function works the same as the one above, but with polygon type amenitites.
 
 
@args kind of network
@return poly amenity dict
"""
def make_poly_amenity_dict_of_dict(kind):
    point_amenity_dict_of_dicts = {}
    shp_path = ""
    if kind == 'r':
        shp_path = "pointer_files/Road/poly_amenitites_to_road_intersections.shp"#file to read
    elif kind == 'w':
        shp_path = "pointer_files/Walk/poly_amenitites_to_walk_intersections.shp"#file to read
    elif kind == 'b':
        shp_path = "pointer_files/Bike/poly_amenitites_to_bike_intersections.shp"
    else:
        print("Not valid pointer dict type")
        return    
    sf = shp.Reader(shp_path)#read file
    length = len(sf.shapes())#number of records
    for i in range(0, length):
        shapeRec = sf.shapeRecord(i)
        data = shapeRec.record
        node = int(data[200])#network node
        amenity = data[2]#amenity name
        try:
            point_amenity_dict_of_dicts[node]            
            if amenity in point_amenity_dict_of_dicts[node].keys():
                point_amenity_dict_of_dicts[node][amenity].append(list(filter(('').__ne__, data[0:])))
            else:
                point_amenity_dict_of_dicts[node][amenity] = [list(filter(('').__ne__, data[0:]))]
        except Exception as e:
            point_amenity_dict_of_dicts[node] = {amenity : [list(filter(('').__ne__, data[0:]))]}
    return point_amenity_dict_of_dicts





"""
This is a legacy function that was used to organize all the housing units of Atlanta
into a list. I determined the housing_types by printing out all building types and
selecting those that people would live in. All buildings described as one of these
housing types are considered a home.
 
The function starts by reading all the building network pointer files which are all
ordered the same. This means they can be iterated through simultaneously. For every
building, if it is a home, its average point, closest network nodes, and distance to
those nodes are appended to a list. This list contains all housing units in atlanta
and their pointers to each network type. 
 
 
home = [average_point, road_node, walk_node, bike_node, road_dist, walk_dist, bike_dist]
 
@args none
@return housing list 2d array of homes.
"""
def get_homes():
    shp_path_road = "Buildings_projected_meters/WGS_projected/wgs_buildings_to_intersections.shp"#file to read
    shp_path_walk = "Buildings_projected_meters/WGS_projected/wgs_buildings_to_walk_intersections.shp"#file to read
    shp_path_bike = "Buildings_projected_meters/WGS_projected/wgs_buildings_to_bike_intersections.shp"#file to read

    housing_types = ['residential', 'Residential_Condominium', 'condominium', 'house', 'shelter', 'condominiums']
    housing_list = []
    sf_road = shp.Reader(shp_path_road)#read file
    sf_walk = shp.Reader(shp_path_walk)#read file
    sf_bike = shp.Reader(shp_path_bike)#read file
    length = len(sf_road.shapes())#number of records
    for i in range(0, length):
        shapeRec = sf_road.shapeRecord(i)
        shapeRecWalk = sf_walk.shapeRecord(i)
        shapeRecBike = sf_bike.shapeRecord(i)
        data = shapeRec.record
        data_walk = shapeRecWalk.record
        data_bike = shapeRecBike.record
        kind = data[12] #All networks have building type at index 12 so only need to check one
        average_point = get_average_point_of_polygon(sf_road.shape(i).points)
        if kind in housing_types:
            road_node = int(list(filter(('').__ne__, data[0:]))[-4])
            road_dist = int(list(filter(('').__ne__, data[0:]))[-1])
            walk_node = int(list(filter(('').__ne__, data_walk[0:]))[-4])
            walk_dist = int(list(filter(('').__ne__, data[0:]))[-1])
            bike_node = int(list(filter(('').__ne__, data_bike[0:]))[-4])
            bike_dist = int(list(filter(('').__ne__, data[0:]))[-1])
            housing_list.append([(str(average_point).replace(",", ""))[1:-1], road_node, walk_node, bike_node, road_dist, walk_dist, bike_dist])
    return housing_list


"""
This function takes the homes list created in the above function and writes it to a csv.
 
@args homes list of home data
@return none
"""
def write_homes(homes):
    r = open("homes.csv", "a")
    r.write("Location, Closest Road Node, Closest Walk Node, Closest Bike Node, Distance to Road Node, Distance to Walk Node, Distance to Bike Node\n")
    for home in homes:
        for information in home:
            r.write(str(information) + ", ")
        r.write("\n")

"""
This function is used to read the information from the homes.csv into a 2d list
similar to the one made by get homes. This list is returned to access simulation
and used to sample homes.
 
@args none
@return home_data
"""
def read_homes():
    home_data = []
    with open("homes.csv") as f:
        content = f.readlines()
    for line in content[1:]:
        home_elements = line.split(", ")
        home_elements[0] = home_elements[0].split(" ") #reset first element to be x,y indexable cords
        home_elements[0][0] = float(home_elements[0][0])
        home_elements[0][1] = float(home_elements[0][1])
        home_data.append(home_elements[:-1])#get rid of new line element of list
    return home_data

"""
get amenities was used to retrieve a list of all amenities. Amenities produced from this
function can be used to calculate access
 
@args none
@return none
"""
def get_amenities():
    amenities = set()
    shp_path = "Buildings_projected_meters/pointer_files/poly_amenitites_to_road_intersections.shp"#file to read
    sf = shp.Reader(shp_path)#read file
    length = len(sf.shapes())#number of records
    for i in range(0, length):    
        shapeRec = sf.shapeRecord(i)
        data = shapeRec.record
        amenity = data[2]
        amenities.add(amenity)
    
    print(amenities)


