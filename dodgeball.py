###################################################################
# This is my first game - programName: Dodging Circle
# Heart, Background, Stripe in the same directory are needed to load the game.
#Settings:

path = "./resources/" 

info = "Made by NEOZEO 24.05.19"
program_name = "DodgeBall"


probability_ = 80#/1000    #the start-probability to spawn stripe
probability_addition = 0.8  #the speed of the addition to the sprite-probability
heart_number = 3  #how many hearts do you want on start (they woudn't be showed)
score = 0   #this is the start-score
score_addition_per_stripe = 1
stripe_speed_min = 2 #the min speed of the stripes
stripe_speed_max = 8 #the max speed of the stripes
stripe_width_min = 4
stripe_width_max = 40
stripe_height_min = 24
stripe_height_max = 120
mouseControl = False



fullscreen = False  # If true: The game runs Fullscreen

screen_width = 800
screen_height = 480

FPS = 60

gui_X_pos = 4
gui_Y_pos = 40
gui_font_size = 10

title_pos_Y = 20

player_Y_pos = int(screen_height * 0.9)
player_width = 40
player_height = 40


heart_witdh = 30
heart_height = 30


gap_between_buttons = 20 #gap between every button of the GUIs
gap_between_label_bgrect = 40 #bgrect = background-rect

#######################################################################################################################################
class Player(object):
    def __init__(self,xc,yc,width,height): #xc - xpos center, yc - ypos center
        self.pos = {'x1':xc-width/2, 'y1':yc-height/2, 'x2':xc+width/2, 'y2':yc+height/2,'xc':xc,'yc':yc}
        self.width = width
        self.height = height
        self.pic = pg.transform.scale(pg.image.load(path+'Player.png'), (self.width, self.height))
    def gotomouse(self,mx): #only go to mouse x-Position , stay on actual y-Position
        if mouseControl:
            self.pos['xc'] = mx

            self.pos['x1'] = mx - self.width / 2
            self.pos['x2'] = mx + self.width / 2
            if self.pos['x2'] > screen_width:
                self.pos['x1'] = screen_width - self.width
                self.pos['x2'] = screen_width
            elif self.pos['x1'] < 0:
                self.pos['x1'] = 0
                self.pos['x2'] = 0 + self.width
        else:
            keys = pg.key.get_pressed()

            if keys[pg.K_d]:
                self.pos['x1'] += 10
                self.pos['x2'] += 10
            elif keys[pg.K_a]:
                self.pos['x1'] -= 10
                self.pos['x2'] -= 10


            if self.pos['x2'] > screen_width:
                self.pos['x1'] = screen_width - self.width
                self.pos['x2'] = screen_width
            elif self.pos['x1'] < 0:
                self.pos['x1'] = 0
                self.pos['x2'] = 0 + self.width

    def show(self):
        screen.blit(self.pic, (self.pos['x1'], self.pos['y1']))
class Stripe(object):
    def __init__(self,speed,x,y,width,height):
        self.pos = {'x1':x, 'y1':y, 'x2':x+width, 'y2':y+height,'xc':x+width/2}
        self.width = width
        self.height = height
        self.speed = speed
        self.pic = pg.transform.scale(pg.image.load(path+'Stripe.png'), (self.width,self.height))
    def move(self):
        self.pos['y1'] += self.speed #move the stripes
        self.pos['y2'] += self.speed
    def outOfScreen(self):
        return self.pos['y1'] > screen_height
class Button(object):
    def __init__(self,xc,yc,label,width=300,fontSize=40,borderThickness=8,lineThickness=2,fontColor=(250,250,250),lineColor=(100,100,255),backgroundColor = [0,0,200]):

        self.label = label
        self.lineColor = lineColor
        self.lineThickness = lineThickness
        self.fontColor = fontColor
        self.fontSize = fontSize

        r,g,b = backgroundColor
        self.mouseNotOverButtonColor = (r,g,b)

        if r-50 < 0: r = 50
        if g-50 < 0: g = 50
        if b-50 < 0: b = 50
        self.mouseOverButtonColor = (r-50,g-50,b-50)

        if r-80 < 0: r = 80
        if g-80 < 0: g = 80
        if b-80 < 0: b = 80
        self.buttonPressedColor = (r-80,g-80,b-80)

        self.font = pg.font.Font('freesansbold.ttf', self.fontSize)
        self.renderedLabel = self.font.render(self.label, True,self.fontColor)
        self.labelWidth = self.renderedLabel.get_width()
        self.labelHeight = self.renderedLabel.get_height()

        self.pos = {'x1':xc-width/2, 'y1':yc-self.labelHeight/2-borderThickness, 'x2':xc+width/2, 'y2':yc+self.labelHeight/2+borderThickness}
        self.lineRect = pg.Rect(self.pos['x1'], self.pos['y1'],self.pos['x2']-self.pos['x1'], self.pos['y2']-self.pos['y1'])
        self.backgroundRect = pg.Rect(self.pos['x1']+self.lineThickness, self.pos['y1']+self.lineThickness,self.pos['x2']-self.pos['x1']-2*self.lineThickness, self.pos['y2']-self.pos['y1']-2*self.lineThickness)

    def checkMouseOverButton(self,mx,my):
        if self.pos['x1'] < mx < self.pos['x2'] and self.pos['y1'] < my < self.pos['y2']:
            return True
        else:
            return False

    def show(self,mx,my,lP):
            pg.draw.rect(screen, self.lineColor, self.lineRect)

            if self.pos['x1'] < mx < self.pos['x2'] and self.pos['y1'] < my < self.pos['y2']:
                if lP:
                    pg.draw.rect(screen, self.buttonPressedColor, self.backgroundRect)
                else:
                    pg.draw.rect(screen, self.mouseOverButtonColor, self.backgroundRect)
            else:
                pg.draw.rect(screen, self.mouseNotOverButtonColor, self.backgroundRect)

            screen.blit(self.renderedLabel,(self.pos['x1']+(self.pos['x2']-self.pos['x1'])/2-self.labelWidth/2 , self.pos['y1'] + (self.pos['y2']-self.pos['y1']) / 2 - self.labelHeight/2))
