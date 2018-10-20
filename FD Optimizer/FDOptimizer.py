import itertools
import datetime
import timeit
import requests
import math
from bs4 import BeautifulSoup

# Set up timer and date
start_timer = timeit.default_timer()
now = datetime.datetime.now()

today_date = now.day
today_month = now.month
# Makes the date into a string and adds '0' if needed to avoid error
# None -> Str
def get_date():
        day = str(today_date)
        month = str(today_month)
        if len(str(today_date)) == 1:
                day = "0"+str(today_date)
        if len(str(today_month)) == 1:
                month = "0"+str(today_month)
        return str(now.year)+month+day
today = get_date()

# Todays Costs:
DailyCosts = open('FDDaily.txt','r')
DailyCosts = DailyCosts.readlines() + ["\n"]


# Skaters 2016
skaters_2016 = requests.get("http://www.hockey-reference.com/leagues/NHL_2016_skaters.html")
skaters_2016_source = BeautifulSoup(skaters_2016.content, "html.parser")
# Goalies 2016
goalies_2016 = requests.get("http://www.hockey-reference.com/leagues/NHL_2016_goalies.html")
goalies_2016_source = BeautifulSoup(goalies_2016.content, "html.parser")
# Matchup Stats
matchups = requests.get("http://www.hockey-reference.com/leagues/NHL_2016_games.html")
matchups_source = BeautifulSoup(matchups.content, "html.parser")
# Injuries
injuries = requests.get("http://www.rotoworld.com/teams/injuries/nhl/all/")
injuries_source = BeautifulSoup(injuries.content, "html.parser")
# Team Standings:
Team_Standings = requests.get("http://www.hockey-reference.com/leagues/NHL_2016_standings.html")
Team_Standings_Source = BeautifulSoup(Team_Standings.content, "html.parser")

def full_names():
        names_lst = []
        for i in range(len(DailyCosts)-1):
                line1 = DailyCosts[i]
                line2 = DailyCosts[i+1]
                name1 = line1[:len(line1)-1]
                name2 = line2[:len(line2)-1]
                full_name = name1+" "+name2
                names_lst += [full_name]
        return names_lst
all_full_names = full_names()

# Get the position of the player based on DraftKings
# Str -> Str
def get_position(plr_name):
        name_lst = list(plr_name)
        first = plr_name[:name_lst.index(" ")]
        last = plr_name[name_lst.index(" ")+1:]
        for i in range(len(DailyCosts)-1):
                line1 = DailyCosts[i]
                line2 = DailyCosts[i+1]
                name1 = line1[:len(line1)-1]
                name2 = line2[:len(line2)-1]
                full_name = name1+" "+name2

                if full_name == plr_name:
                        pos = DailyCosts[i-1].replace("\n","")
                        return pos
                else:
                        pass

# Produces the team abbriviation of the opposing team
# Str -> Str
def other_team(team):
        teams = []
        for line in matchups_source.find_all("td"):
                csk = line.get("csk")
                if today in str(csk) and "." in str(csk):
                        teams += [csk.split(".")[0]]
        index = teams.index(team)
        if index%2 == 0: # Aka is even
                return teams[index+1]
        else:
                return teams[index-1]

# Creates a multiplier based on opposing team
# Player -> Float
def proj_mult(plr):
        team_standings = []
        for line in Team_Standings_Source.find_all("a"):
                if "/teams/" in str(line):
                        team = str(line).split("/")[2]
                        team_standings += [team]
        team_standings = team_standings[1:31]
        opposing_team = other_team(plr[1])
        opp_team_standing = team_standings.index(opposing_team)+1
        # Create Multiplier
        if opp_team_standing > 15:
                rem = opp_team_standing%15
                mult = 1 + rem * 0.01
                return mult
        if opp_team_standing < 15:
                rem = opp_team_standing%15
                mult = 0.85 + rem * 0.01
                return mult
        else:
                return 1

