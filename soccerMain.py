import uuid
from helper import helper
from operations import db_operations


db_ops = db_operations()

def start_screen():
    print("Welcome, soccer fan!")
    Print("Below search through past tournament data.")


# show user options
def options():
    print("Select from the following menu options:\n1 View Tournaments available \n" \
    "2 View by countries \n3 View games \n3 test \n4 Exit")
    return helper.get_choice([1,2,3,4])

def list_Tournaments():
    # song name list to check for existance and avoid error
    query = '''
    SELECT Name
    FROM tournament;
    '''
    names = db_ops.single_attribute(query)

    print(names)

def homequery(index):
    queryHome = '''
    SELECT g.Date, hm.Name AS 'HomeTeam', g.HomeScore, aw.Name AS 'AwayTeam', g.AwayScore,
    t.Name AS 'Tournament', hci.Name AS 'HostCity', hco.Name AS 'HostCountry', g.Shootout
    FROM game g
    JOIN country hm ON g.HomeTeam = hm.countryID
    JOIN country aw ON g.AwayTeam = aw.countryID
    JOIN tournament t ON g.Tournament = t.tournamentID
    JOIN city hci ON g.HostCity = hci.cityID
    JOIN country hco ON g.HostCountry = hco.countryID
    WHERE g.HomeTeam = '''+str(index)+'''
    ORDER BY g.Date;
    '''
    home = db_ops.all_attributes(queryHome)

    print(home)

def awayquery(int):
    queryAway = '''
    SELECT g.Date, hm.Name AS 'HomeTeam', g.HomeScore, aw.Name AS 'AwayTeam', g.AwayScore,
    t.Name AS 'Tournament', hci.Name AS 'HostCity', hco.Name AS 'HostCountry', g.Shootout
    FROM game g
    JOIN country hm ON g.HomeTeam = hm.countryID
    JOIN country aw ON g.AwayTeam = aw.countryID
    JOIN tournament t ON g.Tournament = t.tournamentID
    JOIN city hci ON g.HostCity = hci.cityID
    JOIN country hco ON g.HostCountry = hco.countryID
    WHERE g.AwayTeam = '''+str(index)+'''
    ORDER BY g.Date;
    '''

    away = db_ops.all_attributes(queryAway)

    print(away)

def tiedquery(int):
    queryTied = '''
    SELECT g.Date, hm.Name AS 'HomeTeam', g.HomeScore, aw.Name AS 'AwayTeam', g.AwayScore,
    t.Name AS 'Tournament', hci.Name AS 'HostCity', hco.Name AS 'HostCountry', g.Shootout
    FROM game g
    JOIN country hm ON g.HomeTeam = hm.countryID
    JOIN country aw ON g.AwayTeam = aw.countryID
    JOIN tournament t ON g.Tournament = t.tournamentID
    JOIN city hci ON g.HostCity = hci.cityID
    JOIN country hco ON g.HostCountry = hco.countryID
    WHERE g.HomeTeam = '''+str(index)+''' OR g.AwayTeam = '''+str(index)+''' AND Homescore = AwayScore
    ORDER BY g.Date;
    '''

    gamesTied = db_ops.all_attributes(queryTied)

    print(gamesTied)

def playedquery(int):
    queryPlay = '''
    SELECT g.Date, hm.Name AS 'HomeTeam', g.HomeScore, aw.Name AS 'AwayTeam', g.AwayScore,
    t.Name AS 'Tournament', hci.Name AS 'HostCity', hco.Name AS 'HostCountry', g.Shootout
    FROM game g
    JOIN country hm ON g.HomeTeam = hm.countryID
    JOIN country aw ON g.AwayTeam = aw.countryID
    JOIN tournament t ON g.Tournament = t.tournamentID
    JOIN city hci ON g.HostCity = hci.cityID
    JOIN country hco ON g.HostCountry = hco.countryID
    WHERE g.HomeTeam = '''+str(index)+''' OR g.AwayTeam = '''+str(index)+'''
    ORDER BY g.Date;
    '''

    gamesPlayed = db_ops.all_attributes(queryPlay)

    print(gamesPlayed)


def by_country():
        # song name list to check for existance and avoid error
        query = '''
        SELECT Name
        FROM country;
        '''
        names = db_ops.single_attribute(query)

        # show genres in table, also create dictionary for choices
        choices = {}
        for i in range(len(names)):
            print(i,names[i])
            choices[i] = names[i]
        index = helper.get_choice(choices.keys())

        index = index + 1

        print("Which would you like to know about",choices[index]+"?" \
        "\n1 Games played \n" \
        "2 Games as home \n3 Games as away \n4 Games tied ")
        return helper.get_choice([1,2,3,4])
        if user_choice == 1:
            playedquery(index)
        elif user_choice == 2:
            homequery(index)
        elif user_choice == 3:
            awayquery(index)
        elif user_choice == 4:
            tiedquery(index)



while True:
    user_choice = options()
    if user_choice == 1:
        list_Tournaments()
    elif user_choice == 2:
        by_country()
    elif user_choice == 3:
        homequery(9)
    elif user_choice == 4:
        print("Goodbye!")
        break


db_ops.destructor()
