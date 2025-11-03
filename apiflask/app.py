from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)

# =====================================================
# 🔹 Configurações do Supabase
# =====================================================
SUPABASE_URL = "https://nkqgetlubqewnxqyrhmw.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5rcWdldGx1YnFld254cXlyaG13Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NzE3NTYwNSwiZXhwIjoyMDYyNzUxNjA1fQ.4u3bRy79qQ77XhMiGw43hSc_2rZFkjXfNTl1RJo7KpI"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"  # retorna o registro inserido
}

# =====================================================
# 🔹 Rota inicial (carrega o index2.html)
# =====================================================
@app.route('/')
def index():
    return render_template('index.html')

# =====================================================
# 🔹 Registra dados do serviço
# =====================================================
@app.route('/api/servicos', methods=['POST'])
def registrar_servico():
    dados = request.json
    payload = {
        "placa": dados.get("placa"),
        "data": dados.get("data"),
        "hora": dados.get("hora"),
        "tipo": dados.get("tipo"),
        "responsavel": dados.get("responsaveis")  # se for array, deve corresponder ao tipo da coluna
    }

    url = f"{SUPABASE_URL}/rest/v1/servicos_vistoria"
    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code in [200, 201]:
        return jsonify({"message": "Registro salvo com sucesso!"})
    else:
        return jsonify({"error": "Erro ao registrar serviço", "detalhes": response.text}), 500

# =====================================================
# 🔹 Rota para buscar veículos
# =====================================================
@app.route('/api/veiculos', methods=['GET'])
def get_veiculos():
    url = f"{SUPABASE_URL}/rest/v1/veiculos?select=*&order=placa.asc" #ordena por placa.asc, id.desc eu escolho
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Erro ao buscar veículos"}), 500

# =====================================================
# 🔹 Rota para buscar profissionais
# =====================================================
@app.route('/api/profissionais', methods=['GET'])
def get_profissionais():
    url = f"{SUPABASE_URL}/rest/v1/profissionais?select=*"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Erro ao buscar profissionais"}), 500

# 🔹 Inicialização do servidor Flask
# =====================================================

if __name__ == '__main__':
    app.run(debug=True)
