import pygame

from choices import CollisionDirection


class BaseModel(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite, hitbox_x=-1, hitbox_y=-10):
        super().__init__(groups)
        self.image = pygame.image.load(sprite).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()
        self.hitbox = self.rect.inflate(hitbox_x, hitbox_y)


class CharacterBaseModel(BaseModel):
    def __init__(self, obstacle_sprites: 'pygame.sprite.Group', **kwargs):
        super().__init__(**kwargs)
        self.obstacle_sprites = obstacle_sprites

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

            if self.direction.x != 0:
                self.hitbox.x += self.direction.x * speed
                self.collision(CollisionDirection.HORIZONTAL)

            if self.direction.y != 0:
                self.hitbox.y += self.direction.y * speed
                self.collision(CollisionDirection.VERTICAL)

            self.rect.center = self.hitbox.center

    def collision(self, direction):
        collision_sprites = pygame.sprite.spritecollide(self, self.obstacle_sprites, False)

        if collision_sprites:
            for sprite in collision_sprites:
                if direction == CollisionDirection.HORIZONTAL:
                    if sprite.hitbox.colliderect(self.hitbox):  # sempre retornando true
                        if self.direction.x > 0:  # movendo para direita
                            self.hitbox.right = sprite.hitbox.left
                        elif self.direction.x < 0:  # movendo para esquerda
                            self.hitbox.left = sprite.hitbox.right

                if direction == CollisionDirection.VERTICAL:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.y < 0:  # movendo para cima
                            self.hitbox.top = sprite.hitbox.bottom
                        elif self.direction.y > 0:  # movendo para baixo
                            self.hitbox.bottom = sprite.hitbox.top


class Tile(BaseModel):
    def __init__(self, pos, groups):
        super().__init__(pos=pos, groups=groups, sprite='graphics/sprites/Rock4_grass_shadow_dark1.png')


class Player(CharacterBaseModel):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(obstacle_sprites=obstacle_sprites, pos=pos, groups=groups,  sprite='graphics/sprites/main_character_front.png', hitbox_y=-30)
        self.speed = 5

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def update(self, *args, **kwargs) -> None:
        self.input()
        self.move(self.speed)
