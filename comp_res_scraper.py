from bs4 import BeautifulSoup
import urllib2
import comp_res_references
import helpers
import requests
import re
import pickle
import sys
from mechanize import Browser

competitors = {}

# post request to see all for results of event
def entries_post(competition):

    url = "https://results.o2cm.com/event3.asp?event=" + competition
    br = Browser()
    br.open(url)
    br.select_form(name="webfilter")
    br.submit()
    
    soup = BeautifulSoup(br.response().read(), "html.parser")
    entries = soup.find_all('td', {"class":["h5b", "t2b"]})
    return (entries)

# validates age category
def validate_age_dances(curr_event):
    if len(re.findall("((Social)|(Teddy)|(Juvenile)|(Junior)|(Jr.)|(Youth)|(Yth.)|(Teen)|(Young)|(Under)|(under)|([0-9]-)|([0-9]+)|(Senior)){1}", curr_event)) > 0:
        return False
    elif len(re.findall("((T/S)|(Tea/)|(Stu/)|(Nine Dance)|(Ten Dance)|(Pro)|(Student)|(Mixed)|(WDSF)|(Scholar)|(Rookie)|(Solo)|(Lead)|(Follow)|(Club)|(Formation)|(Showdance)|(Team)|(SS-)){1}", curr_event)):
        return False
    elif len(re.findall("((Polka)|(West Coast)|(Salsa)|(Hustle)|(Salsa)|(Argentine)|(Merengue)|(Lindy)|(Blues)|(Bachata)|(2-Step)|(Country)){1}", curr_event)) > 0:
        return False
    else:
        return True

# finds number of heats
def get_heats(heats):
    if heats:
        return len(heats.find_all("option"))
    else:
        return 1
        
# finds placement for a result
def get_placement(result):
    x = result
    return int(x[0:(x.find(")"))])  

# returns points for a placement
def get_points(placement, curr_heats):
    # YCN rules for determining points awarded
    if placement <= 6:
        if (curr_heats == 2 and placement <= 3) or curr_heats > 2:
            if placement == 1:
                return 3
            elif placement == 2:
                return 2
            else:
                return 1
        else:
            return 0
    else:
        return 0

# validates level and style then sets current heats, 0 if invalid level or style
def set_curr_heats(event, curr_style, curr_level):
    if curr_style in comp_res_references.style_list and curr_level in comp_res_references.level_list:
        e_url = event[0].get('href')
        try:
            e_page = BeautifulSoup(urllib2.urlopen("http://results.o2cm.com/"+e_url), features="html5lib").find(id="selCount")
            return get_heats(e_page)
        except urllib2.HTTPError:
            print "Error 500, possibly no entries"
            return 0
    else:
        print curr_level + ' ' + curr_style + ' is not a valid ycn eligible event'
        return 0


#  gets events and results
def get_ycn_res(competition):
    # current event variables
    curr_event = ""
    curr_heats = 0
    curr_level = ""
    curr_style = ""
    curr_dances = []
    for post in entries_post(competition)[2:]:
        event = post.find_all('a')
        # determines if it is an entry result or an event title
        if len(event) != 0:
            curr_event = event[0].text
            if validate_age_dances(curr_event):
                curr_level = helpers.get_level(curr_event)
                style_dances = helpers.get_style_dances(curr_event)
                curr_style = style_dances[0]
                curr_dances = style_dances[1]
                # print curr_level
                curr_heats = set_curr_heats(event, curr_style, curr_level)
            else:
                curr_heats = 0
        else:
            res_entry = post.text
            placement = get_placement(res_entry)
            points = get_points(placement, curr_heats)
            # do not make entry if there are no points to save on run time
            if points > 0:
                names = res_entry[3:].split(' - ')[0]
                start = names.find(' ') + 1
                for name in names[start:].split(' & '):
                    if name.split(' ')[0] not in ['unknown', 'TBA']:
                        # hash by full name without spaces
                        name_key = name.replace(' ', '')
                        if name_key not in competitors:
                            competitors[name_key] = comp_res_references.ycnObject(name)
                        for dance in curr_dances:
                            competitors[name_key].add_points(curr_level, curr_style, dance, points)

last_comp = ""

if len(sys.argv) > 2 or (len(sys.argv) == 2 and sys.argv[1] != "update"):
    print "Usage: python comp_res_scraper.py [update]"
elif len(sys.argv) == 2:
    pickle_file = raw_input("Pickle file to load previous items from: ")
    print "Loading pickle file"
    competitors = pickle.load(open(pickle_file, "r"))
    print "Done loading pickle file"
    last_comp = raw_input("ID of the last comp included in the pickle file (e.g. adf16): ")

req = urllib2.urlopen('http://results.o2cm.com/')
soup = BeautifulSoup(req, "html.parser")
comp_urls = soup.find_all('a')

for comp_url in comp_urls:
    event_url = comp_url.get('href')
    start = event_url.find('=') + 1
    competition = event_url[start:]
    if last_comp != "" and competition == last_comp:
        break
    print competition
    get_ycn_res(competition)

output_file = raw_input("Pickle file to output results to: ")
pf_out = open(output_file, "wb")
pickle.dump(competitors, pf_out)
pf_out.close()
