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

XMIN = 0.0
XMAX = 5.0

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
status.goto(WIDTH/2 - 50, -1 * HEIGHT/2 + 15)

axes.hideturtle()
axes.penup()
sum_text.hideturtle()
sum_text.penup()
sum_text.goto(WIDTH/2 - 50, -1 * HEIGHT/2)

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
Computes the function to be graphed.
'''
def calc_func(x):
	return 1/(math.e**x)

'''
Sketches the function using a given number of intervals from Xmin to Xmax.
'''
def draw_func():
	grapher.goto(XMIN*SCALE + ORIGIN[0], calc_func(XMIN)*SCALE + ORIGIN[1])
	grapher.pendown()
	for x in [XMIN + i * (XMAX-XMIN)/INTERVALS for i in range(INTERVALS + 1)]:
		status.clear()
		pos = grapher.pos()
		y = calc_func(x)
		status.write('({0:.2f}, {1:.2f})'.format(x, y))
		grapher.goto(SCALE * x + ORIGIN[0], SCALE * y + ORIGIN[1])
	grapher.penup()
	grapher.goto(ORIGIN)

'''
Draws a trapezoid with bottom corner at (x, y).
Bottom left corner if w is positive, bottom right if negative.
Only called directly if using the Trapezoid Rule to calculate the Riemann sum.
'''
def draw_trapezoid(x, y, w, h1, h2):
	grapher.goto(x*SCALE + ORIGIN[0], y*SCALE + ORIGIN[1])
	grapher.pendown()
	grapher.goto(x*SCALE + ORIGIN[0], (y + h1)*SCALE + ORIGIN[1])
	grapher.goto((x + w)*SCALE + ORIGIN[0], (y + h2)*SCALE + ORIGIN[1])
	grapher.goto((x + w)*SCALE + ORIGIN[0], y*SCALE + ORIGIN[1])
	grapher.goto(x*SCALE + ORIGIN[0], y*SCALE + ORIGIN[1])
	grapher.penup()
	
'''
Draws a rectangle with corner at (x, y) to scale with a given width and height.
Positive width means left corner, negative means right corner.
Positive height means bottom corner, negative means top corner.
'''
def draw_rect(x, y, w, h):
	draw_trapezoid(x, y, w, y+h, y+h)

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
Draws and computes the area of a single rectangle/trapezoid with a certain width.
Used to find the Riemann sum.
'''
def calc_rect(method, x, dx):
	if method == SumMethods.LEFT:
		y = calc_func(x)
		draw_rect(x, 0, dx, y)
		return dx * y
	elif method == SumMethods.RIGHT:
		y = calc_func(x + dx)
		draw_rect(x + dx, 0, -dx, y)
		return dx * y
	elif method == SumMethods.MIDPOINT:
		y = calc_func(x + dx/2)
		draw_rect(x, 0, dx, y)
		return dx * y
	elif method == SumMethods.TRAPEZOID:
		y1 = calc_func(x)
		y2 = calc_func(x + dx)
		draw_trapezoid(x, 0, dx, y1, y2)
		if y2 > y1:
			return (dx * y1) + (0.5 * dx * (y2 - y1))
		else:
			return (dx * y2) + (0.5 * dx * (y1 - y2))
	return -1

'''
Draws the rectangles representing the Riemann sum. Returns the approximate total area.
'''
def draw_riemann_sum(subintervals, method=SumMethods.LEFT, color='black'):
	grapher.goto(ORIGIN)
	old_color = grapher.pencolor()
	grapher.pencolor(color)
	dx = (XMAX - XMIN) / subintervals
	total = 0
	for x in [XMIN + i * dx for i in range(subintervals)]:
		sum_text.clear()
		total += calc_rect(method, x, dx)
		sum_text.write('Sum: {0:.3f}...'.format(total))
	grapher.pencolor(old_color)
	# Show final sum
	sum_text.clear()
	sum_text.write('Sum: {0:.3f}'.format(total), font=('Arial', 16, 'normal'))


# Start
if __name__ == '__main__':
	draw_axes()
	draw_func()
	draw_riemann_sum(10, method=SumMethods.TRAPEZOID, color='red')
	turtle.done()
