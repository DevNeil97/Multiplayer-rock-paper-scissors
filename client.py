#importing modules
import pygame
from network import Network

#setting up the wndow size
pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

#Buttons of the Client 
class Button:
    #init funtion
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100
    #main window details
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        #setting the posistion of the text inside the buttons
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))
                        
    #def if user clicked
    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

#Main windows colors and data
def redrawWindow (win, game, p):
    win.fill((29,22,47))
    
    #waiting for players text
    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255,255,255), True)
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        #getting the player  moves and displaying them
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (255,255,255))
        win.blit(text, (80, 200))
        text = font.render("Opponents", 1, (255,255,255))
        win.blit(text, (380, 200))

        #passing the moves to the game.py
        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        #displaying player 1 and player 2 moves
        if game.bothWent():
            text1 = font.render(move1, 1, (127, 179, 213))
            text2 = font.render(move2, 1, (127, 179, 213))
        #displaying additional information
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (179, 182, 183 ))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (127, 179, 213))
            else:
                text1 = font.render("Waiting...", 1, (127, 179, 213))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (123, 36, 28))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (127, 179, 213))
            else:
                text2 = font.render("Waiting...", 1, (127, 179, 213))

        #displaying winner
        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()

#plaing button setup (Rock Paper Scissors)
btns = [Button("Rock", 50, 500, (33, 47, 60)), Button("Scissors", 250, 500, (136, 78,160)),
        Button("Paper", 450, 500, (185, 119, 14))]

#def main
def main():

    run = True
    clock = pygame.time.Clock()
    #importing Network module and player from game module
    n = Network()
    player = int(n.getP())
    #pronting player number (For debugging)
    print("You are player", player)

    while run:
        clock.tick(60)
        #asking the server to send the game class every clock cycle.
        try:
            game = n.send("get")
            #if server does not working. (Game.py error)
        except:
            run = False
            print("Couldn't get game")
            break

        #cheaking if both players went and if not delaying.
        #if both players went resetting the moves for next round
        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break
            #displaying the won, lose or tie game
            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (146, 43, 33 ))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (20, 143, 119))
            else:
                text = font.render("You Lost...", 1, (146, 43, 33))

            #text formatting
            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(2000)

        #closing the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            #getting player mouse inputs and passing it to the game.py vis server
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                #asking the server to connect the player with another player
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)

#main screen Data and colors
def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((29,22,47))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255, 255, 255))
        win.blit(text, (100, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


while True:
    menu_screen()
