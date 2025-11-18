import os

# Codes couleurs ANSI
class Couleurs:
    RESET = '\033[0m'
    ROUGE = '\033[91m'
    VERT = '\033[92m'
    JAUNE = '\033[93m'
    BLEU = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BLANC = '\033[97m'
    GRAS = '\033[1m'

def ajouter_participant():
    pass
def retirer_participant():
    pass
def afficher_agenda():
    pass


def verifier_conflit_participant():
    pass


def trouver_creneau_commun():
    pass


def verifier_conflit_salle():
    pass
def verifier_occupation_max_salle():
    pass


def ajouter_evenement():
    pass
def supprimer_evenement():
    pass
def afficher_evenements_par_date():
    pass


def affiche_intro():
    choix=input(f"""
{Couleurs.CYAN}{Couleurs.GRAS}Que souhaitez-vous faire ?{Couleurs.RESET}
            
{Couleurs.VERT}1{Couleurs.RESET} - Créer un nouvel événement
{Couleurs.VERT}2{Couleurs.RESET} - Ajouter un participant
{Couleurs.VERT}3{Couleurs.RESET} - Afficher l’agenda d’un participant
{Couleurs.VERT}4{Couleurs.RESET} - Trouver un créneau commun
{Couleurs.ROUGE}5{Couleurs.RESET} - Quitter
                
{Couleurs.JAUNE}Votre choix : {Couleurs.RESET}""")
    return choix

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    valuers_correcte=['0','1','2','3','4','5']
    choix=affiche_intro()
    while choix not in valuers_correcte:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Couleurs.ROUGE}Choix incorrect, veuillez rentrer une valeur correcte.{Couleurs.RESET}")
        choix=affiche_intro()
    if choix=='1':
        pass
    if choix=='2':
        pass
    if choix=='3':
        pass
    if choix=='4':
        pass
    if choix=='5':
        print(f"{Couleurs.VERT}Au revoir !{Couleurs.RESET}")