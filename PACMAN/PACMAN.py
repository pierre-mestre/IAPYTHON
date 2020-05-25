import random
import tkinter as tk
from tkinter import font  as tkfont
import numpy as np
 

#################################################################
##
##  variables du jeu 
 
# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

TBL = [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ]
        
        
TBL = np.array(TBL,dtype=np.int32)
TBL = TBL.transpose()  ## ainsi, on peut écrire TBL[x][y]


       
ZOOM = 40   # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels
HAUTEUR = TBL.shape [1]      
LARGEUR = TBL.shape [0]

screeenWidth = (LARGEUR+1) * ZOOM
screenHeight = (HAUTEUR+2) * ZOOM
 


###########################################################################################

# création de la fenetre principale  -- NE PAS TOUCHER

Window = tk.Tk()
Window.geometry(str(screeenWidth)+"x"+str(screenHeight))   # taille de la fenetre
Window.title("ESIEE - PACMAN")

# création de la frame principale stockant plusieurs pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
    
    
def WindowAnim():
    MainLoop()
    Window.after(500,WindowAnim)

Window.after(100,WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas( Frame1, width = screeenWidth, height = screenHeight )
canvas.place(x=0,y=0)
canvas.configure(background='black')
 
################################################################################
#
# placements des pacgums et des fantomes

def PlacementsGUM():  # placements des pacgums
   GUM = np.zeros(TBL.shape)
   
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 0):
            GUM[x][y] = 1
   return GUM

def initGPS():
  GPS = np.zeros(GUM.shape)

  for x in range(LARGEUR):
    for y in range(HAUTEUR):

     if ( GUM[x][y] == 0):
      GPS[x][y] = 1000
     if ( GUM[x][y] == 1):
      GPS[x][y] = 0

  return GPS

def initWhereIsTheGost():
  WhereIsTheGost = np.zeros(GUM.shape)

  for x in range(LARGEUR):
    for y in range(HAUTEUR):

     if ( GUM[x][y] == 0):
      WhereIsTheGost[x][y] = 1000
     if ( GUM[x][y] == 1):
      WhereIsTheGost[x][y] = 99

  return WhereIsTheGost

def majGPS():
  for x in range(LARGEUR):
    for y in range(HAUTEUR):
      if ( GPS[x][y] != 1000):
        if GPS[x][y] > 0 :
          GPS[x][y]=min([GPS[x+1][y], GPS[x-1][y], GPS[x][y+1], GPS[x][y-1]])+1

def majGostPosition(F,tableauGostPosition):
  x=F[0]
  y=F[1]
  tableauGostPosition[x][y]=0
  precision = 0
  if ( tableauGostPosition[x-1][y  ] < 100 ): tableauGostPosition[x-1][y  ] =1
  if ( tableauGostPosition[x  ][y-1] < 100 ): tableauGostPosition[x  ][y-1]=1
  if ( tableauGostPosition[x  ][y+1] < 100 ): tableauGostPosition[x  ][y+1]=1
  if ( tableauGostPosition[x+1][y  ] < 100 ): tableauGostPosition[x+1][y  ]=1

  for i in range(x,LARGEUR):
    for j in range(y,HAUTEUR):
      if tableauGostPosition[i][j]!=1000 and tableauGostPosition[i][j]!=0:
        L = []
        if ( tableauGostPosition[i-1][j  ] < 100 ): L.append(tableauGostPosition[i-1][j  ])
        if ( tableauGostPosition[i  ][j-1] < 100 ): L.append(tableauGostPosition[i  ][j-1])
        if ( tableauGostPosition[i  ][j+1] < 100 ): L.append(tableauGostPosition[i  ][j+1])
        if ( tableauGostPosition[i+1][j  ] < 100 ): L.append(tableauGostPosition[i+1][j  ])
        tableauGostPosition[i][j]=min(L,default=98)+1
  for i in range(x,0,-1):
    for j in range(y,0,-1):
      if tableauGostPosition[i][j]!=1000 and tableauGostPosition[i][j]!=0:
        L = []
        if ( tableauGostPosition[i-1][j  ] < 100 ): L.append(tableauGostPosition[i-1][j  ])
        if ( tableauGostPosition[i  ][j-1] < 100 ): L.append(tableauGostPosition[i  ][j-1])
        if ( tableauGostPosition[i  ][j+1] < 100 ): L.append(tableauGostPosition[i  ][j+1])
        if ( tableauGostPosition[i+1][j  ] < 100 ): L.append(tableauGostPosition[i+1][j  ])
        tableauGostPosition[i][j]=min(L,default=98)+1
  while precision <3:    ##permet d'augmenter la précision de la position des fantom en bouclant plusieurs fois        
    for i in range(0,LARGEUR):
      for j in range(0,HAUTEUR):
        if tableauGostPosition[i][j]!=1000 and tableauGostPosition[i][j]!=0:
          L = []
          if ( tableauGostPosition[i-1][j  ] < 100 ): L.append(tableauGostPosition[i-1][j  ])
          if ( tableauGostPosition[i  ][j-1] < 100 ): L.append(tableauGostPosition[i  ][j-1])
          if ( tableauGostPosition[i  ][j+1] < 100 ): L.append(tableauGostPosition[i  ][j+1])
          if ( tableauGostPosition[i+1][j  ] < 100 ): L.append(tableauGostPosition[i+1][j  ])
          tableauGostPosition[i][j]=min(L,default=98)+1    
    precision=precision+1

