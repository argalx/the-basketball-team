import sqlite3

# Database connection
conn = sqlite3.connect('the-basketball-team/basket.db')

# Create cursor object
cursor = conn.cursor()

# String separator
separator = "_"*75

# String Divider
divider = "-"*75

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

# Display Season Details
def displaySeasonDetails():
    # Get Season Details
    cursor.execute('SELECT id, season FROM seasons')
    seasonDetails = cursor.fetchall()

    for season in seasonDetails:
        seasonTitle = list(season)[1]
        seasonId = list(season)[0]
        
        # (RMBC) Header
        print(f'The Richard Michael County Basketball Conference (RMBC) {seasonTitle}\n{separator}\nTEAMS\n{divider}')
        
        # Get Teams
        cursor.execute('SELECT id, team, city_id FROM teams')
        teamDetails = cursor.fetchall()

        for team in teamDetails:
            teamName = list(team)[1]
            print(teamName)

        # Invoke separator variable
        print(f'{separator}\nMATCHES\n{divider}')

        # Get Season Games
        cursor.execute('SELECT game, home_id, visitor_id FROM games WHERE season_id=?',(seasonId,))
        gameDetails = cursor.fetchall()
        
        for game in gameDetails:
            # Get Home Team
            for team in teamDetails:
                if list(team)[0] == list(game)[1]:
                    homeTeam = list(team)[1]

            # Get Visitor Team
            for team in teamDetails:
                if list(team)[0] == list(game)[2]:
                    visitorTeam = list(team)[1]

            print(f'{list(game)[0]}: {homeTeam} (HOME) vs. {visitorTeam} (Visitor)')

# Display Team Details
def displayTeamDetails():
    # Get Teams
    cursor.execute('SELECT id, team, city_id FROM teams')
    teamDetails = cursor.fetchall()
    
    for team in teamDetails:
        # Get City
        cursor.execute('SELECT city, county_id FROM city WHERE id=?',(list(team)[2],))
        cityDetails = cursor.fetchall()
        city = list(cityDetails[0])[0]

        # Get County
        cursor.execute('SELECT county FROM county WHERE id=?',(list(cityDetails[0])[1],))
        countyDetails = cursor.fetchall()
        county = list(countyDetails[0])[0]

        # Display Team Details
        print(f'TEAM DETAILS\n{divider}\nTeam: {list(team)[1]}\nCity: {city}\nCounty: {county}\n{separator}\nCOACHING STAFF\n{divider}')
        
        # Get Coaches
        cursor.execute('''SELECT coach_type.coach_type, coaches.coach_name
                       FROM coaches
                       INNER JOIN coach_type ON coaches.coach_type_id = coach_type.id WHERE team_id=?''',(list(team)[2],))
        coachDetails = cursor.fetchall()

        for coach in coachDetails:
            print(f'{list(coach)[0]}: {list(coach)[1]}')

        # Separator
        print(f'{separator}\nROSTER\n{divider}')

        # Get Players
        cursor.execute('SELECT player_name FROM players WHERE team_id=?',(list(team)[2],))
        playerDetails = cursor.fetchall()

        for player in playerDetails:
            print(list(player)[0])

        # Separator
        print(f'{separator}\nUPCOMING MATCHES\n{divider}')

        # Get Games
        cursor.execute('SELECT game, home_id, visitor_id FROM games WHERE home_id=? OR visitor_id=?',(list(team)[2],list(team)[2],))
        gameDetails = cursor.fetchall()

        for game in gameDetails:
            if list(game)[1] == list(team)[2]:
                # Get Enemy Team
                cursor.execute('SELECT team FROM teams WHERE id=?',(list(game)[2],))
                enemyDetails = cursor.fetchall()
                enemy = list(enemyDetails[0])[0]
                print(f'{list(game)[0]} - vs. {enemy} (HOME)')
            else:
                cursor.execute('SELECT team FROM teams WHERE id=?',(list(game)[1],))
                enemyDetails = cursor.fetchall()
                enemy = list(enemyDetails[0])[0]
                print(f'{list(game)[0]} - vs. {enemy} (AWAY)')

        print(separator)

# Call insertData() Function
# insertData()

# Call displaySeasonDetails() Function
displaySeasonDetails()

# Call displayTeamDetails() Function
displayTeamDetails()