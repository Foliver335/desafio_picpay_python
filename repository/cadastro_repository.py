from sqlalchemy.exc import IntegrityError
from entity.cadastro_entity import Cadastro

class CadastroRepository:
    def __init__(self, session):
        self.session = session

    def save(self, cadastro):
       
        try:
            self.session.add(cadastro)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise ValueError("Cadastro com este nickname já existe.")

    def find_all(self):
        
        return self.session.query(Cadastro).all()

    def find_by_nickname(self, nickname):
        
        return self.session.query(Cadastro).filter_by(nickname=nickname).first()

    def update(self, nickname, updated_cadastro):
        
        cadastro = self.find_by_nickname(nickname)
        if not cadastro:
            raise ValueError("Cadastro não encontrado.")
        
        for attr, value in updated_cadastro.items():
            setattr(cadastro, attr, value)

        self.session.commit()

    def delete(self, nickname):
        
        cadastro = self.find_by_nickname(nickname)
        if not cadastro:
            raise ValueError("Cadastro não encontrado.")

        self.session.delete(cadastro)
        self.session.commit()
