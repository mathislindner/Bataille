import tkinter as tk
import random
#==============================================================================
taillejeu="1080x1080"
hauteurcadre=800
largeurcadre=400
l=largeurcadre/11
h=hauteurcadre/11
sens="none"
direction="none"
casebatx=0
casebaty=0
ships=[]
shipsai=[]
aitotalhits=0
aihits=0
userhits=0
#==============================================================================

master = tk.Tk()
master.title("Bataille Navale")
master.geometry(taillejeu)
tk.Frame(master).grid()
cadre=tk.Canvas(master, width=largeurcadre, height=hauteurcadre,bg="white")
cadre.grid(column=0, row=0)

orientation='N'#ffaudra voir si on le fait rester à ce que cest ou si on le fait revenir a N
game_mode=False
player_turn=False  #Variable boouléenne qui vérifie que assure le respect du tour de jeu 
bateau_en_vie=True

def gamemode():        #Seperates the moment of boat placement from the game play
    global game_mode
    global player_turn
    game_mode=True
    cadre.configure(cursor='boat')
    master.configure(cursor='boat')
    boatframe.configure(cursor='boat')
    player_turn=True

class case:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.bateau=False
        self.case_attaquee=False        
        self.xdebut=x*l
        self.xfin=(x+1)*l
        self.ydebut=y*(h/2)+hauteurcadre/2
        self.yfin=y*(h/2)+(h/2)+hauteurcadre/2
        self.draw()
    def __repr__(self):
        return str(self.x) + ','+str(self.y)
    
    def draw(self):
        global bateau_en_vie
        rect=cadre.create_rectangle(self.xdebut,self.ydebut,self.xfin,self.yfin, fill=self.color())
        if bateau_en_vie==False and self.color()=="red":
            cadre.create_line(self.xdebut,self.ydebut,self.xfin,self.yfin,fill="black") 
            cadre.create_line(self.xdebut,self.yfin,self.xfin,self.ydebut,fill="black")
        
        cadre.tag_bind(rect, "<Button-1>", self.click)
        
    def boat(self):
        if self.bateau==False:
            self.bateau=True
            self.draw()
        else:
            self.bateau=False
            self.draw()
        
    def color(self):
        global player_turn
        couleur="white"
        if self.bateau==True:
            couleur="grey"
        if self.case_attaquee and self.bateau:
            couleur="red"
            player_turn=False
        elif self.case_attaquee==True and self.bateau==False:
            couleur="blue"
            player_turn=True
        return couleur
    
    def attacked(self):
        if self.case_attaquee==False:
            self.case_attaquee=True
            self.draw()
            
            """def place(event):
    global orientation
    global bl
    global selectable
    global ships
    if selectable==False:
        s=ship(bl,orientation)    #ne fonctionne pas encore 
        s.placement(event.x, event.y)
        selectable=True
    else:
        print('Please select a boat to place.')"""
    
    def click(self, event):
        global game_mode
        global orientation
        global bl
        global selectable
        global ships
        global shipsai
        global caseadversaire
        environs=True
        if selectable==False:
            if game_mode==False:
                ships.append(ship(bl,orientation))
                bateau_selectionne=ships[len(ships)-1]
                bateau_selectionne.projet(self.x, self.y, cases)
                for i in range(len(bateau_selectionne.projection)):
                    print(bateau_selectionne.projection[i])
                    print(bateau_selectionne.projection[i].check_surrounding())
                    if bateau_selectionne.projection[i].check_surrounding()==False:
                        information.itemconfigure(1, text='Boats can not be adjacent.')
                        environs=False
                        ships.pop()
                if environs==True:
                    if bateau_selectionne.check_placement(self.x, self.y)==False:
                        information.itemconfigure(1, text='Boat out of area.')
                        ships.pop()
                    else:
                        bateau_selectionne.placement(self.x, self.y, cases)
                        selectable=True
                        all_placed()
                        actualise(ships)
            else:   
                if player_turn==True:
                    self.attacked()
                    shipsai[quel_bateau(caseadversaire[self.x][self.y])].bateau_en_vie(shipsai)
                else:
                    information.itemconfigure(1, text='It is not your turn to play.')
        else:
             information.itemconfigure(1, text='Please select a boat to place.')
         
    def check_self(self):
        if self.bateau==True:
            return False
        else:
            return True
            
            
    def check_surrounding(self): #check s'il n'y a pas de bateau autour
        xcoordinate=[-1,0,0,+1]
        ycoordinate=[0,+1,-1,0]
        for i in range(4):
            try:
                adjacent_case=cases[(self.x+xcoordinate[i])][self.y+(ycoordinate[i])]
                #print(adjacent_case)
                if adjacent_case.bateau==True:
                    return False
            except:
                    IndexError
        return True
                
                 
    def checks(self):
        return self.check_self() and self.check_surrounding()
        

                  
