from tkinter import Tk, PhotoImage, Button, messagebox, Canvas, Label, Entry
import random
import time


def setWindowDimensions():
    global width, height
    window = Tk()
    window.title("Get Out")
    width = window.winfo_screenwidth()  # computers screen size
    height = window.winfo_screenheight()

    x = 0
    y = 0
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))  #window size
    return window


def restart_program(pause):
    global main_canvas, menu_canvas  #set all variables to 00000000000000000000000
    main_canvas.pack_forget()
    menu_canvas.pack()
    menu_canvas.focus_set()

    if not pause:
        main_canvas.end_button.destroy()
        main_canvas.enterName.destroy()
        main_canvas.stop_label.destroy()
        main_canvas.stop_label2.destroy()
        main_canvas.stop_label3.destroy()
    else:
        pause_canvas.pack_forget()

    main_canvas.isJumping = False  #IF MAN IS JUMPING
    main_canvas.manWidth = 25  #SIZE OF MAAN
    main_canvas.manHeight = 25
    main_canvas.speed = 6  #MOVEMENT SPEED
    main_canvas.jumpDistance = 240
    main_canvas.velocity = 5  #Y-COORDINATE MOVEMENT SPEED
    main_canvas.comeBackPositionY = 0  #COORDINATE OF JUMP START
    main_canvas.airStop = False  #IF REACHED MAX IN AIR
    main_canvas.moveY = 0  #HOW FAR WE ARE MOVING WITH ONE CLICK YYYYY
    main_canvas.moveX = 0  #XXXXX
    main_canvas.direction = ""  #MOVING TO...
    main_canvas.image1 = 0
    main_canvas.score = 0
    main_canvas.teleport = False
    main_canvas.highJump = False

    main_canvas.coords(main_canvas.man, main_canvas.manWidth*3, height-main_canvas.manWidth*6)
    main_canvas.coords(platform1.platform,width-40, height-180, width, height-120)
    main_canvas.coords(platform2.platform, width + 600, height-180, width+640, height-120)
    main_canvas.coords(platform3.platform, width + 660, height-180, width+700, height-120)


def game_over():
    main_canvas.stop_label = Label(main_canvas, text = "Game Over!", bg = main_canvas.bg)
    main_canvas.stop_label.place(relx=0.5, rely=0.2, anchor = 'center')

    if main_canvas.score > -1:
        main_canvas.stop_label2 = Label(main_canvas, text = "Well Done!", bg = main_canvas.bg)
        main_canvas.stop_label2.place(relx=0.5, rely=0.25, anchor = 'center')

        main_canvas.stop_label3 = Label(main_canvas, text="Type your name please: ", bg = main_canvas.bg)
        main_canvas.stop_label3.place(relx=0.45, rely=0.3, anchor = 'center')

        main_canvas.enterName = Entry(main_canvas)
        main_canvas.enterName.place(relx=0.5, rely=0.3, anchor='center')

        end_game_command = lambda: restart_program(False)
        main_canvas.end_button = Button(main_canvas, text="Continue", width=15, height=1, command=end_game_command)
        main_canvas.end_button.place(relx=0.5, rely=0.4, anchor='center')
        main_canvas.end_button.config(font=("Courier", 18))


def moveMan():
    print(main_canvas.score)
    main_canvas.label_score()
    main_canvas.update()
    main_canvas.positions = main_canvas.coords(main_canvas.man)
    print(main_canvas.positions)
    print("Speed" + str(main_canvas.speed))
    print("Speed v" + str(main_canvas.velocity))
    #INCREASE SPEED AT SCORE 3, 5, 10


    #MOVE PLATFORMS
    platform1.move(main_canvas.speed, True)
    if main_canvas.score >=5:
        platform2.move(main_canvas.speed, False)
    if main_canvas.score >=10:
        platform3.move(main_canvas.speed, False)


    if(main_canvas.teleport):

    #NEED COLLISION CONTROL FOR THE MAN, SO HE CAN'T ESCAPE THE LEVEL
        if(main_canvas.positions[0]<=main_canvas.manWidth):
            main_canvas.coords(main_canvas.man, main_canvas.manWidth, main_canvas.positions[1])
        elif(main_canvas.positions[0]>=width):
            main_canvas.coords(main_canvas.man, main_canvas.manWidth, main_canvas.positions[1])
    else:
    #NEED COLLISION CONTROL FOR THE MAN, SO HE CAN'T ESCAPE THE LEVEL
        if(main_canvas.positions[0]<=main_canvas.manWidth):
            main_canvas.coords(main_canvas.man, main_canvas.manWidth, main_canvas.positions[1])
        elif(main_canvas.positions[0]>=width-main_canvas.manWidth):
            main_canvas.coords(main_canvas.man, width-main_canvas.manWidth, main_canvas.positions[1])


