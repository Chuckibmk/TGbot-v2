# In your new create_tables.py file

from db_models import Base, engine

print("Connecting to the database and creating tables...")

# This command takes all the classes that inherit from Base and creates
# the corresponding tables in your database.
Base.metadata.create_all(bind=engine)

print("Tables created successfully (if they didn't already exist).")