class ship:
    def __init__(self,l,orient):
        self.length=l
        self.orientation=orient
        self.endroits=[]
        self.projection=[]
    def __repr__(self):
        return str(self.length)
    
    def check_placement(self, x, y):
        if self.orientation=='S':  #vérifie que le bateau rentre dans le cadre
            if y+self.length>10:
                return False
        elif self.orientation=='E':
            if x-self.length<-1:
                return False
        elif self.orientation=='N':
            if y-self.length<-1:
                return False
        elif self.orientation=='W':
                if x+self.length>10:
                    return False
        
    def projet(self, x,y, liste):
        try:
            for i in range(self.length):
                if self.orientation=='S':  
                    self.cases(self.projection,x,y+i, liste)
                elif self.orientation=='E':
                    self.cases(self.projection,x-i,y, liste)
                elif self.orientation=='N':
                    self.cases(self.projection,x,y-i, liste)
                elif self.orientation=='W':
                    self.cases(self.projection,x+i,y, liste)
        except IndexError:
            return False
                    
    def placement(self,x,y, liste):
        for i in range(self.length):
            if self.orientation=='S':  
                liste[x][y+i].boat()  
                self.cases(self.endroits,x,y+i, liste)
            elif self.orientation=='E':
                liste[x-i][y].boat()
                self.cases(self.endroits,x-i,y, liste)
            elif self.orientation=='N':
                liste[x][y-i].boat()
                self.cases(self.endroits,x,y-i, liste)
            elif self.orientation=='W':
                liste[x+i][y].boat()
                self.cases(self.endroits,x+i,y, liste)
                
    def placementai(self):   #fonction qui place les bateaux de la liste sur cases
        for i in range(self.length):
            self.projection[i].boat()
                    
    def cases(self,liste,x,y, liste2):
        liste.append(liste2[x][y])
        
    def bateau_en_vie(self, liste):
        global bateau_en_vie
        level=0
        for i in range(self.length):
            if self.endroits[i].case_attaquee==True:
                level=level+1
        lvl= int(level/self.length)
        if lvl==1:
            bateau_en_vie=False 
            print('boat fully attacked')
            for i in range(self.length):
                switch_turn()
                self.endroits[i].draw()
            bateau_en_vie=True 
            switch_turn()
        return lvl


        
class ai: #classe pour casesadversaire
    
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.bateau=False
        self.case_attaquee=False
        self.xdebut=x*l
        self.xfin=(x+1)*l
        self.ydebut=y*(h/2)
        self.yfin=y*(h/2)+(h/2)
        self.draw()
        
    def __repr__(self):
        return str(self.x) + ','+str(self.y)
        
    def boat(self):
        if self.bateau==False:
            self.bateau=True
            self.draw()
        else:
            self.bateau=False
            self.draw()
            
    def attacked(self):
        if self.case_attaquee==False:
            self.case_attaquee=True
            self.draw()
            
            
    def check_surrounding(self): #check s'il n'y a pas de bateau autour et sur sa position
        xcoordinate=[-1,0,0,+1]
        ycoordinate=[0,+1,-1,0]
        for i in range(4):
            try:
                if caseadversaire[(self.x+xcoordinate[i])][self.y+(ycoordinate[i])].bateau==True:
                    return False
            except:
                    IndexError
        return True
            
    def draw(self):
        global bateau_en_vie
        rect=cadre.create_rectangle(self.xdebut,self.ydebut,self.xfin,self.yfin, fill=self.color())
        if bateau_en_vie==False and self.color()=="red":
            cadre.create_line(self.xdebut,self.ydebut,self.xfin,self.yfin,fill="black") 
            cadre.create_line(self.xdebut,self.yfin,self.xfin,self.ydebut,fill="black")

        cadre.tag_bind(rect, "<Button-1>", self.click)
        
    def click(self, event):
        global player_turn
        if player_turn==True:
            case.attacked(self)
            #print(self.case_attaquee and self.bateau)
            if self.case_attaquee and self.bateau:
                player_turn=True
            else:
                player_turn=False
                information.itemconfigure(1, text='It is not your turn to play.')
                cadre.after(300, aiattack)
        else:
            information.itemconfigure(1, text='It is not your turn to play.')
        
    def color(self):
        global player_turn 
        couleur="white"
        if self.case_attaquee and self.bateau:
            couleur="red"
            player_turn=True
        elif self.case_attaquee==True and self.bateau==False:
            couleur="blue"
            player_turn=False
        return couleur
        
