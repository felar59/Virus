import pygame
import menu
import terrain
import time
import random

pygame.init()
# Classe Game pour gérer le jeu
class Game:
    def __init__(self):
        # Initialisation de variables
        screen_info = pygame.display.Info()

        screen_width = screen_info.current_w
        screen_height = screen_info.current_h

        self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.terrain = terrain.Terrain()
        self.menu = menu.Menu()
        self.running = True
        self.stop = 0
        
        self.tab = 0
        # Initialisation du module de mixage (son)
        pygame.mixer.init()

        # Chargement des fichier audio (.wav)
        self.randBloop = [pygame.mixer.Sound('sounds/bloop1.wav'), pygame.mixer.Sound('sounds/bloop2.wav'), pygame.mixer.Sound('sounds/bloop3.wav')]

        backgroundSong = pygame.mixer.Sound('sounds/EdgeOfSanity.wav')
        backgroundSong.play(loops=50)

        self.stopTemps = 0
        self.startTemps = 0
        self.nbrCoup = 0
        
        self.AllGoodRecursion = False
        self.reseTerrain = None

        self.selected = {}

    def run(self):
        # Boucle principale 
        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                if self.terrain.terrain is not None:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if self.terrain.terrain[0][0] == "car" and self.terrain.terrain[1][0] == "car":
                            # Bouton Ecran de victoire
                            if self.rect.collidepoint(mouse_pos):
                                self.stop, self.stopTemps, self.startTemps, self.nbrCoup = 0, 0, 0, 0 #met le menu reset le temps et le nbr de coup
                        else:
                            # Boutons en Game
                            if self.rectMenuGame.collidepoint(mouse_pos):
                                self.stop, self.stopTemps, self.startTemps, self.nbrCoup = 0, 0, 0, 0 #met le menu reset le temps et le nbr de coup
                            if self.rectResetGame.collidepoint(mouse_pos):
                                self.terrain.terrain = [row[:] for row in self.reseTerrain] # définir par ligne sinon les listes son "liée"
                                self.stopTemps, self.startTemps, self.nbrCoup = 0, 0, 0 # reset le temps4
                                
            self.mettreajour_screen()
            pygame.display.flip()

    def mettreajour_screen(self):
        keys = pygame.key.get_pressed()
        # Si pas de niveau séléctionne afficher menu
        if self.stop == 0 or self.stop == 1 or self.stop == 3:
            self.stop, self.terrain.terrain = self.menu.afficher_menu(self.stop)
            if self.terrain.terrain is not None:
                self.selected = self.element_select()
                self.reseTerrain = [row[:] for row in self.terrain.terrain] # définir par ligne sinon les listes son "liée"

        # Si je gagne affiche les stats et tout..
        if self.stop == 2 and self.terrain.terrain is not None:

            if self.startTemps == 0:
                self.startTemps = time.time()

            # Si le virus est dans le coin en haut à gauche afficher "you win"
            if self.terrain.terrain[0][0] == "car" and self.terrain.terrain[1][0] == "car":
                self.terrain.draw(self.screen, self.selected, self.tab)
    
                self.endTemps = time.time()

                #  image de fond
                self.screen.blit(pygame.transform.scale(pygame.image.load("./PygameAssets/TableauScore.png"), (550, 600)), (1920//2 - 550/2, 1080//2 - 600/2))

                # écriture gg
                self.font = pygame.font.Font('freesansbold.ttf', 32)
                self.textWin = self.font.render('GG', True, (173,216,230))
                self.text_rect = self.textWin.get_rect(center=(1920 // 2, 1080 // 2 - 200))
                self.screen.blit(self.textWin, self.text_rect)

                # écriture nbr de coup
                self.font = pygame.font.Font('freesansbold.ttf', 32)
                self.textCoup = self.font.render(f'Nombre de coups : {self.nbrCoup}', True, (173,216,230))
                self.text_rect_Coup = self.textCoup.get_rect(center=(1920 // 2, 1080 // 2 - 50))
                self.screen.blit(self.textCoup, self.text_rect_Coup)

                # écriture temps
                if self.stopTemps == 0:
                    self.tempstotal = self.endTemps - self.startTemps
                    self.stopTemps += 1
                    if self.tempstotal > 60:
                        self.ecrieTempstotal = f"{self.tempstotal//60:.0f} min {self.tempstotal%60:.3f} sec"
                    else:
                        self.ecrieTempstotal = f"{self.tempstotal:.3f} sec"
                self.font = pygame.font.Font('freesansbold.ttf', 32)
                self.textTemps = self.font.render(f'Temps : {self.ecrieTempstotal}', True, (173,216,230))
                self.text_rect_Temsp = self.textTemps.get_rect(center=(1920 // 2, 1080 // 2 + 100))
                self.screen.blit(self.textTemps, self.text_rect_Temsp)

                # bouton menu
                self.screen.blit(pygame.image.load("./PygameAssets/Buttons/MENU.png"), (1920//2 - 218//2, 730))
                self.rect = pygame.image.load("./PygameAssets/Buttons/MENU.png").get_rect(topleft=(1920//2 - 218//2, 730))
            else:
                self.mouvement(keys, self.selected, self.tab)
                self.terrain.draw(self.screen, self.selected, self.tab)
                self.terrain.buttonResetAndMenu(self.screen)
                
                self.rectResetGame = pygame.image.load("./PygameAssets/Buttons/RESTART.png").get_rect(topleft=(1920//2 - 250 -218//2, 900))   
                self.rectMenuGame = pygame.image.load("./PygameAssets/Buttons/MENU.png").get_rect(topleft=(1920//2 + 260 -218//2, 900))


    def element_select(self):
        '''
        Permet de séléctionner les élément qui sont bougable dans un dictionnaire, en fonction du niveau qui est choisis 
        ( parcour le terrain et vois si c'est differant de 0 et x (cases solid et vide))
        Variable qui sera utiliser pour séléctionner la "piece" qu'on veut bouger
        '''
        x = 1
        selected_index = {0: "car"}
        for i in range(len(self.terrain.terrain)):
            for y in range(len(self.terrain.terrain[i])):
                if self.terrain.terrain[i][y] not in ["x", "0", "car"] and self.terrain.terrain[i][y] not in selected_index.values():
                    selected_index[x] = self.terrain.terrain[i][y]
                    x += 1
        return selected_index
    

    def mouvement(self, keys, selected, tab):
        '''
        Pour chaque déplacement appele la fonction moveMolecule
        Pour tab juste change la variable tab
        Variable Good sert a faire que si j'appuie une fois sa compte comme 1 fois et pas itére plusieurs fois l'action
        '''
        if keys[pygame.K_a] and self.Good == True:
            self.directionListe = 0 
            self.AllGoodRecursion = True
            self.otherPiece, self.alreadyTest = [], []
            self.moveMolecule(selected[tab], [-1, -1, -1, 0], 1)
            self.Good = False

        if keys[pygame.K_z] and self.Good == True:
            self.directionListe = 0
            self.AllGoodRecursion = True
            self.otherPiece, self.alreadyTest = [], []
            self.moveMolecule(selected[tab], [-1, 0, -1, 1], 1)
            self.Good = False

        if keys[pygame.K_q] and self.Good == True:
            self.directionListe = -1
            self.AllGoodRecursion = True
            self.otherPiece, self.alreadyTest = [], []
            self.moveMolecule(selected[tab], [1, -1, 1, 0], 1)
            self.Good = False

        if keys[pygame.K_s] and self.Good == True:
            self.directionListe = -1
            self.AllGoodRecursion = True
            self.otherPiece, self.alreadyTest = [], []
            self.moveMolecule(selected[tab], [1, 0, 1, 1], 1)
            self.Good = False

        # Si aucun bouton est pressé Good = True donc une action peux être refaite
        if not any(keys):
            self.Good = True

        if keys[pygame.K_TAB] and self.Good == True:
            if len(selected) - 1 == tab:
                self.tab = 0
                self.Good = False
            else:
                self.tab += 1
                self.Good = False

    def moveMolecule(self, select, posxy_xy2, makeAmove = 0):
        '''
        select c'est pour savoir quel element bouger
        posxy_xy2[0], posxy_xy2[1] c'est pour déplacer de haut en bas dans un ces cas là:
            [x, x, x]
           [x, x, x ,x] on cherche a déplacer un element ici en haut ou en bas
            [x, x, x]
        posxy_xy2[2], posxy_xy2[3] c'est pour déplacer de haut en bas dans un ces cas là:
            [x, x, x, x]
              [x, x, x] on quel element bouger
        posxy_xy2[0], posxy_xy2[1] c'est pour déplacer de haut en bas dans un ces cas là:
            [x, x, x]
           [x, x, x ,x] on cherche a déplacer un element ici en haut ou en bas
            [x, x, x]
        posxy_xy2[2], posxy_xy2[3] c'est pour déplacer de haut en bas dans un ces cas là:
            [x, x, x, x]
              [x, x, x] on cherche a déplacer un element ici en haut ou en bas
            [x, x, x, x]
        directionListe c'est pour parcourir le terrain soit d'en haut si on vas en haut sinon d'en bas si on vers le bas (pour éviter un déplacement qui se répéte en boucle, j'ai pris du temps a trouvé ce probleme..)
        '''
        if self.allvalid(select, posxy_xy2) and makeAmove == 1: # Vérifie si le déplacement est possible

            if makeAmove == 1:
                self.randBloop[random.randint(-1,2)].play()
                self.nbrCoup += 1

            for w in range(0, len(self.terrain.terrain), 1) if self.directionListe == 0 else range(len(self.terrain.terrain) - 1, -1, -1): # Parcours le terrain de haut ou de bas en haut en fonction de z
                for q in range(len(self.terrain.terrain[w])):
                    if self.terrain.terrain[w][q] in self.alreadyTest:
                        if len(self.terrain.terrain[w]) % 4 == 0:
                            self.terrain.terrain[w + posxy_xy2[0]][q + posxy_xy2[1]] = self.terrain.terrain[w][q]
                            self.terrain.terrain[w][q] = "x"
                        else:
                            self.terrain.terrain[w + posxy_xy2[2]][q + posxy_xy2[3]] = self.terrain.terrain[w][q]
                            self.terrain.terrain[w][q] = "x"

    def allvalid(self, select, posxy_xy2):
        '''
        Vérifie que pour chaque élément qui compose le globule il puisse se déplacer dans la direction voulue
        en fonction return True ou False
        '''
        p, v = 0, 0
        for m in range(len(self.terrain.terrain)):
            for n in range(len(self.terrain.terrain[m])):
                if self.terrain.terrain[m][n] == select:
                    # Vérifie les conditions de déplacement pour chaque élément en fonction de leur pose
                    if (len(self.terrain.terrain[m]) % 4 == 0 and self.isvalid(select, m + posxy_xy2[0], n + posxy_xy2[1])) or (len(self.terrain.terrain[m]) % 4 != 0 and self.isvalid(select, m + posxy_xy2[2], n + posxy_xy2[3])):
                        p += 1
                    v += 1

        if p == v:
            if self.poussageRecursife(select, posxy_xy2):
                return True
        else:
            self.AllGoodRecursion = False

        return False
    
    def isvalid(self, select, x, y):
        # Vérifie si l'élément peux aller vers la direction souhaité (si il dépasse pas de la map et ne fonce pas dans autre chose)
        if len(self.terrain.terrain) > x > -1 and len(self.terrain.terrain[x]) > y > -1:
            # Permet de voir si l'élément après est dans selected (élément bougable) pour le bouger et le bouger si possible
            if self.terrain.terrain[x][y] in self.selected.values() and self.terrain.terrain[x][y] != select and self.terrain.terrain[x][y] not in self.otherPiece:
                self.otherPiece.append(self.terrain.terrain[x][y]) 
            # vérifie si il peux se déplacer
            if self.terrain.terrain[x][y] == "x" or self.terrain.terrain[x][y] in self.selected.values():
                    return True
        return False

    def poussageRecursife(self, select, posxy_xy2):    
        self.alreadyTest.append(select)
        if self.alreadyTest != self.otherPiece:
            for molecule in self.otherPiece:
                # Appeler moveMolecule uniquement si nécessaire
                if molecule not in self.alreadyTest:
                    self.alreadyTest.append(molecule)
                    self.moveMolecule(molecule, posxy_xy2)
                
        if self.AllGoodRecursion:
            return True
        else: 
            return False
# Initialiser et lancer le jeu
game = Game()
game.run()

pygame.quit()
