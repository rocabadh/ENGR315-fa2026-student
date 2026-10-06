import sys

"""
Create a program which will provide answers to the questions posed in the assignment description.
We've provided a function which will parse the NYT covid database file (named "us-counties.csv"); 
however, its correct implementation will be up to you. DO NOT MODIFY THIS FUNCTION.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.
"""


def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date,county, state, fips, cases, deaths) information

    ____________________ DO NOT MODIFY THIS FUNCTION ___________________
    """
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date,county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, fips, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data

### YOUR CODE HERE ###
#Finding first cases in data
def find_first_case(data, county_name, state_name):
    """Finds the date of the first confirmed positive case for a given county and state.
    :param data: List of parsed tuples (date, county, state, fips, cases, deaths)
    :param county_name: Name of the target county/city (exact match)
    :param state_name: Name of the target state (exact match)
    :return: String representing the date of the first case
    """
    #Runs through every entry sequentially to find first case in specific county and state
    for entry in data:
        date, county, state, fips, cases, deaths = entry
        if county == county_name and state == state_name and cases > 0:
            return date

#Parsing the data from the CSV file
data = parse_nyt_data(r"data\covid\us-counties.csv")

#Find first case in specific county
harrisonburg_first_case = find_first_case(data, "Harrisonburg city", "Virginia")
rockingham_first_case = find_first_case(data, "Rockingham", "Virginia")

#Printing first case results
print(f"Harrisonburg first case: {harrisonburg_first_case}")
print(f"Rockingham first case: {rockingham_first_case}")

#Finding greatest number of cases in a day 
def find_max_new_cases(data, county_name, state_name):
   """Calculates daily new cases by differencing cumulative totals and identifies the single day with the maximum increase.
   :param data: List of parsed tuples
   :param county_name: Target county/city name
   :param state_name: Target state name
   :return: Tuple containing (peak_date, max_daily_cases)
   """
   target_data= []
    #Finding data from specific county and state
   for entry in data:
        date, county, state, fips, cases, deaths = entry
        if county == county_name and state == state_name:
            target_data.append(entry)
   #Tracking variables to findthe maximum number of new cases
   max_new_cases = -1
   max_new_cases_date = None
   previous_cases = 0
   #Calulcate daily new cases
   for entry in target_data:
        date, county, state, fips, cases, deaths = entry
        new_cases = cases - previous_cases
        #Update maximum if current new cases are greater than the previous maximum
        if new_cases > max_new_cases:
            max_new_cases = new_cases
            max_new_cases_date = date
        #Saves the current cumulative cases for the next iteration
        previous_cases = cases
   return max_new_cases_date, max_new_cases

#Printing results for greatest number of new cases in a day
harrisonburg_max_new_cases_date, harrisonburg_max_new_cases = find_max_new_cases(data, "Harrisonburg city", "Virginia")
rockingham_max_new_cases_date, rockingham_max_new_cases = find_max_new_cases(data, "Rockingham", "Virginia")

print(f"Harrisonburg max new cases: {harrisonburg_max_new_cases} on {harrisonburg_max_new_cases_date}")
print(f"Rockingham max new cases: {rockingham_max_new_cases} on {rockingham_max_new_cases_date}")

#Finding greatest number of new cases in a 7 day period 
def find_worst_7_day_period(data, county_name, state_name):
    """Identifies the 7-day period with the highest total number of new cases using a sliding window.
    :param data: List of parsed tuples
    :param county_name: Target county/city name
    :param state_name: Target state name
    :return: Tuple containing (start_date, end_date, total_cases_in_period)
    """
    target_data= []
    #Finding data from specific county and state
    for entry in data:
        date, county, state, fips, cases, deaths = entry
        if county == county_name and state == state_name:
            target_data.append(entry)
    #Calculate daily new cases and sort into a list
    daily_new_cases = []
    previous_cases = 0
    for entry in target_data:
        date, county, state, fips, cases, deaths = entry
        new_cases = cases - previous_cases
        daily_new_cases.append((date, new_cases))
        previous_cases = cases
    #Adding a 7 day window
    max_new_cases_7_day = -1
    max_new_cases_7_day_start_date = None
    max_new_cases_7_day_end_date = None
    #Loop through all possible 7-day windows in the daily new cases list
    for i in range(len(daily_new_cases) - 6):
        window=daily_new_cases[i:i+7]
        new_cases_7_day = sum(day[1] for day in window)
        #If this window has greatest sum, update max_new_cases_7_day and the corresponding start and end dates
        if new_cases_7_day > max_new_cases_7_day:
            max_new_cases_7_day = new_cases_7_day
            max_new_cases_7_day_start_date = window[0][0]
            max_new_cases_7_day_end_date = window[-1][0]
    return max_new_cases_7_day_start_date, max_new_cases_7_day_end_date, max_new_cases_7_day

#Printing results for greatest number of new cases in a 7 day period
harrisonburg_worst_7_day_start_date, harrisonburg_worst_7_day_end_date, harrisonburg_worst_7_day_cases = find_worst_7_day_period(data, "Harrisonburg city", "Virginia")
rockingham_worst_7_day_start_date, rockingham_worst_7_day_end_date, rockingham_worst_7_day_cases = find_worst_7_day_period(data, "Rockingham", "Virginia")

print(f"Harrisonburg worst 7-day period: {harrisonburg_worst_7_day_cases} from {harrisonburg_worst_7_day_start_date} to {harrisonburg_worst_7_day_end_date}")
print(f"Rockingham worst 7-day period: {rockingham_worst_7_day_cases} from {rockingham_worst_7_day_start_date} to {rockingham_worst_7_day_end_date}")