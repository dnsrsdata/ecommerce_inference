import joblib
import os.path
import sqlite3
import numpy as np
import pandas as pd
from flask import request, jsonify, render_template, Flask

# Criando o app Flask
app = Flask(__name__)

# Definindo as rotas para os arquivos HTML
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analise')
def analise():
    return render_template('analise.html')

@app.route('/predicoes')
def predicoes():
    return render_template('predicoes.html')

# Definindo as rotas para as APIs

# Buscando as cidades com base na uf selecionada
@app.route('/cidades', methods=['GET'])
def cidades():
    uf = request.args.get('uf')
    path_db = os.path.join(os.path.dirname(__file__), 'dados_to_web.db')
    with sqlite3.connect(path_db) as conn:
        cur = conn.cursor()
        cur.execute("select municipio_campus from dados_to_predict where uf_campus = ? group by municipio_campus having count(municipio_campus) >= 1", (uf,))
        cidades_uf = cur.fetchall()
    return jsonify(cidades_uf)

# Definindo as APIs para seleção
# Buscando as instituições com base na uf e cidade selecionada
@app.route('/instituicoes', methods=['GET'])
def instituicoes():
    uf = request.args.get('uf')
    cidade = request.args.get('cidade')
    path_db = os.path.join(os.path.dirname(__file__), 'dados_to_web.db')
    with sqlite3.connect(path_db) as conn:
        cur = conn.cursor()
        cur.execute("select ies from dados_to_predict where uf_campus = ? and municipio_campus = ? group by ies having count(ies) >= 1", (uf, cidade,))
        instituicoes_uf = cur.fetchall()
    return jsonify(instituicoes_uf)

# Buscando os cursos com base na uf, cidade e instituição selecionada
@app.route('/cursos', methods=['GET'])
def cursos():
    uf = request.args.get('uf')
    cidade = request.args.get('cidade')
    instituicao = request.args.get('instituicao')
    path_db = os.path.join(os.path.dirname(__file__), 'dados_to_web.db')
    with sqlite3.connect(path_db) as conn:
        cur = conn.cursor()
        cur.execute("select nome_curso from dados_to_predict where uf_campus = ? and municipio_campus = ? and ies = ? group by nome_curso having count(nome_curso) >= 1", (uf, cidade, instituicao,))
        cursos_uf = cur.fetchall()
    return jsonify(cursos_uf)

# Buscando os graus com base na uf, cidade, instituição e curso selecionado
@app.route('/graus', methods=['GET'])
def graus():
    uf = request.args.get('uf')
    cidade = request.args.get('cidade')
    instituicao = request.args.get('instituicao')
    curso = request.args.get('curso')
    path_db = os.path.join(os.path.dirname(__file__), 'dados_to_web.db')
    with sqlite3.connect(path_db) as conn:
        cur = conn.cursor()
        cur.execute("select grau from dados_to_predict where uf_campus = ? and municipio_campus = ? and ies = ? and trim(nome_curso) = ? group by grau having count(grau) >= 1", (uf, cidade, instituicao, curso,))
        graus_uf = cur.fetchall()
    return jsonify(graus_uf)

# Buscando os tunos disponíveis com base na uf, cidade, instituição, curso e grau selecionado
@app.route('/turnos', methods=['GET'])
def turnos():
    uf = request.args.get('uf')
    cidade = request.args.get('cidade')
    instituicao = request.args.get('instituicao')
    curso = request.args.get('curso')
    grau = request.args.get('grau')
    path_db = os.path.join(os.path.dirname(__file__), 'dados_to_web.db')
    with sqlite3.connect(path_db) as conn:
        cur = conn.cursor()
        cur.execute("select turno from dados_to_predict where uf_campus = ? and municipio_campus = ? and ies = ? and nome_curso = ? and grau = ? group by turno having count(turno) >= 1", (uf, cidade, instituicao, curso, grau,))
        turnos_uf = cur.fetchall()
    return jsonify(turnos_uf)