# Returns a list of all skaters
# None -> Listof(Skaters)
def create_all_skaters():
        all_skaters = []
        for line in skaters_2016_source.find_all("tr"):
                player = line.text.replace('\n',',')
                player = player.split(',')
                if "Scoring" in player or "Player" in player:
                        continue
                name = player[2]
                if "'" in name:
                        name = name.replace("'","")
                team = player[4]
                position = get_position(name)

                games_played = int(player[6])
                goals = int(player[7])
                assists = int(player[8])
                # FD Stats
                plus_minus = int(player[10])
                pim = int(player[11])
                #
                shots = int(player[19])

                # Top line multiplier
                tlm_mult = 1
                toi = float(player[21])/games_played
                if 14 <= toi < 18.5:
                        tlm_mult = tlm_mult * 0.9
                if toi < 14:
                        tlm_mult = tlm_mult * 0.85
                if player[17] == 0 or player[13] == 0:
                        tlm_mult = tlm_mult * 0.98

                # Cost percentage
                cost_per = 0
                name_lst = list(name)
                first = name[:name_lst.index(" ")]
                last = name[name_lst.index(" ")+1:]
                for i in range(len(DailyCosts)-1):
                        line1 = DailyCosts[i]
                        line2 = DailyCosts[i+1]
                        name1 = line1[:len(line1)-1]
                        name2 = line2[:len(line2)-1]
                        full_name = name1+" "+name2
                        if full_name == name:
                                cost = DailyCosts[i+4].replace("\n","")
                                cost_per = int(cost)
                        else:
                                pass
                cost_per = cost_per/55000

                all_skaters.append([name, team, position, games_played, goals, assists, shots, plus_minus,tlm_mult, cost_per, pim])
        return(all_skaters)

# Returns a list of all goalies
# None -> Listof(Goalies)
def create_all_goalies():
        all_goalies = []
        for line in goalies_2016_source.find_all("tr"):
                player = line.text.replace('\n',',')
                player = player.split(',')
                if "Rk" in player or "Goalie Stats" in player:
                        continue
                name = player[2]
                if "'" in name:
                        name = name.replace("'","")

                team = player[4]
                games_played = int(player[5])
                wins = int(player[7])
                goals_against = int(player[10])
                saves = int(player[12])
                shut_outs = int(player[15])

                # Cost percentage
                cost_per = 0
                name_lst = list(name)
                first = name[:name_lst.index(" ")]
                last = name[name_lst.index(" ")+1:]
                for i in range(len(DailyCosts)-1):
                        line1 = DailyCosts[i]
                        line2 = DailyCosts[i+1]
                        name1 = line1[:len(line1)-1]
                        name2 = line2[:len(line2)-1]
                        full_name = name1+" "+name2
                        if full_name == name:
                                cost = DailyCosts[i+4].replace("\n","")
                                cost_per = int(cost)
                        else:
                                pass
                cost_per = cost_per/55000


                all_goalies.append([name, team, "G", games_played, wins, goals_against, saves, shut_outs,1, cost_per])
        return all_goalies



# Returns a player's expected value
# Player -> Int
def ev(player):
        if player[2] in ['C','LW','RW','D']:
                gp = player[3]
                goals_ev = (player[4] / gp) * 3
                assists_ev = (player[5] / gp) * 2
                shots_ev = (player[6] / gp) * 0.5
                plus_minus_ev = (player[7] / gp)
                pim_ev = (player[10]/ gp) * 0.25
                expected_points =  goals_ev + assists_ev + shots_ev + plus_minus_ev + pim_ev
                expected_points = expected_points * player[8]
                return round(expected_points,3)
        if player[2] == 'G':
                gs = player[3]
                win_ev = (player[4] / gs) * 3
                goals_against_ev = (player[5] / gs) * -1
                save_ev = (player[6] / gs) * 0.2
                shut_out_ev = (player[7] / gs) * 2
                expected_points = win_ev + goals_against_ev + save_ev + shut_out_ev
                expected_points = expected_points * player[8]
                return round(expected_points,3)
                #return 5
        else:
                print('Invalid Input')

# Returns a player's name and expected value
# Player -> Str
def ev_with_name(player):
        return player[0] + ": " + str(ev(player))

