# Players Module
import itertools
import timeit
import random

start = timeit.default_timer()
'''
** LEGEND **
ls = Last Season
cr = Career
gp = Games Played
g = Goals
a = Assists
sh = Shots
pos = Position
gs = Game Started
w = Win
ga = Goals Against
so = Shut Out
sa = Shots Against
tot_s = Total Saves
'''
#---------------------------------------
## Todays Costs:
doc = open('DailyCosts.txt','r')
daily = doc.readlines()

#---------------------------------------
class Goalie():
    def __init__ (self, name, team, pos, gs_ls, w_ls, sa_ls, ga_ls, so_ls, gs_cr, w_cr, sa_cr, ga_cr, so_cr):
        self.name = name
        self.team = team
        self.pos = pos
        self.gs_ls = gs_ls
        self.w_ls = w_ls
        self.sa_ls = sa_ls
        self.ga_ls = ga_ls
        self.tot_s_ls = self.sa_ls - ga_ls
        self.so_ls = so_ls
        self.gs_cr = gs_cr
        self.w_cr = w_cr
        self.sa_cr = sa_cr
        self.ga_cr = ga_cr
        self.tot_s_cr = self.sa_cr - ga_cr
        self.so_cr = so_cr
    def prefix(self):
            if '-' not in self.name:
                return self.name.split(' ')[0][0] + '_' + self.name.split(' ')[-1]
            else:
                name = ''
                for i in list(self.name):
                    if i != '-':
                        name += i
                    else:
                        name += '_'
            prefix = name.split(' ')[0][0] + '_' + name.split(' ')[-1]
            return prefix
    def ev(self):
        expected_win_points = (((self.w_ls / self.gs_ls) * 3) + ((self.w_cr / self.gs_cr) * 3)) / 2
        expected_save_points = (((self.tot_s_ls / self.gs_ls) * 0.2) + ((self.tot_s_cr / self.gs_cr) * 0.2)) / 2
        expected_goals_against = (((self.ga_ls / self.gs_ls) * -1) + ((self.ga_cr / self.gs_cr) *-1)) /2
        expected_shutout_points = (((self.so_ls / self.gs_ls) * 2) + ((self.so_cr / self.gs_cr) * 2)) / 2
        expected_fantasy_points = expected_win_points + expected_save_points + expected_goals_against + expected_shutout_points
        expected_fantasy_points = round(expected_fantasy_points, 3)
        return self.name + ': ' + str(expected_fantasy_points)
    def ev_int(self):
        ev_str = self.ev().split(' ')
        return float(ev_str[-1])
    def cost(self):
        for i in range(len(daily)):
            line = daily[i]
            name = line[:len(line)-1]
            if name == self.name:
                return int(daily[i+1])
            else:
                pass
        print('Not in Document')
    def dpp(self):
        expected_points = self.ev_int()
        dollars_per_point = self.cost() / expected_points
        return dollars_per_point

#---------------------------------------
class Player():
    def __init__ (self, name, team, pos, gp_ls, g_ls, a_ls, sh_ls, bs_ls, gp_cr, g_cr, a_cr, sh_cr, bs_cr):
        self.name = name
        self.team = team
        self.pos = pos
        self.gp_ls = gp_ls
        self.g_ls = g_ls
        self.a_ls = a_ls
        self.sh_ls = sh_ls
        self.bs_ls = bs_ls
        self.gp_cr = gp_cr
        self.g_cr = g_cr
        self.a_cr = a_cr
        self.sh_cr = sh_cr
        self.bs_cr = bs_cr
    def prefix(self):
        if '-' not in self.name:
            return self.name.split(' ')[0][0] + '_' + self.name.split(' ')[-1]
        else:
            name = ''
            for i in list(self.name):
                if i != '-':
                    name += i
                else:
                    name += '_'
        prefix = name.split(' ')[0][0] + '_' + name.split(' ')[-1]
        return prefix
    def ev(self):
        expected_shot_points = (((self.sh_ls / self.gp_ls) * 0.5) + ((self.sh_cr / self.gp_cr) * 0.5)) / 2
        expected_goal_points = (((self.g_ls / self.gp_ls) * 3) + ((self.g_cr / self.gp_cr) * 3)) / 2
        expected_assist_points = (((self.a_ls / self.gp_ls) * 2) + ((self.a_cr / self.gp_cr) * 2)) / 2
        expected_blocked_shots_points = (((self.bs_ls / self.gp_ls) * 0.5) + ((self.bs_cr / self.gp_cr) * 0.5)) / 2
        expected_fantasy_points = expected_shot_points + expected_assist_points + \
            expected_goal_points + expected_blocked_shots_points
        expected_fantasy_points = round(expected_fantasy_points, 3)
        return self.name + ': ' + str(expected_fantasy_points)
    def ev_int(self):
        ev_str = self.ev().split(' ')
        return float(ev_str[-1])
    def cost(self):
        for i in range(len(daily)):
            line = daily[i]
            name = line[:len(line)-1]
            if name == self.name:
                return int(daily[i+1])
            else:
                pass
        return 0
    def dpp(self):
        expected_points = self.ev_int()
        dollars_per_point = self.cost() / expected_points
        return dollars_per_point

#---------------------------------------
class Team():
    def __init__(self, plr_lst):
        self.plr_lst = plr_lst
        self.len = len(self.plr_lst)
    def switch(self, lst):
        # switch the current player list with new player list
        self.plr_lst = lst
    def players(self):
        players = ''
        for player in self.plr_lst:
            players += player.name + ', '
        return players
    def ev(self):
        total_points = 2
        for player in self.plr_lst:
            total_points += player.ev_int()
        return total_points
    def cost(self):
        total_cost = 0
        for player in self.plr_lst:
            if player.cost() == 'Not in Document':
                return player.cost()
            else:
                total_cost += player.cost()
        return total_cost
    def dpp(self):
        tot_points = self.ev()
        return self.cost() / tot_points
    def worst(self):# Based on cost
        worst_plr = self.plr_lst[0]
        for plr in self.plr_lst:
            if plr.cost() == 'Not in Document':
                return 'Not in Document'
            elif plr.dpp() < worst_plr.dpp():
                pass
            else:
                worst_plr = plr
        return worst_plr.ev()
    def best(self):
        best_plr = self.plr_lst[0]
        for plr in self.plr_lst:
            if plr.cost() == 'Not in Document':
                return 'Not in Document'
            elif plr.dpp() > best_plr.dpp():
                pass
            else:
                best_plr = plr
        return best_plr.ev()
    def valid(self):
        if self.cost() > 50000:
                    return False
        pos_lst = list(map((lambda x: x.pos), self.plr_lst))
        if len(pos_lst) != 9:
            return False
        elif len(self.plr_lst) != len(set(self.plr_lst)):
            return False
        centers = len(list(filter((lambda x: x == 'C'), pos_lst)))
        wings = len(list(filter((lambda x: x == 'L' or x == 'R'), pos_lst)))
        defense = len(list(filter((lambda x: x == 'D'), pos_lst)))
        goalie = len(list(filter((lambda x: x == 'G'), pos_lst)))
        if goalie == 1 and centers == 2 and wings == 3 and defense == 3:
            return True
        elif goalie == 1 and centers == 2 and wings == 4 and defense == 2:
            return True
        elif goalie == 1 and centers == 3 and wings == 3 and defense == 2:
            return True
        else:
            return False




#---------------------------------------
def comp(plr_lst):
    best_player = plr_lst[0]
    for plr in plr_lst:
        if plr.dpp() < best_player.dpp():
            best_player = plr
        else:
            pass
    print(best_player.ev())

