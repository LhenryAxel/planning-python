import os
import json
import datetime

# Gestion du fichier JSON
def charger_donnees():
    try:
        with open("dico.json", "r", encoding="utf-8") as f:
            donnees = json.load(f)
    except FileNotFoundError:
        donnees = {}

    donnees.setdefault("evenements", {})
    donnees.setdefault("participants", {})
    donnees.setdefault("salles", {})

    # Normaliser les IDs d'évènements des participants en chaînes
    for nom, lst in list(donnees["participants"].items()):
        donnees["participants"][nom] = [str(eid) for eid in lst]

    return donnees


def sauvegarder_donnees(donnees):
    with open("dico.json", "w", encoding="utf-8") as f:
        json.dump(donnees, f, indent=4, ensure_ascii=False)


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


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


# Fonctions principales

def ajouter_evenement(dico):
    evenements = dico["evenements"]

    clear_terminal()
    print(f"{Couleurs.GRAS}{Couleurs.MAGENTA}Création d'un nouvel événement{Couleurs.RESET}\n")

    titre = input("Titre de l'événement : ")
    date = input("Date (AAAA-MM-JJ) : ")
    heure_debut = input("Heure de début (HH:mm) : ")
    heure_fin = input("Heure de fin (HH:mm) : ")
    salle = input("Salle (id ou laisser vide) : ")

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
    print(f"\n{Couleurs.VERT}Événement créé avec succès ! ID : {evenement_id}{Couleurs.RESET}")
    input(f"{Couleurs.JAUNE}Appuyez sur Entrée pour revenir au menu...{Couleurs.RESET}")


def verifier_conflit_participant(dico, nom, nouvel_evenement_id):
    evenements = dico["evenements"]
    participants = dico["participants"]

    if nom not in participants:
        return False

    nouvel_evt = evenements[nouvel_evenement_id]  
    date = nouvel_evt["date"]
    debut = nouvel_evt["heure_debut"]
    fin = nouvel_evt["heure_fin"]

    for evt_id in participants[nom]:   
        evt = evenements[evt_id]
        if evt["date"] == date:
            # Chevauchement horaire
            if not (fin <= evt["heure_debut"] or debut >= evt["heure_fin"]):
                return True

    return False


def ajouter_participant(dico):
    evenements = dico["evenements"]
    participants = dico["participants"]

    clear_terminal()
    print(f"{Couleurs.GRAS}{Couleurs.MAGENTA}Ajout d'un participant à un événement{Couleurs.RESET}\n")

    nom = afficher_participants_avec_pagination(
        dico,
        titre="Sélection du participant à ajouter",
        message_selection="Entrez le numéro du participant"
    )

    if nom is None:
        return  # retour au menu

    if not evenements:
        print(f"{Couleurs.ROUGE}Aucun événement n'est encore créé. Impossible d'ajouter un participant.{Couleurs.RESET}")
        input(f"{Couleurs.JAUNE}Appuyez sur Entrée pour revenir au menu...{Couleurs.RESET}")
        return

    print(f"\n{Couleurs.CYAN}Liste des événements :{Couleurs.RESET}")

    for evt_id, evt in sorted(evenements.items(), key=lambda x: (x[1]["date"], x[1]["heure_debut"])):
        print(f"{Couleurs.VERT}{evt_id}{Couleurs.RESET} - {evt['titre']} le {evt['date']} "
              f"({evt['heure_debut']} - {evt['heure_fin']})")

    evenement_id = input(
        f"\n{Couleurs.JAUNE}Entrez l'ID de l'événement auquel ajouter {nom} : {Couleurs.RESET}"
    ).strip()

    if evenement_id not in evenements:
        print(f"{Couleurs.ROUGE}Événement introuvable.{Couleurs.RESET}")
        input(f"{Couleurs.JAUNE}Appuyez sur Entrée pour revenir au menu...{Couleurs.RESET}")
        return

    if nom in evenements[evenement_id]["participants"]:
        print(f"{Couleurs.ROUGE}Ce participant est déjà inscrit à cet événement.{Couleurs.RESET}")
        input(f"{Couleurs.JAUNE}Appuyez sur Entrée pour revenir au menu...{Couleurs.RESET}")
        return

    if verifier_conflit_participant(dico, nom, evenement_id):
        print(f"{Couleurs.ROUGE}Conflit d'agenda détecté. Participant déjà occupé sur ce créneau.{Couleurs.RESET}")
        input(f"{Couleurs.JAUNE}Appuyez sur Entrée pour revenir au menu...{Couleurs.RESET}")
        return

    evenements[evenement_id]["participants"].append(nom)

    if nom not in participants:
        participants[nom] = []
    if evenement_id not in participants[nom]:
        participants[nom].append(evement_id)

    sauvegarder_donnees(dico)

    print(f"\n{Couleurs.VERT}Participant ajouté à l'événement !{Couleurs.RESET}")
    input(f"{Couleurs.JAUNE}Appuyez sur Entrée pour revenir au menu...{Couleurs.RESET}")


