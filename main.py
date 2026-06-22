import sys
from pathlib import Path
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QTableWidgetItem
from modules.buscador import BuscadorProcessos
from modules.controlador import ControladorProcessos


class GerenciadorApp(QtWidgets.QMainWindow):
    """Classe responsável por abrir a janela principal e carregar
    o arquivo que mantém os dados da interface."""

    def __init__(self):
        super().__init__()

        ui_path = Path(__file__).resolve().parent / "interface.ui"
        uic.loadUi(str(ui_path), self)

        self.buscador = BuscadorProcessos()
        self.controlador = ControladorProcessos()

        self.tabela_processos.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.carregar_usuarios()
        self.renderizar_tabela()

        self.botao_buscar.clicked.connect(self.renderizar_tabela)
        self.tabela_processos.cellClicked.connect(self.processo_selecionado)
        self.botao_finalizar.clicked.connect(self.finalizar_processo)
        self.botao_bloquear.clicked.connect(self.bloquear_processo)
        self.botao_continuar.clicked.connect(self.continuar_processo)
        self.botao_reiniciar.clicked.connect(self.reiniciar_processo)
        self.botao_executar.clicked.connect(self.executar_processo)
        self.botao_alterar_nice.clicked.connect(self.alterar_nice_processo)

    def carregar_usuarios(self):
        """Busca os usuários do SO."""
        self.box_usuario.clear()
        self.box_usuario.addItem("")

        lista_de_usuarios = self.buscador.obter_usuarios_do_sistema()
        self.box_usuario.addItems(lista_de_usuarios)

    def renderizar_tabela(self):
        """Função responsável por desenhar a tabela na tela."""
        self.tabela_processos.setRowCount(0)

        usuario_selecionado = self.box_usuario.currentText()
        termo_busca = self.line_busca_processo.text().strip()

        processos = self.buscador.obter_todos_processos(
            usuario_selecionado,
            termo_busca,
        )

        if processos is None:
            processos = []

        self.line_cpu_global.setText(f"{self.buscador.obter_uso_global_cpu():.1f}%")
        self.line_ram_global.setText(f"{self.buscador.obter_uso_global_ram():.1f}%")

        for proc in processos:
            linha_atual = self.tabela_processos.rowCount()
            self.tabela_processos.insertRow(linha_atual)

            self.tabela_processos.setItem(
                linha_atual, 0, QTableWidgetItem(str(proc["pid"]))
            )
            self.tabela_processos.setItem(
                linha_atual, 1, QTableWidgetItem(str(proc["name"]))
            )
            self.tabela_processos.setItem(
                linha_atual, 2, QTableWidgetItem(str(proc["user"]))
            )
            self.tabela_processos.setItem(
                linha_atual, 3, QTableWidgetItem(str(proc["status"]))
            )
            self.tabela_processos.setItem(
                linha_atual, 4, QTableWidgetItem(str(proc["cpu"]))
            )
            self.tabela_processos.setItem(
                linha_atual, 5, QTableWidgetItem(str(proc["ram"]))
            )

    def processo_selecionado(self, linha, coluna):
        """Função dispara quando o usuário clica em um processo da tabela."""
        try:
            item_pid = self.tabela_processos.item(linha, 0)
            if not item_pid:
                return

            pid = int(item_pid.text())
            detalhes = self.buscador.obter_detalhes_do_processo(pid)

            self.line_nice.setText(str(detalhes["nice"]))
            self.line_time.setText(str(detalhes["time"]))
            self.line_cpu.setText(str(detalhes["cpu"]))
            self.line_ram.setText(str(detalhes["ram"]))
            self.line_nice_atualizar.setText(str(detalhes["nice"]))
        except Exception as e:
            print(f"[ERRO] Falha ao carregar detalhes do processo: {e}")

    def executar_processo(self):
        comando = self.line_comando.text().strip()
        if not comando:
            return

        nice_text = self.line_nice_execucao.text().strip()
        novo_nice = None
        if nice_text:
            try:
                novo_nice = int(nice_text)
            except ValueError:
                novo_nice = None

        self.controlador.executar_processo(comando, novo_nice)
        self.renderizar_tabela()

    def alterar_nice_processo(self):
        pid = self.obter_pid_selecionado()
        if pid is None:
            return

        novo_nice_text = self.line_nice_atualizar.text().strip()
        if not novo_nice_text:
            return

        try:
            novo_nice = int(novo_nice_text)
        except ValueError:
            return

        self.controlador.alterar_nice(pid, novo_nice)
        self.renderizar_tabela()

    def obter_pid_selecionado(self):
        linha = self.tabela_processos.currentRow()
        if linha < 0:
            return None

        item = self.tabela_processos.item(linha, 0)
        if item is None:
            return None

        return int(item.text())

    def finalizar_processo(self):
        pid = self.obter_pid_selecionado()
        if pid is not None:
            self.controlador.finalizar_processo(pid)
        self.renderizar_tabela()

    def bloquear_processo(self):
        pid = self.obter_pid_selecionado()
        if pid is not None:
            self.controlador.bloquear_processo(pid)
        self.renderizar_tabela()

    def continuar_processo(self):
        pid = self.obter_pid_selecionado()
        if pid is not None:
            self.controlador.continuar_processo(pid)
        self.renderizar_tabela()

    def reiniciar_processo(self):
        pid = self.obter_pid_selecionado()
        if pid is not None:
            self.controlador.reiniciar_processo(pid)
        self.renderizar_tabela()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    janela = GerenciadorApp()
    janela.show()
    sys.exit(app.exec())
