#main class
class Game:
    def __init__(self, id):
        #ini self. variables
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0,0]
        self.ties = 0

    # getting player moves using the server
    def get_player_move(self, p):
        return self.moves[p]

    # getting players
    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    # checking with the servers if users are connected
    def connected(self):
        return self.ready

    # confrming with server if both players confirmed there move
    def bothWent(self):
        return self.p1Went and self.p2Went

    # algorithem to find the winning player
    def winner(self):

        #getting the player input and turning it upper
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1

        #converting leters to int
        def name2Number (name):
            if name == "R":
                return 1
            elif name == "P" :
                return 2
            elif name == "S" :
                return 3
        #finding the result
        p1= name2Number (p1)       
        p2= name2Number (p2)

        result = (p1-p2)%3

        if result == 0 :
            winner = -1
        elif result == 1 :
            winner = 0
        elif result == 2 :
            winner = 1

        return winner
    def resetWent (self):
        self.p1Went = False
        self.p2Went = False
            
