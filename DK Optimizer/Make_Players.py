# Make Document into Player:

from Players import *


def make_acc_goalies(s_stats, c_stats):
    #Season Doc
    season_stats = open(s_stats,'r')
    read_s_stats = season_stats.readlines()
    # Career Doc
    career_stats = open(c_stats,'r')
    read_c_stats = career_stats.readlines()

    player_lst = ''
    for line in read_s_stats:
        name = line.split('\t')[0]
        if len(line) <= 10:
            pass
        else:
            team = line.split('\t')[2]
            position = 'G'
            games_started = line.split('\t')[4]
            wins = line.split('\t')[5]
            shots_against = line.split('\t')[9]
            goals_against = line.split('\t')[10]
            shutouts = line.split('\t')[13]
            name_prefix = name.split(' ')[0][0] + '_' + name.split(' ')[-1]
            for car in read_c_stats:
                car_name = car.split('\t')[0]
                if len(car) < 10:
                    pass
                elif name == car_name:
                    career_started = car.split('\t')[2]
                    career_wins = car.split('\t')[3]
                    career_shots_against = car.split('\t')[7]
                    career_goals_against = car.split('\t')[8]
                    career_shutouts = car.split('\t')[11]
                    player_lst += name_prefix + ' = ' + "Goalie('"+ name+"', "+ "'"+ team +"', "  \
                        +"'"+ position +"'" +', '+ games_started + ', ' + wins + ', '+ shots_against +', '+ goals_against + ', ' + shutouts +', '+ career_started +', '+ career_wins + ', ' + career_shots_against + ', ' + career_goals_against + ', ' + career_shutouts +') \n'
    print(player_lst)

def make_goalie_doc(s_stats, c_stats):
    #Season Doc
    season_stats = open(s_stats,'r')
    read_s_stats = season_stats.readlines()
    # Career Doc
    career_stats = open(c_stats,'r')
    read_c_stats = career_stats.readlines()

    player_lst = ''
    for line in read_s_stats:
        name = line.split('\t')[0]
        if len(line) <= 10:
            pass
        else:
            team = line.split('\t')[2]
            position = 'G'
            games_started = line.split('\t')[4]
            wins = line.split('\t')[5]
            shots_against = line.split('\t')[9]
            goals_against = line.split('\t')[10]
            shutouts = line.split('\t')[13]
            name_prefix = name.split(' ')[0][0] + '_' + name.split(' ')[-1]
            for car in read_c_stats:
                car_name = car.split('\t')[0]
                if len(car) < 10:
                    pass
                elif name == car_name:
                    career_started = car.split('\t')[2]
                    career_wins = car.split('\t')[3]
                    career_shots_against = car.split('\t')[7]
                    career_goals_against = car.split('\t')[8]
                    career_shutouts = car.split('\t')[11]
                    player_lst += "Goalie('"+ name+"', "+ "'"+ team +"', "  \
                        +"'"+ position +"'" +', '+ games_started + ', ' + wins + ', '+ shots_against +', '+ goals_against + ', ' + shutouts +', '+ career_started +', '+ career_wins + ', ' + career_shots_against + ', ' + career_goals_against + ', ' + career_shutouts +')\n'
    print(player_lst)

#------------------------------------------------------------------------------------------------------------

def filter_document(doc):
    doc_read = open(doc,'r')
    doc_read = doc_read.readlines()

    new_doc = ''

    for line in doc_read:
        if line[0] == 'R' or line[0] == ',':
            pass
        else:
            new_doc += line

    doc_write = open(doc,'w')
    doc_write.write(new_doc)
    doc_write.close()







def make_new_plrs(last_season, this_season):
    # Last Season Document
    last_season = open(last_season,'r')
    last_season = last_season.readlines()
    # Last Season Document
    this_season = open(this_season,'r')
    this_season = this_season.readlines()

    all_plr_lst = ''
    for player in last_season:
        plr_stats = player.split(',')
        name = plr_stats[1]
        name_prefix = name.split(' ')[0][0] + '_' + name.split(' ')[-1]
        team = plr_stats[3]
        pos = plr_stats[4]
        gp_ls = plr_stats[5]
        g_ls = plr_stats[6]
        a_ls = plr_stats[7]
        sh_ls = plr_stats[18]
        bs_ls = plr_stats[22]
        for tsp in this_season:
            tsp_stats = tsp.split(',')
            name2 = tsp_stats[1]
            if name == name2:
                gp_cr = tsp_stats[5]
                g_cr = tsp_stats[6]
                a_cr = tsp_stats[7]
                sh_cr = tsp_stats[18]
                bs_cr = tsp_stats[22]
                all_plr_lst += name_prefix + ' = ' + "Player('"+ name+"', "+ "'"+ team +"', " \
                        +"'"+ pos+"', " + gp_ls + ', ' + g_ls +', ' + a_ls +', '+sh_ls+', ' +bs_ls+','+ \
                        gp_cr +', ' + g_cr+', ' + a_cr+', ' + sh_cr +','+ bs_cr+') \n'
            else:
                pass
    print(all_plr_lst)


def make_plr_doc(last_season, this_season):
    # Last Season Document
    last_season = open(last_season,'r')
    last_season = last_season.readlines()
    # Last Season Document
    this_season = open(this_season,'r')
    this_season = this_season.readlines()

    all_plr_lst = ''
    for player in last_season:
        plr_stats = player.split(',')
        name = plr_stats[1]
        name_prefix = name.split(' ')[0][0] + '_' + name.split(' ')[-1]
        team = plr_stats[3]
        pos = plr_stats[4]
        gp_ls = plr_stats[5]
        g_ls = plr_stats[6]
        a_ls = plr_stats[7]
        sh_ls = plr_stats[18]
        bs_ls = plr_stats[22]
        for tsp in this_season:
            tsp_stats = tsp.split(',')
            name2 = tsp_stats[1]
            if name == name2:
                gp_cr = tsp_stats[5]
                g_cr = tsp_stats[6]
                a_cr = tsp_stats[7]
                sh_cr = tsp_stats[18]
                bs_cr = tsp_stats[22]
                all_plr_lst += 'Player("'+ name+'", '+ "'"+ team +"', " \
                        +"'"+ pos+"', " + gp_ls + ', ' + g_ls +', ' + a_ls +', '+sh_ls+', ' +bs_ls+','+ \
                        gp_cr +', ' + g_cr+', ' + a_cr+', ' + sh_cr +','+ bs_cr+') \n'
            else:
                pass
    plr_class = open('Players_Class.txt', 'w')
    plr_class.write(all_plr_lst)
    plr_class.close()





