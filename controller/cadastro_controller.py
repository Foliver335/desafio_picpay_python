from flask import Flask, jsonify, request
from dto.cadastro_dto import CadastroDTO
from service.service_implementation.cadastro_service_implementation import CadastroServiceImplementation

app = Flask(__name__)  # Cria a aplicação Flask.
cadastro_service = CadastroServiceImplementation()  # Instancia o serviço de cadastro.

@app.route('/', methods=['GET'])
def home():
    # Define uma rota para a raiz do servidor.
    return jsonify({"message": "Bem-vindo à API de Cadastros"}), 200

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
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        birth_date=data['birth_date'],
        addresses=data['addresses']
    )
    cadastro_service.create_cadastro(cadastro_dto)
    return jsonify({"message": "Cadastro created successfully"}), 201

@app.route('/cadastros/<email>', methods=['PUT'])
def update_cadastro(email):
    # Atualiza um cadastro existente.
    data = request.json
    cadastro_dto = CadastroDTO(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        birth_date=data['birth_date'],
        addresses=data['addresses']
    )
    success = cadastro_service.update_cadastro(email, cadastro_dto)
    if success:
        return jsonify({"message": "Cadastro updated successfully"}), 200
    return jsonify({"message": "Cadastro not found"}), 404

@app.route('/cadastros/<email>', methods=['DELETE'])
def delete_cadastro(email):
    # Exclui um cadastro existente.
    success = cadastro_service.delete_cadastro(email)
    if success:
        return jsonify({"message": "Cadastro deleted successfully"}), 200
    return jsonify({"message": "Cadastro not found"}), 404


