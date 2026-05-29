import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, redirect
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)

ARQUIVO_JSON = os.path.join(BASE_DIR, 'produtos.json')

_produtos_cache = None


def ler_produtos():
    global _produtos_cache
    if _produtos_cache is not None:
        return _produtos_cache
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, 'r', encoding='utf-8') as arquivo:
            _produtos_cache = json.load(arquivo)
    else:
        _produtos_cache = []
    return _produtos_cache


def salvar_produtos(produtos):
    global _produtos_cache
    _produtos_cache = produtos
    try:
        with open(ARQUIVO_JSON, 'w', encoding='utf-8') as arquivo:
            json.dump(produtos, arquivo, indent=4, ensure_ascii=False)
    except OSError:
        pass


@app.route('/')
def index():
    produtos = ler_produtos()
    return render_template('index.html', produtos=produtos)


@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        descricao = request.form['descricao']

        produtos = ler_produtos()

        novo_produto = {
            'id': len(produtos) + 1,
            'nome': nome,
            'preco': preco,
            'descricao': descricao
        }

        produtos.append(novo_produto)
        salvar_produtos(produtos)

        return redirect('/')

    return render_template('adicionar.html')


@app.route('/produto/<int:id>')
def detalhes(id):
    produtos = ler_produtos()
    produto_encontrado = None

    for produto in produtos:
        if produto['id'] == id:
            produto_encontrado = produto
            break

    return render_template('detalhes.html', produto=produto_encontrado)


if __name__ == '__main__':
    app.run(debug=True)
