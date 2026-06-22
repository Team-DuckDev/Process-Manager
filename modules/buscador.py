import psutil
import pwd


class BuscadorProcessos:
    """Classe responsável por interagir com o Linux para coletar
    dados sobre os processos do sistema"""
    
    def __init__(self):
        pass

    def obter_todos_processos(self, usuario_filtro: str = "", termo_busca: str = "") -> list:
        """Varre o SO e retorna uma lista de dicionários contendo
        os dados dos processos. Permite filtragem opcional por usuário."""

        lista_de_processos = []

        for proc in psutil.process_iter(['pid', 'name', 'username', 'status', 'cpu_percent', 'memory_percent']):
            try:
                info = proc.info

                if usuario_filtro and info['username'] != usuario_filtro:
                    continue

                if termo_busca and termo_busca.lower() not in info['name'].lower():
                    continue

                lista_de_processos.append({
                    "pid": info['pid'],
                    "name": info['name'],
                    "user": info['username'],
                    "status": info['status'],
                    # AJUSTE AQUI: Adicionado o ponto (.) antes do 1f e o % na RAM
                    "cpu": f"{proc.cpu_percent(interval=None):.1f}%",
                    "ram": f"{proc.memory_percent():.1f}%"
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        lista_ordenada = sorted(
            lista_de_processos,
            key = lambda proc: (proc['status'] != 'running', proc['name'].lower())
        )

        # CORREÇÃO AQUI: Retornar a lista ordenada, não a original!
        return lista_ordenada
    
    def obter_detalhes_do_processo(self, pid: int) -> dict:
        """Busca métricas avançadas de um PID específico."""
        try:
            proc = psutil.Process(pid)
            nice_atual = proc.nice()

            tempo_segundos = proc.cpu_times().user
            tempo_formatado = f"{int(tempo_segundos // 60)}m {int(tempo_segundos % 60)}s"

            cpu_percent = proc.cpu_percent(interval=0.1)
            ram_percent = proc.memory_percent()

            return {
                "nice": nice_atual,
                "time": tempo_formatado,
                "cpu": f"{cpu_percent:.1f}%",
                "ram": f"{ram_percent:.1f}%"
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return {"nice": "N/A", "time": "N/A", "cpu": "N/A", "ram": "N/A"}
    
    def obter_usuarios_do_sistema(self) -> list:
        """Lê o sistema Linux e retorna uma lista com
        o nome de todos os usuários cadastrados no SO."""

        usuarios = []

        for usuario in pwd.getpwall():
            if usuario.pw_uid >= 1000 or usuario.pw_name == "root":
                usuarios.append(usuario.pw_name)
        
        return sorted(usuarios)
    
    def obter_uso_global_cpu(self) -> float:
        """Retorna a porcentagem total de uso da CPU do computador"""
        return psutil.cpu_percent(interval=None)
    
    def obter_uso_global_ram(self) -> float:
        """Retorna a porcentagem total de uso da Memória RAM física do computador"""
        return psutil.virtual_memory().percent
