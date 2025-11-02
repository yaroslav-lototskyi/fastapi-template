"""
Base Use Case (Clean Architecture).

Use Case = application-specific business rules.
Each use case does ONE thing (Single Responsibility Principle).

Use cases orchestrate the flow of data to and from entities,
and direct entities to use their business rules.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

# Generic types for Input and Output
InputDto = TypeVar("InputDto")
OutputDto = TypeVar("OutputDto")


class BaseUseCase(ABC, Generic[InputDto, OutputDto]):
    """
    Base use case interface.

    Example implementation:
    class CreateUserUseCase(BaseUseCase[CreateUserDto, UserResponseDto]):
        def __init__(self, user_repository: IUserRepository):
            self.user_repository = user_repository

        async def execute(self, input_dto: CreateUserDto) -> UserResponseDto:
            # Business logic here
            pass
    """

    @abstractmethod
    async def execute(self, input_dto: InputDto) -> OutputDto:
        """
        Execute the use case.

        Args:
            input_dto: Input data (DTO)

        Returns:
            Output data (DTO)
        """
        pass
