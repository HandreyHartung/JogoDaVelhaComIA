import random
import time

class JogoDaVelha:
    def __init__(self):
        self.tabuleiro = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.jogador_atual = 1
        self.metricas = {
            'nos_explorados': 0,
            'tempo_decisao': [],
            'profundidade_max': 0,
            'vitorias_jogador': 0,
            'vitorias_ia': 0,
            'empates': 0,
            'total_jogos': 0
        }

    def reiniciar_jogo(self):
        self.tabuleiro = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.jogador_atual = 1

    def fazer_jogada(self, linha, coluna):
        if 0 <= linha < 3 and 0 <= coluna < 3 and self.tabuleiro[linha][coluna] == 0:
            self.tabuleiro[linha][coluna] = self.jogador_atual
            self.jogador_atual = 3 - self.jogador_atual
            return True
        return False

    def verificar_vitoria(self):
        for linha in self.tabuleiro:
            if linha[0] == linha[1] == linha[2] != 0:
                return linha[0]
        for coluna in range(3):
            if self.tabuleiro[0][coluna] == self.tabuleiro[1][coluna] == self.tabuleiro[2][coluna] != 0:
                return self.tabuleiro[0][coluna]
        if self.tabuleiro[0][0] == self.tabuleiro[1][1] == self.tabuleiro[2][2] != 0:
            return self.tabuleiro[0][0]
        if self.tabuleiro[0][2] == self.tabuleiro[1][1] == self.tabuleiro[2][0] != 0:
            return self.tabuleiro[0][2]
        if all(self.tabuleiro[i][j] != 0 for i in range(3) for j in range(3)):
            return 3
        return 0

    def movimentos_possiveis(self):
        movimentos = []
        for i in range(3):
            for j in range(3):
                if self.tabuleiro[i][j] == 0:
                    movimentos.append((i, j))
        return movimentos

    def minimax(self, profundidade, e_maximizador, alfa=float('-inf'), beta=float('inf')):
        self.metricas['nos_explorados'] += 1
        if profundidade > self.metricas['profundidade_max']:
            self.metricas['profundidade_max'] = profundidade
        resultado = self.verificar_vitoria()
        if resultado != 0:
            if resultado == 2:
                return 10 - profundidade
            elif resultado == 1:
                return profundidade - 10
            else:
                return 0
        if profundidade >= 9:
            return 0
        if e_maximizador:
            melhor_valor = float('-inf')
            for movimento in self.movimentos_possiveis():
                self.tabuleiro[movimento[0]][movimento[1]] = 2
                valor = self.minimax(profundidade + 1, False, alfa, beta)
                self.tabuleiro[movimento[0]][movimento[1]] = 0
                melhor_valor = max(melhor_valor, valor)
                alfa = max(alfa, melhor_valor)
                if beta <= alfa:
                    break
            return melhor_valor
        else:
            melhor_valor = float('inf')
            for movimento in self.movimentos_possiveis():
                self.tabuleiro[movimento[0]][movimento[1]] = 1
                valor = self.minimax(profundidade + 1, True, alfa, beta)
                self.tabuleiro[movimento[0]][movimento[1]] = 0
                melhor_valor = min(melhor_valor, valor)
                beta = min(beta, melhor_valor)
                if beta <= alfa:
                    break
            return melhor_valor

    def melhor_jogada_ia(self):
        self.metricas['nos_explorados'] = 0
        inicio = time.time()
        melhor_valor = float('-inf')
        melhor_movimento = None
        for movimento in self.movimentos_possiveis():
            self.tabuleiro[movimento[0]][movimento[1]] = 2
            valor = self.minimax(0, False)
            self.tabuleiro[movimento[0]][movimento[1]] = 0
            if valor > melhor_valor:
                melhor_valor = valor
                melhor_movimento = movimento
        fim = time.time()
        self.metricas['tempo_decisao'].append(fim - inicio)
        return melhor_movimento

    def jogada_ia(self):
        if self.jogador_atual == 2:
            movimento = self.melhor_jogada_ia()
            if movimento:
                self.fazer_jogada(movimento[0], movimento[1])
                return True
        return False

    def imprimir_tabuleiro(self):
        simbolos = {0: ' ', 1: 'X', 2: 'O'}
        print("\n  0 1 2")
        for i in range(3):
            print(f"{i}", end=" ")
            for j in range(3):
                print(simbolos[self.tabuleiro[i][j]], end=" ")
            print()
        print()

    def atualizar_estatisticas(self, resultado):
        self.metricas['total_jogos'] += 1
        if resultado == 1:
            self.metricas['vitorias_jogador'] += 1
        elif resultado == 2:
            self.metricas['vitorias_ia'] += 1
        elif resultado == 3:
            self.metricas['empates'] += 1

    def imprimir_estatisticas(self):
        print("\n===== ESTATÍSTICAS =====")
        print(f"Total de jogos: {self.metricas['total_jogos']}")
        print(f"Vitórias do jogador: {self.metricas['vitorias_jogador']}")
        print(f"Vitórias da IA: {self.metricas['vitorias_ia']}")
        print(f"Empates: {self.metricas['empates']}")
        if self.metricas['tempo_decisao']:
            tempo_medio = sum(self.metricas['tempo_decisao']) / len(self.metricas['tempo_decisao'])
            print(f"Tempo médio de decisão da IA: {tempo_medio:.4f} segundos")
        print(f"Profundidade máxima alcançada: {self.metricas['profundidade_max']}")
        print(f"Média de nós explorados por jogada: {self.metricas['nos_explorados'] / max(1, len(self.metricas['tempo_decisao'])):.2f}")
        print("========================\n")

