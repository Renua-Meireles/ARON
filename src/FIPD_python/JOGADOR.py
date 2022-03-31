
import FIPD_python.FATOR_DECISAO as FD


#	CRIANDO AS 8 ESTRATÉGIAS PROPOSTAS POR BORGES (Cada fator recebe uma estrategia -> 8^3 = 512 comportamentos diferentes)
ESTRATEGIAS = [[i,j,k] for i in range(1, 0,-1) for j in range(1,-1,-1) for k in range(1,-1,-1)] \
			+ [[i,j,k] for i in range(1) for j in range(2) for k in range(2)]


# =========== ESTRATÉGIAS  ===========
# ESTRATEGIAS = [ [1,1,1], [1,1,0], [1,0,1], [1,0,0], [0,0,0], [0,0,1], [0,1,0], [0,1,1] ]
#	        1 = C  /  0 = D
#
#  S1	S2	S3	S4	S5	S6	S7	S8
#  C	C	C	C	D	D	D	D
#  C	C	D	D	D	D	C	C
#  C	D	C	D	D	C	D	C

# ================================================================
# ============= TEMPLATE PARA OS JOGADORES =======================
# ================================================================
class Jogador(object):
	def __init__(self):
		self.id                = None	# Representa o indivíduo
		self.qtd_interacoes    = 0
		self.acao_atual        = 0	# A ação que está sendo tomada na interação atual,
									# os dois jogadores precisam definir suas ações separadamente,
									# em seguida cada um receberá o pagamento com base na ação do adversário.
		# ARMAZENANDO DADOS SOBRE OS GANHOS
		self.pagamento_atual   = 0	# Armazena o pagamento atual para atualizar os diversos dados do jogador
		self.ganhos_acumulados = 0
		self.ganho_medio       = 0	# ganhos_acumulados/qtd_interações -> atualiza a cada interação
		self.menor_ganho       = float('inf')	# qualquer PRIMEIRO ganho será o menor
		self.maior_ganho       = -float('inf')	# qualquer PRIMEIRO ganho será o maior

	def determinarAcao(self, *args):	pass

	def determinarPagamento(self, adversario):
		a1 = self.acao_atual 
		a2 = adversario.acao_atual
		self.pagamento_atual = 1 - 2*a1 + 4*a2 if(a1<a2) else 1 - a1 + 3*a2


	def registrarValores(self, adversario):
		self.ganhos_acumulados += self.pagamento_atual
		self.qtd_interacoes    += 1
		self.ganho_medio       = self.ganhos_acumulados / self.qtd_interacoes
		self.salvarRecursosParaAEstrategia(adversario)
		if(self.pagamento_atual > self.maior_ganho): self.maior_ganho = self.pagamento_atual
		if(self.pagamento_atual < self.menor_ganho): self.menor_ganho = self.pagamento_atual

	def salvarRecursosParaAEstrategia(self, adversario):pass

	def resetarJogador(self):
		self.__init__()

	def __repr__(self):
		string = ''
		string += '{}{:<8}'.format('J.',self.id)
		string += '{} {:<9}-  '.format('Ganhos:',round(self.ganhos_acumulados,2))
		string += '{} {:<6}-  '.format('Interações:',self.qtd_interacoes)
		string += '{} {:<6}-  '.format('Ganho médio:',round(self.ganho_medio,2))
		string += '{} {:<6}-  '.format('Maior ganho:',round(self.maior_ganho,2))
		string += '{} {:<6}\n'.format('Menor ganho:',round(self.menor_ganho,2))
		return(string)

	__str__ = __repr__
# ======================================================================
# ========= JOGADORES PARA AS ESTRATÉGIAS TIT-FOR-TAT ==================
# Começa cooperando e repete a ação da última interação com o adversário
# ======================================================================
class Tft(Jogador):
	def __init__(self):
		super().__init__()
		self.id = 'TFT'
		self.ultima_acao_das_interacoes = [[],[]] # Salvar última ação de cada adversário interagido
										# [[id_adv_1,...,id_adv_N], [acao_adv_1,...,acao_adv_1]]

	def determinarAcao(self, adversario, *args):
		if(adversario.id not in self.ultima_acao_das_interacoes[0]): # Se nunca interou com esse adversário
			self.ultima_acao_das_interacoes[0].append(adversario.id)
			self.ultima_acao_das_interacoes[1].append(1)			# Assume que a última ação dele foi C

		indice          =  self.ultima_acao_das_interacoes[0].index(adversario.id)
		ultima_acao_adv =  self.ultima_acao_das_interacoes[1][indice]

		if(ultima_acao_adv > 0.5):
			self.acao_atual = 1 # Clássica cooperação
			return
		elif(ultima_acao_adv < 0.5):
			self.acao_atual = 0 # Clássica traição
			return
		else:
			self.acao_atual = 0.5 # Indiferença


	def salvarRecursosParaAEstrategia(self, adversario):
		indice =  self.ultima_acao_das_interacoes[0].index(adversario.id)
		self.ultima_acao_das_interacoes[1][indice] = adversario.acao_atual