# Returns the expected value of a team
# listof(Players) -> float
def team_ev(team):
        total_points = 0
        for player in team:
                total_points += ev(player)
        return total_points

# Returns the cost of a team
# listof(Players) -> Nat
def team_cost(team):
        total_per = 0
        for player in team:
                total_per += player[9]
        return total_per * 55000

# Returns the names of players on a team
# listof(Players) -> listof(Str)
def team_names(team):
        name_str = ''
        for player in team:
                name = player[0]
                name_str += name + ", "
        return name_str


# Returns True if the team is valid and false otherwise
# listof(Players) -> Bool
def valid(plr_lst):
        if len(plr_lst) != 9:
                return False
        team_price = team_cost(plr_lst)
        if team_price <= 55000 and team_price >= 52000:
                diff_teams = []
                for player in plr_lst:
                        if player[2] != "G":
                                team = player[1]
                                diff_teams += team
                        else:
                                pass
                if len(set(diff_teams)) >= 3:
                        return True
                else:
                        False
        else:
                return False



all_skaters = create_all_skaters()
all_goalies = create_all_goalies()


# Gets all the players that are playing in games today
# None -> listof(Players)
def players_playing_today():
        todays_players = []
        for player in all_skaters + all_goalies:
                name = player[0]
                if name in all_full_names:
                        todays_players.append(player)
                else:
                        pass
        return todays_players

# Creates a list of all injured players
# None -> listof(Players)
def inj_plrs():
        injured_players = []
        for line in injuries_source.find_all("a"):
                href = line.get("href")
                if "/player/nhl" in str(href) and "." not in line.text:
                        injured_players += [line.text]
        return injured_players
injured_players = inj_plrs()

# Getting Todays players and then sorting them by their position
todays_players = players_playing_today()

# **************************** Enter Goalie(s) ***************************************

todays_goalie = ["Frederik Andersen"]

# One Goalie
goalies = list(filter((lambda x: x[2] == 'G' and x[0]==todays_goalie[0]), todays_players))


#************************************************************************************

# Filter out teams that are playing against your goalie
opposing_team = other_team(goalies[0][1])
print(opposing_team)


todays_players = list(filter((lambda x : x[1] != opposing_team), todays_players))

print(todays_players)

# Filter out injured players
# None -> None
for player in todays_players:
        if player[0] in injured_players:
                todays_players.remove(player)
        else:
                pass

# Adjusts a players expected value based on opponent
# None -> listof(players)
def adj_ev():
        plrs_adj = []
        for player in todays_players:
                player[8] = player[8] * proj_mult(player)
                plrs_adj += [player]
        return plrs_adj

todays_players = adj_ev()


# Find Positions
centers = list(filter((lambda x: x[2] == 'C'), todays_players))
centers = sorted(centers, key = lambda x : ev(x))[::-1][:11]#
right_wingers = list(filter((lambda x: x[2] == 'RW'), todays_players))
right_wingers = sorted(right_wingers, key = lambda x : ev(x))[::-1][:9]#
left_wingers = list(filter((lambda x: x[2] == 'LW'), todays_players))
left_wingers = sorted(left_wingers, key = lambda x : ev(x))[::-1][:9]#
defenceman = list(filter((lambda x: x[2] == 'D'), todays_players))
defenceman = sorted(defenceman, key = lambda x : ev(x))[::-1][:11]#


# Gets a specific player
# Str -> ev(player)
def find(name):
        for player in todays_players:
                if player[0] == name:
                        return player
                else:
                        pass

# Goalie Combos
goalie_combos = list(itertools.combinations(goalies,1))
# Combos set 1
set1_C_combos = list(itertools.combinations(centers,2))
set1_RW_combos = list(itertools.combinations(right_wingers,2))
set1_LW_combos = list(itertools.combinations(left_wingers,2))
set1_D_combos = list(itertools.combinations(defenceman,2))



