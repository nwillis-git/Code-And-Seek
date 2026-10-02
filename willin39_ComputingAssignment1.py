## Imports
import turtle
import time
import random
import math

## Constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 450
WINDOW_TITLE = "Code and Seek"

## Initialize the turtle library window
turtle.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
screen = turtle.Screen()
screen.title(WINDOW_TITLE)

t = turtle.Turtle()
t.hideturtle()
screen.tracer(0)

## Initialize global variables
bestGuess = 0
scoreTotal = 0
distanceTotal = 0

## Setup Functions
# The splash screen to be displayed at the start of the game
def splashScreen():
    screen.bgcolor("#E0B758")
    t.up()
    t.goto(0,50)
    t.write("Code and Seek!", align='center', font  =('Arial','36'))
    t.goto(0,-50)
    t.write("Rules: One player will chose a set of hidden co-ordinates, and the other will get 3 chances to guess them.", align='center', font=('Arial','12'))
    screen.update()

# Draws the desert scene
def drawScene():
    t.clear()
    t.color('black')
    # Ensure an even cactus distribution
    for x in range(SCREEN_WIDTH // -2 ,SCREEN_WIDTH // 2, random.randint(150,250)):         # Grid spacing is randomized but consistent
        for y in range(SCREEN_HEIGHT // -2, SCREEN_HEIGHT // 2, random.randint(150,250)):   # Nested loop for x and y allows for grid pattern
            drawCactus(x + random.randint(-70,70),y+random.randint(-30,30))                 # Random offset from grid looks scattered but even
    # Ensure an even rock distribution
    for x in range(SCREEN_WIDTH // -2,SCREEN_WIDTH // 2, random.randint(150,250)):
        for y in range(SCREEN_HEIGHT // -2, SCREEN_HEIGHT // 2, random.randint(150,250)):
            drawRock(x + random.randint(-70,70),y+random.randint(-30,30))
    screen.update()

# Draw a rock with turtle
def drawRock(x,y):
    rockSize = random.uniform(1.0,3.0)
    t.up()
    t.goto(x,y)
    t.setheading(0)
    t.down()
    t.fillcolor('gray')
    t.begin_fill()
    t.fd(33 * rockSize)
    t.left(106.8)
    t.fd(23 * rockSize)
    t.left(73.2)
    t.fd(16 * rockSize)
    t.left(65.3)
    t.fd(24 * rockSize)
    t.left(114.7)
    t.end_fill()

# Draw a cactus with turtle
def drawCactus(x,y):
    cactusSize = random.uniform(0.7,1.3)
    t.up()
    t.goto(x,y)
    t.setheading(0)
    t.down()
    t.fillcolor('green')
    t.begin_fill()
    t.fd(15 * cactusSize)
    t.left(90)
    t.fd(30 * cactusSize)
    t.right(90)
    t.fd(20 * cactusSize)
    t.left(90)
    t.fd(30 * cactusSize)
    t.left(90)
    t.fd(10 * cactusSize)
    t.left(90)
    t.fd(20 * cactusSize)
    t.right(90)
    t.fd(10 * cactusSize)
    t.right(90)
    t.fd(40 * cactusSize)
    t.left(90)
    t.fd(15 * cactusSize)
    t.left(90)
    t.fd(50 * cactusSize)
    t.right(90)
    t.fd(10 * cactusSize)
    t.right(90)
    t.fd(20 * cactusSize)
    t.left(90)
    t.fd(10 * cactusSize)
    t.left(90)
    t.fd(30 * cactusSize)
    t.left(90)
    t.fd(20 * cactusSize)
    t.right(90)
    t.fd(20 * cactusSize)
    t.left(90)
    t.end_fill()

## Game logic functions
# Gets the hider's hidden position
def getHiderPos():
    x = screen.numinput("Hider", "Hider, pick an x-coordinate", minval=-SCREEN_WIDTH // 2, maxval=SCREEN_WIDTH // 2)
    y = screen.numinput("Hider", "Hider, pick a y-coordinate", minval=-SCREEN_HEIGHT // 2, maxval=SCREEN_HEIGHT // 2)
    return x,y

# Gets a guess and calculates distance + score
def guessAndCheck(hiderPos):
    global bestGuess, scoreTotal, distanceTotal
    guessX = screen.numinput("Seeker", "Seeker, pick an x-coordinate", minval=-SCREEN_WIDTH // 2, maxval=SCREEN_WIDTH // 2)
    guessY = screen.numinput("Seeker", "Seeker, pick a y-coordinate", minval=-SCREEN_HEIGHT // 2, maxval=SCREEN_HEIGHT // 2)

    distanceToHider = math.sqrt(math.fabs(hiderPos[0] - guessX) ** 2 + math.fabs(hiderPos[1] - guessY) ** 2)    # Pythagorean theorem
    score = scoreAlgorithm(distanceToHider)

    # Update globals
    bestGuess = max(score, bestGuess)
    scoreTotal += score
    distanceTotal += distanceToHider

    return distanceToHider, score, guessX, guessY

# Calculate the score based on distance, scales relative to screen size (200 - distance is the "default" used for a 900x450 window)
def scoreAlgorithm(distance):
    return max(0, (2 * SCREEN_WIDTH / 9) - distance) ** 2 / ((2 * SCREEN_WIDTH / 9) ** 2 / 10)

# Draw a circle to represent the guess, with the distance and score
def drawGuess(distanceToHider, score, guessX, guessY):
    t.fillcolor('red')
    t.up()
    t.goto(guessX, guessY - 5)          # Offset from point by radius of circle
    t.down()
    t.begin_fill()
    t.circle(10)
    t.end_fill()
    t.up()
    t.goto(guessX + 15, guessY + 5)
    t.write(f"Score: {score:.2f}")      # Round score and distance to 2 decimals for display
    t.goto(guessX + 15, guessY - 10)
    t.write(f"Distance: {distanceToHider:.2f}")

# Reveal the hider's location to the seeker
def revealLocation(x, y):
    t.fillcolor('limegreen')
    t.up()
    t.goto(x, y - 5)
    t.down()
    t.begin_fill()
    t.circle(10)
    t.end_fill()
    t.up()
    t.goto(x, y - 20)
    t.write(f"Location: {x}, {y}", align='center')

def endScreen():
    global bestGuess, scoreTotal, distanceTotal
    t.clear()
    screen.tracer(0)
    t.up()
    t.goto(0,75)
    t.write("GAME OVER!", align='center', font=('Arial', '24'))
    t.goto(0,25)
    t.write(f"Total Score: {scoreTotal:.2f}", align='center', font=('Arial', 12))
    t.goto(0,-25)
    t.write(f"Best Guess: {bestGuess:.2f}", align='center', font=('Arial', 12))
    t.goto(0,-75)
    t.write(f"Total Distance: {distanceTotal:.2f}", align='center', font=('Arial', 12))


## Function calls (Running the game)
splashScreen()  # Title and rules
time.sleep(3)   # Let players read
drawScene()     # Draw the decor

hiderPos = getHiderPos()    # Get the secret location
screen.tracer(1)            # Let the user see the circles appear

for i in range(4):                                                      # Seeker gets 4 guesses
    guessInfo = guessAndCheck(hiderPos)                                 # Guess and compare to hider location
    drawGuess(guessInfo[0], guessInfo[1], guessInfo[2], guessInfo[3])   # Show the results to the user
    #time.sleep(3)                                                       # Admire results

revealLocation(hiderPos[0], hiderPos[1])    # Game over, reveal location
time.sleep(3)                               # Let players see before going to end screen

endScreen()

screen.exitonclick()