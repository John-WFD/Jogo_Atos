from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
from jogo import JogoFlask

app = Flask(__name__)
app.secret_key = "Jwofhdn"

# Instância global do jogo
jogo = JogoFlask()

@app.route('/')
def index():
    tem_jogo_salvo = os.path.exists(jogo.arquivo_jogo_salvo)
    total_perguntas = len(jogo.obter_perguntas())
    usadas = len(jogo.obter_usadas()) if tem_jogo_salvo else 0
    
    return render_template('index.html', 
                         tem_jogo_salvo=tem_jogo_salvo, 
                         total_perguntas=total_perguntas,
                         usadas=usadas)

@app.route('/perguntas')
def listar_perguntas():
    perguntas = jogo.obter_perguntas()
    return render_template('perguntas.html', perguntas=perguntas)

@app.route('/jogar')
def jogar():
    pergunta = jogo.obter_pergunta_aleatoria()
    
    if not pergunta:
        flash('Nenhuma pergunta cadastrada. Cadastre algumas perguntas primeiro!', 'error')
        return redirect(url_for('index'))
    
    # Salva a pergunta atual na sessão
    session['pergunta_atual'] = pergunta
    
    return render_template('jogar.html', pergunta=pergunta)

@app.route('/resposta', methods=['POST'])
def resposta():
    pergunta_atual = session.get('pergunta_atual')
    
    if not pergunta_atual:
        flash('Erro: pergunta não encontrada!', 'error')
        return redirect(url_for('index'))
    
    resposta_usuario = request.form.get('resposta', '')
    
    # Marca a pergunta como usada
    jogo.salvar_usada(pergunta_atual['id'])
    
    # Remove da sessão
    session.pop('pergunta_atual', None)
    
    return render_template('resposta.html', 
                         pergunta=pergunta_atual, 
                         resposta_usuario=resposta_usuario)

@app.route('/novo_jogo')
def novo_jogo():
    jogo.reiniciar_jogo()
    flash('Novo jogo iniciado!', 'success')
    return redirect(url_for('jogar'))

@app.route('/continuar_jogo')
def continuar_jogo():
    return redirect(url_for('jogar'))

@app.route('/status')
def status():
    """Endpoint para obter status do jogo via AJAX"""
    total_perguntas = len(jogo.obter_perguntas())
    usadas = len(jogo.obter_usadas())
    
    return jsonify({
        'total': total_perguntas,
        'usadas': usadas,
        'restantes': total_perguntas - usadas
    })

if __name__ == "__main__":
    app.run(port=8080)