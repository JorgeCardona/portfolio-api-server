# application/interfaces/services/password_service.py

from application.usecases.password_usecase import PasswordUseCase
from application.domain.entities.models.password import PasswordRequest, PasswordResponse

class PasswordService:
    def __init__(self):
        self.password_usecase = PasswordUseCase()

    def generate_password(self, request: PasswordRequest) -> PasswordResponse:
        """
        Generate a secure password by delegating to PasswordUseCase.

        Parameters:
        - request (PasswordRequest): Contains base_string, key_string, and password_length

        Returns:
        - PasswordResponse: The generated password
        """
        # Call the use case to generate password with proper arguments
        password = self.password_usecase.generate_password(
            request.base_string, request.key_string, request.password_length
        )
        return PasswordResponse(password=password)