def rancoord(): #renvoie 2 chiffres random
    a=random.randrange(0,10,1)
    b=random.randrange(0,10,1)
    return a,b
                  
def ranai():    #renvoie un chiffre random entre 1 et 4
    return random.randrange(1,5,1)
                  
def attacked_all(): #check si toutes les cases ont été attaqué
    for i in range(9):
        for j in range(9):
            if cases[i][j].case_attaquee==False:
                return False
                
def random_orientation(): #génère une orientation alèatoire (nord, sud, est, ouest)
    random=ranai()
    if random==1:
        orientation="N"
    elif random==2:
        orientation="E"
    elif random==3:
        orientation="S"
    elif random==4:
        orientation="W" 
    return orientation
    
def placeboatsai(): #fonction qui place les bateaux des l'ai
    global shipsai
    global caseadversaire
    boatlengths=[5,4,3,3,2,2,2]

    for i in range(len(boatlengths)):
        orientation=random_orientation()
        shipsai.append(ship(boatlengths[i],orientation))
        x,y=rancoord()
        shipsai[i].projection.append(shipsai[i].projet(x,y,caseadversaire))
        for l in range(boatlengths[i]):       
            while  shipsai[i].check_placement(x,y)==False:
                del shipsai[i].projection[:]
                x,y=rancoord()
                shipsai[i].projection.append([shipsai[i].projet(x,y,caseadversaire)])
        shipsai[i].projection.pop()
   
    for j in range(len(shipsai)):
        for k in range(len(shipsai[j].projection)):
            while shipsai[j].check_placement(x,y)==False or shipsai[j].projection[k].check_surrounding()==False:
                    shipsai[j].orientation=random_orientation()
                    del shipsai[j].projection[:]
                    x,y=rancoord()
                    shipsai[j].projection.append([shipsai[j].projet(x,y,caseadversaire)])
                    shipsai[j].projection.pop()
            
        shipsai[j].placementai(caseadversaire)    

                                
        

       
    

def hit():       #détermine si un bateau a été touché par l'ai et le score du joueur et de l'ai
    global userhits #nombre de cases bateaux touché par le joueur
    global aihits   #nombre de cases touchée par l'ai au tours precedent
    global aitotalhits  #nombre de cases touchée par l'ai dans le tour present
    a=0
    b=0
    for i in range(10):
        for j in range(10):
            if caseadversaire[i][j].case_attaquee==True and caseadversaire[i][j].bateau==True: #comptage de case touché par le joueur
                a=a+1
            if cases[i][j].case_attaquee==True and cases[i][j].bateau==True:                    #comptage de case touché par l'ai
                b=b+1     
    userhits=a
    aitotalhits=b
    if b==aihits+1:     #si une case de plus a été touché qu'au tour avant
        aihits=aihits+1 #ajouter a la variable 1 pour pouvoir reverifier au prochain tour
        return True     
    
def winner():   #déterminer le gagnant
    global player_turn 
    if aitotalhits==21: #si l'ai a touché les 21 cases bateaux (5+4+3+3+2+2+2) avant le joueur
        player_turn=0   #le joueur n'a plus le droit de jouer
        information.itemconfigure(1, text='You lost.') #indiquation que le joueur a perdu
        return False    
    if userhits==21: #si le joueur a touché les 21 cases bateaux avant l'ai
        player_turn=0   #le joueur n'a plus le droit de jouer
        information.itemconfigure(1, text='You won.') #indiquation qu'il a gagné
        return False
    

