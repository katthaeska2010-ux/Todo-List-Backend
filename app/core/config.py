"""Configuração da aplicação, lida do ambiente (arquivo `.env`)."""
from __future__ import annotations
import os
from dataclasses import dataclass
from functools import lru_cache
from dotenv import load_dotenv
load_dotenv()
_ORIGENS_PADRAO = "http://localhost:5173,http://127.0.0.1:5173"

class ConfiguracaoInvalida(RuntimeError):
    """Falta (ou está errada) uma variável de ambiente obrigatória."""


@dataclass(frozen=True)
class Configuracao:
    """Parâmetros de execução da aplicação."""
    database_url: str = ""
    jwt_secret: str = ""
    jwt_expira_minutos: int = 120
    origens_permitidas: tuple[str, ...]= tuple(_ORIGENS_PADRAO.split(","))
    @classmethod
    def do_ambiente(cls) -> Configuracao:
        """Monta a configuração a partir das variáveis de ambiente."""
        origens = os.getenv("CORS_ORIGINS", _ORIGENS_PADRAO)
        return cls(
            database_url=os.getenv("DATABASE_URL", "").strip(),
            jwt_secret=os.getenv("JWT_SECRET", ""),
            jwt_expira_minutos=int(os.getenv("JWT_EXPIRA_MINUTOS", "120")),
            # "a, b, c," -> ("a", "b", "c",), ignorando itens vazios.
            origens_permitidas=tuple(
                origem.strip() for origem in origens.split(",") if origem.strip()
            ),
        )
    @property
    def url_banco(self) -> str:
        """URL de conexão usada pelo SQLAlchemy, lida de `DATABASE_URL`. """
        if not self.database_url:
            raise ConfiguracaoInvalida(
                "DATABASE_URL não definida. Copie o arquivo .env.example para .env "
                "e deixe ativo um dos dois caminhos: SQLite (local) ou PostgreSQL no Render."
            )
        return self.database_url
    def segredo_jwt(self) -> str:
        """Devolve o segredo que asina os tokens, ou explica como criá-lo."""
        if len(self.jwt_secret) < 32:
            raise ConfiguracaoInvalida(
                "JWT_SECRET ausente ou curto demais (mínimo 32 caracteres). "
                "Gere um com: python -c \"import secrets; print(secrets.token_hex(32))\" "
                "e coloque no arquivo .env."
            )
        return self.jwt_secret
@lru_cache
def obter_configuracao() -> Configuracao:
    """Devolve a configuração da aplicação, carregada uma única vez."""
    return Configuracao.do_ambiente()
    
