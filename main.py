import pygame as py
import os

py.font.init()

WIDTH,HEIGHT = 800, 400
WINDOW = py.display.set_mode((WIDTH, HEIGHT))

GOAL_FONT = py.font.SysFont('comicsans', 40)
WINNER_FONT = py.font.SysFont('comicsans', 100)


FPS = 50
PLAYER_WIDTH, PLAYER_HEIGHT =  80, 80
BALL_WIDTH, BALL_HEIGHT = 30, 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)



RONALDO_HIT = py.USEREVENT + 1
MESSI_HIT = py.USEREVENT + 2

STADE_EMOJI = py.image.load(os.path.join('mini-game','stade.jpg'))
STADE = py.transform.scale(STADE_EMOJI, (WIDTH, HEIGHT))
RONALDO_EMOJI = py.image.load(os.path.join('mini-game','ronaldo.png'))
RONALDO = py.transform.scale(RONALDO_EMOJI,(PLAYER_WIDTH, PLAYER_HEIGHT))
MESSI_EMOJI = py.image.load(os.path.join('mini-game','messi.png'))
MESSI = py.transform.scale(MESSI_EMOJI, (PLAYER_WIDTH, PLAYER_HEIGHT))
BALL_EMOJI = py.image.load(os.path.join('mini-game','ballon.jpg'))
BALL = py.transform.scale(BALL_EMOJI,(BALL_WIDTH, BALL_HEIGHT))


def draw_window(ronaldo, messi, ronaldo_balls, messi_balls, messi_goals, ronaldo_goals):
    WINDOW.blit(STADE, (0,0))

    messi_goal_text = GOAL_FONT.render("goals:" + str(messi_goals),1, WHITE)
    ronaldo_goal_text = GOAL_FONT.render("goals:" + str(ronaldo_goals), 1, WHITE)

    WINDOW.blit(ronaldo_goal_text, (50,10))
    WINDOW.blit(messi_goal_text, (650, 10))
    WINDOW.blit(RONALDO, (ronaldo.x, ronaldo.y))
    WINDOW.blit(MESSI, (messi.x, messi.y))
    #WINDOW.blit(BALL, (ball.x, ball.y))
    for ball in ronaldo_balls:
        WINDOW.blit(BALL, (ball.x, ball.y))
    for ballon in messi_balls:
        WINDOW.blit(BALL, (ballon.x, ballon.y))
    py.display.update()

def handle_ronaldo(key_pressed, ronaldo):
    if key_pressed[py.K_a]:
        ronaldo.x -= 1
    if key_pressed[py.K_e]:
        ronaldo.x += 1
    if key_pressed[py.K_s]:
        ronaldo.y += 1
    if key_pressed[py.K_z]:
        ronaldo.y -= 1

def handle_messi(key_pressed, messi):
    if key_pressed[py.K_LEFT]:
        messi.x -= 1
    if key_pressed[py.K_RIGHT]:
        messi.x += 1
    if key_pressed[py.K_DOWN]:
        messi.y += 1
    if key_pressed[py.K_UP]:
        messi.y -= 1

def handle_balls(ronaldo_balls, messi_balls, ronaldo, messi):
    for bal in ronaldo_balls:
        bal.x += 5
        if messi.colliderect(bal):
            py.event.post(py.event.Event(RONALDO_HIT))
            ronaldo_balls.remove(bal)
        elif bal.x > WIDTH:
            ronaldo_balls.remove(bal)
    for balon in messi_balls:
        balon.x -= 5
        if ronaldo.colliderect(balon):
            py.event.post(py.event.Event(MESSI_HIT))
            messi_balls.remove(balon)
        elif balon.x < 0:
            messi_balls.remove(balon)



def main():

    ronaldo = py.Rect(100, 100, PLAYER_WIDTH, PLAYER_HEIGHT)
    messi = py.Rect(700, 100, PLAYER_WIDTH, PLAYER_HEIGHT)
    # ball = py.Rect(100 + PLAYER_WIDTH, 100 + PLAYER_HEIGHT//2, BALL_WIDTH, BALL_HEIGHT)

    ronaldo_balls = []
    messi_balls = []
    ronaldo_goals = 0
    messi_goals = 0
    clock = py.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
            if event.type == py.KEYDOWN:
                if event.key == py.K_LCTRL:
                    ronaldo_ball = py.Rect(ronaldo.x + PLAYER_WIDTH + 2, ronaldo.y + PLAYER_HEIGHT//2, BALL_WIDTH, BALL_HEIGHT)
                    ronaldo_balls.append(ronaldo_ball)
                if event.key == py.K_RCTRL:
                    messi_ball = py.Rect(messi.x - PLAYER_WIDTH, messi.y + PLAYER_HEIGHT//2, BALL_WIDTH, BALL_HEIGHT)
                    messi_balls.append(messi_ball)
            if event.type == MESSI_HIT:
                ronaldo_goals +=1
            if event.type == RONALDO_HIT:
                messi_goals += 1

        key_pressed = py.key.get_pressed()
        handle_ronaldo(key_pressed=key_pressed, ronaldo=ronaldo)
        handle_messi(key_pressed=key_pressed, messi=messi)
        handle_balls(ronaldo_balls, messi_balls, ronaldo, messi)
        draw_window(ronaldo, messi, ronaldo_balls, messi_balls, ronaldo_goals, messi_goals)
        
    py.quit()

if __name__ == "__main__":
    main()