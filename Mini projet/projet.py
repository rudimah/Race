from condortk import mise_a_jour, type_ev, ferme_fenetre
from condortk import touche, cree_fenetre, efface_tout, donne_ev
from condortk import fleche, ligne, image
from time import sleep
from random import randint
from math import sqrt
from condortk import* 
# dimensions du jeu
largeur_route = 100
largeur_fenetre = 640
hauteur_fenetre = 480


def creer_route(position_route):
    ''' Ne pas modifier. Permet de créer une route initiale.
    Une route est formée de 4 valeurs: 3 abscisses de points
    séparés en ordonnée par une hauteur d'écran et l'ordonnée du point
    du bas.
    Parameters:
        position_route (int): position du point du bas
    Returns:
        (int, int, int, int):   abscisse du point du bas,
                                abscisse du point du milieu,
                                abscisse du point du haut,
                                ordonnée du point du bas
    '''
    x_bas_gauche = position_route
    x_milieu_gauche = randint(50, largeur_fenetre - largeur_route - 50)
    x_haut_gauche = randint(50, largeur_fenetre - largeur_route - 50)
    return x_bas_gauche, x_milieu_gauche, x_haut_gauche, hauteur_fenetre


def affiche_route(route):
    ''' Ne pas modifier. Affiche la route à partir de l'information route
    composée de 4 valeurs: 3 abscisses de points séparés en ordonnée par
    une hauteur d'écran et l'ordonnée du point du bas.
    Parameters:
        route (int, int, int, int): abscisse du point du bas,
                                    abscisse du point du milieu,
                                    abscisse du point du haut,
                                    ordonnée du point du bas
    '''
    x_bas_gauche, x_milieu_gauche, x_haut_gauche, y_bas = route
    ligne(x_bas_gauche, y_bas, x_milieu_gauche, y_bas
          - hauteur_fenetre, epaisseur=2, couleur='white')
    ligne(x_bas_gauche + largeur_route, y_bas, x_milieu_gauche
          + largeur_route, y_bas - hauteur_fenetre, epaisseur=2, couleur='white')
    ligne(x_milieu_gauche, y_bas - hauteur_fenetre,
          x_haut_gauche, y_bas - 2 * hauteur_fenetre, epaisseur=2, couleur='white')
    ligne(x_milieu_gauche + largeur_route, y_bas - hauteur_fenetre, x_haut_gauche
          + largeur_route, y_bas - 2 * hauteur_fenetre, epaisseur=2, couleur='white')


def avance_route(route, vitesse):
    ''' Ne pas modifier. Permet de faire avancer la route à la vitesse de la
    voiture.
    On augmente donc l'ordonnée du point du bas de vitesse.
    Si le point du bas est trop bas, cela signifie que le point du haut devient
    visible, on crée un nouveau point en haut.
    Parameters:
        route (int, int, int, int): abscisse du point du bas,
                                    abscisse du point du milieu,
                                    abscisse du point du haut,
                                    ordonnée du point du bas
        vitesse (int): nombre de pixels défilant à chaque mise à jour du
        graphique.
    Returns:
        (int, int, int, int):   abscisse du point du bas,
                                abscisse du point du milieu,
                                abscisse du point du haut,
                                ordonnée du point du bas
    '''
    x_bas_gauche, x_milieu_gauche, x_haut_gauche, y_bas = route
    y_bas += vitesse
    if y_bas > 2 * hauteur_fenetre:
        x_bas_gauche = x_milieu_gauche
        x_milieu_gauche = x_haut_gauche
        x_haut_gauche = randint(50, largeur_fenetre - largeur_route - 50)
        y_bas = hauteur_fenetre
    return x_bas_gauche, x_milieu_gauche, x_haut_gauche, y_bas


def creer_voiture(route):
    ''' Ne pas modifier. Permet de créer la voiture au milieu de
    la route, aux 3/4 de l'écran en partant du haut, dans la direction
    de la route (inverse du coefficient directeur de la droite)
    Parameters:
        route (int, int, int, int): abscisse du point du bas,
                                    abscisse du point du milieu,
                                    abscisse du point du haut,
                                    ordonnée du point du bas
    Returns:
        (float, float, float):  abscisse de la voiture,
                                ordonnée de la voiture,
                                direction de la voiture
    '''
    x_bas_gauche, x_milieu_gauche, x_haut_gauche, y_bas = route
    x_voiture = (3 * x_bas_gauche + x_milieu_gauche) / 4 + largeur_route / 2
    y_voiture = 3 / 4 * y_bas
    direction = (x_bas_gauche - x_milieu_gauche) / (y_bas)
    return x_voiture, y_voiture, direction


def affiche_voiture(voiture):
    ''' Ne pas modifier. Affiche la voiture comme une flêche rouge
    dans la bonne direction.
    Parameters:
        voiture (float, float, float):  abscisse de la voiture,
                                        ordonnée de la voiture,
                                        direction de la voiture
    '''
    x_voiture, y_voiture, direction = voiture
    '''fleche(x_voiture, y_voiture, x_voiture - direction / sqrt(1 + direction ** 2),
          y_voiture - 1 / sqrt(1 + direction ** 2), epaisseur=4, couleur='green')'''
    image(x_voiture, y_voiture,  "carss.png")
   