def majRecapGostPosition():
  for x in range(LARGEUR):
    for y in range(HAUTEUR):
        recapGostPosition[x][y]=min(tableauGostPosition[0][x][y],tableauGostPosition[1][x][y],tableauGostPosition[2][x][y],tableauGostPosition[3][x][y])


GUM = PlacementsGUM()
GPS = initGPS()   
pinkGostPosition = initWhereIsTheGost()
redGostPosition = initWhereIsTheGost()
blueGostPosition = initWhereIsTheGost()
orangeGostPosition = initWhereIsTheGost()
recapGostPosition = initWhereIsTheGost()
recapGostPosition = initWhereIsTheGost()
PacManPos = [5,5]

Ghosts  = []
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "pink"  ]   )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "orange"] )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "cyan"  ]   )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "red"   ]     )         

 
 
#################################################################
##
##  FNT AFFICHAGE



def To(coord):
   return coord * ZOOM + ZOOM 
   
# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [ 5,10,15,10,5]


def Affiche():
   global anim_bouche
   
   def CreateCircle(x,y,r,coul):
      canvas.create_oval(x-r,y-r,x+r,y+r, fill=coul, width  = 0)
   
   canvas.delete("all")
      
      
   # murs
   
   for x in range(LARGEUR-1):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 1 and TBL[x+1][y] == 1 ):
            xx = To(x)
            xxx = To(x+1)
            yy = To(y)
            canvas.create_line(xx,yy,xxx,yy,width = EPAISS,fill="blue")

   for x in range(LARGEUR):
      for y in range(HAUTEUR-1):
         if ( TBL[x][y] == 1 and TBL[x][y+1] == 1 ):
            xx = To(x) 
            yy = To(y)
            yyy = To(y+1)
            canvas.create_line(xx,yy,xx,yyy,width = EPAISS,fill="blue")
            
   # pacgum
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( GUM[x][y] == 1):
            xx = To(x) 
            yy = To(y)
            e = 5
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="orange")
  
   # dessine pacman
   xx = To(PacManPos[0]) 
   yy = To(PacManPos[1])
   e = 20
   anim_bouche = (anim_bouche+1)%len(animPacman)
   ouv_bouche = animPacman[anim_bouche] 
   tour = 360 - 2 * ouv_bouche
   canvas.create_oval(xx-e,yy-e, xx+e,yy+e, fill = "yellow")
   canvas.create_polygon(xx,yy,xx+e,yy+ouv_bouche,xx+e,yy-ouv_bouche, fill="black")  # bouche
   
  
   #dessine les fantomes
   dec = -3
   for P in Ghosts:
      xx = To(P[0]) 
      yy = To(P[1])
      e = 16
      
      coul = P[2]
      # corps du fantome
      CreateCircle(dec+xx,dec+yy-e+6,e,coul)
      canvas.create_rectangle(dec+xx-e,dec+yy-e,dec+xx+e+1,dec+yy+e, fill=coul, width  = 0)
      
      # oeil gauche
      CreateCircle(dec+xx-7,dec+yy-8,5,"white")
      CreateCircle(dec+xx-7,dec+yy-8,3,"black")
       
      # oeil droit
      CreateCircle(dec+xx+7,dec+yy-8,5,"white")
      CreateCircle(dec+xx+7,dec+yy-8,3,"black")
      
      dec += 3
     
   # texte blabla
   
   canvas.create_text(screeenWidth // 2, screenHeight- 50 , text = "Hello", fill ="yellow", font = PoliceTexte)
 
            
#################################################################
##
##  IA RANDOM
currentX = [-100,-100,-100,-100]
currentY = [-100,-100,-100,-100]
tableauGostPosition = [pinkGostPosition,orangeGostPosition,blueGostPosition,redGostPosition]

def randomGostSave(F,index) :
  L = GhostsPossibleMove(F[0],F[1])
  choix = random.randrange(len(L))
  currentX[index]=L[choix][0]
  currentY[index]=L[choix][1]
  # print(F, " X: ", currentX[index], " Y: ", currentY[index])

def randomGost(F) :
   L = GhostsPossibleMove(F[0],F[1])
   choix = random.randrange(len(L))
   F[0] += L[choix][0]
   F[1] += L[choix][1]

      
def PacManPossibleMove():
   L = []
   x,y = PacManPos
   if ( TBL[x  ][y-1] == 0 ): L.append((0,-1))
   if ( TBL[x  ][y+1] == 0 ): L.append((0, 1))
   if ( TBL[x+1][y  ] == 0 ): L.append(( 1,0))
   if ( TBL[x-1][y  ] == 0 ): L.append((-1,0))
   return L
   
def GhostsPossibleMoveOUT(x,y):
   L = []
   if ( TBL[x  ][y-1] == 2 ): L.append((0,-1))
   if ( TBL[x  ][y+1] == 2 ): L.append((0, 1))
   if ( TBL[x+1][y  ] == 2 ): L.append(( 1,0))
   if ( TBL[x-1][y  ] == 2 ): L.append((-1,0))
   if ( TBL[x-1][y  ] == 0 ): L.append((-1,0))
   if ( TBL[x  ][y-1] == 0 ): L.append((0,-1))
   if ( TBL[x  ][y+1] == 0 ): L.append((0, 1))
   if ( TBL[x+1][y  ] == 0 ): L.append(( 1,0))
   return L

def GhostsPossibleMove(x,y):
   L = []
   if ( TBL[x-1][y  ] == 0 ): L.append((-1,0))
   if ( TBL[x  ][y-1] == 0 ): L.append((0,-1))
   if ( TBL[x  ][y+1] == 0 ): L.append((0, 1))
   if ( TBL[x+1][y  ] == 0 ): L.append(( 1,0))
   return L


def IA():
   score = 0
   global PacManPos, Ghosts
   #deplacement Pacman
   tabDep= [GPS[PacManPos[0]+1][PacManPos[1]],GPS[PacManPos[0]-1][PacManPos[1]],GPS[PacManPos[0]][PacManPos[1]+1],GPS[PacManPos[0]][PacManPos[1]-1]]
   deplacement = tabDep.index(min(tabDep))                           

 
   if deplacement == 0 :
    PacManPos[0] = PacManPos[0]+1
    PacManPos[1] = PacManPos[1]
   elif deplacement == 1:
     PacManPos[0] = PacManPos[0]-1
     PacManPos[1] = PacManPos[1]                     
   elif deplacement == 2:
     PacManPos[0] = PacManPos[0]
     PacManPos[1] = PacManPos[1]+1
   elif deplacement == 3:
     PacManPos[0] = PacManPos[0]
     PacManPos[1] = PacManPos[1]-1
   else :
    L = PacManPossibleMove()
    choix = random.randrange(len(L))
    PacManPos[0] += L[choix][0]
    PacManPos[1] += L[choix][1]


   if GUM[PacManPos[0]][PacManPos[1]] == 1 :
       GUM[PacManPos[0]][PacManPos[1]] = 0;
       score += 1
       GPS[PacManPos[0]][PacManPos[1]] = 1

  #deplacement Fantome
   index = -1
   for F in Ghosts:
    if TBL[F[0]][F[1]] != 0:
      L = GhostsPossibleMoveOUT(F[0],F[1])
      choix = random.randrange(len(L))
      F[0] += L[choix][0]
      F[1] += L[choix][1]
    else :
      if F == Ghosts[0] : 
        index = 0
      elif F == Ghosts[1] :
        index = 1
      elif F == Ghosts[2] :
        index = 2
      elif F == Ghosts[3] :
        index = 3
      if index != -1:
        if(currentX[index] == -100 or currentY == -1000):
          randomGostSave(F,index)
          F[0]+=currentX[index]
          F[1]+=currentY[index]
        elif TBL[F[0]+currentX[index]][F[1]+currentY[index]]!=0:
          randomGostSave(F,index)
          F[0]+=currentX[index]
          F[1]+=currentY[index]
        elif len(GhostsPossibleMove(F[0],F[1])) > 2:
          randomGostSave(F,index)
          F[0]+=currentX[index]
          F[1]+=currentY[index]
        else:
          F[0]+=currentX[index]
          F[1]+=currentY[index]
      else:
        print("else")
      majGostPosition(F,tableauGostPosition[index])


   majGPS()
   majRecapGostPosition()
   print("\n RECAP: \n\n",recapGostPosition)
   # print(GPS)
   print("\n")
   # print("\n\nrecap:\n",recapGostPosition)
   # print(GPS)
   # majGostPosition(pinkGostPosition)
   print("\n PINK: \n\n",pinkGostPosition)
   # majGostPosition(orangeGostPosition)
   print("\n ORANGE: \n\n",orangeGostPosition)
   # majGostPosition(redGostPosition)
   print("\n RED: \n\n",redGostPosition)
   # majGostPosition(blueGostPosition)
   print("\n BLUE: \n\n",blueGostPosition)
   print("\n")
   return score

 

#################################################################
##
##   GAME LOOP

def MainLoop():
  IA()
  Affiche()  
 
 
###########################################:
#  demarrage de la fenetre - ne pas toucher

AfficherPage(0)
Window.mainloop()
   