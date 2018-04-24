from tkinter import *
from random import randrange

# consts
SCALE = 25
FPS = 60
DELAY = 250
VEL = SCALE
HEIGHT = 500
WIDTH = 500
###

class Food(object):
    def __init__(self,parent):
        self.parent = parent
        self.spawn()

    def respawn(self):
        self.parent.delete(self.rect)
        self.spawn()

    def spawn(self):
        self.x = randrange(0,WIDTH-SCALE,SCALE)
        self.y = randrange(0,HEIGHT-SCALE,SCALE)
        print(self.x)
        print(self.y)
        self.rect = self.parent.create_rectangle(self.x,self.y,self.x+SCALE,self.y+SCALE, fill='red')

class Snake(object):
    def __init__(self, parent):
        self.headx = 0
        self.heady = 0
        self.headvx = VEL
        self.headvy = 0
        self.head = parent.create_rectangle(self.headx, self.heady,self.headx+SCALE, self.heady+SCALE, fill='yellow')
        self.body = []        
        self.vel = []
        self.parent = parent
        parent.pack()

    def grow(self):
        x1 = self.headx - self.headvx
        x2 = self.headx - self.headvx + SCALE
        y1 = self.heady - self.headvy
        y2 = self.heady - self.headvy + SCALE

        segment = self.parent.create_rectangle(x1,y1,x2,y2, fill='green')
        self.body = [segment] + self.body
        self.vel.insert(0,[self.headvx, self.headvy])

    def move_head(self):
        self.parent.move(self.head, self.headvx, self.headvy)
        self.headx += self.headvx
        self.heady += self.headvy
    
    def move_body(self):
        for seg,vel in zip(self.body, self.vel):
            self.parent.move(seg, vel[0], vel[1])
        if len(self.body) > 0:
            self.vel.insert(0, [self.headvx, self.headvy])
            self.vel.pop()
    
    def change_direction(self, vx, vy):
        self.headvx = vx
        self.headvy = vy

    def die(self):
        pass

class Game(object):
    def __init__(self, root):
        self.root = root
        self.canvas = canvas
        self.root.bind("<KeyPress>", self.on_press)
        self.food = Food(canvas)
        self.snake = Snake(canvas)
        self.root.update()

    def advance(self):
        self.snake.move_head()
        if (self.snake.headx == self.food.x) and (self.snake.heady == self.food.y):
            print("food get!")
            self.snake.grow()
            self.food.respawn()
        else:
            self.snake.move_body()
        self.root.update()
        self.root.after(DELAY, self.advance)

    def on_press(self, event):
        delta = {
            "Right": (SCALE,0),
            "Left": (-SCALE, 0),
            "Up": (0,-SCALE),
            "Down": (0,SCALE)
        }
        direction = delta.get(event.keysym, None)
        self.snake.change_direction(direction[0], direction[1])


if __name__ == "__main__":
    root = Tk()
    canvas = Canvas(root, bg="black",height=HEIGHT, width=WIDTH)
    game = Game(root)
    root.after(DELAY, game.advance)
    canvas.pack()
    root.mainloop()
