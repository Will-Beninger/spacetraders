from pathlib import Path
import curses
import curses.textpad
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
        header = f"| USER: {self.user} | CREDITS: {self.credits} | HQ: {self.headquarters} | ID: {self.account_id} |"
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

    def list_agent(self):
        url = f"{self.base_url}/my/agent"
        response = requests.get(url,headers=self.auth_header)
        return response

    def list_ships(self):
        url = f"{self.base_url}/my/ships"
        response = requests.get(url,headers=self.auth_header)
        return response
    
class Screen():
    UP = -1
    DOWN = 1
    def __init__(self):
        self.window = None
        self.width = 0
        self.height = 0
        self.max_lines = 0
        self.top = 0
        self.bottom = 0
        self.current = 0
        self.page = 0
        #Initialize the authorization token:
        path = getenv('HOME') + '/.spacetraders/token'
        token = Path(path).read_text()
        token = token.replace('\n', '')
        #Create new API Requester:
        self.requester = APIRequester(token)
        #This must be last!
        curses.wrapper(self.game_loop)


    def paging(self, direction):
        """Paging the window when pressing left/right arrow keys"""
        current_page = (self.top + self.current) // self.max_lines
        next_page = current_page + direction
        if next_page == self.page:
            self.current = min(self.current, self.bottom % self.max_lines - 1)
        if (direction == self.UP) and (current_page > 0):
            self.top = max(0, self.top - self.max_lines)
            return
        if (direction == self.DOWN) and (current_page < self.page):
            self.top += self.max_lines
            return
        
    def scroll(self, direction):
        """Scrolling the window when pressing up/down arrow keys"""
        next_line = self.current + direction
        if (direction == self.UP) and (self.top > 0 and self.current == 0):
            self.top += direction
            return
        if (direction == self.DOWN) and (next_line == self.max_lines) and (self.top + self.max_lines < self.bottom):
            self.top += direction
            return
        if (direction == self.UP) and (self.top > 0 or self.current > 0):
            self.current = next_line
            return
        if (direction == self.DOWN) and (next_line < self.max_lines) and (self.top + next_line < self.bottom):
            self.current = next_line
            return
        
    def login(self):
        #Test Login & Print Message
        self.requester.login()
        if (self.requester.login()):
            text = "Successfully logged in! Welcome to the Game!"
            self.window.addstr(self.height//2,self.width//2-len(text)//2,text,curses.color_pair(1))
            self.window.refresh()
        else:
            raise LoginFailed("Initial Login Failed, Check Connection or Token")
        curses.napms(2000)
        self.window.clear()
    
    def header(self):
        #Create a header with the user's details:
        header = self.requester.get_header()
        center = self.width//2-len(header)//2
        if (center<0):
            center=0
        self.window.addnstr(0,center,header,curses.COLS,curses.color_pair(1))

    def game_loop(self,s):
        # Clear screen & Initialize Settings:
        self.window = s
        self.max_lines=curses.LINES
        self.height, self.width = self.window.getmaxyx()
        self.window.clear()
        curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE)
        curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK)
        self.window.keypad(True)
        curses.noecho()
        curses.cbreak()

        #Test Login & Print Success/Failure
        self.login()
        
        #Put a header at the top of the window
        self.header()

        #Create Option Menu:
        menuStartY=2 #Set what Y axis to start the menu at
        menuStartX=0 #Menu X Axis Alignment to the left
        self.window.addstr(menuStartY,menuStartX,"Press 'ESC' to quit",curses.color_pair(2))
        self.window.addstr(menuStartY+1,menuStartX,"1. List Agent",curses.color_pair(2))

        #Get Input:
        while True:
            c = self.window.getch()
            if c == curses.ascii.ESC:
                break
            elif c == ord('1'): #List Agent
                output = self.requester.list_ships()
                cleanOutput = str(output.json()['data'])
                lines = len(cleanOutput)//60
                padResult.addstr(str(output.json()['data']))
                curY,curX = padResult.getyx()
                padResult.refresh(0, 0, 7, 5, self.height-7, self.width-2-5)
                while True:
                    cmd = padResult.getch()
                    if  (cmd == curses.KEY_DOWN or cmd == 259 or cmd == ord('e') ):
                        curX+=1
                        padResult.move(curY,curX)
                        #padResult.refresh(padPos, 0, 7, 5, height-7, width-2-5)
                    elif (cmd == curses.KEY_DOWN or cmd == 259 or cmd == ord('d')):
                        curX-=1
                        padResult.move(curY,curX)
                        #padResult.refresh(padPos, 0, 7, 5, height-7, width-2-5)
                    if cmd == ord('w'):
                        padResult.clear()
                        s.refresh()
                        break
            else:
                text = "You pressed:"+chr(c)+" or "+str(c)
                self.window.addstr(curses.LINES//2,curses.COLS//2-len(text)//2,text,curses.color_pair(1))


if __name__ == '__main__':
    #Initialize Curses Screen
    s = Screen()