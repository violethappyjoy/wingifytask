from pydantic import BaseModel, Field


class UserCred(BaseModel):
    """
    Request Body for User credentials for sign up and login
    """

    email: str = Field(..., example="example@email.com")
    password: str = Field(..., example="password")


class SignUpSuccess(BaseModel):
    """
    Response Body for a successful sign up and DB update
    Manually done here for testing purposes
    """

    message: bool


class LoginSuccess(BaseModel):
    """
    Response Body for a successful login
    Returns the JWT token and add the same to the header
    """

    access_token: str
    token_type: str


class TokenSuccess(BaseModel):
    """
    Response Body for a successful token verification
    """

    message: str
    file_name: str
