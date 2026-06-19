import os
import signal
import psutil


class ControladorProcessos:
    """
    Classe responsável por controlar processos do Linux.
    """

    def __init__(self):
        pass

    def obter_detalhes_processo(self, pid: int) -> dict:
        """
        Retorna informações detalhadas do processo.
        """
        try:
            proc = psutil.Process(pid)

            return {
                "pid": proc.pid,
                "nome": proc.name(),
                "nice": proc.nice(),
                "tempo_cpu": round(
                    sum(proc.cpu_times()[:2]), 2
                )
            }

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return {}

    def finalizar_processo(self, pid: int) -> bool:
        """
        Encerra definitivamente um processo.
        """
        try:
            os.kill(pid, signal.SIGKILL)
            return True
        except Exception:
            return False

    def bloquear_processo(self, pid: int) -> bool:
        """
        Suspende um processo.
        """
        try:
            os.kill(pid, signal.SIGSTOP)
            return True
        except Exception:
            return False

    def continuar_processo(self, pid: int) -> bool:
        """
        Retoma um processo suspenso.
        """
        try:
            os.kill(pid, signal.SIGCONT)
            return True
        except Exception:
            return False

    def reiniciar_processo(self, pid: int) -> bool:
        """
        Reinicia um processo utilizando o mesmo comando.
        """
        try:
            proc = psutil.Process(pid)

            comando = proc.cmdline()

            proc.kill()

            if comando:
                os.spawnvp(
                    os.P_NOWAIT,
                    comando[0],
                    comando
                )

            return True

        except Exception:
            return False

    def alterar_nice(self, pid: int, novo_nice: int) -> bool:
        """
        Altera a prioridade do processo.
        """
        try:
            proc = psutil.Process(pid)
            proc.nice(novo_nice)
            return True

        except (psutil.NoSuchProcess,
                psutil.AccessDenied):
            return False