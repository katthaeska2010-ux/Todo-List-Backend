"""Modelos de domínio: as entidades do sistema, com seus dados e suas regras.
 
Antes desta refaratoração, estas classes eram apenas listas de colunas - o que
se chama de *modelo anêmico*: dado sem comportamento. As regras de negócio
viviam dentro das funções da rota, de modo que a mesma regra podia ser
reescrita de forma diferente em cada em cada endpoint que a tocasse.
 
Agora cada entidade é responsável por manter o próprio estado válido: A regra
RN-03, por exemplo, não está em nenhuma rota: ela está nos métodos `concluir`
e `reabrir` da `Tarefa`, que são o único caminho possível para mudar o status
"""
 
# Importar as entidades aqui registra as tabelas no SQLalchemy (é o que
# `criar tabelas()` e usa) e permite escrever `from app.models import Usuário`.
from app.models.tarefa import Tarefa
from app.models.usuario import Usuario
 
__all__ = ["Tarefa", "Usuario"]