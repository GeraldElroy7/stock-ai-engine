"""
JWT Authentication System
Simple but secure authentication for Stock AI Engine
Author: Stock AI Engine Team
Date: January 1, 2026
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Dict
from pydantic import BaseModel, EmailStr
import secrets

# Configuration
SECRET_KEY = secrets.token_urlsafe(32)  # Generate secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours
REFRESH_TOKEN_EXPIRE_DAYS = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security
security = HTTPBearer()

# ===== MODELS =====

class User(BaseModel):
    """User model"""
    user_id: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    is_premium: bool = False
    created_at: datetime = datetime.now()


class UserCreate(BaseModel):
    """User registration model"""
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """User login model"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Token response model"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES * 60


class TokenData(BaseModel):
    """Token payload data"""
    user_id: str
    email: str
    exp: datetime


# ===== IN-MEMORY USER STORAGE (Replace with database in production) =====

# Temporary storage - replace with database
USERS_DB: Dict[str, Dict] = {
    "demo@example.com": {
        "user_id": "demo_user_001",
        "email": "demo@example.com",
        "hashed_password": pwd_context.hash("demo123"),  # Password: demo123
        "full_name": "Demo User",
        "is_active": True,
        "is_premium": True,
        "created_at": datetime.now().isoformat()
    }
}

# Store active tokens (in production, use Redis)
ACTIVE_TOKENS: Dict[str, Dict] = {}


# ===== HELPER FUNCTIONS =====

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Dict:
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def authenticate_user(email: str, password: str) -> Optional[Dict]:
    """Authenticate user with email and password"""
    user = USERS_DB.get(email)
    
    if not user:
        return None
    
    if not verify_password(password, user["hashed_password"]):
        return None
    
    return user


def get_user_by_email(email: str) -> Optional[Dict]:
    """Get user by email"""
    return USERS_DB.get(email)


def create_user(user_data: UserCreate) -> Dict:
    """Create new user"""
    # Check if user already exists
    if user_data.email in USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user_id = f"user_{secrets.token_urlsafe(8)}"
    
    new_user = {
        "user_id": user_id,
        "email": user_data.email,
        "hashed_password": get_password_hash(user_data.password),
        "full_name": user_data.full_name,
        "is_active": True,
        "is_premium": False,
        "created_at": datetime.now().isoformat()
    }
    
    USERS_DB[user_data.email] = new_user
    
    return new_user


# ===== DEPENDENCY FUNCTIONS =====

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """
    Dependency to get current authenticated user
    Use this in protected routes: user: User = Depends(get_current_user)
    """
    token = credentials.credentials
    
    # Decode token
    payload = decode_token(token)
    
    # Validate token type
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user data
    email = payload.get("email")
    user_id = payload.get("user_id")
    
    if not email or not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    user_data = get_user_by_email(email)
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user_data.get("is_active", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Return User object
    return User(
        user_id=user_data["user_id"],
        email=user_data["email"],
        full_name=user_data.get("full_name"),
        is_active=user_data.get("is_active", True),
        is_premium=user_data.get("is_premium", False)
    )


async def get_current_premium_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to verify user has premium access
    Use this for premium-only routes: user: User = Depends(get_current_premium_user)
    """
    if not current_user.is_premium:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Premium subscription required for this feature"
        )
    
    return current_user


# ===== API ROUTES =====

def setup_auth_routes(app):
    """Setup authentication routes"""
    
    @app.post("/api/v2/auth/register", response_model=Token)
    async def register(user_data: UserCreate):
        """
        **Register New User** 📝
        
        Create new user account
        
        **Example Request:**
        ```json
        {
          "email": "user@example.com",
          "password": "securepassword123",
          "full_name": "John Doe"
        }
        ```
        
        **Returns:** Access token and refresh token
        """
        try:
            # Create user
            new_user = create_user(user_data)
            
            # Generate tokens
            token_data = {
                "user_id": new_user["user_id"],
                "email": new_user["email"]
            }
            
            access_token = create_access_token(token_data)
            refresh_token = create_refresh_token(token_data)
            
            # Store token
            ACTIVE_TOKENS[access_token] = {
                "user_id": new_user["user_id"],
                "created_at": datetime.now().isoformat()
            }
            
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Registration failed: {str(e)}"
            )
    
    
    @app.post("/api/v2/auth/login", response_model=Token)
    async def login(login_data: UserLogin):
        """
        **User Login** 🔐
        
        Authenticate user and get access token
        
        **Example Request:**
        ```json
        {
          "email": "demo@example.com",
          "password": "demo123"
        }
        ```
        
        **Default Demo Account:**
        - Email: demo@example.com
        - Password: demo123
        
        **Returns:** Access token and refresh token
        """
        # Authenticate user
        user = authenticate_user(login_data.email, login_data.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Generate tokens
        token_data = {
            "user_id": user["user_id"],
            "email": user["email"]
        }
        
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        
        # Store token
        ACTIVE_TOKENS[access_token] = {
            "user_id": user["user_id"],
            "created_at": datetime.now().isoformat()
        }
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    
    
    @app.get("/api/v2/auth/me")
    async def get_current_user_info(current_user: User = Depends(get_current_user)):
        """
        **Get Current User Info** 👤
        
        Get information about currently authenticated user
        
        **Requires:** Valid access token in Authorization header
        
        **Example:**
        ```
        GET /api/v2/auth/me
        Authorization: Bearer <your_access_token>
        ```
        
        **Returns:** User information
        """
        return {
            "user_id": current_user.user_id,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "is_active": current_user.is_active,
            "is_premium": current_user.is_premium,
            "subscription_tier": "premium" if current_user.is_premium else "free"
        }
    
    
    @app.post("/api/v2/auth/logout")
    async def logout(current_user: User = Depends(get_current_user), credentials: HTTPAuthorizationCredentials = Depends(security)):
        """
        **Logout** 🚪
        
        Invalidate current access token
        
        **Requires:** Valid access token
        """
        token = credentials.credentials
        
        # Remove token from active tokens
        if token in ACTIVE_TOKENS:
            del ACTIVE_TOKENS[token]
        
        return {
            "status": "success",
            "message": "Successfully logged out"
        }
    
    
    @app.post("/api/v2/auth/refresh", response_model=Token)
    async def refresh_token(refresh_token: str):
        """
        **Refresh Access Token** 🔄
        
        Get new access token using refresh token
        
        **Example Request:**
        ```json
        {
          "refresh_token": "<your_refresh_token>"
        }
        ```
        
        **Returns:** New access token
        """
        # Decode refresh token
        payload = decode_token(refresh_token)
        
        # Validate token type
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        # Create new access token
        token_data = {
            "user_id": payload.get("user_id"),
            "email": payload.get("email")
        }
        
        new_access_token = create_access_token(token_data)
        
        # Keep the same refresh token
        return {
            "access_token": new_access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    
    return app


if __name__ == "__main__":
    print("JWT Authentication System")
    print(f"Secret Key: {SECRET_KEY[:20]}...")
    print(f"Access Token Expiry: {ACCESS_TOKEN_EXPIRE_MINUTES} minutes")
    print(f"Refresh Token Expiry: {REFRESH_TOKEN_EXPIRE_DAYS} days")
    
    # Test password hashing
    password = "demo123"
    hashed = get_password_hash(password)
    print(f"\nTest Password: {password}")
    print(f"Hashed: {hashed[:50]}...")
    print(f"Verification: {verify_password(password, hashed)}")
