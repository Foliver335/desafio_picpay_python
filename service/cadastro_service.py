
from entity.cadastro_entity import Cadastro
from datetime import datetime
from repository.cadastro_repository import CadastroRepository
class CadastroService:
    def __init__(self, session):
        self.session = session

    def create_cadastro(self, cadastro_dto):
        try:
            birth_date_parsed = datetime.strptime(cadastro_dto.birth_date, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Data de nascimento inválida. Use o formato YYYY-MM-DD.")

        new_cadastro = Cadastro(
            nickname=cadastro_dto.nickname,
            name=cadastro_dto.name,
            email=cadastro_dto.email,
            phone=cadastro_dto.phone,
            birth_date=birth_date_parsed,
            street=cadastro_dto.street,
            number=cadastro_dto.number,
            zip_code=cadastro_dto.zip_code
        )
        
        call_repository = CadastroRepository.save(new_cadastro)


    def get_all_cadastros(self):
        return self.session.query(Cadastro).all()

    def update_cadastro(self, nickname, cadastro_dto):
        cadastro = self.session.query(Cadastro).filter_by(nickname=nickname).first()
        if not cadastro:
            raise ValueError("Cadastro não encontrado.")

        if cadastro_dto.name:
            cadastro.name = cadastro_dto.name
        if cadastro_dto.email:
            cadastro.email = cadastro_dto.email
        if cadastro_dto.phone:
            cadastro.phone = cadastro_dto.phone
        if cadastro_dto.birth_date:
            try:
                cadastro.birth_date = datetime.strptime(cadastro_dto.birth_date, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Data de nascimento inválida.")
        if cadastro_dto.street:
            cadastro.street = cadastro_dto.street
        if cadastro_dto.number:
            cadastro.number = cadastro_dto.number
        if cadastro_dto.zip_code:
            cadastro.zip_code = cadastro_dto.zip_code 

        self.session.commit()

    def delete_cadastro(self, nickname):
        cadastro = self.session.query(Cadastro).filter_by(nickname=nickname).first()
        if not cadastro:
            raise ValueError("Cadastro não encontrado.")

        self.session.delete(cadastro)
        self.session.commit()
        
        
