from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from .db.db import get_session, create_tables
from .db.models import UserLogin

from .auth.auth import Auth, get_current_user, add_user, get_current_user_from_token
from .schema import UserCred, LoginSuccess, SignUpSuccess, TokenSuccess
from .bloodReportUtils.crew import BloodReportCrew
from .bloodReportUtils.pdfutil import extract_text_pdf
from .utils import extract_name_from_email, send_email_to_user, remove_text_before_dear

app = FastAPI()
auth = Auth()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/shared", StaticFiles(directory="/shared"), name="shared")


@app.on_event("startup")
async def on_startup():
    await create_tables()


@app.post("/login", response_model=LoginSuccess)
async def login(user: UserCred, session: AsyncSession = Depends(get_session)):
    usercheck = await get_current_user(session, user.email)
    if usercheck is None or not auth.verify_password(
        user.password, usercheck.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = auth.create_token(user.email)
    return {"access_token": access_token, "token_type": "Bearer"}


@app.post("/signup", response_model=SignUpSuccess)
async def signup(user: UserCred, session: AsyncSession = Depends(get_session)):
    usercheck = await get_current_user(session, user.email)
    if usercheck:
        raise HTTPException(status_code=400, detail="User already exists")
    await add_user(session, user.email, user.password)
    return {"message": True}


@app.post("/upload", response_model=TokenSuccess)
async def tokencheck(
    file: UploadFile = File(...),
    user: UserLogin = Depends(get_current_user_from_token),
    session: AsyncSession = Depends(get_session),
):
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        email = user.email
        file_location = f"/shared/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())

        text = extract_text_pdf(file_location)
        br = BloodReportCrew()
        results = br.kickoff(text)
        results = str(results)

        name = extract_name_from_email(email)
        results = results.replace("[Patient's Name]", name)
        msg, subject = remove_text_before_dear(results)
        send_email_to_user(email, subject, msg)

        if results is None:
            raise ValueError("BloodReportCrew kickoff returned None")

        return {
            "message": "File uploaded and processed successfully!",
            "file_name": file.filename,
        }
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
