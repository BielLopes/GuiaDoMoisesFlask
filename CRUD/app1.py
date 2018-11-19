# encoding: utf-8
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dataBase.sqlite' #'mysql+pymysql://user:senha@localhost/NomeBaseDeDaos'     obs:é mais facil com o MySQLWorkBench
dataBase = SQLAlchemy(app)

class Pessoa(dataBase.Model):


    __tablename__= 'cliente'
    _id = dataBase.Column(dataBase.Integer, primary_key = True, autoincrement = True)
    nome = dataBase.Column(dataBase.String)
    telefone = dataBase.Column(dataBase.String)
    cpf = dataBase.Column(dataBase.String)
    email = dataBase.Column(dataBase.String)
    def __init__(self, nome, telefone, cpf, email):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.cpf = cpf

dataBase.create_all()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastro.html')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        cpf = request.form.get('cpf')
        email = request.form.get('email')

        if nome and telefone and email and cpf:
            p = Pessoa(nome, telefone, cpf, email)
            dataBase.session.add(p)
            dataBase.session.commit()
    return redirect(url_for('index'))


@app.route('/lista')
def lista():
    pessoas = Pessoa.query.all()
    return render_template('lista.html', pessoas = pessoas)


@app.route('/excluir/<int:id>')
def excluir(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()
    dataBase.session.delete(pessoa)
    dataBase.session.commit()
    #Reenviando os usuarios para regarregar a mesma página
    #(Isso é uma classica Requisição clinte servidor, ou seja, toda a página será recarregada)
    pessoas = Pessoa.query.all()
    return render_template('lista.html', pessoas = pessoas)


@app.route('/atualizar/<int:id>', methods=['GET', 'POST'])
def atualizar(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()

    if request.method == 'POST':
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        cpf = request.form.get('cpf')
        email = request.form.get('email')

        if nome and telefone and email and cpf:
            pessoa.nome = nome
            pessoa.telefone = telefone
            pessoa.cpf = cpf
            pessoa.email = email

            dataBase.session.commit()

            return redirect(url_for('lista'))

    return render_template('Atualiza.html', pessoa = pessoa)


if __name__ == '__main__':
    app.run(debug = True)