def retirer_participant(dico):
    evenements = dico["evenements"]
    participants = dico["participants"]

    clear_terminal()
    print(f"{Couleurs.GRAS}{Couleurs.MAGENTA}Retirer un participant d'un événement{Couleurs.RESET}\n")

    # Sélection du participant via pagination
    participant_nom = afficher_participants_avec_pagination(
        dico,
        titre="Sélection du participant à retirer",
        message_selection="Entrez le numéro du participant"
    )

    if participant_nom is None:
        return 

    events_inscrits = []
    for evt_id, evt in evenements.items():
        if participant_nom in evt["participants"]:
            events_inscrits.append(evt_id)  

    if not events_inscrits:
        print(f"{Couleurs.JAUNE}Ce participant n'est inscrit à aucun événement.{Couleurs.RESET}")
        input(f"{Couleurs.JAUNE}Appuyez sur Entrée pour revenir au menu...{Couleurs.RESET}")
        return

    # Afficher les événements
    print(f"\n{Couleurs.CYAN}{participant_nom} est inscrit aux événements suivants :{Couleurs.RESET}")
    for evt_id in events_inscrits:
        evt = evenements[evt_id]
        print(f"{Couleurs.VERT}{evt_id}{Couleurs.RESET} - {evt['titre']} le {evt['date']} "
              f"({evt['heure_debut']} - {evt['heure_fin']})")

    # Choix de l'événement
    evenement_id = input(
        f"\n{Couleurs.JAUNE}Entrez l'ID de l'événement duquel retirer ce participant : {Couleurs.RESET}"
    ).strip()

    if evenement_id not in evenements:
        print(f"{Couleurs.ROUGE}Événement introuvable.{Couleurs.RESET}")
        input(f"{Couleurs.JAUNE}Appuyez sur Entrée pour revenir au menu...{Couleurs.RESET}")
        return

    if participant_nom not in evenements[evenement_id]["participants"]:
        print(f"{Couleurs.ROUGE}Ce participant n'est pas inscrit à cet événement.{Couleurs.RESET}")
        input(f"{Couleurs.JAUNE}Appuyez sur Entrée pour revenir au menu...{Couleurs.RESET}")
        return

    # Suppression dans l'événement
    evenements[evenement_id]["participants"].remove(participant_nom)

    # Suppression dans la liste du participant
    if participant_nom in participants:
        if evenement_id in participants[participant_nom]:
            participants[participant_nom].remove(evenement_id)

    sauvegarder_donnees(dico)

    print(f"\n{Couleurs.VERT}Participant retiré avec succès de l'événement.{Couleurs.RESET}")
    input(f"{Couleurs.JAUNE}Appuyez sur Entrée pour revenir au menu...{Couleurs.RESET}")



# Affichage avec pagination des participants 

