from pathlib import Path
import curses
from os import getenv
import requests

class APIRequester:
    def __init__(self, token):
        self.base_url = "https://api.spacetraders.io/v2"
        self.auth_header = {'Authorization' : 'Bearer '+token}

        #Variables awaiting initialization from login()
        self.user = ""
        self.account_id = ""
        self.credits = 0
        self.headquarters =""

    def login(self):
        url = f"{self.base_url}/my/agent"
        response = requests.get(url,headers=self.auth_header)
        if (response.status_code == 200):
            self.user         = response.json()['data']['symbol']
            self.account_id   = response.json()['data']['accountId']
            self.credits      = response.json()['data']['credits']
            self.headquarters = response.json()['data']['headquarters']
            return True
        else:
            return False

    def get_header(self):
        header = f"|  USER: {self.user}  |  CREDITS: {self.credits}  |"
        return header

    def send_request(self, endpoint, method='GET', data=None):
        url = f"{self.base_url}/{endpoint}"
        if method == 'GET':
            response = requests.get(url,headers=self.auth_header)
        elif method == 'POST':
            response = requests.post(url, data=data, headers=self.auth_header)
        else:
            raise ValueError("Invalid HTTP method. Allowed values: 'GET' or 'POST'.")
        return response

def game_loop(s):
    # Clear screen & Initialize Settings:
    s.clear()
    curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE)

    #Initialize the authorization token:
    path = getenv('HOME') + '/.spacetraders/token'
    token = Path(path).read_text()
    token = token.replace('\n', '')

    #Create new API Requester:
    requester = APIRequester(token)

    #Test Login & Print Message
    requester.login()
    if (requester.login()):
        text = "Successfully logged in! Welcome to the Game!"
        s.addstr(curses.LINES//2,curses.COLS//2-len(text)//2,text,curses.color_pair(1))
        s.refresh()
    else:
        raise LoginFailed("Initial Login Failed, Check Connection or Token")
    curses.napms(2000)
    s.clear()

    #Create a header with the user's details:
    header = requester.get_header()
    s.addstr(0,curses.COLS//2-len(header)//2,header,curses.color_pair(1))
    s.refresh()

    #Create Option Menu:
    menuStartY=2 #Set what Y axis to start the menu at
    menuStartX=0 #Menu X Axis Alignment to the left
    s.addstr(menuStartY,menuStartX,"Press 'q' to quit",curses.color_pair(1))

    #Get Input:
    while True:
        c = s.getch()
        if c == ord('q'):
            break
        else:
            text = "You pressed:"+chr(c)
            s.addstr(curses.LINES//2,curses.COLS//2-len(text)//2,text,curses.color_pair(1))


if __name__ == '__main__':
    #Initialize Curses Screen
    curses.wrapper(game_loop)
