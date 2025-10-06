# In your new file: crud.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from passlib.context import CryptContext  # For secure password hashing

# Import your database models and the SessionLocal you created
from db_models import User, Deposit, Referral, Admin, Product

# --- Security Setup for Admin Passwords ---
# This is the modern, secure way to handle passwords, replacing MD5.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


# --- User Functions ---

def update_user_language(db: Session, telegram_id: int, new_lang_code: str) -> User | None:
    """Updates the language for a given user."""
    user = get_user_by_telegram_id(db, telegram_id)
    if user:
        user.language_code = new_lang_code
        db.commit()
        db.refresh(user)
        return user
    return None

def get_user_by_telegram_id(db: Session, telegram_id: int) -> User | None:
    """
    Replaces both userExists() and refExists().
    Returns the full User object if found, otherwise None.
    """
    return db.query(User).filter(User.telegram_id == telegram_id).first()

def create_user(db: Session, telegram_id: int, first_name: str, last_name: str, username: str) -> User:
    """Replaces registerUser(). Creates and returns a new User object."""
    new_user = User(
        telegram_id=telegram_id,
        first_name=first_name,
        last_name=last_name,
        username=username
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_all_users(db: Session) -> list[User]:
    """Replaces allUsers()."""
    return db.query(User).all()

def delete_user(db: Session, user_id: int) -> bool:
    """Replaces deleteUser(). Deletes a user by their primary key `id`."""
    user_to_delete = db.query(User).filter(User.id == user_id).first()
    if user_to_delete:
        db.delete(user_to_delete)
        db.commit()
        return True
    return False

# --- Referral Functions ---

def create_referral(db: Session, referrer_id: int, new_user_id: int) -> Referral:
    """Replaces createRef(). Note: Uses telegram_ids."""
    new_ref = Referral(
        user_id=referrer_id,
        referred_user_id=new_user_id,
        bonus=0  # Default bonus is 0 as in PHP
    )
    db.add(new_ref)
    db.commit()
    db.refresh(new_ref)
    return new_ref

def get_users_referred_by(db: Session, referrer_id: int) -> list[Referral]:
    """Replaces getReferrees(). Uses the SQLAlchemy relationship for a clean query."""
    return db.query(Referral).filter(Referral.user_id == referrer_id).all()

def count_referrals(db: Session, referrer_id: int, only_paid: bool = False) -> int:
    """
    Replaces both referralNo() and referralNoPaid().
    If only_paid is True, it only counts referrals with a bonus > 0.
    """
    query = db.query(Referral).filter(Referral.user_id == referrer_id)
    if only_paid:
        query = query.filter(Referral.bonus > 0)
    return query.count()

def get_referral_balance(db: Session, referrer_id: int) -> float:
    """Replaces refBalance()."""
    total = db.query(func.sum(Referral.bonus)).filter(Referral.user_id == referrer_id).scalar()
    return total or 0.0

# --- Deposit Functions ---

def create_deposit(db: Session, user_id: int, amount: float, doll_amount: float, coin: str, order_id: str) -> Deposit:
    """Replaces createdeposit()."""
    new_deposit = Deposit(
        user_id=user_id,
        amount=amount,
        doll_amount=doll_amount,
        coin=coin,
        time=order_id, # Assuming 'time' column in PHP was for an order ID
        state='pending'
    )
    db.add(new_deposit)
    db.commit()
    db.refresh(new_deposit)
    return new_deposit

def get_deposits_by_user(db: Session, user_id: int, state: str) -> list[Deposit]:
    """
    Replaces getDepositRequest(), getdepositpaid(), and getDepositConfirmed().
    Pass 'pending', 'paid', or 'approved' to the state parameter.
    """
    return db.query(Deposit).filter(Deposit.user_id == user_id, Deposit.state == state).all()

def get_all_deposits_by_state(db: Session, state: str) -> list:
    """
    Replaces pendingDeposit(), paidpendingDeposit(), and approvedDeposit().
    This function also joins with the User table to get user info.
    """
    return db.query(Deposit, User).join(User, Deposit.user_id == User.telegram_id).filter(Deposit.state == state).all()

def mark_deposit_paid(db: Session, order_id: str) -> Deposit | None:
    """
    Replaces markpaid(). Finds a deposit by the order_id and updates its state.
    """
    deposit_to_update = db.query(Deposit).filter(Deposit.time == order_id).first()
    if deposit_to_update:
        deposit_to_update.state = 'paid'
        db.commit()
        db.refresh(deposit_to_update)
        return deposit_to_update
    return None

def approve_deposit(db: Session, deposit_id: int, amount: float, doll_amount: float) -> Deposit | None:
    """Replaces approveDeposit()."""
    deposit_to_approve = db.query(Deposit).filter(Deposit.id == deposit_id).first()
    if deposit_to_approve:
        deposit_to_approve.state = 'approved'
        deposit_to_approve.amount = amount
        deposit_to_approve.doll_amount = doll_amount
        db.commit()
        db.refresh(deposit_to_approve)
        return deposit_to_approve
    return None

def delete_deposit(db: Session, deposit_id: int) -> bool:
    """Replaces deleteDeposit()."""
    deposit_to_delete = db.query(Deposit).filter(Deposit.id == deposit_id).first()
    if deposit_to_delete:
        db.delete(deposit_to_delete)
        db.commit()
        return True
    return False

# --- Admin Functions (SECURE VERSION) ---

def create_admin(db: Session, username: str, plain_password: str) -> Admin:
    """
    Replaces createadmin() with a SECURE implementation.
    NEVER store plain text passwords.
    """
    hashed_password = get_password_hash(plain_password)
    new_admin = Admin(username=username, password_hash=hashed_password)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

def authenticate_admin(db: Session, username: str, plain_password: str) -> Admin | None:
    """
    Replaces loginUser() with a SECURE implementation.
    """
    admin = db.query(Admin).filter(Admin.username == username).first()
    if admin and verify_password(plain_password, admin.password_hash):
        return admin
    return None

def get_all_admins(db: Session) -> list[Admin]:
    """Replaces allAdmins()."""
    return db.query(Admin).all()

# --- Product Functions ---
# (Assuming you have a Product model as defined previously)

def get_all_products(db: Session) -> list[Product]:
    """Replaces allproducts()."""
    return db.query(Product).all()

def create_product(db: Session, name: str, text: str, image: str, url: str) -> Product:
    """Replaces addProd()."""
    new_product = Product(name=name, text=text, image=image, url=url)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# ... you can add update and delete functions for products if needed ...