def afficher_participants_avec_pagination(dico, titre="Liste des participants",
                                          message_selection="Entrez le numéro du participant"):
    participants_par_page = 10
    participants_noms = sorted(dico["participants"].keys())

    if not participants_noms:
        print(f"{Couleurs.ROUGE}Aucun participant enregistré pour le moment.{Couleurs.RESET}")
        input(f"{Couleurs.JAUNE}Appuyez sur Entrée pour revenir au menu...{Couleurs.RESET}")
        return None

    participants_list = [(str(i), nom) for i, nom in enumerate(participants_noms, start=1)]
    total_participants = len(participants_list)
    total_pages = (total_participants + participants_par_page - 1) // participants_par_page
    page_actuelle = 1

    while True:
        clear_terminal()
        print(f"{Couleurs.GRAS}{Couleurs.MAGENTA}{titre}{Couleurs.RESET}\n")

        debut = (page_actuelle - 1) * participants_par_page
        fin = min(debut + participants_par_page, total_participants)

        for numero, nom in participants_list[debut:fin]:
            print(f"{Couleurs.VERT}{numero}{Couleurs.RESET} - {nom}")

        print(f"\n{Couleurs.CYAN}Page {page_actuelle}/{total_pages}{Couleurs.RESET}")

        options = (f"{Couleurs.JAUNE}\n{message_selection}, "
                   f"{Couleurs.BLEU}'<'{Couleurs.JAUNE} pour page précédente, "
                   f"{Couleurs.BLEU}'>'{Couleurs.JAUNE} pour page suivante, "
                   f"ou {Couleurs.ROUGE}'q'{Couleurs.JAUNE} pour quitter : "
                   f"{Couleurs.RESET}")

        choix = input(options)

        if choix == '<':
            page_actuelle = total_pages if page_actuelle == 1 else page_actuelle - 1
            continue
        elif choix == '>':
            page_actuelle = 1 if page_actuelle == total_pages else page_actuelle + 1
            continue
        elif choix.lower() == 'q':
            return None
        else:
            # Vérifier si le choix correspond à un numéro
            for numero, nom in participants_list:
                if choix == numero:
                    return nom
            print(f"{Couleurs.ROUGE}Choix invalide.{Couleurs.RESET}")
            input(f"{Couleurs.JAUNE}Appuyez sur Entrée pour continuer...{Couleurs.RESET}")


def afficher_agenda(dico):
    # Sélection du participant via pagination
    participant_nom = afficher_participants_avec_pagination(
        dico,
        titre="Affichage de l'agenda d'un participant",
        message_selection="Entrez le numéro du participant"
    )

    if participant_nom is None:
        return

    clear_terminal()
    print(f"{Couleurs.CYAN}Agenda de {participant_nom} :{Couleurs.RESET}\n")

    evenements = dico["evenements"]
    # On parcourt tous les événements pour voir ceux où il est inscrit
    a_trouve = False
    for evt_id, details in sorted(evenements.items(), key=lambda x: (x[1]["date"], x[1]["heure_debut"])):
        if participant_nom in details["participants"]:
            a_trouve = True
            salle_id = details.get("salle", "")
            salle_nom = ""
            if salle_id and salle_id in dico["salles"]:
                salle_nom = f" en {dico['salles'][salle_id]['nom']}"
            print(f"- {details['titre']} le {details['date']} de "
                  f"{details['heure_debut']} à {details['heure_fin']}{salle_nom}")

    if not a_trouve:
        print(f"{Couleurs.JAUNE}Aucun événement trouvé pour ce participant.{Couleurs.RESET}")

    input(f"\n{Couleurs.JAUNE}Appuyez sur Entrée pour revenir au menu...{Couleurs.RESET}")