def jogar_contra_ia():
    jogo = JogoDaVelha()
    jogo.jogador_atual = random.choice([1, 2])
    print("=== JOGO DA VELHA COM IA MINIMAX ===")
    print("Você é X, a IA é O")
    print("Digite as coordenadas como 'linha coluna' (ex: 0 0 para o canto superior esquerdo)")
    print("Digite 'q' para sair\n")
    while True:
        jogo.imprimir_tabuleiro()
        resultado = jogo.verificar_vitoria()
        if resultado != 0:
            if resultado == 1:
                print("Você venceu!")
            elif resultado == 2:
                print("A IA venceu!")
            else:
                print("Empate!")
            jogo.atualizar_estatisticas(resultado)
            resposta = input("Jogar novamente? (s/n): ").lower()
            if resposta != 's':
                jogo.imprimir_estatisticas()
                break
            jogo.reiniciar_jogo()
            continue
        if jogo.jogador_atual == 1:
            try:
                entrada = input("Sua jogada (linha coluna): ")
                if entrada.lower() == 'q':
                    jogo.imprimir_estatisticas()
                    break
                linha, coluna = map(int, entrada.split())
                if not jogo.fazer_jogada(linha, coluna):
                    print("Jogada inválida! Tente novamente.")
            except ValueError:
                print("Entrada inválida! Use o formato 'linha coluna' (ex: 0 0)")
        else:
            print("IA está pensando...")
            jogo.jogada_ia()

def executar_simulacao(num_jogos=100):
    jogo = JogoDaVelha()
    print(f"Simulando {num_jogos} jogos entre IA (Minimax) e jogador aleatório...")
    for _ in range(num_jogos):
        jogo.reiniciar_jogo()
        if random.choice([True, False]):
            jogo.jogador_atual = 2
        while True:
            resultado = jogo.verificar_vitoria()
            if resultado != 0:
                jogo.atualizar_estatisticas(resultado)
                break
            if jogo.jogador_atual == 1:
                movimentos = jogo.movimentos_possiveis()
                if movimentos:
                    movimento = random.choice(movimentos)
                    jogo.fazer_jogada(movimento[0], movimento[1])
            else:
                jogo.jogada_ia()
    jogo.imprimir_estatisticas()
    return jogo.metricas

def menu_principal():
    while True:
        print("\nEscolha uma opção:")
        print("1. Jogar contra a IA")
        print("2. Executar simulação (IA vs. jogador aleatório. (Máximo 999))")
        print("0. Sair")
        opcao = input("Opção: ")
        if opcao == "1":
            jogar_contra_ia()
        elif opcao == "2":
            try:
                num_jogos = int(input("Número de jogos para simular (máximo 999): "))
                if num_jogos > 999:
                    print("Limite excedido!")
                else:
                    executar_simulacao(num_jogos)
            except ValueError:
                print("Entrada inválida! Digite um número inteiro.")
        elif opcao == "0":
            print("Saindo do programa.")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu_principal()

