import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

matches = []

# Ajout des matchs à la liste avec l'adresse
a = {
    'fonction': 'Fonction arbitre',
    'date_heure': 'Dimanche 23/02/2025\n11:30',
    'equipe1': 'NORT AC HANDBALL',
    'equipe2': 'HB STE LUCE SUR LOIRE 1',
    'arbitre': 'EVENO-GALLEN JULES',
    'fiche_de_frais': 'https://ihand-arbitrage.ffhandball.org/modules/compte/aff_pdf.php?DATE=20250223&IND=2034073&CODE=UAFXBLM&VERSION=',
    'convocation': 'https://ihand-arbitrage.ffhandball.org/file/convocation/2025-02-23_UAFXBLM_arb_convoc.pdf',
    'adresse': 'https://www.google.fr/maps/dir/47.72222,-1.38272/47.43486,-1.50642'
}
b = {
    'fonction': 'Fonction arbitre',
    'date_heure': 'Samedi 08/02/2025\n18:00',
    'equipe1': "UNION SPORTIVE GRANDE PRESQU'ILE HANDBALL",
    'equipe2': 'AL ST ETIENNE DE MONTLUC',
    'arbitre': 'EVENO-GALLEN JULES',
    'fiche_de_frais': 'https://media-ffhb-fdm.ffhandball.fr/fdm/U/A/F/W/UAFWHVM.pdf',
    'convocation': 'https://ihand-arbitrage.ffhandball.org/modules/compte/aff_pdf.php?DATE=20250208&IND=2034073&CODE=UAFWHVM&VERSION=',
    'adresse': 'https://ihand-arbitrage.ffhandball.org/index.php?file=compte&page=frais_new&id=2676842&juge1=2034073&etat=Juge'
}
c = {
    'fonction': 'Fonction arbitre',
    'date_heure': 'Samedi 01/02/2025\n19:00',
    'equipe1': 'ASSOCIATION HANDBALL VALLET',
    'equipe2': 'FANS HB LIGNE 2',
    'arbitre': 'EVENO-GALLEN JULES',
    'fiche_de_frais': 'https://media-ffhb-fdm.ffhandball.fr/fdm/U/A/F/V/UAFVGGR.pdf',
    'convocation': 'https://ihand-arbitrage.ffhandball.org/modules/compte/aff_pdf.php?DATE=20250201&IND=2034073&CODE=UAFVGGR&VERSION=',
    'adresse': 'https://ihand-arbitrage.ffhandball.org/index.php?file=compte&page=frais_new&id=2658205&juge1=2034073&etat=Juge'
}

matches.extend([a, b, c])

load_dotenv()
token = os.getenv("TOKEN")

user_selection = {}

async def start(update, context):
    await update.message.reply_text("👋 Bienvenue ! Tapez /match pour voir la liste des matchs. 🏐")

async def match(update, context):
    keyboard = [[InlineKeyboardButton(f"🗓 {m['date_heure']}", callback_data=f"match_{idx}")] for idx, m in enumerate(matches)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Sélectionne un match : 📅", reply_markup=reply_markup)

async def handle_match_choice(update, context):
    query = update.callback_query
    match_index = int(query.data.split('_')[1])
    user_selection[query.from_user.id] = match_index
    match = matches[match_index]

    keyboard = [
        [InlineKeyboardButton("ℹ️ Infos détaillées", callback_data="infos")],
        [InlineKeyboardButton("📜 Convocation", callback_data="convocation")],
        [InlineKeyboardButton("💼 Fiche de frais", callback_data="frais")],
        [InlineKeyboardButton("🔄 Voir la liste des matchs", callback_data="show_matches")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.answer()
    await query.edit_message_text(f"Vous avez sélectionné le match : {match['date_heure']}\nQue voulez-vous faire ?", reply_markup=reply_markup)

async def handle_details(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    match_index = user_selection.get(user_id)
    if match_index is not None:
        match = matches[match_index]
        details_text = f"📅 Match : {match['date_heure']}\n🏅 Équipe 1 : {match['equipe1']}\n🏅 Équipe 2 : {match['equipe2']}\n👨‍⚖️ Arbitre : {match['arbitre']}\n📍 Lieu : [Clique ici pour voir l'adresse]({match['adresse']})"
        keyboard = [
            [InlineKeyboardButton("🔄 Voir la liste des matchs", callback_data="show_matches")],
            [InlineKeyboardButton("⬅️ Retour", callback_data="back")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(details_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await query.edit_message_text("Aucun match sélectionné.")

async def handle_convocation(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    match_index = user_selection.get(user_id)
    if match_index is not None:
        match = matches[match_index]
        await query.edit_message_text(f"📜 Convocation : {match['convocation']}")
    else:
        await query.edit_message_text("Aucun match sélectionné.")

async def handle_frais(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    match_index = user_selection.get(user_id)
    if match_index is not None:
        match = matches[match_index]
        if match['fiche_de_frais']:
            await query.edit_message_text(f"💼 Fiche de frais : {match['fiche_de_frais']}")
        else:
            await query.edit_message_text("Aucune fiche de frais disponible.")
    else:
        await query.edit_message_text("Aucun match sélectionné.")

async def handle_show_matches(update, context):
    keyboard = [[InlineKeyboardButton(f"🗓 {m['date_heure']}", callback_data=f"match_{idx}")] for idx, m in enumerate(matches)]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("Sélectionne un match : 📅", reply_markup=reply_markup)

async def handle_back(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    match_index = user_selection.get(user_id)
    if match_index is not None:
        match = matches[match_index]
        keyboard = [
            [InlineKeyboardButton("ℹ️ Infos détaillées", callback_data="infos")],
            [InlineKeyboardButton("📜 Convocation", callback_data="convocation")],
            [InlineKeyboardButton("💼 Fiche de frais", callback_data="frais")],
            [InlineKeyboardButton("🔄 Voir la liste des matchs", callback_data="show_matches")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.answer()
        await query.edit_message_text(f"Vous avez sélectionné le match : {match['date_heure']}\nQue voulez-vous faire ?", reply_markup=reply_markup)
    else:
        await query.edit_message_text("Aucun match sélectionné.")

if __name__ == '__main__':
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('match', match))
    app.add_handler(CallbackQueryHandler(handle_match_choice, pattern="^match_"))
    app.add_handler(CallbackQueryHandler(handle_details, pattern="^infos"))
    app.add_handler(CallbackQueryHandler(handle_convocation, pattern="^convocation"))
    app.add_handler(CallbackQueryHandler(handle_frais, pattern="^frais"))
    app.add_handler(CallbackQueryHandler(handle_show_matches, pattern="^show_matches"))
    app.add_handler(CallbackQueryHandler(handle_back, pattern="^back"))

    app.run_polling(poll_interval=5)