class GUI(object):
    def __init__(self,x,y,fontSize,fontColor):
        self.pos = {'x1':x,'y1':y}
        self.fontColor = fontColor
        self.fontSize = fontSize
        self.font = pg.font.Font('freesansbold.ttf', self.fontSize)
        test = self.font.render("test", True, self.fontColor)
        self.lineThickness = test.get_height()
    def show(self):
        global clock,stripes
        self.labels = [
            self.font.render("fps: {}".format(str(round(clock.get_fps()))), True, self.fontColor),
            self.font.render("Score:{}".format(str(score)), True, self.fontColor),
            self.font.render("playercoordinates: {},{}".format(str(player.pos['xc']),str(player.pos['yc'])), True, self.fontColor),
            self.font.render("Number of Stripes: {}".format(str(len(stripes))), True, self.fontColor)
            ]
        for label in self.labels:
            screen.blit(label, (self.pos['x1'],self.pos['y1']+(self.labels.index(label)*self.lineThickness*1.2)))

def start():
    global work, run, mLP, gap_between_buttons,screen_width,screen_height,info,program_name,gameRun
    print("startMenu runs")
    playButton = Button(int(screen_width/2),int(screen_height/2),"Play")
    quitButton = Button(int(screen_width/2),int(screen_height/2+(playButton.pos['y2']-playButton.pos['y1'])+gap_between_buttons),"Quit")

    titleFont = pg.font.Font('freesansbold.ttf', 100)
    title = titleFont.render(program_name, True, (0,20,180))
    titlePos = {'x':screen_width/2-title.get_width()/2,'y':title_pos_Y,'w':title.get_width(),'h':title.get_height()}

    infoFont = pg.font.Font('freesansbold.ttf', 10)
    infoLabel = infoFont.render(info, True, (0,20,180))

    screen.blit(backgroundPic, (0,0))
    screen.blit(title,(titlePos['x'],titlePos['y']))
    screen.blit(infoLabel,(10,screen_height-infoLabel.get_height()-10))

    pg.mouse.set_visible(True)

    startLoop = True
    while startLoop:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                work = 0
                run = 0
                startLoop = 0

        lP,mP,rP = pg.mouse.get_pressed()
        mx,my = pg.mouse.get_pos() #mx: mouse-x-pos; my: mouse-y-pos
        if lP:
            if mLP:
                if playButton.checkMouseOverButton(mx,my):
                    print("Playbutton pressed")
                    gameRun = True
                    startLoop = False
                if quitButton.checkMouseOverButton(mx,my):
                    print("Quitbutton pressed")
                    work = False
                    gameRun = False
                    startLoop = False
            mLP = False
        else:
            mLP = True

        clock.tick(FPS)

        playButton.show(mx,my,lP)
        quitButton.show(mx,my,lP)
        pg.display.update()

