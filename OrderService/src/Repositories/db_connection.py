from abc import abstractmethod, ABC
from typing import List


class DbConnection(ABC):
    @abstractmethod
    def execute(self, sql) -> List:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass
