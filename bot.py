import logging
# --- Import your database models and session ---
from db_models import SessionLocal 
import botcontrol  # Import the entire crud.py file

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from deep_translator import GoogleTranslator


# Your Telegram Bot Token from BotFather
BOT_TOKEN = "7523138028:telegram_bot_token"

# --- Basic Setup ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

DEFAULT_LANGUAGE = 'en'  # Target language for translation (e.g., 'es' for Spanish)

# Whitelist of languages you support
LANGUAGES_CONFIG = {
    'en': {'name': 'English', 'emoji': '🇬🇧'},
    'es': {'name': 'Español', 'emoji': '🇪🇸'},
    'de': {'name': 'Deutsch', 'emoji': '🇩🇪'},
    'fr': {'name': 'Français', 'emoji': '🇫🇷'},
    'it': {'name': 'Italiano', 'emoji': '🇮🇹'},
    'pt': {'name': 'Português', 'emoji': '🇵🇹'},
    'ru': {'name': 'Русский', 'emoji': '🇷🇺'},
    'hi': {'name': 'हिन्दी', 'emoji': '🇮🇳'},
    'zh-cn': {'name': '中文 (简体)', 'emoji': '🇨🇳'},  # Google uses 'zh-cn' for Simplified Chinese
    'ar': {'name': 'العربية', 'emoji': '🇸🇦'}
}

# This list is now generated automatically from the config above.
# The auto-detection feature will use this.
SUPPORTED_LANGUAGES = list(LANGUAGES_CONFIG.keys())


def t(text: str, lang: str) -> str:
    """Translates text to the user's target language."""
    if lang == 'en' or not text:
        return text
    try:
         # This creates a new, properly configured translator for each call.
        # It's more reliable.
        return GoogleTranslator(source='auto', target=lang).translate(text)
    except Exception as e:
        logging.error(f"Translation failed for text '{text}' to lang '{lang}': {e}")
        return text # Return original text on failure
    
# --- Helper Function to Get/Create User ---
def get_user_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Gets user's language from context or DB, creates user if non-existent."""
    user_info = update.effective_user
    user_id = user_info.id
    
    # First, check if language is already cached in the context for this update
    if 'language_code' in context.user_data:
        return context.user_data['language_code']

    db = SessionLocal()
    user = botcontrol.get_user_by_telegram_id(db, telegram_id=user_id)
    if not user:
        # --- THIS IS THE NEW LOGIC FOR NEW USERS ---
        detected_lang_code = user_info.language_code
        
        # Check if the user's Telegram language is in our supported list
        default_user_lang = detected_lang_code if detected_lang_code in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE
        logging.info(f"Creating new user {user_id} with language '{default_user_lang}'.")
        
        # Use the CRUD function to create the user
        user = botcontrol.create_user(
            db=db,
            telegram_id=user_id,
            first_name=user_info.first_name,
            last_name=user_info.last_name,
            username=user_info.username
        )
        # Now update their language
        botcontrol.update_user_language(db, telegram_id=user_id, new_lang_code=default_user_lang)
        lang_code = default_user_lang
    else:
        lang_code = user.language_code
    
    db.close()
    # Cache the language code in context for this session
    context.user_data['language_code'] = lang_code
    return lang_code

# --- 1. CENTRALIZED ENGLISH TEXT STRINGS (Content) ---
# This makes it easy to manage all bot text in one place.

# -- General --
TEXT_MAIN_MENU = (
    "Overview of HobbieCode \n"
    "\n"
    "HobbieCode designs and offers algorithmic trading bots primarily for stock and cryptocurrency markets. \n"
    "These bots are based on automated strategies developed by their team and are available via subscription. \n"
    "\n"
    "Key features include: \n"
    "\n"
    "- Automated Execution: Bots execute trades based on pre-defined strategies without manual intervention. \n"
    "- Backtesting: Strategies are tested using historical data via MetaTrader's backtesting module to ensure reliability. \n"
    "- Cloud-Based Operation: Bots run on cloud servers, eliminating the need for users to keep their computers running. \n"
    "\n"
    "\n"
    "How the Bots Function\n"
    "\n"
    "- Bots are built on customized trading strategies tailored to different market conditions. \n"
    "I emphasize on strategies that align with a trader's risk tolerance and style. \n"
    "- Strategies are coded into the bots using languages like MQL (MetaQuotes Language) for MetaTrader platforms \n"
    "\n"
    "\n"
    "Technical Infrastructure \n"
    "\n"
    "- Platform Integration: Bots operate on platforms like, \n"
    "which connects to brokerage accounts for trade execution and decentralized wallets \n"
    "- Sensors & Data Analysis: While not detailed in the search results,  \n"
    "typical trading bots use real-time market data (e.g., price feeds, volume indicators) as 'sensors' to make decisions. \n"
    "- Risk Management: Includes stop-loss orders, position sizing, and leverage control to mitigate losses. \n"
    "\n"
    "\n"
    "Deployment and Monitoring \n"
    "\n"
    "-  Cloud Deployment: Bots are hosted on cloud servers for 24/7 operation and minimal latency. \n"
    "- User Control: Subscribers can monitor performance and adjust parameters via dashboards or APIs, \n"
    "though specifics are not elaborated in the search results. \n"
    "\n"
    "\n"
    "3. Educational Integration \n"
    "\n"
    "HobbieCode emphasizes education alongside bot subscriptions: \n"
    "- Courses and eBooks: They offer training on designing strategies, backtesting, and deploying bots \n"
    "(e.g., a free eBook on algorithmic trading tips)\n"
    "- Customization Guidance: Users learn to tweak bot parameters to align with their trading goals .\n"
    # "Hello! This is a Subscription Bot, and here you can manage your subscription to our indicator:\n"
    # "- Choose and purchase any type of subscription\n"
    # "- See Statistics of your referrals and withdrawal earnings"
)
BUTTON_MAIN_MENU = "⬅️ Main Menu"

