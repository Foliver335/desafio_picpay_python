from utils.common_imports import *  

app = Flask(__name__)
cadastro_service = CadastroService(session)


@app.route('/cadastros', methods=['GET'])
def list_cadastros():
   
    cadastros = cadastro_service.get_all_cadastros()
    return jsonify([cadastro.to_dict() for cadastro in cadastros]), 200

@app.route('/cadastros/<nickname>', methods=['GET'])
def get_cadastro_by_nickname(nickname):
    
    try:
        cadastro = cadastro_service.get_cadastro_by_nickname(nickname)
        if not cadastro:
            return jsonify({"error": "Cadastro não encontrado."}), 404
        return jsonify(cadastro.to_dict()), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cadastros', methods=['POST'])
def create_cadastro():
    try:
        data = request.json

        # AS validações ficam logo em seguida das requisições 
        CadastroValidations.validate_alphanumeric(data['nickname'], "nickname")
        CadastroValidations.validate_letters_only(data['name'], "name")
        CadastroValidations.validate_email(data['email'])
        CadastroValidations.validate_numbers_only(data['phone'], "phone")
        CadastroValidations.validate_date_format(data['birth_date'])
        CadastroValidations.validate_alphanumeric(data['street'], "street")
        CadastroValidations.validate_numbers_only(data['number'], "number")
        CadastroValidations.validate_numbers_only(data['zip_code'], "zip_code")

        # Criar DTO
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

        # Chamar o serviço para criar o cadastro
        cadastro_service.create_cadastro(cadastro_dto)
        return jsonify({"message": "Cadastro created successfully"}), 201
  
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    

@app.route('/cadastros/<nickname>', methods=['PATCH'])
def patch_cadastro(nickname):
    try:
        data = request.json

        validation_map = {
            "name": CadastroValidations.validate_letters_only,
            "email": CadastroValidations.validate_email,
            "phone": CadastroValidations.validate_numbers_only,
            "birth_date": CadastroValidations.validate_date_format,
            "street": CadastroValidations.validate_alphanumeric,
            "number": CadastroValidations.validate_numbers_only,
            "zip_code": CadastroValidations.validate_numbers_only
        }
        for field, value in data.items():
            if field in validation_map:
                validation_map[field](value, field)

        # Criar DTO
        cadastro_dto = CadastroDTO(
            nickname=nickname,
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            birth_date=data.get("birth_date"),
            street=data.get("street"),
            number=data.get("number"),
            zip_code=data.get("zip_code")
        )

        # Atualizar cadastro
        cadastro_service.update_cadastro(nickname, cadastro_dto)
        return jsonify({"message": "Cadastro updated successfully"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/cadastros/<nickname>', methods=['PUT'])
def update_cadastro(nickname):
    try:
        data = request.json

        CadastroValidations.validate_alphanumeric(nickname, "nickname")
        CadastroValidations.validate_letters_only(data['name'], "name")
        CadastroValidations.validate_email(data['email'])
        CadastroValidations.validate_numbers_only(data['phone'], "phone")
        CadastroValidations.validate_date_format(data['birth_date'])
        CadastroValidations.validate_alphanumeric(data['street'], "street")
        CadastroValidations.validate_numbers_only(data['number'], "number")
        CadastroValidations.validate_numbers_only(data['zip_code'], "zip_code")

        cadastro_dto = CadastroDTO(
            nickname=nickname,
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            birth_date=data['birth_date'],
            street=data['street'],
            number=data['number'],
            zip_code=data['zip_code']
        )

       
        cadastro_service.update_cadastro(nickname, cadastro_dto)
        return jsonify({"message": "Cadastro updated successfully"}), 200

    except KeyError as e:
        return jsonify({"error": f"Campo obrigatório ausente: {str(e)}"}), 400
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 409


@app.route('/cadastros/<nickname>', methods=['DELETE'])
def delete_cadastro(nickname):
    try:
        cadastro_service.delete_cadastro(nickname)
        return jsonify({"message": "Cadastro deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
