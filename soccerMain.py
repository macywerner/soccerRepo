import uuid
from helper import helper
from operations import db_operations


db_ops = db_operations()

data_results = helper.data_cleaner("results.csv")
data_results = data_results[1:]
data_shootouts = helper.data_cleaner("shootouts.csv")
data_shootouts = data_shootouts[1:]

def is_empty():
    query = '''
    SELECT COUNT(*)
    FROM game;
    '''

    result = db_ops.single_record(query)
    return result == 0

def pre_process():
    if is_empty():
        countries = set()
        cities = set()
        tournaments = set()
        games = set()
        for i in range(len(data_results)):
            date = data_results[i][0]
            home_team = data_results[i][1]
            away_team = data_results[i][2]
            home_score = data_results[i][3]
            away_score = data_results[i][4]
            tournament = data_results[i][5]
            tournament = tournament.replace("'", "")
            city = data_results[i][6]
            city = city.replace("'", "")
            country = data_results[i][7]
            countries.add(home_team)
            countries.add(away_team)
            countries.add(country)
            cities.add((city,country))
            tournaments.add(tournament)
            games.add((date,home_team,away_team,home_score,away_score,tournament,city,country,"False"))
        countries = list(countries)
        cities = list(cities)
        tournaments = list(tournaments)
        games = list(games)
        for i in range(len(countries)):
            query = "INSERT INTO country(Name) VALUES('"+str(countries[i])+"')"
            db_ops.insert_one(query)
        print("committing countries")
        db_ops.commit()
        for i in range(len(cities)):
            query = "SELECT countryID FROM country WHERE Name LIKE '"+str(cities[i][1])+"' LIMIT 1"
            countryID = db_ops.single_record(query)
            query = "INSERT INTO city(Name, Country) VALUES('"+str(cities[i][0])+"', "+str(countryID)+")"
            db_ops.insert_one(query)
        print("committing cities")
        db_ops.commit()
        for i in range(len(tournaments)):
            query = "INSERT INTO tournament(Name) VALUES('"+str(tournaments[i])+"')"
            db_ops.insert_one(query)
        print("committing tournaments")
        db_ops.commit()
        for i in range(len(games)):
            query = "SELECT countryID FROM country WHERE Name LIKE '"+str(games[i][1])+"' LIMIT 1"
            homecountryID = db_ops.single_record(query)
            query = "SELECT countryID FROM country WHERE Name LIKE '"+str(games[i][2])+"' LIMIT 1"
            awaycountryID = db_ops.single_record(query)
            query = "SELECT tournamentID FROM tournament WHERE Name LIKE '"+str(games[i][5])+"' LIMIT 1"
            tournamentID = db_ops.single_record(query)
            query = "SELECT cityID FROM city WHERE Name LIKE '"+str(games[i][6])+"' LIMIT 1"
            cityID = db_ops.single_record(query)
            query = "SELECT countryID FROM country WHERE Name LIKE '"+str(games[i][7])+"' LIMIT 1"
            hostcountryID = db_ops.single_record(query)
            query = "INSERT INTO game(Date, HomeTeam, AwayTeam, HomeScore, AwayScore, Tournament, HostCity, HostCountry, Shootout)"
            query += " VALUES('"+str(games[i][0])+"', "+str(homecountryID)+", "+str(awaycountryID)+","
            query += " "+str(games[i][3])+", "+str(games[i][4])+", "+str(tournamentID)+","
            query += " "+str(cityID)+", "+str(hostcountryID)+", "+str(games[i][8])+")"
            if i % 1000 == 0:
                print(i)
            print(query)
            db_ops.insert_one(query)
        db_ops.commit()

        shootouts = set()
        for i in range(len(data_shootouts)):
            date = data_shootouts[i][0]
            winner = data_shootouts[i][1]
            shootouts.add((date,winner))
        shootouts = list(shootouts)
        for i in range(len(shootouts)):
            query = "SELECT countryID FROM country WHERE Name LIKE '"+str(shootouts[i][1])+"' LIMIT 1"
            countryID = db_ops.single_record(query)
            query = "SELECT gameID FROM game WHERE Date LIKE '"+str(shootouts[i][0])+"' AND (HomeTeam = "+str(countryID)+" OR AwayTeam = "+str(countryID)+") LIMIT 1"
            gameID = db_ops.single_record(query)
            query = "INSERT INTO shootout VALUES('"+str(gameID)+"', '"+str(countryID)+"')"
            db_ops.insert_one(query)
            query = "UPDATE game SET Shootout = 1 WHERE gameID = "+str(gameID)
            db_ops.insert_one(query)
        db_ops.commit()

