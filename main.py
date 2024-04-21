import sys

from sprites import *


class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        # Set up the game window
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption('Kill The Goblins')
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font('./Arial.ttf', 32)

        # Load spritesheets and images
        self.character_spritesheet = Spritesheet('img/character.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')
        self.enemy_spritesheet = Spritesheet('img/enemy.png')
        self.attack_spritesheet = Spritesheet('img/attack.png')
        self.intro_background = pygame.image.load('img/introbackground.png')
        self.go_background = pygame.image.load('img/gameover.png')

    def createTilemap(self):
        # Create the tilemap based on the tilemap data
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "E":
                    Enemy(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)

    def new(self):
        # Start a new game
        self.playing = True

        # Create sprite groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        # Create the tilemap
        self.createTilemap()

    def events(self):
        # Handle events in the game loop
        for event in pygame.event.get():
            # When you click the X
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Create an attack when spacebar is pressed
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)

    def update(self):
        # Update the game state
        self.all_sprites.update()

    def draw(self):
        # Draw the game on the screen
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)

        # Display player health
        health_text = self.font.render(f"Health: {self.player.health}", True, WHITE)
        self.screen.blit(health_text, (10, 10))  # Adjust position as needed

        pygame.display.flip()

    def main(self):
        # Main game loop
        while self.playing:
            self.events()
            self.update()
            self.check_win_condition()
            self.draw()

    def check_win_condition(self):
        # Checks to see if all enemy sprites are killed
        if len(self.enemies) == 0:
            # No longer playing and display game win screen
            self.playing = False
            self.game_win()
        # If player sprite gets killed
        elif not self.player.alive():
            # No longer playing and display game over screen
            self.player = False
            self.game_over()

    def game_win(self):
        # Display the game win screen
        text = self.font.render("You Win!", True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        restart_button = Button(10, WIN_HEIGHT - 120, 120, 50, WHITE, BLACK, 'Restart', 32)
        quit_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, 'Quit', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                # When you click the X
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            if quit_button.is_pressed(mouse_pos, mouse_pressed):
                self.running = False

            self.screen.fill((0, 0, 255))  # Fill the screen with BLUE
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.screen.blit(quit_button.image, quit_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def game_over(self):
        # Display the game over screen
        text = self.font.render('Game Over', True, WHITE)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        restart_button = Button(10, WIN_HEIGHT - 120, 120, 50, WHITE, BLACK, 'Restart', 32)
        quit_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, 'Quit', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                # When you click the X
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            if quit_button.is_pressed(mouse_pos, mouse_pressed):
                self.running = False

            self.screen.blit(self.go_background, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.screen.blit(quit_button.image, quit_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def intro_screen(self):
        # Display the intro screen
        intro = True

        title = self.font.render('Awesome Game', True, BLACK)
        title_rect = title.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        play_button = Button(10, WIN_HEIGHT - 120, 120, 50, WHITE, BLACK, 'Play', 32)
        quit_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, 'Quit', 32)

        while intro:
            for event in pygame.event.get():
                # When you click the X
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            # PLAY THE GAME!!!
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            # CLOSE THE GAME!!!
            if quit_button.is_pressed(mouse_pos, mouse_pressed):
                self.running = False

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(quit_button.image, quit_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


# Start the game
g = Game()
g.intro_screen()
g.new()

while g.running:
    g.main()
    g.check_win_condition()
    if not g.running:
        break

# Quit pygame and exit the program
pygame.quit()
sys.exit()
