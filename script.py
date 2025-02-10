# *DEPENDENCES : 
#Selenium
#print("Selenium")
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Telegram
#print("Telegram")
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
# Others
#print("Others")
import time
from dotenv import load_dotenv
import os

# *Récuperation des elements de .env
#print("Récupération des éléments de .env")
load_dotenv()
usr = os.getenv("user")
mdp = os.getenv("mdp")
token = os.getenv("TOKEN")

# *Init de Selenium pour firefox
#print("Init de Selenium pour firefox")
# Crée les options pour Firefox
#print("Crée les options pour Firefox")
options = Options()
options.add_argument("--headless")  # Exécuter en arrière-plan
options.add_argument("--no-sandbox")  # Évite des erreurs de permissions
options.add_argument("--disable-dev-shm-usage")  # Évite des problèmes de mémoire


# Chemin vers le geckodriver
#print("Chemin vers le geckodriver")
chromedriver_path = "chromedriver"  # Assure-toi d'avoir chromedriver installé
service = Service(chromedriver_path)


#Variables globales pour les tarifs et les matchs
#print("Variables globales pour les tarifs et les matchs")
tarifs_arbitrage = {"N2F_CNA_FFHB": 80.00, "N3M_CNA_FFHB": 80.00, "N3F_PCO": 60.00, "PNM": 60.00, "PNF": 50.00, "EXC_M": 50.00, "EXC_F": 45.00, "HON_M": 45.00, "HON_F": 40.00, "D1T": 35.00, "D2T": 30.00, "D3T_M": 25.00, "D4T_M": 25.00, "D5T_M": 25.00, "D2FPL": 30.00, "U20FPL": 30.00, "U19MPL": 35.00, "U19M-44": 30.00, "U18M_CDF": 50.00, "U17F_CDF": 50.00, "U17MPL": 30.00, "U16MPL": 30.00, "U15MPL": 30.00, "JAJ_CTA_CLUB": 20.00, "CHAMP_JEUNES_TERR": 15.00}
matches = []
#* Fonctions de recherche dans Ihand
#print("Fonctions de recherche dans Ihand")
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

    # Lien vers la fiche de frais et la convocation, l'adresse et création feuille de frais
    liens = match_element.find_elements(By.TAG_NAME, "a")
    #verifie que lien[3] est different de none
    if len(liens) > 3:
        match_info['fiche_de_frais'] = liens[0].get_attribute("href") if len(liens) > 0 else None
        match_info['convocation'] = liens[1].get_attribute("href") if len(liens) > 1 else None
        match_info['adresse'] = liens[2].get_attribute("href") if len(liens) > 2 else None
        match_info['crea_frais'] = liens[3].get_attribute("href") if len(liens) > 3 else None
    else:
        match_info['convocation'] = liens[1].get_attribute("href") if len(liens) > 0 else None
        match_info['adresse'] = liens[1].get_attribute("href") if len(liens) > 1 else None
        match_info['crea_frais'] = liens[2].get_attribute("href") if len(liens) > 2 else None
        match_info['fiche_de_frais'] = None
    return match_info

# Fonction pour récupérer tous les matchs et créer un dictionnaire
#print("Fonction pour récupérer tous les matchs et créer un dictionnaire")   
def extract_all_matches(driver):
    all_matches = []
    match_elements = driver.find_elements(By.CLASS_NAME, "package_arb")

    for match_element in match_elements:
        match_info = extract_match_info(match_element)
        all_matches.append(match_info)
    return all_matches

# Fonction pour récupérer le tarif en fonction de la catégorie
#print("Fonction pour récupérer le tarif en fonction de la catégorie")
def get_tarif(categorie, tarifs):
    # Remplace les séparateurs par des espaces et découpe la chaîne en éléments
    #print("Remplace les séparateurs par des espaces et découpe la chaîne en éléments")
    elements = set(categorie.replace(";", " ").split())  
    for key in tarifs.keys():
        # Vérification si chaque clé du dictionnaire contient les éléments de la chaîne
        #print("Vérification si chaque clé du dictionnaire contient les éléments de la chaîne")
        if all(part in key for part in elements) and any(part == key for part in elements):
            return tarifs[key]
    #print("Aucun tarif trouvé")
    return None  # Aucun tarif trouvé


# Fonction update de Ihand pour récupérer les infos
#print("Fonction update de Ihand pour récupérer les infos")
def update_ihand():
    # Démarre Firefox sans profil spécifique
    #print("Démarre Firefox sans profil spécifique")
driver = webdriver.Chrome(options=options, service=service)
    #Connection au site
    #print("Connection au site")
    driver.get('https://ihand-arbitrage.ffhandball.org/')
    # Remplir le formulaire de connexion
    #print("Remplir le formulaire de connexion")
    username = driver.find_element(By.ID, "entered_login")
    password = driver.find_element(By.ID, "entered_password")
    username.send_keys(usr)
    password.send_keys(mdp + Keys.ENTER)
    driver.get('https://ihand-arbitrage.ffhandball.org/index.php?file=compte')
    matches = extract_all_matches(driver)
    driver.quit()
    return matches
#* BOT TELEGRAM
#print("BOT TELEGRAM")
# Variables globales pour le bot
#print("Variables globales pour le bot")
user_selection = {}

# Commande de démarrage
#print("Commande de démarrage")
async def start(update, context):
    await update.message.reply_text("""
                                    👋 Bienvenue ! Tapez /match pour voir la liste des matchs. 🏐
                                    Vous pouvez également taper /update pour mettre à jour les matchs depuis Ihand. 🔄
                                    """)