# -- Signals Menu --
TEXT_SIGNALS_MENU = "Please choose the subscription you want to view."
BUTTON_ALL_SIGNALS = "All Signals"
BUTTON_ACCURACY_85 = "Accuracy above 85%"
BUTTON_ACCURACY_90 = "Accuracy above 90%"
TEXT_SUBSCRIPTION_UPDATED = "Successfully updated desired Subscription."

# -- Subscription & Payment --
TEXT_SUBSCRIPTION_MENU = (
    "After selecting the package and payment method, you will receive an invoice. 🧾\n"
    "Please carefully copy the payment address and the amount into a wallet or exchange!"
)
BUTTON_PLAN_1_MONTH = "0.025000000 BTC - 1 month"
BUTTON_PLAN_3_MONTHS = "0.050000000 BTC - 3 months"
BUTTON_PLAN_12_MONTHS = "0.100000000 BTC - 12 months"
TEXT_CHOOSE_CURRENCY = "Please choose currency:"
BUTTON_PAY_BTC = "Pay With BTC"
BUTTON_PAY_ETH = "Pay With ETH"
BUTTON_PAY_USDT = "Pay With USDT"
BUTTON_BACK = "⬅️ Back"
TEXT_PROCEED_PAYMENT = (
    "Please click the 'Proceed to payment' button below to complete payment.\n"
    "Once we receive payment you will be notified."
)
BUTTON_PROCEED_PAYMENT = "Proceed to Payment"

# -- Balance Menu --
TEXT_BALANCE_MENU = (
    "Subscription Days Left: {days} ⏱\n"
    "Your referral balance: {refbalance} 💼\n"
    "Bitcoin 💵 {btc_balance} BTC\n"
    "Ethereum 💵 {eth_balance} ETH\n"
    "Usdt | TRC 20 💵 {usdt_balance} USDT"
)
BUTTON_SUBSCRIPTION = "Subscription"
BUTTON_BALANCE = "My Balance"
BUTTON_REFERRAL = "My Referrals"

# -- Referrals Menu --
TEXT_REFERRALS_MENU = (
    "💼 Your referral balance is:\n\n"
    "💵 {ref_balance}\n"
    "All users: {all_users}\n"
    "- Active users: {active_users}"
)
BUTTON_REFERRAL_LINK = "Referral Link"
BUTTON_WITHDRAW = "Withdraw"
TEXT_REFERRAL_LINK_INTRO = "Here is your personal referral link:"
TEXT_WITHDRAW_MENU = (
    "💰 Your referral balance is:\n"
    "Bitcoin 💵 {btc_balance} BTC\n"
    "Ethereum 💵 {eth_balance} ETH\n"
    "Usdt | TRC 20 💵 {usdt_balance} USDT"
)
BUTTON_BITCOIN = "Bitcoin"
BUTTON_ETHEREUM = "Ethereum"
BUTTON_USDT_TRC20 = "Usdt | TRC20"
ALERT_NO_BTC = "Not Enough BTC on balance to Withdraw"
ALERT_NO_ETH = "Not Enough ETH on balance to Withdraw"
ALERT_NO_USDT = "Not Enough USDT(TRC20) on balance to Withdraw"

# -- Support --
BUTTON_SUPPORT = "Support"

