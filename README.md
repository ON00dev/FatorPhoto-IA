# FatorPhoto-IA
Inteligência Artificial que permite ajustar uma imagem de referência para outra com base em parâmetros extraídos automaticamente.

```
FatorPhoto-IA
├─ app
│  ├─ api
│  │  └─ FatorPhoto-IA.json
│  └─ app.py
├─ client.py
├─ LICENSE
├─ README.md
└─ requirements.txt

```

## Endpoints da API

### 1. Login (/login)
- **Método**: POST
- **Corpo**:
  ```json
  {
    "username": "admin",
    "password": "password"
  }

- **Resposta**: JWT para autenticação.

### 2. Analisar Imagem (/analyze)
Método: POST
Cabeçalho: Authorization: Bearer <JWT_TOKEN>
Corpo: Arquivo de imagem (image).
Resposta: Parâmetros extraídos (brilho, contraste, saturação, etc.).

### 3. Aplicar Filtros (/apply)
Método: POST
Cabeçalho: Authorization: Bearer <JWT_TOKEN>
Corpo: Arquivos de imagem (source_image, target_image).
Resposta: Caminho da imagem ajustada.
Configuração

## 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

## 2. Rodar a API
```bash
python app/app.py
```

## 3. Testar com o Cliente
Edite e execute ```client.py``` para consumir a API.