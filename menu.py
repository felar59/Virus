import pygame

pygame.init()
screen = pygame.display.set_mode((1920, 1080))

class Menu():
    def __init__(self):
        self.terrains = [
            [["x", "x", "x", "x"], ["v", "v", "x"], ["x", "car", "x", "x"], ["v", "car", "x"], ["x", "x", "0", "x"], ["x", "x", "x"], ["x", "x", "x", "x"]], #Lvl 1
            [["x", "x", "car", "d"], ["x", "x", "car"], ["x", "g", "g", "d"], ["x", "0", "x"], ["0", "x", "x", "x"], ["x", "x", "x"], ["x", "x", "x", "x"]], #Lvl 2
            [["x", "x", "x", "x"], ["x", "x", "x"], ["d", "x", "0", "v"], ["g", "x", "x"], ["d", "car", "v", "x"], ["x", "car", "g"], ["0", "x", "x", "x"]], #Lvl 3
            [["x", "u", "x", "0"], ["u", "x", "x"], ["d", "x", "0", "v"], ["g", "x", "x"], ["d", "car", "v", "x"], ["x", "car", "g"], ["0", "x", "x", "x"]], #Lvl 4
            [["r", "v", "v", "x"], ["x", "x", "x"], ["r", "v", "j", "b"], ["j", "j", "b"], ["x", "x", "o", "o"], ["x", "car", "o"], ["x", "x", "car", "x"]], #Lvl 5
        ]
    def backgroundPrint(self, stop):
        if stop == 0 or stop == 1:
            image = pygame.image.load("./PygameAssets/bgLevelSelect.png")
            image_agrandie = pygame.transform.scale(image, (1920, 1080))
            screen.blit(image_agrandie, (0, 0))
        else:
            image = pygame.image.load("./PygameAssets/ReglesBg.png")
            image_agrandie = pygame.transform.scale(image, (1920, 1080))
            screen.blit(image_agrandie, (0, 0))

    def buttonscharge(self, stop):
        if stop == 0:
            boutons = {
                1: {"image": pygame.image.load("./PygameAssets/Buttons/NIVEAUX.png"), "position": (870, 450)},
                2: {"image": pygame.image.load("./PygameAssets/Buttons/RULES.png"), "position": (870, 520)},
            }
        elif stop == 1:
            boutons = {
                1: {"image": pygame.image.load("./PygameAssets/Buttons/STARTER.png"), "position": (750 -5, 470)},
                2: {"image": pygame.image.load("./PygameAssets/Buttons/JUNIOR.png"), "position": (990 -5, 470)},
                3: {"image": pygame.image.load("./PygameAssets/Buttons/EXPERT.png"), "position": (750 -5, 540)},
                4: {"image": pygame.image.load("./PygameAssets/Buttons/MASTER.png"), "position": (990 -5, 540)},
                5: {"image": pygame.image.load("./PygameAssets/Buttons/WIZARD.png"), "position": (1920//2 - 185//2 -5, 610)},
                6: {"image": pygame.image.load("./PygameAssets/Buttons/MENU.png"), "position": (1920//2 - 185//2 -5, 230)},
            }
        elif stop == 3:
            boutons = {
                1: {"image": pygame.image.load("./PygameAssets/Buttons/MENU.png"), "position": (1920//2 - 190//2, 580)},
            }
        return boutons

    def afficher_menu(self, stop):
        self.backgroundPrint(stop)
        boutons = self.buttonscharge(stop)
        for key, bouton in boutons.items():
            screen.blit(bouton["image"], bouton["position"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for key, bouton in boutons.items():
                    rect = bouton["image"].get_rect(topleft=bouton["position"])
                    if rect.collidepoint(mouse_pos):
                        if stop == 0:
                            if key == 1:
                                stop = 1
                            if key == 2:
                                stop = 3
                        elif stop == 1:
                            if key == 6:
                                stop = 0
                            else:
                                #copie d'un niveau sans liée les valeurs pour pouvoir refaire le niveau du début si on retourne dessus
                                terrain = [row[:] for row in self.terrains[key - 1]]
                                stop = 2
                                return stop, terrain
                        elif stop == 3:
                            if key == 1:
                                stop = 0
        return stop, None
