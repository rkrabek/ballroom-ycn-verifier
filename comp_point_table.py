import pickle
import argparse

level_order = {
    'Newcomer'    : 1, 
    'Bronze'      : 2,
    'Silver'      : 3,
    'Gold'        : 4,
    'Novice'      : 5,
    'PreChamp'    : 6,
    'Championship': 7
    }
    
def full_record(comp_record):
    latin = {}
    standard = {}
    rhythm = {}
    smooth = {}
    # Fill out the point data for each style
    for level in comp_record.levels.__dict__:
        latin[level_order[level]] = (level, comp_record.levels.__dict__[level].__dict__['Latin'].__dict__)
        standard[level_order[level]] = (level, comp_record.levels.__dict__[level].__dict__['Standard'].__dict__)
        rhythm[level_order[level]] = (level, comp_record.levels.__dict__[level].__dict__['Rhythm'].__dict__)
        smooth[level_order[level]] = (level, comp_record.levels.__dict__[level].__dict__['Smooth'].__dict__)

    # Display the results

    # Latin - print the header
    print '{:^48}'.format("Latin")    
    print "%15s |" % str('Level').rjust(4, ' '),
    header = ["S", "CC", "R", "PD", "J"]
    for j in header:
        print "%4s " % str(j).rjust(4, ' '),
    print
    # print the results
    for level, value in sorted(latin.iteritems()):
        level_str = value[0]
        res = value[1]
        row = [res['Samba'], res['ChaCha'], res['Rumba'], res['PasoDoble'], res['Jive']]
        print "%15s |" % str(level_str).rjust(4, ' '),
        for j in row:
            print "%4d " % j,
        print
    print

    # Standard - print the header
    print '{:^48}'.format("Standard")    
    print "%15s |" % str('Level').rjust(4, ' '),
    header = ["W", "T", "VW", "F", "Q"]
    for j in header:
        print "%4s " % str(j).rjust(4, ' '),
    print
    # print the results
    for level, value in sorted(standard.iteritems()):
        level_str = value[0]
        res = value[1]
        row = [res['Waltz'], res['Tango'], res['VienneseWaltz'], res['Foxtrot'], res['Quickstep']]
        print "%15s |" % str(level_str).rjust(4, ' '),
        for j in row:
            print "%4d " % j,
        print
    print

    # Rhythm - print the header
    print '{:^48}'.format("Rhythm")    
    print "%15s |" % str('Level').rjust(4, ' '),
    header = ["CC", "R", "SW", "B", "M"]
    for j in header:
        print "%4s " % str(j).rjust(4, ' '),
    print    
    # print the results
    for level, value in sorted(rhythm.iteritems()):
        level_str = value[0]
        res = value[1]
        row = [res['ChaCha'], res['Rumba'], res['Swing'], res['Bolero'], res['Mambo']]
        print "%15s |" % str(level_str).rjust(4, ' '),
        for j in row:
            print "%4d " % j,
        print
    print

    # Standard - print the header
    print '{:^48}'.format("Smooth")    
    print "%15s |" % str('Level').rjust(4, ' '),
    header = ["W", "T", "F", "VW"]
    for j in header:
        print "%4s " % str(j).rjust(4, ' '),
    print
    # print the results
    for level, value in sorted(smooth.iteritems()):
        level_str = value[0]
        res = value[1]
        row = [res['Waltz'], res['Tango'], res['Foxtrot'], res['VienneseWaltz']]
        print "%15s |" % str(level_str).rjust(4, ' '),
        for j in row:
            print "%4d " % j,
        print

# Command-line parser
parser = argparse.ArgumentParser(
    description='Searches the O2CM pickle list and displays the YCN point totals for a competitor.')
parser.add_argument('--name', 
                    metavar='CompetitorName',
                    default='',
                    help='Name of competitor to search. Make sure the competitor\'s name is entered with correct capitalization exactly as it appears on the O2CM results listing, but remove all spaces from the name.')
parser.add_argument('--pickle-file', 
                    metavar='file',
                    default='comp_res.p',
                    help='Allows you to select a custom pickle file with O2CM scraped results. If this argument is ommitted, the default pickle file is used.')

args = parser.parse_args()



pf_in = open(args.pickle_file, "rb")
competitors = pickle.load(pf_in)
name = args.name
if name == '':
    name = raw_input("Please enter name with capitalization and no spaces as appears on results listing: ")

full_record(competitors[name])    
pf_in.close()