# Players
J_Abdelkader = Player('Justin Abdelkader', 'DET', 'LW', 71, 23, 21, 154, 28,71, 23, 21, 154,28)
W_Acton = Player('Will Acton', 'EDM', 'C', 3, 0, 0, 2, 3,3, 0, 0, 2,3)
L_Adam = Player('Luke Adam', 'CBJ', 'C', 3, 0, 0, 0, 0,3, 0, 0, 0,0)
C_Adams = Player('Craig Adams', 'PIT', 'RW', 70, 1, 6, 51, 29,70, 1, 6, 51,29)
A_Agozzino = Player('Andrew Agozzino', 'COL', 'LW', 1, 0, 1, 1, 0,1, 0, 1, 1,0)
J_Akeson = Player('Jason Akeson', 'PHI', 'RW', 13, 0, 0, 9, 4,13, 0, 0, 9,4)
B_Allen = Player('Bryan Allen', 'TOT', 'D', 11, 0, 2, 6, 15,11, 0, 2, 6,15)
C_Allen = Player('Conor Allen', 'NYR', 'D', 4, 0, 0, 2, 0,4, 0, 0, 2,0)
M_Alt = Player('Mark Alt', 'PHI', 'D', 1, 0, 0, 0, 0,1, 0, 0, 0,0)
K_Alzner = Player('Karl Alzner', 'WSH', 'D', 82, 5, 16, 72, 165,82, 5, 16, 72,165)
J_Anderson = Player('Josh Anderson', 'CBJ', 'RW', 6, 0, 1, 10, 2,6, 0, 1, 10,2)
J_Andersson = Player('Joakim Andersson', 'DET', 'C', 68, 3, 5, 74, 24,68, 3, 5, 74,24)
A_Andreoff = Player('Andy Andreoff', 'LAK', 'C', 18, 2, 1, 14, 0,18, 2, 1, 14,0)
S_Andrighetto = Player('Sven Andrighetto', 'MTL', 'RW', 12, 2, 1, 12, 4,12, 2, 1, 12,4)
M_Angelidis = Player('Mike Angelidis', 'TBL', 'LW', 3, 0, 0, 0, 0,3, 0, 0, 0,0)
A_Anisimov = Player('Artem Anisimov', 'CBJ', 'C', 52, 7, 20, 88, 26,52, 7, 20, 88,26)
M_Arcobello = Player('Mark Arcobello', 'TOT', 'C', 77, 17, 14, 129, 27,77, 17, 14, 129,27)
J_Armia = Player('Joel Armia', 'BUF', 'RW', 1, 0, 0, 0, 0,1, 0, 0, 0,0)
V_Arvidsson = Player('Viktor Arvidsson', 'NSH', 'LW', 6, 0, 0, 9, 5,6, 0, 0, 9,5)
C_Ashton = Player('Carter Ashton', 'TOR', 'RW', 7, 0, 0, 4, 3,7, 0, 0, 4,3)
C_Atkinson = Player('Cam Atkinson', 'CBJ', 'RW', 78, 22, 18, 212, 39,78, 22, 18, 212,39)
K_Aulie = Player('Keith Aulie', 'EDM', 'D', 31, 0, 1, 25, 37,31, 0, 1, 25,37)
D_Backes = Player('David Backes', 'STL', 'C', 80, 26, 32, 183, 87,80, 26, 32, 183,87)
M_Backlund = Player('Mikael Backlund', 'CGY', 'C', 52, 10, 17, 103, 33,52, 10, 17, 103,33)
N_Backstrom = Player('Nicklas Backstrom', 'WSH', 'C', 82, 18, 60, 153, 52,82, 18, 60, 153,52)
S_Baertschi = Player('Sven Baertschi', 'TOT', 'LW', 18, 2, 4, 15, 7,18, 2, 4, 15,7)
C_Bailey = Player('Casey Bailey', 'TOR', 'C', 6, 1, 0, 9, 4,6, 1, 0, 9,4)
J_Bailey = Player('Josh Bailey', 'NYI', 'LW', 70, 15, 26, 140, 36,70, 15, 26, 140,36)
K_Ballard = Player('Keith Ballard', 'MIN', 'D', 14, 0, 1, 5, 20,14, 0, 1, 5,20)
M_Barberio = Player('Mark Barberio', 'TBL', 'D', 52, 1, 6, 53, 46,52, 1, 6, 53,46)
A_Barkov = Player('Aleksander Barkov', 'FLA', 'C', 71, 16, 20, 123, 35,71, 16, 20, 123,35)
T_Barrie = Player('Tyson Barrie', 'COL', 'D', 80, 12, 41, 139, 90,80, 12, 41, 139,90)
M_Bartkowski = Player('Matt Bartkowski', 'BOS', 'D', 47, 0, 4, 67, 24,47, 0, 4, 67,24)
V_Bartley = Player('Victor Bartley', 'NSH', 'D', 37, 0, 10, 28, 53,37, 0, 10, 28,53)
K_Baun = Player('Kyle Baun', 'CHI', 'RW', 3, 0, 0, 4, 0,3, 0, 0, 4,0)
J_Beagle = Player('Jay Beagle', 'WSH', 'RW', 62, 10, 10, 84, 33,62, 10, 10, 84,33)
F_Beauchemin = Player('Francois Beauchemin', 'ANA', 'D', 64, 11, 12, 110, 107,64, 11, 12, 110,107)
N_Beaulieu = Player('Nathan Beaulieu', 'MTL', 'D', 64, 1, 8, 62, 69,64, 1, 8, 62,69)
T_Beck = Player('Taylor Beck', 'NSH', 'LW', 62, 8, 8, 78, 23,62, 8, 8, 78,23)
M_Beleskey = Player('Matt Beleskey', 'ANA', 'LW', 65, 22, 10, 145, 25,65, 22, 10, 145,25)
P_Bellemare = Player('Pierre-Edouard Bellemare', 'PHI', 'LW', 81, 6, 6, 113, 61,81, 6, 6, 113,61)
B_Bellemore = Player('Brett Bellemore', 'CAR', 'D', 49, 2, 8, 26, 54,49, 2, 8, 26,54)
J_Benn = Player('Jamie Benn', 'DAL', 'LW', 82, 35, 52, 253, 50,82, 35, 52, 253,50)
B_Bennett = Player('Beau Bennett', 'PIT', 'RW', 49, 4, 8, 81, 13,49, 4, 8, 81,13)
S_Bennett = Player('Sam Bennett', 'CGY', 'C', 1, 0, 1, 1, 0,1, 0, 1, 1,0)
A_Benoit = Player('Andre Benoit', 'BUF', 'D', 59, 1, 8, 45, 98,59, 1, 8, 45,98)
S_Bergenheim = Player('Sean Bergenheim', 'TOT', 'LW', 56, 9, 10, 108, 13,56, 9, 10, 108,13)
P_Bergeron = Player('Patrice Bergeron', 'BOS', 'C', 81, 23, 32, 234, 60,81, 23, 32, 234,60)
P_Berglund = Player('Patrik Berglund', 'STL', 'C', 77, 12, 15, 145, 26,77, 12, 15, 145,26)
S_Bernier = Player('Steve Bernier', 'NJD', 'RW', 67, 16, 16, 107, 48,67, 16, 16, 107,48)
S_Bickel = Player('Stu Bickel', 'MIN', 'D', 9, 0, 1, 3, 9,9, 0, 1, 3,9)
B_Bickell = Player('Bryan Bickell', 'CHI', 'LW', 80, 14, 14, 113, 13,80, 14, 14, 113,13)
A_Biega = Player('Alex Biega', 'VAN', 'D', 7, 1, 0, 7, 8,7, 1, 0, 7,8)
D_Biega = Player('Danny Biega', 'CAR', 'D', 10, 0, 2, 7, 7,10, 0, 2, 7,7)
K_Bieksa = Player('Kevin Bieksa', 'VAN', 'D', 60, 4, 10, 99, 93,60, 4, 10, 99,93)
A_Bitetto = Player('Anthony Bitetto', 'NSH', 'D', 7, 0, 0, 2, 3,7, 0, 0, 2,3)
N_Bjugstad = Player('Nick Bjugstad', 'FLA', 'C', 72, 24, 19, 207, 29,72, 24, 19, 207,29)
J_Blacker = Player('Jesse Blacker', 'ANA', 'D', 1, 0, 0, 0, 1,1, 0, 0, 0,1)
J_Blum = Player('Jonathon Blum', 'MIN', 'D', 4, 0, 1, 3, 2,4, 0, 1, 3,2)
M_Blunden = Player('Mike Blunden', 'TBL', 'RW', 2, 0, 0, 0, 0,2, 0, 0, 0,0)
T_Bodie = Player('Troy Bodie', 'TOR', 'RW', 5, 0, 0, 1, 0,5, 0, 0, 1,0)
M_Boedker = Player('Mikkel Boedker', 'ARI', 'LW', 45, 14, 14, 79, 9,45, 14, 14, 79,9)
Z_Bogosian = Player('Zach Bogosian', 'TOT', 'D', 62, 3, 17, 125, 90,62, 3, 17, 125,90)
A_Bolduc = Player('Alexandre Bolduc', 'ARI', 'C', 3, 0, 0, 3, 1,3, 0, 0, 3,1)
J_Boll = Player('Jared Boll', 'CBJ', 'RW', 72, 1, 4, 28, 17,72, 1, 4, 28,17)
D_Bolland = Player('Dave Bolland', 'FLA', 'C', 53, 6, 17, 76, 21,53, 6, 17, 76,21)
B_Bollig = Player('Brandon Bollig', 'CGY', 'LW', 62, 1, 4, 67, 24,62, 1, 4, 67,24)
N_Bonino = Player('Nick Bonino', 'VAN', 'C', 75, 15, 24, 149, 89,75, 15, 24, 149,89)
D_Booth = Player('David Booth', 'TOR', 'LW', 59, 7, 6, 107, 8,59, 7, 6, 107,8)
P_Bordeleau = Player('Patrick Bordeleau', 'COL', 'LW', 1, 0, 0, 0, 0,1, 0, 0, 0,0)
M_Borowiecki = Player('Mark Borowiecki', 'OTT', 'D', 63, 1, 10, 30, 102,63, 1, 10, 30,102)
R_Bortuzzo = Player('Robert Bortuzzo', 'TOT', 'D', 51, 3, 5, 56, 61,51, 3, 5, 56,61)
R_Boucher = Player('Reid Boucher', 'NJD', 'LW', 11, 1, 0, 20, 5,11, 1, 0, 20,5)
E_Boulton = Player('Eric Boulton', 'NYI', 'LW', 10, 2, 0, 9, 4,10, 2, 0, 9,4)
L_Bouma = Player('Lance Bouma', 'CGY', 'C', 78, 16, 18, 104, 82,78, 16, 18, 104,82)
M_Bournival = Player('Michael Bournival', 'MTL', 'LW', 29, 3, 2, 27, 10,29, 3, 2, 27,10)
G_Bourque = Player('Gabriel Bourque', 'NSH', 'LW', 69, 3, 10, 76, 44,69, 3, 10, 76,44)
R_Bourque = Player('Rene Bourque', 'TOT', 'RW', 51, 6, 8, 85, 11,51, 6, 8, 85,11)
R_Bourque = Player('Ryan Bourque', 'NYR', 'C', 1, 0, 0, 1, 0,1, 0, 0, 1,0)
J_Bouwmeester = Player('Jay Bouwmeester', 'STL', 'D', 72, 2, 11, 92, 99,72, 2, 11, 92,99)
D_Bowman = Player('Drayson Bowman', 'MTL', 'LW', 3, 0, 0, 0, 0,3, 0, 0, 0,0)
J_Boychuk = Player('Johnny Boychuk', 'NYI', 'D', 72, 9, 26, 192, 149,72, 9, 26, 192,149)
Z_Boychuk = Player('Zach Boychuk', 'CAR', 'LW', 31, 3, 3, 35, 9,31, 3, 3, 35,9)
B_Boyes = Player('Brad Boyes', 'FLA', 'RW', 78, 14, 24, 151, 38,78, 14, 24, 151,38)
B_Boyle = Player('Brian Boyle', 'TBL', 'C', 82, 15, 9, 140, 63,82, 15, 9, 140,63)
D_Boyle = Player('Dan Boyle', 'NYR', 'D', 65, 9, 11, 116, 79,65, 9, 11, 116,79)
T_Bozak = Player('Tyler Bozak', 'TOR', 'C', 82, 23, 26, 154, 46,82, 23, 26, 154,46)
D_Brassard = Player('Derick Brassard', 'NYR', 'C', 80, 19, 41, 168, 13,80, 19, 41, 168,13)
J_Braun = Player('Justin Braun', 'SJS', 'D', 70, 1, 22, 94, 130,70, 1, 22, 94,130)
T_Brennan = Player('T.J. Brennan', 'TOR', 'D', 6, 0, 1, 11, 5,6, 0, 1, 11,5)
E_Brewer = Player('Eric Brewer', 'TOT', 'D', 44, 3, 8, 33, 72,44, 3, 8, 33,72)
D_Briere = Player('Daniel Briere', 'COL', 'C', 57, 8, 4, 69, 9,57, 8, 4, 69,9)
T_Brodie = Player('T.J. Brodie', 'CGY', 'D', 81, 11, 30, 133, 178,81, 11, 30, 133,178)
J_Brodin = Player('Jonas Brodin', 'MIN', 'D', 71, 3, 14, 95, 128,71, 3, 14, 95,128)
K_Brodziak = Player('Kyle Brodziak', 'MIN', 'C', 73, 9, 11, 86, 63,73, 9, 11, 86,63)
J_Brouillette = Player('Julien Brouillette', 'WPG', 'D', 1, 0, 0, 0, 1,1, 0, 0, 0,1)
T_Brouwer = Player('Troy Brouwer', 'WSH', 'RW', 82, 21, 22, 145, 39,82, 21, 22, 145,39)
C_Brown = Player('Chris Brown', 'WSH', 'C', 5, 1, 0, 4, 1,5, 1, 0, 4,1)
D_Brown = Player('Dustin Brown', 'LAK', 'RW', 82, 11, 16, 189, 23,82, 11, 16, 189,23)
J_Brown = Player('J.T. Brown', 'TBL', 'RW', 52, 3, 6, 74, 21,52, 3, 6, 74,21)
M_Brown = Player('Mike Brown', 'SJS', 'RW', 12, 0, 0, 11, 7,12, 0, 0, 11,7)
P_Brown = Player('Patrick Brown', 'CAR', 'C', 7, 0, 0, 4, 2,7, 0, 0, 4,2)
D_Brunner = Player('Damien Brunner', 'NJD', 'C', 17, 2, 5, 29, 3,17, 2, 5, 29,3)
A_Burakovsky = Player('Andre Burakovsky', 'WSH', 'LW', 53, 9, 13, 65, 18,53, 9, 13, 65,18)
A_Burish = Player('Adam Burish', 'SJS', 'RW', 20, 1, 2, 22, 19,20, 1, 2, 22,19)
B_Burns = Player('Brent Burns', 'SJS', 'D', 82, 17, 43, 245, 124,82, 17, 43, 245,124)
A_Burrows = Player('Alexandre Burrows', 'VAN', 'RW', 70, 18, 15, 145, 33,70, 18, 15, 145,33)
C_Butler = Player('Chris Butler', 'STL', 'D', 33, 3, 6, 54, 38,33, 3, 6, 54,38)
D_Byfuglien = Player('Dustin Byfuglien', 'WPG', 'D', 69, 18, 27, 209, 60,69, 18, 27, 209,60)
P_Byron = Player('Paul Byron', 'CGY', 'C', 57, 6, 13, 62, 24,57, 6, 13, 62,24)
R_Callahan = Player('Ryan Callahan', 'TBL', 'RW', 77, 24, 30, 191, 48,77, 24, 30, 191,48)
M_Calvert = Player('Matt Calvert', 'CBJ', 'LW', 56, 13, 10, 93, 20,56, 13, 10, 93,20)
M_Cammalleri = Player('Mike Cammalleri', 'NJD', 'LW', 68, 27, 15, 156, 19,68, 27, 15, 156,19)
A_Campbell = Player('Andrew Campbell', 'ARI', 'D', 33, 0, 1, 28, 58,33, 0, 1, 28,58)
B_Campbell = Player('Brian Campbell', 'FLA', 'D', 82, 3, 24, 118, 85,82, 3, 24, 118,85)
G_Campbell = Player('Gregory Campbell', 'BOS', 'C', 70, 6, 6, 64, 41,70, 6, 6, 64,41)
D_Carcillo = Player('Daniel Carcillo', 'CHI', 'LW', 39, 4, 4, 42, 7,39, 4, 4, 42,7)
P_Carey = Player('Paul Carey', 'COL', 'C', 10, 0, 1, 5, 2,10, 0, 1, 5,2)
M_Carle = Player('Matt Carle', 'TBL', 'D', 59, 4, 14, 73, 109,59, 4, 14, 73,109)
J_Carlson = Player('John Carlson', 'WSH', 'D', 82, 12, 43, 193, 200,82, 12, 43, 193,200)
J_Caron = Player('Jordan Caron', 'TOT', 'RW', 30, 0, 0, 12, 8,30, 0, 0, 12,8)
S_Carrick = Player('Sam Carrick', 'TOR', 'C', 16, 1, 1, 17, 1,16, 1, 1, 17,1)
J_Carter = Player('Jeff Carter', 'LAK', 'C', 82, 28, 34, 218, 32,82, 28, 34, 218,32)
R_Carter = Player('Ryan Carter', 'MIN', 'C', 53, 3, 10, 47, 30,53, 3, 10, 47,30)
C_Ceci = Player('Cody Ceci', 'OTT', 'D', 81, 5, 16, 130, 113,81, 5, 16, 130,113)
M_Chaput = Player('Michael Chaput', 'CBJ', 'C', 33, 1, 4, 23, 20,33, 1, 4, 23,20)
Z_Chara = Player('Zdeno Chara', 'BOS', 'D', 63, 8, 12, 138, 99,63, 8, 12, 138,99)
B_Chiarot = Player('Ben Chiarot', 'WPG', 'D', 40, 2, 6, 37, 52,40, 2, 6, 37,52)
A_Chiasson = Player('Alex Chiasson', 'OTT', 'RW', 76, 11, 15, 105, 20,76, 11, 15, 105,20)
J_Chimera = Player('Jason Chimera', 'WSH', 'LW', 77, 7, 12, 96, 18,77, 7, 12, 96,18)
K_Chipchura = Player('Kyle Chipchura', 'ARI', 'C', 70, 4, 10, 81, 29,70, 4, 10, 81,29)
T_Chorney = Player('Taylor Chorney', 'PIT', 'D', 7, 0, 0, 4, 3,7, 0, 0, 4,3)
C_Cizikas = Player('Casey Cizikas', 'NYI', 'C', 70, 9, 9, 90, 50,70, 9, 9, 90,50)
M_Clark = Player('Mat Clark', 'ANA', 'D', 7, 0, 1, 2, 5,7, 0, 1, 2,5)
D_Clarkson = Player('David Clarkson', 'TOT', 'RW', 61, 10, 5, 95, 19,61, 10, 5, 95,19)
D_Cleary = Player('Dan Cleary', 'DET', 'RW', 17, 1, 1, 17, 9,17, 1, 1, 17,9)
A_Clendening = Player('Adam Clendening', 'TOT', 'D', 21, 1, 3, 17, 22,21, 1, 3, 17,22)
M_Cliche = Player('Marc-Andre Cliche', 'COL', 'C', 74, 2, 5, 68, 28,74, 2, 5, 68,28)
K_Clifford = Player('Kyle Clifford', 'LAK', 'LW', 80, 6, 9, 117, 14,80, 6, 9, 117,14)
G_Clitsome = Player('Grant Clitsome', 'WPG', 'D', 24, 0, 4, 22, 20,24, 0, 4, 22,20)
R_Clowe = Player('Ryane Clowe', 'NJD', 'LW', 13, 1, 3, 15, 1,13, 1, 3, 15,1)
R_Clune = Player('Rich Clune', 'NSH', 'LW', 1, 0, 0, 0, 0,1, 0, 0, 0,0)
C_Clutterbuck = Player('Cal Clutterbuck', 'NYI', 'RW', 76, 7, 9, 124, 31,76, 7, 9, 124,31)
B_Coburn = Player('Braydon Coburn', 'TOT', 'D', 43, 1, 10, 46, 66,43, 1, 10, 46,66)
A_Cogliano = Player('Andrew Cogliano', 'ANA', 'C', 82, 15, 14, 134, 30,82, 15, 14, 134,30)
C_Colaiacovo = Player('Carlo Colaiacovo', 'PHI', 'D', 33, 2, 6, 42, 33,33, 2, 6, 42,33)
J_Colborne = Player('Joe Colborne', 'CGY', 'C', 64, 8, 20, 67, 36,64, 8, 20, 67,36)
E_Cole = Player('Erik Cole', 'TOT', 'LW', 68, 21, 18, 122, 20,68, 21, 18, 122,20)
I_Cole = Player('Ian Cole', 'TOT', 'D', 74, 5, 12, 83, 99,74, 5, 12, 83,99)
S_Collins = Player('Sean Collins', 'CBJ', 'C', 8, 0, 2, 4, 0,8, 0, 2, 4,0)
B_Comeau = Player('Blake Comeau', 'PIT', 'LW', 61, 16, 15, 147, 11,61, 16, 15, 147,11)
C_Conacher = Player('Cory Conacher', 'NYI', 'C', 15, 1, 2, 23, 7,15, 1, 2, 23,7)
E_Condra = Player('Erik Condra', 'OTT', 'RW', 68, 9, 14, 106, 53,68, 9, 14, 106,53)
K_Connauton = Player('Kevin Connauton', 'TOT', 'D', 62, 9, 12, 96, 48,62, 9, 12, 96,48)
C_Conner = Player('Chris Conner', 'WSH', 'RW', 2, 0, 0, 3, 0,2, 0, 0, 3,0)
B_Connolly = Player('Brett Connolly', 'TOT', 'RW', 55, 12, 5, 83, 13,55, 12, 5, 83,13)
M_Cooke = Player('Matt Cooke', 'MIN', 'LW', 29, 4, 6, 24, 22,29, 4, 6, 24,22)
A_Copp = Player('Andrew Copp', 'WPG', 'C', 1, 0, 1, 4, 0,1, 0, 1, 4,0)
P_Cormier = Player('Patrice Cormier', 'WPG', 'C', 1, 0, 0, 0, 0,1, 0, 0, 0,0)
F_Corrado = Player('Frank Corrado', 'VAN', 'D', 10, 1, 0, 8, 12,10, 1, 0, 8,12)
N_Cousins = Player('Nick Cousins', 'PHI', 'C', 11, 0, 0, 6, 5,11, 0, 0, 6,5)
L_Couture = Player('Logan Couture', 'SJS', 'C', 82, 27, 40, 263, 64,82, 27, 40, 263,64)
S_Couturier = Player('Sean Couturier', 'PHI', 'C', 82, 15, 22, 148, 35,82, 15, 22, 148,35)
J_Cowen = Player('Jared Cowen', 'OTT', 'D', 54, 3, 6, 47, 76,54, 3, 6, 47,76)
C_Coyle = Player('Charlie Coyle', 'MIN', 'C', 82, 11, 24, 120, 52,82, 11, 24, 120,52)
A_Cracknell = Player('Adam Cracknell', 'CBJ', 'RW', 17, 0, 1, 17, 6,17, 0, 1, 17,6)
R_Craig = Player('Ryan Craig', 'CBJ', 'C', 2, 0, 0, 2, 0,2, 0, 0, 2,0)
B_Crombeen = Player('B.J. Crombeen', 'ARI', 'RW', 58, 3, 3, 43, 12,58, 3, 3, 43,12)
S_Crosby = Player('Sidney Crosby', 'PIT', 'C', 77, 28, 56, 237, 29,77, 28, 56, 237,29)
M_Cullen = Player('Matt Cullen', 'NSH', 'C', 62, 7, 18, 90, 18,62, 7, 18, 90,18)
K_Cumiskey = Player('Kyle Cumiskey', 'CHI', 'D', 7, 0, 0, 5, 11,7, 0, 0, 5,11)
C_Cunningham = Player('Craig Cunningham', 'TOT', 'RW', 51, 3, 4, 54, 31,51, 3, 4, 54,31)
J_DAmigo = Player("Jerry D'Amigo", 'BUF', 'RW', 9, 0, 0, 7, 7,9, 0, 0, 7,7)
K_Dahlbeck = Player('Klas Dahlbeck', 'TOT', 'D', 23, 1, 3, 20, 46,23, 1, 3, 20,46)
T_Daley = Player('Trevor Daley', 'DAL', 'D', 68, 16, 22, 113, 123,68, 16, 22, 113,123)
Z_Dalpe = Player('Zac Dalpe', 'BUF', 'C', 21, 1, 2, 29, 8,21, 1, 2, 29,8)
P_Danault = Player('Phillip Danault', 'CHI', 'C', 2, 0, 0, 2, 0,2, 0, 0, 2,0)
P_Datsyuk = Player('Pavel Datsyuk', 'DET', 'C', 63, 26, 39, 165, 28,63, 26, 39, 165,28)
B_Davidson = Player('Brandon Davidson', 'EDM', 'D', 12, 1, 0, 7, 22,12, 1, 0, 7,22)
C_Haan = Player('Calvin de Haan', 'NYI', 'D', 65, 1, 11, 92, 130,65, 1, 11, 92,130)
J_Rose = Player('Jacob de La Rose', 'MTL', 'LW', 33, 4, 2, 38, 24,33, 4, 2, 38,24)
B_DeFazio = Player('Brandon DeFazio', 'VAN', 'LW', 2, 0, 0, 2, 0,2, 0, 0, 2,0)
D_DeKeyser = Player('Danny DeKeyser', 'DET', 'D', 80, 2, 29, 89, 88,80, 2, 29, 89,88)
M_Zotto = Player('Michael Del Zotto', 'PHI', 'D', 64, 10, 22, 119, 128,64, 10, 22, 119,128)
J_Demers = Player('Jason Demers', 'TOT', 'D', 81, 5, 20, 99, 85,81, 5, 20, 99,85)
D_Desharnais = Player('David Desharnais', 'MTL', 'C', 82, 14, 34, 90, 49,82, 14, 34, 90,49)
A_Desjardins = Player('Andrew Desjardins', 'TOT', 'C', 69, 5, 5, 59, 33,69, 5, 5, 59,33)
N_Deslauriers = Player('Nicolas Deslauriers', 'BUF', 'LW', 82, 5, 10, 76, 36,82, 5, 10, 76,36)
S_Despres = Player('Simon Despres', 'TOT', 'D', 75, 3, 20, 103, 101,75, 3, 20, 103,101)
R_Diaz = Player('Raphael Diaz', 'CGY', 'D', 56, 2, 2, 52, 67,56, 2, 2, 52,67)
B_Dillon = Player('Brenden Dillon', 'TOT', 'D', 80, 2, 8, 91, 139,80, 2, 8, 91,139)
S_Doan = Player('Shane Doan', 'ARI', 'RW', 79, 14, 22, 189, 26,79, 14, 22, 189,26)
M_Donovan = Player('Matt Donovan', 'NYI', 'D', 12, 0, 3, 12, 16,12, 0, 3, 12,16)
D_Dorsett = Player('Derek Dorsett', 'VAN', 'RW', 79, 7, 18, 89, 37,79, 7, 18, 89,37)
D_Doughty = Player('Drew Doughty', 'LAK', 'D', 82, 7, 39, 219, 144,82, 7, 39, 219,144)
S_Downie = Player('Steve Downie', 'PIT', 'RW', 72, 14, 14, 104, 34,72, 14, 14, 104,34)
L_Draisaitl = Player('Leon Draisaitl', 'EDM', 'C', 37, 2, 7, 49, 8,37, 2, 7, 49,8)
J_Drouin = Player('Jonathan Drouin', 'TBL', 'LW', 70, 4, 28, 76, 17,70, 4, 28, 76,17)
B_Dubinsky = Player('Brandon Dubinsky', 'CBJ', 'C', 47, 13, 23, 100, 11,47, 13, 23, 100,11)
M_Duchene = Player('Matt Duchene', 'COL', 'C', 82, 21, 34, 207, 74,82, 21, 34, 207,74)
A_Duclair = Player('Anthony Duclair', 'NYR', 'LW', 18, 1, 6, 18, 5,18, 1, 6, 18,5)
M_Dumba = Player('Mathew Dumba', 'MIN', 'D', 58, 8, 8, 86, 51,58, 8, 8, 86,51)
G_Dumont = Player('Gabriel Dumont', 'MTL', 'C', 3, 0, 0, 4, 2,3, 0, 0, 4,2)
B_Dumoulin = Player('Brian Dumoulin', 'PIT', 'D', 8, 1, 0, 4, 9,8, 1, 0, 4,9)
P_Dupuis = Player('Pascal Dupuis', 'PIT', 'RW', 16, 6, 5, 44, 8,16, 6, 5, 44,8)
P_Dwyer = Player('Patrick Dwyer', 'CAR', 'RW', 71, 5, 7, 77, 38,71, 5, 7, 77,38)
C_Eakin = Player('Cody Eakin', 'DAL', 'C', 78, 19, 21, 142, 59,78, 19, 21, 142,59)
P_Eaves = Player('Patrick Eaves', 'DAL', 'RW', 47, 14, 13, 91, 27,47, 14, 13, 91,27)
A_Ebbett = Player('Andrew Ebbett', 'PIT', 'C', 24, 1, 5, 21, 12,24, 1, 5, 21,12)
J_Eberle = Player('Jordan Eberle', 'EDM', 'RW', 81, 24, 39, 183, 36,81, 24, 39, 183,36)
A_Edler = Player('Alexander Edler', 'VAN', 'D', 74, 8, 23, 175, 126,74, 8, 23, 175,126)
C_Ehrhoff = Player('Christian Ehrhoff', 'PIT', 'D', 49, 3, 11, 110, 49,49, 3, 11, 110,49)
A_Ekblad = Player('Aaron Ekblad', 'FLA', 'D', 81, 12, 27, 170, 80,81, 12, 27, 170,80)
M_Ekholm = Player('Mattias Ekholm', 'NSH', 'D', 80, 7, 11, 86, 102,80, 7, 11, 86,102)
O_Ekman_Larsson = Player('Oliver Ekman-Larsson', 'ARI', 'D', 82, 23, 20, 264, 77,82, 23, 20, 264,77)
P_Elias = Player('Patrik Elias', 'NJD', 'C', 69, 13, 21, 114, 25,69, 13, 21, 114,25)
L_Eller = Player('Lars Eller', 'MTL', 'C', 77, 15, 12, 150, 37,77, 15, 12, 150,37)
K_Ellerby = Player('Keaton Ellerby', 'WPG', 'D', 1, 0, 1, 0, 2,1, 0, 1, 0,2)
S_Elliott = Player('Stefan Elliott', 'COL', 'D', 5, 0, 0, 10, 5,5, 0, 0, 10,5)
M_Ellis = Player('Matt Ellis', 'BUF', 'LW', 39, 1, 1, 29, 16,39, 1, 1, 29,16)
R_Ellis = Player('Ryan Ellis', 'NSH', 'D', 58, 9, 18, 118, 74,58, 9, 18, 118,74)
A_Emelin = Player('Alexei Emelin', 'MTL', 'D', 68, 3, 11, 43, 116,68, 3, 11, 43,116)
D_Engelland = Player('Deryk Engelland', 'CGY', 'D', 76, 2, 9, 51, 142,76, 2, 9, 51,142)
T_Ennis = Player('Tyler Ennis', 'BUF', 'C', 78, 20, 26, 185, 35,78, 20, 26, 185,35)
T_Enstrom = Player('Toby Enstrom', 'WPG', 'D', 60, 4, 19, 58, 93,60, 4, 19, 58,93)
M_Erat = Player('Martin Erat', 'ARI', 'RW', 79, 9, 23, 91, 25,79, 9, 23, 91,25)
J_Ericsson = Player('Jonathan Ericsson', 'DET', 'D', 82, 3, 12, 82, 55,82, 3, 12, 82,55)
L_Eriksson = Player('Loui Eriksson', 'BOS', 'RW', 81, 22, 25, 169, 23,81, 22, 25, 169,23)
T_Erixon = Player('Tim Erixon', 'TOT', 'D', 42, 2, 5, 36, 32,42, 2, 5, 36,32)
E_Etem = Player('Emerson Etem', 'ANA', 'LW', 45, 5, 5, 77, 20,45, 5, 5, 77,20)
D_Everberg = Player('Dennis Everberg', 'COL', 'RW', 55, 3, 9, 62, 41,55, 3, 9, 62,41)
J_Falk = Player('Justin Falk', 'TOT', 'D', 18, 1, 1, 18, 19,18, 1, 1, 18,19)
B_Farnham = Player('Bobby Farnham', 'PIT', 'RW', 11, 0, 0, 6, 2,11, 0, 0, 6,2)
J_Fast = Player('Jesper Fast', 'NYR', 'RW', 58, 6, 8, 52, 28,58, 6, 8, 52,28)
J_Faulk = Player('Justin Faulk', 'CAR', 'D', 82, 15, 34, 238, 114,82, 15, 34, 238,114)
M_Fayne = Player('Mark Fayne', 'EDM', 'D', 74, 2, 6, 78, 125,74, 2, 6, 78,125)
T_Fedun = Player('Taylor Fedun', 'SJS', 'D', 7, 0, 4, 12, 8,7, 0, 4, 12,8)
E_Fehr = Player('Eric Fehr', 'WSH', 'RW', 75, 19, 14, 142, 47,75, 19, 14, 142,47)
A_Ference = Player('Andrew Ference', 'EDM', 'D', 70, 3, 11, 58, 86,70, 3, 11, 58,86)
M_Ferland = Player('Micheal Ferland', 'CGY', 'LW', 26, 2, 3, 34, 11,26, 2, 3, 34,11)
B_Ferlin = Player('Brian Ferlin', 'BOS', 'RW', 7, 0, 1, 6, 0,7, 0, 1, 6,0)
L_Ferraro = Player('Landon Ferraro', 'DET', 'C', 3, 1, 0, 4, 3,3, 1, 0, 4,3)
K_Fiala = Player('Kevin Fiala', 'NSH', 'LW', 1, 0, 0, 3, 1,1, 0, 0, 3,1)
V_Fiddler = Player('Vernon Fiddler', 'DAL', 'C', 80, 13, 16, 132, 61,80, 13, 16, 132,61)
V_Filppula = Player('Valtteri Filppula', 'TBL', 'C', 82, 12, 36, 91, 27,82, 12, 36, 91,27)
M_Fisher = Player('Mike Fisher', 'NSH', 'C', 59, 19, 20, 111, 60,59, 19, 20, 111,60)
M_Fistric = Player('Mark Fistric', 'ANA', 'D', 9, 0, 0, 1, 21,9, 0, 0, 1,21)
T_Fleischmann = Player('Tomas Fleischmann', 'TOT', 'LW', 66, 8, 19, 131, 15,66, 8, 19, 131,15)
B_Flynn = Player('Brian Flynn', 'TOT', 'C', 63, 5, 12, 82, 46,63, 5, 12, 82,46)
M_Foligno = Player('Marcus Foligno', 'BUF', 'LW', 57, 8, 12, 66, 48,57, 8, 12, 66,48)
N_Foligno = Player('Nick Foligno', 'CBJ', 'LW', 79, 31, 42, 182, 52,79, 31, 42, 182,52)
C_Folin = Player('Christian Folin', 'MIN', 'D', 40, 2, 8, 39, 42,40, 2, 8, 39,42)
J_Fontaine = Player('Justin Fontaine', 'MIN', 'RW', 71, 9, 22, 104, 27,71, 9, 22, 104,27)
F_Forsberg = Player('Filip Forsberg', 'NSH', 'C', 82, 26, 37, 237, 28,82, 26, 37, 237,28)
C_Fowler = Player('Cam Fowler', 'ANA', 'D', 80, 7, 27, 87, 107,80, 7, 27, 87,107)
C_Franson = Player('Cody Franson', 'TOT', 'D', 78, 7, 29, 127, 132,78, 7, 29, 127,132)
J_Franzen = Player('Johan Franzen', 'DET', 'C', 33, 7, 15, 74, 13,33, 7, 15, 74,13)
C_Fraser = Player('Colin Fraser', 'STL', 'C', 1, 0, 0, 1, 1,1, 0, 0, 1,1)
M_Fraser = Player('Mark Fraser', 'NJD', 'D', 34, 0, 4, 19, 51,34, 0, 4, 19,51)
M_Fraser = Player('Matt Fraser', 'TOT', 'RW', 60, 8, 4, 92, 20,60, 8, 4, 92,20)
M_Frattin = Player('Matt Frattin', 'TOR', 'RW', 9, 0, 0, 6, 4,9, 0, 0, 6,4)
M_Friberg = Player('Max Friberg', 'ANA', 'LW', 1, 0, 0, 0, 0,1, 0, 0, 0,0)
M_Frolik = Player('Michael Frolik', 'WPG', 'RW', 82, 19, 23, 206, 42,82, 19, 23, 206,42)
M_Gaborik = Player('Marian Gaborik', 'LAK', 'RW', 69, 27, 20, 174, 6,69, 27, 20, 174,6)
S_Gagne = Player('Simon Gagne', 'BOS', 'LW', 23, 3, 1, 27, 7,23, 3, 1, 27,7)
S_Gagner = Player('Sam Gagner', 'ARI', 'C', 81, 15, 26, 183, 19,81, 15, 26, 183,19)
A_Galchenyuk = Player('Alex Galchenyuk', 'MTL', 'C', 80, 20, 26, 163, 44,80, 20, 26, 163,44)
T_Galiardi = Player('T.J. Galiardi', 'WPG', 'LW', 38, 1, 0, 35, 14,38, 1, 0, 35,14)
S_Galiev = Player('Stanislav Galiev', 'WSH', 'RW', 2, 1, 0, 2, 0,2, 1, 0, 2,0)
B_Gallagher = Player('Brendan Gallagher', 'MTL', 'RW', 82, 24, 23, 254, 49,82, 24, 23, 254,49)
R_Garbutt = Player('Ryan Garbutt', 'DAL', 'LW', 67, 8, 17, 143, 48,67, 8, 17, 143,48)
J_Gardiner = Player('Jake Gardiner', 'TOR', 'D', 79, 4, 20, 100, 83,79, 4, 20, 100,83)
J_Garrison = Player('Jason Garrison', 'TBL', 'D', 70, 4, 26, 111, 94,70, 4, 26, 111,94)
T_Gaudet = Player('Tyler Gaudet', 'ARI', 'C', 2, 0, 0, 1, 1,2, 0, 0, 1,1)
J_Gaudreau = Player('John Gaudreau', 'CGY', 'LW', 80, 24, 40, 167, 27,80, 24, 40, 167,27)
P_Gaustad = Player('Paul Gaustad', 'NSH', 'C', 73, 4, 10, 54, 58,73, 4, 10, 54,58)
L_Gazdic = Player('Luke Gazdic', 'EDM', 'LW', 40, 2, 1, 26, 15,40, 2, 1, 26,15)
E_Gelinas = Player('Eric Gelinas', 'NJD', 'D', 61, 6, 13, 112, 50,61, 6, 13, 112,50)
N_Gerbe = Player('Nathan Gerbe', 'CAR', 'LW', 78, 10, 18, 235, 23,78, 10, 18, 235,23)
R_Getzlaf = Player('Ryan Getzlaf', 'ANA', 'C', 77, 25, 45, 191, 95,77, 25, 45, 191,95)
B_Gibbons = Player('Brian Gibbons', 'CBJ', 'C', 25, 0, 5, 21, 17,25, 0, 5, 21,17)
T_Gilbert = Player('Tom Gilbert', 'MTL', 'D', 72, 4, 8, 70, 164,72, 4, 8, 70,164)
B_Gionta = Player('Brian Gionta', 'BUF', 'RW', 69, 13, 22, 153, 31,69, 13, 22, 153,31)
S_Gionta = Player('Stephen Gionta', 'NJD', 'RW', 61, 5, 8, 84, 41,61, 5, 8, 84,41)
M_Giordano = Player('Mark Giordano', 'CGY', 'D', 61, 11, 37, 157, 128,61, 11, 37, 157,128)
D_Girardi = Player('Dan Girardi', 'NYR', 'D', 82, 4, 16, 111, 184,82, 4, 16, 111,184)
Z_Girgensons = Player('Zemgus Girgensons', 'BUF', 'C', 61, 15, 15, 115, 62,61, 15, 15, 115,62)
C_Giroux = Player('Claude Giroux', 'PHI', 'C', 81, 25, 48, 279, 28,81, 25, 48, 279,28)
T_Glass = Player('Tanner Glass', 'NYR', 'LW', 66, 1, 5, 53, 32,66, 1, 5, 53,32)
T_Gleason = Player('Tim Gleason', 'TOT', 'D', 72, 1, 8, 54, 108,72, 1, 8, 54,108)
C_Glencross = Player('Curtis Glencross', 'TOT', 'LW', 71, 13, 22, 108, 50,71, 13, 22, 108,50)
L_Glendening = Player('Luke Glendening', 'DET', 'C', 82, 12, 6, 104, 73,82, 12, 6, 104,73)
M_Goc = Player('Marcel Goc', 'TOT', 'C', 74, 3, 6, 77, 35,74, 3, 6, 77,35)
A_Goligoski = Player('Alex Goligoski', 'DAL', 'D', 81, 4, 32, 122, 157,81, 4, 32, 122,157)
C_Goloubef = Player('Cody Goloubef', 'CBJ', 'D', 36, 0, 9, 23, 32,36, 0, 9, 23,32)
S_Gomez = Player('Scott Gomez', 'NJD', 'C', 58, 7, 27, 70, 15,58, 7, 27, 70,15)
S_Gonchar = Player('Sergei Gonchar', 'TOT', 'D', 48, 1, 13, 46, 71,48, 1, 13, 46,71)
B_Goodrow = Player('Barclay Goodrow', 'SJS', 'RW', 60, 4, 8, 68, 24,60, 4, 8, 68,24)
B_Gordon = Player('Boyd Gordon', 'EDM', 'C', 68, 6, 7, 65, 80,68, 6, 7, 65,80)
J_Gorges = Player('Josh Gorges', 'BUF', 'D', 46, 0, 6, 28, 148,46, 0, 6, 28,148)
B_Gormley = Player('Brandon Gormley', 'ARI', 'D', 27, 2, 2, 39, 32,27, 2, 2, 39,32)
S_Gostisbehere = Player('Shayne Gostisbehere', 'PHI', 'D', 2, 0, 0, 2, 1,2, 0, 0, 2,1)
M_Grabner = Player('Michael Grabner', 'NYI', 'RW', 34, 8, 5, 63, 21,34, 8, 5, 63,21)
M_Grabovski = Player('Mikhail Grabovski', 'NYI', 'C', 51, 9, 10, 81, 19,51, 9, 10, 81,19)
P_Granberg = Player('Petter Granberg', 'TOR', 'D', 7, 0, 0, 1, 7,7, 0, 0, 1,7)
M_Granlund = Player('Markus Granlund', 'CGY', 'C', 48, 8, 10, 65, 25,48, 8, 10, 65,25)
M_Granlund = Player('Mikael Granlund', 'MIN', 'C', 68, 8, 31, 99, 45,68, 8, 31, 99,45)
T_Graovac = Player('Tyler Graovac', 'MIN', 'C', 3, 0, 0, 4, 2,3, 0, 0, 4,2)
M_Green = Player('Mike Green', 'WSH', 'D', 72, 10, 35, 159, 93,72, 10, 35, 159,93)
A_Greene = Player('Andy Greene', 'NJD', 'D', 82, 3, 19, 83, 173,82, 3, 19, 83,173)
M_Greene = Player('Matt Greene', 'LAK', 'D', 82, 3, 6, 69, 129,82, 3, 6, 69,129)
C_Greening = Player('Colin Greening', 'OTT', 'LW', 26, 1, 0, 39, 14,26, 1, 0, 39,14)
S_Griffith = Player('Seth Griffith', 'BOS', 'C', 30, 6, 4, 33, 13,30, 6, 4, 33,13)
M_Grigorenko = Player('Mikhail Grigorenko', 'BUF', 'C', 25, 3, 3, 35, 15,25, 3, 3, 35,15)
R_Grimaldi = Player('Rocco Grimaldi', 'FLA', 'C', 7, 1, 0, 18, 1,7, 1, 0, 18,1)
N_Grossmann = Player('Nicklas Grossmann', 'PHI', 'D', 68, 5, 9, 43, 89,68, 5, 9, 43,89)
E_Gryba = Player('Eric Gryba', 'OTT', 'D', 75, 0, 12, 64, 58,75, 0, 12, 64,58)
R_Gudas = Player('Radko Gudas', 'TBL', 'D', 31, 2, 3, 63, 63,31, 2, 3, 63,63)
E_Gudbranson = Player('Erik Gudbranson', 'FLA', 'D', 76, 4, 9, 110, 75,76, 4, 9, 110,75)
N_Guenin = Player('Nate Guenin', 'COL', 'D', 76, 2, 13, 38, 162,76, 2, 13, 38,162)
C_Gunnarsson = Player('Carl Gunnarsson', 'STL', 'D', 61, 2, 10, 54, 114,61, 2, 10, 54,114)
C_Hagelin = Player('Carl Hagelin', 'NYR', 'LW', 82, 17, 18, 185, 36,82, 17, 18, 185,36)
R_Hainsey = Player('Ron Hainsey', 'CAR', 'D', 81, 2, 8, 83, 120,81, 2, 8, 83,120)
M_Haley = Player('Micheal Haley', 'SJS', 'C', 4, 0, 0, 1, 1,4, 0, 0, 1,1)
M_Halischuk = Player('Matt Halischuk', 'WPG', 'RW', 47, 3, 5, 59, 25,47, 3, 5, 59,25)
T_Hall = Player('Taylor Hall', 'EDM', 'LW', 53, 14, 24, 158, 37,53, 14, 24, 158,37)
D_Hamhuis = Player('Dan Hamhuis', 'VAN', 'D', 59, 1, 22, 82, 71,59, 1, 22, 82,71)
C_Hamilton = Player('Curtis Hamilton', 'EDM', 'LW', 1, 0, 0, 0, 1,1, 0, 0, 0,1)
D_Hamilton = Player('Dougie Hamilton', 'BOS', 'D', 72, 10, 32, 188, 53,72, 10, 32, 188,53)
F_Hamilton = Player('Freddie Hamilton', 'TOT', 'C', 18, 1, 0, 11, 3,18, 1, 0, 11,3)
R_Hamilton = Player('Ryan Hamilton', 'EDM', 'LW', 16, 1, 1, 12, 13,16, 1, 1, 12,13)
T_Hamonic = Player('Travis Hamonic', 'NYI', 'D', 71, 5, 28, 132, 131,71, 5, 28, 132,131)
S_Hannan = Player('Scott Hannan', 'SJS', 'D', 58, 2, 5, 53, 69,58, 2, 5, 53,69)
J_Hansen = Player('Jannik Hansen', 'VAN', 'RW', 81, 16, 17, 145, 30,81, 16, 17, 145,30)
M_Hanzal = Player('Martin Hanzal', 'ARI', 'C', 37, 8, 16, 85, 18,37, 8, 16, 85,18)
S_Harrington = Player('Scott Harrington', 'PIT', 'D', 10, 0, 0, 9, 10,10, 0, 0, 9,10)
J_Harrison = Player('Jay Harrison', 'TOT', 'D', 55, 3, 6, 50, 76,55, 3, 6, 50,76)
P_Harrold = Player('Peter Harrold', 'NJD', 'D', 43, 3, 2, 31, 39,43, 3, 2, 31,39)
R_Hartman = Player('Ryan Hartman', 'CHI', 'RW', 5, 0, 0, 8, 2,5, 0, 0, 8,2)
S_Hartnell = Player('Scott Hartnell', 'CBJ', 'LW', 77, 28, 32, 204, 38,77, 28, 32, 204,38)
E_Haula = Player('Erik Haula', 'MIN', 'C', 72, 7, 7, 92, 42,72, 7, 7, 92,42)
M_Havlat = Player('Martin Havlat', 'NJD', 'RW', 40, 5, 9, 49, 11,40, 5, 9, 49,11)
E_Hayes = Player('Eriah Hayes', 'SJS', 'RW', 4, 0, 0, 10, 4,4, 0, 0, 10,4)
J_Hayes = Player('Jimmy Hayes', 'FLA', 'RW', 72, 19, 16, 166, 12,72, 19, 16, 166,12)
K_Hayes = Player('Kevin Hayes', 'NYR', 'RW', 79, 17, 28, 111, 33,79, 17, 28, 111,33)
D_Heatley = Player('Dany Heatley', 'ANA', 'LW', 6, 0, 0, 8, 3,6, 0, 0, 8,3)
V_Hedman = Player('Victor Hedman', 'TBL', 'D', 59, 10, 28, 115, 111,59, 10, 28, 115,111)
J_Hejda = Player('Jan Hejda', 'COL', 'D', 81, 1, 12, 84, 140,81, 1, 12, 84,140)
S_Helgeson = Player('Seth Helgeson', 'NJD', 'D', 22, 0, 2, 11, 20,22, 0, 2, 11,20)
D_Helm = Player('Darren Helm', 'DET', 'C', 75, 15, 18, 160, 25,75, 15, 18, 160,25)
A_Hemsky = Player('Ales Hemsky', 'DAL', 'RW', 76, 11, 21, 140, 35,76, 11, 21, 140,35)
M_Hendricks = Player('Matt Hendricks', 'EDM', 'LW', 71, 8, 8, 103, 72,71, 8, 8, 103,72)
A_Henrique = Player('Adam Henrique', 'NJD', 'C', 75, 16, 27, 127, 46,75, 16, 27, 127,46)
T_Hertl = Player('Tomas Hertl', 'SJS', 'C', 82, 13, 18, 145, 33,82, 13, 18, 145,33)
T_Hickey = Player('Thomas Hickey', 'NYI', 'D', 81, 2, 20, 82, 136,81, 2, 20, 82,136)
C_Higgins = Player('Chris Higgins', 'VAN', 'LW', 77, 12, 24, 171, 34,77, 12, 24, 171,34)
J_Hillen = Player('Jack Hillen', 'TOT', 'D', 38, 0, 5, 24, 53,38, 0, 5, 24,53)
J_Hishon = Player('Joey Hishon', 'COL', 'C', 13, 1, 1, 19, 7,13, 1, 1, 19,7)
N_Hjalmarsson = Player('Niklas Hjalmarsson', 'CHI', 'D', 82, 3, 16, 97, 127,82, 3, 16, 97,127)
J_Hodgman = Player('Justin Hodgman', 'ARI', 'C', 5, 1, 0, 3, 0,5, 1, 0, 3,0)
C_Hodgson = Player('Cody Hodgson', 'BUF', 'C', 78, 6, 7, 127, 21,78, 6, 7, 127,21)
M_Hoffman = Player('Mike Hoffman', 'OTT', 'LW', 79, 27, 21, 199, 33,79, 27, 21, 199,33)
N_Holden = Player('Nick Holden', 'COL', 'D', 78, 5, 9, 94, 96,78, 5, 9, 94,96)
P_Holland = Player('Peter Holland', 'TOR', 'C', 62, 11, 14, 93, 21,62, 11, 14, 93,21)
K_Holzer = Player('Korbinian Holzer', 'TOR', 'D', 34, 0, 6, 32, 53,34, 0, 6, 32,53)
S_Horcoff = Player('Shawn Horcoff', 'DAL', 'C', 76, 11, 18, 82, 25,76, 11, 18, 82,25)
P_Hornqvist = Player('Patric Hornqvist', 'PIT', 'RW', 64, 25, 26, 220, 33,64, 25, 26, 220,33)
B_Horvat = Player('Bo Horvat', 'VAN', 'C', 68, 13, 12, 93, 47,68, 13, 12, 93,47)
M_Hossa = Player('Marian Hossa', 'CHI', 'RW', 82, 22, 39, 247, 26,82, 22, 39, 247,26)
R_Hrabarenka = Player('Raman Hrabarenka', 'NJD', 'D', 1, 0, 0, 0, 6,1, 0, 0, 0,6)
J_Huberdeau = Player('Jonathan Huberdeau', 'FLA', 'LW', 79, 15, 39, 169, 24,79, 15, 39, 169,24)
J_Hudler = Player('Jiri Hudler', 'CGY', 'C', 78, 31, 45, 158, 14,78, 31, 45, 158,14)
B_Hunt = Player('Brad Hunt', 'EDM', 'D', 11, 1, 2, 20, 10,11, 1, 2, 20,10)
M_Hunwick = Player('Matt Hunwick', 'NYR', 'D', 55, 2, 9, 72, 43,55, 2, 9, 72,43)
J_Iginla = Player('Jarome Iginla', 'COL', 'RW', 82, 29, 30, 189, 47,82, 29, 30, 189,47)
M_Irwin = Player('Matt Irwin', 'SJS', 'D', 53, 8, 11, 93, 65,53, 8, 11, 93,65)
B_Jackman = Player('Barret Jackman', 'STL', 'D', 80, 2, 13, 86, 126,80, 2, 13, 86,126)
T_Jackman = Player('Tim Jackman', 'ANA', 'RW', 55, 5, 2, 55, 19,55, 5, 2, 55,19)
J_Jagr = Player('Jaromir Jagr', 'TOT', 'RW', 77, 17, 30, 169, 14,77, 17, 30, 169,14)
C_Jarnkrok = Player('Calle Jarnkrok', 'NSH', 'C', 74, 7, 11, 95, 21,74, 7, 11, 95,21)
D_Jaskin = Player('Dmitrij Jaskin', 'STL', 'RW', 54, 13, 5, 108, 21,54, 13, 5, 108,21)
B_Jenner = Player('Boone Jenner', 'CBJ', 'C', 31, 9, 8, 83, 25,31, 9, 8, 83,25)
N_Jensen = Player('Nicklas Jensen', 'VAN', 'RW', 5, 0, 0, 7, 4,5, 0, 0, 7,4)
J_Joensuu = Player('Jesse Joensuu', 'EDM', 'LW', 20, 2, 2, 18, 9,20, 2, 2, 18,9)
R_Johansen = Player('Ryan Johansen', 'CBJ', 'C', 82, 26, 45, 202, 33,82, 26, 45, 202,33)
M_Johansson = Player('Marcus Johansson', 'WSH', 'C', 82, 20, 27, 138, 18,82, 20, 27, 138,18)
E_Johnson = Player('Erik Johnson', 'COL', 'D', 47, 12, 11, 115, 107,47, 12, 11, 115,107)
J_Johnson = Player('Jack Johnson', 'CBJ', 'D', 79, 8, 32, 141, 131,79, 8, 32, 141,131)
T_Johnson = Player('Tyler Johnson', 'TBL', 'C', 77, 29, 43, 203, 35,77, 29, 43, 203,35)
J_Jokinen = Player('Jussi Jokinen', 'FLA', 'LW', 81, 8, 36, 134, 50,81, 8, 36, 134,50)
O_Jokinen = Player('Olli Jokinen', 'TOT', 'C', 62, 4, 6, 110, 19,62, 4, 6, 110,19)
J_Jokipakka = Player('Jyrki Jokipakka', 'DAL', 'D', 51, 0, 10, 40, 66,51, 0, 10, 40,66)
B_Jones = Player('Blair Jones', 'PHI', 'C', 4, 0, 0, 0, 1,4, 0, 0, 0,1)
D_Jones = Player('David Jones', 'CGY', 'RW', 67, 14, 16, 114, 45,67, 14, 16, 114,45)
S_Jones = Player('Seth Jones', 'NSH', 'D', 82, 8, 19, 123, 90,82, 8, 19, 123,90)
J_Jooris = Player('Josh Jooris', 'CGY', 'RW', 60, 12, 12, 89, 30,60, 12, 12, 89,30)
M_Jordan = Player('Michal Jordan', 'CAR', 'D', 38, 2, 4, 44, 61,38, 2, 4, 44,61)
J_Josefson = Player('Jacob Josefson', 'NJD', 'C', 62, 6, 5, 61, 31,62, 6, 5, 61,31)
R_Josi = Player('Roman Josi', 'NSH', 'D', 81, 15, 40, 201, 209,81, 15, 40, 201,209)
T_Jurco = Player('Tomas Jurco', 'DET', 'RW', 63, 3, 15, 92, 11,63, 3, 15, 92,11)
N_Kadri = Player('Nazem Kadri', 'TOR', 'C', 73, 18, 21, 176, 23,73, 18, 21, 176,23)
P_Kaleta = Player('Patrick Kaleta', 'BUF', 'RW', 42, 0, 3, 25, 25,42, 0, 3, 25,25)
S_Kampfer = Player('Steven Kampfer', 'FLA', 'D', 25, 2, 2, 28, 33,25, 2, 2, 28,33)
E_Kane = Player('Evander Kane', 'WPG', 'LW', 37, 10, 12, 126, 14,37, 10, 12, 126,14)
P_Kane = Player('Patrick Kane', 'CHI', 'RW', 61, 27, 37, 186, 14,61, 27, 37, 186,14)
E_Karlsson = Player('Erik Karlsson', 'OTT', 'D', 82, 21, 45, 292, 89,82, 21, 45, 292,89)
M_Karlsson = Player('Melker Karlsson', 'SJS', 'C', 53, 13, 11, 100, 26,53, 13, 11, 100,26)
W_Karlsson = Player('William Karlsson', 'TOT', 'C', 21, 3, 2, 29, 7,21, 3, 2, 29,7)
Z_Kassian = Player('Zack Kassian', 'VAN', 'RW', 42, 10, 6, 55, 2,42, 10, 6, 55,2)
D_Keith = Player('Duncan Keith', 'CHI', 'D', 80, 10, 35, 171, 113,80, 10, 35, 171,113)
C_Kelly = Player('Chris Kelly', 'BOS', 'C', 80, 7, 21, 112, 61,80, 7, 21, 112,61)
R_Kenins = Player('Ronalds Kenins', 'VAN', 'LW', 30, 4, 8, 38, 7,30, 4, 8, 38,7)
T_Kennedy = Player('Tyler Kennedy', 'TOT', 'C', 38, 6, 8, 79, 8,38, 6, 8, 79,8)
R_Kesler = Player('Ryan Kesler', 'ANA', 'C', 81, 20, 27, 205, 69,81, 20, 27, 205,69)
P_Kessel = Player('Phil Kessel', 'TOR', 'RW', 82, 25, 36, 280, 13,82, 25, 36, 280,13)
A_Khokhlachev = Player('Alexander Khokhlachev', 'BOS', 'C', 3, 0, 0, 1, 0,3, 0, 0, 1,0)
A_Killorn = Player('Alex Killorn', 'TBL', 'C', 71, 15, 23, 130, 21,71, 15, 23, 130,21)
J_Kindl = Player('Jakub Kindl', 'DET', 'D', 35, 5, 8, 54, 25,35, 5, 8, 54,25)
D_King = Player('Dwight King', 'LAK', 'LW', 81, 13, 13, 127, 14,81, 13, 13, 127,14)
O_Klefbom = Player('Oscar Klefbom', 'EDM', 'D', 60, 2, 18, 98, 102,60, 2, 18, 98,102)
K_Klein = Player('Kevin Klein', 'NYR', 'D', 65, 9, 17, 76, 115,65, 9, 17, 76,115)
C_Klingberg = Player('Carl Klingberg', 'WPG', 'LW', 2, 0, 0, 0, 0,2, 0, 0, 0,0)
J_Klingberg = Player('John Klingberg', 'DAL', 'D', 65, 11, 29, 98, 77,65, 11, 29, 98,77)
R_Klinkhammer = Player('Rob Klinkhammer', 'TOT', 'C', 69, 5, 4, 64, 12,69, 5, 4, 64,12)
C_Knight = Player('Corban Knight', 'CGY', 'C', 2, 0, 0, 2, 1,2, 0, 0, 2,1)
S_Koekkoek = Player('Slater Koekkoek', 'TBL', 'D', 3, 0, 0, 6, 3,3, 0, 0, 6,3)
M_Koivu = Player('Mikko Koivu', 'MIN', 'C', 80, 14, 34, 179, 41,80, 14, 34, 179,41)
L_Komarov = Player('Leo Komarov', 'TOR', 'C', 62, 8, 18, 84, 25,62, 8, 18, 84,25)
T_Kopecky = Player('Tomas Kopecky', 'FLA', 'RW', 64, 2, 6, 106, 22,64, 2, 6, 106,22)
A_Kopitar = Player('Anze Kopitar', 'LAK', 'C', 79, 16, 48, 134, 45,79, 16, 48, 134,45)
L_Korpikoski = Player('Lauri Korpikoski', 'ARI', 'LW', 69, 6, 15, 82, 48,69, 6, 15, 82,48)
M_Kostka = Player('Mike Kostka', 'NYR', 'D', 7, 0, 1, 7, 9,7, 0, 1, 7,9)
B_Kozun = Player('Brandon Kozun', 'TOR', 'RW', 20, 2, 2, 8, 4,20, 2, 2, 8,4)
C_Kreider = Player('Chris Kreider', 'NYR', 'LW', 80, 21, 25, 180, 17,80, 21, 25, 180,17)
D_Krejci = Player('David Krejci', 'BOS', 'C', 47, 7, 24, 70, 29,47, 7, 24, 70,29)
N_Kronwall = Player('Niklas Kronwall', 'DET', 'D', 80, 9, 35, 101, 106,80, 9, 35, 101,106)
T_Krug = Player('Torey Krug', 'BOS', 'D', 78, 12, 27, 205, 68,78, 12, 27, 205,68)
M_Kruger = Player('Marcus Kruger', 'CHI', 'C', 81, 7, 10, 126, 50,81, 7, 10, 126,50)
N_Kucherov = Player('Nikita Kucherov', 'TBL', 'RW', 82, 29, 36, 191, 28,82, 29, 36, 191,28)
B_Kulak = Player('Brett Kulak', 'CGY', 'D', 1, 0, 0, 0, 0,1, 0, 0, 0,0)
N_Kulemin = Player('Nikolai Kulemin', 'NYI', 'LW', 82, 15, 16, 115, 58,82, 15, 16, 115,58)
D_Kulikov = Player('Dmitry Kulikov', 'FLA', 'D', 73, 3, 19, 83, 105,73, 3, 19, 83,105)
C_Kunitz = Player('Chris Kunitz', 'PIT', 'LW', 74, 17, 23, 170, 29,74, 17, 23, 170,29)
E_Kuznetsov = Player('Evgeny Kuznetsov', 'WSH', 'C', 80, 11, 26, 127, 15,80, 11, 26, 127,15)
A_Ladd = Player('Andrew Ladd', 'WPG', 'LW', 81, 24, 38, 224, 38,81, 24, 38, 224,38)
B_Laich = Player('Brooks Laich', 'WSH', 'C', 66, 7, 13, 106, 53,66, 7, 13, 106,53)
A_Lander = Player('Anton Lander', 'EDM', 'C', 38, 6, 14, 61, 12,38, 6, 14, 61,12)
G_Landeskog = Player('Gabriel Landeskog', 'COL', 'LW', 82, 23, 36, 214, 73,82, 23, 36, 214,73)
M_Lapierre = Player('Maxim Lapierre', 'TOT', 'C', 80, 2, 9, 86, 36,80, 2, 9, 86,36)
A_Larsson = Player('Adam Larsson', 'NJD', 'D', 64, 3, 21, 91, 124,64, 3, 21, 91,124)
J_Larsson = Player('Johan Larsson', 'BUF', 'LW', 39, 6, 10, 50, 19,39, 6, 10, 50,19)
B_Lashoff = Player('Brian Lashoff', 'DET', 'D', 11, 0, 2, 7, 14,11, 0, 2, 7,14)
M_Latta = Player('Michael Latta', 'WSH', 'C', 53, 0, 6, 24, 14,53, 0, 6, 24,14)
S_Laughton = Player('Scott Laughton', 'PHI', 'C', 31, 2, 4, 51, 11,31, 2, 4, 51,11)
O_Lauridsen = Player('Oliver Lauridsen', 'PHI', 'D', 1, 0, 0, 2, 0,1, 0, 0, 2,0)
C_Lazar = Player('Curtis Lazar', 'OTT', 'C', 67, 6, 9, 92, 40,67, 6, 9, 92,40)
V_Lecavalier = Player('Vincent Lecavalier', 'PHI', 'C', 57, 8, 12, 103, 15,57, 8, 12, 103,15)
N_Leddy = Player('Nick Leddy', 'NYI', 'D', 78, 10, 27, 120, 90,78, 10, 27, 120,90)
A_Lee = Player('Anders Lee', 'NYI', 'C', 76, 25, 16, 197, 29,76, 25, 16, 197,29)
D_Legwand = Player('David Legwand', 'OTT', 'C', 80, 9, 18, 91, 25,80, 9, 18, 91,25)
J_Lehtera = Player('Jori Lehtera', 'STL', 'C', 75, 14, 30, 103, 34,75, 14, 30, 103,34)
J_Leivo = Player('Josh Leivo', 'TOR', 'LW', 9, 1, 0, 10, 0,9, 1, 0, 10,0)
J_Leopold = Player('Jordan Leopold', 'TOT', 'D', 43, 1, 3, 39, 50,43, 1, 3, 39,50)
L_Lessio = Player('Lucas Lessio', 'ARI', 'LW', 26, 2, 3, 44, 6,26, 2, 3, 44,6)
K_Letang = Player('Kris Letang', 'PIT', 'D', 69, 11, 43, 197, 117,69, 11, 43, 197,117)
M_Letestu = Player('Mark Letestu', 'CBJ', 'C', 54, 7, 6, 63, 24,54, 7, 6, 63,24)
T_Lewis = Player('Trevor Lewis', 'LAK', 'C', 73, 9, 16, 143, 17,73, 9, 16, 143,17)
J_Liles = Player('John-Michael Liles', 'CAR', 'D', 57, 2, 20, 90, 74,57, 2, 20, 90,74)
O_Lindberg = Player('Oscar Lindberg', 'NYR', 'C', 1, 0, 0, 2, 0,1, 0, 0, 2,0)
M_Lindblad = Player('Matt Lindblad', 'BOS', 'C', 2, 0, 0, 3, 0,2, 0, 0, 3,0)
P_Lindbohm = Player('Petteri Lindbohm', 'STL', 'D', 23, 2, 1, 32, 22,23, 2, 1, 32,22)
E_Lindholm = Player('Elias Lindholm', 'CAR', 'C', 81, 17, 22, 170, 30,81, 17, 22, 170,30)
H_Lindholm = Player('Hampus Lindholm', 'ANA', 'D', 78, 7, 27, 107, 77,78, 7, 27, 107,77)
J_Lindstrom = Player('Joakim Lindstrom', 'TOT', 'C', 53, 4, 6, 61, 5,53, 4, 6, 61,5)
B_Little = Player('Bryan Little', 'WPG', 'C', 70, 24, 28, 148, 32,70, 24, 28, 148,32)
B_Lovejoy = Player('Ben Lovejoy', 'TOT', 'D', 60, 2, 12, 86, 105,60, 2, 12, 86,105)
K_Lowe = Player('Keegan Lowe', 'CAR', 'D', 2, 0, 0, 0, 4,2, 0, 0, 0,4)
A_Lowry = Player('Adam Lowry', 'WPG', 'LW', 80, 11, 12, 104, 32,80, 11, 12, 104,32)
M_Lucic = Player('Milan Lucic', 'BOS', 'LW', 81, 18, 26, 141, 23,81, 18, 26, 141,23)
J_Lupul = Player('Joffrey Lupul', 'TOR', 'LW', 55, 10, 11, 97, 20,55, 10, 11, 97,20)
O_Maatta = Player('Olli Maatta', 'PIT', 'D', 20, 1, 8, 27, 33,20, 1, 8, 27,33)
C_MacArthur = Player('Clarke MacArthur', 'OTT', 'LW', 62, 16, 20, 140, 17,62, 16, 20, 140,17)
A_MacDonald = Player('Andrew MacDonald', 'PHI', 'D', 58, 2, 10, 62, 86,58, 2, 10, 62,86)
D_MacKenzie = Player('Derek MacKenzie', 'FLA', 'C', 82, 5, 6, 72, 51,82, 5, 6, 72,51)
N_MacKinnon = Player('Nathan MacKinnon', 'COL', 'C', 64, 14, 24, 192, 41,64, 14, 24, 192,41)
A_MacWilliam = Player('Andrew MacWilliam', 'TOR', 'D', 12, 0, 2, 5, 20,12, 0, 2, 5,20)
M_Malhotra = Player('Manny Malhotra', 'MTL', 'C', 58, 1, 3, 46, 62,58, 1, 3, 46,62)
E_Malkin = Player('Evgeni Malkin', 'PIT', 'C', 69, 28, 42, 212, 18,69, 28, 42, 212,18)
B_Malone = Player('Brad Malone', 'CAR', 'C', 65, 7, 8, 65, 16,65, 7, 8, 65,16)
R_Malone = Player('Ryan Malone', 'NYR', 'LW', 6, 0, 0, 6, 2,6, 0, 0, 6,2)
B_Manning = Player('Brandon Manning', 'PHI', 'D', 11, 0, 3, 10, 13,11, 0, 3, 10,13)
J_Manson = Player('Josh Manson', 'ANA', 'D', 28, 0, 3, 26, 24,28, 0, 3, 26,24)
B_Marchand = Player('Brad Marchand', 'BOS', 'LW', 77, 24, 18, 180, 28,77, 24, 18, 180,28)
A_Marchenko = Player('Alexey Marchenko', 'DET', 'D', 13, 1, 1, 7, 10,13, 1, 1, 7,10)
J_Marchessault = Player('Jon Marchessault', 'TBL', 'C', 2, 1, 0, 3, 0,2, 1, 0, 3,0)
M_Marincin = Player('Martin Marincin', 'EDM', 'D', 41, 1, 4, 38, 59,41, 1, 4, 38,59)
A_Markov = Player('Andrei Markov', 'MTL', 'D', 81, 10, 40, 135, 173,81, 10, 40, 135,173)
P_Marleau = Player('Patrick Marleau', 'SJS', 'LW', 82, 19, 38, 233, 26,82, 19, 38, 233,26)
P_Maroon = Player('Patrick Maroon', 'ANA', 'LW', 71, 9, 25, 120, 10,71, 9, 25, 120,10)
M_Martin = Player('Matt Martin', 'NYI', 'LW', 78, 8, 6, 90, 36,78, 8, 6, 90,36)
P_Martin = Player('Paul Martin', 'PIT', 'D', 74, 3, 17, 61, 139,74, 3, 17, 61,139)
A_Martinez = Player('Alec Martinez', 'LAK', 'D', 56, 6, 16, 103, 117,56, 6, 16, 103,117)
J_Martinook = Player('Jordan Martinook', 'ARI', 'C', 8, 0, 1, 8, 2,8, 0, 1, 8,2)
S_Matteau = Player('Stefan Matteau', 'NJD', 'LW', 7, 1, 0, 8, 1,7, 1, 0, 8,1)
S_Matthias = Player('Shawn Matthias', 'VAN', 'C', 78, 18, 9, 132, 33,78, 18, 9, 132,33)
J_McBain = Player('Jamie McBain', 'LAK', 'D', 26, 3, 6, 18, 28,26, 3, 6, 18,28)
J_McCabe = Player('Jake McCabe', 'BUF', 'D', 2, 0, 0, 2, 1,2, 0, 0, 2,1)
J_McClement = Player('Jay McClement', 'CAR', 'C', 82, 7, 14, 68, 53,82, 7, 14, 68,53)
C_McCormick = Player('Cody McCormick', 'BUF', 'C', 33, 1, 3, 31, 29,33, 1, 3, 31,29)
R_McDonagh = Player('Ryan McDonagh', 'NYR', 'D', 71, 8, 25, 148, 139,71, 8, 25, 148,139)
C_McDonald = Player('Colin McDonald', 'NYI', 'RW', 18, 2, 6, 29, 6,18, 2, 6, 29,6)
J_McGinn = Player('Jamie McGinn', 'COL', 'LW', 19, 4, 2, 36, 7,19, 4, 2, 36,7)
T_McGinn = Player('Tye McGinn', 'TOT', 'LW', 51, 2, 5, 60, 17,51, 2, 5, 60,17)
B_McGrattan = Player('Brian McGrattan', 'CGY', 'RW', 8, 0, 0, 10, 1,8, 0, 0, 10,1)
D_McIlrath = Player('Dylan McIlrath', 'NYR', 'D', 1, 0, 0, 0, 3,1, 0, 0, 0,3)
G_McKegg = Player('Greg McKegg', 'TOR', 'C', 3, 0, 0, 1, 2,3, 0, 0, 1,2)
C_McKenzie = Player('Curtis McKenzie', 'DAL', 'LW', 36, 4, 1, 41, 13,36, 4, 1, 41,13)
C_McLeod = Player('Cody McLeod', 'COL', 'LW', 82, 7, 5, 94, 43,82, 7, 5, 94,43)
B_McMillan = Player('Brandon McMillan', 'TOT', 'C', 58, 1, 3, 51, 23,58, 1, 3, 51,23)
B_McNabb = Player('Brayden McNabb', 'LAK', 'D', 71, 2, 22, 74, 56,71, 2, 22, 74,56)
A_McQuaid = Player('Adam McQuaid', 'BOS', 'D', 63, 1, 6, 60, 91,63, 1, 6, 60,91)
J_Megna = Player('Jayson Megna', 'PIT', 'C', 12, 0, 1, 13, 8,12, 0, 1, 13,8)
J_Merrill = Player('Jonathon Merrill', 'NJD', 'D', 66, 2, 12, 47, 89,66, 2, 12, 47,89)
A_Meszaros = Player('Andrej Meszaros', 'BUF', 'D', 60, 7, 7, 67, 94,60, 7, 7, 67,94)
M_Methot = Player('Marc Methot', 'OTT', 'D', 45, 1, 10, 49, 70,45, 1, 10, 49,70)
M_Michalek = Player('Milan Michalek', 'OTT', 'LW', 66, 13, 21, 130, 40,66, 13, 21, 130,40)
Z_Michalek = Player('Zbynek Michalek', 'TOT', 'D', 68, 4, 8, 86, 160,68, 4, 8, 86,160)
A_Miller = Player('Andrew Miller', 'EDM', 'C', 9, 1, 5, 14, 6,9, 1, 5, 14,6)
D_Miller = Player('Drew Miller', 'DET', 'LW', 82, 5, 8, 98, 99,82, 5, 8, 98,99)
J_Miller = Player('J.T. Miller', 'NYR', 'C', 58, 10, 13, 92, 28,58, 10, 13, 92,28)
K_Miller = Player('Kevan Miller', 'BOS', 'D', 41, 2, 5, 37, 60,41, 2, 5, 37,60)
J_Mitchell = Player('John Mitchell', 'COL', 'C', 68, 11, 15, 105, 56,68, 11, 15, 105,56)
T_Mitchell = Player('Torrey Mitchell', 'TOT', 'C', 65, 6, 8, 55, 61,65, 6, 8, 55,61)
W_Mitchell = Player('Willie Mitchell', 'FLA', 'D', 66, 3, 5, 78, 144,66, 3, 5, 78,144)
T_Moen = Player('Travis Moen', 'TOT', 'LW', 44, 3, 6, 34, 24,44, 3, 6, 34,24)
S_Monahan = Player('Sean Monahan', 'CGY', 'C', 81, 31, 31, 191, 42,81, 31, 31, 191,42)
D_Moore = Player('Dominic Moore', 'NYR', 'C', 82, 10, 17, 116, 45,82, 10, 17, 116,45)
J_Moore = Player('John Moore', 'TOT', 'D', 57, 2, 9, 77, 52,57, 2, 9, 77,52)
J_Morin = Player('Jeremy Morin', 'TOT', 'RW', 43, 2, 4, 73, 5,43, 2, 4, 73,5)
T_Morin = Player('Travis Morin', 'DAL', 'C', 6, 0, 0, 10, 0,6, 0, 0, 10,0)
B_Morrow = Player('Brenden Morrow', 'TBL', 'LW', 70, 3, 5, 28, 16,70, 3, 5, 28,16)
J_Morrow = Player('Joseph Morrow', 'BOS', 'D', 15, 1, 0, 20, 22,15, 1, 0, 20,22)
D_Moss = Player('Dave Moss', 'ARI', 'RW', 60, 4, 8, 96, 36,60, 4, 8, 96,36)
K_Mouillierat = Player('Kael Mouillierat', 'NYI', 'LW', 6, 1, 1, 1, 3,6, 1, 1, 1,3)
M_Moulson = Player('Matt Moulson', 'BUF', 'LW', 77, 13, 28, 156, 49,77, 13, 28, 156,49)
C_Mueller = Player('Chris Mueller', 'NYR', 'C', 7, 1, 1, 10, 1,7, 1, 1, 10,1)
M_Mueller = Player('Mirco Mueller', 'SJS', 'D', 39, 1, 3, 31, 58,39, 1, 3, 31,58)
C_Murphy = Player('Connor Murphy', 'ARI', 'D', 73, 4, 3, 72, 142,73, 4, 3, 72,142)
R_Murphy = Player('Ryan Murphy', 'CAR', 'D', 37, 4, 9, 61, 37,37, 4, 9, 61,37)
R_Murray = Player('Ryan Murray', 'CBJ', 'D', 12, 1, 2, 8, 11,12, 1, 2, 8,11)
D_Musil = Player('David Musil', 'EDM', 'D', 4, 0, 2, 3, 8,4, 0, 2, 3,8)
J_Muzzin = Player('Jake Muzzin', 'LAK', 'D', 76, 10, 31, 173, 108,76, 10, 31, 173,108)
T_Myers = Player('Tyler Myers', 'TOT', 'D', 71, 7, 21, 124, 132,71, 7, 21, 124,132)
V_Namestnikov = Player('Vladislav Namestnikov', 'TBL', 'C', 43, 9, 7, 46, 13,43, 9, 7, 46,13)
R_Nash = Player('Rick Nash', 'NYR', 'LW', 79, 42, 27, 304, 33,79, 42, 27, 304,33)
J_Neal = Player('James Neal', 'NSH', 'LW', 67, 23, 14, 222, 30,67, 23, 14, 222,30)
C_Neil = Player('Chris Neil', 'OTT', 'RW', 38, 4, 3, 23, 11,38, 4, 3, 23,11)
B_Nelson = Player('Brock Nelson', 'NYI', 'C', 82, 20, 22, 190, 52,82, 20, 22, 190,52)
P_Nemeth = Player('Patrik Nemeth', 'DAL', 'D', 22, 0, 3, 16, 21,22, 0, 3, 16,21)
N_Nesterov = Player('Nikita Nesterov', 'TBL', 'D', 27, 2, 5, 44, 18,27, 2, 5, 44,18)
A_Nestrasil = Player('Andrej Nestrasil', 'TOT', 'C', 54, 7, 13, 82, 17,54, 7, 13, 82,17)
V_Nichushkin = Player('Valeri Nichushkin', 'DAL', 'RW', 8, 0, 1, 6, 1,8, 0, 1, 6,1)
N_Niederreiter = Player('Nino Niederreiter', 'MIN', 'RW', 80, 24, 13, 149, 32,80, 24, 13, 149,32)
F_Nielsen = Player('Frans Nielsen', 'NYI', 'C', 78, 14, 29, 157, 80,78, 14, 29, 157,80)
M_Nieto = Player('Matthew Nieto', 'SJS', 'LW', 72, 10, 17, 135, 38,72, 10, 17, 135,38)
N_Nikitin = Player('Nikita Nikitin', 'EDM', 'D', 42, 4, 6, 80, 49,42, 4, 6, 80,49)
M_Niskanen = Player('Matt Niskanen', 'WSH', 'D', 82, 4, 27, 117, 106,82, 4, 27, 117,106)
S_Noesen = Player('Stefan Noesen', 'ANA', 'RW', 1, 0, 0, 0, 1,1, 0, 0, 0,1)
J_Nolan = Player('Jordan Nolan', 'LAK', 'C', 60, 6, 3, 44, 11,60, 6, 3, 44,11)
J_Nordstrom = Player('Joakim Nordstrom', 'CHI', 'C', 38, 0, 3, 42, 17,38, 0, 3, 42,17)
R_Nugent_Hopkins = Player('Ryan Nugent-Hopkins', 'EDM', 'C', 76, 24, 32, 189, 37,76, 24, 32, 189,37)
D_Nurse = Player('Darnell Nurse', 'EDM', 'D', 2, 0, 0, 2, 0,2, 0, 0, 2,0)
G_Nyquist = Player('Gustav Nyquist', 'DET', 'C', 82, 27, 27, 195, 31,82, 27, 27, 195,31)
E_Nystrom = Player('Eric Nystrom', 'NSH', 'LW', 60, 7, 5, 60, 29,60, 7, 5, 60,29)
L_OBrien = Player("Liam O'Brien", 'WSH', 'C', 13, 1, 1, 16, 0,13, 1, 1, 16,0)
S_OBrien = Player("Shane O'Brien", 'FLA', 'D', 9, 0, 1, 4, 12,9, 0, 1, 4,12)
E_ODell = Player("Eric O'Dell", 'WPG', 'C', 11, 0, 1, 6, 0,11, 0, 1, 6,0)
R_OReilly = Player("Ryan O'Reilly", 'COL', 'C', 82, 17, 38, 171, 48,82, 17, 38, 171,48)
J_Oduya = Player('Johnny Oduya', 'CHI', 'D', 76, 2, 8, 76, 123,76, 2, 8, 76,123)
J_Oesterle = Player('Jordan Oesterle', 'EDM', 'D', 6, 0, 1, 7, 3,6, 0, 1, 7,3)
K_Okposo = Player('Kyle Okposo', 'NYI', 'RW', 60, 18, 33, 195, 23,60, 18, 33, 195,23)
J_Oleksiak = Player('Jamie Oleksiak', 'DAL', 'D', 36, 1, 7, 36, 46,36, 1, 7, 36,46)
S_Oleksy = Player('Steven Oleksy', 'WSH', 'D', 1, 0, 0, 1, 0,1, 0, 0, 1,0)
D_Olsen = Player('Dylan Olsen', 'FLA', 'D', 44, 2, 6, 44, 52,44, 2, 6, 44,52)
B_Orpik = Player('Brooks Orpik', 'WSH', 'D', 78, 0, 19, 66, 192,78, 0, 19, 66,192)
T_Oshie = Player('T.J. Oshie', 'STL', 'RW', 72, 19, 36, 162, 39,72, 19, 36, 162,39)
S_Ott = Player('Steve Ott', 'STL', 'C', 78, 3, 9, 49, 14,78, 3, 9, 49,14)
X_Ouellet = Player('Xavier Ouellet', 'DET', 'D', 21, 2, 1, 27, 13,21, 2, 1, 27,13)
A_Ovechkin = Player('Alex Ovechkin', 'WSH', 'LW', 81, 53, 28, 395, 32,81, 53, 28, 395,32)
M_Paajarvi = Player('Magnus Paajarvi', 'STL', 'LW', 10, 0, 1, 9, 0,10, 0, 1, 9,0)
M_Pacioretty = Player('Max Pacioretty', 'MTL', 'LW', 80, 37, 30, 302, 38,80, 37, 30, 302,38)
J_Pageau = Player('Jean-Gabriel Pageau', 'OTT', 'C', 50, 10, 9, 97, 20,50, 10, 9, 97,20)
D_Paille = Player('Daniel Paille', 'BOS', 'LW', 71, 6, 7, 66, 34,71, 6, 7, 66,34)
I_Pakarinen = Player('Iiro Pakarinen', 'EDM', 'RW', 17, 1, 2, 34, 3,17, 1, 2, 34,3)
O_Palat = Player('Ondrej Palat', 'TBL', 'LW', 75, 16, 47, 139, 50,75, 16, 47, 139,50)
M_Paliotta = Player('Michael Paliotta', 'CHI', 'D', 1, 0, 1, 2, 2,1, 0, 1, 2,2)
K_Palmieri = Player('Kyle Palmieri', 'ANA', 'RW', 57, 14, 15, 112, 24,57, 14, 15, 112,24)
R_Panik = Player('Richard Panik', 'TOR', 'RW', 76, 11, 6, 87, 57,76, 11, 6, 87,57)
C_Paquette = Player('Cedric Paquette', 'TBL', 'C', 64, 12, 7, 91, 55,64, 12, 7, 91,55)
A_Pardy = Player('Adam Pardy', 'WPG', 'D', 55, 0, 9, 29, 61,55, 0, 9, 29,61)
P_Parenteau = Player('P.A. Parenteau', 'MTL', 'RW', 56, 8, 14, 97, 19,56, 8, 14, 97,19)
Z_Parise = Player('Zach Parise', 'MIN', 'LW', 74, 33, 29, 259, 56,74, 33, 29, 259,56)
D_Pastrnak = Player('David Pastrnak', 'BOS', 'RW', 46, 10, 17, 93, 11,46, 10, 17, 93,11)
G_Pateryn = Player('Greg Pateryn', 'MTL', 'D', 17, 0, 0, 10, 18,17, 0, 0, 10,18)
J_Pavelski = Player('Joe Pavelski', 'SJS', 'C', 82, 37, 33, 261, 82,82, 37, 33, 261,82)
T_Pearson = Player('Tanner Pearson', 'LAK', 'LW', 42, 12, 4, 68, 9,42, 12, 4, 68,9)
A_Peluso = Player('Anthony Peluso', 'WPG', 'RW', 49, 1, 1, 23, 6,49, 1, 1, 23,6)
S_Percy = Player('Stuart Percy', 'TOR', 'D', 9, 0, 3, 13, 13,9, 0, 3, 13,13)
M_Perreault = Player('Mathieu Perreault', 'WPG', 'C', 62, 18, 23, 129, 13,62, 18, 23, 129,13)
D_Perron = Player('David Perron', 'TOT', 'LW', 81, 17, 24, 196, 21,81, 17, 24, 196,21)
C_Perry = Player('Corey Perry', 'ANA', 'RW', 67, 33, 22, 193, 27,67, 33, 22, 193,27)
A_Petrovic = Player('Alex Petrovic', 'FLA', 'D', 33, 0, 3, 29, 34,33, 0, 3, 29,34)
J_Petry = Player('Jeff Petry', 'TOT', 'D', 78, 7, 15, 126, 109,78, 7, 15, 126,109)
D_Phaneuf = Player('Dion Phaneuf', 'TOR', 'D', 70, 3, 26, 138, 126,70, 3, 26, 138,126)
C_Phillips = Player('Chris Phillips', 'OTT', 'D', 36, 0, 3, 29, 54,36, 0, 3, 29,54)
A_Pietrangelo = Player('Alex Pietrangelo', 'STL', 'D', 81, 7, 39, 195, 161,81, 7, 39, 195,161)
S_Pinizzotto = Player('Steve Pinizzotto', 'EDM', 'RW', 18, 2, 2, 15, 2,18, 2, 2, 15,2)
B_Pirri = Player('Brandon Pirri', 'FLA', 'C', 49, 22, 2, 143, 13,49, 22, 2, 143,13)
J_Piskula = Player('Joe Piskula', 'NSH', 'D', 1, 0, 0, 0, 2,1, 0, 0, 0,2)
T_Pitlick = Player('Tyler Pitlick', 'EDM', 'RW', 17, 2, 0, 18, 17,17, 2, 0, 18,17)
T_Plekanec = Player('Tomas Plekanec', 'MTL', 'C', 82, 26, 34, 248, 55,82, 26, 34, 248,55)
E_Poirier = Player('Emile Poirier', 'CGY', 'RW', 6, 0, 1, 2, 1,6, 0, 1, 2,1)
R_Polak = Player('Roman Polak', 'TOR', 'D', 56, 5, 4, 61, 128,56, 5, 4, 61,128)
J_Pominville = Player('Jason Pominville', 'MIN', 'RW', 82, 18, 36, 252, 32,82, 18, 36, 252,32)
C_Porter = Player('Chris Porter', 'STL', 'LW', 24, 1, 1, 24, 1,24, 1, 1, 24,1)
P_Postma = Player('Paul Postma', 'WPG', 'D', 42, 2, 4, 40, 28,42, 2, 4, 40,28)
C_Potter = Player('Corey Potter', 'CGY', 'D', 6, 0, 0, 2, 6,6, 0, 0, 2,6)
B_Pouliot = Player('Benoit Pouliot', 'EDM', 'LW', 58, 19, 15, 105, 31,58, 19, 15, 105,31)
D_Pouliot = Player('Derrick Pouliot', 'PIT', 'D', 34, 2, 5, 56, 20,34, 2, 5, 56,20)
S_Prince = Player('Shane Prince', 'OTT', 'LW', 2, 0, 1, 2, 0,2, 0, 1, 2,0)
N_Prosser = Player('Nate Prosser', 'MIN', 'D', 63, 2, 5, 38, 102,63, 2, 5, 38,102)
D_Prout = Player('Dalton Prout', 'CBJ', 'D', 63, 0, 8, 64, 84,63, 0, 8, 64,84)
B_Prust = Player('Brandon Prust', 'MTL', 'LW', 82, 4, 14, 78, 34,82, 4, 14, 78,34)
M_Puempel = Player('Matt Puempel', 'OTT', 'LW', 13, 2, 1, 14, 1,13, 2, 1, 14,1)
T_Pulkkinen = Player('Teemu Pulkkinen', 'DET', 'LW', 31, 5, 3, 67, 4,31, 5, 3, 67,4)
T_Purcell = Player('Teddy Purcell', 'EDM', 'RW', 82, 12, 22, 146, 19,82, 12, 22, 146,19)
M_Pysyk = Player('Mark Pysyk', 'BUF', 'D', 7, 2, 1, 4, 11,7, 2, 1, 4,11)
K_Quincey = Player('Kyle Quincey', 'DET', 'D', 73, 3, 15, 90, 82,73, 3, 15, 90,82)
M_Raffl = Player('Michael Raffl', 'PHI', 'LW', 67, 21, 7, 134, 46,67, 21, 7, 134,46)
R_Rakell = Player('Rickard Rakell', 'ANA', 'C', 71, 9, 22, 105, 22,71, 9, 22, 105,22)
J_Ramage = Player('John Ramage', 'CGY', 'D', 1, 0, 0, 4, 2,1, 0, 0, 4,2)
B_Ranford = Player('Brendan Ranford', 'DAL', 'LW', 1, 0, 0, 0, 0,1, 0, 0, 0,0)
V_Rask = Player('Victor Rask', 'CAR', 'C', 80, 11, 22, 172, 36,80, 11, 22, 172,36)
T_Rattie = Player('Ty Rattie', 'STL', 'RW', 11, 0, 2, 8, 4,11, 0, 2, 8,4)
M_Raymond = Player('Mason Raymond', 'CGY', 'LW', 57, 12, 11, 123, 13,57, 12, 11, 123,13)
M_Read = Player('Matt Read', 'PHI', 'RW', 80, 8, 22, 142, 55,80, 8, 22, 142,55)
R_Reaves = Player('Ryan Reaves', 'STL', 'RW', 81, 6, 6, 55, 14,81, 6, 6, 55,14)
Z_Redmond = Player('Zach Redmond', 'COL', 'D', 59, 5, 15, 93, 76,59, 5, 15, 93,76)
D_Reese = Player('Dylan Reese', 'ARI', 'D', 1, 0, 0, 3, 2,1, 0, 0, 3,2)
R_Regehr = Player('Robyn Regehr', 'LAK', 'D', 67, 3, 10, 63, 83,67, 3, 10, 63,83)
P_Regin = Player('Peter Regin', 'CHI', 'C', 4, 0, 1, 3, 0,4, 0, 1, 3,0)
G_Reinhart = Player('Griffin Reinhart', 'NYI', 'D', 8, 0, 1, 4, 8,8, 0, 1, 4,8)
M_Reinhart = Player('Max Reinhart', 'CGY', 'C', 4, 0, 0, 3, 3,4, 0, 0, 3,3)
S_Reinhart = Player('Sam Reinhart', 'BUF', 'C', 9, 0, 1, 3, 5,9, 0, 1, 3,5)
B_Rendulic = Player('Borna Rendulic', 'COL', 'RW', 11, 1, 1, 6, 3,11, 1, 1, 6,3)
M_Ribeiro = Player('Mike Ribeiro', 'NSH', 'C', 82, 15, 47, 96, 19,82, 15, 47, 96,19)
B_Richards = Player('Brad Richards', 'CHI', 'C', 76, 12, 25, 199, 27,76, 12, 25, 199,27)
M_Richards = Player('Mike Richards', 'LAK', 'C', 53, 5, 11, 63, 10,53, 5, 11, 63,10)
B_Richardson = Player('Brad Richardson', 'VAN', 'RW', 45, 8, 13, 66, 20,45, 8, 13, 66,20)
T_Rieder = Player('Tobias Rieder', 'ARI', 'RW', 72, 13, 8, 189, 37,72, 13, 8, 189,37)
M_Rielly = Player('Morgan Rielly', 'TOR', 'D', 81, 8, 21, 148, 103,81, 8, 21, 148,103)
Z_Rinaldo = Player('Zac Rinaldo', 'PHI', 'C', 58, 1, 5, 45, 20,58, 1, 5, 45,20)
R_Rissanen = Player('Rasmus Rissanen', 'CAR', 'D', 6, 0, 0, 3, 7,6, 0, 0, 3,7)
R_Ristolainen = Player('Rasmus Ristolainen', 'BUF', 'D', 78, 8, 12, 121, 136,78, 8, 12, 121,136)
B_Ritchie = Player('Brett Ritchie', 'DAL', 'RW', 31, 6, 3, 78, 5,31, 6, 3, 78,5)
C_Robak = Player('Colby Robak', 'TOT', 'D', 12, 0, 1, 8, 10,12, 0, 1, 8,10)
S_Robidas = Player('Stephane Robidas', 'TOR', 'D', 52, 1, 6, 34, 75,52, 1, 6, 34,75)
B_Robins = Player('Bobby Robins', 'BOS', 'C', 3, 0, 0, 0, 0,3, 0, 0, 0,0)
A_Roussel = Player('Antoine Roussel', 'DAL', 'LW', 80, 13, 12, 113, 71,80, 13, 12, 113,71)
D_Roy = Player('Derek Roy', 'TOT', 'C', 72, 12, 20, 113, 43,72, 12, 20, 113,43)
M_Rozsival = Player('Michal Rozsival', 'CHI', 'D', 65, 1, 12, 56, 87,65, 1, 12, 56,87)
C_Ruhwedel = Player('Chad Ruhwedel', 'BUF', 'D', 4, 0, 1, 4, 2,4, 0, 1, 4,2)
D_Rundblad = Player('David Rundblad', 'CHI', 'D', 49, 3, 11, 58, 38,49, 3, 11, 58,38)
K_Russell = Player('Kris Russell', 'CGY', 'D', 79, 4, 30, 111, 283,79, 4, 30, 111,283)
B_Rust = Player('Bryan Rust', 'PIT', 'RW', 14, 1, 1, 34, 3,14, 1, 1, 34,3)
T_Ruutu = Player('Tuomo Ruutu', 'NJD', 'RW', 77, 7, 6, 74, 23,77, 7, 6, 74,23)
B_Ryan = Player('Bobby Ryan', 'OTT', 'RW', 78, 18, 36, 221, 33,78, 18, 36, 221,33)
K_Rychel = Player('Kerby Rychel', 'CBJ', 'LW', 5, 0, 3, 4, 3,5, 0, 3, 4,3)
M_Ryder = Player('Michael Ryder', 'NJD', 'RW', 47, 6, 13, 89, 14,47, 6, 13, 89,14)
B_Saad = Player('Brandon Saad', 'CHI', 'LW', 82, 23, 29, 203, 29,82, 23, 29, 203,29)
M_Salomaki = Player('Miikka Salomaki', 'NSH', 'RW', 1, 1, 0, 4, 1,1, 1, 0, 4,1)
B_Salvador = Player('Bryce Salvador', 'NJD', 'D', 15, 0, 2, 13, 19,15, 0, 2, 13,19)
H_Samuelsson = Player('Henrik Samuelsson', 'ARI', 'C', 3, 0, 0, 4, 0,3, 0, 0, 4,0)
P_Samuelsson = Player('Philip Samuelsson', 'ARI', 'D', 4, 0, 0, 4, 4,4, 0, 0, 4,4)
M_Santorelli = Player('Mike Santorelli', 'TOT', 'C', 79, 12, 21, 145, 34,79, 12, 21, 145,34)
D_Savard = Player('David Savard', 'CBJ', 'D', 82, 11, 25, 112, 105,82, 11, 25, 112,105)
L_Sbisa = Player('Luca Sbisa', 'VAN', 'D', 76, 3, 8, 79, 128,76, 3, 8, 79,128)
M_Scandella = Player('Marco Scandella', 'MIN', 'D', 64, 11, 12, 112, 100,64, 11, 12, 112,100)
C_Sceviour = Player('Colton Sceviour', 'DAL', 'C', 71, 9, 17, 113, 41,71, 9, 17, 113,41)
T_Schaller = Player('Tim Schaller', 'BUF', 'C', 18, 1, 1, 19, 14,18, 1, 1, 19,14)
M_Scheifele = Player('Mark Scheifele', 'WPG', 'C', 82, 15, 34, 170, 61,82, 15, 34, 170,61)
B_Schenn = Player('Brayden Schenn', 'PHI', 'C', 82, 18, 29, 156, 38,82, 18, 29, 156,38)
L_Schenn = Player('Luke Schenn', 'PHI', 'D', 58, 3, 11, 67, 89,58, 3, 11, 67,89)
C_Schilling = Player('Cameron Schilling', 'WSH', 'D', 4, 0, 0, 2, 2,4, 0, 0, 2,2)
D_Schlemko = Player('David Schlemko', 'TOT', 'D', 44, 1, 3, 45, 85,44, 1, 3, 45,85)
N_Schmidt = Player('Nate Schmidt', 'WSH', 'D', 39, 1, 3, 40, 33,39, 1, 3, 40,33)
J_Schroeder = Player('Jordan Schroeder', 'MIN', 'C', 25, 3, 5, 48, 6,25, 3, 5, 48,6)
J_Schultz = Player('Jeff Schultz', 'LAK', 'D', 9, 0, 1, 7, 9,9, 0, 1, 7,9)
J_Schultz = Player('Justin Schultz', 'EDM', 'D', 81, 6, 25, 122, 114,81, 6, 25, 122,114)
N_Schultz = Player('Nick Schultz', 'PHI', 'D', 80, 2, 13, 69, 166,80, 2, 13, 69,166)
J_Schwartz = Player('Jaden Schwartz', 'STL', 'LW', 75, 28, 35, 184, 46,75, 28, 35, 184,46)
J_Scott = Player('John Scott', 'SJS', 'LW', 38, 3, 1, 19, 14,38, 3, 1, 19,14)
R_Scuderi = Player('Rob Scuderi', 'PIT', 'D', 82, 1, 9, 52, 110,82, 1, 9, 52,110)
B_Seabrook = Player('Brent Seabrook', 'CHI', 'D', 82, 8, 23, 181, 141,82, 8, 23, 181,141)
D_Sedin = Player('Daniel Sedin', 'VAN', 'LW', 82, 20, 56, 226, 16,82, 20, 56, 226,16)
H_Sedin = Player('Henrik Sedin', 'VAN', 'C', 82, 18, 55, 101, 24,82, 18, 55, 101,24)
T_Seguin = Player('Tyler Seguin', 'DAL', 'C', 71, 37, 40, 280, 26,71, 37, 40, 280,26)
D_Seidenberg = Player('Dennis Seidenberg', 'BOS', 'D', 82, 3, 11, 103, 146,82, 3, 11, 103,146)
J_Sekac = Player('Jiri Sekac', 'TOT', 'LW', 69, 9, 14, 85, 29,69, 9, 14, 85,29)
A_Sekera = Player('Andrej Sekera', 'TOT', 'D', 73, 3, 20, 100, 118,73, 3, 20, 100,118)
A_Semin = Player('Alexander Semin', 'CAR', 'RW', 57, 6, 13, 93, 17,57, 6, 13, 93,17)
T_Sestito = Player('Tim Sestito', 'NJD', 'LW', 15, 0, 2, 10, 3,15, 0, 2, 10,3)
T_Sestito = Player('Tom Sestito', 'VAN', 'LW', 3, 0, 1, 1, 0,3, 0, 1, 1,0)
D_Setoguchi = Player('Devin Setoguchi', 'CGY', 'RW', 12, 0, 0, 12, 5,12, 0, 0, 12,5)
D_Severson = Player('Damon Severson', 'NJD', 'D', 51, 5, 12, 93, 37,51, 5, 12, 93,37)
M_Sgarbossa = Player('Michael Sgarbossa', 'COL', 'C', 3, 0, 1, 2, 1,3, 0, 1, 2,1)
P_Sharp = Player('Patrick Sharp', 'CHI', 'LW', 68, 16, 27, 230, 15,68, 16, 27, 230,15)
K_Shattenkirk = Player('Kevin Shattenkirk', 'STL', 'D', 56, 8, 36, 135, 86,56, 8, 36, 135,86)
A_Shaw = Player('Andrew Shaw', 'CHI', 'C', 79, 15, 11, 146, 33,79, 15, 11, 146,33)
R_Sheahan = Player('Riley Sheahan', 'DET', 'C', 79, 13, 23, 123, 20,79, 13, 23, 123,20)
J_Sheppard = Player('James Sheppard', 'TOT', 'C', 71, 7, 11, 79, 40,71, 7, 11, 79,40)
B_Shinnimin = Player('Brendan Shinnimin', 'ARI', 'C', 12, 0, 1, 10, 4,12, 0, 1, 10,4)
D_Shore = Player('Drew Shore', 'CGY', 'C', 11, 1, 2, 13, 4,11, 1, 2, 13,4)
N_Shore = Player('Nick Shore', 'LAK', 'C', 34, 1, 6, 33, 14,34, 1, 6, 33,14)
J_Shugg = Player('Justin Shugg', 'CAR', 'RW', 3, 0, 0, 3, 0,3, 0, 0, 3,0)
D_Siemens = Player('Duncan Siemens', 'COL', 'D', 1, 0, 0, 0, 0,1, 0, 0, 0,0)
J_Silfverberg = Player('Jakob Silfverberg', 'ANA', 'RW', 81, 13, 26, 189, 37,81, 13, 26, 189,37)
Z_Sill = Player('Zach Sill', 'TOT', 'C', 63, 1, 3, 43, 27,63, 1, 3, 43,27)
W_Simmonds = Player('Wayne Simmonds', 'PHI', 'RW', 75, 28, 22, 188, 36,75, 28, 22, 188,36)
M_Sislo = Player('Mike Sislo', 'NJD', 'RW', 10, 0, 1, 13, 2,10, 0, 1, 13,2)
J_Skille = Player('Jack Skille', 'CBJ', 'RW', 45, 6, 2, 95, 15,45, 6, 2, 95,15)
J_Skinner = Player('Jeff Skinner', 'CAR', 'LW', 77, 18, 13, 235, 12,77, 18, 13, 235,12)
J_Slater = Player('Jim Slater', 'WPG', 'C', 82, 5, 8, 51, 52,82, 5, 8, 51,52)
L_Smid = Player('Ladislav Smid', 'CGY', 'D', 31, 0, 1, 21, 54,31, 0, 1, 21,54)
B_Smith = Player('Ben Smith', 'TOT', 'RW', 80, 7, 7, 92, 75,80, 7, 7, 92,75)
B_Smith = Player('Brendan Smith', 'DET', 'D', 76, 4, 9, 88, 68,76, 4, 9, 88,68)
C_Smith = Player('Colin Smith', 'COL', 'C', 1, 0, 0, 1, 0,1, 0, 0, 1,0)
C_Smith = Player('Craig Smith', 'NSH', 'C', 82, 23, 21, 251, 17,82, 23, 21, 251,17)
R_Smith = Player('Reilly Smith', 'BOS', 'RW', 81, 13, 27, 143, 39,81, 13, 27, 143,39)
T_Smith = Player('Trevor Smith', 'TOR', 'C', 54, 2, 3, 46, 25,54, 2, 3, 46,25)
Z_Smith = Player('Zack Smith', 'OTT', 'C', 37, 2, 1, 38, 13,37, 2, 1, 38,13)
D_Smith_Pelly = Player('Devante Smith-Pelly', 'TOT', 'RW', 74, 6, 14, 104, 49,74, 6, 14, 104,49)
C_Soderberg = Player('Carl Soderberg', 'BOS', 'C', 82, 13, 31, 163, 36,82, 13, 31, 163,36)
N_Spaling = Player('Nick Spaling', 'PIT', 'C', 82, 9, 18, 90, 45,82, 9, 18, 90,45)
J_Spezza = Player('Jason Spezza', 'DAL', 'C', 82, 17, 45, 204, 26,82, 17, 45, 204,26)
R_Spooner = Player('Ryan Spooner', 'BOS', 'C', 29, 8, 10, 73, 5,29, 8, 10, 73,5)
J_Spurgeon = Player('Jared Spurgeon', 'MIN', 'D', 66, 9, 16, 128, 124,66, 9, 16, 128,124)
M_Louis = Player('Martin St. Louis', 'NYR', 'RW', 74, 21, 31, 144, 37,74, 21, 31, 144,37)
E_Staal = Player('Eric Staal', 'CAR', 'C', 77, 23, 31, 244, 27,77, 23, 31, 244,27)
J_Staal = Player('Jordan Staal', 'CAR', 'C', 46, 6, 18, 92, 15,46, 6, 18, 92,15)
M_Staal = Player('Marc Staal', 'NYR', 'D', 80, 5, 15, 97, 123,80, 5, 15, 97,123)
D_Stafford = Player('Drew Stafford', 'TOT', 'RW', 76, 18, 25, 147, 15,76, 18, 25, 147,15)
M_Stajan = Player('Matt Stajan', 'CGY', 'C', 59, 7, 10, 46, 21,59, 7, 10, 46,21)
V_Stalberg = Player('Viktor Stalberg', 'NSH', 'LW', 25, 2, 8, 27, 10,25, 2, 8, 27,10)
S_Stamkos = Player('Steven Stamkos', 'TBL', 'C', 82, 43, 29, 268, 33,82, 43, 29, 268,33)
R_Stanton = Player('Ryan Stanton', 'VAN', 'D', 54, 3, 8, 59, 113,54, 3, 8, 59,113)
P_Stastny = Player('Paul Stastny', 'STL', 'C', 74, 16, 30, 143, 30,74, 16, 30, 143,30)
A_Steen = Player('Alex Steen', 'STL', 'LW', 74, 24, 40, 223, 37,74, 24, 40, 223,37)
L_Stempniak = Player('Lee Stempniak', 'TOT', 'RW', 71, 15, 13, 115, 23,71, 15, 13, 115,23)
D_Stepan = Player('Derek Stepan', 'NYR', 'C', 68, 16, 39, 155, 27,68, 16, 39, 155,27)
C_Stewart = Player('Chris Stewart', 'TOT', 'RW', 81, 14, 22, 155, 16,81, 14, 22, 155,16)
J_Stoll = Player('Jarret Stoll', 'LAK', 'C', 73, 6, 11, 83, 53,73, 6, 11, 83,53)
K_Stollery = Player('Karl Stollery', 'TOT', 'D', 10, 0, 0, 9, 21,10, 0, 0, 9,21)
M_Stone = Player('Mark Stone', 'OTT', 'RW', 80, 26, 38, 157, 53,80, 26, 38, 157,53)
M_Stone = Player('Michael Stone', 'ARI', 'D', 81, 3, 15, 144, 189,81, 3, 15, 144,189)
C_Stoner = Player('Clayton Stoner', 'ANA', 'D', 69, 1, 7, 68, 84,69, 1, 7, 68,84)
T_Strachan = Player('Tyson Strachan', 'BUF', 'D', 46, 0, 5, 38, 105,46, 0, 5, 38,105)
B_Strait = Player('Brian Strait', 'NYI', 'D', 52, 2, 5, 59, 85,52, 2, 5, 59,85)
P_Straka = Player('Petr Straka', 'PHI', 'RW', 3, 0, 2, 2, 1,3, 0, 2, 2,1)
A_Stralman = Player('Anton Stralman', 'TBL', 'D', 82, 9, 30, 138, 79,82, 9, 30, 138,79)
B_Street = Player('Ben Street', 'COL', 'C', 3, 0, 0, 4, 0,3, 0, 0, 4,0)
M_Streit = Player('Mark Streit', 'PHI', 'D', 81, 9, 43, 144, 103,81, 9, 43, 144,103)
R_Strome = Player('Ryan Strome', 'NYI', 'C', 81, 17, 33, 179, 21,81, 17, 33, 179,21)
B_Stuart = Player('Brad Stuart', 'COL', 'D', 65, 3, 10, 64, 134,65, 3, 10, 64,134)
M_Stuart = Player('Mark Stuart', 'WPG', 'D', 70, 2, 12, 51, 142,70, 2, 12, 51,142)
P_Subban = Player('P.K. Subban', 'MTL', 'D', 82, 15, 45, 170, 142,82, 15, 45, 170,142)
C_Summers = Player('Chris Summers', 'TOT', 'D', 20, 0, 3, 15, 26,20, 0, 3, 15,26)
A_Sustr = Player('Andrej Sustr', 'TBL', 'D', 72, 0, 13, 55, 84,72, 0, 13, 55,84)
R_Suter = Player('Ryan Suter', 'MIN', 'D', 77, 2, 36, 150, 127,77, 2, 36, 150,127)
B_Sutter = Player('Brandon Sutter', 'PIT', 'C', 80, 21, 12, 180, 48,80, 21, 12, 180,48)
B_Sutter = Player('Brett Sutter', 'MIN', 'C', 6, 0, 3, 6, 1,6, 0, 3, 6,1)
B_Sutter = Player('Brody Sutter', 'CAR', 'C', 4, 0, 0, 0, 2,4, 0, 0, 0,2)
J_Szwarz = Player('Jordan Szwarz', 'ARI', 'RW', 9, 1, 0, 8, 9,9, 1, 0, 8,9)
M_Talbot = Player('Maxime Talbot', 'TOT', 'C', 81, 5, 13, 97, 51,81, 5, 13, 97,51)
C_Tanev = Player('Chris Tanev', 'VAN', 'D', 70, 2, 18, 53, 170,70, 2, 18, 53,170)
E_Tangradi = Player('Eric Tangradi', 'MTL', 'LW', 7, 0, 0, 5, 4,7, 0, 0, 5,4)
A_Tanguay = Player('Alex Tanguay', 'COL', 'LW', 80, 22, 33, 104, 39,80, 22, 33, 104,39)
V_Tarasenko = Player('Vladimir Tarasenko', 'STL', 'RW', 77, 37, 36, 264, 18,77, 37, 36, 264,18)
D_Tarasov = Player('Daniil Tarasov', 'SJS', 'RW', 5, 0, 1, 5, 1,5, 0, 1, 5,1)
T_Tatar = Player('Tomas Tatar', 'DET', 'C', 82, 29, 27, 211, 18,82, 29, 27, 211,18)
J_Tavares = Player('John Tavares', 'NYI', 'C', 82, 38, 48, 278, 37,82, 38, 48, 278,37)
M_Tennyson = Player('Matt Tennyson', 'SJS', 'D', 27, 2, 6, 37, 34,27, 2, 6, 37,34)
T_Teravainen = Player('Teuvo Teravainen', 'CHI', 'LW', 34, 4, 5, 66, 14,34, 4, 5, 66,14)
C_Terry = Player('Chris Terry', 'CAR', 'LW', 57, 11, 9, 71, 17,57, 11, 9, 71,17)
C_Thomas = Player('Christian Thomas', 'MTL', 'LW', 18, 1, 0, 26, 3,18, 1, 0, 26,3)
N_Thompson = Player('Nate Thompson', 'ANA', 'C', 80, 5, 13, 87, 52,80, 5, 13, 87,52)
C_Thorburn = Player('Chris Thorburn', 'WPG', 'RW', 81, 7, 7, 67, 29,81, 7, 7, 67,29)
J_Thornton = Player('Joe Thornton', 'SJS', 'C', 78, 16, 49, 131, 24,78, 16, 49, 131,24)
S_Thornton = Player('Shawn Thornton', 'FLA', 'LW', 46, 1, 4, 53, 5,46, 1, 4, 53,5)
C_Tierney = Player('Chris Tierney', 'SJS', 'C', 43, 6, 15, 48, 17,43, 6, 15, 48,17)
K_Timonen = Player('Kimmo Timonen', 'CHI', 'D', 16, 0, 0, 10, 15,16, 0, 0, 10,15)
J_Tinordi = Player('Jarred Tinordi', 'MTL', 'D', 13, 0, 2, 5, 18,13, 0, 2, 5,18)
J_Tlusty = Player('Jiri Tlusty', 'TOT', 'LW', 72, 14, 17, 123, 39,72, 14, 17, 123,39)
J_Toews = Player('Jonathan Toews', 'CHI', 'C', 81, 28, 38, 192, 16,81, 28, 38, 192,16)
T_Toffoli = Player('Tyler Toffoli', 'LAK', 'C', 76, 23, 26, 200, 11,76, 23, 26, 200,11)
J_Tootoo = Player('Jordin Tootoo', 'NJD', 'RW', 68, 10, 5, 75, 8,68, 10, 5, 75,8)
V_Trocheck = Player('Vincent Trocheck', 'FLA', 'C', 50, 7, 15, 89, 19,50, 7, 15, 89,19)
C_Tropp = Player('Corey Tropp', 'CBJ', 'RW', 61, 1, 7, 22, 28,61, 1, 7, 22,28)
Z_Trotman = Player('Zach Trotman', 'BOS', 'D', 27, 1, 4, 46, 33,27, 1, 4, 46,33)
J_Trouba = Player('Jacob Trouba', 'WPG', 'D', 65, 7, 15, 133, 120,65, 7, 15, 133,120)
K_Turris = Player('Kyle Turris', 'OTT', 'C', 82, 24, 40, 215, 40,82, 24, 40, 215,40)
D_Tyrell = Player('Dana Tyrell', 'CBJ', 'C', 3, 0, 0, 1, 3,3, 0, 0, 1,3)
F_Tyutin = Player('Fedor Tyutin', 'CBJ', 'D', 67, 3, 12, 56, 117,67, 3, 12, 56,117)
D_Uher = Player('Dominik Uher', 'PIT', 'C', 2, 0, 0, 0, 1,2, 0, 0, 0,1)
R_Umberger = Player('R.J. Umberger', 'PHI', 'LW', 67, 9, 6, 96, 40,67, 9, 6, 96,40)
S_Upshall = Player('Scottie Upshall', 'FLA', 'LW', 63, 8, 7, 93, 27,63, 8, 7, 93,27)
D_Gulik = Player('David Van Der Gulik', 'LAK', 'LW', 1, 0, 0, 1, 0,1, 0, 0, 1,0)
J_Riemsdyk = Player('James van Riemsdyk', 'TOR', 'LW', 82, 27, 29, 248, 29,82, 27, 29, 248,29)
T_Riemsdyk = Player('Trevor van Riemsdyk', 'CHI', 'D', 18, 0, 1, 21, 15,18, 0, 1, 21,15)
C_VandeVelde = Player('Chris VandeVelde', 'PHI', 'C', 72, 9, 6, 70, 46,72, 9, 6, 70,46)
T_Vanek = Player('Thomas Vanek', 'MIN', 'LW', 80, 21, 31, 171, 13,80, 21, 31, 171,13)
P_Varone = Player('Philip Varone', 'BUF', 'C', 28, 3, 2, 28, 22,28, 3, 2, 28,22)
S_Vatanen = Player('Sami Vatanen', 'ANA', 'D', 67, 12, 25, 122, 123,67, 12, 25, 122,123)
S_Veilleux = Player('Stephane Veilleux', 'MIN', 'LW', 12, 1, 1, 9, 8,12, 1, 1, 9,8)
A_Vermette = Player('Antoine Vermette', 'TOT', 'C', 82, 13, 25, 109, 50,82, 13, 25, 109,50)
K_Versteeg = Player('Kris Versteeg', 'CHI', 'LW', 61, 14, 20, 134, 22,61, 14, 20, 134,22)
L_Vey = Player('Linden Vey', 'VAN', 'RW', 75, 10, 14, 61, 9,75, 10, 14, 61,9)
T_Vincour = Player('Tomas Vincour', 'COL', 'C', 7, 0, 1, 2, 4,7, 0, 1, 2,4)
L_Visnovsky = Player('Lubomir Visnovsky', 'NYI', 'D', 53, 5, 15, 85, 61,53, 5, 15, 85,61)
J_Vitale = Player('Joe Vitale', 'ARI', 'C', 70, 3, 6, 55, 65,70, 3, 6, 55,65)
M_Vlasic = Player('Marc-Edouard Vlasic', 'SJS', 'D', 70, 9, 14, 98, 112,70, 9, 14, 98,112)
A_Volchenkov = Player('Anton Volchenkov', 'NSH', 'D', 46, 0, 7, 35, 48,46, 0, 7, 35,48)
A_Volpatti = Player('Aaron Volpatti', 'WSH', 'LW', 2, 0, 0, 1, 1,2, 0, 0, 1,1)
J_Voracek = Player('Jakub Voracek', 'PHI', 'RW', 82, 22, 59, 221, 28,82, 22, 59, 221,28)
S_Voynov = Player('Slava Voynov', 'LAK', 'D', 6, 0, 2, 5, 8,6, 0, 2, 5,8)
R_Vrbata = Player('Radim Vrbata', 'VAN', 'RW', 79, 31, 32, 267, 25,79, 31, 32, 267,25)
C_Wagner = Player('Chris Wagner', 'ANA', 'RW', 9, 0, 0, 7, 3,9, 0, 0, 7,3)
J_Ward = Player('Joel Ward', 'WSH', 'RW', 82, 19, 15, 138, 38,82, 19, 15, 138,38)
D_Warsofsky = Player('David Warsofsky', 'BOS', 'D', 4, 0, 1, 7, 2,4, 0, 1, 7,2)
M_Weaver = Player('Mike Weaver', 'MTL', 'D', 31, 0, 4, 8, 61,31, 0, 4, 8,61)
M_Weber = Player('Mike Weber', 'BUF', 'D', 64, 1, 6, 41, 168,64, 1, 6, 41,168)
S_Weber = Player('Shea Weber', 'NSH', 'D', 78, 15, 30, 237, 147,78, 15, 30, 237,147)
Y_Weber = Player('Yannick Weber', 'VAN', 'D', 65, 11, 10, 117, 62,65, 11, 10, 117,62)
D_Weise = Player('Dale Weise', 'MTL', 'RW', 79, 10, 19, 91, 34,79, 10, 19, 91,34)
S_Weiss = Player('Stephen Weiss', 'DET', 'C', 52, 9, 16, 52, 12,52, 9, 16, 52,12)
A_Wennberg = Player('Alexander Wennberg', 'CBJ', 'C', 68, 4, 16, 85, 45,68, 4, 16, 85,45)
B_Wheeler = Player('Blake Wheeler', 'WPG', 'RW', 79, 26, 35, 244, 54,79, 26, 35, 244,54)
R_White = Player('Ryan White', 'PHI', 'C', 34, 6, 6, 45, 14,34, 6, 6, 45,14)
J_Whitney = Player('Joe Whitney', 'NJD', 'RW', 4, 1, 0, 1, 0,4, 1, 0, 1,0)
D_Wideman = Player('Dennis Wideman', 'CGY', 'D', 80, 15, 41, 173, 184,80, 15, 41, 173,184)
P_Wiercioch = Player('Patrick Wiercioch', 'OTT', 'D', 56, 3, 10, 79, 44,56, 3, 10, 79,44)
J_Williams = Player('Justin Williams', 'LAK', 'RW', 81, 18, 23, 174, 24,81, 18, 23, 174,24)
C_Wilson = Player('Colin Wilson', 'NSH', 'C', 77, 20, 22, 172, 33,77, 20, 22, 172,33)
G_Wilson = Player('Garrett Wilson', 'FLA', 'LW', 2, 0, 0, 5, 1,2, 0, 0, 5,1)
R_Wilson = Player('Ryan Wilson', 'COL', 'D', 3, 0, 0, 3, 3,3, 0, 0, 3,3)
T_Wilson = Player('Tom Wilson', 'WSH', 'RW', 67, 4, 13, 79, 24,67, 4, 13, 79,24)
T_Wingels = Player('Tommy Wingels', 'SJS', 'C', 75, 15, 21, 158, 55,75, 15, 21, 158,55)
D_Winnik = Player('Daniel Winnik', 'TOT', 'C', 79, 9, 25, 97, 69,79, 9, 25, 97,69)
J_Wisniewski = Player('James Wisniewski', 'TOT', 'D', 69, 8, 26, 147, 81,69, 8, 26, 147,81)
L_Witkowski = Player('Luke Witkowski', 'TBL', 'D', 16, 0, 0, 10, 22,16, 0, 0, 10,22)
D_Wolf = Player('David Wolf', 'CGY', 'LW', 3, 0, 0, 1, 0,3, 0, 0, 1,0)
B_Woods = Player('Brendan Woods', 'CAR', 'LW', 2, 0, 0, 3, 0,2, 0, 0, 3,0)
T_Wotherspoon = Player('Tyler Wotherspoon', 'CGY', 'D', 1, 0, 0, 1, 4,1, 0, 0, 1,4)
B_Yakimov = Player('Bogdan Yakimov', 'EDM', 'C', 1, 0, 0, 1, 0,1, 0, 0, 1,0)
N_Yakupov = Player('Nail Yakupov', 'EDM', 'RW', 81, 14, 19, 191, 28,81, 14, 19, 191,28)
K_Yandle = Player('Keith Yandle', 'TOT', 'D', 84, 6, 46, 232, 101,84, 6, 46, 232,101)
N_Zadorov = Player('Nikita Zadorov', 'BUF', 'D', 60, 3, 12, 52, 73,60, 3, 12, 52,73)
T_Zajac = Player('Travis Zajac', 'NJD', 'C', 74, 11, 14, 112, 35,74, 11, 14, 112,35)
H_Zetterberg = Player('Henrik Zetterberg', 'DET', 'C', 77, 17, 49, 227, 26,77, 17, 49, 227,26)
M_Zibanejad = Player('Mika Zibanejad', 'OTT', 'C', 80, 20, 26, 150, 26,80, 20, 26, 150,26)
M_Zidlicky = Player('Marek Zidlicky', 'TOT', 'D', 84, 7, 27, 130, 92,84, 7, 27, 130,92)
H_Zolnierczyk = Player('Harry Zolnierczyk', 'NYI', 'LW', 2, 0, 0, 1, 1,2, 0, 0, 1,1)
D_Zubrus = Player('Dainius Zubrus', 'NJD', 'C', 74, 4, 6, 72, 40,74, 4, 6, 72,40)
M_Zuccarello = Player('Mats Zuccarello', 'NYR', 'LW', 78, 15, 34, 154, 42,78, 15, 34, 154,42)
J_Zucker = Player('Jason Zucker', 'MIN', 'LW', 51, 21, 5, 124, 13,51, 21, 5, 124,13)

