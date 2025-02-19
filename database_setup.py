from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the base class for our models
Base = declarative_base()

class Invoice(Base):
    __tablename__ = 'invoices'
    
    id = Column(Integer, primary_key=True)
    invoice_type = Column(String(100))
    client = Column(String(100))
    invoice_number = Column(String(50))
    invoice_date = Column(String(20))  # You can later convert to Date if needed
    due_date = Column(String(20))
    total_amount = Column(String(50))
    vat_number = Column(String(50))
    products = Column(Text)  # Storing as JSON string or comma-separated text

# Create the SQLite database (or switch to PostgreSQL URI if needed)
engine = create_engine('sqlite:///invoices.db')

# Create tables in the database
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    # Simple test to ensure the database and table are created
    session = Session()
    print("Database and invoices table created successfully!")
    session.close()
