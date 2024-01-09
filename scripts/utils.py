import os

import pygame

BASE_IMG_PATH = 'data/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert() #using convert to optimize the memory using by the machine.
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path): #make a seperate function that loads all the images needed
    images = []
    # one thing to remember is that we using sorted here because " os.listdir(BASE_IMG_PATH + path)" maybe behave differently on different os system
    # so using sorted can fix this issue and make everything run consistent on every OS.
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)): #using for loop to loop through the list and find the name the match the variable
        images.append(load_image(path + '/' + img_name)) #then add them in the list.
    return images

class Animation:
                #(     list of image, how many frame image gonna stay)
    def __init__(self, images, img_dur=5, loop = True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop) #we reuse the same image to optimize the memory
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images)) #in case the frame pass the index of the image we will make it loop around 
        else:
            self.frame = min(self.frame +1, self.img_duration * len(self.images) - 1) #since index start at 0
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self): #instead of rendering the img to the screen, we will get the img and do wat we want with it which is more flexiable
        return self.images[int(self.frame / self.img_duration)] #fram here frame of the game
