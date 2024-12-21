from flask import Flask, jsonify, request
from dto.cadastro_dto import CadastroDTO
from service.service_implementation.cadastro_service_implementation import CadastroServiceImplementation

app = Flask(__name__)  # Cria a aplicação Flask.
cadastro_service = CadastroServiceImplementation()  # Instancia o serviço de cadastro.

@app.route('/', methods=['GET'])
def home():
    # Define uma rota para a raiz do servidor.
    return jsonify({"message": """Bem-vindo à API de Cadastros
                    utilise as rotas de acesso selecionando os protocolos REST para a tarefa desejada:
                   
                    /cadastros/ para obter dados de usuarios
                    /cadastros/ para inserir dados
                    /cadastros/<nickname> para modificar dados
                    /cadastros/<nickname> para deletar dados 
                    
                    """}), 200

@app.route('/cadastros', methods=['GET'])
def list_cadastros():
    # Lista todos os cadastros.
    cadastros = cadastro_service.get_all_cadastros()
    # Transforma os objetos de cadastro em dicionários para retorno em JSON.
    cadastros_json = [
        {
            "name": cadastro.name,
            "email": cadastro.email,
            "phone": cadastro.phone,
            "birth_date": cadastro.birth_date,
            "addresses": [
                {
                    "street": address["street"],
                    "number": address["number"],
                    "zip_code": address["zip_code"]
                } for address in cadastro.addresses
            ]
        } for cadastro in cadastros
    ]
    return jsonify(cadastros_json), 200

@app.route('/cadastros', methods=['POST'])
def create_cadastro():
    # Cria um novo cadastro.
    data = request.json
    cadastro_dto = CadastroDTO(
        nickname=data['nickname'],
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        birth_date=data['birth_date'],
        addresses=data['addresses']
    )
    cadastro_service.create_cadastro(cadastro_dto)
    return jsonify({"message": "Cadastro created successfully"}), 201

@app.route('/cadastros/<nickname>', methods=['PUT'])
def update_cadastro(nickname):
    # Atualiza um cadastro existente.
    data = request.json
    cadastro_dto = CadastroDTO(
        nickname=data['nickname'],
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        birth_date=data['birth_date'],
        addresses=data['addresses']
    )
    success = cadastro_service.update_cadastro(nickname, cadastro_dto)
    if success:
        return jsonify({"message": "Cadastro updated successfully"}), 200
    return jsonify({"message": "Cadastro not found"}), 404

@app.route('/cadastros/<nickname>', methods=['DELETE'])
def delete_cadastro(nickname):
    # Exclui um cadastro existente.
    success = cadastro_service.delete_cadastro(nickname)
    if success:
        return jsonify({"message": "Cadastro deleted successfully"}), 200
    return jsonify({"message": "Cadastro not found"}), 404


