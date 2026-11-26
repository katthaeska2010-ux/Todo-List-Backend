"""Contrato JSON da página Analytics
 
Os quatro primeiros têm o mesmo nome e o mesmo formato que a
`AnalyticsPage` do front-end já calcula hoje - na integração, ela só troca a
fonte dos dados
"""
 
from datetime import date
 
from pydantic import Field
 
from app.models.enums import PrioridadeTarefa
from app.schemas.base import EsquemaDeSaida
 
class ConcluidasNoDia(EsquemaDeSaida):
    """Quantas tarefas foram concluídas em um dia"""
 
    dia: date
    quantidade: int
 
class AnalyticsOut(EsquemaDeSaida):
    """Análises das tarefas do usuário, calculadas com pandas"""
 
    total: int
    concluidas: int
    taxa_conclusao: int = Field(description="Percentual de concluídas, de 0 a 100")
    concluidas_na_janela:int = Field(description="Soma de `concluidasPorDia`")
    concluidas_por_dia: list[ConcluidasNoDia]
    pendentes_por_prioridade: dict[PrioridadeTarefa, int]
    tempo_medio_por_dia_da_semana: dict[str, int] = Field(
        description="Média de dias entre criar e concluir; `null` se nada foi concluído0"
    )
    concluidas_por_dia_da_semana: dict[str, int] = Field(
        description="Conclusões de todo o histórico por dia da semana, de `seg` a `dom`"
    )
    percentual_no_prazo: int | None = Field(
        description="Das concluídas que tinham prazo, % concluidas até o prazo; "
        "`null` se nenhuma tinha prazo"
    )
 
 