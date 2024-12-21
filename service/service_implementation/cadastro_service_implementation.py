from repository.cadastro_repository import CadastroRepository
from entity.cadastro_entity import Cadastro

class CadastroServiceImplementation:
    # Implementa os métodos definidos na interface CadastroService.
    def __init__(self):
        self.repository = CadastroRepository()  # Instancia o repositório.

    def create_cadastro(self, cadastro_dto):
        # Cria um novo cadastro a partir do DTO e salva no repositório.
        cadastro = Cadastro(
            nickname=cadastro_dto.nickname,
            name=cadastro_dto.name,
            email=cadastro_dto.email,
            phone=cadastro_dto.phone,
            birth_date=cadastro_dto.birth_date,
            addresses=cadastro_dto.addresses
        )
        self.repository.save(cadastro)

    def get_all_cadastros(self):
        # Retorna todos os cadastros armazenados no repositório.
        return self.repository.find_all()

    def update_cadastro(self, email, cadastro_dto):
        # Atualiza os dados de um cadastro existente com base no email.
        updated_cadastro = Cadastro(
            nickname=cadastro_dto.nickname,
            name=cadastro_dto.name,
            email=cadastro_dto.email,
            phone=cadastro_dto.phone,
            birth_date=cadastro_dto.birth_date,
            addresses=cadastro_dto.addresses
        )
        return self.repository.update(email, updated_cadastro)

    def delete_cadastro(self, email):
        # Remove um cadastro do repositório com base no email.
        # ( a escolha do e-mail foi pelo fato de que varias pessoas podem ter nomes iguais)
        return self.repository.delete(email)
