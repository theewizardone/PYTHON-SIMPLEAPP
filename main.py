
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import requests

import models
from database import engine, get_db
from sms_service import send_sms  # Import the function from sms_service.py

# Load environment variables (for simplicity, hardcode here or use a dotenv package)
OIDC_ISSUER = "https://dev-3vov0ik1g70405bg.us.auth0.com/"
OIDC_JWKS_URL = "https://dev-3vov0ik1g70405bg.us.auth0.com/.well-known/jwks.json"

OIDC_AUDIENCE = "https://simpleapp.com"

# OAuth2 Authorization Code Flow for OpenID Connect
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{OIDC_ISSUER}/authorize",
    tokenUrl=f"{OIDC_ISSUER}/oauth/token",
)

# Fetch JWKS (JSON Web Key Set) for validating tokens
jwks = requests.get(OIDC_JWKS_URL).json()

def get_jwk_kid(token: str):
    """Get the 'kid' (Key ID) from the JWT header to find the matching JWK."""
    try:
        unverified_header = jwt.get_unverified_header(token)
        return unverified_header['kid']
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token header") from e

def verify_token(token: str):
    """Verify the JWT token using the OIDC provider's JWKS."""
    kid = get_jwk_kid(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == kid:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if not rsa_key:
        raise HTTPException(status_code=401, detail="Invalid token signature")

    try:
        payload = jwt.decode(token, rsa_key, algorithms=["RS256"], audience=OIDC_AUDIENCE, issuer=OIDC_ISSUER)
        return payload
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Token verification failed") from exc

# Initialize the FastAPI application
app = FastAPI()

# Pydantic models
class CustomerCreate(BaseModel):
    name: str
    code: str
    number: str

class CustomerResponse(BaseModel):
    id: int
    name: str
    code: str
    number: str

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    customer_id: int
    item: str
    amount: int

class OrderResponse(BaseModel):
    id: int
    customer_id: int
    item: str
    amount: int

    class Config:
        from_attributes = True

# CRUD operations for customers
@app.post("/customers/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # Verify token and ensure the user is authenticated
    verify_token(token)

    db_customer = models.Customer(name=customer.name, code=customer.code, number=customer.number)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    
    return db_customer

@app.get("/customers/", response_model=List[CustomerResponse])
def get_customers(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # Verify token
    verify_token(token)
    
    return db.query(models.Customer).all()

# CRUD operations for orders
@app.post("/orders/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # Verify token
    verify_token(token)

    # Check if customer exists
    customer = db.query(models.Customer).filter(models.Customer.id == order.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Create the order
    db_order = models.Order(customer_id=order.customer_id, item=order.item, amount=order.amount)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Send SMS to the customer who placed the order
    send_sms(f"New order placed for {order.item} with amount {order.amount}", [customer.number])
    
    return db_order

@app.get("/orders/", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # Verify token
    verify_token(token)
    
    return db.query(models.Order).all()
