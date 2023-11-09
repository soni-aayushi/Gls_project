# from jwt import InvalidTokenError
from sqlalchemy import func
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi import FastAPI, Depends, HTTPException, status,Response,Cookie
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import secrets
import string
import smtplib
import uvicorn
from models import *
from schema import *
from database import *
from auth_bearer import *


Base.metadata.create_all(bind=engine)
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

app=FastAPI()

#PAssword patten
PASSWORD_PATTERN = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&*])[A-Za-z\d@#$%^&*]{8,}$"

#session timeout
SESSION_TIMEOUT_MINUTES = 30

#session management

# Function to generate a secure session token
def generate_session_token(length=32):
    characters = string.ascii_letters + string.digits
    session_token = ''.join(secrets.choice(characters) for i in range(length))
    return session_token

# Function to create a session cookie
def create_session_cookie(session_token: str, response: Response):
    response.set_cookie(key="session_token", value=session_token, httponly=True)

# Function to store session in the database
def store_session_to_db(session_token: str, user_id: int, db):
    session = Session(session_token=session_token, user_id=user_id)
    db.add(session)
    db.commit()

def get_current_user(session_token: str = Cookie(None)):
    return session_token

# Function to check if session is valid
def is_session_valid(session_token: str, db) -> bool:
    session = db.query(Session).filter_by(session_token=session_token).first()
    if session:
        now = datetime.utcnow()
        session_lifetime = timedelta(minutes=SESSION_TIMEOUT_MINUTES)
        return (now - session.creation_time) < session_lifetime
    return False




#User  registration
@app.post("/register")
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Validate the password
    if not re.match(PASSWORD_PATTERN, user.password):
        error_message = "Password must meet the following criteria:\n" \
                        "- At least one uppercase letter\n" \
                        "- At least one lowercase letter\n" \
                        "- At least one digit\n" \
                        "- At least one special character from @, #, $, %, ^, &, or *\n" \
                        "- The password must be at least 8 characters long"
        raise HTTPException(status_code=400, detail=error_message)

    encrypted_password = get_hashed_password(user.password)

    new_user = User(username=user.username, email=user.email, password=encrypted_password)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "User created successfully"}


#User Login
@app.post('/login', response_model=TokenSchema)
def login(request: requestdetails,response: Response, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")

    hashed_pass = user.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )

    if not re.match(PASSWORD_PATTERN, request.password):
        error_message = "Password must meet the following criteria:\n" \
                        "- At least one uppercase letter\n" \
                        "- At least one lowercase letter\n" \
                        "- At least one digit\n" \
                        "- At least one special character from @, #, $, %, ^, &, or *\n" \
                        "- The password must be at least 8 characters long"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)

    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    # Generate a session token
    session_token = generate_session_token()

    # Store the session to the database
    token_db = TokenTable(user_id=user.id, access_token=access, refresh_token=refresh, session_token=session_token, status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)

    # Set the session token as a cookie
    create_session_cookie(session_token, response)

    result = {"access_token": access, "refresh_token": refresh, "session_token": session_token, "message": "Login Successful"}
    return result

@app.get("/protected")
def protected_route( response: Response, current_user: str = Depends(get_current_user),db: Session = Depends(get_session)):
    if not is_session_valid(current_user, db):
        response.delete_cookie("session_token")
        raise HTTPException(status_code=401, detail="Session has expired")

    return {"message": "This is a protected route"}
    



#Change password
@app.post('/changepassword')
def change_password(request:changepassword, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    
    if not re.match(PASSWORD_PATTERN, request.password):
        error_message = "Password must meet the following criteria:\n" \
                        "- At least one uppercase letter\n" \
                        "- At least one lowercase letter\n" \
                        "- At least one digit\n" \
                        "- At least one special character from @, #, $, %, ^, &, or *\n" \
                        "- The password must be at least 8 characters long"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)
    
    if not verify_password(request.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")
    
    encrypted_password = get_hashed_password(request.new_password)
    user.password = encrypted_password
    db.commit()
    
    return {"message": "Password changed successfully"}



#forget password 
SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvb545435sha"
PASSWORD_RESET_SECRET_KEY = "1584ugfdfgh@#$%^@&jkl45678902"

def create_password_reset_token(email: str, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = {"email": email, "exp": datetime.utcnow() + expires_delta}
    encoded_token = jwt.encode(to_encode, PASSWORD_RESET_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_token

email_address = "aayushi.fichadiya@gmail.com" # type Email
email_password = "rpyq nluu bmfx aafk"

def send_reset_email(email, token):
    msg = MIMEMultipart()
    msg['From'] = email_address  # Replace with your Gmail email
    msg['To'] = email
    msg['Subject'] = "Password Reset"
    reset_url = f"http://127.0.0.0:8000/forgot-password?email=aayushi.fichadiya%40gmail.com"
    body = f"Click the following link to reset your password: {reset_url}"
    msg.attach(MIMEText(body, 'plain'))

    body = f"Password Reset Token: {token}"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_address, email_password)  # Replace with your Gmail email and password
    text = msg.as_string()
    server.sendmail(email_address, email, text)
    server.quit()
    print("Email sent successfully.")

#forgetpassword api
@app.post("/forgot-password")
async def forgot_password(email: str, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    password_reset_token = create_password_reset_token(email)
    send_reset_email(email, password_reset_token)

    return {"message": "Password reset email sent"}


# reset password 
@app.post("/reset-password")
async def reset_password(reset_data: ResetPassword, db: Session = Depends(get_session)):
    try:
        payload = jwt.decode(reset_data.token, PASSWORD_RESET_SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")

        # Verify that the email exists in your database
        user = db.query(User).filter(User.email == email).first()

        if user:
            # Check the token expiration
            if "exp" in payload and datetime.utcfromtimestamp(payload["exp"]) > datetime.utcnow():
                # Update the user's password
                hashed_password = get_hashed_password(reset_data.new_password)
                user.hashed_password = hashed_password
                db.commit()
                return {"message": "Password reset successfully"}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password reset token is invalid")



#Logout
@app.post('/logout')
def logout(dependencies=Depends(JWTBearer()), db: Session = Depends(get_session)):
    token=dependencies
    payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    user_id = payload['sub']
    token_record = db.query(TokenTable).all()
    info=[]
    for record in token_record :
        print("record",record)
        if (datetime.utcnow() - record.created_date).days >1:
            info.append(record.user_id)
    if info:
        existing_token = db.query(TokenTable).where(TokenTable.user_id.in_(info)).delete()
        db.commit()
        
    existing_token = db.query(TokenTable).filter(TokenTable.user_id == user_id, TokenTable.access_token==token).first()
    if existing_token:
        existing_token.status=False
        db.add(existing_token)
        db.commit()
        db.refresh(existing_token)
    return {"message":"Logout Successfully"} 








if __name__ == "__main__":
    uvicorn.run(app)