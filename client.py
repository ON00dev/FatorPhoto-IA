import requests
import os

# URLs da API
BASE_URL = "http://127.0.0.1:5000"
LOGIN_ENDPOINT = f"{BASE_URL}/login"
ANALYZE_ENDPOINT = f"{BASE_URL}/analyze"
APPLY_ENDPOINT = f"{BASE_URL}/apply"

# Função para obter o token JWT
def get_token(username, password):
    response = requests.post(LOGIN_ENDPOINT, json={"username": username, "password": password})
    if response.status_code == 200:
        token = response.json().get("token")
        print(f"Token obtido: {token}")  # Exibe o token para validação
        return token
    else:
        print(f"Erro ao autenticar: {response.json()}")
        return None


def analyze_image(token, image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {image_path}")

    with open(image_path, 'rb') as image_file:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(ANALYZE_ENDPOINT, files={'image': image_file}, headers=headers)
        if response.status_code == 200:
            print("Parâmetros extraídos com sucesso:")
            print(response.json())
            return response.json()
        else:
            print(f"Erro ao analisar a imagem: {response.json()}")
            return None

def apply_filters(token, source_image_path, target_image_path):
    if not os.path.exists(source_image_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {source_image_path}")
    if not os.path.exists(target_image_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {target_image_path}")

    with open(source_image_path, 'rb') as source_file, open(target_image_path, 'rb') as target_file:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(APPLY_ENDPOINT, files={
            'source_image': source_file,
            'target_image': target_file
        }, headers=headers)
        if response.status_code == 200:
            print("Imagem ajustada com sucesso!")
            print(f"Saída: {response.json()['output_image']}")
            return response.json()['output_image']
        else:
            print(f"Erro ao aplicar filtros: {response.json()}")
            return None

# Teste
if __name__ == "__main__":
    source_image = r"C:/Users/Ronilda/Pictures/frente_loja.png"
    target_image = r"C:/Users/Ronilda/Downloads/paisa.png"

    try:
        # Obter o token de autenticação
        token = get_token("admin", "password")
        if not token:
            exit("Autenticação falhou. Verifique as credenciais.")

        # Analisar a imagem fonte
        analyze_result = analyze_image(token, source_image)

        # Aplicar os filtros na imagem alvo
        if analyze_result:
            output_image = apply_filters(token, source_image, target_image)

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
