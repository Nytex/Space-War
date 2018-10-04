import os
import random
import time
import turtle
import winsound

turtle.speed(0)
turtle.bgcolor("black")
turtle.bgpic("background.gif")
turtle.title("Spacewar")
turtle.ht() #Hide the default turtle
turtle.setundobuffer(1)
turtle.tracer(4)
turtle.register_shape("ufo.gif")
turtle.register_shape("spaceship.gif")
turtle.register_shape("main.gif")



#Create the class for Sprite
class Sprite(turtle.Turtle):
      def __init__(self, spriteshape, color, startx, starty):
            turtle.Turtle.__init__(self, shape = spriteshape)
            self.speed(0)
            self.penup()
            self.color(color)
            self.fd(0)
            self.goto(startx, starty)
            self.speed = 1

      def move(self):
            self.fd(self.speed)

            #Boundary Detection
            if self.xcor() >290:
                  self.setx(290)
                  self.rt(60)

            if self.xcor() < -290:
                  self.setx(-290)
                  self.rt(60)

            if self.ycor() > 290:
                  self.sety(290)
                  self.rt(60)

            if self.ycor () < -290:
                  self.sety(-290)
                  self.rt(60)
                  
      def is_collision(self, other):
            if(self.xcor() >= (other.xcor() -20)) and \
            (self.xcor() <= (other.xcor() + 20)) and \
            (self.ycor() >= (other.ycor() - 20)) and \
            (self.ycor() <= (other.ycor() + 20)):
                  return True
            else:
                  return False

      
                             


#Create a special Class for Player
class Player(Sprite):
      def __init__(self, spriteshape, color, startx, starty):
            Sprite.__init__(self, spriteshape, color, startx, starty)
            self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None)
            self.speed = 4
            self.lives = 3
            
      def turn_left(self):
            self.lt(45)

      def turn_right(self):
            self.rt(45)

      def accelerate(self):
            self.speed += 1
            if self.speed > 7:
                  self.speed = 7
                  
      def decelerate(self):
            self.speed -= 1
            if self.speed < -1:
                  self.speed = -1

class Enemy(Sprite):
      def __init__(self, spriteshape, color, startx, starty):
            Sprite.__init__(self, spriteshape, color, startx, starty)
            self.speed = 6
            self.setheading(random.randint(0 , 360))

class Ally(Sprite):
      def __init__(self, spriteshape, color, startx, starty):
            Sprite.__init__(self, spriteshape, color, startx, starty)
            self.speed = 8
            self.setheading(random.randint(0 , 360))

      def move(self):
            self.fd(self.speed)

            #Boundary Detection special for Ally(Opposite of Normal)
            
            if self.xcor() >290:
                  self.setx(290)
                  self.lt(60)

            if self.xcor() < -290:
                  self.setx(-290)
                  self.lt(60)

            if self.ycor() > 290:
                  self.sety(290)
                  self.lt(60)

            if self.ycor () < -290:
                  self.sety(-290)
                  self.lt(60)

#Class for Missile
class Missile(Sprite):
      def __init__(self, spriteshape, color, startx, starty):
            Sprite.__init__(self, spriteshape, color, startx, starty)
            self.shapesize(stretch_wid=0.3, stretch_len=0.4, outline=None)
            self.speed = 25
            self.status = "ready"
            self.goto(-1000, 1000)

      def fire(self):
            if self.status == "ready":
                  self.goto(player.xcor(), player.ycor())
                  self.setheading(player.heading())
                  self.status = "firing"
                  winsound.PlaySound("laser",winsound.SND_ASYNC)

      def move(self):
            
            if self.status == "firing":
                  self.fd(self.speed)

            #Border Check for Bullet
            if self.xcor() < -290 or self.xcor() > 290 or self.ycor() < -290 or self.ycor() > 290:
                  self.goto(-1000, 1000)
                  self.status = "ready"


class Particle(Sprite):
      def __init__(self, spriteshape, color, startx, starty):
            Sprite.__init__(self, spriteshape, color, startx, starty)
            self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
            self.goto(-1000,-1000)
            self.frame = 0

      def explode(self, startx, starty):
            self.goto(startx, starty)
            self.setheading(random.randint(0,360))
            self.frame = 1

      def move(self):
            self.fd(10)
                  
            #if self.frame < 15:
             #     self.frame = 0
              #    self.goto(-1000,-1000)


#Create Class for the game
class Game():
      def __init__(self):
            self.level = 1
            self.score = 0
            self.state = "playing"
            self.pen = turtle.Turtle()
            self.lives = 3

      def draw_border(self):
            self.pen.speed(0)
            self.pen.color("white")
            self.pen.pensize(3)
            self.pen.penup()
            self.pen.goto(-300, 300)
            self.pen.pendown()
            for side in range(4):
                  self.pen.fd(600)
                  self.pen.rt(90)
            self.pen.penup()
            self.pen.ht()
            self.pen.penup()

      def show_status(self):
            self.pen.undo()
            msg = "Score: %s" %(self.score)
            self.pen.penup()
            self.pen.goto(-300, 310)
            self.pen.write(msg, font=("Arial", 16, "normal"))


#Game Object      
game = Game()

#Draw the game border
game.draw_border()

#Show the State
game.show_status()

#Sprite
player = Player("main.gif","black", 0 , 0)
#enemy = Enemy("circle", "red" , -100 , 0)
missile = Missile("triangle", "yellow", 0, 0)
#ally = Ally("square", "blue",0, 0)

enemies = []
for i in range(6):
      enemies.append(Enemy("ufo.gif", "red" , -100 , 0))

allies = []
for i in range (4):
      allies.append(Ally("spaceship.gif", "blue",0, 0))

particles = []
for i in range(20):
      particles.append(Particle("circle", "orange", 0,0))

#Keyboard Binding
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right,"Right")
turtle.onkey(player.accelerate, "Up")
turtle.onkey(player.decelerate, "Down")
turtle.onkey(missile.fire, "space")
turtle.listen() #Link the Keyboard Binding


#Main game loop
while True:
      turtle.update()
      player.move()
      missile.move()
      
      for enemy in enemies:
            enemy.move()

            #Check for Collision
            if player.is_collision(enemy):
                  x = random.randint(-250, 250)
                  y = random.randint(-250, 250)
                  enemy.goto(x, y)
                  game.score -= 100
                  game.show_status()


#Collision Bullet and Enemy
            if missile.is_collision(enemy):
                  x = random.randint(-250, 250)
                  y = random.randint(-250, 250)
                  enemy.goto(x, y)
                  missile.status = "ready"
#Increase Score
                  game.score += 100
                  game.show_status()
                  winsound.PlaySound("break",winsound.SND_ASYNC)
                  for particle in particles:
                       particle.explode(missile.xcor(),missile.ycor())
                       
      for ally in allies:
            ally.move()
#Collision Bullet and Ally
            if missile.is_collision(ally):
                  x = random.randint(-250, 250)
                  y = random.randint(-250, 250)
                  ally.goto(x, y)
                  missile.status = "ready"
#Decrease Score
                  game.score -= 150
                  game.show_status()
                  for particle in particles:
                        particle.explode(missile.xcor(),missile.ycor())
                       
      for particle in particles:
            particle.move()



delay = raw_input("Press enter to finish. >")

