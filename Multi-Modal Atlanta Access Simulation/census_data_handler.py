'''
This file handles all functions related to the census data and block groups. When collecting census data from quickOSM in QGIS, the
bbox was not exact for collected census data and block groups. This means that 7 census blocks (located on the perimeter of the bbox) will
not return census data, so they are disconsidered when trying to retrieve census data. This file is dependent on the shapefile library and
shapely for doing quick computational geometry. The most important functions are build_demograhic_data_ditionary (builds a dict of block_id
to demographic data), get_census_block (returns census block given x, y cords), and the demographic data getters and probability assignments.
 
The prob_race(), prob_education(), method_of_transport assign the race, education level, and method of commute for the simulated resident
based of the census block's demographic percentages
'''

import shapefile as shp
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import random

global CENSUS_BLOCKS #a list with all the census blocks id, and their respective geometries
global CENSUS_BLOCKS_NOT_IN_DATA_DICT
global DATA_DICT 
CENSUS_BLOCKS = shp.Reader("Block Groups/actual_block_groups.shp")
CENSUS_BLOCKS_NOT_IN_DATA_DICT = ["1210082024", "0899800001", "1219800001", "1210068011", "0890231151", "0639800001", "1210007001"]



'''
LEGACY FUNCTION
 
This is a legacy function that is not used when running the program. It was used to combine the demographic data
and transportation data into a single dictionary. This program and write_demo_data_complete_to_new_file(demo_data)
were used to make demographic_data.csv into a more functional file
 
 
@return old version of demo data
'''
def read_acs_data():
    demo_data = {} #dictionary to hold demographic Data
    with open("accessibility_program/2019ACS.csv") as f:
        content = f.readlines()
    for line in content[2:]:
        elements = line.split(",") #Data for one census block
        data = elements[55:-1] # Relevent Data
        id = int(elements[55][-10:])#The ID for the census block. Ex = 0630402021
        demo_data[id] = data #add to dictionary 
    #print(demo_data.keys())
    with open("accessibility_program/transpo_data.csv") as f:
        content = f.readlines()
    x = 0
    y = 0
    failed_list = []
    for line in content[2:]:
        elements = line.split(",")
        if elements[70] != '':
            road = float(elements[70]) + float(elements[74])
            bike = float(elements[75])
            walk = float(elements[76])
            try:
                demo_data[int(elements[55][-10:])].append(road)
                demo_data[int(elements[55][-10:])].append(walk)
                demo_data[int(elements[55][-10:])].append(bike)
                y += 1
                #print("Sucsees :", y)
            except:

                failed_list.append(int(elements[55][-10:]))
                x += 1
                #print("Failed :", x)
    print("Sucesses rate " + str(y / (x + y)))
    test = set()

""""
LEGACY FUNCTION
 
This function wrote the dictionary data made from read_acs_data onto a file that was better suited for the program.
Transportation data was appended to the end of the file combining demographic and transportation data into a single
file.

@args = old version of demo_data
"""
def write_demo_data_complete_to_new_file(demo_data):
    r = open("/Users/noahgans/Desktop/School/Honors/Semester 2 Work/All the Code and Shit/accessibility_program/demographic_data.csv", "a")
    with open("accessibility_program/titles_clean.txt") as f:
        titles = f.readlines()
    for title in titles:
        r.write(title[:-1] + ", ")
    r.write("\n")
    print("came here")
    
    for key in demo_data.keys():

        print(str(key) + "-->" + str(demo_data[key]))

    #print(demo_data)
    for key in demo_data.keys():
        #print("came hereq1")
        r.write(str(key))
        for data_entry in demo_data[key][:-2]:
            r.write(", " + str(data_entry))
            print(data_entry)
        r.write("\n")
            
    return demo_data


