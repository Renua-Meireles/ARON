from typing import NamedTuple
import axelrod as axl
import FIPD_python.FIPD as FIPD

class Torneio(object):
    """ Classe Base de qualquer torneio
            Atributos:
                jogadores : list()
                turnos : int
                game : axl.Game(Payoff)
                ranking: list()
    """
    def __init__(self):
        self.__jogadores             = []
        self.ranking                 = []
        self.progresso               = 0
        self.qtd_de_jogadores        = 0
        self.qtd_total_de_interacoes = int()
        self.turnos                  = int()
        self.cancelar_torneio        = False

    def iniciar(self, signal_progresso, sinal_inserir_item):
        # Implementar Funcionamento do torneio de acordo com seu modo de interagir
        # Assim como ajustar a barra de progresso a cada interação
        #
        pass

    def atualizarBarraDeProgresso(self, signal_progresso, passo):
        self.progresso += passo
        signal_progresso.emit(int(self.progresso))

    def mostrarResultados(self, inserirItem):
        for i,jogador in enumerate(self.ranking):
            #inserirItem.emit(texto,linha,coluna)
            inserirItem.emit(str(i), 														i, 0)# Rank
            inserirItem.emit(str(jogador['estrategia']), 									i, 1)# nome
            inserirItem.emit(str(jogador['ganhos']), 										i, 2)# ganhos totais
            inserirItem.emit(str(round(jogador['ganhos']/self.qtd_de_jogadores,2)), 		i, 3)# ganho por adversario
            inserirItem.emit(str(round(jogador['ganhos']/self.qtd_total_de_interacoes,2)), 	i, 4)# ganho por interacao
            inserirItem.emit(str(self.qtd_total_de_interacoes), 							i, 5)# interacoes

    def salvarXlsx(self, arq):
        titulo_colunas = ['Rank','Estratégia','Ganho Total','Ganho/Adversário','Ganho/Interação','Interações']
        for i, texto in enumerate(titulo_colunas):
            arq.write(0,i,texto)

        for i,jogador in enumerate(self.ranking):
            #inserirItem.emit(texto,linha,coluna)
            arq.write(i+1,0,i)# Rank
            arq.write(i+1,1,jogador['estrategia'])# nome
            arq.write(i+1,2,jogador['ganhos'])# ganhos totais
            arq.write(i+1,3,jogador['ganhos']/self.qtd_de_jogadores)# ganho por adversario
            arq.write(i+1,4,jogador['ganhos']/self.qtd_total_de_interacoes)# ganho por interacao
            arq.write(i+1,5,self.qtd_total_de_interacoes)# interacoes

class RoundRobin(Torneio):
    """docstring for RoundRobin"""
    def __init__(self, turnos, t, r, p, s):
        super().__init__()
        self.game      = axl.Game(t=t, r=r, p=p, s=s)
        self.turnos    = turnos

    def iniciar(self, signal_progresso, signal_inserir_item): # Funcionamento do torneio RoundRobin
        encontros = self.qtd_de_jogadores**2
        passo_da_barra = 100/encontros
        print(self.qtd_de_jogadores)
        

        for jogador in self.jogadores:
            ganhos_acumulados = 0
            for adversario in self.jogadores:
                oponente = jogador.clone() if jogador == adversario else adversario
                match = axl.Match(players = [jogador,oponente], turns = self.turnos, game = self.game)
                match.play()
                ganhos_acumulados += match.final_score()[0]  # final_score = (int,int) -> tuple[ganho_jogador1, ganho_jogador2] 

                self.atualizarBarraDeProgresso(signal_progresso, passo_da_barra)
                if self.cancelar_torneio is True:
                    return
    
            self.ranking.append({
                'estrategia':jogador.name,
                'ganhos':ganhos_acumulados,
                })

        self.atualizarBarraDeProgresso(signal_progresso, passo_da_barra)
        self.ranking.sort(key= lambda jogador: jogador['ganhos'], reverse = True)
        self.mostrarResultados(signal_inserir_item)
        self.jogadores = []
        signal_progresso.emit(100)

    @property
    def jogadores(self):
        return self.__jogadores

    @jogadores.setter
    def jogadores(self, estrategias:list):
        self.__jogadores = estrategias
        self.qtd_de_jogadores = len(estrategias)
        self.qtd_total_de_interacoes = self.qtd_de_jogadores*self.turnos
        


class Aleatorio(Torneio):
    """docstring for Aleatorio"""
    def __init__(self):
        super().__init__()

    def iniciar(self, signal_progresso):
        pass
        
        


class Axelrod1(RoundRobin):
    def __init__(self, turnos, t, r, p, s):
        super().__init__(turnos = turnos, t=t, r=r, p=p, s=s)

        self.jogadores = [	axl.TitForTat(),
                            axl.TidemanAndChieruzzi(),
                            axl.Nydegger(),
                            axl.Grofman(),
                            axl.Shubik(),
                            axl.SteinAndRapoport(),
                            axl.Grudger(),
                            axl.Davis(),
                            axl.RevisedDowning(),
                            axl.Feld(),
                            axl.Joss(),
                            axl.Tullock(),
                            axl.UnnamedStrategy(),
                            axl.Random(),
                        ]


