import pickle
import helpers
pf_in = open("comp_res_new.p", "rb")
competitors = pickle.load(pf_in)
name = ""
while name != 'na':
    name = raw_input("Please enter name with capitalization and no spaces as appears on results listing: ")
    level = raw_input("Please enter level from: Newcomer, Bronze, Silver, Gold, Novice, PreChamp, Championship: ")
    style = raw_input("Please enter style from: Latin, Standard, Rhythm, Smooth: ")
    
    points = {}
    for dance in vars(competitors[name].levels.__dict__[level].__dict__[style]):
    	points[dance] = helpers.get_points(competitors, name, level, style, dance)
    print points
pf_in.close()