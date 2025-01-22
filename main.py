import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# High scores file
HIGH_SCORES_FILE = "high_scores.txt"

def load_high_scores():
    try:
        with open(HIGH_SCORES_FILE, "r") as file:
            scores = [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        scores = []
    return sorted(scores, reverse=True)[:5]

def save_high_score(score):
    scores = load_high_scores()
    scores.append(score)
    scores = sorted(scores, reverse=True)[:5]
    with open(HIGH_SCORES_FILE, "w") as file:
        for s in scores:
            file.write(f"{s}\n")

class Dinosaur:
    def __init__(self):
        self.width = 40
        self.height = 60
        self.x = 50
        self.y = SCREEN_HEIGHT - self.height - 20
        self.velocity = 0
        self.jump = False
        self.descend = False

    def handle_input(self, keys):
        if keys[pygame.K_UP] and not self.jump:
            self.jump = True
            self.velocity = -12  # Adjusted jump velocity for game balance

        if keys[pygame.K_DOWN]:
            self.y += 40  # Faster descent when pressing down
            self.y = min(self.y, SCREEN_HEIGHT - self.height - 20)

        if self.jump:
            self.y += self.velocity
            self.velocity += 0.5  # Gravity effect
            if self.y >= SCREEN_HEIGHT - self.height - 20:
                self.y = SCREEN_HEIGHT - self.height - 20
                self.jump = False

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))

class Obstacle:
    def __init__(self):
        self.width = random.choice([20, 30])
        self.height = random.randint(30, 60)
        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT - self.height - 20
        self.speed = 5
        self.color = random.choice([RED, BLUE, GREEN])
        self.passed = False

    def move(self):
        self.x -= self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def is_off_screen(self):
        return self.x + self.width < 0

class MovingObstacle(Obstacle):
    def __init__(self):
        super().__init__()
        self.direction = random.choice([-1, 1])  # Direction of vertical movement
        self.y = SCREEN_HEIGHT // 2  # Start in the middle of the screen

    def move(self):
        super().move()
        self.y += self.direction * 2  # Move up or down
        if self.y < 50 or self.y > SCREEN_HEIGHT - self.height - 50:
            self.direction *= -1  # Reverse direction if hitting bounds

    def draw(self):
        pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.height))

class MultiPartObstacle:
    def __init__(self):
        self.parts = []
        for _ in range(random.randint(2, 4)):
            width = random.randint(20, 30)
            height = random.randint(30, 50)
            part_x = SCREEN_WIDTH + random.randint(0, 100)
            part_y = SCREEN_HEIGHT - height - 20
            self.parts.append(pygame.Rect(part_x, part_y, width, height))
        self.speed = 5
        self.color = random.choice([RED, BLUE, GREEN])
        self.passed = False

    def move(self):
        for part in self.parts:
            part.x -= self.speed

    def draw(self):
        for part in self.parts:
            pygame.draw.rect(screen, self.color, part)

    def is_off_screen(self):
        return all(part.x + part.width < 0 for part in self.parts)

    @property
    def x(self):
        return min(part.x for part in self.parts)

    @property
    def width(self):
        return sum(part.width for part in self.parts)

class FlyingObstacle(Obstacle):
    def __init__(self):
        super().__init__()
        self.y = random.randint(50, SCREEN_HEIGHT // 2)  # Starts in the air

    def draw(self):
        pygame.draw.polygon(screen, self.color, [
            (self.x, self.y),
            (self.x + self.width // 2, self.y - self.height),
            (self.x + self.width, self.y)
        ])

class Game:
    def __init__(self):
        self.dino = Dinosaur()
        self.obstacles = []
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.speed_increment = 5

    def show_instructions(self):
        screen.fill(WHITE)
        font = pygame.font.Font(None, 36)
        instructions = [
            "Press UP to jump.",
            "Press DOWN to descend quickly.",
            "Avoid obstacles!",
            "Press any key to start."
        ]
        for i, line in enumerate(instructions):
            text = font.render(line, True, BLACK)
            screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50 + i * 30))
        pygame.display.flip()

        # Wait for user to press a key
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False

    def show_game_over(self):
        screen.fill(WHITE)
        font = pygame.font.Font(None, 36)
        game_over_text = font.render("Game Over!", True, BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 50))

        high_scores = load_high_scores()
        high_scores_text = ["High Scores:"] + [str(score) for score in high_scores]

        for i, line in enumerate(high_scores_text):
            text = font.render(line, True, BLACK)
            screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + i * 30))

        pygame.display.flip()

        # Wait for user to press a key
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False

    def create_obstacle(self):
        obstacle_type = random.choice([Obstacle, MovingObstacle, MultiPartObstacle, FlyingObstacle])
        obstacle = obstacle_type()
        obstacle.speed += self.speed_increment  # Adjust speed based on score
        self.obstacles.append(obstacle)

    def check_collision(self):
        for obstacle in self.obstacles:
            if isinstance(obstacle, MultiPartObstacle):
                for part in obstacle.parts:
                    if pygame.Rect(self.dino.x, self.dino.y, self.dino.width, self.dino.height).colliderect(part):
                        return True
            elif pygame.Rect(self.dino.x, self.dino.y, self.dino.width, self.dino.height).colliderect(
                pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)
            ):
                return True
        return False

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 10))

    def game_loop(self):
        self.show_instructions()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Handle input
            keys = pygame.key.get_pressed()
            self.dino.handle_input(keys)

            # Update obstacles
            if len(self.obstacles) < 2 or (self.obstacles and self.obstacles[-1].x < SCREEN_WIDTH // 2):
                self.create_obstacle()

            for obstacle in self.obstacles:
                obstacle.move()
                if not obstacle.passed and obstacle.x + obstacle.width < self.dino.x:
                    self.score += 1
                    obstacle.passed = True

            # Remove off-screen obstacles
            self.obstacles = [ob for ob in self.obstacles if not ob.is_off_screen()]

            # Check collision
            if self.check_collision():
                save_high_score(self.score)
                self.show_game_over()
                self.running = False

            # Draw everything
            screen.fill(WHITE)
            self.dino.draw()
            for obstacle in self.obstacles:
                obstacle.draw()
            self.draw_score()

            # Update display
            pygame.display.flip()

            # Frame rate
            clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.game_loop()
