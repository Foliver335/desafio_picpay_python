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

        # Campos obrigatórios e suas respectivas validações
        validation_map = {
            "nickname": CadastroValidations.validate_alphanumeric,
            "name": CadastroValidations.validate_letters_only,
            "email": CadastroValidations.validate_email,
            "phone": CadastroValidations.validate_numbers_only,
            "birth_date": CadastroValidations.validate_date_format,
            "street": CadastroValidations.validate_alphanumeric,
            "number": CadastroValidations.validate_numbers_only,
            "zip_code": CadastroValidations.validate_numbers_only
        }

        # Verificar campos obrigatórios ausentes
        missing_fields = [field for field in validation_map if field not in data]
        if missing_fields:
            errors.append(f"Os seguintes campos estão ausentes: {', '.join(missing_fields)}")

        # Validações dinâmicas para os campos presentes
        for field, validator in validation_map.items():
            if field in data:
                try:
                    validator(data[field], field)
                except ValueError as e:
                    errors.append(str(e))

        # Verificar se houve erros
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

        # Lista de erros
        errors = []

        # Validações dinâmicas usando validation_map
        validation_map = {
            "nickname": CadastroValidations.validate_alphanumeric,
            "name": CadastroValidations.validate_letters_only,
            "email": CadastroValidations.validate_email,
            "phone": CadastroValidations.validate_numbers_only,
            "birth_date": CadastroValidations.validate_date_format,
            "street": CadastroValidations.validate_alphanumeric,
            "number": CadastroValidations.validate_numbers_only,
            "zip_code": CadastroValidations.validate_numbers_only
        }

        for field, validator in validation_map.items():
            if field in data:
                try:
                    validator(data[field], field)
                except ValueError as e:
                    errors.append(str(e))

        # Verificar se houve erros
        if errors:
            return jsonify({"errors": errors}), 400

        # Criar DTO com os dados atualizados
        cadastro_dto = CadastroDTO(
            nickname=data.get('nickname', nickname),
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            birth_date=data.get('birth_date'),
            street=data.get('street'),
            number=data.get('number'),
            zip_code=data.get('zip_code')
        )

        # Atualizar o cadastro
        cadastro_service.update_cadastro(nickname, cadastro_dto)
        return jsonify({"message": "Cadastro updated successfully"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@app.route('/cadastros/<nickname>', methods=['PATCH'])
def patch_cadastro(nickname):
    try:
        data = request.json
        errors = []

        # Validações de campos recebidos
        validation_map = {
            "nickname": CadastroValidations.validate_alphanumeric,
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
                try:
                    validation_map[field](value, field)
                except ValueError as e:
                    errors.append(str(e))

        if errors:
            return jsonify({"errors": errors}), 400

        # Atualizar o cadastro
        updated_nickname = data.get("nickname", nickname)
        cadastro_dto = CadastroDTO(
            nickname=updated_nickname,
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            birth_date=data.get("birth_date"),
            street=data.get("street"),
            number=data.get("number"),
            zip_code=data.get("zip_code")
        )

        # Chamar o service para atualizar o cadastro
        cadastro_service.update_cadastro(nickname, cadastro_dto)
        return jsonify({"message": "Cadastro updated successfully"}), 200

    except ValueError as e:
        # Retorna erros do service, incluindo nickname já em uso
        return jsonify({"error": str(e)}), 409

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/cadastros/<nickname>', methods=['DELETE'])
def delete_cadastro(nickname):
    try:
        cadastro_service.delete_cadastro(nickname)
        return jsonify({"message": "Cadastro deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
