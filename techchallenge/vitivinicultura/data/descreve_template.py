import os
import json

def describe_template(json_object):
    """
    Função que descreve o template (estrutura) de um JSON.
    """
    def describe_value(value):
        """
        Retorna o tipo do valor em formato legível.
        """
        if isinstance(value, dict):
            return {k: describe_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            if len(value) > 0:
                return [describe_value(value[0])]
            else:
                return ["empty list"]
        else:
            return type(value).__name__

    return describe_value(json_object)

def process_json_file(file_path):
    """
    Função que processa um único arquivo JSON e descreve seu template.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            json_data = json.load(f)
            return describe_template(json_data)
        except json.JSONDecodeError:
            print(f"Erro ao processar o arquivo {file_path}. Não é um JSON válido.")
            return None

def main():
    # Diretório onde os arquivos JSON estão localizados
    directory = "./"

    # Lista de arquivos JSON que você mencionou
    json_files = [
        "comercio_sanitizado.json",
        "exportacao_sanitizado.json",
        "importacao_sanitizado.json",
        "processamento_sanitizado.json",
        "producao_sanitizado.json"
    ]

    # Processa cada arquivo JSON e imprime seu template
    for json_file in json_files:
        file_path = os.path.join(directory, json_file)
        if os.path.exists(file_path):
            print(f"\nTemplate do arquivo: {json_file}")
            template = process_json_file(file_path)
            if template:
                print(json.dumps(template, indent=4))
        else:
            print(f"Arquivo {json_file} não encontrado no diretório {directory}.")

if __name__ == "__main__":
    main()