# Commande pour afficher la liste des matchs
#print("Commande pour afficher la liste des matchs")
async def match(update, context):
    #si pas de match, retourner pas de match pour le moment
    #print("si pas de match, retourner pas de match pour le moment")
    if not matches:
        await update.message.reply_text("Pas de match pour le moment 🫤")
    else:
        keyboard = [[InlineKeyboardButton(f"🗓 {m['date_heure']}", callback_data=f"match_{idx}")] for idx, m in enumerate(matches)]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Sélectionne un match : 📅", reply_markup=reply_markup)

# Commande pour gérer le choix d'un match
#print("Commande pour gérer le choix d'un match")
async def handle_match_choice(update, context):
    query = update.callback_query
    match_index = int(query.data.split('_')[1])
    user_selection[query.from_user.id] = match_index
    match = matches[match_index]

    keyboard = [
        [InlineKeyboardButton("ℹ️ Infos détaillées", callback_data="infos")],
        [InlineKeyboardButton("📜 Convocation", callback_data="convocation")],
        [InlineKeyboardButton("💸 Fiche de frais", callback_data="frais")],
        [InlineKeyboardButton("📋 Voir la liste des matchs", callback_data="show_matches")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.answer()
    await query.edit_message_text(f"Vous avez sélectionné le match : {match['date_heure']}\nQue voulez-vous faire ?", reply_markup=reply_markup)

# Commande pour afficher les détails d'un match
#print("Commande pour afficher les détails d'un match")
async def handle_details(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    match_index = user_selection.get(user_id)
    if match_index is not None:
        match = matches[match_index]
        details_text = f"""🏐 Détails du match :
        📅 Match : {match['date_heure']}
        🤾‍♀️ Équipe 1 : {match['equipe1']}
        🤾🏼 Équipe 2 : {match['equipe2']}
        👨‍⚖️ Arbitre : {match['arbitre']}
        📍 Lieu : [Clique ici pour voir l'adresse]({match['adresse']})
        💰 Tarif (Estimatif) : {match['tarif']}€"""
        keyboard = [
            [InlineKeyboardButton("📋 Voir la liste des matchs", callback_data="show_matches")],
            [InlineKeyboardButton("◀️ Retour", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(details_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await query.edit_message_text("Aucun match sélectionné.")

# Commande pour afficher la convocation d'un match
#print("Commande pour afficher la convocation d'un match")
async def handle_convocation(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    match_index = user_selection.get(user_id)
    if match_index is not None:
        match = matches[match_index]
        details_text = f"📅 Convocation : {match['convocation']}"
        keyboard = [
            [InlineKeyboardButton("📋 Voir la liste des matchs", callback_data="show_matches")],
            [InlineKeyboardButton("◀️ Retour", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(details_text, reply_markup=reply_markup)
    else:
        await query.edit_message_text("Aucun match sélectionné.")

# Commande pour afficher la fiche de frais d'un match
#print("Commande pour afficher la fiche de frais d'un match")
async def handle_frais(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    match_index = user_selection.get(user_id)
    if match_index is not None:
        match = matches[match_index]
        if match['fiche_de_frais'] is None:
            text_detail = "Aucune fiche de frais disponible."
        else:
            detail_text = f"📅 Fiche de frais : {match['fiche_de_frais']}"
        keyboard = [
            [InlineKeyboardButton("📋 Voir la liste des matchs", callback_data="show_matches")],
            [InlineKeyboardButton("◀️ Retour", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(detail_text, reply_markup=reply_markup)
    else:
        await query.edit_message_text("Aucun match sélectionné.")

# Commande pour afficher la liste des matchs
#print("Commande pour afficher la liste des matchs")
async def handle_show_matches(update, context):
    keyboard = [[InlineKeyboardButton(f"🗓 {m['date_heure']}", callback_data=f"match_{idx}")] for idx, m in enumerate(matches)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("Sélectionne un match : 📅", reply_markup=reply_markup)

# Commande pour revenir en arrière
#print("Commande pour revenir en arrière")
async def handle_back(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    match_index = user_selection.get(user_id)
    if match_index is not None:
        match = matches[match_index]
        keyboard = [
            [InlineKeyboardButton("ℹ️ Infos détaillées", callback_data="infos")],
            [InlineKeyboardButton("📜 Convocation", callback_data="convocation")],
            [InlineKeyboardButton("💸 Fiche de frais", callback_data="frais")],
            [InlineKeyboardButton("📋 Voir la liste des matchs", callback_data="show_matches")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.answer()
        await query.edit_message_text(f"Vous avez sélectionné le match : {match['date_heure']}\nQue voulez-vous faire ?", reply_markup=reply_markup)
    else:
        await query.edit_message_text("Aucun match sélectionné.")

# Execution de update de Ihand a partir d'un input telegram
#print("Execution de update de Ihand a partir d'un input telegram")
async def update_ihand_telegram(update, context):
    global matches
    matches = update_ihand()
    await update.message.reply_text("✅ Mise à jour des matchs effectuée.")

# Lancement de l'application
#print("Lancement de l'application")
def main():
    update_ihand()
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('match', match))
    app.add_handler(CommandHandler('update', update_ihand_telegram))
    app.add_handler(CallbackQueryHandler(handle_match_choice, pattern="^match_"))
    app.add_handler(CallbackQueryHandler(handle_details, pattern="^infos"))
    app.add_handler(CallbackQueryHandler(handle_convocation, pattern="^convocation"))
    app.add_handler(CallbackQueryHandler(handle_frais, pattern="^frais"))
    app.add_handler(CallbackQueryHandler(handle_show_matches, pattern="^show_matches"))
    app.add_handler(CallbackQueryHandler(handle_back, pattern="^back"))

    app.run_polling(poll_interval=5)
main()