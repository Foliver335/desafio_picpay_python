from utils.cadastro_validations import CadastroValidations

class CadastroDTO:
    def __init__(self, nickname, name, email, phone, birth_date, street, number, zip_code):
        CadastroValidations.validate_alphanumeric(nickname, "nickname")  
        CadastroValidations.validate_letters_only(name, "name")
        CadastroValidations.validate_email(email)
        CadastroValidations.validate_numbers_only(phone, "phone")
        CadastroValidations.validate_date_format(birth_date)
        CadastroValidations.validate_alphanumeric(street, "street")
        CadastroValidations.validate_numbers_only(number, "number")
        CadastroValidations.validate_numbers_only(zip_code, "zip_code")

        self.nickname = nickname
        self.name = name
        self.email = email
        self.phone = phone
        self.birth_date = birth_date
        self.street = street
        self.number = number
        self.zip_code = zip_code

    def to_dict(self):
        return {
            "nickname": self.nickname,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "birth_date": self.birth_date,
            "street": self.street,
            "number": self.number,
            "zip_code": self.zip_code
        }
