import re
import comp_res_references

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
        try:
            dances = [comp_res_references.dance_map[style][x] for x in dances_abbr]
        except KeyError:
            dances = []
            print event + " has dances in it which do not match the detected style"
    else:
        dances = []
    return (style, dances)

# gets the points for a competitor and a style, adding in points from above levels
def get_points(competitors, name, level, style, dance):
    level_index = comp_res_references.level_list.index(level)
    counted_levels = comp_res_references.level_list[level_index:]
    # Novice points don't count for lower levels
    if counted_levels[0] != "Novice" and "Novice" in counted_levels:
        counted_levels.remove("Novice")
    points = 0
    for i, currLevel in enumerate(counted_levels):
        if i == 0:
            # Points in this level count normal
            points += competitors[name].levels.__dict__[currLevel].__dict__[style].__dict__[dance]
        elif i == 1:
            # Points in the level above count double
            points += 2 * competitors[name].levels.__dict__[currLevel].__dict__[style].__dict__[dance]
        else:
            # Any placement in two levels above counts as 7 points
            points += 7 if competitors[name].levels.__dict__[currLevel].__dict__[style].__dict__[dance] > 0 else 0
    return points