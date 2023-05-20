from pygame import sprite, display, math


class YSortCameraGroup(sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = display.get_surface()
        self.half_width = self.display_surface.get_width() / 2
        self.half_height = self.display_surface.get_height() / 2
        self.offset = math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for s in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = s.rect.topleft - self.offset
            self.display_surface.blit(s.image, offset_pos)
