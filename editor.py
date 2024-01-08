import sys

import pygame

#from scripts.utils import load_image #, load_images, Animation
#from scripts.entities import PhysicsEntity, Player
#from scripts.cloud import Clouds
from scripts.utils import load_images
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0

class Editor:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Editor mode')
        self.screen = pygame.display.set_mode((640, 480)) #set the size of the display

        self.display = pygame.Surface((320, 240)) #the surface we want the game to run on/ camera angle

        self.clock = pygame.time.Clock() #FRAME RATE   
    
        """
            *Demonstrate how image was loaded and change and move around*

        game.img = pygame.image.load('data/images/clouds/cloud_1.png')
        game.img.set_colorkey((0, 0, 0))

        game.img_pos = [160, 260]

        game.collision_area = pygame.Rect(50, 50, 300, 50)
        """

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'spawners': load_images('tiles/spawners'),
            #'player': load_image('entities/player.png'),
            #'background': load_image('background.png'),
            #'clouds' : load_images('clouds'),
            #'player/idle': Animation(load_images('entities/player/idle'), img_dur = 6),
            #'player/run': Animation(load_images('entities/player/run'), img_dur = 4),
            #'player/jump': Animation(load_images('entities/player/jump')),
            #'player/slide': Animation(load_images('entities/player/slide')),
            #'player/wall_slide': Animation(load_images('entities/player/wall_slide'))
        }

        self.movement = [False, False, False, False]

        """
        self.clouds = Clouds(self.assets['clouds'], count=16)

        #print(game.assets)

        #self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15)) 

        #change line 52 to new line after making Player class
        self.player = Player(self, (50,50), (8, 15))"""
        
        self.tilemap = Tilemap(self, tile_size=16)

        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass
        
    
        self.camera = [0, 0]
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.shift = False 
        self.ongrid = True
    
    def run(self):
        while True:
            #self.display.fill((14, 219, 248)) #render everything in order according to what we want which to go first (first in below, last in ontop)
            self.display.fill((0, 0, 0))
            """
            self.camera[0] += (self.player.rect().centerx - self.display.get_width() / 2 -self.camera[0])
            self.camera[1] += (self.player.rect().centery - self.display.get_height() / 2 -self.camera[1])
            render_camera = (int(self.camera[0]), int(self.camera[1]))

            self.clouds.update()
            self.clouds.render(self.display, offset = render_camera)

            self.tilemap.render(self.display, offset =  render_camera)

            #add tilemap
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0)) #since we want to move left and right we only using X-axis
            self.player.render(self.display, offset =  render_camera)                              # so Y-axis set at 0
            """
            """
            img_r = pygame.Rect(game.img_pos[0], game.img_pos[1], game.img.get_width(), game.img.get_height())
            if img_r.colliderect(game.collision_area):
                pygame.draw.rect(game.screen, (0, 100, 255), game.collision_area)
            else: 
                pygame.draw.rect(game.screen, (0, 50, 255), game.collision_area)

            game.img_pos[1] += (game.movement[1] - game.movement[0]) *5
            game.screen.blit(game.img, game.img_pos)
            
            
            #print(self.tilemap.physics_rects_around(self.player.pos)) test to see the value pass through
            """
            self.camera[0] += (self.movement[1] - self.movement[0]) * 2 #move camera around
            self.camera[1] += (self.movement[3] - self.movement[2]) * 2

            render_camera = (int(self.camera[0]), int(self.camera[1]))

            self.tilemap.render(self.display, offset=render_camera)
            
            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)

            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = (mouse_pos[0] / RENDER_SCALE, mouse_pos[1] / RENDER_SCALE)
            tile_pos = (int((mouse_pos[0] + self.camera[0]) // self.tilemap.tile_size), int ((mouse_pos[1] + self.camera[1]) // self.tilemap.tile_size))

            if self.ongrid: 
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.camera[0], tile_pos[1] * self.tilemap.tile_size - self.camera[1]))
            else:
                self.display.blit(current_tile_img, mouse_pos)

            
            if self.clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
            if self.right_clicking:
                tile_location = str(tile_pos[0]) + ';' + str (tile_pos[1])
                if tile_location in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_location]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.camera[0], tile['pos'][1] - self.camera[1], tile_img.get_width(), tile_img.get_height()) #delete the grid img base their side, position and height
                    if tile_r.collidepoint(mouse_pos):
                        self.tilemap.offgrid_tiles.remove(tile)

            self.display.blit(current_tile_img, (5, 5))

            for event in pygame.event.get():      
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:   #from to line 134 is creating a custom window that we can build a Level
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (mouse_pos[0] + self.camera[0], mouse_pos[1] + self.camera[1])})
                    if event.button == 3:
                        self.right_clicking = True 
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False

                if event.type == pygame.KEYDOWN: #if the player press key turn true
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if event.key == pygame.K_o: #key to store output
                        self.tilemap.save('map.json')
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                if event.type == pygame.KEYUP: #if the player release the key turn false
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False 
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Editor().run()