# Contruindo a API para predição
# Construindo o predict
@app.route('/predict', methods=['GET'])
def predict():
    
    # Recebendo os dados do formulário
    uf = request.args.get('uf')
    cidade = request.args.get('cidade')
    instituicao = request.args.get('instituicao')
    curso = request.args.get('curso')
    grau = request.args.get('grau')
    turno = request.args.get('turno')
    modalidade = request.args.get('modalidade')
    opcao = request.args.get('opcao')
    nota_r = request.args.get('nota_redacao')
    nota_m = request.args.get('nota_matematica')
    nota_cn = request.args.get('nota_cn')
    nota_ch = request.args.get('nota_ch')
    nota_l = request.args.get('nota_linguagens')
    
    # Buscando os dados no banco de dados
    path_db = os.path.join(os.path.dirname(__file__), 'dados_to_web.db')
    with sqlite3.connect(path_db) as conn:
        cur = conn.cursor()
        cur.execute("select * from dados_to_predict where uf_campus = ? and municipio_campus = ? and ies = ? and nome_curso = ? and grau = ? and turno = ? group by turno having count(turno) >= 1", (uf, cidade, instituicao, curso, grau, turno,))
        dados = cur.fetchall()
    
    # Buscando o tipo de modalidade
    if modalidade == 'Ampla Concorrência':
        tipo_modalidade = 'A'
    elif modalidade == 'Cotas para estudantes que cursaram integralmente o ensino médio em escolas públicas':
        tipo_modalidade = 'L'
    elif modalidade == 'Cotas para estudantes autodeclarados pretos, pardos ou indígenas que cursaram integralmente o ensino médio em escolas públicas':
        tipo_modalidade = 'B'
    else:
        tipo_modalidade = 'V'
        
    # Organizando os dados para predição
    # Dados do formulário
    dados_form = [instituicao, uf, cidade, curso, grau, turno, tipo_modalidade]

    # Dados sobre as instituições
    dados_dataset = dados[0][7:20]

    # Dados sobre as notas do candidato
    dados_notas_form = [opcao, nota_l, nota_ch, nota_cn, nota_m, nota_r]

    # Dados sobre as notas do candidato com peso
    dados_notas_com_peso = [float(nota_l) * int(dados[0][9]), 
                            float(nota_ch) * int(dados[0][10]),
                            float(nota_cn )* int(dados[0][11]), 
                            float(nota_m) * int(dados[0][12]),
                            float(nota_r) * int(dados[0][13])]

    # Média ponderada
    media_ponderada = (dados_notas_com_peso[0] + dados_notas_com_peso[1] +
                            dados_notas_com_peso[2] + dados_notas_com_peso[3] +
                            dados_notas_com_peso[4]) / (int(dados[0][9]) + 
                                                        int(dados[0][10]) + 
                                                        int(dados[0][11]) + 
                                                        int(dados[0][12]) + 
                                                        int(dados[0][13]))

    # Dados para predição
    dados_to_predict = np.concatenate((dados_form, dados_dataset, dados_notas_form,
                            dados_notas_com_peso, [media_ponderada])).reshape(1, -1)
            
    # Carregando o modelo
    # Caminho do diretório atual
    diretorio_atual = os.path.dirname(__file__)

    # Caminho do diretório pai
    diretorio_pai = os.path.dirname(diretorio_atual)

    # Caminho do arquivo no diretório pai
    caminho_modelo = os.path.join(diretorio_pai, 'models/best_lr.pkl')

    # Carregando o modelo
    modelo = joblib.load(caminho_modelo)
    
    # Realizando a predição  
    predicao = modelo.predict_proba(dados_to_predict)
    probabilidade = round(predicao[0][1] * 100, 2)
    
    # Retornando a predição
    return jsonify({'probabilidade': probabilidade.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
