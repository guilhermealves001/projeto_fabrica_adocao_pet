# importamos as bibliotecas que iremos utilizar 
from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import json
import resend

# ADICIONAMOS a chave da api para recebimento de email
resend.api_key = 're_2BxPDqZr_3d49nR9wHQAcWqr3uaqZGYbY'

# instanciamos a aplicação web 
app= Flask(__name__)

# Comando para construir o banco de dados com as mensagens recebidas
with open('dados.json','r',encoding='utf-8') as arquivo:
    dados=json.load(arquivo)

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        nome= request.form['name']
        email=request.form['email']
        mensagem=request.form['message']

# montar o dicionário da nova mensagem
        dados_mensagem={
            'nome':nome,
            'email':email,
            'mensagem':mensagem,
            'data':f'{datetime.today()}'
        }

# adicionar e salvar no json

        dados.append(dados_mensagem)
        with open('dados.json','w',encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

# envia email usando resend 
            r = resend.Emails.send({
                "from": "onboarding@resend.dev",
                "to": "guigofort@gmail.com",
                "subject": f"Solicitação de adoção {nome}",
                "html": f"<p>Email:{email}<br>{mensagem}</p>"
                })
# após o post redireciona para o envio de formulário
        return redirect(url_for('index')) # esse é um endpoint de retorno 
    
## get - rendeneriza a página
    return render_template('index.html')

if __name__ =='__main__':
    app.run(debug=True)