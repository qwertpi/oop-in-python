from turtle import Turtle
from numpy.random import normal

#most likely to return 2 but could theorticaly return any number (though the nearer the number is to 2 the more likely it is to be returned)
def random_step_size():
    #if negative returns 0
    #1 number from a norm dist with mean 2 and std dev of 4
    return max([0,round(float(normal(2,4,1)))])

#creating a Turtle object
rory = Turtle()
#modifying attributes/properites of the object
rory.color("blue")
rory.shape("turtle")
#calling some methods of the object
rory.penup()
rory.goto(-150, 50)
rory.pendown()

mark = Turtle()
mark.color("red")
mark.shape("turtle")
mark.penup()
mark.goto(-150, 0)
mark.pendown()

jeff = Turtle()
jeff.color("green")
jeff.shape("turtle")
jeff.penup()
jeff.goto(-150, -50)
jeff.pendown()

for step in range(0, 100):
    rory.forward(random_step_size())
    mark.forward(random_step_size())
    jeff.forward(random_step_size())