def aiattack():
    global sens #par default sens="none"
    global direction #par default direction="none"
    global casebatx  #position ou se trouve un bateau (la variable est set plus basse dans "if sens==none")
    global casebaty
    global ships    #liste dans laquel se trouve les objet ships ou l'ordinateur va attauqer
    global player_turn  #la variable qui determine le tour du joueur ou de l'ordinateur
    global userhits     #le nb de case ou se trouvait un bateau touché par l'utilisateur
    global aihits       #le nb de case ou se trouvait un bateau touché par l'ia
    if winner()==False: #si aucun des deux joueurs n'a touché les 21 positions ou se trouvent les bateaux
        return None
    if player_turn==False and game_mode==True:   #si c'est à l'ia de jouer et que les bateaux sont tous placés
        try:                                    #pour éviter les erreurs d'index il y aura de nombreux fonction try
            if sens=="vertical":                #si le sens est connu et qu'il est "verticale"
                essai=False
                if ships[quel_bateau(cases[casebatx][casebaty])].bateau_en_vie(ships)== 1: #si le bateau est coulé, l'ia attaque aléatoirement a nouveau
                    sens="none"
                    direction="none"
                else:
                    while essai==False:
                        try:
                            if direction=="haut":           #si la direction (qui est déterminer en dessous) est connue l'ia attaque toutes les cases vers le "haut"jusqu a ce qu le bateau est coulé
                                while essai==False:
                                    if cases[casebatx][casebaty-1].case_attaquee==False: 
                                        cases[casebatx][casebaty-1].attacked()
                                        essai=True
                                    elif cases[casebatx][casebaty-2].case_attaquee==False:
                                        cases[casebatx][casebaty-2].attacked()
                                        essai=True
                                    elif cases[casebatx][casebaty-3].case_attaquee==False: 
                                        cases[casebatx][casebaty-3].attacked()
                                        essai=True
                                    elif cases[casebatx][casebaty-4].case_attaquee==False: 
                                        cases[casebatx][casebaty-4].attacked()
                                        essai=True
                                        
                            else:
                                if cases[casebatx][casebaty+1].case_attaquee==False: #l'ia attaque dans une direction jusqu'à ce qu'il n'ait plus de case bateau, elle set donc le direction="haut"
                                    cases[casebatx][casebaty+1].attacked()
                                    essai=True
                                    if cases[casebatx][casebaty+1].bateau==False:
                                        direction="haut"
                                            
                                elif cases[casebatx][casebaty+2].case_attaquee==False: 
                                    cases[casebatx][casebaty+2].attacked()
                                    essai=True
                                    if cases[casebatx][casebaty+2].bateau==False:
                                        direction="haut"
                                        
                                elif cases[casebatx][casebaty+3].case_attaquee==False:
                                    cases[casebatx][casebaty+3].attacked()
                                    essai=True
                                    if cases[casebatx][casebaty+3].bateau==False:
                                        direction="haut"

                                elif cases[casebatx][casebaty+4].case_attaquee==False:
                                    cases[casebatx][casebaty+4].attacked()
                                    essai=True
                                    if cases[casebatx][casebaty+4].bateau==False:
                                        direction="haut"
                                    

                        except IndexError:
                            pass

            
            if sens=="horizontal": #si le sens est connu et qu'il est "horiontal"
                essai=False
                if ships[quel_bateau(cases[casebatx][casebaty])].bateau_en_vie(ships)== 1:
                    sens="none"
                    direction="none"
                else:
                    while essai==False:
                        try:
                            if direction=="gauche":
                                while essai==False:
                                    if cases[casebatx-1][casebaty].case_attaquee==False:    # attaque à gauche de la cases[casebatx][casebaty] jusqu'à ce que le bateau soit coulé
                                        cases[casebatx-1][casebaty].attacked()
                                        essai=True
                                    elif cases[casebatx-2][casebaty].case_attaquee==False: 
                                        cases[casebatx-2][casebaty].attacked()
                                        essai=True
                                    elif cases[casebatx-3][casebaty].case_attaquee==False: 
                                        cases[casebatx-3][casebaty].attacked()
                                        essai=True
                                    elif cases[casebatx-4][casebaty].case_attaquee==False:
                                        cases[casebatx-4][casebaty].attacked()
                                        essai=True
                            else:
                                if cases[casebatx+1][casebaty].case_attaquee==False:    #determination de la direction ou seulement attauqe dans un sens
                                    cases[casebatx+1][casebaty].attacked()
                                    essai=True
                                    if cases[casebatx+1][casebaty].bateau==False:
                                        direction="gauche"
                                        
                                elif cases[casebatx+2][casebaty].case_attaquee==False:
                                    cases[casebatx+2][casebaty].attacked()
                                    essai=True
                                    if cases[casebatx+2][casebaty].bateau==False:
                                        direction="gauche"
                                elif cases[casebatx+3][casebaty].case_attaquee==False:
                                    cases[casebatx+3][casebaty].attacked()
                                    essai=True
                                    if cases[casebatx+3][casebaty].bateau==False:
                                        direction="gauche"

                                elif cases[casebatx+4][casebaty].case_attaquee==False: 
                                    cases[casebatx+4][casebaty].attacked()
                                    essai=True
                                    if cases[casebatx+4][casebaty].bateau==False:
                                        direction="gauche"
    
                        except IndexError:
                            pass
        
            if sens=="unknown":     #si un bateau a été touché mais l'ordinateur ne sait pas dans quel sens se trouve les autres cases
                try:
                    essai=False     #la variable qui check si une case a été attaqué
                    while essai==False:     #l'ia attaque aléatoirement la case au dessus, en dessous a droite et a gauche pour déterminer le sens
                        random=ranai()
                        if random==1:
                            if cases[casebatx+1][casebaty].case_attaquee==False:    #seulement attaqué une case non-attaquée
                                cases[casebatx+1][casebaty].attacked()
                                if cases[casebatx+1][casebaty].bateau==True:        #si un bateau s'y trouuve alors le sens="horizontal" car x et non y a changé
                                    sens="horizontal"
                                else:
                                    sens="unknown"                                  #sinon le sens est encore inconnu et c'est au joueur de jouer car aucune case avec un bateau n'a été touchée
                                essai=True
                                    
                                    
                        if random==2:
                            if cases[casebatx-1][casebaty].case_attaquee==False:
                                cases[casebatx-1][casebaty].attacked()
                                if cases[casebatx-1][casebaty].bateau==True:
                                    sens="horizontal"
                                else:
                                    sens="unknown"
                                essai=True
                                
                        if random==3:
                            if cases[casebatx][casebaty+1].case_attaquee==False:   
                                cases[casebatx][casebaty+1].attacked()
                                if cases[casebatx][casebaty+1].bateau==True:
                                    sens="vertical"
                                else:
                                    sens="unknown"
                                essai=True
                        if random==4:
                            if cases[casebatx][casebaty-1].case_attaquee==False:
                                cases[casebatx][casebaty-1].attacked()
                                essai==True
                                if cases[casebatx][casebaty-1].bateau==True:
                                    sens="vertical"
                                else:
                                    sens="unknown"
                                essai=True
                                    
                except IndexError: 
                    pass   
                
            if sens=="none":            #par défault le sens est "none", l'ia n'a aucune information sur la position des bateaux
                a,b=rancoord()          #des coordonnées aléatoire sont données (voir rancoord())
                while cases[a][b].case_attaquee==True: #determination de coordonées aleatoires qui n'ont pas encore été attaquée
                    a,b=rancoord()
                cases[a][b].attacked()
                if cases[a][b].bateau==True:    #si un bateau se trouve sur cette case
                    sens="unknown"              #le sens="unknown" pour qu'au prochain tour 'l'ia sait où attaquer
                    casebatx=a                  #les coordonées sont enregistrées
                    casebaty=b
        except IndexError:          #si une Erreur d'index occure
            pass                    #ignorer
        
        if hit()==True:             #si un bateau a été touché par l'ia (voir hit())
            cadre.after(300, aiattack) #attendre 300ms, puis executer aiattack()
        else:
            player_turn==True       #sinon c'est au tour du joueur
            information.itemconfigure(1, text='It is your turn to play.')
    
    else:
        information.itemconfigure(1, text='It is your turn to play.')

        
