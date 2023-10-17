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

# function to test sending text message
# assuming carrier will be verizon for simplicity
def send_txt(number):
    print(f'{number}@vtext.com')
    ezgmail.send(f'{number}@vtext.com', '', 'this is a test of python script')

# function to call api and recieve football data
def get_future_fixtures(league_id, season, from_date, to_date):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {"league":f"{league_id}","season":f"{season}","from":f"{from_date}","to":f"{to_date}"}
    headers = {
	"X-RapidAPI-Key": RAPID_API_KEY,
	"X-RapidAPI-Host": RAPID_API_HOST
}
    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())

get_future_fixtures(ids['laliga_2023_id'], "2023", "2023-10-21", "2023-10-23")
