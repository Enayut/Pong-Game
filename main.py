import pygame

SCREEN_WIDTH,SCREEN_HEIGHT = 700,500
PADDLE_WIDTH,PADDLE_HEIGHT = 100,20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
BALL_RADIUS = 17.5
WIN = 5
pygame.font.init()
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
SCORE_FONT1 = pygame.font.SysFont("comicsans", 25)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("pong")



class Paddle:
    COLOR = WHITE
    VEL = 5
    def __init__(self,x,y,height,width):
        self.x = self.xo = x
        self.y = self.yo = y
        self.height = height
        self.width = width
    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))
    def move(self,up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL
    def reset(self):
        self.x = self.xo
        self.y = self.yo

class Ball:
    MAX_VEL = 5
    COLOR = WHITE
    def __init__(self,x,y,radius):
        self.x = self.x_original =x
        self.y = self.y_original =y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
        
    def draw(self,win):
        pygame.draw.circle(win,self.COLOR,(self.x,self.y),self.radius)
        
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    
    def reset(self):
        self.x = self.x_original;
        self.y = self.y_original;
        self.y_vel = 0;
        self.x_vel *= -1;

def fill(win):
    win.fill(BLACK)
    pygame.display.update()

def handle_paddle(keys,left_paddle,right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= SCREEN_HEIGHT:
        left_paddle.move(False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= SCREEN_HEIGHT:
        right_paddle.move(False)
        
def handle_collision(ball,left_paddle,right_paddle):
    if ball.y + ball.radius >= SCREEN_HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1 
        
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y<= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height/2)/ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1*y_vel
                
    else:
        if ball.y >= right_paddle.y and ball.y<= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *=-1
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height/2)/ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1*y_vel
                
def draw(win, paddles, ball,left_score,right_score):
    win.fill(BLACK)
    
    left_score_text = SCORE_FONT.render(f"{left_score}",1,WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}",1,WHITE)
    win.blit(left_score_text,(SCREEN_WIDTH//4-left_score_text.get_width()//2,20))
    win.blit(right_score_text,(SCREEN_WIDTH*3//4-right_score_text.get_width()//2,20))
    for paddle in paddles:
        paddle.draw(win)
        
    for i in range(10,SCREEN_HEIGHT, SCREEN_HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (SCREEN_WIDTH//2-5, i, 10, SCREEN_HEIGHT//20))
    ball.draw(screen)
    pygame.display.update()
    
    

def main():
    running = True
    clock = pygame.time.Clock()
    left_paddle = Paddle(5,SCREEN_HEIGHT//2-2*PADDLE_HEIGHT,PADDLE_WIDTH,PADDLE_HEIGHT)
    right_paddle = Paddle(SCREEN_WIDTH-25,SCREEN_HEIGHT//2-2*PADDLE_HEIGHT,PADDLE_WIDTH,PADDLE_HEIGHT)
    ball = Ball(SCREEN_WIDTH//2,SCREEN_HEIGHT//2,BALL_RADIUS)
    right_score = 0
    left_score = 0
    
    while running:
        clock.tick(FPS)
        draw(screen,[left_paddle, right_paddle],ball,left_score,right_score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                break
            
        keys = pygame.key.get_pressed()
        handle_paddle(keys,left_paddle,right_paddle)
        
        ball.move()
        handle_collision(ball,left_paddle,right_paddle)
        
        if ball.x < 0:
            right_score += 1
            left_paddle.reset()
            right_paddle.reset()
            ball.reset()
        elif ball.x > SCREEN_WIDTH:
            left_score += 1
            left_paddle.reset()
            right_paddle.reset()
            ball.reset()
            
        won = False
        if left_score>= WIN:
            won = True
            win_text = "Left player won"
        elif right_score >= WIN:
            won = True
            win_text = "Right player won"
            
        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            text1 = SCORE_FONT1.render("Press Space to Continue", 1, WHITE)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
            screen.blit(text1, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2+100))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        main()
            
if __name__ == "__main__":
    main()