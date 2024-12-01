import pygame

pygame.init()

# Classe Terrain pour gérer les éléments du terrain, Génération / Affichage
class Terrain:
    def __init__(self):
        self.terrain = None # Definie après avoir selectionné le niveau
        self.load_assets()
            
    def load_assets(self):
        # Charger les images et redimensionner
        self.virus_agrandie = pygame.transform.scale(pygame.image.load("./PygameAssets/carte-mere.png"), (100, 100))
        self.virus_back_agrandie = pygame.transform.scale(pygame.image.load("./PygameAssets/carte-mere-back.png"), (102, 102))
        self.vide_agrandie = pygame.transform.scale(pygame.image.load("./PygameAssets/vide.png"), (100, 100))
        self.Globule_Back_agrandie = pygame.transform.scale(pygame.image.load("./PygameAssets/Globule_Back.png"), (102, 102))
        
        self.back_empty = pygame.transform.scale(pygame.image.load("./PygameAssets/BACK_EMPTY.png"), (1920, 1080))
        
        self.Globules = self.load_globules() #pour tout ce qui n'est pas cases_vide/virus/block_solid utilisé des texure de virus pareille de diferante couleur
        self.block = pygame.transform.scale(pygame.image.load("./PygameAssets/ai-cerveau.png"), (100, 100))

    def load_globules(self):
        # Avec les 6 images de globules je les ranges dans un dictionnaire en fesant une boucle for pour pas prendre trop de place
        globules = {}
        for x in range(1, 7):
            globule_path = f"./PygameAssets/Globule_{x}.png" # Nom des fichier numérotés de 1 à 6 Globule_1, 2 ...
            globule = pygame.image.load(globule_path)
            globules[x] = pygame.transform.scale(globule, (100, 100))
        return globules
    
    def draw(self, screen, selected, tab_index):
        screen.blit(self.back_empty, (0,0)) # Fond du menu mais en écarter pour laisser de la place pour le jeu

        for i in range(len(self.terrain)):
            for y in range(len(self.terrain[i])):
                # Le modulo 4 c'est car le terrain c'est une liste de liste qui alter de taille 4, 3, donc en fonction de si c'est 4 ou 3 ils sont placés differament
                if len(self.terrain[i]) % 4 != 0:
                    self.draw_element(screen, selected, tab_index, i, y, 770, 240)
                else:
                    self.draw_element(screen, selected, tab_index, i, y, 700, 240)
    
    def draw_element(self, screen, selected, tab_index, i, y, x, z):
        # Mettre un fond blanc derrière le globule/virus déplacable, de 2px plus grand donc je décale de 1 px d'ou le -1
        if selected[tab_index] == self.terrain[i][y]:
            if selected[tab_index] == "car":
                screen.blit(self.virus_back_agrandie, ((y * 140 + x -1), (i * 75 + z -1)))
            else:
                screen.blit(self.Globule_Back_agrandie, ((y * 140 + x -1), (i * 75 + z -1)))
        # Mettre image de case vide si il y a "x" en [i][y]
        if self.terrain[i][y] == "x":
            screen.blit(self.vide_agrandie, (y * 140 + x, i * 75 + z))
        # Mettre image de block_solid si il y a "0" en [i][y]
        elif self.terrain[i][y] == "0":
            screen.blit(self.block, (y * 140 + x, i * 75 + z))
        # Mettre image de virus si il y a "car" en [i][y]
        elif self.terrain[i][y] == "car":
            screen.blit(self.virus_agrandie, (y * 140 + x, i * 75 + z))
        else:
            # Pour la longueur du nombre de globule qui n'est pas le virus prendre une texture de globule
            for v in range(len(selected)):
                if selected[v] == self.terrain[i][y]:
                    screen.blit(self.Globules[v], (y * 140 + x, i * 75 + z))
        
    def buttonResetAndMenu(self, screen):
        screen.blit(pygame.image.load("./PygameAssets/Buttons/RESTART.png"), (1920//2 - 250 -218//2, 900))
        screen.blit(pygame.image.load("./PygameAssets/Buttons/MENU.png"), (1920//2 + 250 -218//2, 900))