# Returns all possible teams
# None -> listof(Teams)
def make_all_combos():
        all_teams = []
        # Make Teams With Combo set 1
        for goalie in goalie_combos:
                this_team = []
                for defencemen in set1_D_combos:
                        for rwingers in set1_RW_combos:
                                for lwingers in set1_LW_combos:
                                        for centers in set1_C_combos:
                                                this_team = goalie + defencemen + rwingers+ lwingers + centers
                                                all_teams += [this_team]

        return all_teams


all_possible_teams = make_all_combos()
all_possible_sorted = sorted(all_possible_teams, key = lambda x : team_ev(x))
all_possible_sorted = all_possible_sorted[::-1]


all_possible_sorted = list(filter((lambda x: valid(x)), all_possible_sorted))


# Find the first so many valid teams
# None -> listof(Teams)
def first_valids():
        all_teams = all_possible_sorted
        valid_so_far = []
        amount_valid = 0

        while amount_valid < 100:
                for team in all_teams:
                        index = all_teams.index(team)
                        if valid(team):
                                valid_so_far.append(team)
                                amount_valid += 1
                                all_teams = all_teams[index+1:]
                                break
        return valid_so_far
valid_teams_sorted = first_valids()


# Top 5 Teams:
top1 = team_names(valid_teams_sorted[0])
top2 = team_names(valid_teams_sorted[1])
top3 = team_names(valid_teams_sorted[2])
top4 = team_names(valid_teams_sorted[3])
top5 = team_names(valid_teams_sorted[4])
top1t = valid_teams_sorted[0]
top2t = valid_teams_sorted[1]
top3t = valid_teams_sorted[2]
top4t = valid_teams_sorted[3]
top5t = valid_teams_sorted[4]

# End Timer
end_timer = timeit.default_timer()
total_time = end_timer - start_timer
print('Seconds: ',total_time)

# Creates a string that formats into a document ** Ducument Function **
# listof(Teams) -> Str
def team_to_doc(lot, typ):
        doc_string = ""
        team_num = 1

        for team in lot:
                player_strings = ""
                header = "Team "+str(team_num)+"\n"
                tm_cost = str(math.ceil(team_cost(team)))+"\n"
                team_ev = 0
                if typ == "Paid":
                        for player in team:
                                name = player[0]
                                plr_val = ev(player)
                                plr_cost = player[9]*55000
                                line_in_doc =player[2]+", "+ name+"  |  Expected Points: "+str(plr_val)+"  |  Cost: $"\
                                        +str(int(plr_cost))+"\n"
                                player_strings += line_in_doc
                                team_ev += plr_val
                else:
                        for player in team:
                                name = player[0]
                                plr_val = ev(player)
                                plr_cost = player[9]*55000
                                line_in_doc = player[2]+", "+name+"    | Expected Points: "+str(plr_val)+"\n"
                                player_strings += line_in_doc
                                team_ev += plr_val

                make_team_doc = header + player_strings+"Total Cost: $"+tm_cost+"Expected Points: "\
                        +str(team_ev)+"\n\n"
                team_num += 1
                doc_string += make_team_doc
        return doc_string

test_start = timeit.default_timer()
# Write File with teams:
todays_teams = open('Todays_Teams.txt', 'w')
todays_teams.write(top1 +'\n\n' +top2 +'\n\n' +top3 +'\n\n' +top4 +'\n\n' +top5 +'\n\n' + len(top5) * '-')
todays_teams.write('\n' + 'Total time to create document: ' + str(total_time))
todays_teams.close()

# Write Website File:
web_teams = open('Website_Teams.txt', 'w')
web_teams.write(team_to_doc(valid_teams_sorted[:5], "Web"))
web_teams.close()

# Write Top 100 Teams Website File:
doc_name_dated = "DailyLineups"+today+str(todays_goalie)+str(now.hour)+str(now.minute)
web_teams = open(doc_name_dated, 'w')
web_teams.write(team_to_doc(valid_teams_sorted, "Paid"))
web_teams.close()
test_end = timeit.default_timer()
print("**************** DONE ********************")
print("Test Time: " + str(test_end - test_start))

