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


## Skaters 2016
#skaters_2016 = requests.get("http://www.hockey-reference.com/leagues/NHL_2016_skaters.html")
#skaters_2016_source = BeautifulSoup(skaters_2016.content, "html.parser")
## Goalies 2016
#goalies_2016 = requests.get("http://www.hockey-reference.com/leagues/NHL_2016_goalies.html")
#goalies_2016_source = BeautifulSoup(goalies_2016.content, "html.parser")
## Matchup Stats
#matchups = requests.get("http://www.hockey-reference.com/leagues/NHL_2016_games.html")
#matchups_source = BeautifulSoup(matchups.content, "html.parser")
## Injuries
#injuries = requests.get("http://www.rotoworld.com/teams/injuries/nhl/all/")
#injuries_source = BeautifulSoup(injuries.content, "html.parser")
## Team Standings:
#Team_Standings = requests.get("http://www.hockey-reference.com/leagues/NHL_2016_standings.html")
#Team_Standings_Source = BeautifulSoup(Team_Standings.content, "html.parser")


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
                print(full_name)

                if full_name == plr_name:
                        pos = DailyCosts[i-1].replace("\n","")
                        return pos
                else:
                        pass