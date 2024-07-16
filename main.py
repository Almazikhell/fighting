import random

import pygame as pg
import pygame_menu

pg.init()
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550

CHARACTER_WIDTH = 200
CHARACTER_HEGHT = 350

FPS = 120
font = pg.font.Font(None, 40)


def load_image(file, width, height):
    image = pg.image.load(file).convert_alpha()
    image = pg.transform.scale(image, (width, height))
    return image


def text_render(text):
    return font.render(str(text), True, "black")


class Magicball(pg.sprite.Sprite):
    def __init__(self, coord, side, power, folder):
        super().__init__()
        self.side = side
        self.power = power
        self.image = load_image(f"images/{folder}/magicball.png", 200, 150)
        self.rect = self.image.get_rect()
        self.rect.center = (coord[0], coord[1] + 120)

    def update(self):
        if self.side == "left":
            self.rect.x -= 4
        else:
            self.rect.x += 4

        if self.rect.x < -200 or self.rect.x > SCREEN_WIDTH:
            self.kill()


class Enemy(pg.sprite.Sprite):
    def __init__(self, player, folder):
        super().__init__()
        self.player = player
        self.folder = folder
        self.charge = [load_image(f"images/{self.folder}/charge.png", CHARACTER_WIDTH, CHARACTER_HEGHT)]
        self.attack = [load_image(f"images/{self.folder}/attack.png", CHARACTER_WIDTH, CHARACTER_HEGHT)]
        self.down = [load_image(f"images/{self.folder}/down.png", CHARACTER_WIDTH, CHARACTER_HEGHT)]
        self.move_anim_left = []
        self.move_anim_right = []
        self.idle_anim_left = []
        self.idle_anim_right = []
        self.animation_mode = True
        self.charge_mode = False
        self.load_animation()
        self.hp = 200
        self.side = "left"
        self.image = self.idle_anim_right[0]
        self.current_image = 0
        self.current_anim = self.idle_anim_right
        self.rect = self.image.get_rect()
        self.rect.center = (700, SCREEN_HEIGHT // 2)
        self.timer = pg.time.get_ticks()
        self.interval = 800
        self.charge_power = 0
        self.probality_of_attack = 0
        self.attack_mode = False
        self.attack_interval = 500
        self.magicballs = pg.sprite.Group()
        self.move_interval = 0
        self.move_timer = pg.time.get_ticks()
        self.move_duration = random.randint(400, 1500)
        self.direction = -1

    def update(self):
        self.play_anim()
        self.handle_movemenet()
        self.handle_attack_mode()


    def handle_attack_mode(self):

        if not self.attack_mode:
            self.probality_of_attack = 1

            if self.player.charge_mode:
                self.probality_of_attack += 2

            if random.randint(1, 100) <= self.probality_of_attack:
                self.attack_mode = True
                if self.player.rect.centerx < self.rect.centerx:
                    self.side = "left"
                else:
                    self.side = "right"
                self.animation_mode = False
                self.image = self.attack[self.side != "right"]

        if self.attack_mode:
            if pg.time.get_ticks() - self.timer > self.attack_interval:
                self.attack_mode = False
                self.timer = pg.time.get_ticks()
                magicball_position = self.rect.topright if self.side == "right" else self.rect.topleft
                self.magicballs.add(Magicball(magicball_position, self.side, random.randint(5,42), self.folder))



    def handle_movemenet(self):
        print(self.attack_mode)
        if self.attack_mode:
            return

        now = pg.time.get_ticks()
        if now - self.move_timer < self.move_duration:
            self.animation_mode = True
            self.rect.x += self.direction
            if self.rect.right >= SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
            elif self.rect.left <= 0:
                self.rect.left = 0
        else:
            if random.randint(1, 100) == 1 and now - self.move_timer > self.move_interval:
                self.move_timer = pg.time.get_ticks()
                self.move_duration = random.randint(400, 1500)
                self.direction = random.choice([-1, 1])
            else:
                self.animation_mode = True
                self.current_anim = self.idle_anim_left if self.side == "left" else self.idle_anim_right

    def play_anim(self):
        if not self.charge_mode and self.charge_power > 0:
            self.attack_mode = True

        if pg.time.get_ticks() > self.timer + self.interval:
            self.current_image += 1
            if self.current_image >= len(self.current_anim):
                self.current_image = 0
            self.image = self.current_anim[self.current_image]
            self.timer = pg.time.get_ticks()

    def load_animation(self):
        for i in range(1, 4):
            self.idle_anim_right.append(
                load_image(f"images/{self.folder}/idle{i}.png", CHARACTER_WIDTH, CHARACTER_HEGHT))
        for i in self.idle_anim_right:
            self.idle_anim_left.append(pg.transform.flip(i, True, False))
        for i in range(1, 5):
            self.move_anim_right.append(
                load_image(f"images/{self.folder}/move{i}.png", CHARACTER_WIDTH, CHARACTER_HEGHT))
        for i in self.move_anim_right:
            self.move_anim_left.append(pg.transform.flip(i, True, False))

        self.charge.append(pg.transform.flip(self.charge[0], True, False))
        self.attack.append(pg.transform.flip(self.attack[0], True, False))
        self.down.append(pg.transform.flip(self.down[0], True, False))


class Player(pg.sprite.Sprite):
    def __init__(self, folder='lightning wizard',first_player = True):
        super().__init__()
        self.folder = folder
        self.charge = [load_image("images/"+self.folder+"/charge.png", CHARACTER_WIDTH, CHARACTER_HEGHT)]
        self.attack = [load_image("images/"+self.folder+"/attack.png", CHARACTER_WIDTH, CHARACTER_HEGHT)]
        self.down = [load_image("images/"+self.folder+"/down.png", CHARACTER_WIDTH, CHARACTER_HEGHT)]
        self.move_anim_left = []
        self.move_anim_right = []
        self.idle_anim_left = []
        self.idle_anim_right = []
        self.animation_mode = True
        self.charge_mode = False
        self.load_animation()
        if first_player:
            self.side = "right"
            self.image = self.idle_anim_right[0]
            self.rect = self.image.get_rect()
            self.rect.center = (100,SCREEN_HEIGHT//2)
            self.current_anim = self.idle_anim_right
            self.key_right = pg.K_d
            self.key_left = pg.K_a
            self.key_charge = pg.K_SPACE
            self.key_down = pg.K_s
        else:
            self.side = "left"
            self.image = self.idle_anim_left[0]
            self.rect = self.image.get_rect()
            self.rect.center = (SCREEN_WIDTH-100, SCREEN_HEIGHT // 2)
            self.current_anim = self.idle_anim_left
            self.key_right = pg.K_l
            self.key_left = pg.K_j
            self.key_charge = pg.K_RALT
            self.key_down = pg.K_k
        self.current_image = 0
        self.current_anim = self.idle_anim_right
        self.timer = pg.time.get_ticks()
        self.interval = 333
        self.hp = 200

        self.charge_power = 0
        self.charge_indicator = pg.Surface((self.charge_power, 10))
        self.charge_indicator.fill('purple')

        self.attack_mode = False
        self.attack_interval = 500
        self.magicballs = pg.sprite.Group()


    def load_animation(self):
        for i in range(1, 4):
            self.idle_anim_right.append(
                load_image(f"images/{self.folder}/idle{i}.png", CHARACTER_WIDTH, CHARACTER_HEGHT))
        for i in self.idle_anim_right:
            self.idle_anim_left.append(pg.transform.flip(i, True, False))
        for i in range(1, 5):
            self.move_anim_right.append(
                load_image(f"images/{self.folder}/move{i}.png", CHARACTER_WIDTH, CHARACTER_HEGHT))
        for i in self.move_anim_right:
            self.move_anim_left.append(pg.transform.flip(i, True, False))

        self.charge.append(pg.transform.flip(self.charge[0], True, False))
        self.attack.append(pg.transform.flip(self.attack[0], True, False))
        self.down.append(pg.transform.flip(self.down[0], True, False))

    def update(self):
        self.play_anim()
        keys = pg.key.get_pressed()
        direction = 0
        if keys[self.key_left]:
            direction = -1
            self.side = "left"
        elif keys[self.key_right]:
            direction = 1
            self.side = "right"


        self.handle_attack_mode()
        self.handle_movemenet(direction, keys)

    def handle_attack_mode(self):
        if self.attack_mode:
            if pg.time.get_ticks() - self.timer > self.attack_interval:
                self.attack_mode = False
                self.timer = pg.time.get_ticks()

    def handle_movemenet(self, direction, keys):
        if direction != 0:
            self.animation_mode = True
            self.charge_mode = False
            self.rect.x += direction
            self.current_anim = self.move_anim_left if direction == -1 else self.move_anim_right
        elif keys[self.key_charge]:
            self.animation_mode = False
            self.charge_mode = True
            self.image = self.charge[self.side != "right"]
        elif keys[self.key_down]:
            self.animation_mode = False
            self.charge_mode = False
            self.image = self.down[self.side != "right"]
        else:
            self.current_anim = self.idle_anim_left if self.side == "left" else self.idle_anim_right
            self.animation_mode = True
            self.charge_mode = False

    def play_anim(self):
        if not self.charge_mode and self.charge_power > 0:
            self.attack_mode = True
        if pg.time.get_ticks() > self.timer + self.interval:
            self.current_image += 1
            if self.current_image >= len(self.current_anim):
                self.current_image = 0
            self.image = self.current_anim[self.current_image]
            self.timer = pg.time.get_ticks()

        if self.charge_mode:
            self.charge_power += 1
            self.charge_indicator = pg.Surface((self.charge_power, 10))
            self.charge_indicator.fill('purple')
            if self.charge_power >= 100:
                self.attack_mode = True

        if self.attack_mode and self.charge_power > 0:
            magicball_position = self.rect.topright if self.side == "right" else self.rect.topleft
            self.magicballs.add(Magicball(magicball_position, self.side, self.charge_power, self.folder))
            self.charge_mode = False
            self.attack_mode = False
            self.charge_power = 0
            self.image = self.attack[self.side != "right"]
            self.timer = pg.time.get_ticks()


class Menu:
    def __init__(self):
        self.surface = pg.display.set_mode((900, 550))
        font = pygame_menu.font.FONT_FIRACODE_BOLD
        pygame_menu.themes.THEME_DARK.widget_font = font
        self.menu = pygame_menu.Menu(
            height=550,
            theme=pygame_menu.themes.THEME_DARK,
            title='Меню',
            width=900,
        )
        self.enemy = 'fire wizard'
        self.menu.add.label("На одного")
        self.menu.add.selector("Противник: ",
                               [("Маг молний", 0), ("Монах земли", 1), ("Случайный враг", 777)],
                               onchange=self.set_enemy)
        self.menu.add.button("Играть", self.start_one_player_game)
        self.menu.add.label("На двоих")
        self.menu.add.selector("Первый игрок: ",
                               [("Маг молний", 0), ("Монах земли", 1), ("Маг огня", 2)],
                               onchange=self.set_left_player)
        self.menu.add.selector("Второй игрок: ",
                               [("Маг молний", 0), ("Монах земли", 1), ("Маг огня", 2)],
                               onchange=self.set_right_player)
        self.menu.add.button("Играть", self.start_two_player_game)
        self.menu.add.button("Выйти", self.end_game)
        self.enemy_list = ['fire wizard', "earth monk"]

        self.players = ["lightning wizard", "earth monk", "fire wizard"]
        self.left_player = self.players[0]
        self.right_player = self.players[0]


        self.run()

    def set_enemy(self, name, value):
        if value in (0, 1):
            self.enemy = self.enemy_list[value]
        else:
            self.enemy = random.choice(self.enemy_list)

    def set_left_player(self, selected, value):
        self.left_player = self.players[value]

    def set_right_player(self, selected, value):
        self.right_player = self.players[value]

    def start_one_player_game(self):
        Game("one player", (self.enemy,))


    def start_two_player_game(self):
        Game("two players", (self.left_player, self.right_player))



    def end_game(self):
        quit()

    def run(self):
        self.menu.mainloop(self.surface)


class Game:
    def __init__(self,mode, enemy_name):
        # Создание окна
        if mode == "one player":
            self.player = Player()
            self.enemy = Enemy(self.player, enemy_name[0])
        elif mode == "two players":
            self.player = Player(enemy_name[0])
            self.enemy = Player(enemy_name[1],first_player=False)
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Битва магов")
        self.background = load_image("images/background.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bush = load_image('images/Передний план.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.clock = pg.time.Clock()
        self.win = None
        self.mode = mode

        self.run()

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            if event.type == pg.QUIT:
                self.is_running = False
            if event.type == pg.KEYDOWN and self.win is not None:
                self.is_running = False
                Menu()


    def update(self):
        if self.win is None:
            self.player.update()
            self.enemy.update()
            self.player.magicballs.update()
            self.enemy.magicballs.update()

            hits = pg.sprite.spritecollide(self.enemy, self.player.magicballs, True, pg.sprite.collide_rect_ratio(0.3))
            for hit in hits:
                self.enemy.hp -= hit.power
                print(self.enemy.hp)
            hits = pg.sprite.spritecollide(self.player, self.enemy.magicballs, True, pg.sprite.collide_rect_ratio(0.3))
            for hit in hits:
                self.player.hp -= hit.power
                print(self.player.hp)
            if self.player.hp <= 0:
                self.win = self.enemy
            elif self.enemy.hp <= 0:
                self.win = self.player







    def draw(self):
        # Отрисовка интерфейса
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.enemy.image, self.enemy.rect)
        if self.player.charge_mode:
            self.screen.blit(self.player.charge_indicator, (self.player.rect.left + 60, self.player.rect.top))
        self.screen.blit(self.bush, (0, 0))
        for i in self.player.magicballs:
            self.screen.blit(i.image, i.rect)
        for i in self.enemy.magicballs:
            self.screen.blit(i.image, i.rect)

        rect = pg.Rect(10, 10, 210, 40)
        pg.draw.rect(self.screen, pg.Color('black'), rect)
        rect = pg.Rect(15, 15, self.player.hp, 30)
        pg.draw.rect(self.screen, pg.Color('green'), rect)

        rect = pg.Rect(685, 10, 210, 40)
        pg.draw.rect(self.screen, pg.Color('black'), rect)
        rect = pg.Rect(690, 15, self.enemy.hp, 30)
        pg.draw.rect(self.screen, pg.Color('green'), rect)
        if self.win == self.player:
            text = text_render("ПОБЕДА")
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
            text2 = text_render("press any key")
            text_rect2 = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2+200))
            self.screen.blit(text2, text_rect2)

        elif self.win == self.enemy and self.mode == "two players":
            text = text_render("ПОБЕДА")
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
            text2 = text_render("press any key")
            text_rect2 = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2+200))
            self.screen.blit(text2, text_rect2)
        elif self.win == self.enemy and self.mode == "one player":
            text = text_render("ПОРАЖЕНИЕ")
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
            text2 = text_render("press any key")
            text_rect2 = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2+200))
            self.screen.blit(text2, text_rect2)
        pg.display.flip()



if __name__ == "__main__":
    Menu()