def supprimer_evenement(dico):
    evenements = dico["evenements"]
    participants = dico["participants"]

    clear_terminal()
    print(f"{Couleurs.GRAS}{Couleurs.MAGENTA}Suppression d'un événement{Couleurs.RESET}\n")

    date_recherche = input("Entrez la date de l'événement à supprimer (AAAA-MM-JJ) : ")

    # Filtrer les événements de cette date
    events_trouves = {
        eid: evt for eid, evt in evenements.items() if evt["date"] == date_recherche
    }

    if not events_trouves:
        print(f"{Couleurs.ROUGE}Aucun événement trouvé à cette date.{Couleurs.RESET}")
        input(f"{Couleurs.JAUNE}Appuyez sur Entrée pour revenir au menu...{Couleurs.RESET}")
        return

    print(f"\n{Couleurs.CYAN}Événements le {date_recherche} :{Couleurs.RESET}")
    for eid, evt in events_trouves.items():
        print(f"{Couleurs.VERT}{eid}{Couleurs.RESET} - {evt['titre']} "
              f"({evt['heure_debut']} → {evt['heure_fin']})")

    evenement_id = input(f"\n{Couleurs.JAUNE}Entrez l'ID de l'événement à supprimer : {Couleurs.RESET}")

    if evenement_id not in events_trouves:
        print(f"{Couleurs.ROUGE}Événement introuvable.{Couleurs.RESET}")
        input(f"{Couleurs.JAUNE}Appuyez sur Entrée pour revenir au menu...{Couleurs.RESET}")
        return

    del evenements[evenement_id]

    for nom, liste_evt in participants.items():
        if evenement_id in liste_evt:
            liste_evt.remove(evenement_id)

    sauvegarder_donnees(dico)
    print(f"{Couleurs.VERT}Événement supprimé avec succès.{Couleurs.RESET}")
    input(f"{Couleurs.JAUNE}Appuyez sur Entrée pour revenir au menu...{Couleurs.RESET}")

