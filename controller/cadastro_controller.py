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

        # Lista de erros
        errors = []

        # Validações de campos obrigatórios
        required_fields = [
            "nickname", "name", "email", "phone",
            "birth_date", "street", "number", "zip_code"
        ]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            errors.append(f"Os seguintes campos estão ausentes: {', '.join(missing_fields)}")

        # Validações específicas de cada campo
        if "nickname" in data:
            try:
                CadastroValidations.validate_alphanumeric(data['nickname'], "nickname")
            except ValueError as e:
                errors.append(str(e))

        if "name" in data:
            try:
                CadastroValidations.validate_letters_only(data['name'], "name")
            except ValueError as e:
                errors.append(str(e))

        if "email" in data:
            try:
                CadastroValidations.validate_email(data['email'])
            except ValueError as e:
                errors.append(str(e))

        if "phone" in data:
            try:
                CadastroValidations.validate_numbers_only(data['phone'], "phone")
            except ValueError as e:
                errors.append(str(e))

        if "birth_date" in data:
            try:
                CadastroValidations.validate_date_format(data['birth_date'], "birth_date")
            except ValueError as e:
                errors.append(str(e))

        if "street" in data:
            try:
                CadastroValidations.validate_alphanumeric(data['street'], "street")
            except ValueError as e:
                errors.append(str(e))

        if "number" in data:
            try:
                CadastroValidations.validate_numbers_only(data['number'], "number")
            except ValueError as e:
                errors.append(str(e))

        if "zip_code" in data:
            try:
                CadastroValidations.validate_numbers_only(data['zip_code'], "zip_code")
            except ValueError as e:
                errors.append(str(e))

        # Verificar se há erros
        if errors:
            return jsonify({"errors": errors}), 400

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

    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
