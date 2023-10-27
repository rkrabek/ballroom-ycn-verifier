from bs4 import BeautifulSoup
import urllib2
import requests
import re
import pickle
import helpers
import comp_res_references
from mechanize import Browser


# loads in pickle file with competitor results
competitors = {}
competition = raw_input("Please enter event id as found on in the url of the entries list:")

pf_in = open("comp_res_2018Mar12.p", "rb")
print "loading pickle file"
competitors = pickle.load(pf_in)
print "done loading"

# determines if competitor has placed out based on current level points and points in 2 levels above
def check_eligibility_pts(name, level, style, dance):
    def pt_lookup(level):
        try:
            return helpers.get_points(competitors, name, level, style, dance)
        except KeyError:
            # There is no record of eligible ycn placement history in pickle file
            return 0
    l_index = comp_res_references.level_list.index(level)
    curr_lvl_pts = pt_lookup(level)
    return (curr_lvl_pts < 7, curr_lvl_pts)

# post request to see all entries of an event
def entries_post(competition):

    br = Browser()
    br.open("https://entries.o2cm.com/?event=" + competition)
    br.select_form(name="webfilter")
    br.submit()
    
    soup = BeautifulSoup(br.response().read(), "html.parser")
    entries = soup.find_all('td', {"class":["h5b", "h5n"]})
    return entries

event = ""
level = ""
dances = []
style = ""

# goes through entries line by line
for post in entries_post(competition):
    # determines whether it is a event title or competitor entry
    names = post.find_all('a')
    if len(names) != 0:
        for name in names:
            name_concat = name.text.replace(" ", "")
            for dance in dances:
                elig_true = check_eligibility_pts(name_concat, level, style, dance)
                if not elig_true[0]:
                    print name_concat + " has placed out of " + event + " with " + str(elig_true[1]) + " points in " + level + " " + dance
                #else:
                    #print name_concat + " is ok to dance " + event + " with " + str(elig_true[1]) + " points in " + level + " " + dance
    else:
        # updates current event info
        event = post.text
        level = helpers.get_level(event)
        sty_dan = helpers.get_style_dances(event)
        style = sty_dan[0]
        dances = sty_dan[1]

pf_in.close()
