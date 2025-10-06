# TGbot-v2
A feature-rich, multilingual Telegram bot built with Python and SQLAlchemy. Manages user subscriptions, referrals, and dynamic language preferences through an interactive menu system.


# Multilingual Telegram Subscription Bot

A feature-rich, multilingual Telegram bot built with Python, SQLAlchemy, and the `python-telegram-bot` library. This bot provides an interactive inline menu for managing user subscriptions, referrals, and language preferences, with a clean and scalable architecture.

![Demo Screenshot](https_your_image_link_here.png) 
*(Suggestion: Add a screenshot of your bot in action here)*

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
