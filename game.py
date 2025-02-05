import os
import time
import random
import threading

try:
    import msvcrt  # Windows
except ImportError:
    import sys
    import termios
    import tty

    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# Define constants for game dimensions
WIDTH = 50
HEIGHT = 20

# Define the player's spaceship character
PLAYER_CHAR = ">"

# Define the game state variables
player_y = HEIGHT // 2
asteroids = []
game_over = False

# Function to initialize the game
def init_game():
    global player_y, asteroids, game_over
    player_y = HEIGHT // 2
    asteroids = []
    game_over = False

# Function to draw the game screen
def draw_game():
    os.system("cls" if os.name == "nt" else "clear")
    print("-" * (WIDTH + 2))
    for y in range(HEIGHT):
        row = "|"
        for x in range(WIDTH):
            if x == 0 or x == WIDTH - 1:
                row += "|"
            elif y == player_y and x == 1:
                row += PLAYER_CHAR
            elif (y, x) in asteroids:
                row += "*"
            else:
                row += " "
        row += "|"
        print(row)
    print("-" * (WIDTH + 2))

# Function to move the player's spaceship
def move_player(direction):
    global player_y
    if direction == "up":
        player_y = max(1, player_y - 1)
    elif direction == "down":
        player_y = min(HEIGHT - 2, player_y + 1)

# Function to generate asteroids
def generate_asteroids():
    global asteroids
    if random.randint(1, 10) == 1:
        asteroids.append((random.randint(1, HEIGHT - 2), WIDTH - 2))

# Function to update the game state
def update_game():
    global asteroids
    new_asteroids = []
    for asteroid in asteroids:
        if asteroid[1] > 1:
            new_asteroids.append((asteroid[0], asteroid[1] - 1))
    asteroids = new_asteroids

# Function to check for collisions
def check_collisions():
    global player_y, asteroids
    for asteroid in asteroids:
        if asteroid[0] == player_y and asteroid[1] == 1:
            return True
    return False

# Function to capture user input
def capture_input():
    global game_over
    while not game_over:
        if os.name == "nt":
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8')
                if key == 'w':
                    move_player("up")
                elif key == 's':
                    move_player("down")
        else:
            key = getch()
            if key == 'w':
                move_player("up")
            elif key == 's':
                move_player("down")

# Main game loop
def main():
    global game_over
    init_game()
    input_thread = threading.Thread(target=capture_input)
    input_thread.daemon = True
    input_thread.start()

    while not game_over:
        draw_game()
        generate_asteroids()
        update_game()
        if check_collisions():
            game_over = True
            print("Game Over!")
            break
        time.sleep(0.05)  # Reduced sleep time for smoother gameplay

# Run the game
if __name__ == "__main__":
    main()
