from sqlalchemy import (create_engine, Column, Integer, String, BigInteger, Text, 
                        Enum, Numeric, ForeignKey, DateTime)
from sqlalchemy.orm import declarative_base, relationship,sessionmaker
from sqlalchemy.sql import func

# --- Database Setup (SQLAlchemy) ---
DATABASE_URL = "mysql+mysqlconnector://globaltx_eatup:8WpdhKnWZTi7@localhost/globaltx_tstbot" # <-- IMPORTANT: FILL THIS IN
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# This Base is what all our models will inherit from
Base = declarative_base()

# --- Table Models ---

class User(Base):
    """
    Represents the 'users' table.
    This model has been updated to be more robust and includes the
    language_code field required by the bot.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    # Renamed from 'userid' for clarity and using BigInteger for safety
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True) 
    # Renamed from 'fname' to follow Python conventions
    first_name = Column(String(50), nullable=False)
    # Renamed from 'lname'
    last_name = Column(String(50), nullable=True)
    username = Column(String(50), nullable=True)
    # This field is ESSENTIAL for the language feature we built.
    language_code = Column(String(5), nullable=False, default='en')

    # This creates a link to the Deposit and Referral models for easy access
    deposits = relationship("Deposit", back_populates="user")
    referrals_made = relationship("Referral", back_populates="referrer_user", foreign_keys="[Referral.user_id]")


class Deposit(Base):
    """
    Represents the 'deposit' table.
    Data types for money and time have been corrected for accuracy.
    """
    __tablename__ = 'deposit'

    id = Column(Integer, primary_key=True)
    # IMPORTANT: This now links to a user's telegram_id
    user_id = Column(BigInteger, ForeignKey('users.telegram_id'), nullable=False, index=True)
    # IMPROVEMENT: Using Numeric for money is crucial to avoid floating point errors
    amount = Column(Numeric(18, 8), nullable=False) # Good for crypto (e.g., 18 total digits, 8 decimal places)
    doll_amount = Column(Numeric(10, 2), nullable=True) # Renamed from 'doll'
    coin = Column(String(50), nullable=False)
    # IMPROVEMENT: Using DateTime is much better than string for time
    time = Column(DateTime(timezone=True), server_default=func.now())
    state = Column(Enum('paid', 'false', 'pending', 'approved', name='deposit_state_enum'), nullable=False, default='pending')
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())

    # This creates a link back to the User model
    user = relationship("User", back_populates="deposits")


class Referral(Base):
    """Represents the 'referral' table."""
    __tablename__ = 'referral'

    id = Column(Integer, primary_key=True)
    # The user who did the referring
    user_id = Column(BigInteger, ForeignKey('users.telegram_id'), nullable=False)
    # The new user who was referred
    referred_user_id = Column(BigInteger, ForeignKey('users.telegram_id'), nullable=False)
    # IMPROVEMENT: Using Numeric for money
    bonus = Column(Numeric(18, 8), nullable=False)
    # IMPROVEMENT: Using DateTime for time
    time = Column(DateTime(timezone=True), server_default=func.now())

    # This defines the relationship back to the User who made the referral
    referrer_user = relationship("User", back_populates="referrals_made", foreign_keys=[user_id])


class Product(Base):
    """Represents the 'products' table."""
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    image = Column(Text, nullable=True)
    text = Column(Text, nullable=True)
    url = Column(String(256), nullable=True)


class Admin(Base):
    """
    Represents the 'admin' table.
    NOTE: Storing passwords in plain text is a major security risk.
    """
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    # WARNING: This should be a hashed password, not plain text.
    # The length should be increased to accommodate a hash (e.g., String(255))
    password_hash = Column(String(255), nullable=False) # Renamed from password/pwd

# Create the table in the database if it doesn't exist
# Base.metadata.create_all(bind=engine)