#queries for viewing games
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

def average_goals_at_home(index):
    query = '''
    SELECT AVG(g.HomeScore)
    FROM game g
    JOIN country hm ON g.HomeTeam = hm.countryID
    JOIN country aw ON g.AwayTeam = aw.countryID
    JOIN tournament t ON g.Tournament = t.tournamentID
    WHERE HomeTeam = '''+str(index)+'''
    ORDER BY g.Date;
    '''

    avg_hscore= db_ops.single_record(query)

    print(avg_hscore)

def average_goals_at_away(index):
    query = '''
    SELECT AVG(g.AwayScore)
    FROM game g
    JOIN country hm ON g.HomeTeam = hm.countryID
    JOIN country aw ON g.AwayTeam = aw.countryID
    JOIN tournament t ON g.Tournament = t.tournamentID
    WHERE AwayTeam = '''+str(index)+'''
    ORDER BY g.Date;
    '''

    avg_ascore= db_ops.single_record(query)

    print(avg_ascore)

def start_screen():
    print("Welcome, soccer fan!")
    print("Below search through past tournament data.")

# show user options
def options():
    print("Select from the following menu options:\n1 View Tournaments available \n" \
    "2 View by countries \n3 View all games and scores in a tournament \n4 Add to the database \n5 Update a game\n6 Delete a game \n7 Amount of Games played by each country\n8 Exit")
    return helper.get_choice([1,2,3,4,5,6,7,8])

# list of tournaments in the database
def list_Tournaments():
    query = '''
    SELECT Name
    FROM tournament;
    '''
    helper.pretty_print(db_ops.single_attribute(query))

#search information by country
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
        "2 Games as home \n3 Games as away \n4 Games Won \n5 Games tied\n6 Average goals at home\n7 Average goals away")
        user_choice = helper.get_choice([1,2,3,4,5,6,7])

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
        elif user_choice == 6:
            average_goals_at_home(index)
        elif user_choice == 7:
            average_goals_at_away(index)

# view games and scores in a tournament
def view_Games():
    print("What tournament would you like to view?")
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

    year = input("What year? ")

    view_games = "CREATE VIEW vGames AS SELECT g.Date,CONCAT(hm.Name,"" vs "",aw.Name) Teams,CONCAT(g.HomeScore,"" - "" ,g.AwayScore) Score "
    view_games += "FROM game g JOIN country hm ON g.HomeTeam = hm.countryID JOIN country aw ON g.AwayTeam = aw.countryID"
    view_games += "WHERE g.Tournament = '"+str(tournament)+"' AND g.Date LIKE '"+str(year)+" %' ORDER BY g.Date;"
    db_ops.execute_query(view_games)

    query = '''
    SELECT *
    FROM vGames;
    '''

    results = db_ops.all_attributes(query)

    print(results)

    queryDrop = '''
    DROP VIEW vGames;
    '''
    db_ops.execute_query(queryDrop)

# add a tournament to the database
def create_tournament():
    tournament = input("What is the name of the tournament you would like to create? ")

    query = '''
    INSERT INTO tournament(Name)
    VALUES('''+str(tournament)+''');
    '''

    db_ops.execute_query(query)

    print("Tournament successfully created.")