# ================================================================
# === JOGADORES PARA AS ESTRATÉGIAS GENEROUS TIT-FOT-TAT =========
# 			Assume a última ação nebulosa do adversário
# ================================================================
class Tft_g(Jogador):
	def __init__(self):
		super().__init__()
		self.id = 'TFT-G'
		self.ultima_acao_das_interacoes = [[],[]] # Salvar última ação de cada adversário interagido
										# [[id_adv_1,...,id_adv_N], [acao_adv_1,...,acao_adv_1]]

	def determinarAcao(self, adversario, *args):
		if(adversario.id not in self.ultima_acao_das_interacoes[0]): # Se nunca interou com esse adversário
			self.ultima_acao_das_interacoes[0].append(adversario.id)
			self.ultima_acao_das_interacoes[1].append(1)			# Assume que a última ação dele foi C

		indice          =  self.ultima_acao_das_interacoes[0].index(adversario.id)
		ultima_acao_adv =  self.ultima_acao_das_interacoes[1][indice]

		self.acao_atual = ultima_acao_adv 	# Realiza a mesma última ação nebulosa do adversário


	def salvarRecursosParaAEstrategia(self, adversario):
		indice =  self.ultima_acao_das_interacoes[0].index(adversario.id)
		self.ultima_acao_das_interacoes[1][indice] = adversario.acao_atual

# ================================================================
# ============= JOGADORES PARA AS ESTRATÉGIAS PAVLOV =============
# Começa cooperando, e continua se na última interação com o adverário
# ocorrer CC ou DD, caso contrário, trai.
# ================================================================
class Pavlov(Jogador):
	def __init__(self):
		super().__init__()
		self.id = 'PAVLOV'
		self.ultima_acao_das_interacoes = [[],[]] # Salvar última ação de cada adversário interagido
												  # [[id_adv_1,...,id_adv_N], [[id_adv_1,self.acao1],[adv.acao2,self.acao2]...]]

	def determinarAcao(self, adversario, *args):
		if(adversario.id not in self.ultima_acao_das_interacoes[0]): # Se nunca interou com esse adversário
			self.ultima_acao_das_interacoes[0].append(adversario.id)
			self.ultima_acao_das_interacoes[1].append([1,1])		# Assume que a última ação dele foi CC

		indice          = self.ultima_acao_das_interacoes[0].index(adversario.id)
		ultima_acao_adv = self.ultima_acao_das_interacoes[1][indice][0]   # [[ids],[ações]] -> ações=[1,1],[0,1]...
		ultima_acao     = self.ultima_acao_das_interacoes[1][indice][1]

		if((ultima_acao == 1 and ultima_acao_adv > 0.5)		# CC
			or (ultima_acao == 0 and ultima_acao_adv < 0.5)):	# DD
			self.acao_atual = 1	 	# Cooperação clássica
			return
		if(ultima_acao_adv == 0.5):
			self.acao_atual = 0.5	# Indiferença
			return
		else: self.acao_atual = 0	 			# DC ou CD --> Traição clássica


	def salvarRecursosParaAEstrategia(self, adversario):
		indice = self.ultima_acao_das_interacoes[0].index(adversario.id)
		self.ultima_acao_das_interacoes[1][indice][0] = adversario.acao_atual   # [[ids],[ações]] -> ações=[1,1],[0,1]...
		self.ultima_acao_das_interacoes[1][indice][1] = self.acao_atual


# ================================================================
# ============= JOGADORES PARA AS ESTRATÉGIAS DE BORGES ==========
# ================================================================
class Borges(Jogador):
	def __init__(self, f1_estrategia, f2_estrategia, f3_estrategia):
		super().__init__()
		self.id = '{}{}{}'.format(str(f1_estrategia), str(f2_estrategia), str(f3_estrategia))
		self.f1 = FD.FatorDeDecisao(ESTRATEGIAS[f1_estrategia-1])
		self.f2 = FD.FatorDeDecisao(ESTRATEGIAS[f2_estrategia-1])
		self.f3 = FD.FatorDeDecisao(ESTRATEGIAS[f3_estrategia-1])


	def determinarAcao(self, adversario, grupo):
		#	=================== DETERMINANDO OS FATORES DE DECISÃO ========================
		self.f1.determinarF1(w1 = self.ganhos_acumulados, w2 = adversario.ganhos_acumulados)
		dados = grupo.interacoesEntreOsJogadores(self.id, adversario.id)
		self.f2.determinarF2(dados['qtd_interacoes'], dados['ganhos'])
		self.f3.determinarF3(wkr = self.ganho_medio, wn = grupo.media_de_ganhos)

		#	=================== FUZIFICANDO OS FATORES DE DECISÃO ========================
		self.f1.fuzificarTipo1()
		self.f2.fuzificarTipo2()
		self.f3.fuzificarTipo1()	# Mesma fuzificação de f1

		#	=================== ATIVANDO A REGRA DOS FATORES DE DECISÃO ========================
		self.f1.ativarRegra()
		self.f2.ativarRegra()
		self.f3.ativarRegra()

		self.determinarAcaoFinal()
		return(self.acao_atual)


	def determinarAcaoFinal(self):
		# DETERMINANDO AS CONCLUSÕES PARCIAIS (uC = max(valores de cooperacao entre os fatores
		#									   uD = max(valores de traicao entre os fatores)
		cooperacao = []
		traicao = []
		for f in [self.f1, self.f2, self.f3]:
			cooperacao.extend([valor for comportamento, valor in f.regra if comportamento == 1])
			traicao.extend([valor for comportamento, valor in f.regra if comportamento == 0])
		try: uc = max(cooperacao)
		except: uc = 0 	# Se não existir cooperação
		try: ud = max(traicao)
		except: ud = 0	# Se não existir traição
		# DETREMINANDO AÇÃO FINAL
		self.acao_atual  = round( ( ((1-ud)*ud + (1+uc)*uc) ) / (2*(uc+ud)) ,3)

	def resetarJogador(self):
		id_temp = self.id
		super().__init__()	# não reinicializar as estrategias
		self.id = id_temp

	