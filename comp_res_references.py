level_list = ["Newcomer","Bronze","Silver","Gold","Novice","PreChamp","Championship"]
style_list = ["Standard","Latin","Rhythm","Smooth"]
dance_map = {
    "Latin" : {
        "S" : "Samba",
        "C" : "ChaCha",
        "R" : "Rumba",
        "J" : "Jive",
        "P" : "PasoDoble"
    },
    "Standard" : { 
        "W" : "Waltz",
        "T" : "Tango",
        "V" : "VienneseWaltz",
        "F" : "Foxtrot",
        "Q" : "Quickstep",
    },
    "Rhythm" : {
        "C" : "ChaCha",
        "R" : "Rumba",
        "S" : "Swing",
        "M" : "Mambo",
        "B" : "Bolero"
    },
    "Smooth" : {
        "W" : "Waltz",
        "T" : "Tango",
        "V" : "VienneseWaltz",
        "F" : "Foxtrot"
    }
}

class ycnObject(object):
    def __init__(self, name):
        self.name = name
        self.levels = Levels()
        self.version = 1
    def add_points(self, level, style, dance, points):
        self.levels.__dict__[level].__dict__[style].__dict__[dance] += points
        # setattr(getattr(getattr(getattr(self, "levels"),level),style),dance,getattr(getattr(getattr(getattr(self, "levels"),level),style),dance)+points)
        
class Levels(dict):
    def __init__(self):
        self.Newcomer = Level()
        self.Bronze = Level()
        self.Silver = Level()
        self.Gold = Level()
        self.Novice = Level()
        self.PreChamp = Level()
        self.Championship = Level()

class Level(dict):
    def __init__(self):
        self.Latin = Latin()
        self.Standard = Standard()
        self.Rhythm = Rhythm()
        self.Smooth = Smooth()

class Latin(dict):
    def __init__(self):
        self.Samba = 0
        self.ChaCha = 0
        self.Rumba = 0
        self.Jive = 0
        self.PasoDoble = 0

class Standard(dict): 
    def __init__(self):
        self.Waltz = 0
        self.Tango = 0
        self.VienneseWaltz = 0
        self.Foxtrot = 0
        self.Quickstep = 0

class Rhythm(dict):
    def __init__(self):
        self.ChaCha = 0
        self.Rumba = 0
        self.Swing = 0
        self.Mambo = 0
        self.Bolero = 0

class Smooth(dict):
    def __init__(self):
        self.Waltz = 0
        self.Tango = 0
        self.VienneseWaltz = 0
        self.Foxtrot = 0