"""
This function reads in demographic data from demographic_data.csv. Each line of the file
contains demographic data for one census block. Each id of each line is made a key of the
dictionary, and the respective values are assigned to the data of the census block. All
empty data entries are filled in with the None type in the dictionary. Data is added as
an int or string with the try except phrase.

@ags None
@return demographic_data dictionary
"""
def build_demograhic_data_ditionary():
    demographic_data = {}
    with open("demographic_data.csv") as f:
        content = f.readlines()
    for line in content[1:]:#skip title line
        data_for_one_block_group = line.split(",") #Data for one census block
        data_to_add = []
        for element in data_for_one_block_group[1:]:#skip block id, it will become key of dict
            string_to_add = element.strip()#clean quotes
            if string_to_add == "None":
                data_to_add.append(None)
            else:
                try:
                    data_to_add.append(int(string_to_add))
                except:
                    data_to_add.append(float(string_to_add))
        id = int(data_for_one_block_group[0])#The ID for the census block. Ex = 0630402021
        demographic_data[id] = data_to_add #add to dictionary 
    return demographic_data

DATA_DICT = build_demograhic_data_ditionary()

'''
This function finds the census block group of  the given x,y point using a shapley external library.
It iterated through the each census block, retrieves the geometries, and then checks if the point is within
the geometry. If it is, it returns the respective block_id 

@args x, y  floats
@return block_id
'''
def get_census_tract(x, y):
    point = Point(x, y) #input point, likly a building
    for i in range(len(CENSUS_BLOCKS)):
        polygon = Polygon(CENSUS_BLOCKS.shapeRecord(i).shape.points)
        if(polygon.covers(point)):#if point in polygon
            block_id = CENSUS_BLOCKS.shapeRecord(i).record[1] + CENSUS_BLOCKS.shapeRecord(i).record[2] + CENSUS_BLOCKS.shapeRecord(i).record[3]
            if block_id in CENSUS_BLOCKS_NOT_IN_DATA_DICT:
                return None 
            return int(block_id)
    #if it point is not in census block return None
    return None

"""
Returns the percent racial compositions for the given census block id. 7 total.
["White Alone", "Black or African American Alone", "American Indian and Alaska Native Alone", 
"Asian Alone", "Native Hawaiian and Other Pacific Islander Alone", "Some Other Race Alone", "Two or More Races"]

@args block_id
@return list of racial percents
"""
def get_race_data(id):
    return DATA_DICT[id][47:54]

"""
Returns the percent education attainment compositions for the given census block id. 7 total.
["Less than High School", "High School Graduate (Includes Equivalency)", "Some College", 
"Bachelor's Degree", "Master's Degree", "Professional School Degree", "Doctorate Degree"]
       
@args block_id
@return list of education attainment composisitons
"""
def get_education_data(id):
    return DATA_DICT[id][123:130]
"""
Returns the median houshold income for the respective census block

@args block_id
@return median income
"""
def get_household_income_data(id):
    return DATA_DICT[id][135]

"""
Returns the percent transportation use compositions for the given census block id. 3 total.
Drive, Walk, Bike
       
@args block_id
@return list of transportation use percents
"""
def get_transportation_data(id):
    return DATA_DICT[id][-3:]

"""
Given racial data, probabilistically assigns a race using the probability distributions from the
census block group compositions. A random number between 0 and 100 is generated and then the
race corresponding to the respective interval is selected.
 
@args race demographic data
@return int index corresponding to race
"""
def prob_race(race_data):

        while(True):
                dice_roll = random.uniform(0, 100)
                running_total = 0
                for i, element in enumerate(race_data):
                        running_total += element
                        if running_total > dice_roll:
                                return i

"""
Works the exact same as prob_race but with the education attainment levels
 
@args education attainment demographic data
@return int index corresponding to education attainment
"""                                     
def prob_education(edu_data):
        
        while(True):
                dice_roll = random.uniform(0, 100)
                
                running_total = 0
                for i, element in enumerate(edu_data):
                        running_total += element
                        if (running_total > dice_roll):
                                return i      
"""
Works the exact same as prob_race but with the transportation method
 
@args transportation method demographic data
@return int index corresponding to transportation method
"""
def method_of_transport(data):
        while(True):
                dice_roll = random.uniform(0, 100)
                #print("Rand: ", dice_roll)
                running_total = 0
                #print(type(data))
                for i, element in enumerate(data):
                        
                        running_total += element
                        #print("Comparison : ", running_total, ">", dice_roll)
                        if running_total > dice_roll:
                                return i