# Goalies
C_Price = Goalie('Carey Price', 'MTL', 'G', 66, 44, 1953, 130, 9, 428, 225, 12957, 1044, 34)
P_Rinne = Goalie('Pekka Rinne', 'NSH', 'G', 64, 41, 1807, 140, 4, 372, 206, 10692, 863, 37)
B_Holtby = Goalie('Braden Holtby', 'WSH', 'G', 72, 41, 2044, 157, 9, 171, 102, 5190, 413, 20)
B_Bishop = Goalie('Ben Bishop', 'TBL', 'G', 60, 40, 1620, 136, 4, 164, 98, 4682, 382, 12)
J_Halak = Goalie('Jaroslav Halak', 'NYI', 'G', 59, 38, 1673, 144, 6, 323, 182, 9156, 760, 36)
J_Quick = Goalie('Jonathan Quick', 'LAK', 'G', 71, 36, 1896, 156, 6, 402, 212, 10705, 911, 37)
D_Dubnyk = Goalie('Devan Dubnyk', 'ARI, MIN', 'G', 55, 36, 1625, 115, 6, 216, 99, 6819, 589, 14)
F_Andersen = Goalie('Frederik Andersen', 'ANA', 'G', 53, 35, 1436, 123, 3, 79, 55, 2288, 186, 3)
T_Rask = Goalie('Tuukka Rask', 'BOS', 'G', 67, 34, 2011, 156, 3, 254, 136, 7554, 564, 26)
K_Lehtonen = Goalie('Kari Lehtonen', 'DAL', 'G', 65, 34, 1875, 181, 5, 498, 248, 15307, 1323, 32)
M_Fleury = Goalie('Marc-Andre Fleury', 'PIT', 'G', 64, 34, 1831, 146, 10, 577, 322, 16704, 1479, 38)
C_Crawford = Goalie('Corey Crawford', 'CHI', 'G', 57, 32, 1661, 126, 2, 258, 148, 7266, 606, 12)
A_Niemi = Goalie('Antti Niemi', 'SJS', 'G', 61, 31, 1811, 155, 5, 335, 191, 9402, 792, 33)
S_Bobrovsky = Goalie('Sergei Bobrovsky', 'CBJ', 'G', 49, 30, 1632, 134, 2, 224, 125, 6791, 559, 11)
H_Lundqvist = Goalie('Henrik Lundqvist', 'NYR', 'G', 46, 30, 1329, 103, 5, 615, 342, 17504, 1387, 55)
R_Miller = Goalie('Ryan Miller', 'VAN', 'G', 45, 29, 1198, 107, 6, 598, 325, 17986, 1528, 35)
R_Luongo = Goalie('Roberto Luongo', 'FLA', 'G', 61, 28, 1743, 138, 2, 842, 402, 25630, 2069, 68)
S_Varlamov = Goalie('Semyon Varlamov', 'COL', 'G', 57, 28, 1791, 141, 5, 257, 137, 8074, 665, 18)
J_Hiller = Goalie('Jonas Hiller', 'CGY', 'G', 44, 26, 1376, 113, 1, 353, 189, 10598, 883, 22)
C_Schneider = Goalie('Cory Schneider', 'NJD', 'G', 68, 26, 1982, 148, 5, 198, 97, 5834, 436, 17)
B_Elliott = Goalie('Brian Elliott', 'STL', 'G', 45, 26, 1150, 96, 5, 257, 143, 7143, 631, 30)
J_Howard = Goalie('Jimmy Howard', 'DET', 'G', 50, 23, 1350, 121, 2, 331, 176, 9385, 790, 21)
O_Pavelec = Goalie('Ondrej Pavelec', 'WPG', 'G', 46, 22, 1353, 108, 5, 325, 136, 9907, 914, 16)
C_Ward = Goalie('Cam Ward', 'CAR', 'G', 50, 22, 1351, 121, 1, 502, 246, 14792, 1338, 22)
J_Allen = Goalie('Jake Allen', 'STL', 'G', 32, 22, 909, 79, 4, 46, 31, 1274, 115, 5)
C_Talbot = Goalie('Cam Talbot', 'NYR', 'G', 34, 21, 1038, 77, 5, 55, 33, 1654, 114, 8)
J_Bernier = Goalie('Jonathan Bernier', 'TOR', 'G', 55, 21, 1735, 152, 2, 160, 76, 5112, 431, 9)
M_Hutchinson = Goalie('Michael Hutchinson', 'WPG', 'G', 36, 21, 986, 85, 2, 40, 24, 1095, 91, 2)
A_Hammond = Goalie('Andrew Hammond', 'OTT', 'G', 23, 20, 707, 42, 3, 23, 20, 718, 42, 3)
E_Lack = Goalie('Eddie Lack', 'VAN', 'G', 35, 18, 1201, 95, 2, 72, 34, 2253, 188, 6)
J_Enroth = Goalie('Jhonas Enroth', 'BUF, DAL', 'G', 44, 18, 1504, 145, 2, 115, 43, 3840, 348, 5)
S_Mason = Goalie('Steve Mason', 'PHI', 'G', 48, 18, 1490, 108, 3, 341, 151, 10049, 906, 26)
P_Mrazek = Goalie('Petr Mrazek', 'DET', 'G', 26, 16, 768, 63, 3, 35, 20, 1044, 83, 5)
B_Scrivens = Goalie('Ben Scrivens', 'EDM', 'G', 53, 15, 1542, 170, 1, 116, 42, 3648, 345, 7)
K_Ramo = Goalie('Karri Ramo', 'CGY', 'G', 32, 15, 852, 75, 2, 110, 43, 3398, 325, 4)
M_Smith = Goalie('Mike Smith', 'ARI', 'G', 61, 14, 1955, 187, 0, 371, 163, 11281, 988, 27)
D_Kuemper = Goalie('Darcy Kuemper', 'MIN', 'G', 28, 14, 718, 68, 3, 56, 27, 1539, 138, 5)
C_Anderson = Goalie('Craig Anderson', 'OTT', 'G', 35, 14, 1134, 87, 3, 381, 184, 12367, 1046, 29)
J_Gibson = Goalie('John Gibson', 'ANA', 'G', 21, 13, 674, 58, 1, 24, 16, 761, 62, 2)
C_McElhinney = Goalie('Curtis McElhinney', 'CBJ', 'G', 28, 12, 949, 82, 0, 93, 41, 3270, 310, 4)
T_Greiss = Goalie('Thomas Greiss', 'PIT', 'G', 18, 9, 546, 50, 0, 72, 37, 2305, 200, 3)
R_Lehner = Goalie('Robin Lehner', 'OTT', 'G', 24, 9, 779, 74, 0, 77, 30, 2688, 231, 2)
J_Reimer = Goalie('James Reimer', 'TOR', 'G', 27, 9, 1001, 93, 0, 160, 74, 5245, 459, 11)
S_Darling = Goalie('Scott Darling', 'CHI', 'G', 13, 9, 419, 27, 1, 14, 10, 448, 28, 1)
C_Johnson = Goalie('Chad Johnson', 'NYI', 'G', 17, 8, 488, 54, 0, 50, 29, 1514, 132, 3)
A_Stalock = Goalie('Alex Stalock', 'SJS', 'G', 19, 8, 553, 54, 2, 37, 21, 1146, 95, 4)
A_Khudobin = Goalie('Anton Khudobin', 'CAR', 'G', 32, 8, 874, 87, 1, 85, 41, 2517, 205, 4)
M_Neuvirth = Goalie('Michal Neuvirth', 'BUF, NYI', 'G', 32, 7, 1067, 92, 0, 152, 67, 4829, 425, 8)
A_Vasilevskiy = Goalie('Andrei Vasilevskiy', 'TBL', 'G', 13, 7, 415, 34, 1, 13, 7, 415, 34, 1)
A_Raanta = Goalie('Antti Raanta', 'CHI', 'G', 12, 7, 389, 25, 2, 34, 20, 999, 88, 3)
A_Montoya = Goalie('Al Montoya', 'FLA', 'G', 13, 6, 453, 49, 0, 88, 43, 2895, 269, 5)
C_Hutton = Goalie('Carter Hutton', 'NSH', 'G', 17, 6, 450, 44, 1, 52, 26, 1484, 138, 2)
C_Pickard = Goalie('Calvin Pickard', 'COL', 'G', 13, 6, 511, 35, 0, 13, 6, 511, 35, 0)
A_Lindback = Goalie('Anders Lindback', 'DAL, BUF', 'G', 22, 6, 798, 73, 0, 89, 40, 2960, 280, 3)
K_Kinkaid = Goalie('Keith Kinkaid', 'NJD', 'G', 13, 6, 469, 40, 0, 14, 6, 508, 45, 0)
D_Tokarski = Goalie('Dustin Tokarski', 'MTL', 'G', 16, 6, 509, 46, 0, 23, 9, 734, 68, 1)
R_Berra = Goalie('Reto Berra', 'COL', 'G', 12, 5, 403, 33, 1, 41, 14, 1223, 121, 1)
N_Backstrom = Goalie('Niklas Backstrom', 'MIN', 'G', 14, 5, 452, 51, 0, 391, 194, 11283, 962, 28)
J_Ortio = Goalie('Joni Ortio', 'CGY', 'G', 6, 4, 153, 14, 1, 15, 8, 346, 35, 1)
D_Ellis = Goalie('Dan Ellis', 'FLA', 'G', 8, 4, 221, 19, 1, 181, 87, 5579, 526, 15)
M_Jones = Goalie('Martin Jones', 'LAK', 'G', 11, 4, 307, 29, 3, 31, 18, 854, 63, 8)
J_Peters = Goalie('Justin Peters', 'WSH', 'G', 9, 3, 294, 35, 0, 67, 25, 2243, 223, 3)
R_Bachman = Goalie('Richard Bachman', 'EDM', 'G', 4, 3, 168, 15, 1, 30, 17, 1020, 98, 2)
J_Gustavsson = Goalie('Jonas Gustavsson', 'DET', 'G', 6, 3, 168, 15, 1, 132, 60, 3956, 392, 6)
J_LaBarbera = Goalie('Jason LaBarbera', 'ANA', 'G', 2, 2, 99, 9, 0, 148, 62, 4933, 457, 6)
M_Skapski = Goalie('Mackenzie Skapski', 'NYR', 'G', 2, 2, 45, 1, 1, 2, 2, 45, 1, 1)
P_Grubauer = Goalie('Philipp Grubauer', 'WSH', 'G', 1, 1, 25, 2, 0, 16, 7, 553, 42, 0)
L_Domingue = Goalie('Louis Domingue', 'ARI', 'G', 4, 1, 158, 14, 0, 4, 1, 158, 14, 0)
T_Grosenick = Goalie('Troy Grosenick', 'SJS', 'G', 2, 1, 58, 3, 1, 2, 1, 58, 3, 1)
J_Markstrom = Goalie('Jacob Markstrom', 'VAN', 'G', 2, 1, 33, 4, 0, 43, 13, 1315, 137, 0)
M_Subban = Goalie('Malcolm Subban', 'BOS', 'G', 1, 0, 6, 3, 0, 1, 0, 6, 3, 0)
L_Brossoit = Goalie('Laurent Brossoit', 'EDM', 'G', 1, 0, 51, 2, 0, 1, 0, 51, 2, 0)
A_Makarov = Goalie('Andrey Makarov', 'BUF', 'G', 1, 0, 36, 3, 0, 1, 0, 36, 3, 0)
K_Poulin = Goalie('Kevin Poulin', 'NYI', 'G', 1, 0, 26, 3, 0, 44, 18, 1392, 140, 0)
A_Forsberg = Goalie('Anton Forsberg', 'CBJ', 'G', 5, 0, 149, 20, 0, 5, 0, 149, 20, 0)
M_Hackett = Goalie('Matt Hackett', 'BUF', 'G', 4, 0, 155, 18, 0, 20, 4, 709, 67, 0)
M_McKenna = Goalie('Mike McKenna', 'ARI', 'G', 1, 0, 34, 5, 0, 19, 5, 610, 68, 1)
M_Mazanec = Goalie('Marek Mazanec', 'NSH', 'G', 1, 0, 47, 4, 0, 23, 8, 697, 68, 2)

