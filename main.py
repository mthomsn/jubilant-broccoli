import os
import json
import automation
from dotenv import load_dotenv
import ezgmail
import requests

# loading env variables
load_dotenv()
RAPID_API_KEY=os.getenv('RAPID_API_KEY')
RAPID_API_HOST=os.getenv('RAPID_API_HOST')
PHONE_NUM=os.getenv('PHONE_NUM')

# loading relevent ids for api calls;
with open('ids.json') as json_file:
    ids = json.load(json_file)
# loading test data
with open('test-data.json') as json_file:
    test_data = json.load(json_file)
    teams = test_data['response']
with open('next-fx-data.json') as json_file:
    next_test_data = json.load(json_file)
    next_game_data = next_test_data['response']

# assuming carrier will be verizon for simplicity
def send_txt(number, message):
    ezgmail.send(f'{number}@vtext.com', '', f'{message}')

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
    #game_data = data['response']
    team_data = data['response'][0]
    home_team_data = team_data['teams']['home']
    away_team_data = team_data['teams']['away']
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

def get_next_fixture():
    next_game = get_fixture(ids['barca_team_id'], 2023, 1, True)
    print(json.dumps(next_game, indent=4))
    return next_game

# main function
def main():
    # 1. get previous fixture result
    get_results()
    # 2. run automation.py
    automation.script(get_next_fixture())

main()
