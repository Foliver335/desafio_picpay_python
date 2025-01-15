from utils.common_imports import *  

app = Flask(__name__)

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    app.run(debug=True)