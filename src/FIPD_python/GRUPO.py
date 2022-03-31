from random import sample			# Utilizado para selecionar jogadores para interagir

class Grupo(object):
	contador = 1
	fase = 1
	def __init__(self, jogadores):
		self.__class__.gerarId(self)
		self.jogadores             = jogadores
		self.interacoes            = []	# Contém informações de ganhos das interações para o cálculo de f2
		self.ganhos_acumulados     = 0
		self.qtd_interacoes        = 0
		self.media_de_ganhos       = 0
		self.encontros             = [] # Contém todos os pares de jogadores que irão interar entre si
										# [[j1,j2],[j1,j2],...] len = qtd_interacoes
		for jogador in jogadores: jogador.grupo = str(self.id)

	def realizarInteracoes(self, qtd_interacoes, signal_progresso, passo_da_barra, progresso):
		self.gerarEncontros(qtd_interacoes)
		for j1,j2 in self.encontros:
			self.interagir(j1,j2)				# Interação entre os jogadores selecionados j1,j2
			# Atualizando A barra de Progresso
			progresso += passo_da_barra
			signal_progresso.emit(int(progresso))
			
	def gerarEncontros(self, qtd_interacoes):
		j = [i for i in range(19)] # indice dos 19 jogadores do grupos (16 fuzzy + tft,tft-g,pavlov)
		for i in range(qtd_interacoes):	# Realizar a quantidade de interações do torneio
			inds = sorted(sample(j,2))	# mais rápido ordenar dois inteiros do que dois jogadores pelo indice str
			self.encontros.append([self.jogadores[inds[0]], self.jogadores[inds[1]]]) # append([j1,j2])

	def interagir(self, j1, j2):
		j1.determinarAcao(j2, self)
		j2.determinarAcao(j1, self)
		j1.determinarPagamento(j2)
		j2.determinarPagamento(j1)

		j1.registrarValores(j2)
		j2.registrarValores(j1)
		self.atualizarDados(j1, j2)

	def atualizarDados(self,j1, j2):
		self.interacoes.append({'jogadores':  [j1.id, j2.id],
								'acoes':	  [j1.acao_atual, j2.acao_atual],
								'pagamentos': [j1.pagamento_atual, j2.pagamento_atual]
								})
		self.qtd_interacoes    += 1
		self.ganhos_acumulados += j1.pagamento_atual
		self.ganhos_acumulados += j2.pagamento_atual
		self.media_de_ganhos   = self.ganhos_acumulados /(2*self.qtd_interacoes) # Média de ganhos por disputa do ambiente

	# Coletando dados de até 3 interações anteriores entre os jogadores para a definição do fator de decição 2
	def interacoesEntreOsJogadores(self, id_jogador, id_adversario):
		# Retorna um dicionário contendo a quantidade de interacoes do jogador contra o adversario (no máx. 3)
		# e com os ganhos nas respectivas última, penúltima e ante-penúltima disputas
		dados = {'qtd_interacoes':0,
				 'ganhos':[]
				 }
		for inter in reversed(self.interacoes):
			j1,j2 = inter['jogadores'][0], inter['jogadores'][1]
			if((id_jogador == j1) and (id_adversario == j2)):
				dados['qtd_interacoes']+=1
				dados['ganhos'].append(inter['pagamentos'][0])
			elif((id_jogador == j2) and (id_adversario == j1)):
				dados['qtd_interacoes']+=1
				dados['ganhos'].append(inter['pagamentos'][1])
			if(dados['qtd_interacoes'] == 3): break 	# Só precisa de no máximo 3 interacoes anteriores

		return(dados.copy()) # dados['ganhos'] = [ganho da última, ganho da penúltima, ganho da ante-última]
		
	def vencedor(self):
		self.rankearJogadores()
		return(self.jogadores[0])

	# Rankeando jogadores por ganho médio
	def rankearJogadores(self):
		self.jogadores.sort(key= lambda x: x.ganho_medio, reverse=True)

	# Selecionando os melhores 16 jogadores nebulosos do grupo.
	def selecionarMelhores16(self):
		i = 0
		n = 3
		while(n>0):
			if(	self.jogadores[i].id=='TFT'
				or self.jogadores[i].id=='TFT-G'
				or self.jogadores[i].id=='PAVLOV'):
				self.jogadores.pop(i)
				n-=1
			else: i+=1	# Se não for tft,tftg ou pavlov, verifica o próximo
		return(self.jogadores[:])


	@classmethod
	def gerarId(cls, grupo):
		fase,contador = cls.fase, cls.contador
		if(	   (fase == 1 and contador > 32)
			or (fase == 2 and contador > 11)
			or (fase == 3 and contador > 5)):
			cls.fase += 1
			cls.contador = 1
		grupo.id = '{}.{}'.format(str(cls.fase), str(cls.contador)) if cls.contador>9 else '{}.0{}'.format(str(cls.fase), str(cls.contador))
		cls.contador    += 1

	@classmethod
	def resetarContadores(cls):
		cls.fase = 1
		cls.contador = 1