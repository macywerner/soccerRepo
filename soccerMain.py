import uuid
from helper import helper
from operations import db_operations


db_ops = db_operations()

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
    WHERE HomeTeam = '''+str(index)+''' OR AwayTeam = '''+str(index)+'''
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
    WHERE HomeTeam = '''+str(index)+'''
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
    WHERE AwayTeam = '''+str(index)+'''
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
    WHERE (HomeTeam = '''+str(index)+''' AND g.Homescore > AwayScore) OR (AwayTeam ='''+str(index)+''' AND g.HomeScore < AwayScore)
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
    WHERE HomeTeam = '''+str(index)+''' OR AwayTeam = '''+str(index)+''' AND g.Homescore = g.AwayScore
    ORDER BY g.Date;
    '''

    gamesTied = db_ops.all_attributes(queryTied)

    print(gamesTied)

def start_screen():
    print("Welcome, soccer fan!")
    print("Below search through past tournament data.")


# show user options
def options():
    print("Select from the following menu options:\n1 View Tournaments available \n" \
    "2 View by countries \n3 View all games and data \n4 Add to the database \n5 Exit")
    return helper.get_choice([1,2,3,4,5])

def list_Tournaments():
    query = '''
    SELECT Name
    FROM tournament;
    '''
    helper.pretty_print(db_ops.single_attribute(query))


def by_country():
        query = '''
        SELECT Name
        FROM country;
        '''
        names = db_ops.single_attribute(query)

        choices = {}
        for i in range(len(names)):
            print(i,names[i])
            choices[i] = names[i]
        index = helper.get_choice(choices.keys())


        print("Which would you like to know about",choices[index]+"?" \
        "\n1 Games played \n" \
        "2 Games as home \n3 Games as away \n4 Games Won \n5 Games tied")
        user_choice = helper.get_choice([1,2,3,4,5])

        index = index + 1
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

def create_tournament():
    tournament = input("What is the name of the tournament you would like to create? ")
    tournament = "'"+tournament+"'"

    query = '''
    INSERT INTO tournament(Name)
    VALUES('''+tournament+''');
    '''

    db_ops.execute_query(query)

    print("Tournament successfully created.")

# create_game last step not working
def create_game():
    date = input("What was the date of the game you would like to add? (ex. 2021-01-01) ")

    print("Who was the Home team? ")
    homequery = '''
    SELECT Name
    FROM country;
    '''
    names = db_ops.single_attribute(homequery)

    choices = {}
    for i in range(len(names)):
        print(i,names[i])
        choices[i] = names[i]
    index = helper.get_choice(choices.keys())

    hteam = index + 1

    print("Who was the Away team? ")
    awayquery = '''
    SELECT Name
    FROM country;
    '''
    names = db_ops.single_attribute(awayquery)

    choices = {}
    for i in range(len(names)):
        print(i,names[i])
        choices[i] = names[i]
    index = helper.get_choice(choices.keys())

    ateam = index + 1

    hscore = input("What was the Home team's final score? ")

    ascore = input("What was the Away team's final score? ")

    print("What tournament did they play in?")
    tourn_query = '''
    SELECT Name
    FROM tournament;
    '''
    names = db_ops.single_attribute(tourn_query)

    choices = {}
    for i in range(len(names)):
        print(i,names[i])
        choices[i] = names[i]
    index = helper.get_choice(choices.keys())

    tournament = index + 1

    print("What city hosted the game ")
    cityquery = '''
    SELECT Name
    FROM city;
    '''
    names = db_ops.single_attribute(cityquery)

    choices = {}
    for i in range(len(names)):
        print(i,names[i])
        choices[i] = names[i]
    index = helper.get_choice(choices.keys())

    city = index + 1

    countryquery = '''
    SELECT Name
    FROM country
    WHERE countryID IN (
        SELECT country
        FROM city
        WHERE cityID = '''+str(city)+'''
    );
    '''
    country = db_ops.single_record(countryquery)

    shootout = input("Was there a shootout? (true or false) ")
    if shootout.lower() == "true":
        shootout = shoutout.upper()
        hgoals = input("How many goals did the Home team make? ")
        hgoals = "'"+hgoals+"'"
        agoals = input("How many goals did the Away team make? ")
        agoals = "'"+agoals+"'"
    else:
        shoutout = shootout.upper()

    gamequery = '''
    INSERT INTO game(Date, HomeTeam, AwayTeam, HomeScore, AwayScore, Tournament, HostCity, HostCountry, Shootout)
    VALUES ('''+str(date)+''','''+str(hteam)+''','''+str(ateam)+''','''+str(hscore)+''','''+str(ascore)+''','''+str(tournament)+''','''+str(city)+''','''+str(country)+''','''+str(shootout)+''');
    '''

    db_ops.execute_query(gamequery)

    shootout_query = '''
    INSERT INTO shootout
    VALUES ('''+hgoals+''','''+agoals+''');
    '''

    if shootout.lower() == "true":
        db_ops.execute_query(shootout_query)

    print("Game successfully added.")

def add_country():
    country = input("What is the name of the Country you would like to add? ")
    country = "'"+country+"'"

    query = '''
    INSERT INTO country(Name)
    VALUES('''+country+''');
    '''

    db_ops.execute_query(query)

    print("Country successfully added.")

def add_city():
    print("Which country would you like to add a city in? (Select a number)")
    query = '''
    SELECT Name
    FROM country;
    '''
    names = db_ops.single_attribute(query)

    choices = {}
    for i in range(len(names)):
        print(i,names[i])
        choices[i] = names[i]
    index = helper.get_choice(choices.keys())

    country = choices[index]
    country = "'"+country+"'"

    city = input("What is the name of the City you would like to add? ")
    city = "'"+city+"'"

    country_query = '''
    SELECT countryID
    FROM country
    WHERE Name = '''+country+''';
    '''
    countryID = db_ops.single_record(country_query)

    insert_city = '''
    INSERT INTO city(Name, Country)
    VALUES ('''+city+''','''+str(countryID)+''');
    '''

    db_ops.execute_query(insert_city)

    print("City successfully added.")

def create_func():
    print("What would you like to create/add? \n1 Tournament\n2 Game\n3 Country\n4 City")
    user_choice = helper.get_choice([1,2,3,4])
    if user_choice == 1:
        create_tournament()
    elif user_choice == 2:
        create_game()
    elif user_choice == 3:
        add_country()
    elif user_choice == 4:
        add_city()

def edit_game():

    # what was the date, who was the hometeam, who was the awayteam
    #query them and store for the edits query
    # query = '''
    # SELECT
    # FROM songs;
    # '''
    # names = db_ops.single_attribute(query)
    # # ask song name
    # choice = input("What song would you like to update? (song name, capitializtion matters)\n ")
    #
    # checkName = False
    # while checkName == False:
    #     if choice not in names:
    #         choice = input("Song does not exist, try another name:  ")
    #     else:
    #         checkName = True
    #
    # # edit choice to be ready for query
    # choice = "'"+choice+"'"
    #
    # # select song attributes from table
    # query = "SELECT * FROM songs WHERE Name= "+choice
    # attributes = db_ops.all_attributes(query)
    #
    # # get songID
    # query = "SELECT songID FROM songs WHERE Name= "+choice
    # song_ID = db_ops.single_record(query)
    # song_ID= "'"+song_ID+"'"

    # prompt user for desired attribute
    print("Which attribute would you like to update? \n1 Date\n2 Home Team\n3 AwayTeam\n4 Home Score\n5 Away Score\n6 Tournament\n7 Host Cityn\8 Shootout")
    attribute = helper.get_choice([1,2,3,4,5,6,7,8])

    #prompt user for desired input update
    update = input("What would you like to update? ")
    update = "'"+update+"'"

    # if statement for update, can only update song name, album name, artist name, release date, and Explicit
    attributeName = " "
    if attribute == 1:
        attributeName = "Date"
    elif attribute == 2:
        attributeName = "HomeTeam"
    elif attribute == 3:
        attributeName = "AwayTeam"
    elif attribute == 4:
        attributeName = "HomeScore"
    elif attribute == 5:
        attributeName = "AwayScore"
    elif attribute == 6:
        attributeName = "Tournament"
    elif attribute == 7:
        attributeName = "HostCity"
    elif attribute == 8:
        attributeName = "Shootout"

    # update attribute query
    query = "UPDATE songs SET "+attributeName+" = "+update+" WHERE songID = "+song_ID+";"
    db_ops.execute_query(query)

    print("Update successful")





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
        create_func()
    elif user_choice == 5:
        print("Goodbye!")
        break


db_ops.destructor()
