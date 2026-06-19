import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QTableWidgetItem
from modules.buscador import BuscadorProcessos
#from modules.controlador import ControladorProcessos


class GerenciadorApp(QtWidgets.QMainWindow):
    """"Classe Responsável por abri a janela principal e carregar
    o arquivo que mantém os dados da interface.
    """
    def __init__(self):
        super().__init__()
        uic.loadUi("interface.ui", self)

        self.buscador = BuscadorProcessos()

        self.tabela_processos.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        self.carregar_usuarios()

        self.botao_buscar.clicked.connect(self.renderizar_tabela)

    def carregar_usuarios(self):
        """Busca os usuários do SO"""
        self.box_usuario.clear()

        self.box_usuario.addItem("")

        lista_de_usuarios = self.buscador.obter_usuarios_do_sistema()

        self.box_usuario.addItems(lista_de_usuarios)

    def renderizar_tabela(self):
        """Função responsável por desenhar a tabela na tela"""
        self.tabela_processos.setRowCount(0)

        usuario_selecionado = self.box_usuario.currentText()

        processos = self.buscador.obter_todos_processos(usuario_selecionado)

        if processos is None:
            processos = []
        for proc in processos:
            linha_atual = self.tabela_processos.rowCount()
            self.tabela_processos.insertRow(linha_atual)

            self.tabela_processos.setItem(linha_atual, 0, QTableWidgetItem(str(proc['pid'])))
            self.tabela_processos.setItem(linha_atual, 1, QTableWidgetItem(str(proc['name'])))
            self.tabela_processos.setItem(linha_atual, 2, QTableWidgetItem(str(proc['user'])))
            self.tabela_processos.setItem(linha_atual, 3, QTableWidgetItem(str(proc['status'])))
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    janela = GerenciadorApp()
    janela.show()
    sys.exit(app.exec())