#add a game to the database
def create_game():
    #prompt user for all needed information for a game
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

    countryquery ="SELECT country FROM city WHERE cityID = '"+str(city)+"';"
    country = db_ops.single_record(countryquery)

    shootout = input("Was there a shootout? (true or false) ")

    #if a shootout occurred, do query for both game and shootout
    if shootout.lower() == "true":
        winner = input("Who won? For Home, enter:"+str(hteam)+" or For Away, enter:"+str(ateam)+" ")

        gamequery = "INSERT INTO game(Date, HomeTeam, AwayTeam, HomeScore, AwayScore, Tournament, HostCity, HostCountry, Shootout)"
        gamequery += "VALUES ('"+str(date)+"','"+str(hteam)+"','"+str(ateam)+"','"+str(hscore)+"','"+str(ascore)+"','"+str(tournament)+"','"+str(city)+"','"+str(country)+"',"+str(shootout.upper())+");"

        id = "SELECT MAX(gameID) FROM game; "
        gameID = db_ops.single_record(id)

        shootout_query = "INSERT INTO shootout VALUES ("+str(gameID)+", "+str(winner)+");"
        db_ops.execute_query(shootout_query)

        print("Game successfully added.")

    #if no shootout, do query for game
    else:
        gamequery = "INSERT INTO game(Date, HomeTeam, AwayTeam, HomeScore, AwayScore, Tournament, HostCity, HostCountry, Shootout)"
        gamequery += "VALUES ('"+str(date)+"','"+str(hteam)+"','"+str(ateam)+"','"+str(hscore)+"','"+str(ascore)+"','"+str(tournament)+"','"+str(city)+"','"+str(country)+"',"+str(shootout.upper())+");"

        db_ops.execute_query(gamequery)

        print("Game successfully added.")

# add a country to the database
def add_country():
    country = input("What is the name of the Country you would like to add? ")
    country = "'"+country+"'"

    query = '''
    INSERT INTO country(Name)
    VALUES('''+country+''');
    '''

    db_ops.execute_query(query)

    print("Country successfully added.")

# add a city to the database
def add_city():
    #ask for country first to avoid errors
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

    #get countryID to insert into city table
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

# menu for additions, prompt the user
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

#update information in a specified game
def update_game():

        query = '''
        SELECT Name
        FROM tournament;
        '''
        names = db_ops.single_attribute(query)

        name = input("What was the name of the tournamnet the game you would like to update was in? ")

        #make sure the tournament entered exists
        checkT = False
        while checkT == False:
            if str(name) not in names:
                name = input("That Tournament does not exist, please try again:  ")
            else:
                checkT = True

        #narrow down search

        view_games = "SELECT hm.Name, aw.Name "
        view_games += "FROM game g "
        view_games += "JOIN country hm ON g.HomeTeam = hm.countryID "
        view_games += "JOIN country aw ON g.AwayTeam = aw.countryID "
        view_games += "WHERE Tournament = "
        view_games += "(SELECT tournamentID FROM tournament WHERE Name =  '"+str(name)+"');"

        games = db_ops.all_attributes(view_games)

        print(games)


        print("From the games listed above,")
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

        # # query and show game details
        # view_game = "SELECT g.Date, hm.Name AS 'HomeTeam', g.HomeScore, aw.Name AS 'AwayTeam', g.AwayScore, t.Name AS 'Tournament', hci.Name AS 'HostCity', hco.Name AS 'HostCountry', g.Shootout"
        # view_game += "FROM game g "
        # view_game += "JOIN country hm ON g.HomeTeam = hm.countryID "
        # view_game += "JOIN country aw ON g.AwayTeam = aw.countryID "
        # view_game += "JOIN tournament t ON g.Tournament = t.tournamentID JOIN city hci ON g.HostCity = hci.cityID JOIN country hco ON g.HostCountry = hco.countryID"
        # view_game += "WHERE HomeTeam = '"+str(hteam)+"' AND AwayTeam = '"+str(ateam)+"' AND tournament = "
        # view_game += "(SELECT tournamentID FROM tournament WHERE Name = '"+str(name)+"');"
        # view_game += "ORDER BY g.Date;"
        #
        # game = db_ops.all_attributes(view_game)
        # print(game)

        # prompt user for desired attribute
        print("Which attribute would you like to update? \n1 Date\n2 Home Team\n3 AwayTeam\n4 Home Score\n5 Away Score\n6 Tournament\n7 Host City")
        attribute = helper.get_choice([1,2,3,4,5,6,7])

        #prompt user for desired input update
        update = input("What would you like to update it to? ")

        # if statement for update, can update everything but shootout
        #query inside each due to how to query each differs
        attributeName = " "
        if attribute == 1:
            attributeName = "Date"
            update_query = "UPDATE game SET "+attributeName+" = '"+str(update)+"' WHERE tournament = "
            update_query += "(SELECT tournamentID FROM tournament WHERE Name = '"+str(name)+"') AND HomeTeam = '"+str(hteam)+"'"
            update_query += "AND AwayTeam = '"+str(ateam)+"' "
            db_ops.execute_query(update_query)
        elif attribute == 2:
            attributeName = "HomeTeam"
            query = "SELECT countryID FROM country WHERE Name = '"+str(update)+"';"
            update = db_ops.single_record(query)
            update_query = "UPDATE game SET "+attributeName+" = '"+str(update)+"' WHERE tournament = "
            update_query += "(SELECT tournamentID FROM tournament WHERE Name = '"+str(name)+"');"
            db_ops.execute_query(update_query)
        elif attribute == 3:
            attributeName = "AwayTeam"
            query = "SELECT countryID FROM country WHERE Name = '"+str(update)+"';"
            update = db_ops.single_record(query)
            update_query = "UPDATE game SET "+attributeName+" = '"+str(update)+"' WHERE tournament = "
            update_query += "(SELECT tournamentID FROM tournament WHERE Name = '"+str(name)+"');"
            db_ops.execute_query(update_query)
        elif attribute == 4:
            attributeName = "HomeScore"
            update_query = "UPDATE game SET "+attributeName+" = '"+str(update)+"' WHERE tournament = "
            update_query += "(SELECT tournamentID FROM tournament WHERE Name = '"+str(name)+"');"
            db_ops.execute_query(update_query)
        elif attribute == 5:
            attributeName = "AwayScore"
            update_query = "UPDATE game SET "+attributeName+" = '"+str(update)+"' WHERE tournament = "
            update_query += "(SELECT tournamentID FROM tournament WHERE Name = '"+str(name)+"');"
            db_ops.execute_query(update_query)
        elif attribute == 6:
            attributeName = "Tournament"
            query = "SELECT tournamentID FROM tournament WHERE Name = '"+str(update)+"';"
            update = db_ops.single_record(query)
            update_query = "UPDATE game SET "+attributeName+" = "+str(update)+" WHERE HomeTeam = "+str(hteam)+" "
            update_query += "AND AwayTeam = "+str(ateam)+";"
            db_ops.execute_query(update_query)
        elif attribute == 7:
            attributeName = "HostCity"
            query = "SELECT cityID FROM city WHERE Name = '"+str(update)+"';"
            update = db_ops.single_record(query)
            update_query = "UPDATE game SET "+attributeName+" = '"+str(update)+"' WHERE tournament = "
            update_query += "(SELECT tournamentID FROM tournament WHERE Name = '"+str(name)+"');"
            db_ops.execute_query(update_query)

        print("Update successful")

