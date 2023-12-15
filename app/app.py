import os.path
import sqlite3
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
        cur.execute("select grau from dados_to_predict where uf_campus = ? and municipio_campus = ? and ies = ? and nome_curso = ? group by grau having count(grau) >= 1", (uf, cidade, instituicao, curso,))
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

#TODO: Buscando os dados para a análise com base na uf, cidade, instituição, curso, grau, urno selecionado e notas do aluno

if __name__ == '__main__':
    app.run(debug=True)
