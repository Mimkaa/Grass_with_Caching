import pygame as pg
import math
from settings import *
import random

vec=pg.Vector2



def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)





class Grass_Tile:
    def __init__(self,game,pos,tilesize,index):
        self.tilezise=tilesize
        self.pos=vec(pos)
        self.images=[]
        self.index=index
        self.rect=pg.Rect(self.pos.x,self.pos.y,tilesize,tilesize)
        self.grass = []
        self.hit_rect=self.rect.copy()
        self.current_frame = 0
        self.last_update = 0
        for i in range(10):
            width=10
            height=100
            val=translate(i,0,10,0,255)
            color=[255-val,255,0]
            self.grass.append(
                Grass(game,[random.randint(5,self.rect.width-5),random.randint(0,self.rect.width)],
                      [[-width/2, 0], [0, -height], [width/2, 0]],self.index,width,height,color))
        for g in self.grass:
            g.budge(self.pos)
        self.angle=0
        self.create_images()
        self.animation=False





    def record_var2(self,start_angle,number,gravity,dir=vec(1,0)):
        # leaning forward
        angle = start_angle
        result = []
        for i in range(number):
            all_points = []

            sorted_grass = sorted(self.grass, key=lambda x: x.pos.y)
            for g in sorted_grass:
                points = [p for p in g.points]
                for n, point in enumerate(points):
                    points[n].x = (g.originals[n].x * math.cos(angle) - g.originals[n].y * math.sin(
                        angle))
                    points[n].y = (g.originals[n].x * math.sin(angle) + g.originals[n].y * math.cos(
                        angle))
                all_points += [v + (g.pos - self.pos) for v in points]
            x_vals = [v.x for v in all_points]
            y_vals = [v.y for v in all_points]
            min_x = min(x_vals)
            min_y = min(y_vals)
            max_x = max(x_vals)
            max_y = max(y_vals)
            width = max_x - min_x
            height = max_y - min_y

            img_all_grass = pg.Surface((width,height),pg.SRCALPHA)

            for g in sorted_grass:
                points = [p for p in g.points]
                for n, point in enumerate(points):
                    points[n].x = (g.originals[n].x * math.cos(angle) - g.originals[n].y * math.sin(
                        angle))
                    points[n].y = (g.originals[n].x * math.sin(angle) + g.originals[n].y * math.cos(
                        angle))

                points = [p - vec(min_x, min_y) + (g.pos - self.pos) for p in g.points]

                color_var = 255 - translate(abs(angle), 0, math.pi * 2, 0, 500)
                if color_var < 100:
                    color_var = 100
                color=[int(i * (color_var/255))for i in list(g.color)]
                pg.draw.polygon(img_all_grass, color, points)
                #pg.draw.polygon(img_all_grass, BLACK, points, 1)



            result.append([(min_x,min_y),img_all_grass,angle])

            if dir==vec(1,0):
                angle += 0.1
            else:
                angle-=0.1

        # moving under integration
        vel=0
        force = gravity * math.sin(angle)
        dt=(1000/FPS)/1000
        acc = (-1 * force) /100
        vel += acc * dt
        angle += vel * dt
        vel *= 0.83


        while abs(vel)>0.01:
            all_points = []

            sorted_grass = sorted(self.grass, key=lambda x: x.pos.y)
            for g in sorted_grass:
                points = [p for p in g.points]
                for n, point in enumerate(points):
                    points[n].x = (g.originals[n].x * math.cos(angle) - g.originals[n].y * math.sin(
                        angle))
                    points[n].y = (g.originals[n].x * math.sin(angle) + g.originals[n].y * math.cos(
                        angle))
                all_points += [v + (g.pos - self.pos) for v in points]
            x_vals = [v.x for v in all_points]
            y_vals = [v.y for v in all_points]
            min_x = min(x_vals)
            min_y = min(y_vals)
            max_x = max(x_vals)
            max_y = max(y_vals)
            width = max_x - min_x
            height = max_y - min_y

            img_all_grass = pg.Surface((width, height), pg.SRCALPHA)

            for g in sorted_grass:
                points = [p for p in g.points]
                for n, point in enumerate(points):
                    points[n].x = (g.originals[n].x * math.cos(angle) - g.originals[n].y * math.sin(
                        angle))
                    points[n].y = (g.originals[n].x * math.sin(angle) + g.originals[n].y * math.cos(
                        angle))

                points = [p - vec(min_x, min_y) + (g.pos - self.pos) for p in g.points]

                color_var = 255 - translate(abs(angle), 0, math.pi * 2, 0, 500)
                if color_var < 100:
                    color_var = 100
                color = [int(i * (color_var / 255)) for i in list(g.color)]
                pg.draw.polygon(img_all_grass, color, points)
                #pg.draw.polygon(img_all_grass, BLACK, points, 1)

            result.append([(min_x,min_y),img_all_grass,angle])

            dt = (1000 / FPS) / 1000
            force = gravity * math.sin(angle)
            acc = (-1 * force) / 100
            vel += acc * dt
            angle += vel * dt
            vel *= 0.83


        return result

    def create_images(self):
        if not self.images:
            self.images=self.record_var2(0,5,7500)


    def update(self,wind):
        now = pg.time.get_ticks()
        if not self.animation and self.hit_rect.colliderect(wind.rect):
            self.animation=True

        if not self.animation:
            self.current_frame=0

        else:
            if now - self.last_update > 30:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.images)

            if self.current_frame == len(self.images) - 1:
                self.animation = False
                self.current_frame = -1
            # adjusting for the case when wind blows a little earlier than animation ends
            if self.hit_rect.colliderect(wind.hit_rect) and self.current_frame > int(len(self.images) * 0.5):
                self.current_frame = 0



    def draw(self,surf):

        frames=tuple([f[1] for f in self.images])
        positions=tuple([f[0] for f in self.images])
        angles=tuple([f[2] for f in self.images])


        surf.blit(frames[self.current_frame],vec(self.rect.topleft) + positions[self.current_frame])
        self.angle=angles[self.current_frame]












