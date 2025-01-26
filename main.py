from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Criando a instância do Flask e configurando o banco de dados
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///motivations.db'  # Banco SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desabilitar notificações de mudanças no banco

# Instância do SQLAlchemy
db = SQLAlchemy(app)

# Definindo o modelo Motivation para a tabela no banco de dados
class Motivation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)  # Data em formato string
    mood = db.Column(db.String(10), nullable=False)  # Humor
    note = db.Column(db.String(200), nullable=True)  # Nota (opcional)

# Função para criar as tabelas no banco de dados, se não existirem
def create_tables():
    with app.app_context():  # Criar o contexto do aplicativo
        db.create_all()  # Cria todas as tabelas no banco de dados

# Rota principal para exibir as motivações
@app.route('/')
def index():
    motivations = Motivation.query.all()  # Pegando todas as motivações do banco
    return render_template('index.html', motivations=motivations)

# Rota para adicionar uma nova motivação
@app.route('/add', methods=['POST'])
def add_motivation():
    date = request.form['date']  # Pegando a data do formulário
    mood = request.form['mood']  # Pegando o humor do formulário
    note = request.form['note']  # Pegando a nota do formulário (pode ser vazia)

    # Criando um novo registro de motivação
    new_motivation = Motivation(date=date, mood=mood, note=note)
    db.session.add(new_motivation)  # Adicionando à sessão do banco de dados
    db.session.commit()  # Salvando no banco de dados

    return redirect(url_for('index'))  # Redirecionando de volta para a página principal

# Rota para deletar uma motivação
@app.route('/delete/<int:id>')
def delete_motivation(id):
    motivation = Motivation.query.get(id)  # Buscando a motivação pelo ID
    if motivation:
        db.session.delete(motivation)  # Deletando a motivação do banco de dados
        db.session.commit()  # Commit para garantir que a exclusão seja realizada

    return redirect(url_for('index'))  # Redirecionando de volta para a página principal

# Função principal para rodar o servidor Flask
if __name__ == '__main__':
    create_tables()  # Certifique-se de chamar essa função para criar as tabelas
    app.run(debug=True)
