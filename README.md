# TGbot-v2
A feature-rich, multilingual Telegram bot built with Python and SQLAlchemy. Manages user subscriptions, referrals, and dynamic language preferences through an interactive menu system.


# Multilingual Telegram Subscription Bot

A feature-rich, multilingual Telegram bot built with Python, SQLAlchemy, and the `python-telegram-bot` library. This bot provides an interactive inline menu for managing user subscriptions, referrals, and language preferences, with a clean and scalable architecture.

---

## ✨ Key Features

*   **🌐 Multilingual Support:** Automatically detects the user's language on first contact and allows users to switch between 10+ supported languages at any time.
*   **🤖 Interactive Menus:** All interactions are handled through clean, dynamic inline keyboard menus that edit messages in place for a smooth user experience.
*   **🐘 Robust Database Layer:** Uses SQLAlchemy ORM for all database operations, providing a secure and maintainable way to interact with a MySQL database.
*   **👤 User Onboarding & Management:** Automatically registers new users, saves their preferences, and provides a foundation for tracking subscriptions and referrals.
*   **📈 Referral System Ready:** Includes database models and logic placeholders for tracking user referrals, number of referees, and referral bonuses.
*   **🔩 Clean Architecture:** The project is organized into separate modules for bot logic (`bot.py`), database models (`database_models.py`), and CRUD operations (`botcontrol.py`), making it easy to extend.

---

## 🛠️ Technology Stack

*   **Backend:** Python 3.10+
*   **Telegram Bot Framework:** `python-telegram-bot`
*   **Database ORM:** SQLAlchemy
*   **Database:** MySQL / MariaDB
*   **Translation Service:** `deep-translator` (via Google Translate)

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine or server for development and testing purposes.

### Prerequisites

*   Python 3.10 or newer
*   A MySQL or MariaDB database
*   A Telegram Bot Token obtained from [@BotFather](https://t.me/BotFather)

### Installation & Setup

**1. Clone the Repository**
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
### 2. Create a Configuration File
The bot is configured using environment variables. Create a file named .env in the project root by copying the example file.

```bash
cp .env.example .env
```
###Now, edit the .env file with your credentials:**
TELEGRAM_BOT_TOKEN="7523138028:YOUR_REAL_TOKEN_HERE"
DATABASE_URL="mysql+mysqlconnector://user:password@host/db_name"

**3. Set Up the Python Environment**
It is highly recommended to use a virtual environment.

# Create the virtual environment
```python3 -m venv venv```

# Activate it
*  ##On Linux/macOS:
*  **```source venv/bin/activate```
*  ##On Windows:
*  **```.\venv\Scripts\activate```

# Install the required packages
*  ```pip install -r requirements.txt```

#4. Set Up the Database
*   Ensure your database is created and the credentials in your .env file are correct. Then, run the table creation script once.

```bash
python create_tables.py
```
This will create all the necessary tables (users, deposit, referral, etc.) in your database.

#Running the Bot

Once the setup is complete, you can start the bot.
```python bot.py```

You should see the message "Bot is running..." in your terminal. You can now interact with your bot on Telegram.

#Deploying to a Server
For 24/7 uptime, deploy the bot to your server and run it inside a screen session.
Follow the installation steps on your server.
Start a new screen session:

```bash
screen -S telegram-bot
```
#📂 Project Structure
.
*  ├── bot.py                  # Main bot logic, handlers, and UI
*  ├── botcontrol.py           # CRUD functions (Create, Read, Update, Delete)
*  ├── database_models.py      # SQLAlchemy database table models
*  ├── create_tables.py        # Script to initialize the database schema
*  ├── requirements.txt        # List of Python dependencies
*  ├── .env                    # Local configuration (Tokens, DB URL) - DO NOT COMMIT
*  └── .env.example            # Example configuration file

#🤖 Bot Usage
*  /start: Initializes the bot and shows the main menu.
*  /language: Allows the user to change their language preference.
*  Inline Menus: All other functionality is accessed through the interactive buttons.

#🤝 Contributing
*  Contributions are welcome! If you have suggestions for improvements or find a bug, please feel free to:
*  Fork the repository.
*  Create a new feature branch (git checkout -b feature/AmazingFeature).
*  Commit your changes (git commit -m 'Add some AmazingFeature').
*  Push to the branch (git push origin feature/AmazingFeature).
*  Open a Pull Request.

Final Step: You will need to slightly modify your bot.py and database_models.py to load the variables from the .env file instead of having them hardcoded.
*  Install the library:  ``` pip install python-dotenv```
*  Add it to your requirements.txt.
*  At the very top of bot.py and database_models.py, add:

```Python
import os
from dotenv import load_dotenv
```

load_dotenv() # This loads the variables from .env

# Then, access the variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
