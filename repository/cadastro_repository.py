from sqlalchemy.exc import IntegrityError

class CadastroRepository:
    def __init__(self):
        self.cadastros = []  

    def save(self, cadastro):
        
        try:
            self.session.add(cadastro)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            
            raise ValueError("Cadastro com este nickname já existe.")
        self.cadastros.append(cadastro)

    def find_all(self):
        return self.cadastros

    def find_by_email(self, email):
        
        for cadastro in self.cadastros:
            if cadastro.email == email:
                return cadastro  
        return None  

    def update(self, email, updated_cadastro):
        for idx, cadastro in enumerate(self.cadastros):
            if cadastro.email == email:
                self.cadastros[idx] = updated_cadastro 
                return True  
        return False  
    def delete(self, email):
       
        for idx, cadastro in enumerate(self.cadastros):
            if cadastro.email == email:
                del self.cadastros[idx]  
                return True 
        return False  
    
    