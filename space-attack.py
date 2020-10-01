import pygame
import random
import pygame.freetype
# pylint: disable=no-member



class Game:
    state = dict()
    missiles = []
    enemies = []
    enemy_missiles = []

    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height)) # initialize the window and size
        self.clock = pygame.time.Clock() # object to track time
        self.clock.tick(60) # tells clock to tick 60 times a second, 60fps

        self.score = 0

        pygame.font.init()
        self.font = pygame.font.SysFont("Impact", 50)
        self.background_image = pygame.image.load("./sprites/background.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

        self.missile_sound = pygame.mixer.Sound("./sounds/missile.wav")
        self.explosion_sound = pygame.mixer.Sound("./sounds/explosion.wav")
        
        self.state["play"] = False
        self.state["quit"] = False
        self.state["end"] = False
        self.state["start"] = True

        while self.state["quit"] is False:
            if self.state["start"] is True:
                self.start()
            if self.state["play"] is True:
                self.play_game()
            if self.state["end"] is True:
                self.end()
            if self.state["quit"] is True:
                pass
    
    def play_game(self):
        self.player = Player(self, 50, self.height // 2)
        speed = 4

        state_cooldown = 0
        up_cooldown = 30

        spawn_cooldown = 0

        shoot_cooldown = 0
        shoot1_cooldown = 0
        shoot2_cooldown = 0

        shoot_button = Button2((255, 0, 0), (255, 255, 255), self.width - 150, 550, 80, 40, 50, "./sprites/missile.png")
        shoot1_button = Button2((0, 0, 255), (255, 255, 255), self.width - 150 - 150, 550, 80, 40, 50, "./sprites/missile1.png")
        shoot2_button = Button2((0, 255, 0), (255, 255, 255), self.width - 150 - 150 - 150, 550, 80, 40, 50, "./sprites/missile2.png")

        inside_button = CircleButton((255, 255, 0), (255, 255, 0), 100, self.height - 100, 30)
        outside_button = CircleButton((255, 255, 255), (255, 255, 255), 100, self.height - 100, 75)
        
        exitwarning = pygame.image.load("./sprites/exitwarning.jpg")
        exitwarning = pygame.transform.scale(exitwarning, (self.width, self.height))

        while self.state["quit"] is False: # MAIN GAME LOOP
            pressed = pygame.key.get_pressed()
            
            if pressed[pygame.K_LEFT] == 1:
                if self.player.x > 50:
                    self.player.x -= speed
            if pressed[pygame.K_RIGHT] == 1:
                if self.player.x < self.width - 100: 
                    self.player.x += speed
            if pressed[pygame.K_SPACE] == 1:
                if up_cooldown == 0 and self.player.y > 20:  
                    self.player.y -= 4
                else:
                    up_cooldown -= 1
            elif pressed[pygame.K_SPACE] == 0:
                up_cooldown = 30
            if pressed[pygame.K_s] == 1 or pressed[pygame.K_UP] == 1:
                if shoot_cooldown == 0:
                    self.player.shoot()
                    shoot_cooldown = 60
                    pygame.mixer.Sound.play(self.missile_sound)
            if pressed[pygame.K_d] == 1:
                if shoot1_cooldown == 0:
                    self.player.shoot1()
                    shoot1_cooldown = 180
                    pygame.mixer.Sound.play(self.missile_sound)
            if pressed[pygame.K_f] == 1:
                if shoot2_cooldown == 0:
                    self.player.shoot2()
                    shoot2_cooldown = 180
                    pygame.mixer.Sound.play(self.missile_sound)


            pos = pygame.mouse.get_pos()
            moused = pygame.mouse.get_pressed()
            if moused[0] == 1: # if left mouse clicked
                if inside_button.y < outside_button.y:
                    if self.player.y > 20:
                        self.player.y -= 4
                
                if inside_button.x < outside_button.x:
                    if self.player.x > 50:
                        self.player.x -= speed

                if inside_button.x > outside_button.x:
                    if self.player.x < self.width - 100: 
                        self.player.x += speed

            if moused[0] == 1: # if left mouse clicked
                if shoot_button.isOver(pos):
                    if shoot_cooldown == 0:
                        self.player.shoot()
                        shoot_cooldown = 60
                        pygame.mixer.Sound.play(self.missile_sound)
                if shoot1_button.isOver(pos):
                    if shoot1_cooldown == 0:
                        self.player.shoot1()
                        shoot1_cooldown = 180
                        pygame.mixer.Sound.play(self.missile_sound)
                if shoot2_button.isOver(pos):
                    if shoot2_cooldown == 0:
                        self.player.shoot2()
                        shoot2_cooldown = 180
                        pygame.mixer.Sound.play(self.missile_sound)
                        
            if moused[0] == 1: # if left mouse clicked
                if inside_button.isOver(pos): # this is to move the yellow circle 
                    if outside_button.x - outside_button.radius < pos[0] < outside_button.x + outside_button.radius:
                        if outside_button.y - outside_button.radius < pos[1] < outside_button.y + outside_button.radius: 
                            inside_button.x = pos[0]
                            inside_button.y = pos[1]

            if moused[0] == 0: # reset the yellow circle
                inside_button.x = 100
                inside_button.y = self.height - 100


            for event in pygame.event.get(): # clears all the events in pygame 
                if event.type == pygame.QUIT: # important to check if quit rather than clear
                    pause = True
                    while pause is True:
                        self.screen.blit(exitwarning, (0,0))
                        pygame.display.flip() # updates game window

                        # very important
                        for event in pygame.event.get():
                            pass
                        
                        # make buttons 
                        # left = yes
                        # right = no

                    # self.new_state("quit")
            
            pygame.display.flip() # updates game window
            self.screen.blit(self.background_image, (0,0))

            if state_cooldown == 0:
                self.player.state = (self.player.state + 1) % 4
                self.player.image = self.player.image_list[self.player.state]
                state_cooldown = 1
            else:
                state_cooldown -= 1

            if spawn_cooldown == 0:
                Generator(self)
                spawn_cooldown = 360
            else:
                spawn_cooldown -= 1

            if shoot_cooldown > 0:
                # shoot_button.back_colour = (255 -  (255 * shoot_cooldown // 60),0,0)
                shoot_button.back_colour = (0,0,0)
                shoot_cooldown -= 1
            else:
                shoot_button.back_colour = (255,0,0)

            if shoot1_cooldown > 0:
                shoot1_button.back_colour = (0,0,0)
                shoot1_cooldown -= 1
            else:
                shoot1_button.back_colour = (0,0,255)


            if shoot2_cooldown > 0:
                shoot2_button.back_colour = (0,0,0)
                shoot2_cooldown -= 1
            else:
                shoot2_button.back_colour = (0,255,0)


            for missile in self.missiles:
                missile.check_collision()
                missile.draw()

            for enemy in self.enemies:
                enemy.draw()


            shoot_button.draw(self.screen)
            shoot1_button.draw(self.screen)
            shoot2_button.draw(self.screen)

            self.player.draw()

            # happens after draw player so explosion is in front
            for e_missile in self.enemy_missiles:
                e_missile.check_collision()
                e_missile.draw()

            outside_button.draw(self.screen)
            inside_button.draw(self.screen)

            self.player.draw_health()

            if self.player.current_health <= 0: # game over
                self.new_state("end")
                self.state["play"] == False
                self.state["end"] == True
                break

            
            text = self.font.render(f"SCORE: {str(self.score)}", True, (255, 255, 255))
            textRect = text.get_rect()
            self.screen.blit(text, textRect)



    def start(self):
        self.startfont = pygame.font.SysFont("Impact", 100)

        self.start_image = pygame.image.load("./sprites/start_screen.png")
        self.start_image = pygame.transform.scale(self.start_image, (self.width, self.height))

        title_str = "Helicopter Attack!"

        self.start_button = Image_Button(self.width // 2 - 200 // 2, self.height // 2, 200, 200, "./sprites/start_button.png")

        while self.state["start"] is True:
            ###
            black = True
            for i, char in enumerate(title_str):

                if black is True:
                    letter = self.startfont.render(char, True, (0, 0, 0))
                    black = False
                else:
                    letter = self.startfont.render(char, True, (255, 255, 0))
                    black = True

                text_rect = letter.get_rect(center=(self.width // 2 - len(title_str)*40 // 2 + 40*i, self.height // 5))
                self.screen.blit(letter, text_rect)
            ###



            pygame.display.flip() # updates game window
            self.screen.blit(self.start_image, (0,0))

            self.start_button.draw(self.screen)

            # self.screen.blit(start_text, text_rect)

            for event in pygame.event.get(): # clears all the events in pygame 
                pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT: # important to check if quit rather than clear
                    self.new_state("quit")

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.isOver(pos):
                        self.new_state("play")


    def end(self):
        # end_text = self.font.render(f"GAME OVER: SCORE = {str(self.score)}", True, (255, 255, 255))
        endfont = pygame.font.SysFont("Impact", 100)

        end_text = endfont.render(f"M I S S I O N    F A I L E D", True, (255, 0, 0))
        text_rect = end_text.get_rect(center=(self.width // 2, self.height // 5)) # centers

        score_text = endfont.render(f"SCORE = {str(self.score)}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.width // 2, self.height // 5 + 150)) # centers

        self.restart_button = Image_Button(self.width // 2 - 400 // 2, self.height // 2, 400, 200, "./sprites/restart_button.png")
            
        while self.state["end"] is True:
            pygame.display.flip() # updates game window
            self.screen.blit(self.background_image, (0,0))

            self.screen.blit(end_text, text_rect)

            self.screen.blit(score_text, score_rect)

            self.restart_button.draw(self.screen)

            for event in pygame.event.get(): # clears all the events in pygame 
                pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT: # important to check if quit rather than clear
                    self.new_state("quit")

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.restart_button.isOver(pos):
                        self.new_state("start")


    def new_state(self, value):
        # updates all states in dict
        for key, _ in self.state.items():
            if key == value:
                self.state[key] = True
            else:
                self.state[key] = False


    # def exit_screen(self):
        # exitfont = pygame.font.SysFont("Impact", 100)
        # end_text = exitfont.render(f"Do you want to give up mission?", True, (255, 0, 0))
        # text_rect = end_text.get_rect(center=(self.width // 2, self.height // 5)) # centers





class Player:
    height = 80
    width = 150

    max_health = 5

    def __init__(self, game, x, y):
        self.x = x
        self.y = y # sets coordinates
        self.game = game

        self.image1 = pygame.image.load("./sprites/heli_1.png")
        self.image1 = pygame.transform.scale(self.image1, (self.width, self.height))

        self.image2 = pygame.image.load("./sprites/heli_2.png")
        self.image2 = pygame.transform.scale(self.image2, (self.width, self.height))

        self.image3 = pygame.image.load("./sprites/heli_3.png")
        self.image3 = pygame.transform.scale(self.image3, (self.width, self.height))

        self.image4 = pygame.image.load("./sprites/heli_4.png")
        self.image4 = pygame.transform.scale(self.image4, (self.width, self.height))

        self.image_list = [self.image1, self.image2, self.image3, self.image4]
        self.state = 1

        self.image = self.image1

        self.noise_cooldown = 15
        self.left = 0

        ##
        self.health_picture = pygame.image.load("./sprites/heart.png")
        self.health_picture = pygame.transform.scale(self.health_picture, (80, 80))

        self.health_empty_picture = pygame.image.load("./sprites/heart1.png")
        self.health_empty_picture = pygame.transform.scale(self.health_empty_picture, (80, 80))

        self.current_health = self.max_health
        ##

    def draw(self):
        self.game.screen.blit(self.image, (self.x, self.y))
        if self.y < self.game.height - self.height:
            self.y += 2

        if self.noise_cooldown == 0:
            self.left = random.randint(0, 1)
            self.noise_cooldown = 15
        else:
            if self.left == 1 and self.x > 0:
                self.x -= 1
            else:
                self.x += 1

            self.noise_cooldown -= 1

    def draw_health(self):
        gap = 0
        current_x = self.game.width

        for i in range(self.max_health):
            current_x -= gap
            current_x -= 80 # how wide our hearts are

            if i >= self.current_health:
                self.game.screen.blit(self.health_empty_picture, (current_x, gap))
            else:
                self.game.screen.blit(self.health_picture, (current_x, gap))


    def shoot(self):
        self.game.missiles.append(Missile(self.game, self.x + self.width - 20, self.y + self.height - 20, right=True))
        
    def shoot1(self, alt_start = None):
        if alt_start is None:
            self.game.missiles.append(Missile1(self.game, self.x + self.width - 20, self.y + self.height - 20))
        else:
            temp_x = alt_start[0]
            temp_y = alt_start[1]
            self.game.missiles.append(Missile1(self.game, temp_x, temp_y))

    def shoot2(self):
        self.game.missiles.append(Missile2(self.game, self.x + self.width - 20, self.y + self.height - 20))



class Missile:
    def __init__(self, game, x, y, right=False, up=False, down=False, left=False):
        self.x = x
        self.y = y # sets coordinates
        self.game = game

        self.image = pygame.image.load("./sprites/missile.png")
        self.image = pygame.transform.scale(self.image, (40, 20))

        self.explode_image = pygame.image.load("./sprites/explosion.png")
        self.explode_image = pygame.transform.scale(self.explode_image, (100, 100))
        self.explode = False
        self.countdown = 60

        self.right = right
        self.up = up
        self.down = down
        self.left = left
        

        if self.up is True:
            self.image = pygame.transform.rotate(self.image, 90)
        if self.down is True:
            self.image = pygame.transform.rotate(self.image, -90)
        if self.left is True:
            self.image = pygame.transform.rotate(self.image, 180)
    
    def draw(self):
        self.game.screen.blit(self.image, (self.x, self.y))
        if self.explode is False and self.right is True:
            self.x += 2
        elif self.explode is False and self.up is True:
            self.y -= 2
        elif self.explode is False and self.down is True:
            self.y += 2
        elif self.explode is False and self.left is True:
            self.x -= 2
        
        else:
            self.countdown -= 1
        if self.countdown == 0:
            self.game.missiles.remove(self) # removes item from list
    
    def check_collision(self):
        for enemy in self.game.enemies:
            if (enemy.x <= self.x + 10 <= enemy.x + enemy.width) \
                and (enemy.y + 20 <= self.y + 10 <= enemy.y + enemy.height):
                # and self.explode is False:
                # self.game.missiles.remove(self) # removes item from list
                self.image = self.explode_image
                self.explode = True
                self.y -= 20
                self.game.enemies.remove(enemy)
                pygame.mixer.Sound.play(self.game.explosion_sound)

                self.game.score += 1
                break


class Missile1:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y # sets coordinates
        self.game = game

        self.image = pygame.image.load("./sprites/missile1.png")
        self.image = pygame.transform.scale(self.image, (50, 40))

        self.explode_image = pygame.image.load("./sprites/explosion.png")
        self.explode_image = pygame.transform.scale(self.explode_image, (200, 200))
        self.explode = False
        self.countdown = 90
    def draw(self):
        self.game.screen.blit(self.image, (self.x, self.y))
        if self.explode is False and len(self.game.enemies) != 0:
            ####
            # this is where missile moves to enemy
            enemy = self.game.enemies[0]

            enemy_x = enemy.x + enemy.width // 2
            enemy_y = enemy.y + enemy.height // 2

            me_x = self.x + 25
            me_y = self.y + 20

            y_diff = enemy_y - me_y
            x_diff = enemy_x - me_x

            if x_diff > 0:
                self.x += max(x_diff // 50, 10)
            else:
                self.x += min(x_diff // 50, -10)
            if y_diff > 0:
                self.y += max(y_diff // 50, 10)
            else:
                self.y += min(y_diff // 50, -10)

            ####
        elif self.explode is True:
            self.countdown -= 1
        if self.countdown == 0:
            self.game.missiles.remove(self) # removes item from list

        if len(self.game.enemies) == 0:
            self.x += 5
        

    def check_collision(self):
        for enemy in self.game.enemies:
            if (enemy.x - 100 <= self.x + 10 <= enemy.x + enemy.width + 100) \
                and (enemy.y + 20 - 100 <= self.y + 10 <= enemy.y + enemy.height + 100) \
                and self.explode is False:
                # self.game.missiles.remove(self) # removes item from list
                self.image = self.explode_image
                self.explode = True
                self.y -= 40
                self.game.enemies.remove(enemy)
                pygame.mixer.Sound.play(self.game.explosion_sound)

                self.game.score += 1
                break




class Missile2:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y # sets coordinates
        self.game = game

        self.image = pygame.image.load("./sprites/missile2.png")
        self.image = pygame.transform.scale(self.image, (50, 40))

        self.explode_image = pygame.image.load("./sprites/explosion.png")
        self.explode_image = pygame.transform.scale(self.explode_image, (100, 100))
        self.explode = False
        self.countdown = 90
    def draw(self):
        self.game.screen.blit(self.image, (self.x, self.y))
        if self.explode is False and len(self.game.enemies) != 0:
            ####
            # this is where missile moves to enemy
            enemy = self.game.enemies[0]

            enemy_x = enemy.x + enemy.width // 2
            enemy_y = enemy.y + enemy.height // 2

            me_x = self.x + 25
            me_y = self.y + 20

            y_diff = enemy_y - me_y
            x_diff = enemy_x - me_x

            if x_diff > 0:
                self.x += max(x_diff // 50, 10)
            else:
                if x_diff == 0:
                    if y_diff > 0:
                        self.y += max(y_diff // 50, 10)
                    else:
                        self.y += min(y_diff // 50, -10)
                else:
                    self.x += min(x_diff // 50, -10)
            if y_diff > 0:
                self.y += max(y_diff // 50, 10)
            else:
                self.y += min(y_diff // 50, -10)

            

            ####
        elif self.explode is True:
            self.countdown -= 1
        if self.countdown == 0:
            self.game.missiles.remove(self) # removes item from list

        if len(self.game.enemies) == 0:
            self.x += 5

    def check_collision(self):
        for enemy in self.game.enemies:
            if (enemy.x <= self.x + 10 <= enemy.x + enemy.width) \
                and (enemy.y + 20 <= self.y + 10 <= enemy.y + enemy.height) \
                and self.explode is False:
                # self.game.missiles.remove(self) # removes item from list
                self.image = self.explode_image
                self.explode = True
                self.y -= 40
                self.game.enemies.remove(enemy)
                pygame.mixer.Sound.play(self.game.explosion_sound)

                self.game.missiles.append(Missile(self.game, self.x, self.y, right=True))
                self.game.missiles.append(Missile(self.game, self.x, self.y, up=True))
                self.game.missiles.append(Missile(self.game, self.x, self.y, down=True))
                self.game.missiles.append(Missile(self.game, self.x, self.y, left=True))

                self.game.score += 1

                break

    
class E_Missile1:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y # sets coordinates
        self.game = game

        self.image = pygame.image.load("./sprites/missile_enemy.png")
        self.image = pygame.transform.scale(self.image, (40, 20))

        self.explode_image = pygame.image.load("./sprites/explosion2.png")
        self.explode_image = pygame.transform.scale(self.explode_image, (100, 100))
    
        self.explode = False
        self.countdown = 60

    def draw(self):
        self.game.screen.blit(self.image, (self.x, self.y))
        if self.explode is False:
            self.x -= 2
        else:
            self.y = self.game.player.y + self.game.player.height // 4 - 10
            self.x = self.game.player.x + self.game.player.width // 4
            self.countdown -= 1

        if self.countdown == 0:
            self.game.enemy_missiles.remove(self) # removes item from list

    def check_collision(self):
        if self.game.player.x <= self.x <= self.game.player.x + self.game.player.width:
            if self.game.player.y <= self.y + 10 <= self.game.player.y + self.game.player.height:
                if self.explode is False:
                    self.image = self.explode_image
                    self.explode = True
                    self.y = self.game.player.y + self.game.player.height // 2
                    self.x = self.game.player.x + self.game.player.width // 2
                    pygame.mixer.Sound.play(self.game.explosion_sound)

                    self.game.player.current_health -= 1




class Enemy:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y # sets coordinates
        self.game = game
        self.width = 150 # for collision checking
        self.height = 80

        num = random.randint(1, 3)
        self.image = pygame.image.load(f"./sprites/enemy_{num}.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

        self.start = True
        self.current_move = False

    def draw(self):
        self.game.screen.blit(self.image, (self.x, self.y))

        if self.start is True and self.x > 800:
            self.x -= 3
        else:
            self.start = False

        if self.start is False and self.current_move is False:
            self.current_move = True
            self.x_dir = random.randint(0, 1)
            self.y_dir = random.randint(0, 1)
            self.dist = random.randint(100, 200)
            self.move(self.x_dir, self.y_dir, self.dist)
        
        if self.current_move is True:
            self.move(self.x_dir, self.y_dir, self.dist)

        if random.randint(0, 1000) == 0 and self.start is False:
            self.shoot()

        if self.x < -self.width:
            self.game.enemies.remove(self)

    def shoot(self):
        self.game.enemy_missiles.append(E_Missile1(self.game, self.x + self.width - 20, self.y + self.height - 20))

    def move(self, x_dir, y_dir, dist):
        # if x_dir = 1: right
        # if x_dir = 0: left
        # y_dir = 1: down
        # y_dir = 0: up
        dist = dist // 100

        if x_dir == 1:
            if self.x < self.game.width - 150:
                self.x += dist
            else:
                self.current_move = False

        if x_dir == 0:
            if self.x > 150:
                self.x -= dist
            else:
                self.current_move = False

        if y_dir == 0:
            if self.y < self.game.height - 100:
                self.y += dist
            else:
                self.current_move = False

        if y_dir == 1:
            if self.y > 100:
                self.y -= dist
            else:
                self.current_move = False



class Generator:
    def __init__(self, game):
        margin = 30 # how far from edge
        width = 50 # how far between each alien
        # count = random.randint(1, 5)
        count = 3

        current_spawn_y = []
        
        for _ in range(count):
            y = random.randint(margin, game.height - margin)
            # y = 400
            # y = random.randint(300, 400)

            block = False
            for item in current_spawn_y:
                if -30 < y - item < 30:
                    block = True                        

            if block is True:
                break
            
            current_spawn_y.append(y)
            x = int(game.width + 30)
            y = int(y)
            game.enemies.append(Enemy(game, x, y))


class Button:
    # these are the original rectangle buttons
    def __init__(self, back_colour, text_colour, x, y, width, height, text=''):
        self.back_colour = back_colour
        self.text_color = text_colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen):
        # draw the button on the screen            
        pygame.draw.rect(screen, self.back_colour, (self.x,self.y,self.width,self.height), 0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, self.text_color)
            screen.blit(text, (self.x + (self.width//2 - text.get_width()//2), self.y + (self.height//2 - text.get_height()//2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False


class Image_Button:
    # custom button that uses image instead
    # no support for text
    def __init__(self, x, y, width, height, image_path):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image_path = image_path

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, screen):
        # draw the button on the screen            
        screen.blit(self.image, (self.x, self.y))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


class Button2:
    # this is the circle buttons for shooting
    def __init__(self, back_colour, text_colour, x, y, width, height, radius, path=''):
        self.back_colour = back_colour
        self.text_color = text_colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.radius = radius
        self.image = pygame.image.load(f"{path}") # path to inside image
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, screen):
        pygame.draw.circle(screen, self.back_colour, (self.x, self.y), self.radius)
        screen.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))


    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x - self.radius < pos[0] < self.x + self.radius:
            if self.y - self.radius < pos[1] < self.y + self.radius:
                return True
            
        return False


class CircleButton:
    def __init__(self, back_colour, inner_colour, x, y, radius):
        self.back_colour = back_colour
        self.inner_colour = inner_colour
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.back_colour, (self.x, self.y), self.radius)

    def isOver(self, pos):
        if self.x - self.radius < pos[0] < self.x + self.radius:
            if self.y - self.radius < pos[1] < self.y + self.radius:
                return True
            
        return False


if __name__ == '__main__':
    Game(1200, 600)
