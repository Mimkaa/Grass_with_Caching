import pygame as pg
import sys
from settings import *
from objects import *
from os import path
from testing import *
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.draw_cache=False
        self.draw_tiles_checking=False
        self.draw_rects=False
        self.draw_hit_rects=False

    def load_data(self):
        self.font=path.join("PixelatedRegular-aLKm.ttf")
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.testing=Testing(self,(WIDTH//2,HEIGHT//2))

        #self.wind=Wind(self,(WIDTH/2,HEIGHT/2),WIDTH/20,HEIGHT)
        self.world={}
        for i in range((WIDTH // TILESIZE) * (HEIGHT // TILESIZE)):
            coord = self.from_1d_to_2d(i)
            tile = Grass_Tile(self, coord, TILESIZE, len([i for i in list(self.world.values()) if i]))
            self.world[self.from_1d_to_2d(i)]=(tile,tuple(tile.grass.copy()))
            tile.grass.clear()
        self.to_check=[]
        self.memory_pos=[]

        # for grass-wind animation
        self.current_frame=0
        self.last_update=0
        self.wind = Wind(self, (WIDTH / 2, HEIGHT / 2), WIDTH / 20, HEIGHT)


    def from_1d_to_2d(self,index):
        x = index % (WIDTH//TILESIZE)
        y = index//(WIDTH//TILESIZE)
        return (x*TILESIZE,y*TILESIZE)

    def create_cell(self):
        mx, my = pg.mouse.get_pos()
        # getting coord in 1d
        index = int((my // TILESIZE) * WIDTH / TILESIZE + (mx // TILESIZE))
        coord=self.from_1d_to_2d(index)
        tile=Grass_Tile(self,coord,TILESIZE,len([i for i in list(self.world.values()) if i ]))
        if coord in (self.world.keys()) :
            if not self.world[coord]:
                self.world[coord]=(tile,tuple(tile.grass.copy()))
                tile.grass.clear()
            else:
                self.world[coord]=None




    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def in_bound(self,coords):
        return True if -TILESIZE<coords[0]<WIDTH and -TILESIZE<coords[1]<HEIGHT else False

    def any_action(self,objects):
        any_action=False
        for obj in objects:
            if abs(obj.angle) > 0.1:
                any_action=True
        return any_action

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.testing.update()

        # update the current frame
        values=[i[0] for i in list(self.world.values()) if i]

        if values:
            length_images=len(values[0].images)

            now=pg.time.get_ticks()
            if now - self.last_update > 30:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % length_images

            if self.current_frame==length_images-1 :
                self.current_frame=-1







        # get tiles
        tile_testing_pos=vec(self.testing.pos.x//TILESIZE,self.testing.pos.y//TILESIZE)
        directions = [vec(1, 0), vec(-1, 0), vec(0, -1), vec(0, 1), vec(1, 1),
                      vec(1, -1), vec(-1, -1),
                      vec(-1, 1),vec(0,0)]
        #directions=[vec(0,0)]

        to_check=[tuple((tile_testing_pos*TILESIZE)+i*TILESIZE) for i in directions]

        self.to_check=list(filter(self.in_bound,to_check))

        # adding tiles to the list of visited tiles(in the memory where we were)
        for c in self.to_check:
            if c not in self.memory_pos:
                self.memory_pos.append(c)



        active_tiles=[self.world[g][1] for g in self.memory_pos if self.world[g]]

        if active_tiles:
            grass=[g for grass in active_tiles for g in grass]
            for g in grass:
                g.update()
                g.rotate_following(self.testing)
                g.wind_reaction(self.wind)

        # synchronization of all grass_tiles
        not_active_tiles = [self.world[t][0] for t in self.world.keys() if self.world[t]]
        if  not_active_tiles:
            for t in not_active_tiles:
                t.update(self.wind)

        # popping all tiles where grass is idle from memory_pos
        for n, tile in enumerate(self.memory_pos):
            if not self.world[tile] or self.world[tile] and not self.any_action(self.world[tile][1]):
                if tile not in self.to_check:
                    self.memory_pos.pop(n)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        #self.draw_grid()
        self.all_sprites.draw(self.screen)
        all_objects_draw=[]
        self.testing.draw(self.screen)
        all_objects_draw.append(self.testing)

        #draw_grass
        active_tiles = [self.world[g][1] for g in self.memory_pos if self.world[g]]
        if active_tiles:
            grass=[g for grass in active_tiles for g in grass]
            for g in grass:
                all_objects_draw.append(g)

        # draw tiles
        not_to_check = [i for i in list(self.world.keys()) if i not in self.memory_pos]
        not_active_tiles = [self.world[t][0] for t in not_to_check if self.world[t]]
        if not_active_tiles:
            for tile in not_active_tiles:
                all_objects_draw.append(tile)


        all_objects_draw=sorted(all_objects_draw,key=lambda x: x.rect.bottom)

        for obj in all_objects_draw:
            obj.draw(self.screen)

        # draw rects that are currently checked and grass of which is updated
        if self.draw_tiles_checking:
            for c in self.to_check:
                pg.draw.rect(self.screen,BLUE,(c[0],c[1],TILESIZE,TILESIZE),1)

        # draw cached tiles
        if self.draw_cache:
            for c in not_to_check:
                pg.draw.rect(self.screen,RED,(c[0],c[1],TILESIZE,TILESIZE),1)

        # draw hit_rects:
        if self.draw_hit_rects:
            gg=[g for grass in active_tiles for g in grass]
            objs=gg+not_active_tiles
            for ob in objs:
                pg.draw.rect(self.screen,BLUE,ob.hit_rect,1)
        # draw rects
        if self.draw_rects:
            gg = [g for grass in active_tiles for g in grass]
            objs = gg + not_active_tiles
            for ob in objs:
                pg.draw.rect(self.screen, YELLOW, ob.rect, 1)

        # fps
        self.draw_text(str(int(self.clock.get_fps())), self.font, 40, WHITE, 50, 50, align="center")


        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.MOUSEBUTTONUP:
                self.create_cell()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key==pg.K_c:
                    self.draw_tiles_checking=not self.draw_tiles_checking
                if event.key==pg.K_x:
                    self.draw_cache=not self.draw_cache
                if event.key==pg.K_h:
                    self.draw_hit_rects=not self.draw_hit_rects
                if event.key==pg.K_r:
                    self.draw_rects=not self.draw_rects

                



# create the game object
g = Game()
g.new()
g.run()
