import socket
import threading
from queue import Queue


IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"
opponentTurn = "Opponent's Turn"
yourTurn = "Your Turn"
lost = "You Lose"
Win = "You Win"

#available boards for match (currently  = 5)
boards = []

#defining a board for the match
class memory:
    board = [['|','|','|'],['|','|','|'],['|','|','|']]
    turn = -1
    moves = 0
    flag = [0,0]
    result = "unallocated"

    def reset(self):
        self.turn = 0
        self.moves = 0
        self.reset = "unallocated"
        self.board = [['|','|','|'],['|','|','|'],['|','|','|']]
    def changeTurn(self):
        if(self.turn == 1):
            self.turn = 2
        else:
            self.turn = 1

    def start(self):
        self.turn = 2

    def move(self,x,y,value):
        self.board[x][y] = value
        self.moves = self.moves+1
    
    def win(self,player):
        if(self.moves < 5):
            return False
        else:
            if(self.board[0][0] == self.board[0][1]==self.board[0][2] and self.board[0][2]!='|'):
                result = "finished"
                return True
            elif(self.board[1][0] == self.board[1][1]==self.board[0][2] and self.board[1][2]!='|'):
                result = "finished"
                return True
            elif(self.board[2][0] == self.board[2][1]==self.board[2][2] and self.board[2][2]!='|'):
                result = "finished"
                return True
            elif(self.board[0][0] == self.board[1][0]==self.board[2][0] and self.board[0][0]!='|'):
                result = "finished"
                return True
            elif(self.board[0][1] == self.board[1][1]==self.board[2][1] and self.board[0][1]!='|'):
                result = "finished"
                return True
            elif(self.board[0][2] == self.board[1][2]==self.board[2][2] and self.board[0][2]!='|'):
                result = "finished"
                return True
            elif(self.board[0][0] == self.board[1][1]==self.board[2][2] and self.board[0][0]!='|'):
                result = "finished"
                return True
            elif(self.board[0][2] == self.board[1][1]==self.board[2][0] and self.board[0][2]!='|'):
                result = "finished"
                return True
            else:
                return False


#list of players requesting an opponent
players = Queue(0)

#dictionary to keep the corresponding board
users = {}
foundMatchBoard = {}

def handle_client(conn, addr):
   
    msg = conn.recv(SIZE).decode(FORMAT)
    print(f"[NEW SOLDIER] {addr} connected. with username {msg} 🐱‍👤")

    if(players.qsize() == 0):
        players.put(msg)
        cont = True
        while(cont):
            if msg in users.keys():
                opponent = "Your opponent is " + users[msg] +"\n Waiting for Match to Start .. \n"
                del users[msg]
                conn.send(opponent.encode(FORMAT))
                cont = False

        memLoc = -1
        cont = True
        while(cont):
            if msg in users.keys():
                memLoc = users[msg]
                del users[msg]
                cont = False
        
        #TurnMessage = "2"
        #conn.send(TurnMessage.encode(FORMAT))
        while True:

            boards[memLoc].flag[0] = 1
            boards[memLoc].turn = 1
            i = 0
            while(boards[memLoc].flag[1]==1 and boards[memLoc].turn==1):
                if i==0:
                    conn.send(opponentTurn.encode(FORMAT))
                    i = i+1

            if(boards[memLoc].result == "finished"):
                conn.send(lost.encode(FORMAT))
                break
            else:
                print(boards[memLoc].turn)
                conn.send(yourTurn.encode(FORMAT))
                x = conn.recv(1024).decode(FORMAT)
                y = conn.recv(1024).decode(FORMAT)
                boards[memLoc].flag[0] = 0
                #boards[memLoc].move(int(x),int(y),'O')
                #if(boards[memLoc].win(1) == True):
                 #   conn.send(Win.encode(FORMAT))
                  #  break
                #else:
                 #   boards[memLoc].changeTurn()
        conn.close()

    else:
        while(players.qsize() == 0):
            if(players.qsize()>0):
                break
        opponent = players.get()
        

        cont = True
        memLoc = -1
        while(cont):
            for i in range(len(boards)):
                if(boards[i].result == "unallocated"):
                    cont = False
                    boards[i].result = "allocated"
                    memLoc = i
        
        users[opponent] = msg
        oppo = "Your opponent is " + opponent
        conn.send(oppo.encode(FORMAT))  

        if opponent in users.keys():
            print("Not deleted yet")
        else:
            print("Key deleted")
            
        users[opponent] = memLoc
        #TurnMessage = "1"
        #conn.send(TurnMessage.encode(FORMAT))

        while True:
            
            boards[memLoc].flag[1] = 1
            boards[memLoc].turn = 0
            
            i = 0
            while(boards[memLoc].flag[0]==1 and boards[memLoc].turn==0):
                if i==0:
                    conn.send(opponentTurn.encode(FORMAT))
                    i = i+1
            
            if(boards[memLoc].result == "finished"):
                conn.send(lost.encode(FORMAT))
                break
            else:
                print(boards[memLoc].turn)
                conn.send(yourTurn.encode(FORMAT))
                x = conn.recv(1024).decode(FORMAT)
                y = conn.recv(1024).decode(FORMAT)

               # boards[memLoc].move(int(x),int(y),'O')
                boards[memLoc].flag[1] = 0

                #if(boards[memLoc].win(1) == True):
                 #   conn.send(Win.encode(FORMAT))
                  #  break
                #else:
                 #   boards[memLoc].changeTurn()
        
        boards[memLoc].reset()
        conn.close()
def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")
    boards.append(memory())
    boards.append(memory())
    boards.append(memory())
    boards.append(memory())
    boards.append(memory())

    for obj in boards:
        print(obj.moves, obj.result,sep = ' ')

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()