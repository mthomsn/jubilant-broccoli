import os
import json
import ezgmail
import requests
from dotenv import load_dotenv

# loading env variables
load_dotenv()
RAPID_API_KEY=os.getenv('RAPID_API_KEY')
RAPID_API_HOST=os.getenv('RAPID_API_HOST')

# loading relevent ids for api calls
with open('ids.json') as json_file:
    ids = json.load(json_file)
    print(ids['laliga_2023_id'])

# assuming carrier will be verizon for simplicity
def send_txt(number):
    print(f'{number}@vtext.com')
    ezgmail.send(f'{number}@vtext.com', '', 'this is a test of python script using cron')

def get_league_fixtures(league_id, season, from_date, to_date):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"league":f"{league_id}","season":f"{season}","from":f"{from_date}","to":f"{to_date}"}
    headers = {"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": RAPID_API_HOST}
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# returns fixture on given time, future or past fixtures indicated by future param
def get_fixture(team_id, season, qty, future):
    if future == 'next':
        querystring = {"team":f"{team_id}", "season":f"{season}", "next":f"{qty}"}
    elif future == 'last':
        querystring = {"team":f"{team_id}", "season":f"{season}", "last":f"{qty}"}
    elif future != 'next' and future != 'last':
        print("invalid future/past indicator")
        exit()
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": RAPID_API_HOST}
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

#fixtures = get_league_fixtures(ids['laliga_2023_id'], "2023", "2023-10-21", "2023-10-23")
fixtures = get_fixture(ids['barca_team_id'], 2023, 1, 'last')
print(json.dumps(fixtures, indent=4))