#x-coordinate moving logic
    if main_canvas.direction == "left":
        main_canvas.updateImage()
        main_canvas.move(main_canvas.man, -main_canvas.speed, 0)
    elif main_canvas.direction == "right":
        main_canvas.updateImage()
        main_canvas.move(main_canvas.man, main_canvas.speed, 0)

    if main_canvas.highJump:
        main_canvas.jumpDistance = 500
    else:
        main_canvas.jumpDistance = 240

#y-coordinate moving object
    if main_canvas.isJumping:
        main_canvas.unbind("<Up>")
        main_canvas.unbind("j")
        main_canvas.updateImage()


        if main_canvas.positions[1] != main_canvas.moveY and not main_canvas.airStop:
            main_canvas.move(main_canvas.man, 0, -main_canvas.velocity)
        elif main_canvas.positions[1] < main_canvas.comeBackPositionY:
            main_canvas.move(main_canvas.man, 0, main_canvas.velocity)
        else:
            main_canvas.coords(main_canvas.man, main_canvas.positions[0], height-main_canvas.manWidth*6)
            main_canvas.isJumping = False

        if main_canvas.positions[1] <= main_canvas.moveY:
            main_canvas.airStop = True
    else:
        main_canvas.bind("<Up>", main_canvas.upKey)
        main_canvas.bind("j", lambda e: main_canvas.highJumpButton())


#game over logic
    print(main_canvas.focus_get())
    inGame = str(main_canvas.focus_get()) == '.!my_canvas'
    inProgram = str(main_canvas.focus_get()) == '.!my_canvas2' or main_canvas.focus_get() == '.!my_canvas3'

    manPosition = main_canvas.coords(main_canvas.man)
    platformPosition1 = main_canvas.coords(platform1.platform)
    platformPosition2 = main_canvas.coords(platform2.platform)
    platformPosition3 = main_canvas.coords(platform3.platform)

    if main_canvas.collision(manPosition, platformPosition1) or main_canvas.collision(manPosition, platformPosition2) or main_canvas.collision(manPosition, platformPosition3) :
        game_over()
    elif inGame:
        main_canvas.after(30, moveMan)



