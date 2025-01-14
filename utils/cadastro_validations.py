import re
from datetime import datetime

class CadastroValidations:
    @staticmethod
    def validate_field(field, field_name):
        
        if field is None or str(field).strip() == "":
            raise ValueError(f"O campo '{field_name}' é obrigatório e não pode estar vazio ou em branco.")

    @staticmethod
    def validate_alphanumeric(field, field_name):
       
        CadastroValidations.validate_field(field, field_name)
        if not re.fullmatch(r'^[a-zA-Z0-9]+$', field):
            raise ValueError(f"O campo '{field_name}' deve conter apenas caracteres alfanuméricos (letras e números).")

    @staticmethod
    def validate_letters_only(field, field_name):
        
        CadastroValidations.validate_field(field, field_name)
        if not re.fullmatch(r'^[A-Za-zÀ-ÿ\s]+$', field):
            raise ValueError(f"O campo '{field_name}' deve conter apenas letras (sem números ou caracteres especiais).")

    @staticmethod
    def validate_email(field):
        
        CadastroValidations.validate_field(field, "email")
        if not re.fullmatch(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', field):
            raise ValueError("O campo 'email' deve ser um endereço de e-mail válido.")

    @staticmethod
    def validate_numbers_only(field, field_name):
        
        CadastroValidations.validate_field(field, field_name)
        if not re.fullmatch(r'^\d+$', field):
            raise ValueError(f"O campo '{field_name}' deve conter apenas números.")

    @staticmethod
    def validate_date_format(field):
       
        CadastroValidations.validate_field(field, "birth_date")
        try:
            datetime.strptime(field, '%Y-%m-%d')
        except ValueError:
            raise ValueError("O campo 'birth_date' deve estar no formato YYYY-MM-DD.")

    @staticmethod
    def validate_address(address):
       
        CadastroValidations.validate_alphanumeric(address.get("street"), "street")
        CadastroValidations.validate_numbers_only(address.get("number"), "number")
        CadastroValidations.validate_numbers_only(address.get("zip_code"), "zip_code")
