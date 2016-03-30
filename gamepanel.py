import time
import math
import tkinter
from tkinter import *
from threading import Timer
from maze import *


class Application(Frame):
    """
    GUI, implement fcuntion from maze.py to generate maze
    """

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(expand=True, fill=BOTH)
        self.master = master
        self.maze = Maze(40, 40) # maze object
        self.createWindow() # create gui window
        self.initCvs()
        self.initButton()
        self.show_icon = False


    def createWindow(self):
        """
        Set windows size, and central it
        :return:
        """
        sw = self.master.winfo_screenwidth() # screen width
        sh = self.master.winfo_screenheight() # screen height

        self.h = sh - 100
        self.w = self.h

        self.block_size = int((self.h - 40) / (max(self.maze.row_size, self.maze.col_size)))
        self.hero_x = self.maze.start_p[0]
        self.hero_y = self.maze.start_p[1]
        self.hero_id = 0

        self.master.title("Maze") # title number
        # central
        x = (sw - self.w) / 2
        y = (sh - self.h) / 2
        # width * length + x-cord + y-cord
        self.master.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))


    def initButton(self):
        self.bottomFrame = Frame(self, borderwidth=2, relief="groove")

        self.bottomFrame.pack(side=BOTTOM, expand=FALSE, fill=BOTH)

        # col size, label, allow user to customize
        Label(self.bottomFrame, text="col size:").pack(side=LEFT, pady=3, expand=True)
        # default value, unless user specific at GUI
        self.row_num = IntVar(value=40)
        self.row_num._default = 40

        size = Entry(self.bottomFrame, textvariable=self.row_num, width=6)
        size.tk_focusNext()
        size.pack(side=LEFT, pady=3, expand=True)


        # row size, label, allow user to customize
        Label(self.bottomFrame, text="row size:").pack(side=LEFT, pady=3, expand=True)
        # default value, unless user specific at GUI
        self.col_num = IntVar(value=40)
        self.col_num._default = 40

        size = Entry(self.bottomFrame, textvariable=self.col_num, width=6)
        size.pack(side=LEFT, pady=3, expand=True)

        # user can config how long with the icon path last for
        Label(self.bottomFrame, text="icon show time:").pack(side=LEFT, pady=3, expand=True)
        # default value, unless user speicif
        self.icon_time = IntVar(value=8)
        self.icon_time._default = 8

        size = Entry(self.bottomFrame, textvariable=self.icon_time, width=6)
        size.pack(side=LEFT, pady=3, expand=True)
        # 'New Game' and 'Quit Game' buttom
        newGameButton = Button(self.bottomFrame, text="New Game",
                               command=self.handler.on_new_game)
        newGameButton.pack(side=LEFT, pady=3, expand=True)

        quitGameButton = Button(self.bottomFrame, text="Quit Game",
                                command=self.handler.on_quit_game)
        quitGameButton.pack(side=LEFT, pady=3, expand=True)

    def initCvs(self):
        # create top frame, main canvane, and control event
        self.topFrame = Frame(self, background="green")
        self.mainCvs = Canvas(self.topFrame)
        self.handler = Handler(self)
        self.mainCvs.bind('<Up>', self.handler.move) # press 'UP'
        self.mainCvs.bind('<Down>', self.handler.move) # press 'DOWN'
        self.mainCvs.bind('<Left>', self.handler.move) # press 'LEFT'
        self.mainCvs.bind('<Right>', self.handler.move) # press 'RIGHT'
        self.mainCvs.bind('<Button-1>', self.handler.onclick)
        self.mainCvs.pack(expand=True, fill=BOTH)
        self.topFrame.pack(fill=BOTH, expand=True, side=TOP)


    def light_block(self, i, j):
        """
        determine what area shoule be blocked to player
        """
        # only within two blocks is avaiable to player
        if math.fabs(self.hero_y - j) > 2 or math.fabs(self.hero_x - i) > 2:
            return False
        # hero is avaibale
        if (i, j) == (self.hero_x, self.hero_y):
            return True
        # 对某点上下左右四个方向判断,如果四个方向有一个是英雄的位置 是 白
        # 否则,在对这个各个方向的 各个点进行相同判断

        # if some point can be reach within 2 blocks, visualable
        for a in range(4):
            (npx, npy) = self.maze.get_arround(i, j, a, 1)
            if npx:
                if self.maze.maze_map[npx][npy] == 1:
                    continue
                if (npx, npy) == (self.hero_x, self.hero_y):
                    return True
                for b in range(4):
                    (nnpx, nnpy) = self.maze.get_arround(npx, npy, b, 1)
                    if nnpx:
                        if self.maze.maze_map[nnpx][nnpy] == 1:
                            continue
                        if nnpx and (nnpx, nnpy) == (self.hero_x, self.hero_y):
                            return True


    # draw the whole map from maze_map
    def init_blocks(self):
        self.color_map = {}
        self.maze.display()
        for i in range(self.maze.row_size):
            for j in range(self.maze.col_size):
                type = self.maze.maze_map[i][j]
                # '0' - represnt path or interesection
                if type == 0:
                    self.color_map[(i, j)] = self.draw_block(i, j, "gray")
                # '1' - represent wall
                if type == 1:
                    self.color_map[(i, j)] = self.draw_block(i, j, "black")
        # drwa player
        self.draw_hero()
        # draw exit
        self.draw_block(self.maze.end_p[0], self.maze.end_p[1], "green")
        # draw bonue - coin path
        self.award_id = ''
        self.draw_award()


    def draw_hero(self):
        """
        when player position changes, redraw canvas
        """
        # remove coin path
        self.mainCvs.delete("coin")
        # delete prev_player
        self.mainCvs.delete(self.hero_id)
        # draw player
        self.hero_id = self.mainCvs.create_rectangle((self.hero_x + (1 / 4)) * self.block_size,
                                                     (self.hero_y + (1 / 4)) * self.block_size,
                                                     (self.hero_x + (3 / 4)) * self.block_size,
                                                     (self.hero_y + (3 / 4)) * self.block_size,
                                                     fill="blue", outline="blue")

        # check every position, you may comment out this part
        # you may this part, then the whole map is visuable
        for i in range(self.maze.row_size):
            for j in range(self.maze.col_size):
                id = self.color_map.get((i, j))
                type = self.maze.maze_map[i][j]
                if self.light_block(i, j):
                    # yes!!
                    if type == 0 and self.mainCvs.itemcget(id, "fill") != "gray":
                        self.mainCvs.itemconfigure(id, fill="gray", outline="gray")
                    # draw coin
                    elif type == 7 and self.show_icon:
                        c_id = self.draw_coin(i, j, "gold")
                        self.mainCvs.itemconfigure(c_id, tags="coin")
                        self.mainCvs.itemconfigure(id, fill="gray", outline="gray")
                else:
                    if type == 7 and self.show_icon:
                        c_id = self.draw_coin(i, j, "gold")
                        self.mainCvs.itemconfigure(c_id, tags="coin")
                    elif self.mainCvs.itemcget(id, "fill") != "black":
                        self.mainCvs.itemconfigure(id, fill="black", outline="black")


    def draw_coin(self, i, j, color):
        """
        at coordinate(i, j), draw coin(circle)
        """
        return self.mainCvs.create_oval((i + (1 / 4)) * self.block_size,
                                        (j + (1 / 4)) * self.block_size,
                                        (i + (3 / 4)) * self.block_size,
                                        (j + (3 / 4)) * self.block_size,
                                        fill=color, outline=color)


    def draw_block(self, i, j, color):
        """
        at coordinate(i, j), draw block with 'color'
        """
        return self.mainCvs.create_rectangle((i) * self.block_size, (j) * self.block_size,
                                             (i + 1) * self.block_size, (j + 1) * self.block_size,
                                             fill=color, outline=color)


    def draw_award(self):
        """
        draw a red block as bonus
        randomly generate one
        only one upon a time
        :return:
        """
        if self.award_id:
            self.mainCvs.delete(self.award_id)

        while True:
            self.award_p = self.maze.random_point(self.maze.row_size, self.maze.col_size)
            if self.maze.maze_map[self.award_p[0]][self.award_p[1]] == 0:
                break
        self.award_id = self.draw_block(*self.award_p, "red") # draw red block


    def set_show_icon(self, bool):
        """
        implement timer, determine when to get rid of 'coin path'
        """
        self.show_icon = bool
        if bool == False:
            for i in range(self.maze.row_size):
                for j in range(self.maze.col_size):
                    if self.maze.maze_map[i][j] == 7:
                        self.maze.maze_map[i][j] = 0
            self.draw_hero()


    def show_message(self, m):
        """
        popup message
        """
        import tkinter.messagebox
        # default messagebox
        tkinter.messagebox.showinfo(title="Note", message=m)


