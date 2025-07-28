import csv
import random
import os

class JogoFlask:
    def __init__(self):
        self.arquivo = "perguntas.csv"
        self.arquivo_jogo_salvo = "jogo_salvo.csv"
        self._carregar_perguntas()

    def _carregar_perguntas(self):
        if not os.path.exists(self.arquivo):
            with open(self.arquivo, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'pergunta', 'resposta', 'versiculo'])
            self.perguntas = []
        else:
            with open(self.arquivo, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.perguntas = [row for row in reader]

    def cadastrar_pergunta(self, pergunta, resposta, versiculo):
        novo_id = str(len(self.perguntas) + 1)
        nova = {
            'id': novo_id,
            'pergunta': pergunta.strip(),
            'resposta': resposta.strip(),
            'versiculo': versiculo.strip()
        }

        with open(self.arquivo, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'pergunta', 'resposta', 'versiculo'])
            writer.writerow(nova)
        
        self.perguntas.append(nova)
        return novo_id

    def obter_perguntas(self):
        self._carregar_perguntas()
        return self.perguntas

    def obter_usadas(self):
        if not os.path.exists(self.arquivo_jogo_salvo):
            return set()
        
        with open(self.arquivo_jogo_salvo, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            return {row[0] for row in reader if row}

    def salvar_usada(self, pergunta_id):
        with open(self.arquivo_jogo_salvo, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([pergunta_id])

    def reiniciar_jogo(self):
        if os.path.exists(self.arquivo_jogo_salvo):
            os.remove(self.arquivo_jogo_salvo)

    def obter_pergunta_aleatoria(self):
        if not self.perguntas:
            return None

        usadas = self.obter_usadas()
        restantes = [p for p in self.perguntas if p['id'] not in usadas]
        
        if not restantes:
            # Todas foram usadas, reinicia o ciclo
            self.reiniciar_jogo()
            restantes = self.perguntas.copy()

        return random.choice(restantes)