class My_canvas(Canvas):
    def __init__(self, window, width, height, bg, name):
        super().__init__(window, bg=bg, width=width, height=height)
        self.name = name
        self.bind_keys()
        self.bg=bg


        if self.name == "main_canvas":
            self.isJumping = False#IF MAN IS JUMPING
            self.manWidth = 25#SIZE OF MAAN
            self.manHeight = 25
            self.speed = 6#MOVEMENT SPEED
            self.jumpDistance = 240
            self.velocity = 5#Y-COORDINATE MOVEMENT SPEED
            self.comeBackPositionY = 0#COORDINATE OF JUMP START
            self.airStop = False#IF REACHED MAX IN AIR
            self.moveY = 0#HOW FAR WE ARE MOVING WITH ONE CLICK YYYYY
            self.moveX = 0#XXXXX
            self.direction = ""#MOVING TO...
            self.image1 =0
            self.score = 0
            self.teleport = False
            self.highJump = False

            self.label_score()
            self.create_floor()
            self.create_man()

        elif self.name == "menu_canvas":
            #self.focus_set()
            start_game_command=lambda: self.start_game(menu_canvas, main_canvas)
            leaderboard_command = lambda: self.leaderboard()
            tutorial_command = lambda: self.switch_canvas(menu_canvas, tutorial_canvas)

            self.label = Label(self, text = "Main Menu", bg = bg)
            self.label.config(font=("Courier", 44))
            self.label.place(relx=0.5, rely=0.2, anchor = 'center')

            self.switch_canvas_button("Tutorial",tutorial_command,0.5,0.60)
            self.switch_canvas_button("Leaderboard",leaderboard_command,0.5,0.50)
            self.switch_canvas_button("Play",start_game_command,0.5,0.40)




        elif self.name == "pause_canvas":
            #self.focus_set()
            #self.boss = False


            self.label_pause_game = Label(self, text = 'Game Paused')
            self.label_pause_game.place(relx=0.4, rely=0.1)

            unPause_game_command = lambda: self.start_game(pause_canvas, main_canvas)
            self.switch_canvas_button("Continue", unPause_game_command, 0.5, 0.5)

            back_to_menu_command = lambda: restart_program(True)
            self.switch_canvas_button("Menu", back_to_menu_command, 0.5, 0.55)

        elif self.name == "leaderboard_canvas":
            pass
        elif self.name == "tutorial_canvas":
            self.bg=bg
            self.tutorial_txt = "1. Move using arrow keys!\n2. Pause with space!\n3. Avoid the monsters!\n4. Jumping is fun\n5. Every time you survive yellow block, you get a point\n6. T - cheat for passing left wall\n7. J - cheat for jumping higher"

            self.label = Label(self, text = "My tutorial", bg = self.bg )
            self.label.config(font=("Courier", 24))
            self.label.place(relx=0.5, rely=0.2, anchor = 'center',)

            self.label2 = Label(self, text = self.tutorial_txt, bg = self.bg )
            self.label2.config(font=("Courier", 16))
            self.label2.place(relx=0.5, rely=0.4, anchor = 'center',)

            back_to_menu_command = lambda: self.switch_canvas(tutorial_canvas, menu_canvas)
            self.switch_canvas_button("Back",back_to_menu_command,0.1,0.05)
        elif self.name == "boss_key_canvas":
            self.bossImage = self.create_image(width/2, height/2, image = bossKeyImage)

    def bossKey(self):
        global boss_key_on
        if(not boss_key_on):
            self.switch_canvas(main_canvas, boss_key_canvas)
            boss_key_on = True
        else:
            print(main_canvas.focus_get())
            self.switch_canvas(boss_key_canvas, main_canvas)
            moveMan()
            boss_key_on = False

    def leaderboard():
        pass




    def switch_canvas_button(self, text, command, relx, rely):
        self.button = Button(self, text = text, width = 15, height = 1, command = command)
        self.button.place(relx=relx, rely=rely, anchor = 'center')
        self.button.config(font=("Courier", 18))


    def start_game(self, canvas_to_hide, canvas_to_show):
        canvas_to_hide.pack_forget()
        canvas_to_show.pack()
        canvas_to_show.focus_set()
        moveMan()


    def switch_canvas(self, canvas_to_hide, canvas_to_show):
        print("Old canvas")
        print(canvas_to_hide.focus_get())
        canvas_to_hide.pack_forget()
        canvas_to_show.pack()
        canvas_to_show.focus_set()
        print("New canvas")
        print(canvas_to_show.focus_get())


    def pause_game(self, canvas_to_hide):
        canvas_to_hide.pack_forget()
        pause_canvas.pack()
        pause_canvas.focus_set()



    def create_floor(self):
        self.create_rectangle(0,height - 160,width,height,fill = "#3F688C")


    def create_man(self):
        self.man = self.create_image(self.manWidth*3, height-self.manWidth*6, image = manStanding)

    def un_bind_keys(self):
        self.unbind("<Left>")
        self.unbind("<Right>")
        self.unbind("<Up>")
        self.unbind("<Escape>")

    def bind_keys(self):
        self.bind("<Left>", self.leftKey)
        self.bind("<Right>", self.rightKey)
        self.bind("<Up>", self.upKey)
        self.bind("<Escape>", lambda e: self.pause_game(main_canvas))
        self.bind("<space>", lambda e: self.pause_game(main_canvas))
        self.bind("b", lambda e: self.bossKey())
        self.bind("t", lambda e: self.teleportButton())
        self.bind("j", lambda e: self.highJumpButton())

    def highJumpButton(self):
        if self.highJump:
            self.highJump = False
        else:
            self.highJump = True

    def teleportButton(self):
        if self.teleport:
            self.teleport = False
        else:
            self.teleport = True

    def leftKey(self, event):
        self.positions = self.coords(self.man)
        self.moveX = self.positions[0]-20
        self.direction = "left"


    def rightKey(self, event):
        self.positions = self.coords(self.man)
        self.moveX = self.positions[0]+20
        self.direction = "right"


    def upKey(self, event):#THIS KEY SHOULD ALLOW YOU TO JUMP FROM TOP TO ANY PLATFORM IN THE GAME
        self.positions = self.coords(self.man)
        self.comeBackPositionY = self.positions[1]
        self.moveY = self.positions[1] - self.jumpDistance
        self.isJumping = True
        self.airStop = False


    def label_score(self):
        txt = "Score: " + str(self.score)#SCORETEXT = SOMETHING
        self.scoreLabel = Label(self, text = txt, bg = self.bg)
        self.scoreLabel.config(font=("Courier", 44))
        self.scoreLabel.place(relx=0.01, rely=0.1)


    def updateImage(self):

        if self.direction == "right":
            if self.image1 > 5:
                self.itemconfig(self.man,image = manRunning2)
                self.image1 += 1
            else:
                self.itemconfig(self.man,image = manRunning1)
                self.image1 +=1
        elif self.direction == "left":
            if self.image1 > 5:
                self.itemconfig(self.man,image = manRunning2)
                self.image1 += 1
            else:
                self.itemconfig(self.man,image = manRunning1)
                self.image1 +=1
        if self.isJumping:
            self.itemconfig(self.man, image = manJumping)

        if self.image1 == 10:
            self.image1 = 0

    def collision(self, manPosition, platformPosition):
        if manPosition[0]+self.manWidth >= platformPosition[0] and manPosition[0] <= platformPosition[2] and manPosition[1]+self.manHeight >= platformPosition[1] and manPosition[1] <= platformPosition[3]:
            return True
        return False