def escapeMenu():
    global run,mLP, gameRun
    pg.mouse.set_visible(True)
    continueButton = Button(screen_width/2,screen_height/2,"Continue")
    backButton = Button(screen_width/2,screen_height/2+continueButton.pos['y2']-continueButton.pos['y1']+gap_between_buttons,"Back to Menu")

    titleFont = pg.font.Font('freesansbold.ttf', 100)
    titleLabel = titleFont.render("Stop", True, (0,20,180))
    infoFont = pg.font.Font('freesansbold.ttf', 10)
    infoLabel = infoFont.render(info, True, (0,20,180))

    escapeMenuOn = True


    screen.blit(backgroundPic, (0,0))
    for stripe in stripes:
        screen.blit(stripe.pic, (stripe.pos['x1'], stripe.pos['y1']))
    titlePos = {'x':screen_width/2-titleLabel.get_width()/2,'y':title_pos_Y,'w':titleLabel.get_width(),'h':titleLabel.get_height()}
    screen.blit(titleLabel,(titlePos['x'],titlePos['y']))
    screen.blit(infoLabel,(10,screen_height-infoLabel.get_height()-10))
    print("EscapeMenu runs")
    while escapeMenuOn:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                work = 0
                run = 0
                escapeMenuOn = 0


        lP,mP,rP = pg.mouse.get_pressed()
        mx,my = pg.mouse.get_pos() #mx: mouse-x-pos; my: mouse-y-pos

        if lP:
            if mLP:
                if continueButton.checkMouseOverButton(mx,my):
                    print("continueButton pressed")
                    escapeMenuOn = False
                if backButton.checkMouseOverButton(mx,my):
                    print("backButton pressed")
                    gameRun = False
                    escapeMenuOn = False
            mLP = False
        else:
            mLP = True

        continueButton.show(mx,my,lP)
        backButton.show(mx,my,lP)
        pg.display.update()
    pg.mouse.set_visible(False)

def game():
    global heart_number,probability,score,stripes,gameRun
    stripes = []
    heartNumber = heart_number
    score_ = score
    quit = False
    pg.mouse.set_visible(False)
    probability = probability_
    print("game runs")
    while gameRun:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                work = 0
                gameRun = 0

        keys = pg.key.get_pressed()
        mx,my = pg.mouse.get_pos() #mx: mouse-x-pos; my: mouse-y-pos

        if keys[pg.K_ESCAPE]:
            print("escapeMenu open")
            escapeMenu()
            print("escapeMenu closed")

        player.gotomouse(mx)

        if heartNumber < 0:
            gameRun = False

        if r.randrange(0,1000) < probability:

            newStripeWidth = r.randrange(stripe_width_min,stripe_width_max)
            newStripeHeight = r.randrange(stripe_height_min,stripe_height_max)
            newStripeX = r.randrange(0,screen_width-newStripeWidth)
            newStripeSpeed = r.randrange(stripe_speed_min,stripe_speed_max)
            stripes.append(Stripe(newStripeSpeed, newStripeX,-newStripeHeight,newStripeWidth, newStripeHeight))

        screen.blit(backgroundPic, (0,0))
        for stripe in stripes:
            stripe.move()
            #if player.pos['xc'] < stripe.pos['x1']:
            #    stripe.pos['x1'] -= (stripe.pos['x1'] - player.pos['xc'])/32
            #if player.pos['xc'] > stripe.pos['x1']:
            #    stripe.pos['x1'] += (player.pos['xc']-stripe.pos['x1'])/32

            if stripe.pos['y2'] >= player.pos['y1']+3 and stripe.pos['y1'] <= player.pos['y2']-3:

                if player.pos['x1'] < stripe.pos['x1'] < player.pos['x2'] or player.pos['x1'] < stripe.pos['x2'] < player.pos['x2']:
                    heartNumber -= 1
                    del stripes[stripes.index(stripe)]

            if stripe.outOfScreen():
                del stripes[stripes.index(stripe)]
                score += score_addition_per_stripe
                probability += probability_addition

        #show

        for g in range(heartNumber):
            screen.blit(heart, (screen_width * (0.95 - g * 0.05) ,15))
        for stripe in stripes:
            screen.blit(stripe.pic, (stripe.pos['x1'], stripe.pos['y1']))
        player.show()
        gui.show()
        pg.display.update()
        print("Updated")

        clock.tick(FPS)
    print("Game Over at Score: {}".format(score))

##########################################################################################################
#Setup
import pygame as pg
import random as r
pg.init()
if pg.joystick.get_count() == 1:
    pg.joystick.init()
    con = pg.joystick.Joystick(0)
    con.init()
    controllerConnected = True
else:
    controllerConnected = False


print(2*"\n"+"Packages imported")


#infoObject = pg.display.Info()
if fullscreen:
    screen = pg.display.set_mode((screen_width,screen_height),pg.FULLSCREEN)
else:
    screen = pg.display.set_mode((screen_width,screen_height))

work = True
pg.display.set_caption(program_name)
heart = pg.image.load(path+'Heart.png')
heart = pg.transform.scale(heart, (heart_witdh, heart_height)) #resize the picture
backgroundPic = pg.image.load(path+'Background.png')
backgroundPic = pg.transform.scale(backgroundPic, (screen_width,screen_height)) #resize the picture

clock = pg.time.Clock()
mLP = False
player = Player(0,player_Y_pos,player_width,player_height)
gui = GUI(gui_X_pos,gui_Y_pos,gui_font_size,(0,0,0))

font = pg.font.Font(None, 70)

############################################################################################################
#mainloop

while work:
    print("work run")
    start()
    game()

############################################################################################################
#end
pg.quit()
print("Dodgeball ended.")
