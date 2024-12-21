class Cadastro:
    # Define a classe Cadastro, que representa a entidade principal do sistema.
    def __init__(self,nickname: str, name: str, email: str, phone: str, birth_date: str, addresses: list):
        # Inicializa os atributos da entidade com os dados do cadastro.
        self.nickname = nickname # Apelido do usuário cadastrado.
        self.name = name  # Nome do usuário cadastrado.
        self.email = email  # Email do usuário cadastrado.
        self.phone = phone  # Telefone do usuário cadastrado.
        self.birth_date = birth_date  # Data de nascimento do usuário cadastrado.
        self.addresses = addresses  # Lista de endereços associados ao cadastro.