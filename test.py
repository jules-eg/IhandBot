from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time
from dotenv import load_dotenv
import os
load_dotenv()
usr = os.getenv("user")
mdp = os.getenv("mdp")

print(usr)
print(mdp)
tarifs_arbitrage = {"N2F_CNA_FFHB": 80.00, "N3M_CNA_FFHB": 80.00, "N3F_PCO": 60.00, "PNM": 60.00, "PNF": 50.00, "EXC_M": 50.00, "EXC_F": 45.00, "HON_M": 45.00, "HON_F": 40.00, "D1T": 35.00, "D2T": 30.00, "D3T_M": 25.00, "D4T_M": 25.00, "D5T_M": 25.00, "D2FPL": 30.00, "U20FPL": 30.00, "U19MPL": 35.00, "U19M-44": 30.00, "U18M_CDF": 50.00, "U17F_CDF": 50.00, "U17MPL": 30.00, "U16MPL": 30.00, "U15MPL": 30.00, "JAJ_CTA_CLUB": 20.00, "CHAMP_JEUNES_TERR": 15.00}
# Crée les options pour Firefox
options = Options()
options.headless = True  # Si tu veux que le navigateur soit visible, sinon True pour mode sans tête

# Chemin vers le geckodriver
geckodriver_path = "geckodriver"
service = Service(geckodriver_path)

def get_tarif(categorie, tarifs):
    # Remplace les séparateurs par des espaces et découpe la chaîne en éléments
    elements = set(categorie.replace(";", " ").split())  
    for key in tarifs.keys():
        # Vérification si chaque clé du dictionnaire contient les éléments de la chaîne
        if all(part in key for part in elements) and any(part == key for part in elements):
            return tarifs[key]
    return None  # Aucun tarif trouvé


def extract_match_info(match_element):
    match_info = {}
    # Fonction arbitre
    fonction = match_element.find_element(By.TAG_NAME, "h2").text
    match_info['fonction'] = fonction if fonction else None


    # Date et heure du match
    date_heure = match_element.find_element(By.CLASS_NAME, "match").text
    match_info['date_heure'] = date_heure if date_heure else None

    # Informations championat
    championat = match_element.find_elements(By.CLASS_NAME, "champ")
    match_info['championat'] = championat[0].text if championat else None

    #Tarif présumé
    match_info['tarif'] = get_tarif(match_info['championat'], tarifs_arbitrage) if championat else None

    # Informations sur le match
    details_match = match_element.find_elements(By.CLASS_NAME, "eq")
    if details_match:
        teams = details_match[0].text.split('-')
        match_info['equipe1'] = teams[0].strip()
        match_info['equipe2'] = teams[1].strip()

    # Récupérer l'arbitre
    arbitre_info = match_element.find_element(By.CLASS_NAME, "moi").text
    match_info['arbitre'] = arbitre_info.split(" ")[0] + " " + arbitre_info.split(" ")[1]

    # Lien vers la fiche de frais et la convocation
    liens = match_element.find_elements(By.TAG_NAME, "a")
    match_info['fiche_de_frais'] = liens[0].get_attribute("href") if len(liens) > 0 else None
    match_info['convocation'] = liens[1].get_attribute("href") if len(liens) > 1 else None

    return match_info

# Fonction pour récupérer tous les matchs et créer un dictionnaire
def extract_all_matches(driver):
    all_matches = []
    match_elements = driver.find_elements(By.CLASS_NAME, "package_arb")

    for match_element in match_elements:
        match_info = extract_match_info(match_element)
        all_matches.append(match_info)
    
    return all_matches

# Fonction pour ouvrir un lien dans un nouvel onglet
def open_link_in_new_tab(driver, url):
    driver.execute_script(f"window.open('{url}', '_blank');")
    time.sleep(2)  # Attendre quelques secondes pour que l'onglet se charge

def update_ihand():
    # Démarre Firefox sans profil spécifique
    driver = webdriver.Firefox(options=options, service=service)

    # Fais ce que tu veux avec le driver ici
    driver.get('https://ihand-arbitrage.ffhandball.org/')

    # Remplir le formulaire de connexion
    username = driver.find_element(By.ID, "entered_login")
    password = driver.find_element(By.ID, "entered_password")
    username.send_keys(usr)
    password.send_keys(mdp + Keys.ENTER)
    driver.get('https://ihand-arbitrage.ffhandball.org/index.php?file=compte')
    return extract_all_matches(driver)
matches = update_ihand()
# Afficher les résultats pour voir ce que ça donne



for match in matches:
    for e in match:
        print(e, match[e])
    print('******************************************************')
    
