# ================================================================
# CONTROLA OS FATORES DE DECISÃO INDIVIDUALMENTE, ASSIM COMO TODAS
# 					AS OPERAÇÕES NECESSÁRIAS.
# ================================================================
class FatorDeDecisao(object):
	def __init__(self, estrategia_de_comportamento):
		self.valor         = 0		# Armazenar o fator de decisão
		self.comportamento = estrategia_de_comportamento[:]		# S1 ou S2 ou ... ou S8
		self.grau          = [] 	# Armazenar o grau do fator fuzificado/ [ulw, usl, ugt] ou [up, uf, uh]

		self.regra         = []	# Armazenar a regra ativada pelo valor do fator
								# EX: f1.regra = [[1, 0.123], [0, 0.421], [0, 0]] -> [[Comportamento, valor], ...]
								# O comportamento de trair (0) ou cooperar (C) é ativado pela estratégia ulw, usl, ugt (para f1)
								# para regra[0]: comportamento 1-C, ou seja, coopera(0.123)
								# para regra[1]: comportamento 0-D, ou seja, trai(0.123)

	def determinarF1(self, w1,w2):
		if(not w1 and not w2):	self.valor = 0				# ---> CASO SEJA A PRIMEIRA INTERAÇÃO DOS DOIS
		else: 					self.valor = round(w1/(w1+w2),3)

	def determinarF2(self, qtd_interacoes, ganhos):
		if(qtd_interacoes == 0):	self.valor = 0.4
		elif(qtd_interacoes == 1):	self.valor = round(ganhos[0]/5,3)
		elif(qtd_interacoes == 2):
			termo_p1 = ganhos[0]/5
			termo_p2 = ganhos[1]/5
			self.valor = round((0.4*termo_p2) + (0.6*termo_p1),3)
		else:
			termo_p1 = ganhos[0]/5	# O ganho obtido na última interação contra o adversário
			termo_p2 = ganhos[1]/5	# O ganho obtido na Penúltima interação contra o adversário
			termo_p3 = ganhos[2]/5	# O ganho obtido na Ante-penúltima interação contra o adversário
			self.valor = round((0.1*termo_p3) + (0.3*termo_p2) + (0.6*termo_p1),3)

	def determinarF3(self, wkr, wn):
		if(not wn): self.valor = 0	# Se ainda não houveram disputas
		else: self.valor = round(wkr/(wkr+wn),3)

	#	DETERMINA OS GRAUS DO FATOR
	def fuzificarTipo1(self):	# A Mesma fuzificação para os fatores f1 e f3
		f = self.valor
		#	*** ulw ***
		if(0 <= f and f <= 0.5):  ulw = -2*f + 1
		else:                     ulw = 0
		#	*** usl ***
		if(0.44 <= f and f <= 0.5):    usl = (50/3)*f - 22/3
		elif(0.5 <= f and f <= 0.57):  usl = -(100/7)*f + 57/7
		else:                          usl = 0
		#	*** ugt ***
		if(0.55 <= f and f <= 1):  ugt = (20/9)*f - 11/9
		else:                      ugt = 0

		self.grau = [round(ulw,3), round(usl,3), round(ugt,3)]

	#	DETERMINA OS GRAUS DO FATOR
	def fuzificarTipo2(self):	# Fuzificação para o fator f2
		f = self.valor
		#	*** up ***
		if(0 <= f and f <= 0.4):  up = -2.5*f + 1
		else:                     up = 0
		#	*** uf ***
		if(0.2 <= f and f <= 0.4):    uf = 5*f - 1
		elif(0.4 <= f and f <= 0.6):  uf = -5*f + 3
		else:                         uf = 0
		#	*** uh ***
		if(0.4 <= f and f <= 1):  uh = (5/3)*f - 2/3
		else:                     uh = 0

		self.grau = [round(up,3), round(uf,3), round(uh,3)]

	def ativarRegra(self):
		# EX: f1.regra = [[1, 0.123], [0, 0.421], [0, 0]] -> [[Comportamento, valor], ...]
		# O comportamento de trair (0) ou cooperar (C) é ativado pela estratégia ulw, usl, ugt (para f1)
		# para regra[0]: comportamento 1-C, ou seja, coopera(0.123)
		# para regra[1]: comportamento 0-D, ou seja, trai(0.123)
		self.regra = [[self.comportamento[i], grau] \
						for i,grau in enumerate(self.grau) if grau]  # Percorrendo os graus [ulw, usl, ugt]

	def __repr__(self):
		return(str(self.valor))
	__str__=__repr__