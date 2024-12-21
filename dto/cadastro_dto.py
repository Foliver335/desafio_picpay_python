class CadastroDTO:
    # Define a classe DTO (Data Transfer Object) para transferir dados entre camadas.
    
    def __init__(self,nickname: str, name: str, email: str, phone: str, birth_date: str, addresses: list):
        # Inicializa os atributos do DTO com os dados do cadastro.
        self.nickname = nickname
        self.name = name
        self.email = email
        self.phone = phone
        self.birth_date = birth_date
        self.addresses = addresses

    def to_dict(self):
        # Converte os dados do DTO para um dicionário, facilitando a serialização em JSON.
        return {
            'nickname': self.nickname,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'birth_date': self.birth_date,
            'addresses': self.addresses
        }