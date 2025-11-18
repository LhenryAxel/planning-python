import os
import json

# --- Gestion du fichier JSON ---
def charger_donnees():
    try:
        with open("dico.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Si le fichier n'existe pas encore, on initialise une structure vide
        return {"evenements": {}, "participants": {}}

def sauvegarder_donnees(donnees):
    with open("dico.json", "w") as f:
        json.dump(donnees, f, indent=4)

# --- Codes couleurs ANSI ---
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

# --- Fonctions principales ---
def ajouter_participant(dico):
    evenements = dico["evenements"]
    participants = dico["participants"]

    nom = input("Nom du participant : ")
    evenement_id = int(input("ID de l'événement : "))

    if str(evenement_id) not in evenements:
        print(f"{Couleurs.ROUGE}Événement introuvable.{Couleurs.RESET}")
        return

    if verifier_conflit_participant(dico, nom, evenement_id):
        print(f"{Couleurs.ROUGE}Conflit d'agenda détecté. Participant déjà occupé.{Couleurs.RESET}")
        return

    evenements[str(evenement_id)]["participants"].append(nom)
    if nom not in participants:
        participants[nom] = []
    participants[nom].append(evenement_id)

    sauvegarder_donnees(dico)
    print(f"{Couleurs.VERT}Participant ajouté à l'événement !{Couleurs.RESET}")

def retirer_participant(dico):
    pass

def afficher_agenda(dico):
    pass

def verifier_conflit_participant(dico, nom, nouvel_evenement_id):
    evenements = dico["evenements"]
    participants = dico["participants"]

    nouvel_evt = evenements[str(nouvel_evenement_id)]
    date = nouvel_evt["date"]
    debut = nouvel_evt["heure_debut"]
    fin = nouvel_evt["heure_fin"]

    if nom not in participants:
        return False

    for evt_id in participants[nom]:
        evt = evenements[str(evt_id)]
        if evt["date"] == date:
            if not (fin <= evt["heure_debut"] or debut >= evt["heure_fin"]):
                return True
    return False

def trouver_creneau_commun(dico):
    pass

def verifier_conflit_salle(dico):
    pass

def verifier_occupation_max_salle(dico):
    pass

def ajouter_evenement(dico):
    evenements = dico["evenements"]

    titre = input("Titre de l'événement : ")
    date = input("Date (AAAA-MM-JJ) : ")
    heure_debut = input("Heure de début (HH:mm) : ")
    heure_fin = input("Heure de fin (HH:mm) : ")
    salle = input("Salle (optionnelle) : ")

    evenement_id = str(len(evenements) + 1)
    evenements[evenement_id] = {
        "titre": titre,
        "date": date,
        "heure_debut": heure_debut,
        "heure_fin": heure_fin,
        "salle": salle,
        "participants": []
    }

    sauvegarder_donnees(dico)
    print(f"{Couleurs.VERT}Événement créé avec succès ! ID : {evenement_id}{Couleurs.RESET}")

def supprimer_evenement(dico):
    pass

def afficher_evenements_par_date(dico):
    pass

# --- Menu principal ---
def affiche_intro():
    choix = input(f"""
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
    dico = charger_donnees()

    valeurs_correctes = ['0','1','2','3','4','5']
    choix = affiche_intro()
    while choix not in valeurs_correctes:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Couleurs.ROUGE}Choix incorrect, veuillez rentrer une valeur correcte.{Couleurs.RESET}")
        choix = affiche_intro()

    if choix == '1':
        ajouter_evenement(dico)
    if choix == '2':
        ajouter_participant(dico)
    if choix == '3':
        afficher_agenda(dico)
    if choix == '4':
        trouver_creneau_commun(dico)
    if choix == '5':
        print(f"{Couleurs.VERT}Au revoir !{Couleurs.RESET}")