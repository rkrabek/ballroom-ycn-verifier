from bs4 import BeautifulSoup
import urllib2
import comp_res_references
import requests
import re
import pickle


competitors = {}
# comp_base_url = 'http://results.o2cm.com/event3.asp?event=hid16&bclr='
# url_color = '#FFFFFF&tclr=#000000'
# r = urllib2.urlopen(comp_base_url)
# soup = BeautifulSoup(r)
# names = soup.find(id="selEnt").find_all("option")

# post request for results of event
def entries_post(competition):
    #  only works until USA dance championships 07 because it switches to event2.asp
    url = "http://results.o2cm.com/event3.asp"
    
    headers = { "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding":"gzip, deflate",
                "Accept-Language":"en-US,en;q=0.8",
                "Cache-Control":"max-age=0",
                "Connection":"keep-alive",
                "Content-Length":"61",
                "Content-Type":"application/x-www-form-urlencoded",
                "Cookie":"ASPSESSIONIDQSCQBCST=ENACDHMCCJJNNCKJGLKAGBAG; ASPSESSIONIDSQDQACSS=LDNCAPFAAHLLLNKMPLEPPJBO; ASPSESSIONIDSQDRBDTT=LFLGOKCBLMEHPFMNPINFBMCE; ASPSESSIONIDSSCQBCSS=NEPKLCMCJAGFIKFCPEKKBCEB; ASPSESSIONIDSQDRADTT=OLJDLOIDAEOLHMCIJKIAIGEF; ASPSESSIONIDQQBSACTS=BHHMGGCBLFHJPMDFMAFPGAIN; ASPSESSIONIDSQBQADTT=HKGFFCPBPEGGCAJGLCCCMLGL",
                "Host":"results.o2cm.com",
                "Origin":"http://results.o2cm.com",
                "Referer":"http://results.o2cm.com/event3.asp",
                "user-agent":"ycn-points-scraper"
    }

    payload = { "selDiv": "",
                "selAge": "",
                "selSkl": "",
                "selSty": "",
                "selEnt": "",
                "submit": "OK",
                "event": competition
    }            
    r = requests.post(url, headers=headers, data=payload).text
    soup = BeautifulSoup(r)
    entries = soup.find_all('td', {"class":["h5b", "t2b"]})
    return (entries)

# validates age category
def validate_age_dances(curr_event):
    if len(re.findall("((Social)|(Teddy)|(Juvenile)|(Junior)|(Jr.)|(Youth)|(Yth.)|(Teen)|(Young)|(Under)|(under)|([0-9]-)|([0-9]+)|(Senior)){1}", curr_event)) > 0:
        # print curr_event + " is not in the adult age category"
        return False
    elif len(re.findall("((T/S)|(Tea/)|(Stu/)|(Nine Dance)|(Ten Dance)|(Pro)|(Student)|(Mixed)|(WDSF)|(Scholar)|(Rookie)|(Solo)|(Lead)|(Follow)|(Club)|(Formation)|(Showdance)|(Team)|(SS-)){1}", curr_event)):
        # print curr_event + " is not a valid ycn category"
        return False
    elif len(re.findall("((Polka)|(West Coast)|(Salsa)|(Hustle)|(Salsa)|(Argentine)|(Merengue)|(Lindy)|(Blues)|(Bachata)|(2-Step)|(Country)){1}", curr_event)) > 0:
        # print curr_event + " is not a valid ycn dance"
        return False
    else:
        return True

# finds level of event
def get_level(event):
    level = ""
    newcomer_try = re.findall("((Pre Bronze)|(Pre-Bronze))", event)
    if len(newcomer_try) != 0:
        level = "Newcomer"
    else:
        level_try = re.findall("((Newcomer)|(Bronze)|(Silver)|(Gold)|(Novice)|(Championship))", event)
        if len(level_try) == 0:
            level_try = re.findall("((Beginner)|(Intermediate)|(Advanced)|(Syllabus)|(Open)|(Pre-Champ))", event)
            if len(level_try) == 0:
                print "Level not found in" + event
                level = event
            else:
                level = level_try[-1][0]
            if level == "Pre-Champ":
                level = "PreChamp"
            elif level == "Beginner" or level == "Syllabus":
                level = "Bronze"
            elif level == "Intermediate":
                level = "Silver"
            elif level == "Advanced":
                level = "Gold"
            elif level == "Open":
                level = "Championship"
        else:
            level = level_try[0][0]
    return level

# finds dances of event
def get_dances_abbr(event):
    start = event.rfind("(")
    end = event.rfind(")")
    dances_abbr = re.findall("([WTVFQCRSJPMB])", event[start:end])
    return dances_abbr

# returns style and full name of dances
def get_style_dances(event):
    dances_abbr = get_dances_abbr(event)
    style = ""
    style_try = re.findall("((Standard)|(Latin)|(Rhythm)|(Smooth))", event)
    if len(style_try) == 0:
        style_try = re.findall("((Intl\.|Intl|Am\.|Am|Ballroom|BALLROOM|LATIN))", event)
        if len(style_try) == 0:
            print "Style not found in" + event
            style = event
        else:
            style = style_try[-1][0]
        if style in ["Intl.", "Intl"]:
            if any(x in dances_abbr for x in ['C','S','R','P','J']):
                style = "Latin"
            else:
                style = "Standard"
        elif style in ["Am.", "Am"]:
            if any(x in dances_abbr for x in ['W','T','F','V']):
                style = "Smooth"
            else:
                style = "Rhythm"
        elif style in ["Ballroom", "BALLROOM"]:
            style = "Standard"
        elif style == "LATIN":
            style = "Latin"
    else:
        style = style_try[0][0]
    if style in comp_res_references.style_list:
        # print event
        # event_list.write(event + '\n')
        try:
            dances = [comp_res_references.dance_map[style][x] for x in dances_abbr]
        except KeyError:
            dances = []
            # event_list.write(event + " has dances in it which do not match the detected style \n")
            print event + " has dances in it which do not match the detected style"
    else:
        dances = []
    return (style, dances)

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
            e_page = BeautifulSoup(urllib2.urlopen("http://results.o2cm.com/"+e_url)).find(id="selCount")
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
        if len(event) != 0:
            curr_event = event[0].text
            if validate_age_dances(curr_event):
                curr_level = get_level(curr_event)
                style_dances = get_style_dances(curr_event)
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

            if points > 0:
                names = res_entry[3:].split(' - ')[0]
                start = names.find(' ') + 1
                for name in names[start:].split(' & '):
                    if name.split(' ')[0] not in ['unknown', 'TBA']:
                        name_key = name.replace(' ', '')
                        if name_key not in competitors:
                            competitors[name_key] = comp_res_references.ycnObject(name)
                        for dance in curr_dances:
                            competitors[name_key].add_points(curr_level, curr_style, dance, points)


# event_list = open("eventlist.txt", "w")

req = urllib2.urlopen('http://www.o2cm.com/results/')
soup = BeautifulSoup(req)
comp_urls = soup.find_all('a')
for comp_url in comp_urls:
    event_url = comp_url.get('href')
    start = event_url.find('=') + 1
    competition = event_url[start:]
    print competition
    # event_list.write(competition + '\n')
    get_ycn_res(competition)
    
pf_out = open("comp_res.p", "wb")
pickle.dump(competitors, pf_out)
pf_out.close()