class Axelrod2(RoundRobin):
    def __init__(self, turnos, t, r, p, s):
        super().__init__(turnos = turnos, t=t, r=r, p=p, s=s)

        self.jogadores = [	axl.TitForTat(),
                            axl.Champion(),
                            axl.Borufsen(),
                            axl.Cave(),
                            axl.WmAdams(),
                            axl.GraaskampKatzen(),
                            axl.Weiner(),
                            axl.Harrington(),
                            axl.MoreTidemanAndChieruzzi(),
                            axl.Kluepfel(), # Abraham Getzler logo após
                            axl.Leyvraz(),
                            axl.White(), # 2 Whites
                            axl.RichardHufford(),
                            axl.Yamachi(),
                            axl.Rowsam(),
                            axl.GoByMajority(),
                            axl.TitFor2Tats(),
                            axl.Tranquilizer(),
                            axl.Grofman(),
                            axl.Joss(),
                            axl.Nydegger(),
                            axl.RevisedDowning(),
                            axl.Gladstein(),
                            axl.Grudger(),
                            axl.Feld(),
                            axl.Random(),
                        ]


class Aniversario20Anos(RoundRobin):
    def __init__(self, turnos, t, r, p, s):
        super().__init__(turnos = turnos, t=t, r=r, p=p, s=s)
        self.jogadores = [
                        ]


class Knight(RoundRobin):
    def __init__(self, turnos, t, r, p, s):
        super().__init__(turnos = turnos, t=t, r=r, p=p, s=s)

        self.jogadores = [estrategia() for estrategia in axl.all_strategies]


class Borges(Torneio):
    def __init__(self, qtd_de_interacoes):
        self.torneio = FIPD.TorneioFIPD(qtd_interacoes = qtd_de_interacoes)
        self.qtd_total_de_interacoes = qtd_de_interacoes

    def iniciar(self, signal_progresso, signal_inserir_item):
        self.ranking = self.torneio.iniciar(signal_progresso)
        self.mostrarResultados(signal_inserir_item)
        signal_progresso.emit(100)

    def mostrarResultados(self, inserir_item):
        linha = 0
        fase = 0
        for i,jogador in enumerate(self.ranking):
            if jogador['fase'] != str(fase):
                fase+=1
                inserir_item.emit('Fase '+str(fase), linha, 0)	
                linha+=1
            rank = '1° do Grupo {}'.format(jogador['grupo'])
            inserir_item.emit(rank, 										linha, 0)# Rank
            inserir_item.emit(str(jogador['id']), 							linha, 1)# nome
            inserir_item.emit(str(round(jogador['ganhos_acumulados'],2)), 	linha, 2)# ganhos totais
            inserir_item.emit('?', 											linha, 3)# ganho por adversario
            inserir_item.emit(str(round(jogador['ganho_medio'],2)), 		linha, 4)# ganho por interacao
            inserir_item.emit(str(jogador['qtd_interacoes']), 				linha, 5)# interacoes
            linha+=1

    def salvarXlsx(self, arq):
        titulo_colunas = ['Rank','Estratégia','Ganho Total','Ganho/Adversário','Ganho/Interação','Interações']
        for i, texto in enumerate(titulo_colunas):
            arq.write(0,i,texto)

        linha = 1
        fase = 0
        for i,jogador in enumerate(self.ranking):
            if jogador['fase'] != str(fase):
                fase+=1
                arq.write(linha, 0, 'Fase '+str(fase))	
                linha+=1
            rank = '1° do Grupo {}'.format(jogador['grupo'])
            arq.write(linha, 0, rank)# Rank
            arq.write(linha, 1, jogador['id'])# nome
            arq.write(linha, 2, jogador['ganhos_acumulados'])# ganhos totais
            arq.write(linha, 3, '?')# ganho por adversario
            arq.write(linha, 4, jogador['ganho_medio'])# ganho por interacao
            arq.write(linha, 5, jogador['qtd_interacoes'])# interacoes
            linha+=1

# =========================================================================================
# Armazendo o nome das estrategias separando por TORNEIO e por CLASSIFICAÇÃO DA DISSERTAÇÃO
# =========================================================================================
estrategias_torneioAxel1  = [axl.TitForTat,axl.TidemanAndChieruzzi,axl.Nydegger,
                            axl.Grofman,axl.Shubik,axl.SteinAndRapoport,axl.Grudger,
                            axl.Davis,axl.RevisedDowning,axl.Feld,axl.Joss,axl.Tullock,
                            axl.UnnamedStrategy,axl.Random]
estrategias_torneioAxel1 = dict([(s.name, s) for s in estrategias_torneioAxel1])

estrategias_torneioAxel2  = [axl.TitForTat, axl.Champion,	axl.Borufsen,
                            axl.Cave, axl.WmAdams, axl.GraaskampKatzen,
                            axl.Weiner, axl.Harrington, axl.MoreTidemanAndChieruzzi,
                            axl.Kluepfel, axl.Leyvraz, axl.White,
                            axl.RichardHufford, axl.Yamachi, axl.Rowsam,
                            axl.GoByMajority, axl.TitFor2Tats, axl.Tranquilizer, 
                            axl.Grofman, axl.Joss, axl.Nydegger, axl.RevisedDowning,
                            axl.Gladstein, axl.Grudger, axl.Feld, axl.Random]
estrategias_torneioAxel2 = dict([(s.name, s) for s in estrategias_torneioAxel2])

estrategias_torneio20Anos = {}
estrategias_torneioBorges = ['{}{}{}'.format(i,j,k) for i in range(1,9) for j in range(1,9) for k in range(1,9)]	#111,...,888
estrategias_torneioBorges = dict([(s, s) for s in estrategias_torneioBorges])
estrategias_torneioKnight = [estrategia for estrategia in axl.all_strategies]
estrategias_torneioKnight = dict([(s.name, s) for s in estrategias_torneioKnight])

estrategias_todas         = {**estrategias_torneioKnight, **estrategias_torneioBorges}



reativo_simples      = [axl.Cooperator, axl.Defector]
reativo_simples = dict([(s.name, s) for s in reativo_simples])
baseado_em_modelo    = {}
baseado_em_objetivo  = {}
baseado_em_utilidade = {}
com_aprendizado      = {}
# =========================================================================================