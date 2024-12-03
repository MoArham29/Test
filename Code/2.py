import pygame
import sys
#added a comment 
# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dimension Shift")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GREEN = (50, 255, 50)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Player settings
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60
player_x, player_y = 50, HEIGHT - PLAYER_HEIGHT - 50
player_speed = 5
player_jump = 12
player_velocity_y = 0
gravity = 0.5
on_ground = False

# Dimensions
current_dimension = 1  # 1 = Bright, 2 = Dark
platforms_dim1 = [(100, 500, 200, 20), (400, 400, 200, 20), (700, 300, 80, 20)]
platforms_dim2 = [(50, 500, 150, 20), (300, 400, 250, 20), (600, 350, 100, 20)]
goal_position = (750, 250, 40, 40)

# Load assets
bg_dim1 = pygame.image.load("11.PNG")  # Replace with your image path
bg_dim2 = pygame.image.load("22.PNG")  # Replace with your image path
player_image = pygame.image.load("Char.PNG")  # Replace with your player sprite path
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

# Music
pygame.mixer.music.load("BGMusic.mp3")  # Replace with your music file path
pygame.mixer.music.play(-1)  # Loop the music
music_muted = False

# Functions
def draw_platforms(platforms):
    for platform in platforms:
        pygame.draw.rect(screen, BLUE, platform)

def draw_goal():
    pygame.draw.rect(screen, GREEN, goal_position)

def check_collision(player_rect, platforms):
    for platform in platforms:
        if player_rect.colliderect(platform):
            return platform
    return None

# Game loop
running = True
while running:
    # Draw background
    if current_dimension == 1:
        screen.blit(bg_dim1, (0, 0))
    else:
        screen.blit(bg_dim2, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Dimension shift
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            current_dimension = 1 if current_dimension == 2 else 2

        # Mute/unmute music
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            if music_muted:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()
            music_muted = not music_muted

    # Player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_SPACE] and on_ground:
        player_velocity_y = -player_jump
        on_ground = False

    # Apply gravity
    player_velocity_y += gravity
    player_y += player_velocity_y

    # Create player rect
    player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)

    # Get current platforms
    platforms = platforms_dim1 if current_dimension == 1 else platforms_dim2

    # Collision handling
    collision = check_collision(player_rect, platforms)
    if collision:
        if player_velocity_y > 0:  # Falling
            player_y = collision[1] - PLAYER_HEIGHT
            player_velocity_y = 0
            on_ground = True
    else:
        on_ground = False

    # Check goal
    goal_rect = pygame.Rect(goal_position)
    if player_rect.colliderect(goal_rect):
        print("You Win!")
        pygame.quit()
        sys.exit()

    # Keep player on screen
    if player_x < 0:
        player_x = 0
    if player_x + PLAYER_WIDTH > WIDTH:
        player_x = WIDTH - PLAYER_WIDTH
    if player_y > HEIGHT:
        player_y = HEIGHT - PLAYER_HEIGHT
        player_velocity_y = 0
        on_ground = True

    # Draw everything
    draw_platforms(platforms)
    draw_goal()
    screen.blit(player_image, (player_x, player_y))

    pygame.display.flip()
    clock.tick(FPS)
