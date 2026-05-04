from main import SessionLocal, UserTable
from passlib.context import CryptContext

# Initializing Bcrypt context for secure password encryption
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def setup_admin():
    # Opening a database transaction session
    db = SessionLocal()
    
    # Target credentials for the administrative account
    username = "car"
    password = "car4321"
    
    # Checking if the user already exists in the 'users' table
    user = db.query(UserTable).filter(UserTable.username == username).first()
    
    if user:
        # Update existing user to Admin status (Authorization Level Up)
        user.is_admin = True
        print(f"User '{username}' found. Promoting to Admin...")
    else:
        # Create a new Admin user if not found in the database
        print(f"User '{username}' not found. Creating new Admin user...")
        
        # Hashing the password to prevent plain-text storage (Security Best Practice)
        hashed_pw = pwd_context.hash(password)
        
        # Mapping data to the UserTable model (ORM implementation)
        new_user = UserTable(
            username=username, 
            hashed_password=hashed_pw, 
            is_admin=True
        )
        db.add(new_user)
    
    # Committing the transaction to finalize database changes
    db.commit()
    print(f"✅ SUCCESS: '{username}' is now an Admin!")
    
    # Resource management: Closing the session after execution
    db.close()

if __name__ == "__main__":
    # Starting the admin setup process
    setup_admin()