class Handler(object):
    """
    event handler
    """
    def __init__(self, app):
        self.app = app
        self.maze = app.maze
        self.mainCvs = app.mainCvs

    def onclick(self, event):
        """
        handling
        click event
        """
        self.mainCvs.focus_force()

    def on_new_game(self):
        """
        create a new game
        """
        self.mainCvs.focus_force()
        self.mainCvs.delete('all')
        if self.app.show_icon == True:
            self.timer.cancel()
        if self.app.row_num.get() < 1 :
            self.app.row_num.__init__()
        if self.app.col_num.get() < 1 or self.app.col_num.get() > 40:
            self.app.col_num.__init__()
        self.app.hero_id = 0
        self.maze.__init__(self.app.row_num.get(), self.app.col_num.get())
        self.app.hero_x = self.maze.start_p[0]
        self.app.hero_y = self.maze.start_p[1]
        self.app.init_blocks() # start drawing block

    def on_quit_game(self): # when 'Quit Game'
        if self.app.show_icon == True:
            self.timer.cancel()
        self.app.master.quit() # quit

    def on_draw_path(self):
        """
        slove 'click'
        """
        self.app.show_message("not devlop") # not avaibale for now

    def move(self, event):
        """
        handling keyboard
        """
        key_name = event.keysym
        cx = self.app.hero_x
        cy = self.app.hero_y
        if key_name == "Up": # UP
            cy = self.app.hero_y - 1
        if key_name == "Down": # DOWN
            cy = self.app.hero_y + 1
        if key_name == "Left": # LEFT
            cx = self.app.hero_x - 1
        if key_name == "Right": # RIGHT
            cx = self.app.hero_x + 1
        # when reach exit
        if (cx, cy) == self.maze.end_p:
            self.app.show_message("you win the game!")
            self.on_new_game()
        if self.maze.maze_map[cx][cy] == 0:
            # when player reach bonus - red block - coin path
            if (cx, cy) == self.app.award_p:
                self.maze.solve((cx, cy))
                # redraw bonus - red block
                self.app.draw_award()
                # set how long with it last for
                self.app.set_show_icon(True)
                self.timer = Timer(self.app.icon_time.get(), self.app.set_show_icon, (False,))
                self.timer.start()
            self.app.hero_x = cx
            self.app.hero_y = cy
            self.app.draw_hero()
        # if player lay on a coin
        if self.maze.maze_map[cx][cy] == 7:
            # get rid of that one
            self.maze.maze_map[cx][cy] = 0

            self.app.hero_x = cx
            self.app.hero_y = cy
            self.app.draw_hero()

# main function, start GUI
if __name__ == "__main__":
    root = Tk()
    app = Application(master=root)
    app.mainloop()
