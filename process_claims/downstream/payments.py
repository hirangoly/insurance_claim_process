from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Initialize FastAPI app
app = FastAPI()

# Set up SQLite database
DATABASE_URL = "sqlite:///./providers.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the Provider model (SQLAlchemy)
class Provider(Base):
    __tablename__ = "providers"
    id = Column(Integer, primary_key=True, index=True)
    provider_npi = Column(Integer, index=True)
    net_fee = Column(Float)

# Pydantic model for incoming provider data
class ProviderData(BaseModel):
    provider_npi: int
    net_fee: float

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to return all provider NPIs and net fees from SQLite
@app.get("/api/providers")
async def get_providers():
    db = next(get_db())
    providers = db.query(Provider.provider_npi, Provider.net_fee).all()
    
    if not providers:
        raise HTTPException(status_code=404, detail="No provider data available")

    # Convert the list of tuples to a list of dictionaries
    providers_list = [{"provider_npi": provider_npi, "net_fee": net_fee} for provider_npi, net_fee in providers]

    
    return {"providers": providers_list}

# Endpoint to receive payment data from the upstream service
@app.post("/api/payments")
async def receive_payments(data: List[ProviderData]):
    here = 'here'
    db = next(get_db())
    for entry in data:
        there = 'there'
        provider = Provider(provider_npi=entry.provider_npi, net_fee=entry.net_fee)
        db.add(provider)
    db.commit()

    return {"message": "Payments data received successfully!"}

# Endpoint to return the top 10 providers based on total net_fee
@app.get("/api/top_providers")
async def get_top_providers():
    db = next(get_db())
    top_providers = (
        db.query(Provider.provider_npi, Provider.net_fee)
        .order_by(Provider.net_fee.desc())
        .limit(10)
        .all()
    )
    if not top_providers:
        raise HTTPException(status_code=404, detail="No providers found")

    # Convert the list of tuples to a list of dictionaries
    top_providers_list = [{"provider_npi": provider_npi, "net_fee": net_fee} for provider_npi, net_fee in top_providers]

    return {"top_10_providers": top_providers_list}

# On startup event to create tables in SQLite if they don't exist
@app.on_event("startup")
def startup_event():
    print("Creating the database tables...")
    Base.metadata.create_all(bind=engine)  # Ensure tables are created on startup
    print("Database tables created.")

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
