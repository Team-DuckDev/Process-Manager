import sys
from PyQt6 import QtWidgets, uic
#from modules.buscador import BuscadorProcessos
#from modules.controlador import ControladorProcessos


import sys
from PyQt6 import QtWidgets, uic
#from modules.buscador import BuscadorProcessos
#from modules.controlador import ControladorProcessos

class GerenciadorApp(QtWidgets.QMainWindow):
    """"Classe Responsável por abri a janela principal e carregar o arquivo que mantém os dados da interface
    """
    def __init__(self):
        super().__init__()
        uic.loadUi("interface.ui", self)
        
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    janela = GerenciadorApp()
    janela.show()
    sys.exit(app.exec())