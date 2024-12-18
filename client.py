import requests

# URLs da API
BASE_URL = "http://127.0.0.1:5000"
ANALYZE_ENDPOINT = f"{BASE_URL}/analyze"
APPLY_ENDPOINT = f"{BASE_URL}/apply"

def analyze_image(image_path):
    """
    Envia uma imagem para o endpoint /analyze e retorna os parâmetros de filtros extraídos.
    """
    with open(image_path, 'rb') as image_file:
        response = requests.post(ANALYZE_ENDPOINT, files={'image': image_file})
        if response.status_code == 200:
            print("Parâmetros extraídos com sucesso:")
            print(response.json())
            return response.json()
        else:
            print(f"Erro ao analisar a imagem: {response.json()}")
            return None

def apply_filters(source_image_path, target_image_path):
    """
    Envia uma imagem de referência e uma imagem alvo para o endpoint /apply.
    Retorna o caminho da imagem ajustada.
    """
    with open(source_image_path, 'rb') as source_file, open(target_image_path, 'rb') as target_file:
        response = requests.post(APPLY_ENDPOINT, files={
            'source_image': source_file,
            'target_image': target_file
        })
        if response.status_code == 200:
            print("Imagem ajustada com sucesso!")
            print(f"Saída: {response.json()['output_image']}")
            return response.json()['output_image']
        else:
            print(f"Erro ao aplicar filtros: {response.json()}")
            return None

# Teste
if __name__ == "__main__":
    # Caminhos das imagens
    source_image = "path/to/source_image.jpg"
    target_image = "path/to/target_image.jpg"

    # 1. Analisa a imagem fonte
    analyze_result = analyze_image(source_image)

    # 2. Aplica os filtros da imagem fonte na imagem alvo
    if analyze_result:
        output_image = apply_filters(source_image, target_image)
