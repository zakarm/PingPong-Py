import pygame
import sys

class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 200
        self.speed = 15

    def move_up(self):
        if self.y > 60:
            self.y -= self.speed

    def move_down(self):
        if self.y < 435:
            self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))

class Ball:
    def __init__(self):
        self.radius = 10
        self.x = 550
        self.y = 350
        self.dx = 5
        self.dy = 5

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def check_collision(self):
        if self.y - self.radius < 50 or self.y + self.radius > 650:
            self.dy *= -1
        if self.x - self.radius < 50 or self.x + self.radius > 1050:
            self.dx *= -1

    def check_paddle_collision(self, paddleA, paddleB):
        if self.x - self.radius <= paddleA.x + paddleA.width and paddleA.y <= self.y <= paddleA.y + paddleA.height:
            self.dx *= -1
        if self.x + self.radius >= paddleB.x and paddleB.y <= self.y <= paddleB.y + paddleB.height:
            self.dx *= -1

    def check_score(self):
        if self.x <= 60:
            return "B"
        elif self.x >= 1020:
            return "A"
        return None

    def reset(self):
        self.x = 550
        self.y = 350
        self.dx *= -1
        self.dy *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, (139,0,0), (self.x, self.y), self.radius)

class PingPong:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption("Ping Pong")
        self.clock = pygame.time.Clock()
        self.paddleA = Paddle(100, 250)
        self.paddleB = Paddle(960, 250)
        self.ball = Ball()
        self.scoreA = 0
        self.scoreB = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.paddleA.move_up()
        if keys[pygame.K_s]:
            self.paddleA.move_down()
        if keys[pygame.K_UP]:
            self.paddleB.move_up()
        if keys[pygame.K_DOWN]:
            self.paddleB.move_down()

        self.ball.move()
        self.ball.check_collision()
        self.ball.check_paddle_collision(self.paddleA, self.paddleB)
        score = self.ball.check_score()
        if score == "A":
            self.scoreA += 1
            self.ball.reset()
        elif score == "B":
            self.scoreB += 1
            self.ball.reset()

    def draw(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), ((50, 50), (1000, 600)), 3)
        pygame.draw.line(self.screen, (255, 255, 255), (550, 50), (550, 650), 3)
        pygame.draw.circle(self.screen, (255, 255, 255), (550, 350), 100, 2)
        pygame.draw.circle(self.screen, (255, 255, 255), (550, 350), 3)
        self.paddleA.draw(self.screen)
        self.paddleB.draw(self.screen)
        self.ball.draw(self.screen)
        font = pygame.font.SysFont(None, 48)
        score_text = f"{self.scoreA} - {self.scoreB}"
        text = font.render(score_text, True, (255, 255, 255))
        self.screen.blit(text, (500, 20))

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = PingPong()
    game.run()
