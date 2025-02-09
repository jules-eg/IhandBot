import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

matches = []

# Ajout des matchs à la liste
a = dict({'fonction': 'Fonction arbitre', 'date_heure': 'Dimanche 23/02/2025\n11:30', 'equipe1': 'NORT AC HANDBALL', 'equipe2': 'HB STE LUCE SUR LOIRE 1', 'arbitre': 'EVENO-GALLEN JULES', 'fiche_de_frais': 'https://ihand-arbitrage.ffhandball.org/modules/compte/aff_pdf.php?DATE=20250223&IND=2034073&CODE=UAFXBLM&VERSION=', 'convocation': 'https://ihand-arbitrage.ffhandball.org/file/convocation/2025-02-23_UAFXBLM_arb_convoc.pdf'})
b = dict({'fonction': 'Fonction arbitre', 'date_heure': 'Samedi 08/02/2025\n18:00', 'equipe1': "UNION SPORTIVE GRANDE PRESQU'ILE HANDBALL", 'equipe2': 'AL ST ETIENNE DE MONTLUC', 'arbitre': 'EVENO-GALLEN JULES', 'fiche_de_frais': 'https://media-ffhb-fdm.ffhandball.fr/fdm/U/A/F/W/UAFWHVM.pdf', 'convocation': 'https://ihand-arbitrage.ffhandball.org/modules/compte/aff_pdf.php?DATE=20250208&IND=2034073&CODE=UAFWHVM&VERSION='})
c = dict({'fonction': 'Fonction arbitre', 'date_heure': 'Samedi 01/02/2025\n19:00', 'equipe1': 'ASSOCIATION HANDBALL VALLET', 'equipe2': 'FANS HB LIGNE 2', 'arbitre': 'EVENO-GALLEN JULES', 'fiche_de_frais': 'https://media-ffhb-fdm.ffhandball.fr/fdm/U/A/F/V/UAFVGGR.pdf', 'convocation': 'https://ihand-arbitrage.ffhandball.org/modules/compte/aff_pdf.php?DATE=20250201&IND=2034073&CODE=UAFVGGR&VERSION='})
d = dict({'fonction': None, 'date_heure': None, 'equipe1': None, 'equipe2': None, 'arbitre': None, 'fiche_de_frais': None, 'convocation': None})

for i in a, b, c:
    matches.append(i)

load_dotenv()
token = os.getenv("TOKEN")

user_selection = {}  # Pour mémoriser quel match l'utilisateur a choisi

# Fonction hello() qui affiche dans le terminal et sur Telegram
def hello():
    print("Hello World")
    return "Hello World"

async def start(update, context):
    await update.message.reply_text("""
    - /match pour la liste des matches""")


async def match(update, context):
    keyboard = []
    for idx, m in enumerate(matches):
        match_button = InlineKeyboardButton(m['date_heure'], callback_data=f"match_{idx}")
        keyboard.append([match_button])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Sélectionne un match :", reply_markup=reply_markup)


# Gérer le choix d'un match
async def handle_match_choice(update, context):
    query = update.callback_query
    match_index = int(query.data.split('_')[1])  # Récupérer l'index du match
    user_selection[query.from_user.id] = match_index  # Mémoriser le match sélectionné

    # Afficher les nouvelles options après la sélection
    match = matches[match_index]
    keyboard = [
        [InlineKeyboardButton("Lancer Hello World", callback_data="hello")],
        [InlineKeyboardButton(f"Équipes : {match['equipe1']} vs {match['equipe2']}", callback_data="teams")],
        [InlineKeyboardButton("Voir la liste des matchs", callback_data="show_matches")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.answer()  # Répondre au callback
    await query.edit_message_text("Vous avez sélectionné un match. Que voulez-vous faire ?", reply_markup=reply_markup)

# Gérer l'action Hello World
async def handle_hello(update, context):
    hello_message = hello()  # Appeler la fonction hello()
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(f"Hello World: {hello_message}")

# Afficher les équipes
async def handle_teams(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    match_index = user_selection.get(user_id)
    if match_index is not None:
        match = matches[match_index]
        await query.edit_message_text(f"Les équipes sont :\n{match['equipe1']} vs {match['equipe2']}")
    else:
        await query.edit_message_text("Aucun match sélectionné.")

# Afficher la liste des matchs à nouveau
async def handle_show_matches(update, context):
    keyboard = []
    for idx, m in enumerate(matches):
        match_button = InlineKeyboardButton(m['date_heure'], callback_data=f"match_{idx}")
        keyboard.append([match_button])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("Sélectionne un match :", reply_markup=reply_markup)

if __name__ == '__main__':
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('match', match))

    # Ajout des handlers pour les actions
    app.add_handler(CallbackQueryHandler(handle_match_choice, pattern="^match_"))
    app.add_handler(CallbackQueryHandler(handle_hello, pattern="^hello$"))
    app.add_handler(CallbackQueryHandler(handle_teams, pattern="^teams$"))
    app.add_handler(CallbackQueryHandler(handle_show_matches, pattern="^show_matches$"))

    app.run_polling(poll_interval=5)
