import pygame
import sys
import random

# Initialize Pygame
pygame.init()

WIDTH, HEIGHT = 400, 600
BIRD_WIDTH, BIRD_HEIGHT = 50, 50
PIPE_WIDTH, PIPE_HEIGHT = 100, 300
PIPE_GAP = 200
GRAVITY = 0.5
FLAP_STRENGTH = 10
PIPE_SPEED = 5

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load assets
bird_image = pygame.image.load("bird.png")
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))

pipe_image = pygame.Surface((PIPE_WIDTH, PIPE_HEIGHT))
pipe_image.fill(GREEN)

# Bird properties
bird_x = 50
bird_y = HEIGHT // 2
bird_velocity = 0

# Pipe properties
pipes = []

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game over flag
game_over = False

def draw_bird(x, y):
    screen.blit(bird_image, (x, y))

def draw_pipes():
    for pipe in pipes:
        screen.blit(pipe_image, pipe)

def update_pipes():
    for pipe in pipes:
        pipe[0] -= PIPE_SPEED

    pipes[:] = [pipe for pipe in pipes if pipe[0] + PIPE_WIDTH > 0]

def generate_pipe():
    pipe_height = random.randint(100, 400)
    top_pipe = [WIDTH, 0, PIPE_WIDTH, pipe_height]
    bottom_pipe = [WIDTH, pipe_height + PIPE_GAP, PIPE_WIDTH, HEIGHT - pipe_height - PIPE_GAP]
    pipes.append(top_pipe)
    pipes.append(bottom_pipe)

def check_collision():
    for pipe in pipes:
        if bird_x + BIRD_WIDTH > pipe[0] and bird_x < pipe[0] + PIPE_WIDTH:
            if bird_y < pipe[1] or bird_y + BIRD_HEIGHT > pipe[1] + pipe[3]:
                return True
    if bird_y < 0 or bird_y + BIRD_HEIGHT > HEIGHT:
        return True
    return False

def main():
    global bird_y, bird_velocity, score, game_over

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird_velocity = -FLAP_STRENGTH

                if game_over and event.key == pygame.K_RETURN:
                    bird_y = HEIGHT // 2
                    bird_velocity = 0
                    pipes.clear()
                    score = 0
                    game_over = False

        if not game_over:
            bird_velocity += GRAVITY
            bird_y += bird_velocity

            if bird_y < 0:
                bird_y = 0

            if bird_y + BIRD_HEIGHT > HEIGHT:
                bird_y = HEIGHT - BIRD_HEIGHT

            update_pipes()

            if len(pipes) == 0 or pipes[-1][0] < WIDTH - 200:
                generate_pipe()

            if pipes and pipes[0][0] + PIPE_WIDTH < 0:
                pipes.pop(0)
                pipes.pop(0)
                score += 1

            if check_collision():
                game_over = True

        screen.fill(WHITE)
        draw_bird(bird_x, bird_y)
        draw_pipes()

        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render("Game Over. Press Enter to Play Again.", True, (255, 0, 0))
            screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 18))

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
