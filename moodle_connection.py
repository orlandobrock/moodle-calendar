import pickle
import requests
from bs4 import BeautifulSoup
import os


def login_credentials(token):
    return {
        'logintoken': token,
        'username': os.getenv('MATRICULA'),
        'password': os.getenv('SENHA')
     }

def get_sesskey(moodleSession):
    sess_key_url = 'https://moodle.gravatai.ifsul.edu.br/calendar/export.php?'
    form_key = moodleSession.get(sess_key_url)
    soup = BeautifulSoup(form_key.content, 'html5lib')
    return soup.find('input', attrs={'name': 'sesskey'})['value']


def get_cookie_key():
    headers = {'Connection': "keep-alive"}
    with requests.Session() as s:
        url = 'https://moodle.gravatai.ifsul.edu.br/login/index.php'
        secure = 'https://moodle.gravatai.ifsul.edu.br/my/'
        if not os.path.isfile('./somefile'):
            f = s.get(url)
            soup = BeautifulSoup(f.content, 'html5lib')
            data = login_credentials(soup.find('input', attrs={'name': 'logintoken'})['value'])
            x = s.post(url, data=data, headers=headers, cookies=s.cookies)
            r = s.get(secure)
            with open('somefile', 'wb') as f:
                pickle.dump(s.cookies, f)
        else:
            with open('somefile', 'rb') as f:
                s.cookies.update(pickle.load(f))
                return [s.cookies, get_sesskey(s)]