class Platforms:

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.start_coordinates = [x1,y1,x2,y2]

    def show_platform(self, first):
        if first:
            self.platform = main_canvas.create_rectangle(self.start_coordinates[0],self.start_coordinates[1],self.start_coordinates[2],self.start_coordinates[3], fill="yellow")
        else:
            self.platform = main_canvas.create_rectangle(self.start_coordinates[0],self.start_coordinates[1],self.start_coordinates[2],self.start_coordinates[3], fill="red")

    def move(self, speed, is1):
        platformGap = random.randint(100, 800)
        platformSize = random.randint(-20, 0)
        main_canvas.move(self.platform, -speed, 0)
        self.coordiantes = main_canvas.coords(self.platform)

        if(self.coordiantes[2] < 0):
            main_canvas.coords(self.platform, self.start_coordinates[0]+platformGap,self.start_coordinates[1]+platformSize,self.start_coordinates[2]+platformGap,self.start_coordinates[3])
            if is1:
                main_canvas.score+=1
                if main_canvas.score == 1:
                    main_canvas.speed +=5
                    main_canvas.velocity +=5
                elif main_canvas.score ==3:
                    main_canvas.speed +=5
                elif main_canvas.score ==5:
                    main_canvas.speed +=5
                    main_canvas.velocity +=10
                elif main_canvas.score ==10:
                    main_canvas.speed +=5

width = 0
height = 0
boss_key_on = False

window = setWindowDimensions()
manRunning1 = PhotoImage(file = "manRunning1.png")
manRunning2 = PhotoImage(file = "manRunning2.png")
manStanding = PhotoImage(file = "spaceManStanding.png")
manJumping = PhotoImage(file = "manJumping.png")
bossKeyImage = PhotoImage(file = "bossKeyImage.png")

#NEED TO RANDOMISE THE DISTANCE AT WHICH THEY SPAWN AND THEN COLLISION FOR 2ND PLATFORM
#THEN SAVES, LEADERBOARD, ETC
main_canvas = My_canvas(window, width, height, '#B6F2E1', 'main_canvas')
platform1 = Platforms(width-40, height-180, width, height-120)
platform1.show_platform(True)
platform2 = Platforms(width + 600, height-180, width+640, height-120)
platform2.show_platform(False)
platform3 = Platforms(width + 660, height-180, width+700, height-120)
platform3.show_platform(False)
pause_canvas = My_canvas(window, width, height, '#B6F2E1', 'pause_canvas')
boss_key_canvas = My_canvas(window, width, height, '#B6F2E1', 'boss_key_canvas')
tutorial_canvas = My_canvas(window, width, height, '#B6F2E1', 'tutorial_canvas')
leaderboard_canvas = My_canvas(window, width, height, '#B6F2E1', 'leaderboard_canvas')
menu_canvas = My_canvas(window, width, height, '#B6F2E1', 'menu_canvas')
menu_canvas.pack()

window.mainloop()
