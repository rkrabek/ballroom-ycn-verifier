from bs4 import BeautifulSoup
import urllib2
import requests
import re
import pickle
import helpers
import comp_res_references

competitors = {}
pf_in = open("comp_res.p", "rb")
print "loading pickle file"
competitors = pickle.load(pf_in)
print "done loading"

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

def entries_post(event):

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
                "event": event
    }
    
    r = requests.post(url, headers=headers, data=payload).text
    soup = BeautifulSoup(r)
    entries = soup.find_all('td', {"class":["h5b", "h5n"]})
    return entries

# def get_entry_level(header):
#     level = ""
#     level_try = re.findall("((Newcomer)|(Bronze)|(Silver)|(Gold)|(Novice)|(Championship))", header)
#     if len(level_try) == 0:
#         level_try = re.findall("((Beginner)|(Intermediate)|(Advanced)|(Syllabus)|(Open)|(Pre-Champ))", header)
#         if len(level_try) == 0:
#             print "Level not found in" + header
#             level = header
#         else:
#             level = level_try[0][0]
#         if level == "Pre-Champ":
#             level = "PreChamp"
#         elif level == "Beginner" or level == "Syllabus":
#             level = "Bronze"
#         elif level == "Intermediate":
#             level = "Silver"
#         elif level == "Advanced":
#             level = "Gold"
#         elif level == "Open":
#             level = "Championship"
#     else:
#         level = level_try[0][0]
#     return level

# def get_entry_dances(header):
#     start = header.find("(")
#     end = header.find(")")
#     dances = re.findall("([WTVFQCRSJPMB])", header[start:end])
#     return dances

# def get_entry_style(entry, dances):
#     style = ""
#     dances_expanded = []
#     style_try = re.findall("((Standard)|(Latin)|(Rhythm)|(Smooth))", entry)
#     if len(style_try) == 0:
#         style_try = re.findall("((Intl\.|Am\.|Ballroom))", entry)
        
#         if len(style_try) == 0:
#             print "Style not found in" + entry
#             style = entry
#         else:
#             style = style_try[0][0]
#         if style == "Intl.":
#             if any(x in dances for x in ['C','S','R','P','J']):
#                 style = "Latin"
#             else:
#                 style = "Standard"
#         elif style == "Am.":
#             if any(x in dances for x in ['W','T','F','V']):
#                 style = "Smooth"
#             else:
#                 style = "Rhythm"
#         elif style == "Ballroom":
#             style = "Standard"
#     else:
#         style = style_try[0][0]
#         # print style
#     dances = [comp_res_references.dance_map[style][x] for x in dances]
#     return (style, dances)

event = ""
level = ""
dances = []
style = ""

for post in entries_post("mit"):
    names = post.find_all('a')
    if len(names) != 0:
        for name in names:
            name_concat = name.text.replace(" ", "")
            for dance in dances:
                elig_true = check_eligibility_pts(name_concat, level, style, dance)
                if not elig_true[0]:
                    print name_concat + " has placed out of " + event + " with " + str(elig_true[1]) + " points in " + level + " " + dance
    else:
        event = post.text
        level = helpers.get_level(event)
        sty_dan = helpers.get_style_dances(event)
        style = sty_dan[0]
        dances = sty_dan[1]
        # print '\n'+ event
        # print level
        # print dances
        # print style

pf_in.close()
# def get_entries(event, competitor_id):
#     entries = entries_post(event, competitor_id)
#     entry_list = []
#     for entry in entries:
#         level = get_entry_level(entry.text).encode("utf8")
#         style = get_entry_style(entry.text).encode("utf8")
#         entry_list.append((level, style))
#     return entry_list