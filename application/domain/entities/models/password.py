# application\domain\entities\models\password.py

from pydantic import BaseModel

class PasswordRequest(BaseModel):
    base_string: str
    key_string: str
    password_length: int

class PasswordResponse(BaseModel):
    password: str