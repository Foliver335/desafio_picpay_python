from flask import Flask, jsonify, request
from dto.cadastro_dto import CadastroDTO
from service.cadastro_service import CadastroService
from config.database_config import session

app = Flask(__name__)
cadastro_service = CadastroService(session)

@app.route('/cadastros', methods=['GET'])
def list_cadastros():
    cadastros = cadastro_service.get_all_cadastros()
    return jsonify([cadastro.__dict__ for cadastro in cadastros]), 200

@app.route('/cadastros', methods=['POST'])
def create_cadastro():
    data = request.json
    cadastro_dto = CadastroDTO(
        nickname=data['nickname'],
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        birth_date=data['birth_date'],
        street=data['street'],
        number=data['number'],
        zip_code=data['zip_code']
    )
    cadastro_service.create_cadastro(cadastro_dto)
    return jsonify({"message": "Cadastro created successfully"}), 201

@app.route('/cadastros/<nickname>', methods=['PUT'])
def update_cadastro(nickname):
    data = request.json
    cadastro_dto = CadastroDTO(
        nickname=nickname,
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone'),
        birth_date=data.get('birth_date'),
        street=data.get('street'),
        number=data.get('number'),
        zip_code=data.get('zip_code')
    )
    cadastro_service.update_cadastro(nickname, cadastro_dto)
    return jsonify({"message": "Cadastro updated successfully"}), 200

@app.route('/cadastros/<nickname>', methods=['DELETE'])
def delete_cadastro(nickname):
    cadastro_service.delete_cadastro(nickname)
    return jsonify({"message": "Cadastro deleted successfully"}), 200
