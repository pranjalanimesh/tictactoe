import socket
import threading
import time

class TicTacToe:
    
    def __init__(self):
        self.ttt=[[" "," "," "],
                  [" "," "," "],
                  [" "," "," "]]
        self.turn= "X"
        self.you= "X"
        self.opponent= "O"
        self.winner = None
        self.game_over = False
        self.counter = 0
    

    def host_game(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host,port))
        server.listen(1)

        client, addr = server.accept()

        self.you = "X"
        self.opponent = "O"
        threading.Thread(target=self.handle_connection, args=(client,)).start()
        server.close()

    def connect_to_game(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        self.you = "O"
        self.opponent = "X"
        threading.Thread(target=self.handle_connection, args=(client,)).start()

    def handle_connection(self, client):
        while not self.game_over:
            if self.turn==self.you:
                move = input("Enter your move:")
                if self.check_valid_move(move.split(',')):
                    client.send(move.encode('utf-8'))
                    self.apply_move(move.split(','),self.you)
                    self.turn=self.opponent
                else:
                    print("Invalid move!!!")

            else:
                data = client.recv(1024)
                if not data:
                    client.close()
                    break
                else:
                    self.apply_move(data.decode('utf-8').split(','), self.opponent)
                    self.turn = self.you
    
        client.close() 
    
    def apply_move(self, move, player):
        if self.game_over:
            return
        self.counter +=1
        self.ttt[int(move[0])][int(move[1])] = player
        self.print_ttt()
        if self.check_if_won():
            if self.winner == self.you:
                print("You Win!!!")
                quit()
            elif self.winner == self.opponent:
                print("You Lose")
                quit()
        else:
           if self.counter==9:
                print("It is a tie!!!")
                quit()

    def check_valid_move(self, move):
        return self.ttt[int(move[0])][int(move[1])]==" "

    def check_if_won(self):
        for row in range(3):
            if self.ttt[row][0] == self.ttt[row][1] ==self.ttt[row][2] !=" ":
                self.winner = self.ttt[row][0]
                self.game_over = True
                return True
        for col in range(3):
            if self.ttt[0][col] == self.ttt[1][col] == self.ttt[0][col] != " ":
                self.winner = self.ttt[0][col]
                self.game_over = True
                return True

        if self.ttt[0][0] == self.ttt[1][1] == self.ttt[2][2] != " ":
                self.winner = self.ttt[0][0]
                self.game_over = True
                return True
        if self.ttt[0][2] == self.ttt[1][1] == self.ttt[2][0] != " ":
                self.winner = self.ttt[0][2]
                self.game_over = True
                return True 

    def print_ttt(self):
        for row in range(3):
            print(" | ".join(self.ttt[row]))
            if row !=2:
                print("------------")

