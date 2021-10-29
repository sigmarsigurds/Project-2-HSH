from typing import List
from abc import abstractmethod, ABC


class DbConnection(ABC):
    @abstractmethod
    def execute(self, sql) -> List:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass
