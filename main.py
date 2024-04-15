import tbapy
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time
import io

#import picamera

#defining the rgb-matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.parallel = 1
options.chain_length = 1
options.hardware_mapping = 'regular'
options.drop_privileges = False
options.brightness = 75
#options.disabled_rt_throttled = True
#options.pwm_lsb_nanoseconds = 50
#options.disable_hardware_pulsing = True
#draw = ImageDraw.Draw(image)

startTimer = time.time()
state = "showScores"

redLength = 32
blueLength = 32
sideLength = -3

switched = False

red = (140, 15, 25)
blue = (0, 117, 62)

#red = (255,0,0)
#blue = (0,255,0)

tba = tbapy.TBA("DTMnL4hL8CpDwSj65VEJWEy5q9nE1yNZbFQKL1rvMVo9fBZt1Vwo8Ui0vGnhRxPC")


team = "frc7211"
eventKey = "2024miwmi"
match = tba.team_matches(team, eventKey)

amountOfMatches = len(match[-1])

for x in range(amountOfMatches):
    lastMatch = x
    if match[x].alliances['red']['score'] == -1:
        lastMatch -= 1
        break

redScore = match[lastMatch].alliances['red']['score']
blueScore = match[lastMatch].alliances['blue']['score']
redRP = match[lastMatch].score_breakdown['red']['rp']
blueRP = match[lastMatch].score_breakdown['blue']['rp']

side = ""
for x in range(3): #check if red
    teams = match[lastMatch].alliances['red']['team_keys']
    if teams[x] == team:
        print('red!')
        side = "red"
for x in range(3): #check if blue
    teams = match[lastMatch].alliances['blue']['team_keys']
    if teams[x] == team:
        print('blue!')
        side = "blue"


redTeams = match[lastMatch].alliances['red']['team_keys']
blueTeams = match[lastMatch].alliances['blue']['team_keys']
print(team + " was on " + side + " side!")
print("red: " + str(match[lastMatch].alliances['red']['score'])   + " | blue: " +str(match[lastMatch].alliances['blue']['score']))
print("red rp: " + str(match[lastMatch].score_breakdown['red']['rp']) + " | blue rp: " + str(match[lastMatch].score_breakdown['blue']['rp']))
print("red teams: " + str(match[lastMatch].alliances['red']['team_keys'][0]))



matrix = RGBMatrix(options=options)
image = Image.new("RGB", (64, 32))

draw = ImageDraw.Draw(image)

canvas = matrix.CreateFrameCanvas()

fnt = ImageFont.truetype('fonts/7x11.ttf')
fnt5x3 = ImageFont.truetype('fonts/5x3.ttf', 6)

def draw_text(xy, text, font, color, align = "left"):
    w = 0
    h = 0
    if align == "center":
        w, h = font.getsize(text)
    if align == "right":
        w, h = font.getsize(text)  
        w = w*2
        h = h*2     
    draw.text(((xy[0] -w/2)+1, ((xy[1] - h/2))+1), text, font = font, fill = (0,0,0))
    draw.text(((xy[0] -w/2), ((xy[1] - h/2))), text, font = font, fill = color)

def lerp(a, b, w):
    return a + w*(b-a)


def getTeam(alliance):
    side = 'blue'
    for x in range(3): #check if red
        teams = alliance['red']['team_keys']
        if teams[x] == team:
            #print('red!')
            side = "red"
    for x in range(3): #check if blue
        teams = alliance['blue']['team_keys']
        if teams[x] == team:
            #print('blue!')
            side = "blue"
    return side



def matchesWePlay(teamNum):
    
    mat = tba.match(eventKey, )

