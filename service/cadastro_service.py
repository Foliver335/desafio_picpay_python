
from entity.cadastro_entity import Cadastro
from datetime import datetime
from repository.cadastro_repository import CadastroRepository
from utils.cadastro_validations import CadastroValidations


class CadastroService:
    def __init__(self, session):
        self.session = session
        self.repository = CadastroRepository(session)

    def create_cadastro(self, cadastro_dto):
        # Validações
        CadastroValidations.validate_alphanumeric(cadastro_dto.nickname, "nickname")
        CadastroValidations.validate_letters_only(cadastro_dto.name, "name")
        CadastroValidations.validate_email(cadastro_dto.email)
        CadastroValidations.validate_numbers_only(cadastro_dto.phone, "phone")
        CadastroValidations.validate_date_format(cadastro_dto.birth_date)
        CadastroValidations.validate_alphanumeric(cadastro_dto.street, "street")
        CadastroValidations.validate_numbers_only(cadastro_dto.number, "number")
        CadastroValidations.validate_numbers_only(cadastro_dto.zip_code, "zip_code")
        
        birth_date_parsed = datetime.strptime(cadastro_dto.birth_date, '%Y-%m-%d').date()
        
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
        self.repository.save(new_cadastro)


    def get_all_cadastros(self):
        return self.session.query(Cadastro).all()

    def update_cadastro(self, nickname, cadastro_dto):
        cadastro = self.repository.find_by_nickname(nickname)
        if not cadastro:
            raise ValueError("Cadastro não encontrado.")

        fields_to_update = {
            "name": (CadastroValidations.validate_letters_only, cadastro_dto.name),
            "email": (CadastroValidations.validate_email, cadastro_dto.email),
            "phone": (CadastroValidations.validate_numbers_only, cadastro_dto.phone),
            "birth_date": (CadastroValidations.validate_date_format, cadastro_dto.birth_date),
            "street": (CadastroValidations.validate_alphanumeric, cadastro_dto.street),
            "number": (CadastroValidations.validate_numbers_only, cadastro_dto.number),
            "zip_code": (CadastroValidations.validate_numbers_only, cadastro_dto.zip_code),
        }

        for field, (validation_func, value) in fields_to_update.items():
            if value:  
                validation_func(value, field) 
                if field == "birth_date": 
                    setattr(cadastro, field, datetime.strptime(value, '%Y-%m-%d').date())
                else:
                    setattr(cadastro, field, value)  

        self.session.commit()
        
    def delete_cadastro(self, nickname):
        cadastro = self.session.query(Cadastro).filter_by(nickname=nickname).first()
        if not cadastro:
            raise ValueError("Cadastro não encontrado.")

        self.session.delete(cadastro)
        self.session.commit()
        
        
