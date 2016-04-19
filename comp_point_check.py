import pickle
pf_in = open("comp_res.p", "rb")
competitors = pickle.load(pf_in)
name = ""
while name != 'na':
    name = raw_input("Please enter name with capitalization and no spaces as appears on results listing: ")
    level = raw_input("Please enter level from: Newcomer, Bronze, Silver, Gold, Novice, PreChamp, Championship: ")
    style = raw_input("Please enter style from: Latin, Standard, Rhythm, Smooth: ")
    print vars(competitors[name].levels.__dict__[level].__dict__[style])
pf_in.close()