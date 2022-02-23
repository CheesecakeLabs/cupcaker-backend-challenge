from abc import ABC, abstractmethod
from typing import Any


class BaseUseCase(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """Execute the use case"""
        pass
