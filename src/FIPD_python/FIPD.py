#coding: utf-8
from random import shuffle
import FIPD_python.GRUPO as gp
import FIPD_python.JOGADOR as J

# ================================================================
# ========= CLASSE QUE REPRESENTA O TORNEIO =====================
# ========= CONTÉM A ESTRUTURA DO TORNEIO ========================
# ================================================================
class TorneioFIPD(object):
	def __init__(self,qtd_interacoes = 30000):
		self.jogadores = []    # armazenar os jogadores BORGES. tamanho 512
		self.fases     = []
		self.qtd_interacoes = qtd_interacoes
		self.qtd_fases = 4

	# ========================================================
	# Carregar os jogadores com as 512 estratégias de BORGES
	# ========================================================
	def carregarJogadores(self):
		# Cada fator de decisão do jogador recebe uma das 8 estratégias
		self.jogadores = [J.Borges(i+1, j+1, k+1) for i in range(8) for j in range(8) for k in range(8)] 
		# jogadores = [Borges(111), Borges(112), ... , Borges(118),  Borges(121), ... , Borges(887), Borges(888)]

	# ========================================================
	# INICIAR O TORNEIO COMPOSTO POR QUATRO FASES DIFERENTES
	# ========================================================
	def iniciar(self, signal_progresso):
		progresso = 0
		qtd_total_de_interacoes = self.qtd_interacoes*(32+11+5+1)	# fase1(32gps), fase2(11gps), fase3(5gps), fase4(1gp)
		passo_da_barra          = 100/qtd_total_de_interacoes 		# Quantidade de progresso ralizado em cada interação
		progresso_por_grupo     = 100/(32+11+5+1)					# Quantidade de progresso ralizado em cada grupo

		self.carregarJogadores()
		grupos = None
		dados = []
		for f in range(1,self.qtd_fases+1):	# se quatro fases: range(1,5) -> [1,2,3,4]
			grupos = self.criarGrupos(fase = f, grupos_anteriores = grupos)
			self.fases.append(grupos)
			for grupo in grupos:
				grupo.realizarInteracoes(self.qtd_interacoes, signal_progresso, passo_da_barra, progresso)
				jogador = {	'fase':grupo.vencedor().grupo[0],
							'grupo':grupo.vencedor().grupo[-2:],
							'id':grupo.vencedor().id,
							'ganhos_acumulados':grupo.vencedor().ganhos_acumulados,
							'ganho_medio':grupo.vencedor().ganho_medio,
							'qtd_interacoes':grupo.vencedor().qtd_interacoes,
							}
				dados.append(jogador.copy())
				progresso += progresso_por_grupo
		gp.Grupo.resetarContadores()
		return(dados)
				
	# ========================================================
	# RETORNAR UMA LISTA CONTENDO TODOS OS JOGADORES INSERIDOS EM SEUS
	# REPECTIVOS GRUPOS DA FASE ATUAL
	# ========================================================
	def criarGrupos(self, fase, grupos_anteriores = None):
		n_jogadores  = 16
		if  (fase==1):					# Na fase 1: 32 grupos; Todos os 512 jogadores + 3 irão participar
			n_grupos = 32
			sacola_de_jogadores = self.jogadores[:]
		else:							# Nas fases posteriores; apenas jogadores selecionados irão participar
			if(fase==2): 	n_grupos = 11
			elif(fase==3): 	n_grupos = 5
			else: 			n_grupos = 1
			sacola_de_jogadores = self.melhoresJogadoresDaFaseAnterior(grupos_anteriores)
			for jogador in sacola_de_jogadores: jogador.resetarJogador()
			

		# Retira n_jogadores da sacola + 3 jogadores (tft,tft-g e pavlov)
		# E os coloca em um grupo. ---> REPETIR n_grupos vezes
		shuffle(sacola_de_jogadores)
		novos_grupos = [ gp.Grupo([sacola_de_jogadores.pop() for i in range(n_jogadores)]\
								+[J.Tft(), J.Tft_g(), J.Pavlov()])  for j in range(n_grupos)]
		return(novos_grupos)  # [ [grupo 1], [grupo 2], ... , [grupo n] ]

	# ========================================================
	# RETORNAR UMA LISTA DE JOGADORES PARA A FASE POSTERIOR (FASE2:176jgdrs, FASE3:80jgdrs, FASE4:16jgdrs)
	# ========================================================
	def melhoresJogadoresDaFaseAnterior(self, grupos_anteriores):
		n_grupos = len(grupos_anteriores)
		#	DEFINIR QUANTOS JOGADORES SERÃO SELECIONADOS, DE ACORDO COM A FASE (VER BORGES)
		if(n_grupos == 32):   contador = 176
		elif(n_grupos == 11): contador = 80
		elif(n_grupos == 5):  contador = 16

		melhores     = []
		selecionados = []
		# Colocar os 16 melhores jogadores de cada grupo em uma lista
		for grupo in grupos_anteriores:	melhores.extend(grupo.selecionarMelhores16())
		melhores.sort(key = lambda x:x.ganho_medio, reverse=True)	# Prioridade para os melhores por ganho médio
		for jogador in melhores:
			for i in range(n_grupos*16):	# Verificar se a estratégia do jogador aparece em algum outro jogador rankeado
				if(jogador!=melhores[i]):
					if(jogador.f1 == melhores[i].f1):
						selecionados.append(jogador); break
					if(jogador.f2 == melhores[i].f2):
						selecionados.append(jogador); break
					if(jogador.f3 == melhores[i].f3):
						selecionados.append(jogador); break
			else: contador +=1	# Se executar, não existe outro jogador com a mesma estratégia. Entao corrige o contador
			contador -= 1
			if(contador==0):break	# Se já tiver preenchido com os jogadores necessarios finaliza
		if(contador>0):	# Se não foram selecionados jogadores o suficiente. preenche os melhores rankeados
			for jogador in selecionados: melhores.remove(jogador)
			i=0
			while(contador>0):
				selecionados.append(melhores[i])
				i+=1
				contador-=1
		return(selecionados)


