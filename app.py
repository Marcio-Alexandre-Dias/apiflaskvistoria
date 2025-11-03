from flask import Flask, jsonify, request, render_template
import os
import requests

app = Flask(__name__)

# =====================================================
# 🔹 Configurações do Supabase
# =====================================================
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nkqgetlubqewnxqyrhmw.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5rcWdldGx1YnFld254cXlyaG13Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NzE3NTYwNSwiZXhwIjoyMDYyNzUxNjA1fQ.4u3bRy79qQ77XhMiGw43hSc_2rZFkjXfNTl1RJo7KpI")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# =====================================================
# 🔹 Rota inicial (HTML opcional)
# =====================================================
@app.route('/')
def index():
    return jsonify({"status": "API Flask Vistoria rodando!"})

# =====================================================
# 🔹 Registra dados do serviço
# =====================================================
@app.route('/api/servicos', methods=['POST'])
def registrar_servico():
    dados = request.json or {}
    payload = {
        "placa": dados.get("placa"),
        "data": dados.get("data"),
        "hora": dados.get("hora"),
        "tipo": dados.get("tipo"),
        "responsavel": dados.get("responsaveis")
    }

    url = f"{SUPABASE_URL}/rest/v1/servicos_vistoria"
    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code in (200, 201):
        return jsonify({"message": "Registro salvo com sucesso!"})
    return jsonify({"error": "Erro ao registrar serviço", "detalhes": response.text}), 500

# =====================================================
# 🔹 Buscar veículos
# =====================================================
@app.route('/api/veiculos', methods=['GET'])
def get_veiculos():
    url = f"{SUPABASE_URL}/rest/v1/veiculos?select=*&order=placa.asc"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({"error": "Erro ao buscar veículos"}), 500

# =====================================================
# 🔹 Buscar profissionais
# =====================================================
@app.route('/api/profissionais', methods=['GET'])
def get_profissionais():
    url = f"{SUPABASE_URL}/rest/v1/profissionais?select=*"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({"error": "Erro ao buscar profissionais"}), 500

# =====================================================
# 🔹 Inicialização (modo local)
# =====================================================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8000)), debug=False)
