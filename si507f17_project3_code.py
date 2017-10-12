from bs4 import BeautifulSoup
import unittest
import requests

#########
## Instr note: the outline comments will stay as suggestions, otherwise it's too difficult.
## Of course, it could be structured in an easier/neater way, and if a student decides to commit to that, that is OK.

## NOTE OF ADVICE:
## When you go to make your GitHub milestones, think pretty seriously about all the different parts and their requirements, and what you need to understand. Make sure you've asked your questions about Part 2 as much as you need to before Fall Break!


######### PART 0 #########

# Write your code for Part 0 here.

html_data = requests.get("http://newmantaylor.com/gallery.html").text

soup = BeautifulSoup(html_data, "html.parser")

def get_waiving_kitty(object):
    kitty_list = []
    kitty_data = soup.find("body")
    img = kitty_data.find_all('img')
    for alt in img:
        if alt.get('alt') == None:
            kitty_list.append("No alternate text provided!")
        else:
            kitty_list.append(alt.get('alt'))
    return(kitty_list)

######### PART 1 #########

# Get the main page data...

# Try to get and cache main page data if not yet cached
# Result of a following try/except block should be that
# there exists a file nps_gov_data.html,
# and the html text saved in it is stored in a variable
# that the rest of the program can access.

try:
    with open("nps_gov_data.html", "r") as f:
        nps_gov_data = f.read()

except:
    nps_gov_data = requests.get("https://www.nps.gov/index.htm").text
    with open("nps_gov_data.html", "w") as f:
        f.write(nps_gov_data)

# We've provided comments to guide you through the complex try/except, but if you prefer to build up the code to do this scraping and caching yourself, that is OK.

# Get individual states' data...

# Result of a following try/except block should be that
# there exist 3 files -- arkansas_data.html, california_data.html, michigan_data.html
# and the HTML-formatted text stored in each one is available
# in a variable or data structure
# that the rest of the program can access.

# TRY:
# To open and read all 3 of the files
try:
    with open("arkansas_data.html", 'r') as a:
        arkansas_data = a.read()
    with open("california_data.html", 'r') as c:
        california_data = c.read()
    with open("michigan_data.html", 'r') as m:
        michigan_data = m.read()

# # But if you can't, EXCEPT:
except:
    main_soup = BeautifulSoup(nps_gov_data, "html.parser")
    state_index = main_soup.find("ul", {"class":"dropdown-menu SearchBar-keywordSearch"})
    list_of_states = []
    for st in state_index.find_all("a"):
        list_of_states.append(st.get('href'))

    list_of_wanted_states = []
    for state in list_of_states:
        if "/ar/" in state:
            list_of_wanted_states.append(state)
        elif "/ca/" in state:
            list_of_wanted_states.append(state)
        elif "/mi/" in state:
            list_of_wanted_states.append(state)

    full_urls = []
    for url in list_of_wanted_states:
        full_urls.append("http://www.nps.gov" + url)

    arkansas_data = requests.get(full_urls[0]).text
    with open("arkansas_data.html", "w") as f:
        f.write(arkansas_data)

    california_data = requests.get(full_urls[1]).text
    with open("california_data.html", 'w') as f:
        f.write(california_data)

    michigan_data = requests.get(full_urls[2]).text
    with open("michigan_data.html", "w") as f:
        f.write(michigan_data)

# Create a BeautifulSoup instance of main page data
# Access the unordered list with the states' dropdown

# Get a list of all the li (list elements) from the unordered list, using the BeautifulSoup find_all method

# Use a list comprehension or accumulation to get all of the 'href' attributes of the 'a' tag objects in each li, instead of the full li objects

# Filter the list of relative URLs you just got to include only the 3 you want: AR's, CA's, MI's, using the accumulator pattern & conditional statements


# Create 3 URLs to access data from by appending those 3 href values to the main part of the NPS url. Save each URL in a variable.


## To figure out what URLs you want to get data from (as if you weren't told initially)...
# As seen if you debug on the actual site. e.g. Maine parks URL is "http://www.nps.gov/state/me/index.htm", Michigan's is "http://www.nps.gov/state/mi/index.htm" -- so if you compare that to the values in those href attributes you just got... how can you build the full URLs?


# Finally, get the HTML data from each of these URLs, and save it in the variables you used in the try clause
# (Make sure they're the same variables you used in the try clause! Otherwise, all this code will run every time you run the program!)


# And then, write each set of data to a file so this won't have to run again.


######### PART 2 #########

## Before truly embarking on Part 2, we recommend you do a few things:

# - Create BeautifulSoup objects out of all the data you have access to in variables from Part 1

# - Do some investigation on those BeautifulSoup objects. What data do you have about each state? How is it organized in HTML?