switched = False
matchesSlide = 0
#draw.rectangle()
while True:
    currentTime = time.time()
    elapsedTime = currentTime - startTimer

    if(elapsedTime > 7):
        if((state == "showScores") and (switched == False)):
            state = "showMain"#"showMain"
            switched = True
        if((state == "showMain") and (switched == False)):
            state = "showMatches"    
            switched = True   
        print(state)
        elapsedTime = 0
        startTimer = time.time()
        switched = False

    if state == "showMain":
        if(side == "red"):
            redLength = lerp(redLength, 65, 0.05)
            blueLength = lerp(blueLength, -25, 0.05)
        if(side == "blue"):
            redLength = lerp(redLength, -25, 0.05)
            blueLength = lerp(blueLength, 67, 0.05)
        sideLength = lerp(sideLength, -2, 0.05)
    if state == "showScores":
        redLength = lerp(redLength, 32, 0.05)
        blueLength = lerp(blueLength, 32, 0.05)
        sideLength = lerp(sideLength, -2, 0.05)
    if state == "showMatches":
        sideLength = lerp(sideLength, 33, 0.15)


    draw.rectangle((0,0, 64, 32), fill = (255, 255, 255))

    draw.rectangle((-1,-1, redLength,32), fill = red, outline = (255, 255, 255))
    draw.rectangle((64-blueLength,32, 65,-1), fill = blue, outline = (255, 255, 255))
    
    draw.rectangle((40,33, 64, -sideLength+32), fill = red, outline = (255,255,255))



    #drawing the match stuff
    for ox in range(amountOfMatches):
        x = ox
        side = getTeam(match[x].alliances)
        string = str(match[x].alliances[side]['score'])
        mn = str(match[x]['match_number'])

        if(len(mn) == 1):
            mn = "0" + mn

        string = mn + ":" + string

        
        if(side == 'red'):
            color = red
        else:
            color = blue
        draw.rectangle((41, 4+(7*x)+(-sideLength+32)+matchesSlide, 64, (7*x)+10+(-sideLength+32)+matchesSlide), fill = color)
        draw_text((42,0+(7*x)+(-sideLength+32)+matchesSlide), str(string),fnt5x3, (255,255,255), align = "left")
    
    


    if(state == "showMatches"):
        matchesSlide -= 0.2
        #print(abs(matchesSlide))
        #print(abs(matchesSlide)*amountOfMatches*8)
        if(amountOfMatches*8 < abs(matchesSlide)):
            state = "showScores"
            elapsedTime = 0
            startTimer = time.time()
    if(state == "showScores"):
        matchesSlide = lerp(matchesSlide, 0, 0.15)

    draw_text((redLength-64+1, -5+1), str(redTeams[0]).replace("frc", ""), fnt5x3, (255,255,255), align = "left")
    draw_text((redLength-64+1, -5+7+1), str(redTeams[1]).replace("frc", ""), fnt5x3, (255,255,255), align = "left")
    draw_text((redLength-64+1, -5+14+1), str(redTeams[2]).replace("frc", ""), fnt5x3, (255,255,255), align = "left")

    draw_text((blueLength-64+1, -5+1), str(blueTeams[0]).replace("frc", ""), fnt5x3, (255,255,255), align = "left")
    draw_text((blueLength-64+1, -5+1+7), str(blueTeams[1]).replace("frc", ""), fnt5x3, (255,255,255), align = "left")
    draw_text((blueLength-64+1, -5+1+14), str(blueTeams[2]).replace("frc", ""), fnt5x3, (255,255,255), align = "left")
    #draw scores
    draw_text((redLength/2, 12), str(redScore), fnt, (255,255,255), align = "center")
    draw_text((64-blueLength/2, 12), str(blueScore), fnt, (255,255,255), align = "center")

    #draw rp
    draw_text((redLength/2, 20), "RP: " + str(redRP), fnt5x3, (255,255,255), align = "center")
    draw_text((64-blueLength/2, 20), "RP: " + str(blueRP), fnt5x3, (255,255,255), align = "center")

    #draw side
    if(side == "red"):
        draw_text((redLength/2, 1), "US", fnt5x3, (255,255,255), align = "center")
    else:
        draw_text((64-blueLength/2, 1), "US", fnt5x3, (255,255,255), align = "center")


    #stream = io.BytesIO()
    #with picamera.PiCamera() as camera:
    #    camera.start_preview()
    #    camera.capture(stream, format = "jpeg")
#
    #stream.seek(0)
    


    #matrix.SetImage(img)

    matrix.SetImage(image)
    time.sleep(0.05)
    #canvas = matrix.SwapOnVSync(canvas)
    

   

