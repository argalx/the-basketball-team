import sqlite3

# Database connection
conn = sqlite3.connect('the-basketball-team/basket.db')

# Create cursor object
cursor = conn.cursor()

# The Basketball Team Table Creation

# county
cursor.execute('''
    CREATE TABLE IF NOT EXISTS county (
               id INTEGER PRIMARY KEY,
               county TEXT NOT NULL
    )
''')

# city
cursor.execute('''
    CREATE TABLE IF NOT EXISTS city (
               id INTEGER PRIMARY KEY,
               city TEXT NOT NULL,
               county_id INTEGER NOT NULL
    )
''')

# teams
cursor.execute('''
    CREATE TABLE IF NOT EXISTS teams (
               id INTEGER PRIMARY KEY,
               team TEXT NOT NULL,
               city_id INTEGER NOT NULL
    )
''')

# players
cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
               id INTEGER PRIMARY KEY,
               player_name TEXT NOT NULL,
               team_id INTEGER NOT NULL
    )
''')

# coach_type
cursor.execute('''
    CREATE TABLE IF NOT EXISTS coach_type (
               id INTEGER PRIMARY KEY,
               coach_type TEXT NOT NULL
    )
''')

# coaches
cursor.execute('''
    CREATE TABLE IF NOT EXISTS coaches (
               id INTEGER PRIMARY KEY,
               coach_name TEXT NOT NULL,
               team_id INTEGER NOT NULL,
               coach_type_id INTEGER NOT NULL
    )
''')

# seasons
cursor.execute('''
    CREATE TABLE IF NOT EXISTS seasons (
               id INTEGER PRIMARY KEY,
               season TEXT NOT NULL
    )
''')

# games
cursor.execute('''
    CREATE TABLE IF NOT EXISTS games (
               id INTEGER PRIMARY KEY,
               game TEXT NOT NULL,
               season_id INTEGER NOT NULL,
               home_id INTEGER NOT NULL,
               visitor_id INTEGER NOT NULL
    )
''')

# Insert Data Function
def insertData():
    # Data Variables
    county = {
        'Platte':['New York', 'Chicago'],
        }
    
    cities = {
        'New York':{'team':'New York Knicks', 'coaches': {'Offensive':'Tom Thibodeau', 'Defensive': 'Char Aznable', 'Physical Training': 'Amuro Ray'}, 'players': ['Ryan Arcidiacono','RJ Barrett','Charlie Brown Jr.','Jalen Brunson','Donte DiVincenzo','Evan Fournier','Quentin Grimes','Josh Hart','Isaiah Hartenstein','DaQuan Jeffries','Jaylen Martin','Miles McBride']},

        'Chicago':{'team':'Chicago Bulls', 'coaches': {'Offensive':'Billy Donovan', 'Defensive':'Uzumaki Naruto', 'Physical Training':'Uchiha Sasuke'}, 'players': ['Lonzo Ball','Onuralp Bitim','Jevon Carter','Alex Caruso','Torrey Craig','DeMar DeRozan','Ayo Dosunmu','Andre Drummond','Zach LaVine','Justin Lewis','Julian Phillips','Adama Sanogo']},
        }
    
    coachType = ['Offensive', 'Defensive', 'Physical Training']

    seasons = ['Season 1']

    games = {
         'Season 1':{
              'Game 1':{'Location': 'New York', 'teams':['New York Knicks','Chicago Bulls']},
              'Game 2':{'Location': 'Chicago', 'teams':['New York Knicks','Chicago Bulls']}
              }
            }

    # Insert County and City
    for i, cityList in county.items():
        # Insert County
        cursor.execute('INSERT INTO county (county) VALUES (?)',(i,))
        
        # Commit Changes
        # conn.commit()

        for city in cityList:
            # Get County ID
            cursor.execute('SELECT id FROM county WHERE county=?',(i,))
            countyDetails = cursor.fetchall()
            countyId = list(countyDetails[0])[0]
            
            # Insert City
            cursor.execute('INSERT INTO city (city, county_id) VALUES (?, ?)',(city, countyId,))

            # Commit Changes
            # conn.commit()

    # Insert Coach Type
    for type in coachType:
        cursor.execute('INSERT INTO coach_type (coach_type) VALUES (?)',(type,))

        # Commit Changes
        # conn.commit()

    # Insert Team, Coaches, and Players
    for city, team in cities.items():
        # Get City ID
        cursor.execute('SELECT id FROM city WHERE city=?',(city,))
        cityDetails = cursor.fetchall()
        cityId = list(cityDetails[0])[0]
        
        # Insert Team
        cursor.execute('INSERT INTO teams (team, city_id) VALUES (?, ?)',(team.get('team'), cityId,))

        # Commit Changes
        # conn.commit()

        # Get Team ID
        cursor.execute('SELECT id FROM teams WHERE team=?',(team.get('team'),))
        teamDetails = cursor.fetchall()
        teamId = list(teamDetails[0])[0]

        for type, coach in team.get('coaches').items():
            # Get Coach Type ID
            cursor.execute('SELECT id FROM coach_type WHERE coach_type=?',(type,))
            coachTypeDetails = cursor.fetchall()
            coachTypeId = list(coachTypeDetails[0])[0]
            
            # Insert Coach
            cursor.execute('INSERT INTO coaches (coach_name, team_id, coach_type_id) VALUES (?, ?, ?)',(coach, teamId, coachTypeId,))
            
            # Commit Changes
            # conn.commit()

        for player in team.get('players'):
                # Insert Player
                cursor.execute('INSERT INTO players (player_name, team_id) VALUES (?, ?)',(player, teamId,))

                # Commit Changes
                # conn.commit()

    # Insert Seasons
    for season in seasons:
         cursor.execute('INSERT INTO seasons (season) VALUES (?)',(season,))

    # Insert Games
    for season, matches in games.items():
         # Get Season ID
        cursor.execute('SELECT id FROM seasons WHERE season=?',(season,))
        seasonDetails = cursor.fetchall()
        seasonId = list(seasonDetails[0])[0]           
        
        for game, gameMatch in matches.items():
            # Get Location City ID
            cursor.execute('SELECT id FROM city WHERE city=?',(gameMatch.get('Location'),))
            cityDetail = cursor.fetchall()
            cityId = list(cityDetail[0])[0]

            # Get Match Local Team ID
            cursor.execute('SELECT id FROM teams WHERE city_id=?',(cityId,))
            teamDetail = cursor.fetchall()
            homeTeamId = list(teamDetail[0])[0]
            
            # Get Match Visitor Team ID
            for team in gameMatch.get('teams'):
                # Get Team ID
                cursor.execute('SELECT id FROM teams WHERE team=?',(team,))
                matchTeamId = cursor.fetchall()
                currentTeamId = list(matchTeamId[0])[0]
                
                if currentTeamId != homeTeamId:
                    # Get Visitor Team ID
                    visitorTeamId = currentTeamId

            # Insert Games
            cursor.execute('INSERT INTO games (game, season_id, home_id, visitor_id) VALUES (?, ?, ?, ?)',(game, seasonId, homeTeamId, visitorTeamId))

    # Commit Changes
    conn.commit()

insertData()