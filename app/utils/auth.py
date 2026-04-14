from fastapi import Depends
from fastapi import security
from fastapi.security import HTTPBasicCredentials
from services import verify_user


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    return verify_user(credentials.username, credentials.password)  