import pygame
import random
import sys

# Function to initialize Pygame
def initialize_pygame():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('assets/background_music.mp3')  # Replace with your background music file
    pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
    pygame.mixer.music.play(-1)  # Play music in a loop

# Set up the display
def setup_display():
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Subway Surfer Animation")
    return screen

# Set up colors
background_color = (135, 206, 235)  # Sky blue background
ground_color = (139, 69, 19)  # Brown for ground
text_color = (255, 255, 255)  # White text

# Load images
def load_images():
    character_image = pygame.image.load('assets/character.png')  # Replace with your character image
    obstacle_image = pygame.image.load('assets/obstacle.png')  # Replace with your obstacle image
    coin_image = pygame.image.load('assets/coin.png')  # Replace with your coin image
    powerup_image = pygame.image.load('assets/powerup.png')  # Replace with your powerup image
    background_image = pygame.image.load('assets/background.png')  # Replace with your background image

    # Scale images
    character_image = pygame.transform.scale(character_image, (50, 50))
    obstacle_image = pygame.transform.scale(obstacle_image, (50, 50))
    coin_image = pygame.transform.scale(coin_image, (30, 30))
    powerup_image = pygame.transform.scale(powerup_image, (30, 30))
    background_image = pygame.transform.scale(background_image, (800, 600))

    return character_image, obstacle_image, coin_image, powerup_image, background_image

# Set up clock
def setup_clock():
    return pygame.time.Clock()

# Function to draw the character
def draw_character(screen, character_image, x, y):
    screen.blit(character_image, (x, y))

# Function to draw obstacles
def draw_obstacles(screen, obstacle_image, obstacles):
    for obstacle in obstacles:
        screen.blit(obstacle_image, (obstacle['x'], obstacle['y']))

# Function to draw coins
def draw_coins(screen, coin_image, coins):
    for coin in coins:
        screen.blit(coin_image, (coin['x'], coin['y']))

# Function to draw powerups
def draw_powerups(screen, powerup_image, powerups):
    for powerup in powerups:
        screen.blit(powerup_image, (powerup['x'], powerup['y']))

# Function to display score
def display_score(screen, font, score):
    score_surface = font.render(f'Score: {score}', True, text_color)
    screen.blit(score_surface, (10, 10))

# Function to handle jumping
def handle_jumping(character_y, jump_count, powerup_jump):
    if jump_count >= -10:
        neg = 1
        if jump_count < 0:
            neg = -1
        multiplier = 0.5 if not powerup_jump else 0.7  # Higher jump with power-up
        character_y -= (jump_count ** 2) * multiplier * neg
        jump_count -= 1
    else:
        jump_count = 10
        return character_y, jump_count, False  # Reset jump and powerup_jump after completion
    return character_y, jump_count, powerup_jump

# Main animation loop
def main():
    initialize_pygame()
    screen = setup_display()
    character_image, obstacle_image, coin_image, powerup_image, background_image = load_images()
    clock = setup_clock()

    # Font
    font = pygame.font.Font(None, 36)

    # Animation variables
    character_x = 100
    character_y = screen.get_height() - 145
    character_speed = 5
    jumping = False
    jump_count = 10
    powerup_jump = False  # True if power-up makes the next jump higher
    obstacles = []
    coins = []
    powerups = []
    obstacle_timer = 0
    coin_timer = 0
    powerup_timer = 0
    score = 0

    while True:
        screen.blit(background_image, (0, 0))  # Draw background
        pygame.draw.rect(screen, ground_color, (0, screen.get_height() - 100, screen.get_width(), 100))  # Draw ground

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle jumping
        if jumping:
            character_y, jump_count, powerup_jump = handle_jumping(character_y, jump_count, powerup_jump)
            if jump_count == 10:  # Jump finished
                jumping = False  # Reset jumping state after jump completion

        # Generate obstacles, coins, and powerups (more spread out)
        obstacle_timer += 1
        if obstacle_timer > 150:  # Adjusted for less frequent obstacles
            obstacle_x = random.randint(screen.get_width(), screen.get_width() + 100)
            obstacle_y = screen.get_height() - 143
            obstacles.append({'x': obstacle_x, 'y': obstacle_y})
            obstacle_timer = 0

        coin_timer += 1
        if coin_timer > 200:  # Less frequent coins
            coin_x = random.randint(screen.get_width(), screen.get_width() + 100)
            coin_y = screen.get_height() - 200
            coins.append({'x': coin_x, 'y': coin_y})
            coin_timer = 0

        powerup_timer += 1
        if powerup_timer > 400:  # Less frequent power-ups
            powerup_x = random.randint(screen.get_width(), screen.get_width() + 100)
            powerup_y = screen.get_height() - 200
            powerups.append({'x': powerup_x, 'y': powerup_y})
            powerup_timer = 0

        # Move and draw obstacles
        for obstacle in obstacles:
            obstacle['x'] -= character_speed  # Move left
            if obstacle['x'] < -50:
                obstacles.remove(obstacle)

            # Avoid obstacles by jumping
            if (character_x + 50 > obstacle['x'] > character_x - 50) and (character_y >= screen.get_height() - 150):
                if not jumping:  # Only jump if not already jumping
                    jumping = True

        # Move and draw coins
        for coin in coins:
            coin['x'] -= character_speed  # Move left
            if coin['x'] < -30:
                coins.remove(coin)

            # Collect coins by jumping if no obstacle is near
            if (character_x < coin['x'] < character_x + 50) and (character_y >= screen.get_height() - 200):
                if not jumping:  # Only jump if not already jumping
                    jumping = True
                    coins.remove(coin)
                    score += 1  # Increment score

        # Move and draw powerups
        for powerup in powerups:
            powerup['x'] -= character_speed  # Move left
            if powerup['x'] < -30:
                powerups.remove(powerup)

            # Collect powerups and trigger higher jump on the next jump
            if (character_x < powerup['x'] < character_x + 50) and (character_y >= screen.get_height() - 200):
                if not jumping:  # Only jump if not already jumping
                    jumping = True
                    powerup_jump = True  # Set power-up to boost next jump
                    powerups.remove(powerup)
                    score += 5  # Increment score with power-up

        # Draw all elements
        draw_character(screen, character_image, character_x, character_y)
        draw_obstacles(screen, obstacle_image, obstacles)
        draw_coins(screen, coin_image, coins)
        draw_powerups(screen, powerup_image, powerups)
        display_score(screen, font, score)

        pygame.display.flip()
        clock.tick(60)

# Only call main() when the script is executed directly
if __name__ == "__main__":
    main()
