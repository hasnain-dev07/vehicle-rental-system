from sqlalchemy.orm import Session
from main import VehicleTable, SessionLocal, engine

def seed_data():
    db = SessionLocal()
    
    # Dataset of 30 vehicles
    pak_vehicles = [
        {"brand": "Suzuki", "model": "Alto VXR", "price_per_day": 3500},
        {"brand": "Suzuki", "model": "Cultus VXL", "price_per_day": 4500},
        {"brand": "Suzuki", "model": "Swift GLX", "price_per_day": 5500},
        {"brand": "Suzuki", "model": "Wagon R", "price_per_day": 4000},
        {"brand": "Suzuki", "model": "Mehran", "price_per_day": 2500},
        {"brand": "Toyota", "model": "Corolla GLI", "price_per_day": 6000},
        {"brand": "Toyota", "model": "Corolla Altis 1.6", "price_per_day": 8000},
        {"brand": "Toyota", "model": "Corolla Grande", "price_per_day": 10000},
        {"brand": "Toyota", "model": "Yaris ATIV X", "price_per_day": 7000},
        {"brand": "Toyota", "model": "Fortuner Legender", "price_per_day": 25000},
        {"brand": "Toyota", "model": "Hilux Revo", "price_per_day": 18000},
        {"brand": "Toyota", "model": "Prado TX", "price_per_day": 35000},
        {"brand": "Toyota", "model": "Vitz", "price_per_day": 5000},
        {"brand": "Toyota", "model": "Aqua", "price_per_day": 6000},
        {"brand": "Honda", "model": "Civic Oriel", "price_per_day": 10000},
        {"brand": "Honda", "model": "Civic RS Turbo", "price_per_day": 14000},
        {"brand": "Honda", "model": "City Aspire 1.5", "price_per_day": 7000},
        {"brand": "Honda", "model": "BR-V", "price_per_day": 9000},
        {"brand": "Honda", "model": "Vezel", "price_per_day": 8500},
        {"brand": "Kia", "model": "Sportage AWD", "price_per_day": 12000},
        {"brand": "Kia", "model": "Picanto", "price_per_day": 4000},
        {"brand": "Hyundai", "model": "Tucson", "price_per_day": 12000},
        {"brand": "Hyundai", "model": "Elantra", "price_per_day": 9000},
        {"brand": "Hyundai", "model": "Sonata", "price_per_day": 15000},
        {"brand": "MG", "model": "HS", "price_per_day": 12000},
        {"brand": "Changan", "model": "Alsvin Lumiere", "price_per_day": 6000},
        {"brand": "Changan", "model": "Oshan X7", "price_per_day": 14000},
        {"brand": "Haval", "model": "H6 HEV", "price_per_day": 16000},
        {"brand": "Daihatsu", "model": "Mira ES", "price_per_day": 4000},
        {"brand": "Nissan", "model": "Dayz", "price_per_day": 4500}
    ]

    # Prevent duplicate entries
    if db.query(VehicleTable).count() == 0:
        for car in pak_vehicles:
            db.add(VehicleTable(**car, is_available=True))
        db.commit()
        print("Success: 30 vehicles added to database.")
    else:
        print("Database already contains data.")
    
    db.close()

if __name__ == "__main__":
    seed_data()