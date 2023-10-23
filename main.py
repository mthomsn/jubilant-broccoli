import os
import json
import ezgmail
import requests
from dotenv import load_dotenv
from crontab import CronTab
#cron = CronTab(tabfile='/etc/crontab', user=False)  # system users cron
#cron  = CronTab(user=True)  # current users cron
#cron  = CronTab(user='username')  # other users cron
#for job in cron:
#    print(job)

# loading env variables
load_dotenv()
RAPID_API_KEY=os.getenv('RAPID_API_KEY')
RAPID_API_HOST=os.getenv('RAPID_API_HOST')
PHONE_NUM=os.getenv('PHONE_NUM')

# loading relevent ids for api calls;
with open('ids.json') as json_file:
    ids = json.load(json_file)

with open('test-data.json') as json_file:
    test_data = json.load(json_file)
    teams = test_data['response']

# assuming carrier will be verizon for simplicity
def send_txt(number, message):
    ezgmail.send(f'{number}@vtext.com', '', f'{message}')

def get_league_fixtures(league_id, season, from_date, to_date):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"league":f"{league_id}","season":f"{season}","from":f"{from_date}","to":f"{to_date}"}
    headers = {"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": RAPID_API_HOST}
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# returns fixture on given time, future or past fixtures indicated by future param
def get_fixture(team_id, season, qty, future):
    if future == True:
        querystring = {"team":f"{team_id}", "season":f"{season}", "next":f"{qty}"}
    elif future == False:
        querystring = {"team":f"{team_id}", "season":f"{season}", "last":f"{qty}"}
    else:
        print("invalid future/past indicator")
        exit()
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": RAPID_API_HOST}
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def determine_winner(data):
    game_data = data['response']
    team_data = game_data[0]
    home_team_data = team_data['teams']['home']
    away_team_data = team_data['teams']['away']
    #print(type(home_team_data['winner']))
    #print(f"home team: {home_team_data['winner']}")
    #print(f"away team: {away_team_data['winner']}")
    if home_team_data['winner'] == True:
        res = f"{home_team_data['name']} won!"
        return res
    elif away_team_data['winner'] == True:
        res = f"{away_team_data['name']} won!"
        return res
    else:
        res = f"{home_team_data['name']} and {away_team_data['name']} tied."
        return res


# get results and send message
def get_results():
    game = get_fixture(ids['barca_team_id'], 2023, 1, False)
    game_result = determine_winner(game)
    send_txt(PHONE_NUM, game_result)

# main function
#def main():
    # query server to get next game
    # set timer to get results of next game
    # query server to get previous results
 

get_results()