caseadversaire=[]   #créations des objets grace au classe ai et case
cases=[]
for i in range(10):
    cases.append([])
    caseadversaire.append([])
    for j in range(10):
        cases[i].append(case(i,j))
        caseadversaire[i].append(ai(i,j))
      

    
#================== Selectable boats ================================
boatframe=tk.Canvas(master, width=450, height=300)
boatframe.grid(column=1,row=0, sticky="N")

selectable=True #variable qui assure que seulement un bateau soit séléctionné à la fois
bl=0

b5_coord = (l+300),(h-40), (l+300),h, (l+50),h, (l+50),(h-40)
b4_coord = (l+270),(h+30), (l+270),(h+70), (l+80),(h+70), (l+80),(h+30)
b3_coord = (l+240),(h+100), (l+240),(h+140), (l+110),(h+140), (l+110),(h+100)
b2_coord = (l+210),(h+170), (l+210),(h+210), (l+140),(h+210), (l+140),(h+170)
    
"""
    for i in range (2,5): 
        bi=boatframe.create_polygon(bi_coord, fill="blue")
        def clicked_bi(event):
            print("Boat i selected")
            boatframe.create_polygon(bi_coord, fill="grey")
        boatframe.tag_bind(bi,"<Button-1>",clicked_bi)
"""
    