# HINT: remember the method .prettify() on a BeautifulSoup object -- might be useful for your investigation! So, of course, might be .find or .find_all, etc...

# HINT: Remember that the data you saved is data that includes ALL of the parks/sites/etc in a certain state, but you want the class to represent just ONE park/site/monument/lakeshore.

# We have provided, in sample_html_of_park.html an HTML file that represents the HTML about 1 park. However, your code should rely upon HTML data about Michigan, Arkansas, and Califoria you saved and accessed in Part 1.

# However, to begin your investigation and begin to plan your class definition, you may want to open this file and create a BeautifulSoup instance of it to do investigation on.

# Remember that there are things you'll have to be careful about listed in the instructions -- e.g. if no type of park/site/monument is listed in input, one of your instance variables should have a None value...

arkansas_soup = BeautifulSoup(arkansas_data, "html.parser")
california_soup = BeautifulSoup(california_data, "html.parser")
michigan_soup = BeautifulSoup(michigan_data, "html.parser")

# park = arkansas_soup.find("li", {"class":"clearfix"})
# park = arkansas_soup.find("li", {"class": "clearfix"})

class NationalSite(object):
    def __init__(self, park):
        self.name = park.find("h3").text
        self.location = park.find("h4").text
        if park.find("h2") is None:
            self.type = ""
        else:
            self.type = park.find("h2").text
        self.description = park.find("p").text
        self.basic_info = ""
        basic_links = []
        basic_info_index = park.find(
                                "div",
                                {"class": "col-md-12 col-sm-12 noPadding stateListLinks"})
        for basic_info in basic_info_index.find_all("a"):
            basic_links.append(basic_info.get('href'))
        for each in basic_links:
            if "/basicinfo" in each:
                self.basic_info = str(each)

    def __str__(self):
        return "{} | {}".format(self.name, self.location)

    def get_mailing_address(self):
        basic = self.basic_info
        r = requests.get(basic).text
        basic_soup = BeautifulSoup(r, "html.parser")
        if basic_soup.get("span",
                        {"itemprop": "streetAddress"}) is None:
            self.street = ""
        else:
            self.street = basic_soup.find("span", {"itemprop": "streetAddress"}).text.strip('\n')
        if basic_soup.get("span",
                        {"itemprop": "addressLocality"}) is None:
            self.city = ""
        else:
            self.city = basic_soup.find(
                                    "span",
                                    {"itemprop": "addressLocality"}).text
        if basic_soup.get("span",
                        {"itemprop": "addressRegion"}) is None:
            self.state = ""
        else:
            self.state = basic_soup.find(
                                    "span",
                                    {"itemprop": "addressRegion"}).text
        if basic_soup.get("span",
                        {"itemprop": "postalCode"}) is None:
            self.state = ""
        else:
            self.zip_code = basic_soup.find(
                                        "span",
                                        {"itemprop": "postalCode"}).text

        return "{} / {} / {} / {}".format(
                                        self.street,
                                        self.city,
                                        self.state,
                                        self.zip_code)

    def __contains__(self, string):
        if string in self.name:
            return True
        else:
            return False

## Recommendation: to test the class, at various points, uncomment the following code and invoke some of the methods / check out the instance variables of the test instance saved in the variable sample_inst:


######### PART 3 #########

# Create lists of NationalSite objects for each state's parks.

# HINT: Get a Python list of all the HTML BeautifulSoup instances that represent each park, for each state.

arkansas_natl_sites = []
california_natl_sites = []
michigan_natl_sites = []

# print(arkansas_soup.find("ul", {"id": "list_parks"}))
# for ark_park in arkansas_soup.find_all("li", {"class": "clearfix"}):
ark = arkansas_soup.find("ul", {"id": "list_parks"})
for ark_park in ark.find_all("li", {"class": "clearfix"}):
    arkansas_natl_sites.append(NationalSite(ark_park))

cali = california_soup.find("ul", {"id": "list_parks"})
for cali_park in cali.find_all("li", {"class": "clearfix"}):
    california_natl_sites.append(NationalSite(cali_park))

mich = michigan_soup.find("ul", {"id": "list_parks"})
for mich_park in mich.find_all("li", {"class": "clearfix"}):
    michigan_natl_sites.append(NationalSite(mich_park))

#Code to help you test these out:
for p in california_natl_sites:
	print(p)
for a in arkansas_natl_sites:
	print(a)
for m in michigan_natl_sites:
	print(m)



######### PART 4 #########

## Remember the hints / things you learned from Project 2 about writing CSV files from lists of objects!

## Note that running this step for ALL your data make take a minute or few to run -- so it's a good idea to test any methods/functions you write with just a little bit of data, so running the program will take less time!

## Also remember that IF you have None values that may occur, you might run into some problems and have to debug for where you need to put in some None value / error handling!
