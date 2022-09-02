
"""
This file contains the Results_For_Amenity class which handles all the data collection and presentation for the
access simulation. More functions could easily be added to write data to files or present data in different ways.
"""
import matplotlib.pyplot as plt


"""
This class handles all the data storage, update, and presentation from the access simulation file.
The data recording happens in the add_data function, and all of it is stored in the attributes for the
class. The class stores all entries in matrices, number of entries in lists, averages in lists,
and entries over time(iterations) in dicts. The initializer sets the amenity name that the class
represents and initializes all empty data storages. After that add_data is used to update data
storage structures. Update survey is used to maintain the survey structures by adding the
number of entries for each collected data type over time. Update averages, updates the
averages list for race and education each time data is added. Every other function is used to
display the data using the matplotlib library. There are 6 charts, all called by the multip_plot
function. This function is called at the end of the access_simulation function. 
"""
class Results_For_Amenity:
    amenity = ""
    #These matrices hold every data entry for respective demographic data
    #Ex. first index of race matrix holds all white times
    race_matrix = [[], [], [], [], [], [], []]
    education_matrix = [[], [], [], [], [], [], []]
    median_income = [[],[]]#fist index is income, second is time(x, y relation)
    #These data structures hold the number of entries for each 
    #demographic varrible and type
    race_entries = [0, 0, 0, 0, 0, 0, 0]
    education_entries = [0, 0, 0, 0, 0, 0, 0]
    income_entries = 0 
    network_entries = [0, 0, 0]
    #These lists hold the avrage times for each demographic 
    #varrible
    race_averages = [0, 0, 0, 0, 0, 0, 0]
    education_averages = [0, 0, 0, 0, 0, 0, 0]

    #These dictionaries record the survey entries of iterations
    #used for stack plots (bottom row)
    race_survey_dict = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[]}
    eductaion_survey_dict = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[]}
    trans_survey_dict = {0:[], 1:[], 2:[]}
    #homes sampled
    iterations = 0
    #labels for charts
    race_labels = ["White", "Black or\nAfrican American", "American Indian and\n Alaska Native", "Asian", "Native Hawaiian and\nOther Pacific Islander", "Some Other Race", "Two or More Races"]
    education_Labels = ["Less than High School", "High School Graduate", "Some College", "Bachelor's Degree", "Master's Degree", "Professional School Degree", "Doctorate Degree"]

    """
    Initilizer sets the amenity name to the input amenity

    @args amenity name
    @return instance of class
    """
    def __init__(self, amenity):
        self.amenity = amenity
        

    """
   add_data takes the race, education, median household income, network type, and dist to node(really time) data
   and adds it to the appropriate structures. dist_to_node_hours is multiplied by 60 to get it into minutes. The
   update_averages and update_survey functions are called after data has been added, and their respective structures are
   updated in those functions. The iterations are also updated before the calling of those functions so that
   the survey data accurately reflects entries at time of entry.
 
   @args race, edu, wealth, network_type, dist_to_node_hours
   @return none
   """

    def add_data(self, race, edu, wealth, network_type, dist_to_node_hours):
        dist_to_node = dist_to_node_hours * 60
        self.race_matrix[race].append(dist_to_node)
        self.race_entries[race] += 1
        self.education_matrix[edu].append(dist_to_node)
        self.education_entries[edu] += 1
        self.median_income[0].append(wealth)
        self.median_income[1].append(dist_to_node)
        self.income_entries += 1
        self.network_entries[network_type] += 1
        self.iterations += 1
        self.update_averages()
        self.update_survey()
        

    """
    update_survey iterates through the recently updated entry counts and appends those
    values to lists in dicts associated with the correct demographic variable. It does this for
    each of race, education, and transportation. The structure then is a dict of lists
    that has entries for a demographic variable over time.
    
    Ex. race_survey_dict[0] = [1, 2, 2, 3, 4]
        white person sampled on first, second, fourth and fifth iteration
    
    updates attribute data
    """
    def update_survey(self):
        for race, entries in enumerate(self.race_entries):
            self.race_survey_dict[race].append(entries)
        for edu, entries in enumerate(self.education_entries):
            self.eductaion_survey_dict[edu].append(entries)
        for trans, entries in enumerate(self.network_entries):
            self.trans_survey_dict[trans].append(entries)
        

    """
    update_averages updates the averages of the the racial and education data for the most recent
    data entry. If it is the first entry old_mean == 0 then just add the most recent data entry
    (self.race_matrix[i][-1]) otherwise re-calculate the mean given the new value. It does this by
    not iterating through all the values to save time. Updates attribute data.
    
    @args none
    @return none
    """
    def update_averages(self):
        for i, old_mean in enumerate(self.race_averages):
            if old_mean == 0:
                if self.race_matrix[i] != []:
                    self.race_averages[i] = self.race_matrix[i][-1]
            else:
                self.race_averages[i] = old_mean + ( (self.race_matrix[i][-1] - old_mean) / self.race_entries[i])
        for i, old_mean in enumerate(self.education_averages):
            if old_mean == 0:
                if self.education_matrix[i] != []:
                    self.education_averages[i] = self.education_matrix[i][-1]
            else:
                self.education_averages[i] = old_mean + ( (self.education_matrix[i][-1] - old_mean) / self.education_entries[i])
        
    ### Data Visulization Below ###


    """
    This function handles the formatting of the Race subplot using matplotlib. It's
    a bar chart comparing race (labels) to average travel times. Title, x axis, and y
    axis labels are set. No need to return the subplot because it is pointed to and updated.
    
    @args Race sub-plot
    """
    def handle_race_chart(self, Race):
        Race.bar(self.race_labels, self.race_averages, 0.4, color=["blue", "orange", "green", "red", "purple", "brown", "pink"])
        Race.set_title("Access Time for " + self.amenity + " Given Race")
        Race.set_xticklabels(self.race_labels, rotation=20, fontsize='x-small', stretch='semi-condensed')
        Race.set_xlabel("Race")
        Race.set_ylabel("Access Time in Min")

    """
    This function handles the formatting of the education chart and is formatted the same as the race
    chart. Read for information


    @args Edu sup-plot
    """
    def handle_education_chart(self, Edu):
        Edu.bar(self.education_Labels, self.education_averages, 0.4, color=["blue", "orange", "green", "red", "purple", "brown", "pink"])
        Edu.set_title("Access Time for " + self.amenity + "\n Given Education Attainment")
        Edu.set_xticklabels(self.education_Labels, rotation=20, fontsize='x-small', stretch='semi-condensed')
        Edu.set_xlabel("Education Attainment Level")
        Edu.set_ylabel("Access Time in Min")

    """
    This function handles the formatting of the income chart. It is a scatter plot that displays the
    access time as a function of household income. The first line establishes this relationship, and
    following line edit labels


    @args Income
    """
    def handle_Income_Chart(self, Income):
        Income.scatter(self.median_income[0], self.median_income[1], s=1)
        Income.set_title("Access Time for " + self.amenity + "\n as a Function of Household Income")
        Income.set_xlabel("Household Income")
        Income.set_ylabel("Access Time in Min")


    """
    This function handles the formatting of the race sample chart which is a stack plot. Stack
    plots are usually used to display population over time data, and seemed appropriate for
    the sample data. The first line uses the range of 0-iteration count for the x axis, the
    values from the race_survey_dict to represent race groups sampled over time, and the race
    labels to label each group. The remaining lines format the axes and legends.

    @args r_samp sub-plot
    """
    def handle_race_sample_chart(self, r_samp):
        r_samp.stackplot(range(self.iterations), self.race_survey_dict.values(), labels= self.race_labels, alpha=0.8)
        r_samp.legend(loc='upper left')
        r_samp.set_title('Race of Homes Sampled Over Sample Iteration')
        r_samp.set_xlabel('Number of Simulated Access Times')
        r_samp.set_ylabel('Sample Iterations')


    """
    This function formats the education sample chart. It is identical to the above function, but uses the
    education data and labels.

    @args edu_samp sub plot for education
    """
    def handle_edu_sample_chart(self, edu_samp):
        edu_samp.stackplot(range(self.iterations), self.eductaion_survey_dict.values(), labels=self.education_Labels, alpha=0.8)
        edu_samp.legend(loc='upper left')
        edu_samp.set_title('Education Attainment of \nHomes Sampled Over Sample Iteration')
        edu_samp.set_xlabel('Number of Simulated Access Time Times')
        edu_samp.set_ylabel('Sample Iterations')

    """
    This function formats the transportation sample chart. It is identical to the above function, but uses transportation
    data and labels.

    @args trapo_samp sub plot for transportation
    """
    def hadle_transpo_sample_chart(self, trapo_samp):
        trapo_samp.stackplot(range(self.iterations), self.trans_survey_dict.values(), labels=["Car", "Walk", "Bike"], alpha=0.8)
        trapo_samp.legend(loc='upper left')
        trapo_samp.set_title('Method of Transportation Used by\n Homes Sampled Over Sample Iteration')
        trapo_samp.set_xlabel('Number of Simulated Access Times')
        trapo_samp.set_ylabel('Sample Iterations')


    """
    This function displays all collected data for an instance of the class using matplot lib.
    First it creates a figure to display and 6 subplots which are charts to display on the figure.
    The subplots are organized into a 2 by 3 grid, and represent the Race, Education, Household income,
    race sample, education sample, and transportation sample data. Each subplot is formated
    in their own function. A title is added to the entire chart and the figure is shown at the end
    with aesthetic formatting. Full screen is the best way to view the results.

    """
    def multi_plot(self):
        fig, ((Race, Edu, Income), (r_samp, edu_samp, trapo_samp)) = plt.subplots(2, 3)
        fig.suptitle('Race, Education, and Household Income Access Relations & Sampled Population of ' + str(self.iterations) + ' Homes')
        self.handle_race_chart(Race)
        self.handle_education_chart(Edu)
        self.handle_Income_Chart(Income)
        self.handle_race_sample_chart(r_samp)
        self.handle_edu_sample_chart(edu_samp)
        self.hadle_transpo_sample_chart(trapo_samp)
        plt.subplots_adjust(left=.08, bottom=.08, right=.92, top=.92, wspace=0.25, hspace=0.5)
        plt.show()


