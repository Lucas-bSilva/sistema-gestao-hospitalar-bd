from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Boolean,
    CHAR,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hospital_yuska.modelos.base import Base


class Pessoa(Base):
    __tablename__ = "pessoa"

    id_pessoa: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    nome: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    cpf: Mapped[str] = mapped_column(
        CHAR(11),
        nullable=False,
        unique=True,
    )

    data_nascimento: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    is_flamengo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    telefone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    paciente: Mapped[Paciente | None] = relationship(
        back_populates="pessoa",
        uselist=False,
    )

    profissional: Mapped[Profissional | None] = relationship(
        back_populates="pessoa",
        uselist=False,
    )


class Paciente(Base):
    __tablename__ = "paciente"

    id_pessoa: Mapped[int] = mapped_column(
        ForeignKey(
            "pessoa.id_pessoa",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    num_convenio: Mapped[str | None] = mapped_column(
        String(40),
        unique=True,
    )

    alergias: Mapped[str | None] = mapped_column(Text)

    grupo_sanguineo: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    endereco: Mapped[str | None] = mapped_column(
        String(180)
    )

    pessoa: Mapped[Pessoa] = relationship(
        back_populates="paciente"
    )

    atendimentos: Mapped[list[Atendimento]] = relationship(
        back_populates="paciente"
    )

    internacoes: Mapped[list[Internacao]] = relationship(
        back_populates="paciente"
    )


class Profissional(Base):
    __tablename__ = "profissional"

    id_pessoa: Mapped[int] = mapped_column(
        ForeignKey(
            "pessoa.id_pessoa",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    crm: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
    )

    data_admissao: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    especialidade: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )

    pessoa: Mapped[Pessoa] = relationship(
        back_populates="profissional"
    )

    residente: Mapped[Residente | None] = relationship(
        back_populates="profissional",
        uselist=False,
    )

    preceptor: Mapped[Preceptor | None] = relationship(
        back_populates="profissional",
        uselist=False,
    )


class Residente(Base):
    __tablename__ = "residente"

    id_profissional: Mapped[int] = mapped_column(
        ForeignKey(
            "profissional.id_pessoa",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    ano_residencia: Mapped[str] = mapped_column(
        String(2),
        nullable=False,
    )

    profissional: Mapped[Profissional] = relationship(
        back_populates="residente"
    )

    atendimentos: Mapped[list[Atendimento]] = relationship(
        back_populates="residente",
        foreign_keys="Atendimento.id_residente",
    )

    escalas: Mapped[list[Escala]] = relationship(
        back_populates="residente",
        foreign_keys="Escala.id_residente",
    )


class Preceptor(Base):
    __tablename__ = "preceptor"

    id_profissional: Mapped[int] = mapped_column(
        ForeignKey(
            "profissional.id_pessoa",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    titulacao: Mapped[str] = mapped_column(
        String(60),
        nullable=False,
    )

    profissional: Mapped[Profissional] = relationship(
        back_populates="preceptor"
    )

    atendimentos: Mapped[list[Atendimento]] = relationship(
        back_populates="preceptor",
        foreign_keys="Atendimento.id_preceptor",
    )

    escalas: Mapped[list[Escala]] = relationship(
        back_populates="preceptor",
        foreign_keys="Escala.id_preceptor",
    )


class Unidade(Base):
    __tablename__ = "unidade"

    id_unidade: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    nome: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        unique=True,
    )

    tipo: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    capacidade_leitos: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    atendimentos: Mapped[list[Atendimento]] = relationship(
        back_populates="unidade"
    )

    escalas: Mapped[list[Escala]] = relationship(
        back_populates="unidade"
    )

    internacoes: Mapped[list[Internacao]] = relationship(
        back_populates="unidade"
    )


class Atendimento(Base):
    __tablename__ = "atendimento"

    id_atendimento: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    data_hora: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    duracao_minutos: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    id_paciente: Mapped[int] = mapped_column(
        ForeignKey(
            "paciente.id_pessoa",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    id_residente: Mapped[int] = mapped_column(
        ForeignKey(
            "residente.id_profissional",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    id_preceptor: Mapped[int] = mapped_column(
        ForeignKey(
            "preceptor.id_profissional",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    id_unidade: Mapped[int] = mapped_column(
        ForeignKey(
            "unidade.id_unidade",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    paciente: Mapped[Paciente] = relationship(
        back_populates="atendimentos"
    )

    residente: Mapped[Residente] = relationship(
        back_populates="atendimentos",
        foreign_keys=[id_residente],
    )

    preceptor: Mapped[Preceptor] = relationship(
        back_populates="atendimentos",
        foreign_keys=[id_preceptor],
    )

    unidade: Mapped[Unidade] = relationship(
        back_populates="atendimentos"
    )

    procedimentos_realizados: Mapped[
        list[ProcedimentoRealizado]
    ] = relationship(
        back_populates="atendimento",
        cascade="all, delete-orphan",
    )


class Procedimento(Base):
    __tablename__ = "procedimento"

    id_procedimento: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    codigo: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    tempo_medio_minutos: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    nivel_risco: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="BAIXO",
    )

    media_tempo_procedimento: Mapped[
        Decimal | None
    ] = mapped_column(
        Numeric(10, 2)
    )

    realizacoes: Mapped[
        list[ProcedimentoRealizado]
    ] = relationship(
        back_populates="procedimento"
    )


class ProcedimentoRealizado(Base):
    __tablename__ = "procedimento_realizado"

    id_atendimento: Mapped[int] = mapped_column(
        ForeignKey(
            "atendimento.id_atendimento",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    id_procedimento: Mapped[int] = mapped_column(
        ForeignKey(
            "procedimento.id_procedimento",
            ondelete="RESTRICT",
        ),
        primary_key=True,
    )

    quantidade: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    tempo_real_minutos: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    observacao: Mapped[str | None] = mapped_column(Text)

    faturado: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    data_hora_inicio: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    atendimento: Mapped[Atendimento] = relationship(
        back_populates="procedimentos_realizados"
    )

    procedimento: Mapped[Procedimento] = relationship(
        back_populates="realizacoes"
    )


class Escala(Base):
    __tablename__ = "escala"

    id_escala: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    id_unidade: Mapped[int] = mapped_column(
        ForeignKey(
            "unidade.id_unidade",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    data_plantao: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    dia_semana: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    turno: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    id_residente: Mapped[int] = mapped_column(
        ForeignKey(
            "residente.id_profissional",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    id_preceptor: Mapped[int] = mapped_column(
        ForeignKey(
            "preceptor.id_profissional",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    supervisao_ativa: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    unidade: Mapped[Unidade] = relationship(
        back_populates="escalas"
    )

    residente: Mapped[Residente] = relationship(
        back_populates="escalas",
        foreign_keys=[id_residente],
    )

    preceptor: Mapped[Preceptor] = relationship(
        back_populates="escalas",
        foreign_keys=[id_preceptor],
    )


class Internacao(Base):
    __tablename__ = "internacao"

    id_internacao: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    id_paciente: Mapped[int] = mapped_column(
        ForeignKey(
            "paciente.id_pessoa",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    id_unidade: Mapped[int] = mapped_column(
        ForeignKey(
            "unidade.id_unidade",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    data_hora_entrada: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    data_hora_saida: Mapped[
        datetime | None
    ] = mapped_column(DateTime)

    paciente: Mapped[Paciente] = relationship(
        back_populates="internacoes"
    )

    unidade: Mapped[Unidade] = relationship(
        back_populates="internacoes"
    )


class AuditoriaAtendimento(Base):
    __tablename__ = "auditoria_atendimento"

    id_auditoria: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    id_atendimento: Mapped[int | None] = mapped_column(
        BigInteger
    )

    operacao: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    usuario: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    data_hora: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    dados_antigos: Mapped[dict | None] = mapped_column(
        JSONB
    )

    dados_novos: Mapped[dict | None] = mapped_column(
        JSONB
    )