b5=boatframe.create_polygon(b5_coord, fill="blue")
b4=boatframe.create_polygon(b4_coord, fill="blue")
b3=boatframe.create_polygon(b3_coord, fill="blue")
b2=boatframe.create_polygon(b2_coord, fill="blue")

compteur_b5=1
compteur_b4=1
compteur_b3=2
compteur_b2=3

nb_5=boatframe.create_text((l+320),(h-20), text='x 1')
nb_4=boatframe.create_text((l+290),(h+50), text='x 1')
nb_3=boatframe.create_text((l+260),(h+120), text='x 2')
nb_2=boatframe.create_text((l+230),(h+190), text='x 3')
 
c_selected=0
   
def clicked_b5(event):
    global bl
    global selectable 
    info()
    global compteur_b5
    if compteur_b5==0:
        information.itemconfigure(1, text='Tous les bateaux de cette categorie ont ete places')
    else:
        if selectable==True:
            selectable=False
            print("Boat 5 selected")
            boatframe.itemconfigure(1, fill="grey")
            rotate_north(event)
            bl=5
            compteur_b5=compteur_b5-1
            boatframe.itemconfigure(5, text='x '+str(compteur_b5))
        else:
            information.itemconfigure(1, text="Veuillez placer le bateau avant de selectionner un autre.")

def clicked_b4(event):
    global bl
    global selectable 
    info()
    global compteur_b4
    if compteur_b4==0:
        information.itemconfigure(1, text='Tous les bateaux de cette categorie ont ete places')
    else:
        if selectable==True:
            selectable=False
            print("Boat 4 selected")
            boatframe.itemconfigure(2, fill="grey")
            rotate_north(event)
            bl=4
            compteur_b4=compteur_b4-1
            boatframe.itemconfigure(6, text='x '+str(compteur_b4))
        else:
            information.itemconfigure(1, text="Veuillez placer le bateau avant de selectionner un autre.")
            
def clicked_b3(event):
    global bl
    global selectable 
    global compteur_b3
    info()
    if compteur_b3==0:
        information.itemconfigure(1, text='Tous les bateaux de cette categorie ont ete places')
    else:
        if selectable==True:
            print("Boat 3 selected")
            selectable=False
            if compteur_b3==2: 
                boatframe.itemconfigure(3, fill='#A9CCE3')
                boatframe.itemconfigure(7, text='x 1')
            elif compteur_b3==1:
                boatframe.itemconfigure(3, fill='grey')
                boatframe.itemconfigure(7, text='x 0')
            rotate_north(event)
            bl=3    
            compteur_b3=compteur_b3-1
        else: 
            information.itemconfigure(1, text="Veuillez placer le bateau avant de selectionner un autre.")
            
