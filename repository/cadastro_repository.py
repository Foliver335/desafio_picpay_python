class CadastroRepository:
    # Define o repositório para gerenciar operações de persistência dos dados.
    def __init__(self):
        self.cadastros = []  # Lista que simula um banco de dados em memória.

    def save(self, cadastro):
        # Salva um novo cadastro no repositório.
        self.cadastros.append(cadastro)

    def find_all(self):
        # Retorna todos os cadastros armazenados no repositório.
        return self.cadastros

    def find_by_email(self, email):
        # Busca um cadastro no repositório pelo email.
        for cadastro in self.cadastros:
            if cadastro.email == email:
                return cadastro  # Retorna o cadastro encontrado.
        return None  # Retorna None se o cadastro não for encontrado.

    def update(self, email, updated_cadastro):
        # Atualiza um cadastro existente no repositório com base no email.
        for idx, cadastro in enumerate(self.cadastros):
            if cadastro.email == email:
                self.cadastros[idx] = updated_cadastro  # Substitui pelo novo cadastro.
                return True  # Indica sucesso na atualização.
        return False  # Retorna False se o cadastro não for encontrado.

    def delete(self, email):
        # Remove um cadastro do repositório com base no email.
        for idx, cadastro in enumerate(self.cadastros):
            if cadastro.email == email:
                del self.cadastros[idx]  # Remove o cadastro da lista.
                return True  # Indica sucesso na remoção.
        return False  # Retorna False se o cadastro não for encontrado.