def deplace(voiture, vitesse):
    ''' Permet de déplacer la voiture. Soustrait à l'abscisse de la voiture la
    vitesse multuplié par la direction.
    Parameters:
        voiture (float, float, float):  abscisse de la voiture,
                                        ordonnée de la voiture,
                                        direction de la voiture
    Returns:
        (float, float, float):  abscisse de la voiture,
                                ordonnée de la voiture,
                                direction de la voiture
    '''
    x_voiture, y_voiture, direction = voiture
    x_voiture -= vitesse * direction
    return x_voiture, y_voiture, direction


def change_direction(voiture, vitesse, touche):
    ''' Permet de changer la direction et la vitesse de la voiture avec
    le clavier.
    Si on appuie sur la touche du "Up", on ajoute 1 à la vitesse.
    Si on appuie sur la touche du "Down", on retire 1 à la vitesse.
    Si on appuie sur la touche du "Right", on retire 0.1 à la direction.
    Si on appuie sur la touche du "Left", on ajoute 0.1 à la direction.
    Parameters:
        voiture (float, float, float):  abscisse de la voiture,
                                        ordonnée de la voiture,
                                        direction de la voiture
        vitesse (int): vitesse de la x_voiture
        touche (str): nom de la touche pressée
    Returns:
        voiture (float, float, float):  abscisse de la voiture,
                                        ordonnée de la voiture,
                                        direction de la voiture
        vitesse (int): vitesse de la x_voiture
    '''
    x_voiture, y_voiture, direction = voiture
   
    if touche == "Up":
        vitesse += 1
        if vitesse > 10:
            vitesse = 10
    elif touche == "Down":
        vitesse -= 1
        if vitesse < 0:
            vitesse =0
    if touche == "space":
        vitesse = 0
    if touche == "Right":
        direction -= 0.1
    elif touche == "Left":
        direction += 0.1
       
             
               
           
    voiture = x_voiture, y_voiture, direction
    return voiture, vitesse


def detection_impact(route, voiture):
    ''' Ne pas modifier. Permet de détecter la colision avec bord de la route.
    Parameters:
        route (int, int, int, int): abscisse du point du bas,
                                    abscisse du point du milieu,
                                    abscisse du point du haut,
                                    ordonnée du point du bas
        voiture (float, float, float):  abscisse de la voiture,
                                        ordonnée de la voiture,
                                        direction de la voiture
    Returns:
        (bool): True si il y a eu collision, False sinon
    '''
    x_voiture, y_voiture, direction = voiture
    x_bas_gauche, x_milieu_gauche, x_haut_gauche, y_bas = route
    coef_directeur_bas = (x_milieu_gauche - x_bas_gauche)/(- hauteur_fenetre)
    coef_directeur_haut = (x_haut_gauche - x_milieu_gauche)/(- hauteur_fenetre)
    if y_bas < (1 + 3/4) * hauteur_fenetre:
        if x_voiture < x_bas_gauche + coef_directeur_bas * (y_voiture - y_bas) or x_voiture > x_bas_gauche + coef_directeur_bas * (y_voiture - y_bas) + largeur_route:
            return True
        else:
            return False
    else:
        if x_voiture < x_milieu_gauche + coef_directeur_haut * (y_voiture - y_bas + hauteur_fenetre) or x_voiture > x_milieu_gauche + coef_directeur_haut * (y_voiture - y_bas + hauteur_fenetre) + largeur_route:
            return True
        else:
            return False


def affiche_victoire():
    ''' Fonction permettant de gérer graphiquement la fin de jeu
    Parameters:
        ...
    Returns:
        ...
    '''
    ...

def menu():
    texte(180, 160, "Jouer", couleur="black", taille=80, tag="Jouer"  )
    
    attend_ev()
    
    efface("Jouer")

def score(): #  Pas réussis 
    score = 0
    
    while crash:
        score+= 1 
    return score 
    

    
# programme principal
if __name__ == "__main__":
    # initialisation du jeu
    framerate = 20    # taux de rafraîchissement du jeu en images/s
    direction_voiture = (0, -1)  # direction initiale de la balle
    position_route = 100  # position initiale de la balle
    cree_fenetre(largeur_fenetre, hauteur_fenetre)
    menu()

    vitesse = 0# Vitesse initiale
    route = creer_route(position_route)
    voiture = creer_voiture(route)
    
    # boucle principale
    jouer = True
    while jouer:
        # affichage des objets
        efface_tout()  # efface tous les objets
        
        
        
        affiche_route(route)  # affiche la route
        affiche_voiture(voiture)  # affiche la voiture
        texte(580, 0, vitesse, couleur="black", taille=40)
        texte(-287.5, 0, route, couleur="black", taille=40)
        mise_a_jour()  # met à jour l'affichage

        # gestion des événements
        ev = donne_ev()  # récupère les évènements clavier ou souris
        ty = type_ev(ev)  # récupère le type d'événement
        if ty == 'Quitte':
            jouer = False
        elif ty == 'Touche':  # Si c'est un événement clavier
            # print(touche(ev))
            voiture, vitesse = change_direction(voiture, vitesse, touche(ev))
        route = avance_route(route, vitesse)
        voiture = deplace(voiture, vitesse)
        crash = detection_impact(route, voiture)
        jouer = not crash
        ...  # à modifier
        # attente avant rafraîchissement
        sleep(1 / framerate)

    # Affichage fin de jeu
    affiche_victoire()
    # fermeture et sortie
    ferme_fenetre()