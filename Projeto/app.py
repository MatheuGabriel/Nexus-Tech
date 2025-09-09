from flask import Flask, request, jsonify, send_from_directory
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

EMAIL_VENDEDOR = "vendedor@example.com"
EMAIL_SAIDA = "sua_conta@gmail.com"
SENHA_EMAIL = "SUA_SENHA_AQUI"

# Servir o index.html
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Receber pedido
@app.route('/finalizar', methods=['POST'])
def finalizar():
    data = request.get_json()
    produtos = data.get('produtos')
    total = data.get('total')
    mensagem = "Novo pedido recebido:\n\n"
    for p in produtos:
        mensagem += f"- {p}\n"
    mensagem += f"\nTotal: R${total},00"

    # Enviar email
    try:
        msg = MIMEText(mensagem)
        msg['Subject'] = "Novo Pedido TechStore"
        msg['From'] = EMAIL_SAIDA
        msg['To'] = EMAIL_VENDEDOR

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_SAIDA, SENHA_EMAIL)
        server.send_message(msg)
        server.quit()
        return "Pedido enviado com sucesso!"
    except Exception as e:
        return f"Erro ao enviar pedido: {e}"

if __name__=="__main__":
    app.run(debug=True)