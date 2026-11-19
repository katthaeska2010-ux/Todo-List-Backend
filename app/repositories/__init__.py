"""Repositórios: a única camada que conversa com o banco de dados.

Antes, as consultas estavam escritas dentro das funções de rota. Isso
misturava três assuntos em uma função só - HTTP, regra de negócio e SQL - e
repetia o mesmo trecho de busca-ou-404 em quatro endpoints.

Com os repositórios, a regra passa a ser: serviço não sabe SQL, rota não sabe
banco. Quem precisa de dados pede a um repositório.
"""

from app.repositories.base import RepositorioBase
from app.repositories.tarefa import FiltroDeTarefas, PaginaDeTarefas, TarefaRepositorio
from app.repositories.usuarios import UsuarioRepositorio

__all__ =[
    "FiltroDeTarefas",
    "PaginaDeTarefas",
    "RepositorioBase",
    "TarefaRepositorio",
    "UsuarioRepositorio",
]