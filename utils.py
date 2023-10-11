import json
import re
import requests

USERS_FILE = 'users.json'
KEYBOARD_FILE = 'keyboard.json'
MESSAGES_FILE = 'text.json'

API_URL = "https://ecmasecurity.uz/yourls-api.php"

API_USERNAME = "shortly"
API_PASSWORD = "123xensa"

def load(file):
  return json.load(open(f'{file}', 'r', encoding='utf-8'))

def dump(file, data):
  json.dump(data, open(f'{file}', 'w'))

def get_mes(mes):
  with open(MESSAGES_FILE, encoding='utf-8') as f:
    data = json.load(f)
    return data[mes]

def get_key(keyboard_name):
  with open(KEYBOARD_FILE, encoding='utf-8') as f:
    data = json.load(f)
    return data[keyboard_name]

def add_user(user_id:str):
  data = load(USERS_FILE)
  if str(user_id) not in data:
    data[str(user_id)] = {}
    dump(USERS_FILE, data)

def get_urls(user_id:str):
  data = load(USERS_FILE)
  return data[str(user_id)]

def add_url(user_id:str, url:str):
  add_user(str(user_id))
  data = load(USERS_FILE)
  data[str(user_id)].append(url['keyword'])
  data[str(user_id)][url['keyword']].append({
    "long_url": url['url']['url'],
    "date": url['url']['date'],
    "title": url['title'],
    "shorturl": url['shorturl']
  })
  dump(USERS_FILE, data)

def check_url(url):
  # Check if url is valid using regular expression example of valid url is "https or http://www.example.com"
  if re.match(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', url):
    return True
  
def long_to_short(long_url:str):
  # Convert long url to short url using bitly api
  res = requests.get(API_URL, params={
    "action": "shorturl",
    "format": "json",
    "username": API_USERNAME,
    "password": API_PASSWORD,
    "url": long_url})
  print(res.text)
  if(res.json()['statusCode'] == 200):
    
    return res.json()