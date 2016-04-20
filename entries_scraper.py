from bs4 import BeautifulSoup
import urllib2
import requests
import re
import pickle
import helpers
import comp_res_references

# loads in pickle file with competitor results
competitors = {}
pf_in = open("comp_res.p", "rb")
print "loading pickle file"
competitors = pickle.load(pf_in)
print "done loading"

competition = raw_input("Please enter event id as found on in the url of the entries list:")

# determines if competitor has placed out based on current level points and points in 2 levels above
def check_eligibility_pts(name, level, style, dance):
    def pt_lookup(level):
        try:
            return competitors[name].levels.__dict__[level].__dict__[style].__dict__[dance]
        except KeyError:
            # There is no record of eligible ycn placement history in pickle file
            return 0
    l_index = comp_res_references.level_list.index(level)
    curr_lvl_pts = pt_lookup(level)
    if l_index > 5:
        return (True, 0)
    else:
        pt_trickle = (curr_lvl_pts + pt_lookup(comp_res_references.level_list[l_index+1]))
        if l_index < 5:
            if pt_trickle < 7:
                if (pt_lookup(comp_res_references.level_list[l_index+2]) != 0):
                    return (False, pt_trickle + 7)
                else:
                    return (True, pt_trickle)
            else:
                return (False, pt_trickle)
        else:
            return ((pt_trickle < 7), pt_trickle)

# post request to see all entries of an event
def entries_post(competition):

    url = "http://entries.o2cm.com/default.asp"
    
    headers = { "Accept":"text/html,application/xhtml+xml,application/xml;q0.9,image/webp,*/*;q0.8",
                "Accept-Encoding":"gzip, deflate",
                "Accept-Language":"en-US,en;q0.8",
                "Cache-Control":"max-age0",
                "Connection":"keep-alive",
                "Content-Length":"69",
                "Content-Type":"application/x-www-form-urlencoded",
                "Cookie":"ASPSESSIONIDSQDRBDTTDOOHOKCBDPOBDGELJDLKOJLO; ASPSESSIONIDSSBRBCTTOMEKMGPBBLLEEANOMIMLPOMI",
                "Host":"entries.o2cm.com",
                "Origin":"http//entries.o2cm.com",
                "Referer":"http//entries.o2cm.com/default.asp",
                "user-agent":"entries-scraper"
    }
    
    payload = { "selDiv": "",
                "selAge": 00,
                "selSkl": 00,
                "selSty": "",
                "submit": "OK",
                "selEnt": "",
                "event": competition
    }
    
    r = requests.post(url, headers=headers, data=payload).text
    soup = BeautifulSoup(r)
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
    else:
        # updates current event info
        event = post.text
        level = helpers.get_level(event)
        sty_dan = helpers.get_style_dances(event)
        style = sty_dan[0]
        dances = sty_dan[1]

pf_in.close()
