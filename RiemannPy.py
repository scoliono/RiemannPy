'''
RiemannPy
Copyright (c) 2019  James Shiffer
AP Computer Science Principles: Create Task
'''

import turtle, math, enum

INTERVALS = 100
ORIGIN = (-314, 0)
SCALE = 100
HEIGHT = 500
WIDTH = 500

grapher = turtle.Turtle()
status = turtle.Turtle()
sum_text = turtle.Turtle()
axes = turtle.Turtle()

screen = grapher.getscreen()
screen.screensize(WIDTH, HEIGHT)
screen.title('Riemann Sum Calculator')

grapher.penup()
grapher.speed(0)
grapher.hideturtle()
grapher.goto(ORIGIN)

status.penup()
status.hideturtle()
status.goto(WIDTH/2 - 50, -1 * HEIGHT/2 + 5)

axes.hideturtle()
axes.penup()
sum_text.hideturtle()
sum_text.penup()

'''
Draws the x- and y-axes on the coordinate plane.
'''
def draw_axes():
	# Draw lines
	grapher.goto(ORIGIN[0], HEIGHT)
	grapher.pendown()
	grapher.goto(ORIGIN[0], -1 * HEIGHT)
	grapher.penup()
	grapher.goto(WIDTH, ORIGIN[1])
	grapher.pendown()
	grapher.goto(-1 * WIDTH, ORIGIN[1])
	grapher.penup()

	grapher.goto(ORIGIN)

	# Draw markers along both axes
	for x in range(0, math.ceil(WIDTH/SCALE) + 1):
		axes.goto(ORIGIN[0] + x*SCALE, ORIGIN[1] - 5)
		axes.write(str(x))

	for y in range(1, math.ceil(HEIGHT/SCALE) + 1):
		axes.goto(ORIGIN[0] - 5, ORIGIN[1] + y*SCALE)
		axes.write(str(y))

	grapher.goto(ORIGIN)

'''
Draws the sine wave with a given amplitude and period (in radians).
'''
def draw_sin(amplitude=1, period=math.pi * 2):
	grapher.pendown()
	for x in [i * period/INTERVALS for i in range(INTERVALS + 1)]:
		status.clear()
		pos = grapher.pos()
		y = amplitude * math.sin(x * (math.pi * 2 / period))
		status.write('({0:.2f}, {1:.2f})'.format(x, y))
		grapher.goto(SCALE * x + ORIGIN[0], SCALE * y + ORIGIN[1])
	grapher.penup()
	grapher.goto(ORIGIN)

'''
Draws a rectangle with corner at (x, y) to scale with a given width and height.
Positive width means left corner, negative means right corner.
Positive height means bottom corner, negative means top corner.
'''
def draw_rect(x, y, w, h):
	grapher.goto(x*SCALE + ORIGIN[0], y*SCALE + ORIGIN[1])
	grapher.pendown()
	grapher.goto(x*SCALE + ORIGIN[0], (y+h)*SCALE + ORIGIN[1])
	grapher.goto((x+w)*SCALE + ORIGIN[0], (y+h)*SCALE + ORIGIN[1])
	grapher.goto((x+w)*SCALE + ORIGIN[0], y*SCALE + ORIGIN[1])
	grapher.goto(x*SCALE + ORIGIN[0], y*SCALE + ORIGIN[1])
	grapher.penup()
	
'''
Enum representing the various methods for taking a Riemann sum: from the left,
the right, using the Midpoint Rule, or using the Trapezoidal Rule.
'''
class SumMethods(enum.Enum):
	LEFT = 0
	MIDPOINT = 1
	RIGHT = 2
	TRAPEZOID = 3

'''
Draws the rectangles representing the Riemann sum.
'''
def draw_riemann_sum(subintervals, method=SumMethods.LEFT, color='black'):
	grapher.goto(ORIGIN)
	old_color = grapher.pencolor()
	grapher.pencolor(color)
	for x in [i * math.pi*2/subintervals for i in range(subintervals + 1)]:
		draw_rect(x, 0, math.pi*2/subintervals, math.sin(x)) #todo use amplitude+period
	grapher.pencolor(old_color)


# Start
if __name__ == '__main__':
	draw_axes()
	draw_sin()
	draw_riemann_sum(10)
	turtle.done()