##--------------------------------------
def create_teams():
    # Start Timer
    start = timeit.default_timer()

    # Opens document 'Players_Class.txt' and creates a list of Players
    #    - Uses eval() to evaluate the string obtained from the document
    #    - all_players_class is a list of all the classes of Players
    #    - all_players is a list of all the players names as strings
    plr_doc = open('Players_Class.txt','r')
    plr_doc = plr_doc.readlines()
    all_players_class = []
    for line in plr_doc:
        plr = eval(line)
        all_players_class += [plr]
    all_players = list(map((lambda x: x.name), all_players_class))

    # Opens document 'Goalies_Class.txt' and creates a list of Goalies
    #    - Uses eval() to evaluate the string obtained from the document
    #    - all_goalies_class is a list of all the classes of Goalies
    #    - all_goalies is a list of all the goalie's names as strings
    gol_doc = open('Goalies_Class.txt','r')
    gol_doc = gol_doc.readlines()
    all_goalies_class = []
    for line in gol_doc:
        gol = eval(line)
        all_goalies_class += [gol]
    all_goalies = list(map((lambda x: x.name), all_goalies_class))

    # Scans document 'DailyCosts.txt' for strings of player's names
    #    - daily_players is all players and goalies names as strings that
    #      are in both DailyCosts.txt and Goalies_Class.txt or Players_Class.txt
    daily_players = []
    for line in daily:
        if line[:len(line)-1] in all_players:
            daily_players += [line[:len(line)-1]]
        elif line[:len(line)-1] in all_goalies:
            daily_players += [line[:len(line)-1]]
        else:
            pass

    # Transverses lists daily_players and all_players_class to find names of players
    #      that are in both lists then makes a list of those players as classes
    #    - daily_players_class is all the classes of Players that are
    #      also in DailyCosts.txt
    daily_players_class = []
    for plr_str in daily_players:
        for plr_cl in all_players_class:
            if plr_str == plr_cl.name:
                daily_players_class += [plr_cl]
            else:
                pass

    # Transverses lists daily_players and all_goalies_classes to find names of goalies
    #      that are in both lists then makes a list of those goalies as classes
    #    - daily_goalies_class is all the classes of Goalies that are
    #      also in DailyCosts.txt
    daily_goalies_class = []
    for plr_str in daily_players:
        for gol_cl in all_goalies_class:
            if plr_str == gol_cl.name:
                daily_goalies_class += [gol_cl]

    # Create lists of Players my filtering by their position
    #    - goalies is all the Goalies in daily_goalies_class that meet the requirements
    #    - centers is all the Centers in daily_players_class that meet the requirements
    #    - wingers is all the Wingers in daily_players_class that meet the requirements
    #    - defense is all the Defenceman in daily_players_class
    goalies = list(filter((lambda x: x.dpp() < 1500 and x.ev_int() > 5), daily_goalies_class))
    centers = list(filter((lambda x: x.pos == 'C' and x.ev_int() > 3.375), daily_players_class))
    wingers = list(filter((lambda x: x.pos == ('LW' or x.pos == 'RW') and x.ev_int() > 3.3),\
                          daily_players_class))
    defence = list(filter((lambda x: x.pos == 'D' and x.ev_int() > 3.25), daily_players_class))
    # Create lists of eligible player's prefix that meet requirements for later use of eval()
    #    - goalie_names is a list of goalie's prefix' as strings
    #    - center_names is a list of center's prefix' as strings
    #    - winger_names is a list of winger's prefix' as strings
    #    - defenceman_names is a list of defenceman's prefix' as strings
    goalie_names = ['B_Holtby'] # User input or 'list(map((lambda x: x.prefix()),goalies))'
    center_names = list(map((lambda x: x.prefix()),centers))
    winger_names = list(map((lambda x: x.prefix()),wingers))
    defenceman_names = list(map((lambda x: x.prefix()),defence))
    #print(defenceman_names)------------------------------------------
    # Creates a lists of eligible player's expected value for final document
    #    - center_ev is a list of all the center's expected values
    #    - winger_ev is a list of all the winger's expected values
    #    - defenceman_ev is a list of all the defenceman's expected values
    center_ev = list(map((lambda x: x.ev()),centers))
    winger_ev = list(map((lambda x: x.ev()),wingers))
    defenceman_ev = list(map((lambda x: x.ev()),defence))

    # Print number of eligible players for each position in order
    #      to adjust eligiable player pool to reasonable size
    print('Eligible Goalies: ' + str(len(goalie_names)))
    print('Eligible Centers: ' + str(len(center_names)))
    print('Eligible Wingers: ' + str(len(winger_names)))
    print('Eligible Defencemen: ' + str(len(defenceman_names)))







    # Efficient Combos
    ug = list(itertools.combinations(goalie_names,1))
    #Combo 1
    c1d = list(itertools.combinations(defenceman_names,3))
    c1w = list(itertools.combinations(winger_names,3))
    c1c = list(itertools.combinations(center_names,2))
    #Combo 2
    c2d = list(itertools.combinations(defenceman_names,2))
    c2w = list(itertools.combinations(winger_names,4))
    c2c = list(itertools.combinations(center_names,2))
    #Combo 3
    c3d = list(itertools.combinations(defenceman_names,2))
    c3w = list(itertools.combinations(winger_names,3))
    c3c = list(itertools.combinations(center_names,3))

    all_team = []
    #Make Teams With Combo 1
    for gol in ug:
        this_team = []
        for dman in c1d:
            for wing in c1w:
                for cent in c1c:
                    this_team = gol+dman+wing+cent
                    all_team += [this_team]
    #Make Teams With Combo 2
    for gol in ug:
        this_team = []
        for dman in c2d:
            for wing in c2w:
                for cent in c2c:
                    this_team = gol+dman+wing+cent
                    all_team += [this_team]
    #Make Teams With Combo 3
    for gol in ug:
        this_team = []
        for dman in c3d:
            for wing in c3w:
                for cent in c3c:
                    this_team = gol+dman+wing+cent
                    all_team += [this_team]



    new_comb_lst = ''
    for team in all_team:
        new_comb_lst += 'Team('+ str(team) + ')\n'

    team_file = open('Team_File.txt', 'w')
    team_file.write(str(new_comb_lst))
    team_file.close()

    created_teams = open('Team_File.txt','r')
    created_teams = created_teams.readlines()


    teams_class = []
    for line in created_teams:
        team = eval(line)
        plrs_as_class = []
        for plr_str in team.plr_lst:
            plr_cl = eval(plr_str)
            plrs_as_class += [plr_cl]
        team.switch(plrs_as_class)
        teams_class += [team]

    make_combo_start = timeit.default_timer() #----------------
    valid_teams = list(filter((lambda x: x.cost() <= 50000), teams_class))
    make_combo_end = timeit.default_timer() #----------------
    time_test_start = timeit.default_timer() #-------------------
    print('Valid Teams: ' + str(len(valid_teams)))

    val_teams_ev = list(map((lambda x: x.ev()),valid_teams))

    val_teams_ev = sorted(val_teams_ev)[::-1]

    top1 = val_teams_ev[0]
    top2 = val_teams_ev[1]
    top3 = val_teams_ev[2]
    top4 = val_teams_ev[3]
    top1p = val_teams_ev[random.randint(4,int(len(valid_teams)*0.01))]

    todays_teams = ''
    todays_random_teams = ''
    for team in valid_teams:
        if team.ev() == top1:
            full_team = team.players()+'\n'
            todays_teams += full_team + '\n'
            break
        else:
            pass
    for team in valid_teams:
        if team.ev() == top2:
            full_team = team.players()+'\n'
            todays_teams += full_team + '\n'
            break
        else:
            pass
    for team in valid_teams:
        if team.ev() == top3:
            full_team = team.players()+'\n'
            todays_teams += full_team + '\n'
            break
        else:
            pass
    for team in valid_teams:
        if team.ev() == top4:
            full_team = team.players()+'\n'
            todays_teams += full_team + '\n'
            break
        else:
            pass
    for team in valid_teams:
        if team.ev() == top1p:
            full_team = team.players()+'\n'
            todays_teams += full_team + '\n'
            break
        else:
            pass
    time_test_end = timeit.default_timer() #----------------


    team_file = open('Todays_Teams.txt', 'w')
    team_file.write("Today's Teams:\n\n")
    team_file.write(todays_teams)
    team_file.write('\nValid Teams: ' + str(len(valid_teams)) + \
                    '\n Total Players: ' + str(len(goalie_names)+len(defenceman_names)+len(winger_names)+len(center_names)))
    team_file.write('\n'+'-'*(len(todays_teams)//5))
    team_file.write('\nPlayer Pool')
    team_file.write('\nCenters: ' + str(center_ev))
    team_file.write('\nWingers: ' + str(winger_ev))
    team_file.write('\nDefence: ' + str(defenceman_ev))
    cur_time = timeit.default_timer()
    team_file.write('\nMinutes: ' + str((cur_time-start)/60))
    team_file.close()


    # End Timer
    stop = timeit.default_timer()
    sec = stop - start
    minu = sec/60
    hours = minu/60
    print('')
    print('Seconds: ' + str(sec))
    print('Minutes: ' + str(minu))
    print('Hours: ' + str(hours))
    print('Make Combos Time: ' + str(make_combo_end - make_combo_start))
    print('Make File Time: ' + str(time_test_end - time_test_start))