def clicked_b2(event):
    global bl
    global selectable 
    global compteur_b2
    info()
    if compteur_b2==0:
        information.itemconfigure(1, text='Tous les bateaux de cette categorie ont ete places')
    else:
        if selectable==True:
            print("Boat 2 selected")
            selectable=False
            if compteur_b2==3: 
                boatframe.itemconfigure(4, fill='#5DADE2')
                boatframe.itemconfigure(8, text='x 2')
            elif compteur_b2==2:
                boatframe.itemconfigure(4, fill='#A9CCE3')
                boatframe.itemconfigure(8, text='x 1')
            elif compteur_b2==1:
                boatframe.itemconfigure(4, fill='grey')
                boatframe.itemconfigure(8, text='x 0')        
            rotate_north(event)
            bl=2    
            compteur_b2=compteur_b2-1
        else: 
            information.itemconfigure(1, text="Veuillez placer le bateau avant de selectionner un autre.")
            

def rotate_north(event): #Default orientation
    global orientation
    cadre.configure(cursor='sb_up_arrow')
    boatframe.configure(cursor='sb_up_arrow')
    orientation='N'
def rotate_east(event):
    global orientation
    cadre.configure(cursor='sb_left_arrow')
    boatframe.configure(cursor='sb_left_arrow')
    orientation='E'
def rotate_south(event):
    global orientation
    cadre.configure(cursor='sb_down_arrow')
    boatframe.configure(cursor='sb_down_arrow')
    orientation='S'
def rotate_west(event):
    global orientation
    cadre.configure(cursor='sb_right_arrow')
    boatframe.configure(cursor='sb_right_arrow')
    orientation='W'

boatframe.tag_bind(b5,"<Button-1>",clicked_b5)
boatframe.tag_bind(b4,"<Button-1>",clicked_b4)
boatframe.tag_bind(b3,"<Button-1>",clicked_b3)
boatframe.tag_bind(b2,"<Button-1>",clicked_b2)
master.bind('<Left>', rotate_east)
master.bind('<Up>', rotate_north)
master.bind('<Down>', rotate_south)
master.bind('<Right>', rotate_west)

#====================================================================
def switch_turn():
    global player_turn
    if player_turn==False:
        player_turn=True
    else:
        player_turn=False
#======================== Info box ==================================
information=tk.Canvas(master, width=300, height=300)
information.grid(column=1,row=0, sticky='S')

info=information.create_text(150,20, text='Select boats above to begin.')

def info():
    if c_selected==0:
        information.itemconfigure(1, text='Use arrow keys to modify the orientation of the boat. \n Place boats on the bottom grid, this one is yours.')
#====================================================================
vies=tk.Canvas(master, width=300, height=300)
vies.grid(column=2,row=0)

def calcul_vie(liste):
    longueur_totale=0
    vie=0
    for i in range(len(liste)):
        longueur_totale=longueur_totale+liste[i].length
        vie=vie+(liste[i].bateau_en_vie(liste)*liste[i].length)
        #print(vie)
    if longueur_totale!=0:
        #print(vie/longueur_totale*100)
        return vie/longueur_totale*100
        
joueur=vies.create_text(150,20,text='Joueur:'+str(calcul_vie(ships))+'%')

def actualise(liste):
    vies.itemconfigure(1, text='Joueur:'+str(calcul_vie(liste))+'%')

def quel_bateau(case):
    for i in range(len(ships)):
        for j in range(len(ships[i].endroits)):
            if ships[i].endroits[j]==case:
                return i #ca te renvoie l'indice du bateau, genre cest le seul moyen de dire "quel bateau" cest
            
def all_placed():
    if compteur_b5==0 and compteur_b4==0 and compteur_b3==0 and compteur_b2==0:
        gamemode()
        boatframe.destroy()
        information.itemconfigure(1, text='It is your turn to play.')
        return True
    else:
        return False
#Bouton2 = tk.Button(master, text = 'Placer bateau2', command = placer_boats).grid(row=2, column=1)
ai = tk.Button(master, text = 'ai', command = aiattack).grid(row=0, column=1)
#play=tk.Button(master, text="Jouer", width="10", height="2", command=gamemode).grid(column=2, row=0)
placeboatsai()
master.mainloop()
