import pygame
import textwrap3
import os
import sys
import random


class Game:

    # Set important variables and other stuff
    def __init__(self):
        # ================== INITIALIZE PYGAME ================== #
        pygame.init()
        pygame.mixer.init()
        # ================== IMPORTANT VARIABLES ================== #
        self.VERSION = "1.0.1"  # When the game is in working order, will be version 1
        self.W_WIDTH = 192  # 16 * 12 = 192
        self.W_HEIGHT = 192  # 16 * 12 = 192
        self.BKG = 0, 0, 0  # Background color
        self.running = True  # Should be set to True
        self.playing = False  # You start at the menu, not playing. When you press start, will be True
        self.CURSOR_SHOWN = True  # False hides the cursor when hovering over the window
        self.FLAGS = pygame.RESIZABLE | pygame.SCALED  # Makes the window resizable while always keeping its resolution
        self.hertz = 10  # 1 Hz = 1 FPS
        self.GAME_NAME = 'La révolte'
        self.current_level = '0'
        self.level = LevelIntro(self)
        # ================== CREATE THE SPRITES AND CAMERA ================== #
        self.p1 = Player(self, self.level.spawnpoint_x, self.level.spawnpoint_y)
        self.camera = Camera(self)  # Need to pass self, because RPG is only defined at the end
        self.main_menu = Menu(self)
        # ================== CREATE DIALOGS ================== #
        # Intro
        self.papineau1 = "Aujourd'hui, nous avons reçu les résolutions et ils ont tous refusé!"
        self.papineau2_1 = "Pour protester nous allons boycotter les produits anglais! Achetez des produits locaux et"
        self.papineau2_2 = "envoyez des pétitions."
        self.nelson1 = "Non! Citoyens, nous devons nous battre pour nos droits en tant que canadiens français!"
        self.adam1 = "Aux armes citoyens!"

        # ================== LOAD SYSTEM ASSETS ================== ########################################################################################
        self.endingCredits = pygame.image.load((os.path.join('Assets', 'credits.png')))  # Credits image
        self.splashScreen = pygame.image.load((os.path.join('Assets', 'splash.png')))  # Splash screen image
        self.icon = pygame.image.load((os.path.join('Assets', 'icon.png')))
        self.gameFontBody = pygame.font.Font((os.path.join('Assets', 'font.ttf')), 8)  # The primary font
        self.gameFontBody2 = pygame.font.Font((os.path.join('Assets', 'font.ttf')), 6)  # The primary font
        pygame.display.set_icon(self.icon)

        self.menu_bkg = pygame.image.load((os.path.join('Assets', 'splash.png')))  # The backgroung image for the menu
        self.jouer_button = []
        self.jouer_button.append(pygame.image.load(os.path.join('Assets', 'Menu', 'jouer1.png')))
        self.jouer_button.append(pygame.image.load(os.path.join('Assets', 'Menu', 'jouer2.png')))
        self.options_button = []
        self.options_button.append(pygame.image.load(os.path.join('Assets', 'Menu', 'options1.png')))
        self.options_button.append(pygame.image.load(os.path.join('Assets', 'Menu', 'options2.png')))
        self.credits_button = []
        self.credits_button.append(pygame.image.load(os.path.join('Assets', 'Menu', 'jouer1.png')))
        self.credits_button.append(pygame.image.load(os.path.join('Assets', 'Menu', 'jouer2.png')))
        pygame.mixer.music.load(os.path.join('Assets', 'Sounds', 'bgm.mp3'))
        pygame.mixer.music.play(-1)
        # ================== LOAD SOUNDS ================== #
        self.shoot_sound = pygame.mixer.Sound(os.path.join('Assets', 'Sounds', 'gunshot.mp3'))
        self.swoosh_sound = pygame.mixer.Sound(os.path.join('Assets', 'Sounds', 'swoosh.mp3'))
        self.axe_hit_sound = pygame.mixer.Sound(os.path.join('Assets', 'Sounds', 'axe_hit.mp3'))
        self.click_sound = pygame.mixer.Sound(os.path.join('Assets', 'Sounds', 'click.mp3'))  # When you miss with axe
        self.fail_sound = pygame.mixer.Sound(os.path.join('Assets', 'Sounds', 'error.mp3'))  # When you miss with axe
        self.death_anim = []
        self.death_anim.append(pygame.image.load(os.path.join('Assets', 'Death', 'death1.png')))
        self.death_anim.append(pygame.image.load(os.path.join('Assets', 'Death', 'death2.png')))
        self.death_anim.append(pygame.image.load(os.path.join('Assets', 'Death', 'death3.png')))
        self.death_anim.append(pygame.image.load(os.path.join('Assets', 'Death', 'death4.png')))
        self.index = 0
        self.txt1 = pygame.image.load(os.path.join('Assets', 'texte_st_charles.png'))
        self.txt2 = pygame.image.load(os.path.join('Assets', 'texte_st_eustache.png'))
        self.txt3 = pygame.image.load(os.path.join('Assets', 'victoire.png'))
        # ================== CREATE THE WINDOW ================== #
        self.screen = pygame.display.set_mode((self.W_WIDTH, self.W_HEIGHT), self.FLAGS)  # Creates the window
        pygame.display.set_caption(self.GAME_NAME, self.GAME_NAME)  # Whatever the hell an icontitle is...
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(self.CURSOR_SHOWN)
        # ==================== GUI =========================== #
        self.gui = False
        self.gui_type = False

    def npc_death(self, npc, x, y):
        npc.alive = False
        if npc.index >= len(self.death_anim):
            npc.index = 0
            if npc.npc_type == 'brit':
                self.level.ennemies.remove(npc)
        self.screen.blit(self.death_anim[npc.index], (x - self.camera.offset.x, y - self.camera.offset.y))
        npc.index += 1

    def player_death(self):
        self.p1.alive = False
        if self.p1.index >= len(self.death_anim):
            self.p1.index = 0
            for i in range(10):
                self.clock.tick(self.hertz)
                death_screen = pygame.Surface((self.W_WIDTH, self.W_HEIGHT))
                death_screen.set_alpha(128)
                death_screen.fill((0, 0, 0))
                death_text = self.gameFontBody.render('Vous êtes mort.', True, (255, 255, 255))
                self.screen.blit(death_screen, (0, 0))
                self.screen.blit(death_text, (self.W_HEIGHT / 2 - death_text.get_rect().width / 2,
                                              self.W_HEIGHT / 2 - death_text.get_rect().height / 2))
                death_text2 = self.gameFontBody2.render('Veuillez redémarrer le jeu pour recommencer.', True,
                                                        (255, 255, 255))
                self.screen.blit(death_text2, (self.W_HEIGHT / 2 - death_text2.get_rect().width / 2,
                                               self.W_HEIGHT / 2 - death_text2.get_rect().height / 2 + 10))

                pygame.display.update()
            while True:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:

                    self.running = False
                    self.playing = False
                    pygame.quit()
                    sys.exit("Quitting")
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        self.playing = False
                        pygame.quit()
                        sys.exit("Quitting")

            # self.playing = False
        self.screen.blit(self.death_anim[self.p1.index],
                         (self.p1.x - self.camera.offset.x, self.p1.y - self.camera.offset.y))
        self.p1.index += 1

    def text_box(self, title, text, first=True, box_color=(255, 255, 255),
                 text_color=(0, 0, 0), charperline=27):

        self.click_sound.play()
        if first:
            transparent_bkg = pygame.Surface((self.W_WIDTH, self.W_HEIGHT))
            transparent_bkg.set_alpha(128)
            transparent_bkg.fill((0, 0, 0))
            self.screen.blit(transparent_bkg, (0, 0))
        pygame.draw.rect(self.screen, box_color, pygame.Rect(0, 123, self.W_WIDTH, 69))
        text.split()
        wrappedtext = textwrap3.wrap(text, charperline)
        title_text = self.gameFontBody.render(title, True, text_color)
        self.screen.blit(title_text, (3, 126))
        if 0 < len(wrappedtext):  # Checks if this index exists
            line_1_text = self.gameFontBody.render(wrappedtext[0], True, text_color)  # Creates the text object
            self.screen.blit(line_1_text, (3, 139))  # Displays the text object
        if 1 < len(wrappedtext):
            line_2_text = self.gameFontBody.render(wrappedtext[1], True, text_color)
            self.screen.blit(line_2_text, (3, 152))
        if 2 < len(wrappedtext):
            line_3_text = self.gameFontBody.render(wrappedtext[2], True, text_color)
            self.screen.blit(line_3_text, (3, 165))
        if 3 < len(wrappedtext):
            line_4_text = self.gameFontBody.render(wrappedtext[3], True, text_color)
            self.screen.blit(line_4_text, (3, 178))

        pygame.display.update()
        pygame.event.clear()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                pygame.quit()
                sys.exit("Quitting")

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    break

    def window_diagnostics(self, shown=False):  # Show developer-relevant info on the toolbar
        if shown:
            pygame.display.set_caption(self.GAME_NAME + " /// " + self.VERSION + " /// " + str(self.clock))
        else:
            pygame.display.set_caption(self.GAME_NAME)

    # def create_obstacles(self):
    #     # Examples, these are the borders
    #     self.obstacles.append(self.new_obstacle(-1, -1, self.level.MAP_WIDTH + 2, 1))
    #     self.obstacles.append(self.new_obstacle(-1, self.level.MAP_HEIGHT + 1, self.level.MAP_WIDTH + 2, 1))
    #     self.obstacles.append(self.new_obstacle(self.level.MAP_WIDTH + 1, -1, 1, self.level.MAP_HEIGHT + 2))
    #     self.obstacles.append(self.new_obstacle(-1, -1, 1, self.level.MAP_HEIGHT + 2))
    #
    # def new_obstacle(self, x, y, w, h):
    #     return pygame.Rect(x, y, w, h)

    def main_loop(self):
        while self.running:
            if self.running and not self.playing:  # Menu loop
                self.clock.tick(self.hertz)
                # Menu
                self.window_diagnostics(True)
                self.main_menu.main()
                pygame.display.update()

            if self.running and self.playing:  # Main game loop
                self.clock.tick(self.hertz)
                # Main code here
                if int(random.random() * 200) == 1:
                    RPG.p1.bois += 1
                    # print('bois += 1')
                if self.gui_type != 'dialog':
                    self.screen.fill(self.BKG)
                    self.screen.blit(self.level.image, (0 - self.camera.offset.x, 0 - self.camera.offset.y))
                self.window_diagnostics(True)  # Should be False when released
                # To change for in level.animate() (except player)
                if not self.gui:
                    self.level.animate()
                    self.p1.animate()
                else:
                    self.gui.animate()

                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print(pygame.mouse.get_pos())

                    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                        self.click_sound.play()
                        self.gui = False
                        self.gui_type = False

                self.camera.scroll()
                pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.gui == False:
                        self.playing = False
                    elif event.key == pygame.K_c:  # DEV TOOL FOR OBSTACLES
                        print("(" + str(self.p1.x) + ", " + str(self.p1.y) + ")" + " - " + "(" + str(
                            self.p1.x + self.p1.width) + ", " + str(self.p1.y) + ")")
                        print("(" + str(self.p1.x) + ", " + str(self.p1.y + self.p1.height) + ")" + " - " + "(" + str(
                            self.p1.x + self.p1.width) + ", " + str(self.p1.y + self.p1.height) + ")")
                        print("-------------------")
                    # elif event.key == pygame.K_v:
                    #     if self.p1.velocity == 4:
                    #         self.p1.velocity = 16
                    #     else:
                    #         self.p1.velocity = 4
                    # elif event.key == pygame.K_b:
                    #     if self.p1.dev == True:
                    #         self.p1.dev = False
                    #     else:
                    #         self.p1.dev = True
                elif event.type == pygame.QUIT:

                    self.running = False
                    self.playing = False
                    pygame.quit()

    # def save(self):
    #     with open('save.txt', 'w+') as save:
    #         save.write(f'health:{self.p1.hp}\n')
    #         save.write(f'money:{self.p1.money}\n')
    #         save.write(f'axe:{self.p1.current_axe}\n')
    #         save.write(f'gun:{self.p1.current_arquebus}\n')
    #         save.write(f'pain:{self.p1.pain}\n')
    #         save.write(f'bois:{self.p1.bois}\n')
    #         save.write(f'munitions:{self.p1.munitions}\n')
    #         save.write(f'fer:{self.p1.fer}\n')
    #         save.write(f'bandages:{self.p1.bandage}\n')
    #         save.write(f'current_axe:{self.p1.current_axe}\n')
    #         save.write(f'current_gun:{self.p1.current_arquebus}\n')


class Camera:
    def __init__(self, RPG):
        # Initialize Vector2
        self.vec = pygame.math.Vector2
        # Sets a constant to put the player to the middle of the screen
        self.CONST = self.vec(- RPG.W_WIDTH / 2 + RPG.p1.width / 2, - RPG.W_HEIGHT / 2 + RPG.p1.height / 2)
        # Sets offset
        self.offset = self.vec(0, 0)
        self.offset_float = self.vec(0, 0)

    def scroll(self):
        self.offset_float.x += (RPG.p1.x - self.offset_float.x + self.CONST.x)
        self.offset_float.y += (RPG.p1.y - self.offset_float.y + self.CONST.y)
        self.offset.x, self.offset.y = int(self.offset_float.x), int(self.offset_float.y)

        # For Borders - Comments are for template
        # self.offset.x = max(left_border, self.offset.x)
        # self.offset.x = min(self.offset.x, right_border - RPG.W_WIDTH)
        # Example of border (LIMIT OF BIRD IMAGE)
        self.offset.x = max(0, self.offset.x)
        self.offset.x = min(self.offset.x, RPG.level.MAP_WIDTH - RPG.W_WIDTH)
        self.offset.y = max(0, self.offset.y)
        self.offset.y = min(self.offset.y, RPG.level.MAP_HEIGHT - RPG.W_HEIGHT)


