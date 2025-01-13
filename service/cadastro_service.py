from abc import ABC, abstractmethod

class CadastroServiceInterface(ABC):
    @abstractmethod
    def create_cadastro(self, cadastro_dto):
        pass

    @abstractmethod
    def get_all_cadastros(self):
        pass

    @abstractmethod
    def update_cadastro(self, nickname, cadastro_dto):
        pass

    @abstractmethod
    def delete_cadastro(self, nickname):
        pass