class Wind(pg.sprite.Sprite):
    def __init__(self,game,pos,width,height):
        self.hit_rect=pg.Rect(0,0,width,height)
        self.game=game
        self.groups=self.game.all_sprites
        super().__init__(self.groups)
        self.pos=vec(pos)
        self.hit_rect.center=self.pos
        self.vel=vec(0,0)
        self.speed=400
        self.image=pg.Surface((width,height),pg.SRCALPHA)
        self.rect=self.hit_rect.copy()
    def update(self):
        self.vel=vec(self.speed*self.game.dt,0)
        self.pos+=self.vel
        self.vel.x+=self.speed
        if self.pos.x>WIDTH:
            self.pos.x=0
        self.hit_rect.center=self.pos
        self.rect.center=self.pos
    def draw(self,surf):
        pass



class Grass:
    def __init__(self,game,pos,points,index,width,height,color):
        self.pos=vec(pos)
        self.color=color
        self.originals=tuple([vec(i) for i in points])
        self.points=[vec(i) for i in points]
        self.acc=0
        self.vel=0
        self.gravity=8500
        self.angle=0
        self.tile=index
        self.game=game
        self.width=width
        self.height=height

        self.angle_to_add=0
        self.acc_to_add = 0
        self.vel_to_add = 0



    def wind_reaction(self,obj):
        if obj.hit_rect.colliderect(self.rect):
            self.angle_to_add+=0.03





    def add_angle(self,angle):

        self.angle+=angle
        if self.angle > math.pi / 2:
            self.angle = math.pi / 2
        elif self.angle < -math.pi / 2:
            self.angle = -math.pi / 2


    def rotate_following(self,obj):

        force = self.gravity * math.sin(self.angle)
        self.acc = ((-1 * force) / self.height)
        self.vel += self.acc * self.game.dt
        self.angle += self.vel * self.game.dt

        self.vel *= 0.83
        if abs(self.angle) < 0.1:
            self.reset()

        # integration but for wind
        force2 = self.gravity * math.sin(self.angle_to_add)
        self.acc_to_add = ((-1 * force2) / self.height)
        self.vel_to_add += self.acc_to_add * self.game.dt
        self.angle_to_add += self.vel_to_add * self.game.dt

        self.vel_to_add *= 0.83

        if abs(self.angle_to_add) < 0.02:
            self.acc_to_add=0
            self.vel_to_add=0
            self.angle_to_add=0



        if (obj.circle_pos.x-self.pos.x)**2+(obj.circle_pos.y-self.pos.y)**2<obj.radius**2:
            point_vec =  self.pos - obj.circle_pos
            self.angle = math.sin(math.atan2(point_vec.x, point_vec.y))+self.angle_to_add
        else:
            self.angle=self.angle_to_add




    def reset(self):
        self.vel=0
        self.angle=0
        self.acc=0

    def budge(self,pos):
        self.pos+=pos

    def render(self):
        points = [v.copy() for v in self.originals]
        for n, point in enumerate(points):
            points[n].x = (self.originals[n].x * math.cos(self.angle) - self.originals[n].y * math.sin(
                self.angle))
            points[n].y = (self.originals[n].x * math.sin(self.angle) + self.originals[n].y * math.cos(
                self.angle))
        x_vals = [v.x for v in points]
        y_vals = [v.y for v in points]
        min_x = min(x_vals)
        min_y = min(y_vals)
        max_x = max(x_vals)
        max_y = max(y_vals)
        width = max_x - min_x
        height = max_y - min_y
        image = pg.Surface((width+1, height+1),pg.SRCALPHA)

        points=tuple([v-vec(min_x,min_y) for v in points])
        # rendering
        color_var=255-translate(abs(self.angle),0,math.pi*2,0,500)
        if color_var<100:
            color_var=100
        color = [int(i * (color_var / 255)) for i in list(self.color)]
        pg.draw.polygon(image,color,points)

        pointer=(points[0]+points[2])/2

        offset=vec(width/2,height/2)-pointer
        return image,offset

    def update(self):
        self.image,offset=self.render()
        self.rect=self.image.get_rect()
        self.rect.center=self.pos+offset
        self.hit_rect = pg.Rect(0, 0, self.width, self.width)

        self.hit_rect.center=self.pos-vec(0,self.width/2)


    def draw(self,surf):
        surf.blit(self.image,self.rect)


        # color_var=255-translate(abs(self.angle),0,math.pi*2,0,500)
        # if color_var<100:
        #     color_var=100
        #
        # pg.draw.polygon(surf,(0,int(color_var),0),self.points)
        #pg.draw.polygon(surf, BLACK, self.points,1)
