def trouver_creneau_commun(dico):
    participants_selectionnes = []  # liste de noms de participants
    participants_par_page = 10
    page_actuelle = 1

    participants_noms = sorted(dico["participants"].keys())
    if not participants_noms:
        print(f"{Couleurs.ROUGE}Aucun participant enregistré, impossible de chercher un créneau commun.{Couleurs.RESET}")
        input(f"{Couleurs.JAUNE}Appuyez sur Entrée pour revenir au menu...{Couleurs.RESET}")
        return

    while True:
        participants_list = [(str(i), nom) for i, nom in enumerate(participants_noms, start=1)]
        total_participants = len(participants_list)
        total_pages = (total_participants + participants_par_page - 1) // participants_par_page

        clear_terminal()
        print(f"{Couleurs.GRAS}{Couleurs.MAGENTA}Recherche d'un créneau commun{Couleurs.RESET}\n")

        # Affichage des participants déjà choisis
        if participants_selectionnes:
            print(f"{Couleurs.CYAN}Participants sélectionnés :{Couleurs.RESET}")
            for nom in participants_selectionnes:
                print(f"  - {Couleurs.VERT}{nom}{Couleurs.RESET}")
            print()

        # Calcul de la page actuelle
        debut = (page_actuelle - 1) * participants_par_page
        fin = min(debut + participants_par_page, total_participants)

        print(f"{Couleurs.CYAN}Liste des participants :{Couleurs.RESET}")
        for numero, nom in participants_list[debut:fin]:
            if nom in participants_selectionnes:
                print(f"{Couleurs.VERT}{numero}{Couleurs.RESET} - {nom} {Couleurs.JAUNE}(déjà sélectionné){Couleurs.RESET}")
            else:
                print(f"{Couleurs.VERT}{numero}{Couleurs.RESET} - {nom}")

        print(f"\n{Couleurs.CYAN}Page {page_actuelle}/{total_pages}{Couleurs.RESET}")

        options = f"{Couleurs.JAUNE}\nEntrez le numéro d'un participant pour l'ajouter"
        options += f", {Couleurs.BLEU}'<'{Couleurs.JAUNE} pour page précédente"
        options += f", {Couleurs.BLEU}'>'{Couleurs.JAUNE} pour page suivante"
        options += f", {Couleurs.VERT}'0'{Couleurs.JAUNE} pour lancer la recherche"
        options += f", ou {Couleurs.ROUGE}'q'{Couleurs.JAUNE} pour quitter : {Couleurs.RESET}"

        choix = input(options)

        if choix == '<':
            page_actuelle = total_pages if page_actuelle == 1 else page_actuelle - 1
            continue
        elif choix == '>':
            page_actuelle = 1 if page_actuelle == total_pages else page_actuelle + 1
            continue
        elif choix == '0':
            # au moins 2 participants
            if len(participants_selectionnes) < 2:
                print(f"{Couleurs.ROUGE}Vous devez sélectionner au moins 2 participants.{Couleurs.RESET}")
                input(f"{Couleurs.JAUNE}Appuyez sur Entrée pour continuer...{Couleurs.RESET}")
                continue

            # Demande durée
            clear_terminal()
            duree_heure = input(
                f"{Couleurs.JAUNE}Entrez la durée du créneau recherché en heures (ex: 1.5) : {Couleurs.RESET}"
            )
            while duree_heure.replace('.', '', 1).isdigit() is False or float(duree_heure) <= 0:
                print(f"{Couleurs.ROUGE}Durée invalide. Veuillez entrer un nombre positif.{Couleurs.RESET}")
                duree_heure = input(
                    f"{Couleurs.JAUNE}Entrez la durée du créneau recherché en heures (ex: 1.5) : {Couleurs.RESET}"
                )
            duree_heure = float(duree_heure)

            print(f"{Couleurs.CYAN}Recherche d'un créneau commun pour :{Couleurs.RESET}")
            for nom in participants_selectionnes:
                print(f"  - {nom}")

            # Récupère tous les événements des participants
            evenements_participants = []
            for id_event, details in dico["evenements"].items():
                if any(nom in details["participants"] for nom in participants_selectionnes):
                    evenements_participants.append({
                        'date': details['date'],
                        'heure_debut': details['heure_debut'],
                        'heure_fin': details['heure_fin'],
                        'titre': details['titre'],
                        'salle': details.get('salle', '')
                    })

            evenements_participants.sort(key=lambda x: (x['date'], x['heure_debut']))

            def heure_en_minutes(heure_str):
                h, m = map(int, heure_str.split(':'))
                return h * 60 + m

            def minutes_en_heure(minutes):
                h = minutes // 60
                m = minutes % 60
                return f"{h:02d}:{m:02d}"

            duree_minutes = int(duree_heure * 60)
            heure_debut_matin = 9 * 60
            heure_fin_matin = 12 * 60 + 30
            heure_debut_aprem = 14 * 60
            heure_fin_aprem = 18 * 60

            date_actuelle = datetime.datetime.now().date()
            creneau_trouve = None

            # On teste sur 30 jours
            dates_a_tester = [
                (date_actuelle + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(31)
            ]

            for date_test in dates_a_tester:
                events_du_jour = [e for e in evenements_participants if e['date'] == date_test]

                intervalles_occupes_matin = []
                intervalles_occupes_aprem = []

                for event in events_du_jour:
                    debut = heure_en_minutes(event['heure_debut'])
                    fin = heure_en_minutes(event['heure_fin'])

                    if fin <= heure_fin_matin:
                        intervalles_occupes_matin.append((debut, fin))
                    elif debut >= heure_debut_aprem:
                        intervalles_occupes_aprem.append((debut, fin))
                    else:
                        if debut < heure_fin_matin:
                            intervalles_occupes_matin.append((debut, min(fin, heure_fin_matin)))
                        if fin > heure_debut_aprem:
                            intervalles_occupes_aprem.append((max(debut, heure_debut_aprem), fin))

                intervalles_occupes_matin.sort()
                intervalles_occupes_aprem.sort()

                # Matin
                if not intervalles_occupes_matin:
                    if heure_fin_matin - heure_debut_matin >= duree_minutes:
                        creneau_trouve = {
                            'date': date_test,
                            'heure_debut': minutes_en_heure(heure_debut_matin),
                            'heure_fin': minutes_en_heure(heure_debut_matin + duree_minutes)
                        }
                        break
                else:
                    premier_event_debut = intervalles_occupes_matin[0][0]
                    if premier_event_debut - heure_debut_matin >= duree_minutes:
                        creneau_trouve = {
                            'date': date_test,
                            'heure_debut': minutes_en_heure(heure_debut_matin),
                            'heure_fin': minutes_en_heure(heure_debut_matin + duree_minutes)
                        }
                        break

                    for i in range(len(intervalles_occupes_matin) - 1):
                        fin_event_actuel = intervalles_occupes_matin[i][1]
                        debut_event_suivant = intervalles_occupes_matin[i + 1][0]

                        if debut_event_suivant - fin_event_actuel >= duree_minutes:
                            creneau_trouve = {
                                'date': date_test,
                                'heure_debut': minutes_en_heure(fin_event_actuel),
                                'heure_fin': minutes_en_heure(fin_event_actuel + duree_minutes)
                            }
                            break

                    if creneau_trouve:
                        break

                    dernier_event_fin = intervalles_occupes_matin[-1][1]
                    if heure_fin_matin - dernier_event_fin >= duree_minutes:
                        creneau_trouve = {
                            'date': date_test,
                            'heure_debut': minutes_en_heure(dernier_event_fin),
                            'heure_fin': minutes_en_heure(dernier_event_fin + duree_minutes)
                        }
                        break

                # Après-midi
                if not intervalles_occupes_aprem:
                    if heure_fin_aprem - heure_debut_aprem >= duree_minutes:
                        creneau_trouve = {
                            'date': date_test,
                            'heure_debut': minutes_en_heure(heure_debut_aprem),
                            'heure_fin': minutes_en_heure(heure_debut_aprem + duree_minutes)
                        }
                        break
                else:
                    premier_event_debut = intervalles_occupes_aprem[0][0]
                    if premier_event_debut - heure_debut_aprem >= duree_minutes:
                        creneau_trouve = {
                            'date': date_test,
                            'heure_debut': minutes_en_heure(heure_debut_aprem),
                            'heure_fin': minutes_en_heure(heure_debut_aprem + duree_minutes)
                        }
                        break

                    for i in range(len(intervalles_occupes_aprem) - 1):
                        fin_event_actuel = intervalles_occupes_aprem[i][1]
                        debut_event_suivant = intervalles_occupes_aprem[i + 1][0]

                        if debut_event_suivant - fin_event_actuel >= duree_minutes:
                            creneau_trouve = {
                                'date': date_test,
                                'heure_debut': minutes_en_heure(fin_event_actuel),
                                'heure_fin': minutes_en_heure(fin_event_actuel + duree_minutes)
                            }
                            break

                    if creneau_trouve:
                        break

                    dernier_event_fin = intervalles_occupes_aprem[-1][1]
                    if heure_fin_aprem - dernier_event_fin >= duree_minutes:
                        creneau_trouve = {
                            'date': date_test,
                            'heure_debut': minutes_en_heure(dernier_event_fin),
                            'heure_fin': minutes_en_heure(dernier_event_fin + duree_minutes)
                        }
                        break

            print(f"\n{Couleurs.GRAS}Résultat de la recherche :{Couleurs.RESET}")
            if creneau_trouve:
                print(f"{Couleurs.VERT}✓ Créneau disponible trouvé !{Couleurs.RESET}")
                print(f"{Couleurs.CYAN}Date :{Couleurs.RESET} {creneau_trouve['date']}")
                print(f"{Couleurs.CYAN}Horaire :{Couleurs.RESET} {creneau_trouve['heure_debut']} - {creneau_trouve['heure_fin']}")
                print(f"{Couleurs.CYAN}Durée :{Couleurs.RESET} {duree_heure} h")
                print(f"{Couleurs.CYAN}Participants :{Couleurs.RESET} {len(participants_selectionnes)} personne(s)")

                # salles dispo (optionnel, dépend du JSON)
                salles_disponibles = []
                for id_salle, details_salle in dico["salles"].items():
                    if details_salle['capacite'] >= len(participants_selectionnes):
                        salle_occupee = False
                        for id_event, details_event in dico["evenements"].items():
                            if (details_event.get('salle') == id_salle and
                                details_event['date'] == creneau_trouve['date']):
                                event_debut = heure_en_minutes(details_event['heure_debut'])
                                event_fin = heure_en_minutes(details_event['heure_fin'])
                                creneau_debut = heure_en_minutes(creneau_trouve['heure_debut'])
                                creneau_fin = heure_en_minutes(creneau_trouve['heure_fin'])
                                if event_debut < creneau_fin and event_fin > creneau_debut:
                                    salle_occupee = True
                                    break
                        if not salle_occupee:
                            salles_disponibles.append({
                                'id': id_salle,
                                'nom': details_salle['nom'],
                                'capacite': details_salle['capacite']
                            })

                if salles_disponibles:
                    print(f"\n{Couleurs.CYAN}Salles disponibles :{Couleurs.RESET}")
                    for salle in salles_disponibles:
                        print(f"  - {Couleurs.VERT}{salle['nom']}{Couleurs.RESET} (capacité: {salle['capacite']} personnes)")
                else:
                    if dico["salles"]:
                        print(f"\n{Couleurs.ROUGE}⚠ Aucune salle disponible pour ce créneau.{Couleurs.RESET}")
            else:
                print(f"{Couleurs.ROUGE}✗ Aucun créneau disponible trouvé dans les 30 prochains jours.{Couleurs.RESET}")

            input(f"\n{Couleurs.JAUNE}Appuyez sur Entrée pour revenir au menu...{Couleurs.RESET}")
            return

        elif choix.lower() == 'q':
            return
        else:
            # Ajout du participant
            for numero, nom in participants_list:
                if choix == numero:
                    if nom in participants_selectionnes:
                        print(f"{Couleurs.ROUGE}Ce participant est déjà sélectionné !{Couleurs.RESET}")
                    else:
                        participants_selectionnes.append(nom)
                        print(f"{Couleurs.VERT}{nom} a été ajouté à la sélection.{Couleurs.RESET}")
                    input(f"{Couleurs.JAUNE}Appuyez sur Entrée pour continuer...{Couleurs.RESET}")
                    break
            else:
                print(f"{Couleurs.ROUGE}Choix invalide.{Couleurs.RESET}")
                input(f"{Couleurs.JAUNE}Appuyez sur Entrée pour continuer...{Couleurs.RESET}")

def verifier_conflit_salle(dico):
    pass


def verifier_occupation_max_salle(dico):
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
{Couleurs.VERT}5{Couleurs.RESET} - Retirer un participant
{Couleurs.VERT}6{Couleurs.RESET} - Supprimer un événement
{Couleurs.ROUGE}7{Couleurs.RESET} - Quitter
                
{Couleurs.JAUNE}Votre choix : {Couleurs.RESET}""")
    return choix


if __name__ == "__main__":
    dico = charger_donnees()

    while True:
        clear_terminal()
        choix = affiche_intro()

        if choix not in ['1', '2', '3', '4', '5', '6', '7']:
            print(f"{Couleurs.ROUGE}Choix incorrect, veuillez rentrer une valeur correcte.{Couleurs.RESET}")
            input(f"{Couleurs.JAUNE}Appuyez sur Entrée pour continuer...{Couleurs.RESET}")
            continue

        if choix == '1':          # 1 - Création Evènement
            ajouter_evenement(dico)
        elif choix == '2':        # 2 - Ajout Participant
            ajouter_participant(dico)
        elif choix == '3':        # 3 - Affichage Agenda
            afficher_agenda(dico)
        elif choix == '4':        # 4 - Créneau Commun
            trouver_creneau_commun(dico)
        elif choix == '5':        # 5 - Retirer participant
            retirer_participant(dico)
        elif choix == '6':        # 6 - Supprimer un évènement
            supprimer_evenement(dico)
        elif choix == '7':        # 7 - Quitter
            print(f"{Couleurs.VERT}Au revoir !{Couleurs.RESET}")
            break