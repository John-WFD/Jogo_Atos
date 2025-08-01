import csv
import random
import os

class Jogo:
    arquivo = "perguntas.csv"
    perguntas = []
    usadas = set()
    def __init__(self):
        while True:
            self._carregar_perguntas()

            if os.path.exists("jogo_salvo.csv"):
                op = input("""
                (1) Cadastrar pergunta
                (2) Perguntas cadastradas
                (3) Continuar jogo
                (4) Novo jogo
                (0) Sair
                """) 

                if op == "1":
                    perg = input("Pergunta: ")
                    resp = input("Resposta: ")
                    vers = input("Versículo: ")

                    self.cadastrar_pergunta(perg, resp, vers)
                elif op == "2":
                    self.ver_perguntas()
                elif op == "3":
                    os.remove("jogo_salvo.csv")
                    self.jogar()
                elif op == "4":
                    with open("jogo_salvo.csv", mode='r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        self.usadas = [row for row in reader]
                    self.jogar()
                elif op == "0":
                    break
                else:
                    print("opção inválida")
            else:
                op = input("""
                (1) Cadastrar pergunta
                (2) Perguntas cadastradas
                (3) Novo jogo
                (0) Sair
                """) 

                if op == "1":
                    perg = input("Pergunta: ")
                    resp = input("Resposta: ")
                    vers = input("Versículo: ")

                    self.cadastrar_pergunta(perg, resp, vers)
                elif op == "2":
                    self.ver_perguntas()
                elif op == "3":
                    self.jogar()
                elif op == "0":
                    break
                else:
                    print("opção inválida")


    def _carregar_perguntas(self):
        if not os.path.exists(self.arquivo):
            with open(self.arquivo, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'pergunta', 'resposta', 'versiculo'])  # cabeçalho
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
        print(f"Pergunta {novo_id} cadastrada com sucesso.")

    def ver_perguntas(self):
        if not self.perguntas:
            print("Nenhuma pergunta cadastrada.")
            return
        for p in self.perguntas:
            print(f"{p['id']}. {p['pergunta']} (Versículo: {p['versiculo']})")

    def jogar(self):
        if not self.perguntas:
            print("Nenhuma pergunta cadastrada.")
            return

        print("Iniciando o jogo. Pressione Ctrl+C para sair.")
        while True:
            restantes = [p for p in self.perguntas if p['id'] not in self.usadas]
            if not restantes:
                print("\nTodas as perguntas foram usadas. Reiniciando ciclo...\n")
                self.usadas.clear()
                os.remove("jogo_salvo.csv")
                restantes = self.perguntas.copy()

            pergunta = random.choice(restantes)
            self.usadas.add(pergunta['id'])

            if not os.path.exists("jogo_salvo.csv"):
                with open("jogo_salvo.csv", mode='a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([pergunta['id']])

            if 126 < int(pergunta['id']):
                print(f"\nID: {pergunta['id']}")
                print(f"\nPergunta: {pergunta['pergunta']}")
                input("Sua resposta: ")
                print(f"Resposta correta: {pergunta['resposta']} (Versículo: {pergunta['versiculo']})")

                with open("jogo_salvo.csv", mode='a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([pergunta['id']])

Jogo()