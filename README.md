# Pixel Runner

A fun and optimized dinosaur game built using Python and Pygame. Control the dinosaur, avoid obstacles, and aim for the highest score!

## Features

- **Dynamic Gameplay**: Jump over and avoid various types of obstacles.
- **Obstacle Types**:
  - Static obstacles.
  - Moving obstacles.
  - Multi-part obstacles.
  - Flying obstacles.
- **High Score Tracking**: Save and display your best scores.
- **Optimized Code**: Efficient game mechanics and collision detection.



## How to Play

- Press **UP** arrow to jump.
- Press **DOWN** arrow to descend quickly.
- Avoid hitting obstacles to keep the game going.
- Aim to beat your high score!


## Contributing

We welcome contributions to improve the game! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.


# Detailed Documentation of Functions

This document provides an in-depth explanation of all the functions and loops used in the Dino Game, including their purpose, implementation details, and behavior in various scenarios.

---

## 1. `load_high_scores()`

### **Description:**
This function reads high scores from a file (`high_scores.txt`) and returns them as a sorted list. If the file doesn't exist, it handles the error gracefully and returns an empty list.

### **Implementation Details:**
- **File Handling:**
  - Opens the file in read mode.
  - If the file doesn't exist, it raises a `FileNotFoundError` and returns an empty list.
- **Data Processing:**
  - Reads each line, converts it to an integer, and stores it in a list.
  - Sorts the list in descending order and limits it to the top 5 scores.

```python
try:
    with open(HIGH_SCORES_FILE, "r") as file:
        scores = [int(line.strip()) for line in file.readlines()]
except FileNotFoundError:
    scores = []
return sorted(scores, reverse=True)[:5]
```

### **Use Case:**
- Ensures that the game always has a list of high scores to display, even if the file is missing or corrupted.

---

## 2. `save_high_score(score)`

### **Description:**
Saves a new high score to the `high_scores.txt` file and ensures the list contains only the top 5 scores.

### **Implementation Details:**
- **Score Handling:**
  - Appends the new score to the existing list.
  - Sorts the list in descending order and retains the top 5.
- **File Handling:**
  - Opens the file in write mode and writes each score on a new line.

```python
scores = load_high_scores()
scores.append(score)
scores = sorted(scores, reverse=True)[:5]
with open(HIGH_SCORES_FILE, "w") as file:
    for s in scores:
        file.write(f"{s}\n")
```

### **Use Case:**
- Updates the high scores file whenever the player achieves a new score.

---

## 3. `Dinosaur` Class

### **Description:**
Represents the player's character in the game. The pixels can jump, descend quickly, and interact with obstacles.

### **Key Methods:**

#### a. `__init__()`
- **Initializes:**
  - Position: Starts near the bottom-left corner of the screen.
  - Size: Fixed width (40) and height (60).
  - Jumping State: Tracks whether the dinosaur is mid-jump.
  
```python
self.rect.x = 50
self.rect.y = SCREEN_HEIGHT - self.rect.height - 20
self.velocity = 0
self.jump = False
```

#### b. `update(keys)`
- **Handles Input:**
  - Checks for the `UP` arrow to initiate a jump.
  - Adjusts the dinosaur's vertical position based on velocity and gravity.
  - Resets the jump state when it lands.

```python
if keys[pygame.K_UP] and not self.jump:
    self.jump = True
    self.velocity = -12

if self.jump:
    self.rect.y += self.velocity
    self.velocity += 0.5
    if self.rect.y >= SCREEN_HEIGHT - self.rect.height - 20:
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 20
        self.jump = False
```

### **Use Case:**
- Provides the primary control mechanics for the player.

---

## 4. `Obstacle` Class

### **Description:**
Represents a basic obstacle that moves from right to left across the screen.

### **Key Methods:**

#### a. `__init__()`
- **Initializes:**
  - Dimensions: Random width (20-40) and height (30-60).
  - Position: Starts off-screen to the right.

```python
self.rect.x = SCREEN_WIDTH
self.rect.y = SCREEN_HEIGHT - self.height - 20
```

#### b. `update()`
- Moves the obstacle leftward by reducing its `x` position.
- Deletes the obstacle if it moves off-screen.

```python
self.rect.x -= 5
if self.rect.right < 0:
    self.kill()
```

### **Use Case:**
- Creates dynamic challenges for the player to avoid.

---

## 5. `Game` Class

### **Description:**
The main class that manages the game loop, event handling, rendering, and collision detection.

### **Key Methods:**

#### a. `__init__()`
- Initializes:
  - The player's dinosaur.
  - Groups for all sprites and obstacles.
  - The game score and font.

#### b. `spawn_obstacle()`
- Spawns a new obstacle if necessary, ensuring consistent gameplay.

```python
if not self.obstacles or self.obstacles.sprites()[-1].rect.x < SCREEN_WIDTH // 2:
    obstacle = Obstacle()
    self.obstacles.add(obstacle)
    self.all_sprites.add(obstacle)
```

#### c. `draw_score()`
- Renders the player's current score on the screen.

```python
score_text = self.font.render(f"Score: {self.score}", True, BLACK)
screen.blit(score_text, (10, 10))
```

#### d. `game_loop()`
- The core game loop that:
  - Handles events (e.g., quitting the game).
  - Updates the player and obstacles.
  - Checks for collisions.
  - Draws all elements on the screen.

```python
while self.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.running = False

    keys = pygame.key.get_pressed()
    self.dino.update(keys)

    self.spawn_obstacle()
    self.all_sprites.update()

    if pygame.sprite.spritecollideany(self.dino, self.obstacles):
        save_high_score(self.score)
        self.running = False

    screen.fill(WHITE)
    self.all_sprites.draw(screen)
    self.draw_score()
    pygame.display.update()
    clock.tick(30)
```

### **Use Case:**
- Orchestrates all game functionality, ensuring smooth gameplay.



## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Enjoy the game and happy coding! If you encounter any issues, feel free to open an issue or contribute with suggestions.
