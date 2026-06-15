import psutil
import pwd


class BuscadorProcessos:
    """Classe responsável por interagir com o Linux para coletar
    dados sobre os processos do sistema"""
    
    def __init__(self):
        pass

    def obter_todos_processos(self, usuario_filtro: str = "") -> list:
        """Varre o SO e retorna uma lista de dicionários contendo
        os dados dos processos. Permite filtragem opcional por usuário."""

        lista_de_processos = []

        for proc in psutil.process_iter(['pid', 'name', 'username', 'status']):
            try:
                info = proc.info

                if usuario_filtro and info ['username'] != usuario_filtro:
                    continue

                lista_de_processos.append({
                    "pid": info['pid'],
                    "name": info['name'],
                    "user": info['username'],
                    "status": info['status']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        lista_ordenada = sorted(
            lista_de_processos,
            key = lambda proc: (proc['status'] != 'running', proc['name'].lower())
        )

        return lista_de_processos
    
    def obter_usuarios_do_sistema(self) -> list:
        """Lê o sistema Linux e retorna uma lista com
        o nome de todos os usuários cadastrados no SO."""

        usuarios = []

        for usuario in pwd.getpwall():
            if usuario.pw_uid >= 1000 or usuario.pw_name == "root":
                usuarios.append(usuario.pw_name)
        
        return sorted(usuarios)