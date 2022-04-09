import pygame as pg
vec=pg.Vector2
from settings import *
class Testing:
    def __init__(self,game,pos):
        self.game=game


        self.pos=vec(pos)
        self.vel=vec(0,0)
        surf=pg.Surface((50,50))
        surf.fill(YELLOW)
        self.image=surf
        self.rect=self.image.get_rect()
        pg.draw.rect(self.image,BLACK,self.rect,1)
        self.image.convert_alpha()
        self.speed=300

        self.hit_rect=self.rect.copy()
        self.hit_rect.height=self.rect.height/2
        self._layer = self.hit_rect.bottom
        self.dir_vec=vec(0,0)
        self.rect.center = self.pos
        self.hit_rect.bottom = self.rect.bottom
        self.hit_rect.centerx = self.rect.centerx
        self.circle_pos=vec(self.hit_rect.center)
        self.radius=60

    def get_keys(self):
        self.vel = vec(0, 0)
        #if not self.eat and self.game.cutscene_manager.cut_scene==None and self.game.current_character==self.name:
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vel.x = -self.speed
            self.dir_vec=vec(-1,0)
        if keys[pg.K_RIGHT] :
            self.vel.x = self.speed
            self.dir_vec = vec(1, 0)
        if keys[pg.K_UP] :
            self.vel.y = -self.speed
            self.dir_vec = vec(0, -1)
        if keys[pg.K_DOWN] :
            self.vel.y = self.speed
            self.dir_vec = vec(0, 1)

    def update(self):
        self.get_keys()

        self.pos+=self.vel*self.game.dt
        self.rect.center=self.pos
        self.hit_rect.bottom=self.rect.bottom
        self.hit_rect.centerx=self.rect.centerx
        self.circle_pos=vec(self.hit_rect.center)
    def draw(self,surf):
        surf.blit(self.image,self.rect)