from random import seed
seed(1408)

from PyQt5 import QtWidgets

from compilar_interface import compilar
compilar('src/interface.ui')
import interface

from thread_class import ThreadClass

import gerenciador_de_torneio as Torneios

from xlwt import Workbook

class MainUIClass(QtWidgets.QMainWindow,interface.Ui_MainWindow):
    def __init__(self,parent=None):
        super(MainUIClass,self).__init__(parent)
        self.setupUi(self)

        self.selecao_torneio_personalizado = []
        self.filtro_torneios = ['Selecionar Torneio','Primeiro Torneio de Axelrod','Segundo Torneio de Axelrod','Torneio de Aniversáio de 20 Anos','Torneio Knight','Torneio Nebuloso de Borges']
        self.filtro_classificacao = ['Selecionar Classificação','Reativo Simples','Baseado em Modelo','Baseado em Objetivo','Baseado em Utilidade','Com Aprendizado']

        self.threaded_class = ThreadClass()
        self.configurarComportamentos()
        self.listarEstrategias()
        self.personalizarConfigs()

    def configurarComportamentos(self):
        # ====== MENU DE TORNEIOS PERSONALIZADOS ======
        self.pushButtonAdicionarEstrategia.clicked.connect(self.adicionarItem)
        self.pushButtonRemoverEstrategia.clicked.connect(self.removerItem)
        self.comboBoxFiltro1.currentIndexChanged.connect(self.atualizarFiltro2)
        self.comboBoxFiltro2.currentIndexChanged.connect(self.listarEstrategias)
        self.pushButtonIniciarTorneioPersonalizado.clicked.connect(self.iniciarTorneio)

        # ====== MENU DE TORNEIOS ANTERIORES ======
        # ----> Thread <-----
        self.threaded_class.atualizar_progresso.connect(self.progressBarSimulacao.setValue)
        self.threaded_class.inserir_item_tabela.connect(self.inserirItemNaTabela)
        self.threaded_class.finished.connect(self.desbloquearLayout)

        # ----> Botões <-----
        self.pushButtonSimularTorneio2.clicked.connect(self.threaded_class.start)
        self.pushButtonSimularTorneio2.clicked.connect(self.ressimularTorneio)
        self.pushButtonCancelarSimulacao.clicked.connect(self.cancelarThread)

        # ----> MenuCascade <-----
        self.actionSair.triggered.connect(exit)

        # ----> ComboBox <-----
        self.comboBoxSelecionarTorneio.currentIndexChanged.connect(self.personalizarConfigs)

        # ----> TabWidget <-----
        self.TableResultados.resizeColumnsToContents()
        self.pushButtonLimpar.clicked.connect(self.limparTabelaResutados)

        self.pushButtonSalvar.clicked.connect(self.salvarResultados)

    # =====================================================================
    # ============= FUNÇÕES DO MENU DE TORNEIO PERSONALIZADO ==============
    # =====================================================================
    def iniciarTorneio(self):
        t, r, p, s, turnos, _ = self.carregarValoresConfigurados(1)
        print('t:{} r:{} p:{} s:{} Turnos:{}'.format(t, r, p, s, turnos))
        strats = []
        for i in range(self.listWidgetEstrategiasSelecionadas.count()):
            name = self.listWidgetEstrategiasSelecionadas.item(i).text()
            strat = Torneios.estrategias_todas[name]()
            strats.append(strat)
            
        t = Torneios.RoundRobin(t=t, r=r, p=p, s=s, turnos=turnos)
        t.jogadores = strats
        self.threaded_class.torneio = t

        self.limparTabelaResutados()
        self.toolBox.setEnabled(False)
        self.pushButtonCancelarSimulacao.setEnabled(True)
        self.pushButtonSimularTorneio2.setText('Simulando...')
        self.threaded_class.torneio_selecionado = True
        self.threaded_class.start()

    def atualizarFiltro2(self):
        indice = self.comboBoxFiltro1.currentIndex()
        self.comboBoxFiltro2.clear()

        if indice == 0:
            self.comboBoxFiltro2.setEnabled(False)
            self.listarEstrategias()

        elif indice == 1:
            self.comboBoxFiltro2.setEnabled(True)
            self.comboBoxFiltro2.addItems(self.filtro_torneios)
        elif indice == 2:
            self.comboBoxFiltro2.setEnabled(True)
            self.comboBoxFiltro2.addItems(self.filtro_classificacao)

    def listarEstrategias(self):
        self.listWidgetEstrategias.clear()
        estrategias = Torneios.estrategias_todas
        indice = self.comboBoxFiltro2.currentIndex()
        if indice == 0: estrategias = Torneios.estrategias_todas
        elif indice == 1:
            estrategias = Torneios.estrategias_torneioAxel1 if self.comboBoxFiltro1.currentIndex()==1 else Torneios.reativo_simples
        elif indice == 2:
            estrategias = Torneios.estrategias_torneioAxel2 if self.comboBoxFiltro1.currentIndex()==1 else Torneios.baseado_em_modelo
        elif indice == 3:
            estrategias = Torneios.estrategias_torneio20Anos if self.comboBoxFiltro1.currentIndex()==1 else Torneios.baseado_em_objetivo
        elif indice == 4:
            estrategias = Torneios.estrategias_torneioKnight if self.comboBoxFiltro1.currentIndex()==1 else Torneios.baseado_em_utilidade
        elif indice == 5:
            estrategias = Torneios.estrategias_torneioBorges if self.comboBoxFiltro1.currentIndex()==1 else Torneios.com_aprendizado
        for name in estrategias.keys():
            # if name not in self.selecao_torneio_personalizado:
            self.listWidgetEstrategias.addItem(name)


    def adicionarItem(self):
        try:
            indice = self.listWidgetEstrategias.selectedIndexes()[0].row()
            nome = self.listWidgetEstrategias.item(indice).text()
            self.selecao_torneio_personalizado.append(nome)
            if len(self.selecao_torneio_personalizado) >=2\
            and not self.pushButtonIniciarTorneioPersonalizado.isEnabled():
                self.pushButtonIniciarTorneioPersonalizado.setEnabled(True)
            self.listWidgetEstrategiasSelecionadas.addItem(nome)
        except IndexError: pass

    def removerItem(self):
        try:
            indice = self.listWidgetEstrategiasSelecionadas.selectedIndexes()[0].row()
            nome = self.listWidgetEstrategiasSelecionadas.takeItem(indice).text()
            self.selecao_torneio_personalizado.remove(nome)
            if len(self.selecao_torneio_personalizado) <2\
            and self.pushButtonIniciarTorneioPersonalizado.isEnabled():
                self.pushButtonIniciarTorneioPersonalizado.setEnabled(False)
            self.listWidgetEstrategias.addItem(nome)
        except IndexError: pass

    # =====================================================================
    # ============== FUNÇÕES DO MENU DE TORNEIOS ANTERIORES ===============
    # =====================================================================
    def ressimularTorneio(self):
        indice = self.comboBoxSelecionarTorneio.currentIndex()
        if indice == 3 or indice == 4:
            return
        t, r, p, s, turnos, interacoes = self.carregarValoresConfigurados(2)
        if indice == 1: self.threaded_class.torneio = Torneios.Axelrod1(t=t, r=r, p=p, s=s, turnos=turnos)
        if indice == 2: self.threaded_class.torneio = Torneios.Axelrod2(t=t, r=r, p=p, s=s, turnos=turnos)
        if indice == 3: self.threaded_class.torneio = Torneios.Aniversario20Anos(t=t, r=r, p=p, s=s, turnos=turnos)
        if indice == 4: self.threaded_class.torneio = Torneios.Knight(t=t, r=r, p=p, s=s, turnos=turnos)
        if indice == 5: self.threaded_class.torneio = Torneios.Borges(qtd_de_interacoes = interacoes)
        if self.threaded_class.torneio:
            self.limparTabelaResutados()
            self.toolBox.setEnabled(False)
            self.pushButtonCancelarSimulacao.setEnabled(True)
            self.pushButtonSimularTorneio2.setText('Simulando...')
            self.threaded_class.torneio_selecionado = True
            self.threaded_class.start()


    def inserirItemNaTabela(self, texto, linha, coluna):
        if linha != self.TableResultados.currentRow():
            self.TableResultados.insertRow(linha)
            self.TableResultados.selectRow(linha)
        centralizado = 4
        item = None
        item = QtWidgets.QTableWidgetItem()
        item.setText(texto)
        item.setTextAlignment(centralizado)
        self.TableResultados.setItem(linha,coluna,item)

    def desbloquearLayout(self):
        if self.progressBarSimulacao.value() == 0 \
        or self.progressBarSimulacao.value() == 100:
            self.pushButtonLimpar.setEnabled(True)
            self.pushButtonSalvar.setEnabled(True)
        self.threaded_class.torneio_selecionado = False
        self.pushButtonSimularTorneio2.setText('Iniciar Simulação')
        self.toolBox.setEnabled(True)
        self.pushButtonCancelarSimulacao.setEnabled(False)
        self.TableResultados.resizeColumnsToContents()
        self.TableResultados.resizeRowsToContents()

    def cancelarThread(self,val):
        self.threaded_class.torneio_selecionado = False
        self.threaded_class.torneio.cancelar_torneio = True


    def personalizarConfigs(self):
        indice = self.comboBoxSelecionarTorneio.currentIndex()
        if indice == 0:
            self.pushButtonSimularTorneio2.setEnabled(False)
            self.widgetPersonalizarConfiguracoes2.setEnabled(False)

        if indice >= 1:
            self.pushButtonSimularTorneio2.setEnabled(True)					# Ativa o botão
            self.widgetPersonalizarConfiguracoes2.setEnabled(True)	# Ativa as Configurações
            self.widgetPayoff2.setEnabled(True)				# Ativa a tabela de pagamento
            # self.widgetTurnos2.setEnabled(True)				# Ativa os turnos
            self.resetarInteracoes()
            self.widgetQuantidadeInteracoes2.setEnabled(False)	# desativa a Quantidade total de interações

        if indice == 5:
            self.resetarPayoff()
            self.resetarTurnos()
            self.widgetPayoff2.setEnabled(False)				# Desativa a tabela de pagamento
            # self.widgetTurnos2.setEnabled(False)				# Desativa os turnos
            self.widgetQuantidadeInteracoes2.setEnabled(True)	# Ativa a Quantidade total de interações

    def limparTabelaResutados(self):
        self.pushButtonLimpar.setEnabled(False)
        self.pushButtonSalvar.setEnabled(False)
        self.TableResultados.clearContents()
        while self.TableResultados.rowCount()>0:
            self.TableResultados.removeRow(0)

    def resetarPayoff(self):
        self.spinBoxT2.setValue(5)
        self.spinBoxR2.setValue(3)
        self.spinBoxP2.setValue(1)
        self.spinBoxS2.setValue(0)

    def resetarTurnos(self):
        self.spinBoxTurnos2.setValue(200)

    def resetarInteracoes(self):
        self.spinBoxQuantidadeInteracoest2.setValue(30000)

    def carregarValoresConfigurados(self,i):
        t          = self.spinBoxT2.value() if i == 2 else self.spinBoxT1.value()
        r          = self.spinBoxR2.value() if i == 2 else self.spinBoxR1.value()
        p          = self.spinBoxP2.value() if i == 2 else self.spinBoxP1.value()
        s          = self.spinBoxS2.value() if i == 2 else self.spinBoxS1.value()
        turnos     = self.spinBoxTurnos2.value()  if i == 2 else self.spinBoxTurnos1.value()
        interacoes = self.spinBoxQuantidadeInteracoest2.value() if i==2 else None

        return t,r,p,s,turnos,interacoes

    def salvarResultados(self):
        # opcoes = QtWidgets.QFileDialog.options()
        nome_arquivo, tipo = QtWidgets.QFileDialog.getSaveFileName(self,'Salvar Dados','','Arquivos Excel (*.xls);;')
        if not nome_arquivo: return
        xlsx = Workbook(encoding='utf-8')
        planilha = xlsx.add_sheet('Resultados')
        self.threaded_class.torneio.salvarXlsx(planilha)
        xlsx.save(nome_arquivo)


def main():
    app = QtWidgets.QApplication([])
    self = MainUIClass()
    self.show()
    app.exec()


if __name__== '__main__':
    main()