"""
Exemplo de integração entre SQLAlchemy e pgvector.

Configure a variável de ambiente `DATABASE_URL` com a string de conexão PostgreSQL.
Exemplo: postgresql://user:password@host:5432/dbname

Funções:
- create_tables(): cria a tabela `documents` se não existir
- upsert_document(id, text, embedding): insere ou atualiza documento com embedding (lista/tuple)
- nearest_neighbors(vector, limit=5): retorna os mais próximos usando operador `<->`
"""
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import declarative_base, Session
from pgvector.sqlalchemy import Vector
import os
from typing import Sequence, List, Tuple

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/dbname")

engine = create_engine(DATABASE_URL)
Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    # ajuste a dimensão conforme seu embedding (ex.: 1536)
    embedding = Column(Vector(1536))


def create_tables() -> None:
    """Cria as tabelas necessárias no banco."""
    Base.metadata.create_all(engine)


def upsert_document(doc_id: int, text: str, embedding: Sequence[float]) -> None:
    """Insere ou atualiza um documento com embedding.

    embedding: lista ou tupla de floats com a dimensão correta.
    """
    with Session(engine) as session:
        doc = Document(id=doc_id, text=text, embedding=list(embedding))
        session.merge(doc)
        session.commit()


def nearest_neighbors(vector: Sequence[float], limit: int = 5) -> List[Tuple[int, str, float]]:
    """Retorna (id, text, distance) dos `limit` documentos mais próximos.

    Usa operador `<->` do pgvector (distância euclidiana por padrão).
    """
    sql = text(
        "SELECT id, text, embedding <-> :vec AS distance "
        "FROM documents "
        "ORDER BY distance "
        "LIMIT :limit"
    )
    with Session(engine) as session:
        rows = session.execute(sql, {"vec": list(vector), "limit": limit}).all()
    return [(r.id, r.text, float(r.distance)) for r in rows]


if __name__ == "__main__":
    print("Arquivo de exemplo: ajuste DATABASE_URL e use as funções create_tables/upsert_document/nearest_neighbors.")
