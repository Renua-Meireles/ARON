from PyQt5.QtCore import QThread, pyqtSignal

# from gerenciador_de_torneio import Torneio

class ThreadClass(QThread):
    atualizar_progresso = pyqtSignal(int)
    inserir_item_tabela = pyqtSignal(str,int,int)


    def __init__(self, parent=None):
        super(ThreadClass,self).__init__(parent)
        self.torneio_selecionado = False
        self.torneio = None

    def run(self):
        if not self.torneio_selecionado: 
            return
        self.torneio.iniciar(self.atualizar_progresso, self.inserir_item_tabela)
        self.torneio_selecionado = False
        # self.torneio = None