import uuid
from helper import helper
from operations import db_operations


db_ops = db_operations()

def start_screen():
    print("Welcome, soccer fan!")
    print("Below search through past tournament data.")


# show user options
def options():
    print("Select from the following menu options:\n1 View Tournaments available \n" \
    "2 View by countries \n3 View all games and data \n4 Exit")
    return helper.get_choice([1,2,3,4])

def list_Tournaments():
    # song name list to check for existance and avoid error
    query = '''
    SELECT Name
    FROM tournament;
    '''
    names = db_ops.single_attribute(query)

    print(names)


def playedquery(index):
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

def awayquery(index):
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

def gamesWon(index):
    queryTied = '''
    SELECT g.Date, hm.Name AS 'HomeTeam', g.HomeScore, aw.Name AS 'AwayTeam', g.AwayScore,
    t.Name AS 'Tournament', hci.Name AS 'HostCity', hco.Name AS 'HostCountry', g.Shootout
    FROM game g
    JOIN country hm ON g.HomeTeam = hm.countryID
    JOIN country aw ON g.AwayTeam = aw.countryID
    JOIN tournament t ON g.Tournament = t.tournamentID
    JOIN city hci ON g.HostCity = hci.cityID
    JOIN country hco ON g.HostCountry = hco.countryID
    WHERE g.HomeTeam = '''+str(index)+''' AND Homescore > AwayScore OR AwayTeam ='''+str(index)+''' AND HomeScore < AwayScore
    ORDER BY g.Date;
    '''

    gamesWon = db_ops.all_attributes(queryTied)

    print(gamesWon)

def tiedquery(index):
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
        user_choice = helper.get_choice([1,2,3,4,5])
        if user_choice == 1:
            playedquery(index)
        elif user_choice == 2:
            homequery(index)
        elif user_choice == 3:
            awayquery(index)
        elif user_choice == 4:
            gamesWon(index)
        elif user_choice == 5:
            tiedquery(index)

def view_Games():
    query = '''
    SELECT g.Date, hm.Name AS 'HomeTeam', g.HomeScore, aw.Name AS 'AwayTeam', g.AwayScore,
    t.Name AS 'Tournament', hci.Name AS 'HostCity', hco.Name AS 'HostCountry', g.Shootout
    FROM game g
    JOIN country hm ON g.HomeTeam = hm.countryID
    JOIN country aw ON g.AwayTeam = aw.countryID
    JOIN tournament t ON g.Tournament = t.tournamentID
    JOIN city hci ON g.HostCity = hci.cityID
    JOIN country hco ON g.HostCountry = hco.countryID
    ORDER BY g.Date;
    '''
    results = db_ops.all_attributes(query)

    print(results)



start_screen()

while True:
    user_choice = options()
    if user_choice == 1:
        list_Tournaments()
    elif user_choice == 2:
        by_country()
    elif user_choice == 3:
        view_Games()
    elif user_choice == 4:
        print("Goodbye!")
        break


db_ops.destructor()