#delete a game
def delete_game():
        query = '''
        SELECT Name
        FROM tournament;
        '''
        names = db_ops.single_attribute(query)

        name = input("What was the name of the tournamnet the game you would like to delete was in? ")


        checkT = False
        while checkT == False:
            if str(name) not in names:
                name = input("That Tournament does not exist, please try again:  ")
            else:
                checkT = True

        query = "SELECT * FROM game WHERE Tournament = (SELECT tournamentID FROM tournament WHERE Name = '"+str(name)+"');"
        attributes = db_ops.all_attributes(query)

        view_games = "SELECT hm.Name, aw.Name FROM game g JOIN country hm ON g.HomeTeam = hm.countryID JOIN country aw ON g.AwayTeam = aw.countryID WHERE Tournament = (SELECT tournamentID FROM tournament WHERE Name =  '"+str(name)+"');"

        games = db_ops.all_attributes(view_games)

        print(games)


        print("From the games listed above,")
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

        delete_game = "DELETE FROM game WHERE HomeTeam = "+str(hteam)+" AND AwayTeam = "+str(ateam)+" AND tournament = "
        delete_game += "(SELECT tournamentID FROM tournament WHERE Name = '"+str(name)+"');"
        db_ops.execute_query(delete_game)

        print("Game was deleted.")

def games_played():
    query = '''
    SELECT c.Name,COUNT(g.gameID) AS TotalGames
    FROM game g
    JOIN country c ON g.HomeTeam = c.countryID
    GROUP BY c.Name;
    '''

    results = db_ops.all_attributes(query)

    print(results)
# load file, check if its loaded
pre_process()

#call the start
start_screen()

#call function based on user input
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
        update_game()
    elif user_choice == 6:
        delete_game()
    elif user_choice == 7:
        games_played()
    elif user_choice == 8:
        print("Goodbye!")
        break


db_ops.destructor()