#lang fxn
async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /language command."""
    await language_menu(update, context)
        
async def language_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shows the language selection menu, dynamically built in two columns."""
    lang = get_user_language(update, context)
    text = t("Please select your language:", lang)
    
    keyboard = []
    row = []
    # Iterate through the language config to build buttons
    for code, details in LANGUAGES_CONFIG.items():
        button = InlineKeyboardButton(
            f"{details['emoji']} {details['name']}",
            callback_data=f"set_lang_{code}"
        )
        row.append(button)
        
        # When two buttons are in a row, add it to the keyboard and start a new row
        if len(row) == 2:
            keyboard.append(row)
            row = []
    
    # If there's an odd number of languages, add the last button
    if row:
        keyboard.append(row)
        
    # Add the "Back" button at the very bottom
    keyboard.append([InlineKeyboardButton(t("⬅️ Back", lang), callback_data='mainme')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    # This logic remains the same
    query = update.callback_query
    if query:
        await query.edit_message_text(text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text, reply_markup=reply_markup)


# --- 2. BOT LOGIC (Handlers) ---

def get_main_menu(lang: str) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(t(BUTTON_ALL_SIGNALS,lang), callback_data='signa')],
        [InlineKeyboardButton(t(BUTTON_SUBSCRIPTION,lang), callback_data='subscr')],
        [InlineKeyboardButton(t(BUTTON_BALANCE,lang), callback_data='balan')], # Assuming 'My Balance' is a brand name
        [InlineKeyboardButton(t(BUTTON_REFERRAL,lang), callback_data='refer')],
        [InlineKeyboardButton("🌐 " + t("Language", lang), callback_data='language_menu')],
        [InlineKeyboardButton(t(BUTTON_SUPPORT,lang), url='https://t.me/DecryptDAO')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shows the main menu, editing the previous message."""
    lang = get_user_language(update, context)
    text = t(TEXT_MAIN_MENU, lang)
    reply_markup = get_main_menu(lang)
    query = update.callback_query
    if query:
        # If called from a button, edit the message
        await query.edit_message_text(text, reply_markup=reply_markup)
    else:
        # If called from a command like /start, send a new message
        await update.message.reply_text(text, reply_markup=reply_markup)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command by showing the main menu."""
    await show_main_menu(update, context)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles all button presses."""
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    lang = get_user_language(update, context)
    
    db = SessionLocal() # Open a database session for this interaction

    try:
        # Main Menu
        if data == 'mainme':
            await show_main_menu(update, context)
    
        #lang menu
        elif data == 'language_menu':
            await language_menu(update, context)
    
        elif data.startswith('set_lang_'):
            new_lang = data.split('_')[-1] # 'en' or 'es'

            # Use the new CRUD function to update the language
            botcontrol.update_user_language(db, telegram_id=user_id, new_lang_code=new_lang)
            context.user_data['language_code'] = new_lang # Update cache
    
            # Confirm the change to the user
            await query.answer(t("Language updated!", new_lang))
            # Show the main menu again, now in the new language
            await show_main_menu(update, context)
    
    
        # Signals Menu
        elif data == 'signa':
            keyboard = [
                [InlineKeyboardButton(t(BUTTON_ALL_SIGNALS,lang), callback_data='allsig')],
                [InlineKeyboardButton(t(BUTTON_ACCURACY_85,lang), callback_data='accu85')],
                [InlineKeyboardButton(t(BUTTON_ACCURACY_90,lang), callback_data='accu90')],
                [InlineKeyboardButton(t(BUTTON_MAIN_MENU,lang), callback_data='mainme')]
            ]
            await query.edit_message_text(text=t(TEXT_SIGNALS_MENU,lang), reply_markup=InlineKeyboardMarkup(keyboard))
        
        elif data in ['allsig', 'accu85', 'accu90']:
            keyboard = [[InlineKeyboardButton(t(BUTTON_MAIN_MENU,lang), callback_data='mainme')]]
            await query.edit_message_text(text=t(TEXT_SUBSCRIPTION_UPDATED,lang), reply_markup=InlineKeyboardMarkup(keyboard))
    
        # Subscription & Payment Flow
        elif data == 'subscr':
            keyboard = [
                [InlineKeyboardButton(t(BUTTON_PLAN_1_MONTH,lang), callback_data='1mont')],
                [InlineKeyboardButton(t(BUTTON_PLAN_3_MONTHS,lang), callback_data='2mont')],
                [InlineKeyboardButton(t(BUTTON_PLAN_12_MONTHS,lang), callback_data='3mont')],
                [InlineKeyboardButton(t(BUTTON_MAIN_MENU,lang), callback_data='mainme')]
            ]
            await query.edit_message_text(text=t(TEXT_SUBSCRIPTION_MENU,lang), reply_markup=InlineKeyboardMarkup(keyboard))
            
        elif data in ['1mont', '2mont', '3mont']:
            keyboard = [
                [InlineKeyboardButton(t(BUTTON_PAY_BTC,lang), callback_data='proced')],
                [InlineKeyboardButton(t(BUTTON_PAY_ETH,lang), callback_data='proced')],
                [InlineKeyboardButton(t(BUTTON_PAY_USDT,lang), callback_data='proced')],
                [InlineKeyboardButton(t(BUTTON_BACK,lang), callback_data='subscr')]
            ]
            await query.edit_message_text(text=t(TEXT_CHOOSE_CURRENCY,lang), reply_markup=InlineKeyboardMarkup(keyboard))
        
        elif data == 'proced':
            keyboard = [
                [InlineKeyboardButton(t(BUTTON_PROCEED_PAYMENT,lang), callback_data='payment_final_step')],
                [InlineKeyboardButton(t(BUTTON_MAIN_MENU,lang), callback_data='mainme')]
            ]
            await query.edit_message_text(text=t(TEXT_PROCEED_PAYMENT,lang), reply_markup=InlineKeyboardMarkup(keyboard))
    
        # Balance Menu
        elif data == 'balan':
            ref_balance = botcontrol.get_referral_balance(db, referrer_id=user_id)
            
            # --- DATABASE LOGIC will replace these placeholder values ---
            balance_text = TEXT_BALANCE_MENU.format(days=0, btc_balance="0.000000", eth_balance="0.000000", usdt_balance="0.000000",refbalance=ref_balance)
            keyboard = [
                [InlineKeyboardButton(t(BUTTON_SUBSCRIPTION,lang), callback_data='subscr')],
                [InlineKeyboardButton(t(BUTTON_MAIN_MENU,lang), callback_data='mainme')]
            ]
            await query.edit_message_text(text=t(balance_text,lang), reply_markup=InlineKeyboardMarkup(keyboard))
    
        # Referrals Menu
        elif data == 'refer':
            ref_balance = botcontrol.get_referral_balance(db, referrer_id=user_id)
            total_refs = botcontrol.count_referrals(db, referrer_id=user_id, only_paid=False)
            active_refs = botcontrol.count_referrals(db, referrer_id=user_id, only_paid=True)

            # --- DATABASE LOGIC will replace these placeholder values ---
            referral_text = TEXT_REFERRALS_MENU.format(refbalance=ref_balance, all_users=total_refs, active_users=active_refs)
            keyboard = [
                [InlineKeyboardButton(t(BUTTON_REFERRAL_LINK,lang), callback_data='referlink')],
                [InlineKeyboardButton(t(BUTTON_WITHDRAW,lang), callback_data='withref')],
                [InlineKeyboardButton(t(BUTTON_MAIN_MENU,lang), callback_data='mainme')]
            ]
            await query.edit_message_text(text=t(referral_text,lang), reply_markup=InlineKeyboardMarkup(keyboard))
            
        elif data == 'referlink':
            chat_id = query.from_user.id
            referral_link = f"https://t.me/{context.bot.username}?start={user_id}" # Replace with your bot's username
            text = f"{t(TEXT_REFERRAL_LINK_INTRO,lang)}\n{referral_link}"
            keyboard = [[InlineKeyboardButton(t(BUTTON_BACK,lang), callback_data='refer')]]
            await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))
            
        elif data == 'withref':
            # --- DATABASE LOGIC will replace these placeholder values ---
            withdraw_text = TEXT_WITHDRAW_MENU.format(btc_balance="0.000000", eth_balance="0.000000", usdt_balance="0.000000")
            keyboard = [
                [InlineKeyboardButton(t(BUTTON_BITCOIN,lang), callback_data='alert_btc')],
                [InlineKeyboardButton(t(BUTTON_ETHEREUM,lang), callback_data='alert_eth')],
                [InlineKeyboardButton(t(BUTTON_USDT_TRC20,lang), callback_data='alert_usdt')],
                [InlineKeyboardButton(t(BUTTON_BACK,lang), callback_data='refer')]
            ]
            await query.edit_message_text(text=t(withdraw_text,lang), reply_markup=InlineKeyboardMarkup(keyboard))
    
        # Handling the alerts
        elif data == 'alert_btc':
            await query.answer(t(ALERT_NO_BTC,lang), show_alert=True)
        elif data == 'alert_eth':
            await query.answer(t(ALERT_NO_ETH,lang), show_alert=True)
        elif data == 'alert_usdt':
            await query.answer(t(ALERT_NO_USDT,lang), show_alert=True)
    
    finally:
        db.close() # Ensure the database session is always closed
    

# --- Main Function to Run the Bot ---
def main() -> None:
    """Run the bot."""
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    #add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("language", language_command))

    #add the callback handler for all buttons
    application.add_handler(CallbackQueryHandler(button_handler))
    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()