class Player(pygame.sprite.Sprite):
    def __init__(self, RPG, x, y):
        super(Player, self).__init__()
        # self.camera = RPG.camera
        self.index = 0
        self.x = x
        self.y = y
        self.velocity = 4  # Changing it every time lol
        self.direction = 'down'
        self.collided = False
        self.pressed = False
        self.alive = True
        self.hp = 20
        self.money = 10
        self.pain = 0
        self.bois = 5
        self.munitions = 6
        self.fer = 0
        self.bandage = 2
        self.armure = 0

        self.max_health = 20
        self.range = 5
        self.gun_range = 50
        # For inventory
        self.axe = Axe0()
        self.arquebus = Arquebus0()

        self.current_axe = 'Axe0'  # Because Ameliorations May Interfer With Shop Just Leave It Alone
        self.current_arquebus = 'Arquebus0'

        self.axe_cooldown = self.axe.reload_time  # Deciseconds, the game runs at 10 Hertz
        self.gun_cooldown = self.arquebus.reload_time
        self.can_move = True
        self.have_horse = False
        # Cooldowns
        self.axe_cooldown_manager = 5
        self.gun_cooldown_manager = 30
        # ================== ANIMATION ================== #
        self.p_walk_rt = []
        self.p_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Right', 'right1.png')))
        self.p_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Right', 'right2.png')))
        self.p_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Right', 'right3.png')))
        self.p_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Right', 'right4.png')))
        self.p_idle_rt = []
        self.p_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Right', 'idle1.png')))
        self.p_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Right', 'idle1.png')))
        self.p_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Right', 'idle1.png')))
        self.p_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Right', 'idle2.png')))
        self.p_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Right', 'idle2.png')))
        self.p_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Right', 'idle2.png')))
        self.p_axe_rt = []
        self.p_axe_rt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Right', 'axe1.png')))
        self.p_axe_rt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Right', 'axe2.png')))
        self.p_shoot_rt = []
        self.p_shoot_rt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Right', 'shoot1.png')))
        self.p_shoot_rt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Right', 'shoot2.png')))
        self.p_shoot_rt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Right', 'shoot3.png')))
        self.p_shoot_rt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Right', 'shoot4.png')))
        self.p_walk_lt = []
        self.p_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Left', 'left1.png')))
        self.p_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Left', 'left2.png')))
        self.p_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Left', 'left3.png')))
        self.p_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Left', 'left4.png')))
        self.p_idle_lt = []
        self.p_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Left', 'idle1.png')))
        self.p_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Left', 'idle1.png')))
        self.p_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Left', 'idle1.png')))
        self.p_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Left', 'idle2.png')))
        self.p_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Left', 'idle2.png')))
        self.p_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Left', 'idle2.png')))
        self.p_axe_lt = []
        self.p_axe_lt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Left', 'axe1.png')))
        self.p_axe_lt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Left', 'axe2.png')))
        self.p_shoot_lt = []
        self.p_shoot_lt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Left', 'shoot1.png')))
        self.p_shoot_lt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Left', 'shoot2.png')))
        self.p_shoot_lt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Left', 'shoot3.png')))
        self.p_shoot_lt.append(pygame.image.load(os.path.join('Assets', 'Player', 'Left', 'shoot4.png')))
        self.p_walk_up = []
        self.p_walk_up.append(pygame.image.load(os.path.join('Assets', 'Player', 'Up', 'up1.png')))
        self.p_walk_up.append(pygame.image.load(os.path.join('Assets', 'Player', 'Up', 'up2.png')))
        self.p_walk_up.append(pygame.image.load(os.path.join('Assets', 'Player', 'Up', 'up3.png')))
        self.p_walk_up.append(pygame.image.load(os.path.join('Assets', 'Player', 'Up', 'up4.png')))
        self.p_idle_up = []
        self.p_idle_up.append(pygame.image.load(os.path.join('Assets', 'Player', 'Up', 'idle1.png')))
        self.p_idle_up.append(pygame.image.load(os.path.join('Assets', 'Player', 'Up', 'idle1.png')))
        self.p_idle_up.append(pygame.image.load(os.path.join('Assets', 'Player', 'Up', 'idle1.png')))
        self.p_idle_up.append(pygame.image.load(os.path.join('Assets', 'Player', 'Up', 'idle2.png')))
        self.p_idle_up.append(pygame.image.load(os.path.join('Assets', 'Player', 'Up', 'idle2.png')))
        self.p_idle_up.append(pygame.image.load(os.path.join('Assets', 'Player', 'Up', 'idle2.png')))
        self.p_axe_up = []
        self.p_axe_up.append(pygame.image.load(os.path.join('Assets', 'Player', 'Up', 'axe1.png')))
        self.p_axe_up.append(pygame.image.load(os.path.join('Assets', 'Player', 'Up', 'axe2.png')))
        self.p_shoot_up = []
        self.p_shoot_up.append(pygame.image.load(os.path.join('Assets', 'Player', 'Up', 'shoot1.png')))
        self.p_shoot_up.append(pygame.image.load(os.path.join('Assets', 'Player', 'Up', 'shoot2.png')))
        self.p_shoot_up.append(pygame.image.load(os.path.join('Assets', 'Player', 'Up', 'shoot3.png')))
        self.p_shoot_up.append(pygame.image.load(os.path.join('Assets', 'Player', 'Up', 'shoot4.png')))
        self.p_walk_dn = []
        self.p_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Player', 'Down', 'down1.png')))
        self.p_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Player', 'Down', 'down2.png')))
        self.p_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Player', 'Down', 'down3.png')))
        self.p_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Player', 'Down', 'down4.png')))
        self.p_idle_dn = []
        self.p_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Player', 'Down', 'idle1.png')))
        self.p_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Player', 'Down', 'idle1.png')))
        self.p_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Player', 'Down', 'idle1.png')))
        self.p_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Player', 'Down', 'idle2.png')))
        self.p_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Player', 'Down', 'idle2.png')))
        self.p_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Player', 'Down', 'idle2.png')))
        self.p_axe_dn = []
        self.p_axe_dn.append(pygame.image.load(os.path.join('Assets', 'Player', 'Down', 'axe1.png')))
        self.p_axe_dn.append(pygame.image.load(os.path.join('Assets', 'Player', 'Down', 'axe2.png')))
        self.p_shoot_dn = []
        self.p_shoot_dn.append(pygame.image.load(os.path.join('Assets', 'Player', 'Down', 'shoot1.png')))
        self.p_shoot_dn.append(pygame.image.load(os.path.join('Assets', 'Player', 'Down', 'shoot2.png')))
        self.p_shoot_dn.append(pygame.image.load(os.path.join('Assets', 'Player', 'Down', 'shoot3.png')))
        self.p_shoot_dn.append(pygame.image.load(os.path.join('Assets', 'Player', 'Down', 'shoot4.png')))
        self.p_death = []
        self.p_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death1.png')))
        self.p_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death2.png')))
        self.p_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death3.png')))
        self.p_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death4.png')))

        # Use one image as a template for dimensions
        self.rect = self.p_idle_dn[0].get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        # Index of sprites
        self.index = 0
        # Sprite stuff
        self.rect = self.p_walk_dn[0].get_rect()
        self.rect.topleft = self.x, self.y
        self.isaxing = False
        self.isshooting = False
        self.dev = False  # For dev

    def animate(self):
        self.axe_cooldown = self.axe.reload_time
        self.gun_cooldown = self.arquebus.reload_time
        self.gun_range = self.arquebus.range
        self.velocity = self.axe.speed
        self.max_health = 20 + self.armure * Armure().hp

        if self.hp > self.max_health:
            self.hp = self.max_health

        if self.hp < 1:
            if self.alive:
                self.index = 0
                # print('You died')
            RPG.player_death()
        key = pygame.key.get_pressed()
        if key[pygame.K_z] and self.axe_cooldown_manager > self.axe_cooldown and not self.isshooting and self.alive:
            self.isaxing = True
            self.index = 0
            self.axe_cooldown_manager = 0
            self.attack('axe')

        elif key[
            pygame.K_x] and self.gun_cooldown_manager > self.gun_cooldown and not self.isaxing and self.alive and self.munitions > 0:
            self.isshooting = True
            self.index = 0
            self.gun_cooldown_manager = 0
            self.attack('arquebus')
        elif key[pygame.K_x] and self.munitions <= 0:
            RPG.fail_sound.play()

        # elif key[pygame.K_f]:
        #     self.interact()

        elif key[pygame.K_e]:
            RPG.gui = Inventory(RPG)
            RPG.click_sound.play()

        if self.alive:
            key = pygame.key.get_pressed()

            if key[pygame.K_DOWN] and not self.isaxing and not self.isshooting and self.can_move:
                if self.index >= len(self.p_walk_dn):  # Resets the frame count to avoid a Traceback "out of range"
                    self.index = 0
                RPG.screen.blit(self.p_walk_dn[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.y += self.velocity
                self.direction = 'down'
                self.collide()
                if self.collided:
                    self.collided = False
                    self.y -= self.velocity

            elif key[pygame.K_UP] and not self.isaxing and not self.isshooting and self.can_move:
                if self.index >= len(self.p_walk_dn):  # Resets the frame count to avoid a Traceback "out of range"
                    self.index = 0
                RPG.screen.blit(self.p_walk_up[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.y -= self.velocity
                self.direction = 'up'
                self.collide()
                if self.collided:
                    self.collided = False
                    self.y += self.velocity

            elif key[pygame.K_RIGHT] and not self.isaxing and not self.isshooting and self.can_move:
                if self.index >= len(self.p_walk_dn):  # Resets the frame count to avoid a Traceback "out of range"
                    self.index = 0
                RPG.screen.blit(self.p_walk_rt[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.x += self.velocity
                self.direction = 'right'
                self.collide()
                if self.collided:
                    self.collided = False
                    self.x -= self.velocity

            elif key[pygame.K_LEFT] and not self.isaxing and not self.isshooting and self.can_move:
                if self.index >= len(self.p_walk_dn):  # Resets the frame count to avoid a Traceback "out of range"
                    self.index = 0
                RPG.screen.blit(self.p_walk_lt[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.x -= self.velocity
                self.direction = 'left'
                self.collide()
                if self.collided:
                    self.collided = False
                    self.x += self.velocity

            elif self.isaxing:

                if self.index >= len(self.p_axe_dn):  # Resets the frame count to avoid a Traceback "out of range"
                    RPG.axe_hit_sound.play()
                    self.index = 0
                    self.isaxing = False
                if self.direction == 'down':
                    RPG.screen.blit(self.p_axe_dn[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'up':
                    RPG.screen.blit(self.p_axe_up[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'right':
                    RPG.screen.blit(self.p_axe_rt[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'left':
                    RPG.screen.blit(self.p_axe_lt[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))

            elif self.isshooting:
                if self.index == 2:
                    RPG.shoot_sound.play()
                if self.index >= len(self.p_shoot_dn):  # Resets the frame count to avoid a Traceback "out of range"
                    self.index = 0
                    self.isshooting = False
                if self.direction == 'down':
                    RPG.screen.blit(self.p_shoot_dn[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'up':
                    RPG.screen.blit(self.p_shoot_up[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'right':
                    RPG.screen.blit(self.p_shoot_rt[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'left':
                    RPG.screen.blit(self.p_shoot_lt[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                # self.isshooting = False

            else:
                if self.index >= len(self.p_idle_dn):  # Resets the frame count to avoid a Traceback "out of range"
                    self.index = 0

                if self.direction == 'down':
                    RPG.screen.blit(self.p_idle_dn[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'up':
                    RPG.screen.blit(self.p_idle_up[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'right':
                    RPG.screen.blit(self.p_idle_rt[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'left':
                    RPG.screen.blit(self.p_idle_lt[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                else:
                    return

            self.index += 1  # Increment the frame count by 1
            self.axe_cooldown_manager += 1
            self.gun_cooldown_manager += 1

            if self.axe_cooldown_manager >= 500:
                self.axe_cooldown_manager = 10

            if self.gun_cooldown_manager >= 500:
                self.gun_cooldown_manager = 30

            if pygame.key.get_pressed()[pygame.K_f]:
                self.interact()

            if self.dev:
                pygame.draw.rect(RPG.screen, (0, 0, 0),
                                 (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y, self.width, self.height))

    def collide(self):
        for obstacle in RPG.level.obstacles:
            if obstacle.colliderect(pygame.Rect(self.x, self.y, self.width, self.height)):
                self.collided = True
                # pygame.draw.rect(RPG.screen, (0, 0, 0), (
                #     (obstacle.x - RPG.camera.offset.x, obstacle.y - RPG.camera.offset.y),
                #     (obstacle.width, obstacle.height)))

        for i in RPG.level.ennemies:
            if pygame.Rect(i.x + 6, i.y, 4, 4).colliderect(pygame.Rect(self.x, self.y, self.width, self.height)):
                self.collided = True

    def interact(self):
        if self.direction == 'down':
            interact_square = pygame.Rect(self.x, self.y + self.height, self.width, self.range)
            for npc in RPG.level.npcs:
                if npc.rect.colliderect(interact_square) and npc.can_interact:
                    npc.interacted()
            # pygame.draw.rect(RPG.screen, (0,0,0), interact_square) BE CAREFUL NEED CAMERA.OFFSET

        elif self.direction == 'up':
            interact_square = pygame.Rect(self.x, self.y - self.range, self.width, self.range)
            # pygame.draw.rect(RPG.screen, (0,0,0), interact_square) BE CAREFUL NEED CAMERA.OFFSET
            for npc in RPG.level.npcs:
                if interact_square.colliderect(npc.rect) and npc.can_interact:
                    npc.interacted()

        elif self.direction == 'right':
            interact_square = pygame.Rect(self.x + self.width, self.y, self.range, self.height)
            # pygame.draw.rect(RPG.screen, (0,0,0), interact_square) BE CAREFUL NEED CAMERA.OFFSET
            for npc in RPG.level.npcs:
                if npc.rect.colliderect(interact_square) and npc.can_interact:
                    npc.interacted()

        elif self.direction == 'left':
            interact_square = pygame.Rect(self.x - self.range, self.y, self.range, self.height)
            # pygame.draw.rect(RPG.screen, (0,0,0), interact_square) BE CAREFUL NEED CAMERA.OFFSET
            for npc in RPG.level.npcs:
                if npc.rect.colliderect(interact_square) and npc.can_interact:
                    npc.interacted()

    def heal(self, type):
        if type == 'pain':
            self.pain -= 1
            self.hp += Pain().heal
            if self.hp > self.max_health:
                self.hp = self.max_health
        if type == 'bandage':
            self.bandage -= 1
            self.hp = self.max_health
            if self.hp > self.max_health:
                self.hp = self.max_health

    def attack(self, type):
        if type == 'axe':
            if self.direction == 'down':
                attack_square = pygame.Rect(self.x, self.y + self.height, self.width, self.range)
                # pygame.draw.rect(RPG.screen, (0, 0, 0), (self.x - RPG.camera.offset.x, self.y + self.height - RPG.camera.offset.y, self.width, self.range))  # BE CAREFUL NEED CAMERA.OFFSET
                for npc in RPG.level.ennemies:
                    if attack_square.colliderect(pygame.Rect(npc.x, npc.y, npc.rect.width, npc.rect.height)):
                        npc.health -= self.axe.damage


            elif self.direction == 'up':
                attack_square = pygame.Rect(self.x, self.y - self.range, self.width, self.range)
                # pygame.draw.rect(RPG.screen, (0,0,0), (self.x - RPG.camera.offset.x, self.y - self.range - RPG.camera.offset.y, self.width, self.range)) # BE CAREFUL NEED CAMERA.OFFSET
                for npc in RPG.level.ennemies:
                    if attack_square.colliderect(pygame.Rect(npc.x, npc.y, npc.rect.width, npc.rect.height)):
                        npc.health -= self.axe.damage


            elif self.direction == 'right':
                attack_square = pygame.Rect(self.x + self.width, self.y, self.range, self.height)
                # pygame.draw.rect(RPG.screen, (0,0,0), (self.x + self.width - RPG.camera.offset.x, self.y - RPG.camera.offset.y, self.range, self.height)) #BE CAREFUL NEED CAMERA.OFFSET
                for npc in RPG.level.ennemies:
                    if attack_square.colliderect(pygame.Rect(npc.x, npc.y, npc.rect.width, npc.rect.height)):
                        npc.health -= self.axe.damage


            elif self.direction == 'left':
                attack_square = pygame.Rect(self.x - self.range, self.y, self.range, self.height)
                # pygame.draw.rect(RPG.screen, (0,0,0), (self.x - self.range-RPG.camera.offset.x, self.y-RPG.camera.offset.y, self.range, self.height)) # BE CAREFUL NEED CAMERA.OFFSET
                for npc in RPG.level.ennemies:
                    if attack_square.colliderect(pygame.Rect(npc.x, npc.y, npc.rect.width, npc.rect.height)):
                        npc.health -= self.axe.damage



        elif type == 'arquebus' and self.munitions >= 0:
            self.munitions -= 1
            ran = int(random.random() * 3)
            if self.direction == 'down':
                attack_square = pygame.Rect(self.x, self.y + self.height, self.width, self.gun_range)
                # pygame.draw.rect(RPG.screen, (0, 0, 0), (self.x - RPG.camera.offset.x, self.y + self.height - RPG.camera.offset.y, self.width, self.gun_range))  # BE CAREFUL NEED CAMERA.OFFSET
                for npc in RPG.level.ennemies:
                    if attack_square.colliderect(pygame.Rect(npc.x, npc.y, npc.rect.width, npc.rect.height)):
                        if ran == 0:
                            npc.health -= 20
                        else:
                            npc.health -= self.arquebus.damage
                            if npc.health > 0:
                                if ran == 0:
                                    npc.direction = "up"
                                elif ran == 1:
                                    npc.direction = "right"
                                elif ran == 2:
                                    npc.direction = "left"

            elif self.direction == 'up':
                attack_square = pygame.Rect(self.x, self.y - self.gun_range, self.width, self.gun_range)
                # pygame.draw.rect(RPG.screen, (0,0,0), (self.x - RPG.camera.offset.x, self.y - self.gun_range - RPG.camera.offset.y, self.width, self.gun_range)) # BE CAREFUL NEED CAMERA.OFFSET
                for npc in RPG.level.ennemies:
                    if attack_square.colliderect(pygame.Rect(npc.x, npc.y, npc.rect.width, npc.rect.height)):
                        if ran == 0:
                            npc.health -= 20
                        else:
                            npc.health -= self.arquebus.damage
                            if npc.health > 0:
                                if ran == 0:
                                    npc.direction = "up"
                                elif ran == 1:
                                    npc.direction = "right"
                                elif ran == 2:
                                    npc.direction = "left"

            elif self.direction == 'right':
                attack_square = pygame.Rect(self.x + self.width, self.y, self.gun_range, self.height)
                # pygame.draw.rect(RPG.screen, (0,0,0), (self.x + self.width - RPG.camera.offset.x, self.y - RPG.camera.offset.y, self.gun_range, self.height)) #BE CAREFUL NEED CAMERA.OFFSET
                for npc in RPG.level.ennemies:
                    if attack_square.colliderect(pygame.Rect(npc.x, npc.y, npc.rect.width, npc.rect.height)):
                        if ran == 0:
                            npc.health -= 20
                        else:
                            npc.health -= self.arquebus.damage
                            if npc.health > 0:
                                if ran == 0:
                                    npc.direction = "up"
                                elif ran == 1:
                                    npc.direction = "right"
                                elif ran == 2:
                                    npc.direction = "left"

            elif self.direction == 'left':
                attack_square = pygame.Rect(self.x - self.gun_range, self.y, self.gun_range, self.height)
                # pygame.draw.rect(RPG.screen, (0,0,0), (self.x - self.gun_range-RPG.camera.offset.x, self.y-RPG.camera.offset.y, self.gun_range, self.height)) # BE CAREFUL NEED CAMERA.OFFSET
                for npc in RPG.level.ennemies:
                    if attack_square.colliderect(pygame.Rect(npc.x, npc.y, npc.rect.width, npc.rect.height)):
                        if ran == 0:
                            npc.health -= 20
                        else:
                            npc.health -= self.arquebus.damage
                            if npc.health > 0:
                                if ran == 0:
                                    npc.direction = "up"
                                elif ran == 1:
                                    npc.direction = "right"
                                elif ran == 2:
                                    npc.direction = "left"


class Brit(pygame.sprite.Sprite):
    def __init__(self, RPG, x, y, level=False):
        # ================== INITIALIZATION ================== #
        super(Brit, self).__init__()
        self.index = 0
        self.x = x
        self.y = y
        self.velocity = 1
        self.direction = 'down'
        self.moving = False
        self.collided = False
        self.alive = True
        self.health = 20
        self.max_health = 20
        self.attacking = False
        self.range = 8
        self.can_b_hit = True
        self.can_interact = False
        self.level = level
        self.npc_type = 'brit'
        self.gun_range = 30
        self.damage = 5
        # ================== ANIMATION ================== #
        self.b_walk_rt = []
        self.b_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Right', 'right1.png')))
        self.b_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Right', 'right2.png')))
        self.b_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Right', 'right3.png')))
        self.b_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Right', 'right4.png')))
        self.b_idle_rt = []
        self.b_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Right', 'idle1.png')))
        self.b_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Right', 'idle1.png')))
        self.b_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Right', 'idle1.png')))
        self.b_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Right', 'idle2.png')))
        self.b_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Right', 'idle2.png')))
        self.b_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Right', 'idle2.png')))
        self.b_shoot_rt = []
        self.b_shoot_rt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Right', 'shoot1.png')))
        self.b_shoot_rt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Right', 'shoot2.png')))
        self.b_shoot_rt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Right', 'shoot3.png')))
        self.b_shoot_rt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Right', 'shoot4.png')))

        self.b_walk_lt = []
        self.b_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Left', 'left1.png')))
        self.b_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Left', 'left2.png')))
        self.b_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Left', 'left3.png')))
        self.b_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Left', 'left4.png')))
        self.b_idle_lt = []
        self.b_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Left', 'idle1.png')))
        self.b_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Left', 'idle1.png')))
        self.b_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Left', 'idle1.png')))
        self.b_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Left', 'idle2.png')))
        self.b_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Left', 'idle2.png')))
        self.b_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Left', 'idle2.png')))
        self.b_shoot_lt = []
        self.b_shoot_lt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Left', 'shoot1.png')))
        self.b_shoot_lt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Left', 'shoot2.png')))
        self.b_shoot_lt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Left', 'shoot3.png')))
        self.b_shoot_lt.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Left', 'shoot4.png')))

        self.b_walk_up = []
        self.b_walk_up.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Up', 'up1.png')))
        self.b_walk_up.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Up', 'up2.png')))
        self.b_walk_up.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Up', 'up3.png')))
        self.b_walk_up.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Up', 'up4.png')))
        self.b_idle_up = []
        self.b_idle_up.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Up', 'idle1.png')))
        self.b_idle_up.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Up', 'idle1.png')))
        self.b_idle_up.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Up', 'idle1.png')))
        self.b_idle_up.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Up', 'idle2.png')))
        self.b_idle_up.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Up', 'idle2.png')))
        self.b_idle_up.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Up', 'idle2.png')))
        self.b_shoot_up = []
        self.b_shoot_up.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Up', 'shoot1.png')))
        self.b_shoot_up.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Up', 'shoot2.png')))
        self.b_shoot_up.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Up', 'shoot3.png')))
        self.b_shoot_up.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Up', 'shoot4.png')))

        self.b_walk_dn = []
        self.b_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Down', 'down1.png')))
        self.b_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Down', 'down2.png')))
        self.b_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Down', 'down3.png')))
        self.b_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Down', 'down4.png')))
        self.b_idle_dn = []
        self.b_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Down', 'idle1.png')))
        self.b_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Down', 'idle1.png')))
        self.b_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Down', 'idle1.png')))
        self.b_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Down', 'idle2.png')))
        self.b_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Down', 'idle2.png')))
        self.b_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Down', 'idle2.png')))
        self.b_shoot_dn = []
        self.b_shoot_dn.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Down', 'shoot1.png')))
        self.b_shoot_dn.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Down', 'shoot2.png')))
        self.b_shoot_dn.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Down', 'shoot3.png')))
        self.b_shoot_dn.append(pygame.image.load(os.path.join('Assets', 'Brit', 'Down', 'shoot4.png')))
        self.b_death = []
        self.b_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death1.png')))
        self.b_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death2.png')))
        self.b_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death3.png')))
        self.b_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death4.png')))
        # Sprite stuff
        self.rect = self.b_walk_dn[0].get_rect()
        self.rect.topleft = self.x, self.y
        self.width = self.rect.width
        self.height = self.rect.height
        # Attack Cooldown
        self.cooldown = 25
        self.cooldown_manager = 25

        # RPG.level.obstacles.append(self.rect)

    def animate(self):
        if self.health <= 0:
            if self.alive:
                self.index = 0
                RPG.p1.bois += 3
                RPG.p1.money += 5
                if int(random.random()*10) == 4:
                    RPG.p1.fer += 1
                #     RPG.text_box('-', "Un fer est tombé du britannique.")
                # print(int(random.random()*10))
            self.death()
        if self.alive:
            if self.direction == 'down' and self.moving:
                if self.index >= len(self.b_walk_dn):
                    self.index = 0
                RPG.screen.blit(self.b_walk_dn[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.y += self.velocity
            elif self.direction == 'up' and self.moving:
                if self.index >= len(self.b_walk_dn):
                    self.index = 0
                RPG.screen.blit(self.b_walk_up[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.y -= self.velocity
            elif self.direction == 'right' and self.moving:
                if self.index >= len(self.b_walk_dn):
                    self.index = 0
                RPG.screen.blit(self.b_walk_rt[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.x += self.velocity
            elif self.direction == 'left' and self.moving:
                if self.index >= len(self.b_walk_dn):
                    self.index = 0
                RPG.screen.blit(self.b_walk_lt[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.x -= self.velocity

            elif self.attacking:
                if self.index >= len(self.b_shoot_dn):
                    self.index = 0
                    self.cooldown_manager = 0
                    self.attacking = False
                elif self.index == 2:
                    RPG.shoot_sound.play()
                    self.attack()

                if self.direction == 'down':
                    RPG.screen.blit(self.b_shoot_dn[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'up':
                    RPG.screen.blit(self.b_shoot_up[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'right':
                    RPG.screen.blit(self.b_shoot_rt[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'left':
                    RPG.screen.blit(self.b_shoot_lt[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))

            else:
                if self.direction == 'down' and not self.moving:
                    if self.index >= len(self.b_idle_dn):
                        self.index = 0
                    RPG.screen.blit(self.b_idle_dn[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'up' and not self.moving:
                    if self.index >= len(self.b_idle_dn):
                        self.index = 0
                    RPG.screen.blit(self.b_idle_up[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'right' and not self.moving:
                    if self.index >= len(self.b_idle_dn):
                        self.index = 0
                    RPG.screen.blit(self.b_idle_rt[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'left' and not self.moving:
                    if self.index >= len(self.b_idle_dn):
                        self.index = 0
                    RPG.screen.blit(self.b_idle_lt[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
            self.index += 1
            self.cooldown_manager += 1

            if self.cooldown_manager > self.cooldown:
                if pygame.Rect(RPG.p1.x, RPG.p1.y, RPG.p1.width, RPG.p1.height).colliderect(
                        pygame.Rect(self.x, self.y + self.height, self.width, self.gun_range)):
                    self.direction = 'down'
                    self.attacking = True
                    self.index = 0
                    self.cooldown_manager = 0
                    # print('asd')
                elif pygame.Rect(RPG.p1.x, RPG.p1.y, RPG.p1.width, RPG.p1.height).colliderect(
                        pygame.Rect(self.x, self.y - self.gun_range, self.width, self.gun_range)):
                    self.direction = 'up'
                    self.attacking = True
                    self.index = 0
                    self.cooldown_manager = 0
                    # print('asd')
                elif pygame.Rect(RPG.p1.x, RPG.p1.y, RPG.p1.width, RPG.p1.height).colliderect(
                        pygame.Rect(self.x + self.width, self.y, self.gun_range, self.height)):
                    self.direction = 'right'
                    self.attacking = True
                    self.index = 0
                    self.cooldown_manager = 0
                    # print('asd')
                elif pygame.Rect(RPG.p1.x, RPG.p1.y, RPG.p1.width, RPG.p1.height).colliderect(
                        pygame.Rect(self.x - self.gun_range, self.y, self.gun_range, self.height)):
                    self.direction = 'left'
                    self.attacking = True
                    self.index = 0
                    self.cooldown_manager = 0
                    # print('asd')

            if self.cooldown_manager >= 300:
                self.cooldown_manager = 20

    def goto(self, targetx, targety, preferx=True):
        if preferx:
            if self.x in range(targetx - self.range, targetx + self.range):
                if self.x < targetx:
                    self.direction = 'right'
                elif self.x > targetx:
                    self.direction = 'left'
                elif self.y < targety:
                    self.direction = 'down'
                elif self.y > targety:
                    self.direction = 'up'
                self.moving = False
                self.attacking = True
            elif self.y in range(targety - self.range, targety + self.range):
                if self.x < targetx:
                    self.direction = 'right'
                if self.x > targetx:
                    self.direction = 'left'
                if self.y < targety:
                    self.direction = 'down'
                if self.y > targety:
                    self.direction = 'up'
                self.moving = False
                self.attacking = True
            elif self.x < targetx:
                self.attacking = False
                self.moving = True
                self.direction = 'right'
            elif self.x > targetx:
                self.direction = 'left'
                self.attacking = False
                self.moving = True
            elif self.y < targety:
                self.direction = 'down'
                self.attacking = False
                self.moving = True
            elif self.y > targety:
                self.direction = 'up'
                self.attacking = False
                self.moving = True
            else:
                self.moving = False

        elif not preferx:
            if self.x in range(targetx - self.range, targetx + self.range):
                if self.x < targetx:
                    self.direction = 'right'
                elif self.x > targetx:
                    self.direction = 'left'
                elif self.y < targety:
                    self.direction = 'down'
                elif self.y > targety:
                    self.direction = 'up'
                self.moving = False
                self.attacking = True
            elif self.y in range(targety - self.range, targety + self.range):
                if self.x < targetx:
                    self.direction = 'right'
                if self.x > targetx:
                    self.direction = 'left'
                if self.y < targety:
                    self.direction = 'down'
                if self.y > targety:
                    self.direction = 'up'
                self.attacking = True
                self.moving = False
            if self.y < targety:
                self.moving = True
                self.attacking = False
                self.direction = 'down'
            elif self.y > targety:
                self.direction = 'up'
                self.attacking = False
                self.moving = True
            elif self.x < targetx:
                self.direction = 'right'
                self.attacking = False
                self.moving = True
            elif self.x > targetx:
                self.direction = 'left'
                self.attacking = False
                self.moving = True
            elif self.x == targetx or self.y == targety:
                self.moving = False
                self.attacking = True
            else:
                self.moving = False

    def attack(self):
        if self.direction == 'down':
            attack_square = pygame.Rect(self.x, self.y + self.height, self.width, self.gun_range)
            # pygame.draw.rect(RPG.screen, (0, 0, 0), (self.x - RPG.camera.offset.x, self.y + self.height - RPG.camera.offset.y, self.width, self.gun_range))  # BE CAREFUL NEED CAMERA.OFFSET

            if attack_square.colliderect(pygame.Rect(RPG.p1.x, RPG.p1.y, RPG.p1.width, RPG.p1.height)):
                RPG.p1.hp -= self.damage
                self.attacking = False

        elif self.direction == 'up':
            attack_square = pygame.Rect(self.x, self.y - self.gun_range, self.width, self.gun_range)
            # pygame.draw.rect(RPG.screen, (0,0,0), (self.x - RPG.camera.offset.x, self.y - self.gun_range - RPG.camera.offset.y, self.width, self.gun_range)) # BE CAREFUL NEED CAMERA.OFFSET

            if attack_square.colliderect(pygame.Rect(RPG.p1.x, RPG.p1.y, RPG.p1.width, RPG.p1.height)):
                RPG.p1.hp -= self.damage
                self.attacking = False

        elif self.direction == 'right':
            attack_square = pygame.Rect(self.x + self.width, self.y, self.gun_range, self.height)
            # pygame.draw.rect(RPG.screen, (0,0,0), (self.x + self.width - RPG.camera.offset.x, self.y - RPG.camera.offset.y, self.gun_range, self.height)) #BE CAREFUL NEED CAMERA.OFFSET

            if attack_square.colliderect(pygame.Rect(RPG.p1.x, RPG.p1.y, RPG.p1.width, RPG.p1.height)):
                RPG.p1.hp -= self.damage
                self.attacking = False

        elif self.direction == 'left':
            attack_square = pygame.Rect(self.x - self.gun_range, self.y, self.gun_range, self.height)
            # pygame.draw.rect(RPG.screen, (0,0,0), (self.x - self.gun_range-RPG.camera.offset.x, self.y-RPG.camera.offset.y, self.gun_range, self.height)) # BE CAREFUL NEED CAMERA.OFFSET

            if attack_square.colliderect(pygame.Rect(RPG.p1.x, RPG.p1.y, RPG.p1.width, RPG.p1.height)):
                RPG.p1.hp -= self.damage
                self.attacking = False

    def death(self):
        RPG.npc_death(self, self.x, self.y)


class Red(pygame.sprite.Sprite):
    def __init__(self, RPG, x, y):
        # ================== INITIALIZATION ================== #
        super(Red, self).__init__()
        self.npc_type = 'red'
        self.index = 0
        self.x = x
        self.y = y
        self.velocity = 2
        self.direction = 'down'
        self.moving = False
        self.collided = False
        self.alive = True
        self.can_interact = True
        # ================== ANIMATION ================== #
        self.r_walk_rt = []
        self.r_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Red', 'Right', 'right1.png')))
        self.r_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Red', 'Right', 'right2.png')))
        self.r_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Red', 'Right', 'right3.png')))
        self.r_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Red', 'Right', 'right4.png')))
        self.r_idle_rt = []
        self.r_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Red', 'Right', 'idle1.png')))
        self.r_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Red', 'Right', 'idle1.png')))
        self.r_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Red', 'Right', 'idle1.png')))
        self.r_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Red', 'Right', 'idle2.png')))
        self.r_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Red', 'Right', 'idle2.png')))
        self.r_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Red', 'Right', 'idle2.png')))
        self.r_walk_lt = []
        self.r_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Red', 'Left', 'left1.png')))
        self.r_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Red', 'Left', 'left2.png')))
        self.r_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Red', 'Left', 'left3.png')))
        self.r_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Red', 'Left', 'left4.png')))
        self.r_idle_lt = []
        self.r_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Red', 'Left', 'idle1.png')))
        self.r_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Red', 'Left', 'idle1.png')))
        self.r_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Red', 'Left', 'idle1.png')))
        self.r_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Red', 'Left', 'idle2.png')))
        self.r_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Red', 'Left', 'idle2.png')))
        self.r_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Red', 'Left', 'idle2.png')))
        self.r_walk_up = []
        self.r_walk_up.append(pygame.image.load(os.path.join('Assets', 'Red', 'Up', 'up1.png')))
        self.r_walk_up.append(pygame.image.load(os.path.join('Assets', 'Red', 'Up', 'up2.png')))
        self.r_walk_up.append(pygame.image.load(os.path.join('Assets', 'Red', 'Up', 'up3.png')))
        self.r_walk_up.append(pygame.image.load(os.path.join('Assets', 'Red', 'Up', 'up4.png')))
        self.r_idle_up = []
        self.r_idle_up.append(pygame.image.load(os.path.join('Assets', 'Red', 'Up', 'idle1.png')))
        self.r_idle_up.append(pygame.image.load(os.path.join('Assets', 'Red', 'Up', 'idle1.png')))
        self.r_idle_up.append(pygame.image.load(os.path.join('Assets', 'Red', 'Up', 'idle1.png')))
        self.r_idle_up.append(pygame.image.load(os.path.join('Assets', 'Red', 'Up', 'idle2.png')))
        self.r_idle_up.append(pygame.image.load(os.path.join('Assets', 'Red', 'Up', 'idle2.png')))
        self.r_idle_up.append(pygame.image.load(os.path.join('Assets', 'Red', 'Up', 'idle2.png')))
        self.r_walk_dn = []
        self.r_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Red', 'Down', 'down1.png')))
        self.r_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Red', 'Down', 'down2.png')))
        self.r_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Red', 'Down', 'down3.png')))
        self.r_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Red', 'Down', 'down4.png')))
        self.r_idle_dn = []
        self.r_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Red', 'Down', 'idle1.png')))
        self.r_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Red', 'Down', 'idle1.png')))
        self.r_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Red', 'Down', 'idle1.png')))
        self.r_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Red', 'Down', 'idle2.png')))
        self.r_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Red', 'Down', 'idle2.png')))
        self.r_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Red', 'Down', 'idle2.png')))
        self.r_death = []
        self.r_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death1.png')))
        self.r_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death2.png')))
        self.r_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death3.png')))
        self.r_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death4.png')))
        # Sprite stuff
        self.rect = self.r_walk_dn[0].get_rect()
        self.rect.topleft = self.x, self.y

    def animate(self):
        if self.alive:
            if self.direction == 'down' and self.moving:
                if self.index >= len(self.r_walk_dn):
                    self.index = 0
                RPG.screen.blit(self.r_walk_dn[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.y += self.velocity
            elif self.direction == 'up' and self.moving:
                if self.index >= len(self.r_walk_dn):
                    self.index = 0
                RPG.screen.blit(self.r_walk_up[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.y -= self.velocity
            elif self.direction == 'right' and self.moving:
                if self.index >= len(self.r_walk_dn):
                    self.index = 0
                RPG.screen.blit(self.r_walk_rt[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.x += self.velocity
            elif self.direction == 'left' and self.moving:
                if self.index >= len(self.r_walk_dn):
                    self.index = 0
                RPG.screen.blit(self.r_walk_lt[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.x -= self.velocity
            else:
                if self.index >= len(self.r_idle_dn):
                    self.index = 0
                if self.direction == 'down' and not self.moving:
                    RPG.screen.blit(self.r_idle_dn[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'up' and not self.moving:
                    RPG.screen.blit(self.r_idle_up[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'right' and not self.moving:
                    RPG.screen.blit(self.r_idle_rt[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'left' and not self.moving:
                    RPG.screen.blit(self.r_idle_lt[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
            self.index += 1

    def interacted(self):
        if RPG.current_level == '0':
            RPG.text_box('Wolfred Nelson', 'TUEZ LES TOUS !')
        elif RPG.current_level == '1':
            RPG.text_box('Commandant Brown',
                         "Ils sont peut-être plus nombreux, mais nous nous battrons jusqu'à la mort !")
        elif RPG.current_level == '2':
            RPG.text_box('Commandant Chénier', "Colborn est malin, mais il faut penser en dehors de la boite.")

    def goto(self, targetx, targety, preferx=True):
        if preferx:
            if self.x < targetx:
                self.moving = True
                self.direction = 'right'
            elif self.x > targetx:
                self.direction = 'left'
                self.moving = True
            elif self.y < targety:
                self.direction = 'down'
                self.moving = True
            elif self.y > targety:
                self.direction = 'up'
                self.moving = True
            else:
                self.moving = False
        elif not preferx:
            if self.x < targetx:
                self.moving = True
                self.direction = 'right'
            elif self.x > targetx:
                self.direction = 'left'
                self.moving = True
            elif self.y < targety:
                self.direction = 'down'
                self.moving = True
            elif self.y > targety:
                self.direction = 'up'
                self.moving = True
            else:
                self.moving = False


class Patriote(pygame.sprite.Sprite):
    def __init__(self, RPG, x, y):
        # ================== INITIALIZATION ================== #
        super(Patriote, self).__init__()
        self.npc_type = 'patriote'
        self.index = 0
        self.x = x
        self.y = y
        self.velocity = 2
        self.direction = 'down'
        self.moving = False
        self.collided = False
        self.alive = True
        self.can_interact = True
        # ================== ANIMATION ================== #
        self.p_walk_rt = []
        self.p_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Right', 'right1.png')))
        self.p_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Right', 'right2.png')))
        self.p_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Right', 'right3.png')))
        self.p_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Right', 'right4.png')))
        self.p_idle_rt = []
        self.p_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Right', 'idle1.png')))
        self.p_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Right', 'idle1.png')))
        self.p_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Right', 'idle1.png')))
        self.p_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Right', 'idle2.png')))
        self.p_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Right', 'idle2.png')))
        self.p_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Right', 'idle2.png')))
        self.p_walk_lt = []
        self.p_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Left', 'left1.png')))
        self.p_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Left', 'left2.png')))
        self.p_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Left', 'left3.png')))
        self.p_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Left', 'left4.png')))
        self.p_idle_lt = []
        self.p_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Left', 'idle1.png')))
        self.p_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Left', 'idle1.png')))
        self.p_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Left', 'idle1.png')))
        self.p_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Left', 'idle2.png')))
        self.p_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Left', 'idle2.png')))
        self.p_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Left', 'idle2.png')))
        self.p_walk_up = []
        self.p_walk_up.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Up', 'up1.png')))
        self.p_walk_up.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Up', 'up2.png')))
        self.p_walk_up.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Up', 'up3.png')))
        self.p_walk_up.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Up', 'up4.png')))
        self.p_idle_up = []
        self.p_idle_up.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Up', 'idle1.png')))
        self.p_idle_up.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Up', 'idle1.png')))
        self.p_idle_up.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Up', 'idle1.png')))
        self.p_idle_up.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Up', 'idle2.png')))
        self.p_idle_up.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Up', 'idle2.png')))
        self.p_idle_up.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Up', 'idle2.png')))
        self.p_walk_dn = []
        self.p_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Down', 'down1.png')))
        self.p_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Down', 'down2.png')))
        self.p_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Down', 'down3.png')))
        self.p_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Down', 'down4.png')))
        self.p_idle_dn = []
        self.p_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Down', 'idle1.png')))
        self.p_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Down', 'idle1.png')))
        self.p_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Down', 'idle1.png')))
        self.p_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Down', 'idle2.png')))
        self.p_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Down', 'idle2.png')))
        self.p_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Patriote', 'Down', 'idle2.png')))
        self.p_death = []
        self.p_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death1.png')))
        self.p_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death2.png')))
        self.p_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death3.png')))
        self.p_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death4.png')))
        # Sprite stuff
        self.rect = self.p_walk_dn[0].get_rect()
        self.rect.topleft = self.x, self.y

        self.t_index = 0

    def interacted(self):
        if RPG.current_level == '0':

            RPG.text_box("Alexis", "J'ai dû quitter ma famille pour venir me battre. J'espère que tu vas t'en sortir...")
            RPG.text_box("Alexis", "Je te souhaite bonne chance pour ta mission, plusieurs hommes sont morts pour cet événement.", False)
            RPG.text_box("Alexis", "Les anglais sont regroupés devant leur camp, règle les leur compte pour nous tous !", False)
        elif RPG.current_level == '1':

            RPG.text_box("Pierre", "Malgré notre victoire à Saint-Denis, je pense que les anglais vont remporter cette bataille.")
            RPG.text_box("Pierre", "Ils sont beaucoup trop nombreux, ils n'ont fait qu'une bouchée de nous. Tu es notre seul espoir.", False)
            RPG.text_box("Pierre","410 soldats et 20 cavaliers contre 250 citoyens, la bataille est perdue d'avance", False)

        elif RPG.current_level == '2':

            RPG.text_box("Jean-Pierre", "QUOI ?! Ils sont 1500 et nous sommes 200 ! Nous ne pouvons vaincre !")
            RPG.text_box("Jean-Pierre", "200 soldats ... Nous avions prévu au moins 3 fois plus ...", False)
            RPG.text_box("Jean-Pierre", "Après tout, peut-être que l'église a raison, nous devrions nous rendre ...", False)

    def animate(self):
        if self.alive:
            if self.direction == 'down' and self.moving:
                if self.index >= len(self.p_walk_dn):
                    self.index = 0
                RPG.screen.blit(self.p_walk_dn[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.y += self.velocity
            elif self.direction == 'up' and self.moving:
                if self.index >= len(self.p_walk_dn):
                    self.index = 0
                RPG.screen.blit(self.p_walk_up[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.y -= self.velocity
            elif self.direction == 'right' and self.moving:
                if self.index >= len(self.p_walk_dn):
                    self.index = 0
                RPG.screen.blit(self.p_walk_rt[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.x += self.velocity
            elif self.direction == 'left' and self.moving:
                if self.index >= len(self.p_walk_dn):
                    self.index = 0
                RPG.screen.blit(self.p_walk_lt[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.x -= self.velocity
            else:
                if self.index >= len(self.p_idle_dn):
                    self.index = 0
                if self.direction == 'down' and not self.moving:
                    RPG.screen.blit(self.p_idle_dn[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'up' and not self.moving:
                    RPG.screen.blit(self.p_idle_up[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'right' and not self.moving:
                    RPG.screen.blit(self.p_idle_rt[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'left' and not self.moving:
                    RPG.screen.blit(self.p_idle_lt[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
            self.index += 1

    def goto(self, targetx, targety, preferx=True):
        if preferx:
            if self.x < targetx:
                self.moving = True
                self.direction = 'right'
            elif self.x > targetx:
                self.direction = 'left'
                self.moving = True
            elif self.y < targety:
                self.direction = 'down'
                self.moving = True
            elif self.y > targety:
                self.direction = 'up'
                self.moving = True
            else:
                self.moving = False
        elif not preferx:
            if self.x < targetx:
                self.moving = True
                self.direction = 'right'
            elif self.x > targetx:
                self.direction = 'left'
                self.moving = True
            elif self.y < targety:
                self.direction = 'down'
                self.moving = True
            elif self.y > targety:
                self.direction = 'up'
                self.moving = True
            else:
                self.moving = False


class Jean(pygame.sprite.Sprite):
    def __init__(self, RPG, x, y):
        # ================== INITIALIZATION ================== #
        super(Jean, self).__init__()
        self.npc_type = 'jean'
        self.index = 0
        self.x = x
        self.y = y
        self.velocity = 2
        self.direction = 'down'
        self.moving = False
        self.collided = False
        self.alive = True
        self.can_interact = True
        # ================== ANIMATION ================== #
        self.j_walk_rt = []
        self.j_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Right', 'right1.png')))
        self.j_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Right', 'right2.png')))
        self.j_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Right', 'right3.png')))
        self.j_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Right', 'right4.png')))
        self.j_idle_rt = []
        self.j_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Right', 'idle1.png')))
        self.j_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Right', 'idle1.png')))
        self.j_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Right', 'idle1.png')))
        self.j_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Right', 'idle2.png')))
        self.j_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Right', 'idle2.png')))
        self.j_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Right', 'idle2.png')))
        self.j_shoot_rt = []
        self.j_shoot_rt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Right', 'shoot1.png')))
        self.j_shoot_rt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Right', 'shoot2.png')))
        self.j_shoot_rt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Right', 'shoot3.png')))
        self.j_shoot_rt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Right', 'shoot4.png')))
        self.j_walk_lt = []
        self.j_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Left', 'left1.png')))
        self.j_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Left', 'left2.png')))
        self.j_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Left', 'left3.png')))
        self.j_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Left', 'left4.png')))
        self.j_idle_lt = []
        self.j_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Left', 'idle1.png')))
        self.j_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Left', 'idle1.png')))
        self.j_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Left', 'idle1.png')))
        self.j_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Left', 'idle2.png')))
        self.j_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Left', 'idle2.png')))
        self.j_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Left', 'idle2.png')))
        self.j_shoot_lt = []
        self.j_shoot_lt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Left', 'shoot1.png')))
        self.j_shoot_lt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Left', 'shoot2.png')))
        self.j_shoot_lt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Left', 'shoot3.png')))
        self.j_shoot_lt.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Left', 'shoot4.png')))
        self.j_walk_up = []
        self.j_walk_up.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Up', 'up1.png')))
        self.j_walk_up.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Up', 'up2.png')))
        self.j_walk_up.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Up', 'up3.png')))
        self.j_walk_up.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Up', 'up4.png')))
        self.j_idle_up = []
        self.j_idle_up.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Up', 'idle1.png')))
        self.j_idle_up.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Up', 'idle1.png')))
        self.j_idle_up.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Up', 'idle1.png')))
        self.j_idle_up.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Up', 'idle2.png')))
        self.j_idle_up.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Up', 'idle2.png')))
        self.j_idle_up.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Up', 'idle2.png')))
        self.j_shoot_up = []
        self.j_shoot_up.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Up', 'shoot1.png')))
        self.j_shoot_up.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Up', 'shoot2.png')))
        self.j_shoot_up.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Up', 'shoot3.png')))
        self.j_shoot_up.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Up', 'shoot4.png')))
        self.j_walk_dn = []
        self.j_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Down', 'down1.png')))
        self.j_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Down', 'down2.png')))
        self.j_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Down', 'down3.png')))
        self.j_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Down', 'down4.png')))
        self.j_idle_dn = []
        self.j_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Down', 'idle1.png')))
        self.j_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Down', 'idle1.png')))
        self.j_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Down', 'idle1.png')))
        self.j_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Down', 'idle2.png')))
        self.j_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Down', 'idle2.png')))
        self.j_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Down', 'idle2.png')))
        self.j_shoot_dn = []
        self.j_shoot_dn.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Down', 'shoot1.png')))
        self.j_shoot_dn.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Down', 'shoot2.png')))
        self.j_shoot_dn.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Down', 'shoot3.png')))
        self.j_shoot_dn.append(pygame.image.load(os.path.join('Assets', 'Jean', 'Down', 'shoot4.png')))
        self.j_death = []
        self.j_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death1.png')))
        self.j_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death2.png')))
        self.j_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death3.png')))
        self.j_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death4.png')))
        # Sprite stuff
        self.rect = self.j_walk_dn[0].get_rect()
        self.rect.topleft = self.x, self.y

    def interacted(self):
        if RPG.current_level == '0':
            RPG.text_box("Jean", "N'oublie pas ce qu'ils ont fait à ton père et a toute nos familles.")
            RPG.text_box("Jean", "La vengeance est un plat qui se mange froid. Détruit leur campement, ", False)
            RPG.text_box("Jean", "et fait peur aux commandants anglais avec cette attaque.", False)
        elif RPG.current_level == '1':
            RPG.text_box('Jean', "Ils ont commencé par nous donner du faux pouvoir avec la chambre d'assemblée.")
            RPG.text_box('Jean', "Le gouverneur pouvait détruire toute une décision avec son droit de véto.", False)
            RPG.text_box('Jean', "Nous avions manifesté notre mécontentement pacifiquement, jusqu'à maintenant,", False)
            RPG.text_box('Jean', "MAIS IL EST TEMPS D'EN FINIR !", False)
        elif RPG.current_level == '2':
            RPG.text_box('Jean',
                         "Tu es incroyable, grâce à toi, nous avons gagné la bataille désespérée de Saint-Charles,")
            RPG.text_box('Jean', "Je me demande comment tu as fait pour en vaincre autant, quel est ton secret ?",
                         False)
            RPG.text_box('Jean', "Parviendras-tu à nous venger ? À régler l'injustice ?", False)
            # RPG.text_box('Jean', "Ne fais jamais confiance aux anglais, ils nous ont enlever notre ", False)

    def animate(self):
        if self.alive:
            if self.direction == 'down' and self.moving:
                if self.index >= len(self.j_walk_dn):
                    self.index = 0
                RPG.screen.blit(self.j_walk_dn[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.y += self.velocity
            elif self.direction == 'up' and self.moving:
                if self.index >= len(self.j_walk_dn):
                    self.index = 0
                RPG.screen.blit(self.j_walk_up[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.y -= self.velocity
            elif self.direction == 'right' and self.moving:
                if self.index >= len(self.j_walk_dn):
                    self.index = 0
                RPG.screen.blit(self.j_walk_rt[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.x += self.velocity
            elif self.direction == 'left' and self.moving:
                if self.index >= len(self.j_walk_dn):
                    self.index = 0
                RPG.screen.blit(self.j_walk_lt[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.x -= self.velocity
            else:
                if self.index >= len(self.j_idle_dn):
                    self.index = 0
                if self.direction == 'down' and not self.moving:
                    RPG.screen.blit(self.j_idle_dn[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'up' and not self.moving:
                    RPG.screen.blit(self.j_idle_up[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'right' and not self.moving:
                    RPG.screen.blit(self.j_idle_rt[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'left' and not self.moving:
                    RPG.screen.blit(self.j_idle_lt[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
            self.index += 1

    def goto(self, targetx, targety, preferx=True):
        if preferx:
            if self.x < targetx:
                self.moving = True
                self.direction = 'right'
            elif self.x > targetx:
                self.direction = 'left'
                self.moving = True
            elif self.y < targety:
                self.direction = 'down'
                self.moving = True
            elif self.y > targety:
                self.direction = 'up'
                self.moving = True
            else:
                self.moving = False
        elif not preferx:
            if self.x < targetx:
                self.moving = True
                self.direction = 'right'
            elif self.x > targetx:
                self.direction = 'left'
                self.moving = True
            elif self.y < targety:
                self.direction = 'down'
                self.moving = True
            elif self.y > targety:
                self.direction = 'up'
                self.moving = True
            else:
                self.moving = False


class Roger(pygame.sprite.Sprite):
    def __init__(self, RPG, x, y):
        # ================== INITIALIZATION ================== #
        super(Roger, self).__init__()
        self.npc_type = 'roger'
        self.index = 0
        self.x = x
        self.y = y
        self.velocity = 2
        self.direction = 'down'
        self.moving = False
        self.collided = False
        self.alive = True
        self.can_interact = True
        # ================== ANIMATION ================== #
        self.r_walk_rt = []
        self.r_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Right', 'right1.png')))
        self.r_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Right', 'right2.png')))
        self.r_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Right', 'right3.png')))
        self.r_walk_rt.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Right', 'right4.png')))
        self.r_idle_rt = []
        self.r_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Right', 'idle1.png')))
        self.r_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Right', 'idle1.png')))
        self.r_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Right', 'idle1.png')))
        self.r_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Right', 'idle2.png')))
        self.r_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Right', 'idle2.png')))
        self.r_idle_rt.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Right', 'idle2.png')))
        self.r_walk_lt = []
        self.r_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Left', 'left1.png')))
        self.r_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Left', 'left2.png')))
        self.r_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Left', 'left3.png')))
        self.r_walk_lt.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Left', 'left4.png')))
        self.r_idle_lt = []
        self.r_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Left', 'idle1.png')))
        self.r_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Left', 'idle1.png')))
        self.r_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Left', 'idle1.png')))
        self.r_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Left', 'idle2.png')))
        self.r_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Left', 'idle2.png')))
        self.r_idle_lt.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Left', 'idle2.png')))
        self.r_walk_up = []
        self.r_walk_up.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Up', 'up1.png')))
        self.r_walk_up.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Up', 'up2.png')))
        self.r_walk_up.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Up', 'up3.png')))
        self.r_walk_up.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Up', 'up4.png')))
        self.r_idle_up = []
        self.r_idle_up.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Up', 'idle1.png')))
        self.r_idle_up.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Up', 'idle1.png')))
        self.r_idle_up.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Up', 'idle1.png')))
        self.r_idle_up.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Up', 'idle2.png')))
        self.r_idle_up.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Up', 'idle2.png')))
        self.r_idle_up.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Up', 'idle2.png')))
        self.r_walk_dn = []
        self.r_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Down', 'down1.png')))
        self.r_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Down', 'down2.png')))
        self.r_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Down', 'down3.png')))
        self.r_walk_dn.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Down', 'down4.png')))
        self.r_idle_dn = []
        self.r_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Down', 'idle1.png')))
        self.r_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Down', 'idle1.png')))
        self.r_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Down', 'idle1.png')))
        self.r_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Down', 'idle2.png')))
        self.r_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Down', 'idle2.png')))
        self.r_idle_dn.append(pygame.image.load(os.path.join('Assets', 'Roger', 'Down', 'idle2.png')))
        self.r_death = []
        self.r_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death1.png')))
        self.r_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death2.png')))
        self.r_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death3.png')))
        self.r_death.append(pygame.image.load(os.path.join('Assets', 'Death', 'death4.png')))
        # Sprite stuff
        self.rect = self.r_walk_dn[0].get_rect()
        self.rect.topleft = self.x, self.y

    def interacted(self):
        if RPG.current_level == '0':
            RPG.text_box("Roger", "Il est important de se battre pour notre liberté. Joins-toi aux tiens.")
            RPG.text_box("Roger", "Et d'ailleurs, tiens quelques conseils :", False)
            RPG.text_box("Roger", "Tu peux tirer à travers les murs et ta portée est plus grande,", False)
            RPG.text_box("Roger", "Tu peux donc tuer sans te faire toucher !", False)

        elif RPG.current_level == '1':
            RPG.text_box("Roger", "Je vais me battre jusqu'à la fin, même si cela signifie ma mort.")
            RPG.text_box("Roger", "Mais toi protège-toi, tu es notre seul espoir.", False)
            RPG.text_box("Roger", "Si tu n'as pas assez de ressource, attend un peu,", False)
            RPG.text_box("Roger", "Tant que le jeu est ouvert, tu gagneras du bois petit à petit,", False)
            RPG.text_box('Roger', "N'oublie pas de le vendre !", False)


        elif RPG.current_level == '2':
            RPG.text_box("Roger", "Quand le moral est bas, il faut lancer une attaque!")
            RPG.text_box("Roger", "Ils sont très nombreux, mais nous comptons tous sur toi.", False)

    def animate(self):
        if self.alive:
            if self.direction == 'down' and self.moving:
                if self.index >= len(self.r_walk_dn):
                    self.index = 0
                RPG.screen.blit(self.r_walk_dn[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.y += self.velocity
            elif self.direction == 'up' and self.moving:
                if self.index >= len(self.r_walk_dn):
                    self.index = 0
                RPG.screen.blit(self.r_walk_up[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.y -= self.velocity
            elif self.direction == 'right' and self.moving:
                if self.index >= len(self.r_walk_dn):
                    self.index = 0
                RPG.screen.blit(self.r_walk_rt[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.x += self.velocity
            elif self.direction == 'left' and self.moving:
                if self.index >= len(self.r_walk_dn):
                    self.index = 0
                RPG.screen.blit(self.r_walk_lt[self.index],
                                (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                self.x -= self.velocity
            else:
                if self.index >= len(self.r_idle_dn):
                    self.index = 0
                if self.direction == 'down' and not self.moving:
                    RPG.screen.blit(self.r_idle_dn[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'up' and not self.moving:
                    RPG.screen.blit(self.r_idle_up[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'right' and not self.moving:
                    RPG.screen.blit(self.r_idle_rt[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
                elif self.direction == 'left' and not self.moving:
                    RPG.screen.blit(self.r_idle_lt[self.index],
                                    (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
            self.index += 1

    def goto(self, targetx, targety, preferx=True):
        if preferx:
            if self.x < targetx:
                self.moving = True
                self.direction = 'right'
            elif self.x > targetx:
                self.direction = 'left'
                self.moving = True
            elif self.y < targety:
                self.direction = 'down'
                self.moving = True
            elif self.y > targety:
                self.direction = 'up'
                self.moving = True
            else:
                self.moving = False
        elif not preferx:
            if self.x < targetx:
                self.moving = True
                self.direction = 'right'
            elif self.x > targetx:
                self.direction = 'left'
                self.moving = True
            elif self.y < targety:
                self.direction = 'down'
                self.moving = True
            elif self.y > targety:
                self.direction = 'up'
                self.moving = True
            else:
                self.moving = False


class Forgeron(pygame.sprite.Sprite):
    def __init__(self, RPG, x, y):
        # ================== INITIALIZATION ================== #
        super(Forgeron, self).__init__()
        self.index = 0
        self.x = x
        self.y = y
        self.velocity = 2
        self.can_interact = True
        self.alr_interacted = False

        # ================== ANIMATION ================== #
        self.images = []
        self.images.append(pygame.image.load(os.path.join('Assets', 'BasicNPCS', 'forgeron1.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'BasicNPCS', 'forgeron1.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'BasicNPCS', 'forgeron1.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'BasicNPCS', 'forgeron2.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'BasicNPCS', 'forgeron2.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'BasicNPCS', 'forgeron2.png')))
        # Sprite stuff
        self.rect = self.images[0].get_rect()
        self.rect.topleft = self.x, self.y

    def animate(self):
        if self.index >= len(self.images):
            self.index = 0
        RPG.screen.blit(self.images[self.index],
                        (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
        # Interaction
        # obstacle.colliderect(pygame.Rect(self.x, self.y, self.width, self.height)):
        # if self.rect.colliderect()

        self.index += 1

    def interacted(self):
        if RPG.current_level == "0":
            if not self.alr_interacted:
                if RPG.p1.bois >= 1:
                    RPG.text_box('Forgeron',
                                 "J'ai besoin de bois pour mon foyer, je t'achète tout ton bois pour 2 Louis chaque.")
                    RPG.text_box('Forgeron',
                                 "Il ne sert à rien de refuser, je propose un meilleur prix que le marchand.", False)
                    RPG.p1.money += RPG.p1.bois * 2
                    RPG.p1.bois = 0
                    self.alr_interacted = True
                    RPG.text_box('-', "L'échange a été réalisé avec succès !", False)
                else:
                    RPG.text_box('Forgeron',
                                 "Je t'acheterai bien tout ton bois, mais je vois que tu n'en a pas actuellement.")
                    RPG.text_box('Forgeron', "Reviens me voir plus tard quand tu en auras !", False)
            else:
                RPG.text_box('Forgeron', "Tu es ici pour que je t'explique les armes ?")
                RPG.text_box('Forgeron', "Le marchand vend trois armes différentes :", False)
                RPG.text_box('Forgeron',
                             "La première hache (avec un seul côté) permet de tuer à coup sûr un britannique, ", False)
                RPG.text_box('Forgeron', "en un seul coup, cependant, elle est plus lourde,", False)
                RPG.text_box('Forgeron', "il faut donc se reposer plus longtemps avant chaque coup", False)
                RPG.text_box('Forgeron', "L'autre hache permet aussi de tuer en un coup, mais elle est légère,", False)
                RPG.text_box('Forgeron', "Le temps de repos est donc moindre et elle augmente la vitesse de marche",
                             False)
                RPG.text_box('Forgeron', "Le fusil à une plus grande portée et il tue à coup sûr.", False)
                RPG.text_box('Forgeron', "Il prend ausis moins de temps à recharger. ", False)
                RPG.text_box('Forgeron', "Ah et j'allais oublier : l'armure augmente vos pv.", False)


        elif RPG.current_level == "1":
            RPG.text_box('Forgeron', "Je te passerai bien quelques munitions, mais les balles sont rares ces temps-ci.")
            RPG.text_box('Forgeron', "Je n'ai aucune idée comment ce marchand arrive à avoir autant de munitions.",
                         False)
            if not self.alr_interacted:
                if RPG.p1.fer >= 1:
                    RPG.text_box('Forgeron', "D'ailleurs, je vois que tu a du fer, je vais prendre tout ton stock.", False)
                    RPG.text_box('Forgeron', "Un fer pour 30 louis, ça te va non ?", False)
                    RPG.p1.money += RPG.p1.fer*30
                    RPG.p1.fer = 0
                    RPG.text_box('-', "L'échange a été réalisé avec succès !", False)
                    self.alr_interacted = True
                else:
                    RPG.text_box('Forgeron', "D'ailleurs, je t'acheterai bien un peu de fer, reviens me voir quand tu en auras.", False)
            else:
                RPG.text_box('Forgeron', "Et non désolé, je n'ai plus d'argent pour acheter ton fer.", False)

        elif RPG.current_level == "2":
            RPG.text_box('Forgeron',
                         "Ils sont très nombreux, je te souhaite la meilleure des chances, tout le monde compte sur toi.")
            RPG.text_box('Forgeron',
                         "C'est la dernière bataille et la bataille ultime qui décidera le futur de nos enfants.",
                         False)
            if not self.alr_interacted:
                self.alr_interacted = True
                RPG.text_box('Forgeron', "Tiens quelques balles pour t'encourager", False)
                RPG.p1.munitions += 12
                RPG.text_box('-', "Vous avez reçu 12 munitions !", False)


class Marchand(pygame.sprite.Sprite):
    def __init__(self, RPG, x, y):
        # ================== INITIALIZATION ================== #
        super(Marchand, self).__init__()
        self.index = 0
        self.x = x
        self.y = y
        self.velocity = 2
        self.can_interact = True
        # ================== ANIMATION ================== #
        self.images = []
        self.images.append(pygame.image.load(os.path.join('Assets', 'BasicNPCS', 'vendeur1.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'BasicNPCS', 'vendeur1.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'BasicNPCS', 'vendeur1.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'BasicNPCS', 'vendeur2.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'BasicNPCS', 'vendeur2.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'BasicNPCS', 'vendeur2.png')))
        # Sprite stuff
        self.rect = self.images[0].get_rect()
        self.rect.topleft = self.x, self.y

        self.alr_interacted = False

    def animate(self):
        if self.index >= len(self.images):
            self.index = 0
        RPG.screen.blit(self.images[self.index],
                        (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
        self.index += 1

    def interacted(self):
        if RPG.current_level == '0' and not self.alr_interacted:
            RPG.text_box('Marchand', 'Voici mon magasin, click droit pour vendre, click gauche pour acheter.')
            self.alr_interacted = True
        RPG.click_sound.play()
        RPG.gui = Shop_menu(RPG)


class Religieuse(pygame.sprite.Sprite):
    def __init__(self, RPG, x, y):
        # ================== INITIALIZATION ================== #
        super(Religieuse, self).__init__()
        self.index = 0
        self.x = x
        self.y = y
        self.velocity = 2
        self.can_interact = True
        # ================== ANIMATION ================== #
        self.images = []
        self.images.append(pygame.image.load(os.path.join('Assets', 'BasicNPCS', 'religieuse1.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'BasicNPCS', 'religieuse1.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'BasicNPCS', 'religieuse1.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'BasicNPCS', 'religieuse2.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'BasicNPCS', 'religieuse2.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'BasicNPCS', 'religieuse2.png')))
        # Sprite stuff
        self.rect = self.images[0].get_rect()
        self.rect.topleft = self.x, self.y

        self.alr_interacted = False

    def interacted(self):
        if RPG.current_level == '0':
            RPG.text_box("Religieuse", "Vous devriez rester du côté des Anglais, c'est ce que notre évêque souhaite.")
            RPG.text_box("Religieuse", "Dieu nous protegera.", False)  # RPG.gui = Text_box

        elif RPG.current_level == '1':
            if not self.alr_interacted:
                self.alr_interacted = True
                RPG.text_box('Religieuse', "Je déteste la guerre et le sang, tiens prend ça pour te soigner.")
                RPG.p1.bandage += 2
                RPG.text_box('-', "Vous avez reçu 2 bandages.", False)
            else:
                RPG.text_box('Religieuse', "Suivez les consignes de l'évêque,")
                RPG.text_box('Religieuse', "Dieu nous guidera ...", False)

        elif RPG.current_level == '2':
            RPG.text_box('Religieuse', "L'évêque n'aime pas du tout ce que vous faites.")
            RPG.text_box('Religieuse', "Mais secrètement je vous soutient, les anglais ont dépassés les limites.",
                         False)

    def animate(self):
        if self.index >= len(self.images):
            self.index = 0
        RPG.screen.blit(self.images[self.index],
                        (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
        self.index += 1


class Papineau(pygame.sprite.Sprite):
    def __init__(self, RPG, x, y):
        # ================== INITIALIZATION ================== #
        super(Papineau, self).__init__()
        self.index = 0
        self.x = x
        self.y = y
        self.velocity = 2
        # ================== ANIMATION ================== #
        self.images = []
        self.images.append(pygame.image.load(os.path.join('Assets', 'Papineau', 'Down', 'down1.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'Papineau', 'Down', 'down1.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'Papineau', 'Down', 'down1.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'Papineau', 'Down', 'down2.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'Papineau', 'Down', 'down2.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'Papineau', 'Down', 'down2.png')))
        # Sprite stuff
        self.rect = self.images[0].get_rect()
        self.rect.topleft = self.x, self.y

    def animate(self):
        if self.index >= len(self.images):
            self.index = 0
        RPG.screen.blit(self.images[self.index],
                        (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
        self.index += 1


class Nelson(pygame.sprite.Sprite):
    def __init__(self, RPG, x, y):
        # ================== INITIALIZATION ================== #
        super(Nelson, self).__init__()
        self.index = 0
        self.x = x
        self.y = y
        self.velocity = 2
        # ================== ANIMATION ================== #
        self.images = []
        self.images.append(pygame.image.load(os.path.join('Assets', 'Nelson', 'Down', 'idle1.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'Nelson', 'Down', 'idle1.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'Nelson', 'Down', 'idle1.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'Nelson', 'Down', 'idle2.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'Nelson', 'Down', 'idle2.png')))
        self.images.append(pygame.image.load(os.path.join('Assets', 'Nelson', 'Down', 'idle2.png')))
        # Sprite stuff
        self.rect = self.images[0].get_rect()
        self.rect.topleft = self.x, self.y
        self.can_interact = True

    def animate(self):
        if self.index >= len(self.images):
            self.index = 0
        RPG.screen.blit(self.images[self.index],
                        (self.x - RPG.camera.offset.x, self.y - RPG.camera.offset.y))
        self.index += 1

    def interacted(self):
        if RPG.current_level == '0':
            RPG.text_box('Nelson', "J'en ai assez de rester pacifique et de suivre les plans de Papineau.")
            RPG.text_box('Nelson', "Faisons leur comprendre que nous ne sommes pas ici pour rigoler !!", False)


class Menu:
    def __init__(self, RPG):
        # Load Images
        self.menu_bkg = pygame.image.load((os.path.join('Assets', 'menu_bkg.png')))  # The backgroung image for the menu
        self.jouer_button = []
        self.jouer_button.append(pygame.image.load(os.path.join('Assets', 'Menu', 'jouer1.png')))  # "Jouer"
        self.jouer_button.append(pygame.image.load(os.path.join('Assets', 'Menu', 'jouer2.png')))
        self.options_button = []
        self.options_button.append(pygame.image.load(os.path.join('Assets', 'Menu', 'options1.png')))  # "Options"
        self.options_button.append(pygame.image.load(os.path.join('Assets', 'Menu', 'options2.png')))
        self.credits_button = []
        self.credits_button.append(pygame.image.load(os.path.join('Assets', 'Menu', 'credits1.png')))  # "Crédits"
        self.credits_button.append(pygame.image.load(os.path.join('Assets', 'Menu', 'credits2.png')))
        # Variables
        self.button_y = 160
        self.jouer_button_x = 1
        self.options_button_x = 65
        self.credits_button_x = 129
        # Check if mouse is clicking
        self.is_clicking = False
        self.mode = False

    def main(self):
        if not self.mode:
            RPG.screen.blit(RPG.menu_bkg, (0, 0))  # Replace with backgrouns image later on...
            # Update the position of the buttons's hitboxes
            self.jouer_button_rect = self.jouer_button[0].get_rect(
                topleft=(self.jouer_button_x, self.button_y))  # center=(self.button_x, self.jouer_button_y
            self.options_button_rect = self.options_button[0].get_rect(
                topleft=(self.options_button_x, self.button_y))  #
            # center=(self.button_x, self.options_button_y
            self.credits_button_rect = self.credits_button[0].get_rect(
                topleft=(self.credits_button_x, self.button_y))  # center=(self.button_x, self.credits_button_y

            # Place the menu buttons and check for hover
            if self.jouer_button_rect.collidepoint(pygame.mouse.get_pos()):  # Check for hover on "Jouer"
                RPG.screen.blit(self.jouer_button[1], (self.jouer_button_x, self.button_y))
                if self.is_clicking:
                    RPG.click_sound.play()
                    RPG.playing = True
                    self.is_clicking = False
            else:
                RPG.screen.blit(self.jouer_button[0], (self.jouer_button_x, self.button_y))

            # if pygame.Rect.collidepoint(self.options_button_rect, pygame.mouse.get_pos()):  # Check for hover on "Options"
            #     RPG.screen.blit(self.options_button[1], (self.options_button_x, self.button_y))
            # else:
            #     RPG.screen.blit(self.options_button[0], (self.options_button_x, self.button_y))

            if pygame.Rect.collidepoint(self.credits_button_rect,
                                        pygame.mouse.get_pos()):  # Check for hover on "Crédits"
                RPG.screen.blit(self.credits_button[1], (self.credits_button_x, self.button_y))
                if self.is_clicking:
                    self.mode = "Credits"
                    RPG.click_sound.play()
                    self.is_clicking = False
            else:
                RPG.screen.blit(self.credits_button[0], (self.credits_button_x, self.button_y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit("Quitting")
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.is_clicking = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.is_clicking = False

        if self.mode == "Credits":
            RPG.screen.blit(RPG.endingCredits, (0, 0))

        if self.mode is not False:
            key1 = pygame.key.get_pressed()
            if key1[pygame.K_ESCAPE]:
                self.mode = False


class Shop_menu:
    def __init__(self, RPG):
        # Load Assets
        self.image = pygame.image.load(os.path.join('Assets', 'Shop', 'store.png'))
        self.bandage = pygame.image.load(os.path.join('Assets', 'Shop', 'bandage.png'))
        self.pain = pygame.image.load(os.path.join('Assets', 'Shop', 'pain.png'))
        self.armure = pygame.image.load(os.path.join('Assets', 'Shop', 'armure.png'))
        self.bois = pygame.image.load(os.path.join('Assets', 'Shop', 'bois.png'))
        self.munition = pygame.image.load(os.path.join('Assets', 'Shop', 'munition.png'))
        self.hache2 = pygame.image.load(os.path.join('Assets', 'Shop', 'hache2.png'))
        self.hache3 = pygame.image.load(os.path.join('Assets', 'Shop', 'hache3.png'))
        self.arquebus2 = pygame.image.load(os.path.join('Assets', 'Shop', 'arquebus2.png'))
        # Sounds
        self.buy_sound = pygame.mixer.Sound(os.path.join('Assets', 'Sounds', 'buy.mp3'))
        self.sell_sound = pygame.mixer.Sound(os.path.join('Assets', 'Sounds', 'sell.mp3'))
        self.fail_sound = pygame.mixer.Sound(os.path.join('Assets', 'Sounds', 'error.mp3'))
        # Font
        self.font = pygame.font.Font((os.path.join('Assets', 'font.ttf')), 5)

        self.buystore = pygame.image.load(os.path.join('Assets', 'Shop', 'buystore.png'))
        # Transparent bckg
        self.bkg = pygame.Surface((RPG.W_WIDTH, RPG.W_HEIGHT))
        self.bkg.set_alpha(128)
        self.bkg.fill((0, 0, 0))

        self.is_buying = False
        self.is_selling = False

    def animate(self):
        RPG.screen.blit(self.bkg, (0, 0))
        RPG.screen.blit(self.image, (
        RPG.W_WIDTH / 2 - self.image.get_rect().width / 2, RPG.W_HEIGHT / 2 - self.image.get_rect().height / 2))

        # Hover Effect
        if pygame.Rect(70, 50, 24, 11).collidepoint(pygame.mouse.get_pos()):
            if self.is_buying:
                if RPG.p1.money >= Bandage().price:
                    RPG.p1.money -= Bandage().price
                    RPG.p1.bandage += 1
                    self.buy_sound.play()
                else:
                    self.fail_sound.play()
                self.is_buying = False
            elif self.is_selling:
                if RPG.p1.bandage >= 1:
                    RPG.p1.money += int(Bandage().price / 2)
                    RPG.p1.bandage -= 1
                    self.sell_sound.play()
                else:
                    self.fail_sound.play()
                self.is_selling = False
            else:
                RPG.screen.blit(self.buystore, (70, 50))  # 24x11
        elif pygame.Rect(70, 75, 24, 11).collidepoint(pygame.mouse.get_pos()):
            if self.is_buying:
                if RPG.p1.money >= Bois().price:
                    RPG.p1.money -= Bois().price
                    RPG.p1.bois += 1
                    self.buy_sound.play()
                else:
                    self.fail_sound.play()
                self.is_buying = False
            elif self.is_selling:
                if RPG.p1.bois >= 1:
                    RPG.p1.money += int(Bois().price / 2)
                    RPG.p1.bois -= 1
                    self.sell_sound.play()
                else:
                    self.fail_sound.play()
                self.is_selling = False
            else:
                RPG.screen.blit(self.buystore, (70, 75))  # 24x11
        elif pygame.Rect(69, 100, 24, 11).collidepoint(pygame.mouse.get_pos()):
            if self.is_buying:
                if RPG.p1.money >= Armure().price:
                    RPG.p1.money -= Armure().price
                    RPG.p1.armure += 1
                    if RPG.p1.hp - Armure().hp == RPG.p1.max_health:
                        RPG.p1.hp = RPG.p1.max_health + Armure().hp
                    self.buy_sound.play()
                else:
                    self.fail_sound.play()
                self.is_buying = False
            elif self.is_selling:
                if RPG.p1.armure >= 1:
                    RPG.p1.money += int(Armure().price / 3)
                    RPG.p1.armure -= 1
                    self.sell_sound.play()
                else:
                    self.fail_sound.play()
                self.is_selling = False
            else:
                RPG.screen.blit(self.buystore, (69, 100))  # 24x11
        elif pygame.Rect(69, 125, 24, 11).collidepoint(pygame.mouse.get_pos()):
            if self.is_buying:
                if RPG.p1.money >= Axe1().price and RPG.p1.current_axe != 'Axe1' and RPG.p1.current_axe != 'Axe2':
                    RPG.p1.money -= Axe1().price
                    RPG.p1.axe = Axe1()
                    RPG.p1.current_axe = 'Axe1'
                    self.buy_sound.play()
                else:
                    self.fail_sound.play()
                self.is_buying = False
            elif self.is_selling:
                if RPG.p1.current_axe == 'Axe1':
                    RPG.p1.money += int(Axe1().price / 3)
                    RPG.p1.axe = Axe0()
                    RPG.p1.current_axe = 'Axe0'
                    self.sell_sound.play()
                else:
                    self.fail_sound.play()
                self.is_selling = False
            else:
                RPG.screen.blit(self.buystore, (69, 125))  # 24x11

        elif pygame.Rect(121, 50, 24, 11).collidepoint(pygame.mouse.get_pos()):
            if self.is_buying:
                if RPG.p1.money >= Pain().price:
                    RPG.p1.money -= Pain().price
                    RPG.p1.pain += 1
                    self.buy_sound.play()
                else:
                    self.fail_sound.play()
                self.is_buying = False
            elif self.is_selling:
                if RPG.p1.pain >= 1:
                    RPG.p1.money += int(Pain().price / 2)
                    RPG.p1.pain -= 1
                    self.sell_sound.play()
                else:
                    self.fail_sound.play()
                self.is_selling = False
            else:
                RPG.screen.blit(self.buystore, (121, 50))  # 24x11
        elif pygame.Rect(121, 75, 24, 11).collidepoint(pygame.mouse.get_pos()):
            if self.is_buying:
                if RPG.p1.money >= Munitions().price:
                    RPG.p1.money -= Munitions().price
                    RPG.p1.munitions += Munitions().number
                    self.buy_sound.play()
                else:
                    self.fail_sound.play()
                self.is_buying = False
            elif self.is_selling:
                if RPG.p1.munitions >= 1:
                    RPG.p1.money += int(Munitions().sell_price)
                    RPG.p1.munitions -= 1
                    self.sell_sound.play()
                else:
                    self.fail_sound.play()
                self.is_selling = False
            else:
                RPG.screen.blit(self.buystore, (121, 75))  # 24x11
        elif pygame.Rect(120, 100, 24, 11).collidepoint(pygame.mouse.get_pos()):
            if self.is_buying:
                if RPG.p1.money >= Arquebus1().price and RPG.p1.current_arquebus != 'Arquebus1':
                    RPG.p1.money -= Arquebus1().price
                    RPG.p1.arquebus = Arquebus1()
                    RPG.p1.current_arquebus = 'Arquebus1'
                    self.buy_sound.play()
                else:
                    self.fail_sound.play()
                self.is_buying = False
            elif self.is_selling:
                if RPG.p1.current_arquebus == 'Arquebus1':
                    RPG.p1.money += int(Arquebus1().price / 2)
                    RPG.p1.arquebus = Arquebus0()
                    RPG.p1.current_arquebus = 'Arquebus0'
                    self.sell_sound.play()
                else:
                    self.fail_sound.play()
                self.is_selling = False
            else:
                RPG.screen.blit(self.buystore, (120, 100))  # 24x11
        elif pygame.Rect(120, 125, 24, 11).collidepoint(pygame.mouse.get_pos()):
            if self.is_buying:
                if RPG.p1.money >= Axe2().price and RPG.p1.current_axe != 'Axe2':
                    RPG.p1.money -= Axe2().price
                    RPG.p1.axe = Axe2()
                    RPG.p1.current_axe = 'Axe2'
                    self.buy_sound.play()
                else:
                    self.fail_sound.play()
                self.is_buying = False
            elif self.is_selling:
                if RPG.p1.current_axe == 'Axe2':
                    RPG.p1.money += int(Axe2().price / 3)
                    RPG.p1.axe = Axe0()
                    RPG.p1.current_axe = 'Axe0'
                    self.sell_sound.play()
                else:
                    self.fail_sound.play()
                self.is_selling = False
            else:
                RPG.screen.blit(self.buystore, (120, 125))  # 24x11

        # Blit items
        RPG.screen.blit(self.bandage, (50, 50))
        RPG.screen.blit(self.bois, (50, 75))
        RPG.screen.blit(self.armure, (50, 100))
        RPG.screen.blit(self.hache2, (50, 125))

        RPG.screen.blit(self.pain, (100, 50))
        RPG.screen.blit(self.munition, (100, 75))
        RPG.screen.blit(self.arquebus2, (100, 100))
        RPG.screen.blit(self.hache3, (100, 125))

        RPG.screen.blit(self.font.render(str(RPG.p1.bandage), True, (0, 0, 0)),
                        (66 - 3 - 2 * len(str(RPG.p1.bandage)), 66 - 6))
        RPG.screen.blit(self.font.render(str(RPG.p1.pain), True, (0, 0, 0)),
                        (117 - 3 - 2 * len(str(RPG.p1.pain)), 66 - 6))
        RPG.screen.blit(self.font.render(str(RPG.p1.bois), True, (0, 0, 0)),
                        (66 - 3 - 2 * len(str(RPG.p1.bois)), 91 - 6))
        RPG.screen.blit(self.font.render(str(RPG.p1.munitions), True, (0, 0, 0)),
                        (117 - 3 - 2 * len(str(RPG.p1.munitions)), 91 - 6))

        # line_1_text = self.gameFontBody.render(wrappedtext[0], True, text_color)  # Creates the text object
        # self.screen.blit(line_1_text, (3, 139))  # Displays the text object

        price1_font = self.font.render(str(Bandage().price), True, (0, 0, 0))
        price2_font = self.font.render(str(Bois().price), True, (0, 0, 0))
        price3_font = self.font.render(str(Armure().price), True, (0, 0, 0))
        price4_font = self.font.render(str(Axe1().price), True, (0, 0, 0))
        price5_font = self.font.render(str(Pain().price), True, (0, 0, 0))
        price6_font = self.font.render(str(Munitions().price), True, (0, 0, 0))
        price7_font = self.font.render(str(Arquebus1().price), True, (0, 0, 0))
        price8_font = self.font.render(str(Axe2().price), True, (0, 0, 0))

        RPG.screen.blit(price1_font, (70 + 4, 50 + 2))
        RPG.screen.blit(price2_font, (70 + 4, 75 + 2))
        RPG.screen.blit(price3_font, (69 + 4, 100 + 2))
        RPG.screen.blit(price4_font, (69 + 4, 125 + 2))
        RPG.screen.blit(price5_font, (121 + 4, 50 + 2))
        RPG.screen.blit(price6_font, (121 + 4, 75 + 2))
        RPG.screen.blit(price7_font, (120 + 4, 100 + 2))
        RPG.screen.blit(price8_font, (120 + 4, 125 + 2))

        # Display Current Money
        c_m_f = self.font.render("Louis : " + str(RPG.p1.money), True, (0, 0, 0))
        RPG.screen.blit(c_m_f, (RPG.W_WIDTH / 2 - c_m_f.get_rect().width / 2, 144))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.is_buying = True
                elif event.button == 3:
                    self.is_selling = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.is_buying = False
                elif event.button == 3:
                    self.is_selling = False
            elif event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                pygame.quit()
                sys.exit("Quitting")


class Inventory:
    def __init__(self, RPG):
        self.image = pygame.image.load(os.path.join('Assets', 'Inventory', 'inventory.png'))
        self.bandage = pygame.image.load(os.path.join('Assets', 'Shop', 'bandage.png'))
        self.pain = pygame.image.load(os.path.join('Assets', 'Shop', 'pain.png'))
        self.fer = pygame.image.load(os.path.join('Assets', 'Inventory', 'fer.png'))
        self.bois = pygame.image.load(os.path.join('Assets', 'Shop', 'bois.png'))
        self.munition = pygame.image.load(os.path.join('Assets', 'Shop', 'munition.png'))
        self.overlay = pygame.image.load(os.path.join('Assets', 'Inventory', 'inventory_overlay.png'))
        # BKG
        self.bkg = pygame.Surface((RPG.W_WIDTH, RPG.W_HEIGHT))
        self.bkg.set_alpha(128)
        self.bkg.fill((0, 0, 0))
        # Font
        self.font = pygame.font.Font((os.path.join('Assets', 'font.ttf')), 5)
        # Clicking Management
        self.is_clicking = False

    def animate(self):
        RPG.screen.blit(self.bkg, (0, 0))
        RPG.screen.blit(self.image, (
        RPG.W_WIDTH / 2 - self.image.get_rect().width / 2, RPG.W_HEIGHT / 2 - self.image.get_rect().height / 2))

        health_font = self.font.render(str(RPG.p1.hp), True, (0, 0, 0))
        RPG.screen.blit(health_font, (153, 64 + 3))

        attack_font = self.font.render(str(RPG.p1.axe.damage), True, (0, 0, 0))
        RPG.screen.blit(attack_font, (159 - 2 * len(str(RPG.p1.axe.damage)), 87 + 3))

        money_font = self.font.render(str(RPG.p1.money), True, (0, 0, 0))
        RPG.screen.blit(money_font, (160 - 2 * len(str(RPG.p1.money)), 109 + 3))

        if pygame.Rect(31, 84, 20, 20).collidepoint(pygame.mouse.get_pos()):
            RPG.screen.blit(self.overlay, (31, 84))
            if self.is_clicking and RPG.p1.hp < RPG.p1.max_health and RPG.p1.bandage >= 1:
                RPG.click_sound.play()
                RPG.p1.heal('bandage')
                self.is_clicking = False
            elif self.is_clicking:
                RPG.fail_sound.play()
                self.is_clicking = False

        elif pygame.Rect(56, 84, 20, 20).collidepoint(pygame.mouse.get_pos()):
            RPG.screen.blit(self.overlay, (56, 84))
            if self.is_clicking and RPG.p1.hp < RPG.p1.max_health and RPG.p1.pain >= 1:
                RPG.click_sound.play()
                RPG.p1.heal('pain')
                self.is_clicking = False
            elif self.is_clicking:
                RPG.fail_sound.play()
                self.is_clicking = False

        RPG.screen.blit(RPG.p1.axe.image, (45, 55))
        RPG.screen.blit(RPG.p1.arquebus.image, (70, 55))

        RPG.screen.blit(self.bandage, (33, 86))
        RPG.screen.blit(self.font.render(str(RPG.p1.bandage), True, (0, 0, 0)),
                        (49 - 3 - 2 * len(str(RPG.p1.bandage)), 102 - 6))

        RPG.screen.blit(self.pain, (57, 86))
        RPG.screen.blit(self.font.render(str(RPG.p1.pain), True, (0, 0, 0)),
                        (74 - 3 - 2 * len(str(RPG.p1.pain)), 102 - 6))

        RPG.screen.blit(self.bois, (82, 86))
        RPG.screen.blit(self.font.render(str(RPG.p1.bois), True, (0, 0, 0)),
                        (98 - 3 - 2 * len(str(RPG.p1.bois)), 102 - 6))

        RPG.screen.blit(self.munition, (33, 108))
        RPG.screen.blit(self.font.render(str(RPG.p1.munitions), True, (0, 0, 0)),
                        (49 - 3 - 2 * len(str(RPG.p1.munitions)), 125 - 6))

        RPG.screen.blit(self.fer, (58, 109))
        RPG.screen.blit(self.font.render(str(RPG.p1.fer), True, (0, 0, 0)),
                        (74 - 3 - 2 * len(str(RPG.p1.fer)), 125 - 6))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit("Quitting")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.is_clicking = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.is_clicking = False


class Axe0:
    def __init__(self):
        self.image = pygame.image.load(os.path.join('Assets', 'Inventory', 'hache.png'))
        self.damage = 10
        self.reload_time = 5
        self.speed = 4


class Axe1:
    def __init__(self):
        self.image = pygame.image.load(os.path.join('Assets', 'Shop', 'hache2.png'))
        self.damage = 20
        self.reload_time = 7
        self.price = 60
        self.speed = 4


class Axe2:
    def __init__(self):
        self.image = pygame.image.load(os.path.join('Assets', 'Shop', 'hache3.png'))
        self.damage = 20
        self.reload_time = 3
        self.price = 150
        self.speed = 6


class Arquebus0:
    def __init__(self):
        self.image = pygame.image.load(os.path.join('Assets', 'Inventory', 'arquebus.png'))
        self.damage = 15
        self.reload_time = 20
        self.range = 40


class Arquebus1:
    def __init__(self):
        self.image = pygame.image.load(os.path.join('Assets', 'Shop', 'arquebus2.png'))
        self.damage = 20
        self.reload_time = 10
        self.price = 250
        self.range = 70


class Bandage:
    def __init__(self):
        self.price = 9
        self.heal = 10


class Pain:
    def __init__(self):
        self.price = 3
        self.heal = 5


class Munitions:
    def __init__(self):
        self.price = 15
        self.number = 6
        self.sell_price = 2


class Bois:
    def __init__(self):
        self.price = 2

class Horse:
    def __init__(self):
        self.price = 210
        self.speed = 8


class Armure:
    def __init__(self):
        self.price = 50
        self.hp = 10


class LevelIntro:
    def __init__(self, RPG):
        self.image = pygame.image.load((os.path.join('Assets', 'grass.png')))
        self.MAP_WIDTH = self.image.get_rect().width
        self.MAP_HEIGHT = self.image.get_rect().height
        self.obstacles = []
        self.npcs = []
        self.ennemies = []
        self.spawnpoint_x = 708
        self.spawnpoint_y = 196
        self.npcs.append(Papineau(self, 96, 48))
        self.npcs.append(Nelson(self, 112, 48))

        self.npcs.append(Patriote(self, 0, 82))
        self.npcs.append(Jean(self, 16, 82))
        self.npcs.append(Roger(self, 32, 82))
        self.npcs.append(Patriote(self, 48, 82))
        self.npcs.append(Jean(self, 64, 82))
        self.npcs.append(Roger(self, 80, 82))
        self.npcs.append(Patriote(self, 96, 82))
        self.npcs.append(Jean(self, 112, 82))
        self.npcs.append(Roger(self, 128, 82))
        self.npcs.append(Patriote(self, 144, 82))
        self.npcs.append(Jean(self, 160, 82))
        self.npcs.append(Roger(self, 176, 82))

        self.npcs.append(Patriote(self, 0, 98))
        self.npcs.append(Jean(self, 16, 98))
        self.npcs.append(Roger(self, 32, 98))
        self.npcs.append(Patriote(self, 48, 98))
        self.npcs.append(Jean(self, 64, 98))
        self.npcs.append(Roger(self, 80, 98))
        self.npcs.append(Patriote(self, 96, 98))
        self.npcs.append(Jean(self, 112, 98))
        self.npcs.append(Roger(self, 128, 98))
        self.npcs.append(Patriote(self, 144, 98))
        self.npcs.append(Jean(self, 160, 98))
        self.npcs.append(Roger(self, 176, 98))

        self.npcs.append(Patriote(self, 0, 114))
        self.npcs.append(Jean(self, 16, 114))
        self.npcs.append(Roger(self, 32, 114))
        self.npcs.append(Patriote(self, 48, 114))
        self.npcs.append(Jean(self, 64, 114))
        self.npcs.append(Roger(self, 80, 114))
        self.npcs.append(Patriote(self, 96, 114))
        self.npcs.append(Jean(self, 112, 114))
        self.npcs.append(Roger(self, 128, 114))
        self.npcs.append(Patriote(self, 144, 114))
        self.npcs.append(Jean(self, 160, 114))
        self.npcs.append(Roger(self, 176, 114))

        self.npcs.append(Patriote(self, 0, 130))
        self.npcs.append(Jean(self, 16, 130))
        self.npcs.append(Roger(self, 32, 130))
        self.npcs.append(Patriote(self, 48, 130))
        self.npcs.append(Jean(self, 64, 130))
        self.npcs.append(Roger(self, 80, 130))
        self.npcs.append(Patriote(self, 96, 130))
        self.npcs.append(Jean(self, 112, 130))
        self.npcs.append(Roger(self, 128, 130))
        self.npcs.append(Patriote(self, 144, 130))
        self.npcs.append(Jean(self, 160, 130))
        self.npcs.append(Roger(self, 176, 130))

        self.npcs.append(Patriote(self, 0, 146))
        self.npcs.append(Jean(self, 16, 146))
        self.npcs.append(Roger(self, 32, 146))
        self.npcs.append(Patriote(self, 48, 146))
        self.npcs.append(Jean(self, 64, 146))
        self.npcs.append(Roger(self, 80, 146))
        self.npcs.append(Patriote(self, 96, 146))
        self.npcs.append(Jean(self, 112, 146))
        self.npcs.append(Roger(self, 128, 146))
        self.npcs.append(Patriote(self, 144, 146))
        self.npcs.append(Jean(self, 160, 146))
        self.npcs.append(Roger(self, 176, 146))

        self.npcs.append(Patriote(self, 0, 162))
        self.npcs.append(Jean(self, 16, 162))
        self.npcs.append(Roger(self, 32, 162))
        self.npcs.append(Patriote(self, 48, 162))
        self.npcs.append(Jean(self, 64, 162))
        self.npcs.append(Roger(self, 80, 162))
        self.npcs.append(Patriote(self, 96, 162))
        self.npcs.append(Jean(self, 112, 162))
        self.npcs.append(Roger(self, 128, 162))
        self.npcs.append(Patriote(self, 144, 162))
        self.npcs.append(Jean(self, 160, 162))
        self.npcs.append(Roger(self, 176, 162))

        self.npcs.append(Patriote(self, 0, 178))
        self.npcs.append(Jean(self, 16, 178))
        self.npcs.append(Roger(self, 32, 178))
        self.npcs.append(Patriote(self, 48, 178))
        self.npcs.append(Jean(self, 64, 178))
        self.npcs.append(Roger(self, 80, 178))
        self.npcs.append(Patriote(self, 96, 178))
        self.npcs.append(Jean(self, 112, 178))
        self.npcs.append(Roger(self, 128, 178))
        self.npcs.append(Patriote(self, 144, 178))
        self.npcs.append(Jean(self, 160, 178))
        self.npcs.append(Roger(self, 176, 178))

    def animate(self):
        RPG.p1.can_move = False
        for npc in self.npcs:
            npc.direction = 'up'
            npc.animate()

        RPG.text_box("Papineau", "Aujourd'hui, nous avons reçu les résolutions et ils ont tout refusé!", False)
        RPG.text_box("Papineau",
                     "Pour protester nous allons boycotter les produits anglais! Achetez des produits locaux, ", False)
        RPG.text_box("Papineau", "envoyez des pétitions, et n'oubliez pas de ...", False)
        RPG.text_box("Nelson", "Non !", False)
        RPG.text_box("Nelson", "Citoyens, nous allons nous battre pour nos droits en tant que canadiens français !", False)
        RPG.text_box("Adam (Patriote parmis la foule)", "AUX ARMES CITOYENS !", False)
        RPG.level = Level0(RPG)
        RPG.p1.x = 708
        RPG.p1.y = 196
        RPG.p1.can_move = True
        # pygame.display.update()
        # pygame.event.clear()
        # while True:
        #     event = pygame.event.wait()
        #     if event.type == pygame.QUIT:
        #         self.running = False
        #         self.playing = False
        #         pygame.quit()
        #         sys.exit("Quitting")
        #
        #     elif event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
        #             break


class Level0:
    # Quick description of the level :
    # But : Tuer tous les anglais + Tutoriel
    def __init__(self, RPG):
        self.image = pygame.image.load((os.path.join('Assets', 'Levels', 'level0.png')))
        self.MAP_WIDTH = self.image.get_rect().width
        self.MAP_HEIGHT = self.image.get_rect().height
        self.obstacles = []
        self.npcs = []
        self.ennemies = []
        self.spawnpoint_x = 708
        self.spawnpoint_y = 196

        RPG.current_level = '0'
        # Creating Obstacles
        # Basic obstacles
        self.obstacles.append(pygame.Rect(-1, -1, self.MAP_WIDTH + 2, 1))
        self.obstacles.append(pygame.Rect(-1, self.MAP_HEIGHT + 1, self.MAP_WIDTH + 2, 1))
        self.obstacles.append(pygame.Rect(self.MAP_WIDTH + 1, -1, 1, self.MAP_HEIGHT + 2))
        self.obstacles.append(pygame.Rect(-1, -1, 1, self.MAP_HEIGHT + 2))
        # Obstacles
        self.obstacles.append(pygame.Rect(697, 1, 28, 184))
        self.obstacles.append(pygame.Rect(305, 221, 420, 128))
        self.obstacles.append(pygame.Rect(565 + 20, 1, 673 - 593, 201 - 18))
        self.obstacles.append(pygame.Rect(417, 1, 557 - 417, 76))
        self.obstacles.append(pygame.Rect(417, 77, 557 - 421, 185 - 77))
        self.obstacles.append(pygame.Rect(309, 1, 417 - 309, 85 - 1))
        self.obstacles.append(pygame.Rect(309, 1, 4, 184))
        self.obstacles.append(pygame.Rect(276, 152, 308 - 276, 180 - 152))
        self.obstacles.append(pygame.Rect(193, 1, 309 - 193, 84))
        self.obstacles.append(pygame.Rect(1, 1, 191, 92))
        self.obstacles.append(pygame.Rect(408, 212, 476 - 408, 220 - 212))
        self.obstacles.append(pygame.Rect(356, 120, 416 - 340, 200 - 136))
        self.obstacles.append(pygame.Rect(380, 92, 416 - 364, 120 - 92))
        self.obstacles.append(pygame.Rect(0, 96, 116, 184 - 96))
        self.obstacles.append(pygame.Rect(0, 212, 76, 220 - 212))
        self.obstacles.append(pygame.Rect(76, 220, 212 - 76, 348 - 220))
        self.obstacles.append(pygame.Rect(268 + 16, 256, 304 - 268, 312 - 256))
        self.obstacles.append(pygame.Rect(256, 284, 304 - 256, 312 - 284))
        self.obstacles.append(pygame.Rect(196, 304, 304 - 196, 348 - 304))
        self.obstacles.append(pygame.Rect(160, 208, 168 - 160, 220 - 208))
        # Dialog
        self.joseph1_1 = "Soldats! Nous sommes à St-Denis et nous devons éliminer les anglais. Ils sont plus nombreux et"
        self.joseph1_2 = "sont mieux armés, mais si nous avons la volonté de vaincre, nous vaincrons."
        self.joseph2_1 = "Tiens, prends ton arme, soldat, tu seras l'une des 109 personnes à avoir un fusil,"
        self.joseph2_2 = "prend tes 6 cartouches, c'est tout ce que nous avons."
        self.joseph3_1 = "Chaque anglais tué te rapportera des ressource que tu pourras utiliser pour"
        self.joseph3_2 = "acheter ou vendre des objets dans la boutique."
        self.joseph4 = "CHARGEONS!"
        self.joseph5 = "JE SAVAIS QUE TU POUVAIS LE FAIRE ! VICTOIRE !"
        # NPCS
        self.forgeron = Forgeron(RPG, 352, 92 - 12)
        self.marchand = Marchand(RPG, 616, 188 - 12)
        self.religieuse = Religieuse(RPG, 376, 184 - 8)
        self.jean = Jean(RPG, 570, 91)
        self.roger = Roger(RPG, 478, 181)
        # HITBOXES
        self.obstacles.append(
            pygame.Rect(self.jean.x + 6, self.jean.y, self.jean.rect.width - 12, self.jean.rect.height - 8))
        self.obstacles.append(
            pygame.Rect(self.roger.x + 6, self.roger.y, self.roger.rect.width - 12, self.roger.rect.height - 8))
        # self.obstacles.append(pygame.Rect(436 + 6, 188, 16 - 12, self.roger.rect.height-8))
        self.obstacles.append(pygame.Rect(676, 168, 16, 16))

        self.npcs.append(Nelson(RPG, 676, 168))
        # self.npcs.append(Patriote(RPG, 676, 144))
        self.npcs.append(Patriote(RPG, 668, 144))
        self.npcs.append(Patriote(RPG, 680, 144))

        self.npcs.append(Patriote(RPG, 436, 188 - 16))
        self.npcs.append(self.forgeron)
        self.npcs.append(self.marchand)
        self.npcs.append(self.religieuse)
        self.npcs.append(self.jean)
        self.npcs.append(self.roger)
        self.ennemies.append(Brit(RPG, 115, 104, self))
        self.ennemies.append(Brit(RPG, 137, 104, self))
        self.ennemies.append(Brit(RPG, 161, 103, self))
        self.ennemies.append(Brit(RPG, 137, 120, self))
        self.ennemies.append(Brit(RPG, 209, 201, self))
        self.ennemies.append(Brit(RPG, 208, 226, self))
        self.ennemies.append(Brit(RPG, 156, 128, self))
        self.ennemies.append(Brit(RPG, 192, 152, self))
        self.ennemies.append(Brit(RPG, 144, 172, self))
        self.ennemies.append(Brit(RPG, 220, 160, self))
        self.ennemies.append(Brit(RPG, 284, 116, self))
        self.ennemies.append(Brit(RPG, 248, 252, self))
        self.ennemies.append(Brit(RPG, 228, 276, self))

        # self.ennemies.append(Brit(RPG, self.spawnpoint_x, self.spawnpoint_y, self))
        self.alr_init = 0

    def animate(self):

        if self.alr_init == 0:
            self.alr_init += 1

        elif self.alr_init == 1:
            self.alr_init += 1
            RPG.text_box('Nelson', self.joseph1_1)
            RPG.text_box('Nelson', self.joseph1_2, False)
            RPG.text_box('Nelson', self.joseph2_1, False)
            RPG.text_box('Nelson', self.joseph2_2, False)
            RPG.text_box('Nelson', self.joseph3_1, False)
            RPG.text_box('Nelson', self.joseph3_2, False)
            RPG.text_box('Nelson', self.joseph4, False)
            RPG.text_box('Nelson', "Et n'oublie pas, parle aux autres, ils te donneront des informations importante !",
                         False)
            RPG.text_box('-', "Flèches pour bouger, Z pour la hache, X pour l'arquebuse, F pour intéragir avec les autres.")

        for npc in self.npcs:
            npc.animate()
        for i in self.ennemies:
            i.animate()
        if self.ennemies == []:
            RPG.text_box('Nelson', self.joseph5)
            RPG.level = Level1(RPG)
            RPG.p1.x = 0
            RPG.p1.y = 252
            RPG.screen.blit(RPG.txt1, (0, 0))
            pygame.display.update()
            pygame.event.clear()
            while True:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    self.running = False
                    self.playing = False
                    pygame.quit()
                    sys.exit("Quitting")

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        break


class Level1:
    # Quick description of the level :
    # But : Tuer tous les anglais + Tutoriel
    def __init__(self, RPG):
        self.image = pygame.image.load((os.path.join('Assets', 'Levels', 'level1.png')))
        self.MAP_WIDTH = self.image.get_rect().width
        self.MAP_HEIGHT = self.image.get_rect().height
        self.obstacles = []
        self.npcs = []
        self.ennemies = []
        self.spawnpoint_x = 0
        self.spawnpoint_y = 252

        RPG.current_level = '1'
        # Creating Obstacles
        # Basic obstacles
        self.obstacles.append(pygame.Rect(-1, -1, self.MAP_WIDTH + 2, 1))
        self.obstacles.append(pygame.Rect(-1, self.MAP_HEIGHT + 1, self.MAP_WIDTH + 2, 1))
        self.obstacles.append(pygame.Rect(self.MAP_WIDTH + 1, -1, 1, self.MAP_HEIGHT + 2))
        self.obstacles.append(pygame.Rect(-1, -1, 1, self.MAP_HEIGHT + 2))
        # Obstacles
        self.obstacles.append(pygame.Rect(0, 276, 848, 380 - 276))
        self.obstacles.append(pygame.Rect(0, 168, 48, 184 - 168))
        self.obstacles.append(pygame.Rect(48, 0, 176 - 40, 186 - 16))
        self.obstacles.append(pygame.Rect(76 + 16, 172, 160 - 84, 232 - 172))
        self.obstacles.append(pygame.Rect(189, 0, 260 - 184 - 16, 240))
        self.obstacles.append(pygame.Rect(252, 0, 452 - 252, 88))
        self.obstacles.append(pygame.Rect(284, 124, 428 - 284 - 8, 240 - 124))
        self.obstacles.append(pygame.Rect(460, 52, 8, 88 - 52))
        self.obstacles.append(pygame.Rect(468, 88, 472 - 468, 236 - 88))
        self.obstacles.append(pygame.Rect(472, 212, 512 - 472 - 12, 244 - 212 - 8))
        self.obstacles.append(pygame.Rect(836, 0, 848 - 836, 236))
        self.obstacles.append(pygame.Rect(784, 0, 836 - 784, 132))
        self.obstacles.append(pygame.Rect(468, 4, 784 - 468, 80 - 4))
        self.obstacles.append(pygame.Rect(724, 104, 736 - 724, 8))
        self.obstacles.append(pygame.Rect(472, 112, 524 - 472 - 16, 132 - 112))
        self.obstacles.append(pygame.Rect(556, 100, 568 - 556, 8))
        self.obstacles.append(pygame.Rect(472, 80, 540 - 472 - 16, 96 - 80))
        self.obstacles.append(pygame.Rect(632, 96, 660 - 632, 104 - 96))
        # Dialog
        self.joseph6_1 = "Protégez le village, nous allons établir le quartier général des patriotes, pour protéger le"
        self.joseph6_2 = "village des anglais qui arrivent."
        self.joseph7 = "Je vous confie la mission de nous sortir de ce siège en passant la ligne anglaise."
        self.joseph8_1 = "Échappez-vous et allez reporter ça aux autres chefs patriotes pour organiser une autre"
        self.joseph8_2 = "bataille."
        # NPCS
        self.forgeron = Forgeron(RPG, 28, 184 - 8)
        self.marchand = Marchand(RPG, 120, 240 - 8)
        self.religieuse = Religieuse(RPG, 384, 240 - 8)
        self.jean = Jean(RPG, 68, 228)
        self.roger = Roger(RPG, 252, 224)
        # NPCS HITBOX WHEN NECESSARY
        self.obstacles.append(
            pygame.Rect(self.marchand.x + 6, self.marchand.y, self.marchand.images[0].get_rect().width - 12,
                        self.marchand.images[0].get_rect().height - 8))
        self.obstacles.append(
            pygame.Rect(self.jean.x + 6, self.jean.y, self.jean.rect.width - 12, self.jean.rect.height - 8))
        self.obstacles.append(
            pygame.Rect(self.roger.x + 6, self.roger.y, self.roger.rect.width - 12, self.roger.rect.height - 8))
        self.obstacles.append(pygame.Rect(4 + 6, 232, 16 - 12, 16 - 8))

        self.npcs.append(Red(RPG, 4, 232))
        self.npcs.append(Patriote(RPG, 216, 244-16))
        self.npcs.append(self.forgeron)
        self.npcs.append(self.marchand)
        self.npcs.append(self.religieuse)
        self.npcs.append(self.jean)
        self.npcs.append(self.roger)

        self.ennemies.append(Brit(RPG, 624, 196, self))
        self.ennemies.append(Brit(RPG, 592, 112, self))
        self.ennemies.append(Brit(RPG, 516, 124, self))
        self.ennemies.append(Brit(RPG, 684, 108, self))
        self.ennemies.append(Brit(RPG, 776, 160, self))
        self.ennemies.append(Brit(RPG, 696, 208, self))
        self.ennemies.append(Brit(RPG, 672, 268, self))

        self.ennemies.append(Brit(RPG, 512, 172, self))
        self.ennemies.append(Brit(RPG, 512, 220, self))
        self.ennemies.append(Brit(RPG, 672, 172, self))
        self.ennemies.append(Brit(RPG, 576, 220, self))
        self.ennemies.append(Brit(RPG, 640, 124, self))
        self.ennemies.append(Brit(RPG, 736, 172, self))
        self.ennemies.append(Brit(RPG, 544, 188, self))
        self.ennemies.append(Brit(RPG, 768, 252, self))
        self.ennemies.append(Brit(RPG, 768, 188, self))

        self.alr_init = 0

    def animate(self):

        for npc in self.npcs:
            npc.animate()
        for i in self.ennemies:
            i.animate()
        if self.ennemies == []:
            RPG.level = Level2(RPG)
            RPG.p1.x = 0
            RPG.p1.y = 252
            RPG.screen.blit(RPG.txt2, (0, 0))
            pygame.display.update()
            pygame.event.clear()
            while True:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    self.running = False
                    self.playing = False
                    pygame.quit()
                    sys.exit("Quitting")

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        break

        if self.alr_init == 0:
            self.alr_init += 1

        elif self.alr_init == 1:
            self.alr_init += 1
            RPG.text_box('Commandant Brown', self.joseph6_1)
            RPG.text_box('Commandant Brown', self.joseph6_2, False)
            RPG.text_box('Commandant Brown', self.joseph7, False)
            RPG.text_box('Commandant Brown', self.joseph8_1, False)
            RPG.text_box('Commandant Brown', self.joseph8_2, False)


class Level2:
    # Quick description of the level :
    # But : Tuer tous les anglais + Tutoriel
    def __init__(self, RPG):
        self.image = pygame.image.load((os.path.join('Assets', 'Levels', 'level2.png')))
        self.MAP_WIDTH = self.image.get_rect().width
        self.MAP_HEIGHT = self.image.get_rect().height
        self.obstacles = []
        self.npcs = []
        self.ennemies = []
        self.spawnpoint_x = 0
        self.spawnpoint_y = 252

        RPG.current_level = '2'
        # Creating Obstacles
        # Basic obstacles
        self.obstacles.append(pygame.Rect(-1, -1, self.MAP_WIDTH + 2, 1))
        self.obstacles.append(pygame.Rect(-1, self.MAP_HEIGHT + 1, self.MAP_WIDTH + 2, 1))
        self.obstacles.append(pygame.Rect(self.MAP_WIDTH + 1, -1, 1, self.MAP_HEIGHT + 2))
        self.obstacles.append(pygame.Rect(-1, -1, 1, self.MAP_HEIGHT + 2))
        # Obstacles
        self.obstacles.append(pygame.Rect(0, 140, 60, 252 - 140))
        self.obstacles.append(pygame.Rect(60, 0, 556 - 60, 140))
        self.obstacles.append(pygame.Rect(372, 140, 428 - 372, 176 - 140 - 16))
        self.obstacles.append(pygame.Rect(0, 284, 120, 336 - 120))
        self.obstacles.append(pygame.Rect(120, 336, 276 - 120, 416 - 336))
        self.obstacles.append(pygame.Rect(272, 268 + 16, 856 - 272, 316 - 268))
        self.obstacles.append(pygame.Rect(156, 284, 272 - 156, 316 - 284 - 16))
        self.obstacles.append(pygame.Rect(372, 196, 428 - 372, 248 - 196 - 4))
        self.obstacles.append(pygame.Rect(92, 176, 336 - 92, 248 - 176))
        self.obstacles.append(pygame.Rect(432, 0, 644 - 432, 88))
        self.obstacles.append(pygame.Rect(644, 0, 800 - 644, 72))
        self.obstacles.append(pygame.Rect(760, 104, 788 - 760, 116 - 104))
        self.obstacles.append(pygame.Rect(792, 156, 856 - 792, 216 - 156))
        self.obstacles.append(pygame.Rect(800, 72, 856 - 800, 156 - 72))
        self.obstacles.append(pygame.Rect(588, 204, 616 - 588, 248 - 204))
        self.obstacles.append(pygame.Rect(632 - 16, 224, 644 - 632 + 16, 248 - 224))
        self.obstacles.append(pygame.Rect(492, 196, 572 - 492 - 16, 244 - 196))
        self.obstacles.append(pygame.Rect(428, 188, 488 - 428, 196 - 188))
        self.obstacles.append(pygame.Rect(420, 136, 556 - 420, 160 - 136))
        self.obstacles.append(pygame.Rect(428, 276, 492 - 428, 284 - 276))
        self.obstacles.append(pygame.Rect(428, 196, 492 - 428, 244 - 196))
        # Dialog
        self.gauthier1_1 = "Nous réorganisons une attaque, nous avons plus d'efficacité cette fois-ci, nous avons deux"
        self.gauthier1_2 = "canons. Même s'ils sont en mauvais état, ils peuvent nous être utiles."
        self.gauthier2_1 = "Nos éclaireurs nous ont rapporté qu'une force anglaise approchait St-Eustache avec des canons"
        self.gauthier2_2 = "de la Royal Artillery. Ils sont plus nombreux que nous et c'est un certain Colborn qui les mène."
        self.gauthier2_3 = "Récupérez vos armes et préparez-vous!"
        self.gauthier3 = "Les anglais ont occupé le campement, et il faut que tu les dégages de cet endroit."
        self.gauthier4_1 = "Ils sont extrêmement nombreux, tous nos combattants sont morts ou se sont enfuis."
        self.gauthier4_2 = "Pourrais-tu arriver à les stopper ? Tout ce que je sais, c'est qu'une trappe permet "
        self.gauthier5_1 = "de passer sous la rivière, peut-être que passer par là les prendront par surprise,"
        self.gauthier5_2 = "mais la seule chose dont je suis certain, c'est que tout repose sur tes épaules."

        self.gauthier6 = "Allez tuer le commandant, c'est notre seule chance!"
        self.colborn = "Votre cause est voué au néant, laissez-vous assimiler, ce sera plus simple."
        # NPCS
        self.forgeron = Forgeron(RPG, 116, 140 - 8)
        self.marchand = Marchand(RPG, 128, 248 - 8)
        self.religieuse = Religieuse(RPG, 200, 140 - 8)
        self.jean = Jean(RPG, 224, 316)
        self.roger = Roger(RPG, 320, 140)

        self.npcs.append(Red(RPG, 24, 256-16))
        self.obstacles.append(
            pygame.Rect(self.jean.x + 6, self.jean.y, self.jean.rect.width - 12, self.jean.rect.height - 8))
        self.obstacles.append(
            pygame.Rect(self.roger.x + 6, self.roger.y, self.roger.rect.width - 12, self.roger.rect.height - 8))

        self.ennemies.append(Brit(RPG, 720, 132, self))
        self.ennemies.append(Brit(RPG, 720, 188, self))
        self.ennemies.append(Brit(RPG, 656, 136, self))
        self.ennemies.append(Brit(RPG, 656, 192, self))
        self.ennemies.append(Brit(RPG, 616, 124, self))
        self.ennemies.append(Brit(RPG, 572, 168, self))
        self.ennemies.append(Brit(RPG, 644, 260, self))
        self.ennemies.append(Brit(RPG, 840, 280, self))
        self.ennemies.append(Brit(RPG, 624, 172, self))
        self.ennemies.append(Brit(RPG, 704, 220, self))
        self.ennemies.append(Brit(RPG, 752, 252, self))
        self.ennemies.append(Brit(RPG, 720, 268, self))
        self.ennemies.append(Brit(RPG, 768, 236, self))
        self.ennemies.append(Brit(RPG, 624, 156, self))
        self.ennemies.append(Brit(RPG, 528, 172, self))
        self.ennemies.append(Brit(RPG, 512, 252, self))
        self.ennemies.append(Brit(RPG, 768, 80, self))
        self.ennemies.append(Brit(RPG, 720, 80, self))
        self.ennemies.append(Brit(RPG, 664, 80, self))
        self.ennemies.append(Brit(RPG, 684, 164, self))
        self.ennemies.append(Brit(RPG, 580, 124, self))
        self.ennemies.append(Brit(RPG, 592, 140, self))
        self.ennemies.append(Brit(RPG, 592, 104, self))
        self.ennemies.append(Brit(RPG, 576, 108, self))
        self.ennemies.append(Brit(RPG, 576, 136, self))
        self.ennemies.append(Brit(RPG, 616, 108, self))
        self.ennemies.append(Brit(RPG, 612, 140, self))

        self.ennemies.append(Brit(RPG, 652, 236, self))
        self.ennemies.append(Brit(RPG, 712, 236, self))
        self.ennemies.append(Brit(RPG, 564, 192, self))
        self.ennemies.append(Brit(RPG, 564, 220, self))
        self.ennemies.append(Brit(RPG, 724, 168, self))
        self.ennemies.append(Brit(RPG, 756, 168, self))
        self.ennemies.append(Brit(RPG, 756, 132, self))

        self.ennemies.append(Brit(RPG, 784+32, 140, self))
        self.ennemies.append(Brit(RPG, 652, 268+32, self))
        self.ennemies.append(Brit(RPG, 696, 268+32, self))
        self.ennemies.append(Brit(RPG, 744, 268+32, self))


        self.npcs.append(self.forgeron)
        self.npcs.append(self.marchand)
        self.npcs.append(self.religieuse)
        self.npcs.append(self.jean)
        self.npcs.append(self.roger)
        self.npcs.append(Patriote(RPG, 296, 268-32))

        self.alr_init = 0

    def animate(self):
        if self.alr_init == 0:
            self.alr_init += 1
        elif self.alr_init == 1:
            self.alr_init += 1

            RPG.text_box('Commandant Chénier', self.gauthier1_1)
            RPG.text_box('Commandant Chénier', self.gauthier1_2, False)
            RPG.text_box('Commandant Chénier', self.gauthier2_1, False)
            RPG.text_box('Commandant Chénier', self.gauthier2_2, False)
            RPG.text_box('Commandant Chénier', self.gauthier2_3, False)
            RPG.text_box('Commandant Chénier', self.gauthier3, False)
            RPG.text_box('Commandant Chénier', self.gauthier4_1, False)
            RPG.text_box('Commandant Chénier', self.gauthier4_2, False)
            RPG.text_box('Commandant Chénier', self.gauthier5_1, False)
            RPG.text_box('Commandant Chénier', self.gauthier5_2, False)
            # RPG.text_box('Commandant Chénier', self.gauthier6, False)

            # RPG.text_box('Commandant Anglais Colborn (au loin)', self.colborn, False)

        for npc in self.npcs:
            npc.animate()
        for i in self.ennemies:
            i.animate()

        # Trap:
        if pygame.Rect(RPG.p1.x, RPG.p1.y, RPG.p1.width, RPG.p1.height).colliderect(pygame.Rect(240, 316, 32, 16)):
            RPG.p1.x = 596
            RPG.p1.y = 124

        if self.ennemies == []:
            RPG.text_box("Commandant Chénier", "Je savais que tu pouvais le faire !")
            RPG.text_box("Commandant Chénier", "Félicitation ! Tu leur as reglé leurs comptes !", False)
            RPG.text_box("Jean", "Ton père serait fier de toi ...", False)
            for i in range(10):
                RPG.clock.tick(RPG.hertz)
                v_transition = pygame.Surface((RPG.W_WIDTH, RPG.W_HEIGHT))
                v_transition.set_alpha(128)
                v_transition.fill((0, 0, 0))
                RPG.screen.blit(v_transition, (0, 0))
                pygame.display.update()
            RPG.screen.blit(RPG.txt3, (0, 0))
            pygame.display.update()
            pygame.event.clear()
            while True:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    self.running = False
                    self.playing = False
                    pygame.quit()
                    sys.exit("Quitting")

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        break
            self.running = False
            self.playing = False
            pygame.quit()
            sys.exit("Quitting")


if __name__ == '__main__':
    RPG = Game()
    RPG.main_loop()
