from __future__ import annotations

import threading
from datetime import datetime
from tkinter import messagebox, ttk
from typing import Callable

import customtkinter as ctk

from hospital_yuska.interface import servicos


class OperacaoCancelada(Exception):
    """Indica que o usuário cancelou uma entrada."""


class AplicacaoHospital(ctk.CTk):
    """Interface desktop para demonstração das funcionalidades da Etapa 2."""

    COR_FUNDO = "#08111F"
    COR_CABECALHO = "#0F1B2D"
    COR_SUPERFICIE = "#111D31"
    COR_CARTAO = "#15243A"
    COR_CARTAO_ALTERNADO = "#101B2D"
    COR_BORDA = "#2A3B55"
    COR_PRIMARIA = "#2563EB"
    COR_PRIMARIA_HOVER = "#1D4ED8"
    COR_DESTAQUE = "#0EA5E9"
    COR_TEXTO = "#F8FAFC"
    COR_TEXTO_SECUNDARIO = "#A8B4C7"
    COR_SUCESSO = "#34D399"
    COR_ERRO = "#F87171"

    def __init__(self) -> None:
        super().__init__()

        self.title("Sistema de Gestão Hospitalar Dra. Yuska")
        self.geometry("1360x820")
        self.minsize(1120, 700)
        self.configure(fg_color=self.COR_FUNDO)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._configurar_estilo()
        self._criar_cabecalho()
        self._criar_abas()
        self._criar_resultados()
        self._criar_status()

    def _configurar_estilo(self) -> None:
        """Configura a identidade visual da tabela e das barras de rolagem."""
        estilo = ttk.Style(self)
        estilo.theme_use("clam")

        estilo.configure(
            "Treeview",
            background=self.COR_CARTAO_ALTERNADO,
            fieldbackground=self.COR_CARTAO_ALTERNADO,
            foreground=self.COR_TEXTO,
            rowheight=34,
            borderwidth=0,
            relief="flat",
            font=("Segoe UI", 10),
        )

        estilo.configure(
            "Treeview.Heading",
            background="#20314B",
            foreground=self.COR_TEXTO,
            relief="flat",
            borderwidth=0,
            padding=(10, 9),
            font=("Segoe UI", 11, "bold"),
        )

        estilo.map(
            "Treeview",
            background=[("selected", self.COR_PRIMARIA)],
            foreground=[("selected", "#FFFFFF")],
        )

        estilo.map(
            "Treeview.Heading",
            background=[("active", "#2B4262")],
        )

        estilo.configure(
            "Vertical.TScrollbar",
            background="#31445F",
            troughcolor=self.COR_SUPERFICIE,
            bordercolor=self.COR_SUPERFICIE,
            arrowcolor=self.COR_TEXTO,
        )

        estilo.configure(
            "Horizontal.TScrollbar",
            background="#31445F",
            troughcolor=self.COR_SUPERFICIE,
            bordercolor=self.COR_SUPERFICIE,
            arrowcolor=self.COR_TEXTO,
        )

    def _criar_cabecalho(self) -> None:
        """Cria o cabeçalho principal da aplicação."""
        cabecalho = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=self.COR_CABECALHO,
            border_width=0,
        )
        cabecalho.grid(row=0, column=0, sticky="ew")
        cabecalho.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            cabecalho,
            text="Sistema de Gestão Hospitalar Dra. Yuska",
            text_color=self.COR_TEXTO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=27,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=0,
            padx=28,
            pady=(20, 3),
            sticky="w",
        )

        ctk.CTkLabel(
            cabecalho,
            text=(
                "Etapa 2 — PostgreSQL, SQLAlchemy "
                "e funcionalidades avançadas"
            ),
            text_color=self.COR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=14,
            ),
        ).grid(
            row=1,
            column=0,
            padx=28,
            pady=(0, 18),
            sticky="w",
        )

        ctk.CTkFrame(
            cabecalho,
            height=3,
            corner_radius=0,
            fg_color=self.COR_DESTAQUE,
        ).grid(
            row=2,
            column=0,
            sticky="ew",
        )

    def _criar_abas(self) -> None:
        """Organiza as funcionalidades em grupos de navegação."""
        self.abas = ctk.CTkTabview(
            self,
            height=240,
            corner_radius=12,
            fg_color=self.COR_SUPERFICIE,
            border_width=1,
            border_color=self.COR_BORDA,
            segmented_button_fg_color="#1B2B43",
            segmented_button_selected_color=self.COR_PRIMARIA,
            segmented_button_selected_hover_color=self.COR_PRIMARIA_HOVER,
            segmented_button_unselected_color="#1B2B43",
            segmented_button_unselected_hover_color="#2A3B55",
            text_color=self.COR_TEXTO,
        )
        self.abas.grid(
            row=1,
            column=0,
            padx=22,
            pady=(16, 12),
            sticky="ew",
        )

        nomes = (
            "Visão geral",
            "ORM — Etapa 1",
            "ORM — Avançadas",
            "Procedures e views",
        )

        for nome in nomes:
            aba = self.abas.add(nome)
            aba.configure(fg_color=self.COR_SUPERFICIE)

            for coluna in range(4):
                aba.grid_columnconfigure(coluna, weight=1)

        self._botoes_visao_geral()
        self._botoes_etapa1()
        self._botoes_avancadas()
        self._botoes_procedures_views()

    def _adicionar_botao(
        self,
        aba: str,
        texto: str,
        comando: Callable[[], None],
        linha: int,
        coluna: int,
    ) -> None:
        """Adiciona um botão padronizado à aba informada."""
        ctk.CTkButton(
            self.abas.tab(aba),
            text=texto,
            command=comando,
            height=46,
            corner_radius=9,
            border_width=1,
            border_color="#3B82F6",
            fg_color=self.COR_PRIMARIA,
            hover_color=self.COR_PRIMARIA_HOVER,
            text_color="#FFFFFF",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
                weight="bold",
            ),
        ).grid(
            row=linha,
            column=coluna,
            padx=9,
            pady=9,
            sticky="ew",
        )

    def _botoes_visao_geral(self) -> None:
        self._adicionar_botao(
            "Visão geral",
            "Verificar objetos do banco",
            lambda: self._executar(
                "Objetos da Etapa 2",
                servicos.verificar_objetos_banco,
            ),
            0,
            0,
        )

        self._adicionar_botao(
            "Visão geral",
            "Auditoria de atendimentos",
            lambda: self._executar(
                "Auditoria",
                servicos.listar_auditoria,
            ),
            0,
            1,
        )

        self._adicionar_botao(
            "Visão geral",
            "Médias dos procedimentos",
            lambda: self._executar(
                "Médias dos procedimentos",
                servicos.listar_medias_procedimentos,
            ),
            0,
            2,
        )

        self._adicionar_botao(
            "Visão geral",
            "Simular concorrência",
            self._iniciar_concorrencia,
            0,
            3,
        )

    def _botoes_etapa1(self) -> None:
        botoes = (
            (
                "Inserir atendimento",
                self._inserir_atendimento,
            ),
            (
                "Atendimentos do paciente",
                self._listar_atendimentos,
            ),
            (
                "Procedimentos do atendimento",
                self._listar_procedimentos,
            ),
            (
                "Atualizar paciente",
                self._atualizar_paciente,
            ),
            (
                "Remover procedimento",
                self._remover_procedimento,
            ),
            (
                "Média por residente",
                lambda: self._executar(
                    "Média de duração",
                    servicos.obter_media_duracao,
                ),
            ),
            (
                "Ranking dos residentes",
                lambda: self._executar(
                    "Ranking dos residentes",
                    servicos.obter_ranking_residentes,
                ),
            ),
            (
                "Preceptores com mais de 5",
                lambda: self._executar(
                    "Preceptores com mais de cinco",
                    servicos.obter_preceptores_mais_cinco,
                ),
            ),
            (
                "Plantões do mês",
                lambda: self._executar(
                    "Plantões do mês",
                    servicos.obter_plantoes_mes_atual,
                ),
            ),
            (
                "Pacientes sem alto risco",
                lambda: self._executar(
                    "Pacientes sem alto risco",
                    servicos.obter_pacientes_sem_alto_risco,
                ),
            ),
        )

        for indice, (texto, comando) in enumerate(botoes):
            self._adicionar_botao(
                "ORM — Etapa 1",
                texto,
                comando,
                indice // 4,
                indice % 4,
            )

    def _botoes_avancadas(self) -> None:
        botoes = (
            (
                "Preceptores e flamenguistas",
                lambda: self._executar(
                    "Preceptores",
                    servicos.obter_preceptores_flamenguistas,
                ),
            ),
            (
                "Último atendimento por paciente",
                lambda: self._executar(
                    "Últimos atendimentos",
                    servicos.obter_ultimos_atendimentos,
                ),
            ),
            (
                "Percentual de alto risco",
                lambda: self._executar(
                    "Percentual de alto risco",
                    servicos.obter_percentual_alto_risco,
                ),
            ),
            (
                "Lazy loading x eager loading",
                self._demonstrar_carregamento,
            ),
        )

        for indice, (texto, comando) in enumerate(botoes):
            self._adicionar_botao(
                "ORM — Avançadas",
                texto,
                comando,
                0,
                indice,
            )

    def _botoes_procedures_views(self) -> None:
        botoes = (
            (
                "Pacientes internados",
                lambda: self._mostrar_view(
                    "vw_pacientes_internados"
                ),
            ),
            (
                "Supervisão inadequada",
                lambda: self._mostrar_view(
                    "vw_residentes_sem_supervisor"
                ),
            ),
            (
                "Estatísticas mensais",
                lambda: self._mostrar_view(
                    "vw_estatisticas_atendimentos_mensal"
                ),
            ),
            (
                "Registrar atendimento completo",
                self._registrar_atendimento_completo,
            ),
            (
                "Tempo médio de espera",
                lambda: self._executar(
                    "Tempo médio de espera",
                    servicos.calcular_tempo_medio_espera,
                ),
            ),
            (
                "Reajustar escala",
                self._reajustar_escala,
            ),
        )

        for indice, (texto, comando) in enumerate(botoes):
            self._adicionar_botao(
                "Procedures e views",
                texto,
                comando,
                indice // 4,
                indice % 4,
            )

    def _criar_resultados(self) -> None:
        """Cria o painel responsável por exibir os resultados das consultas."""
        quadro = ctk.CTkFrame(
            self,
            corner_radius=12,
            fg_color=self.COR_SUPERFICIE,
            border_width=1,
            border_color=self.COR_BORDA,
        )
        quadro.grid(
            row=2,
            column=0,
            padx=22,
            pady=(0, 12),
            sticky="nsew",
        )

        quadro.grid_rowconfigure(1, weight=1)
        quadro.grid_columnconfigure(0, weight=1)

        self.titulo_resultado = ctk.CTkLabel(
            quadro,
            text="Resultados",
            text_color=self.COR_TEXTO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=19,
                weight="bold",
            ),
        )
        self.titulo_resultado.grid(
            row=0,
            column=0,
            padx=18,
            pady=(14, 10),
            sticky="w",
        )

        moldura_tabela = ctk.CTkFrame(
            quadro,
            fg_color=self.COR_CARTAO_ALTERNADO,
            corner_radius=8,
            border_width=1,
            border_color=self.COR_BORDA,
        )
        moldura_tabela.grid(
            row=1,
            column=0,
            padx=14,
            pady=(0, 14),
            sticky="nsew",
        )

        moldura_tabela.grid_rowconfigure(0, weight=1)
        moldura_tabela.grid_columnconfigure(0, weight=1)

        self.tabela = ttk.Treeview(
            moldura_tabela,
            show="headings",
            selectmode="browse",
        )
        self.tabela.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        self.tabela.tag_configure(
            "linha_par",
            background=self.COR_CARTAO_ALTERNADO,
        )
        self.tabela.tag_configure(
            "linha_impar",
            background=self.COR_CARTAO,
        )

        barra_vertical = ttk.Scrollbar(
            moldura_tabela,
            orient="vertical",
            command=self.tabela.yview,
        )
        barra_vertical.grid(
            row=0,
            column=1,
            sticky="ns",
        )

        barra_horizontal = ttk.Scrollbar(
            moldura_tabela,
            orient="horizontal",
            command=self.tabela.xview,
        )
        barra_horizontal.grid(
            row=1,
            column=0,
            sticky="ew",
        )

        self.tabela.configure(
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set,
        )

    def _criar_status(self) -> None:
        """Cria a área inferior de mensagens da aplicação."""
        self.status = ctk.CTkLabel(
            self,
            text="Aplicação pronta.",
            anchor="w",
            text_color=self.COR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
            ),
        )
        self.status.grid(
            row=3,
            column=0,
            padx=26,
            pady=(0, 12),
            sticky="ew",
        )

    def _pedir(
        self,
        titulo: str,
        mensagem: str,
        *,
        permitir_vazio: bool = False,
    ) -> str:
        valor = ctk.CTkInputDialog(
            title=titulo,
            text=mensagem,
        ).get_input()

        if valor is None:
            raise OperacaoCancelada()

        valor = valor.strip()

        if not valor and not permitir_vazio:
            raise ValueError(
                "O campo informado é obrigatório."
            )

        return valor

    def _pedir_inteiro(
        self,
        titulo: str,
        mensagem: str,
    ) -> int:
        return int(
            self._pedir(
                titulo,
                mensagem,
            )
        )

    def _executar(
        self,
        titulo: str,
        operacao: Callable[[], list[dict]],
    ) -> None:
        try:
            self.status.configure(
                text=f"Executando: {titulo}...",
                text_color=self.COR_DESTAQUE,
            )

            registros = operacao()

            self._mostrar_resultados(
                titulo,
                registros,
            )

        except OperacaoCancelada:
            self.status.configure(
                text="Operação cancelada.",
                text_color=self.COR_TEXTO_SECUNDARIO,
            )

        except Exception as erro:
            self.status.configure(
                text="A operação não foi concluída.",
                text_color=self.COR_ERRO,
            )

            messagebox.showerror(
                "Erro",
                str(erro),
                parent=self,
            )

    def _mostrar_resultados(
        self,
        titulo: str,
        registros: list[dict],
    ) -> None:
        self.titulo_resultado.configure(text=titulo)

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        if not registros:
            self.tabela["columns"] = ("resultado",)
            self.tabela.heading(
                "resultado",
                text="Resultado",
                anchor="center",
            )
            self.tabela.column(
                "resultado",
                width=700,
                minwidth=300,
                anchor="w",
            )
            self.tabela.insert(
                "",
                "end",
                values=("Nenhum registro encontrado.",),
                tags=("linha_par",),
            )

            self.status.configure(
                text="Consulta concluída sem registros.",
                text_color=self.COR_TEXTO_SECUNDARIO,
            )
            return

        colunas = list(registros[0].keys())
        linhas_formatadas = [
            [
                self._formatar(registro.get(coluna))
                for coluna in colunas
            ]
            for registro in registros
        ]

        self.tabela["columns"] = colunas

        for indice_coluna, coluna in enumerate(colunas):
            titulo_coluna = coluna.replace("_", " ").title()
            valores_coluna = [
                linha[indice_coluna]
                for linha in linhas_formatadas[:100]
            ]

            self.tabela.heading(
                coluna,
                text=titulo_coluna,
                anchor="center",
            )
            self.tabela.column(
                coluna,
                width=self._calcular_largura_coluna(
                    titulo_coluna,
                    valores_coluna,
                ),
                minwidth=110,
                anchor=self._definir_ancora_coluna(coluna),
                stretch=True,
            )

        for indice_linha, valores in enumerate(linhas_formatadas):
            etiqueta = (
                "linha_par"
                if indice_linha % 2 == 0
                else "linha_impar"
            )
            self.tabela.insert(
                "",
                "end",
                values=valores,
                tags=(etiqueta,),
            )

        self.status.configure(
            text=(
                f"Consulta concluída: "
                f"{len(registros)} registro(s)."
            ),
            text_color=self.COR_SUCESSO,
        )

    @staticmethod
    def _calcular_largura_coluna(
        titulo: str,
        valores: list[str],
    ) -> int:
        """Calcula uma largura legível sem deixar a tabela excessivamente larga."""
        maior_conteudo = max(
            [len(titulo), *(len(valor) for valor in valores)],
            default=len(titulo),
        )
        return min(max(125, maior_conteudo * 8 + 34), 360)

    @staticmethod
    def _definir_ancora_coluna(coluna: str) -> str:
        """Centraliza identificadores e indicadores numéricos na tabela."""
        nome = coluna.lower()
        prefixos_centralizados = (
            "id_",
            "total",
            "quantidade",
            "media",
            "média",
            "percentual",
            "duracao",
            "duração",
            "status",
            "supervisao",
            "supervisão",
        )
        return (
            "center"
            if nome.startswith(prefixos_centralizados)
            else "w"
        )

    @staticmethod
    def _formatar(valor: object) -> str:
        if valor is None:
            return ""

        if isinstance(valor, datetime):
            return valor.strftime("%d/%m/%Y %H:%M")

        if isinstance(valor, bool):
            return "Sim" if valor else "Não"

        return str(valor)

    def _inserir_atendimento(self) -> None:
        def operacao() -> list[dict]:
            data_hora = datetime.fromisoformat(
                self._pedir(
                    "Novo atendimento",
                    "Data e horário (AAAA-MM-DD HH:MM):",
                )
            )

            return servicos.inserir_atendimento_orm(
                data_hora=data_hora,
                duracao_minutos=self._pedir_inteiro(
                    "Novo atendimento",
                    "Duração em minutos:",
                ),
                id_paciente=self._pedir_inteiro(
                    "Novo atendimento",
                    "ID do paciente:",
                ),
                id_residente=self._pedir_inteiro(
                    "Novo atendimento",
                    "ID do residente:",
                ),
                id_preceptor=self._pedir_inteiro(
                    "Novo atendimento",
                    "ID do preceptor:",
                ),
                id_unidade=self._pedir_inteiro(
                    "Novo atendimento",
                    "ID da unidade:",
                ),
            )

        self._executar(
            "Inserção de atendimento com ORM",
            operacao,
        )

    def _listar_atendimentos(self) -> None:
        self._executar(
            "Atendimentos do paciente",
            lambda: servicos.listar_atendimentos_orm(
                self._pedir_inteiro(
                    "Atendimentos",
                    "ID do paciente:",
                )
            ),
        )

    def _listar_procedimentos(self) -> None:
        self._executar(
            "Procedimentos do atendimento",
            lambda: servicos.listar_procedimentos_orm(
                self._pedir_inteiro(
                    "Procedimentos",
                    "ID do atendimento:",
                )
            ),
        )

    def _atualizar_paciente(self) -> None:
        def operacao() -> list[dict]:
            id_paciente = self._pedir_inteiro(
                "Atualizar paciente",
                "ID do paciente:",
            )

            endereco = self._pedir(
                "Atualizar paciente",
                "Novo endereço — deixe vazio para manter:",
                permitir_vazio=True,
            )

            convenio = self._pedir(
                "Atualizar paciente",
                "Novo convênio — deixe vazio para manter:",
                permitir_vazio=True,
            )

            return servicos.atualizar_paciente_orm(
                id_paciente=id_paciente,
                endereco=endereco or None,
                num_convenio=convenio or None,
            )

        self._executar(
            "Atualização do paciente",
            operacao,
        )

    def _remover_procedimento(self) -> None:
        def operacao() -> list[dict]:
            return servicos.remover_procedimento_orm(
                id_atendimento=self._pedir_inteiro(
                    "Remover procedimento",
                    "ID do atendimento:",
                ),
                id_procedimento=self._pedir_inteiro(
                    "Remover procedimento",
                    "ID do procedimento:",
                ),
            )

        self._executar(
            "Remoção condicionada",
            operacao,
        )

    def _demonstrar_carregamento(self) -> None:
        self._executar(
            "Lazy loading x eager loading",
            lambda: servicos.demonstrar_lazy_eager(
                self._pedir_inteiro(
                    "Relacionamentos",
                    "ID do atendimento:",
                )
            ),
        )

    def _mostrar_view(
        self,
        nome_view: str,
    ) -> None:
        self._executar(
            nome_view,
            lambda: servicos.consultar_view(nome_view),
        )

    def _registrar_atendimento_completo(
        self,
    ) -> None:
        def operacao() -> list[dict]:
            data_hora = datetime.fromisoformat(
                self._pedir(
                    "Procedure",
                    "Data e horário (AAAA-MM-DD HH:MM):",
                )
            )

            procedimentos = self._pedir(
                "Procedure",
                (
                    "Array JSON de procedimentos. Exemplo:\n"
                    '[{"id_procedimento": 1, '
                    '"quantidade": 1, '
                    '"tempo_real_minutos": 30}]'
                ),
            )

            return servicos.registrar_atendimento_completo(
                data_hora=data_hora,
                duracao_minutos=self._pedir_inteiro(
                    "Procedure",
                    "Duração em minutos:",
                ),
                id_paciente=self._pedir_inteiro(
                    "Procedure",
                    "ID do paciente:",
                ),
                id_residente=self._pedir_inteiro(
                    "Procedure",
                    "ID do residente:",
                ),
                id_preceptor=self._pedir_inteiro(
                    "Procedure",
                    "ID do preceptor:",
                ),
                id_unidade=self._pedir_inteiro(
                    "Procedure",
                    "ID da unidade:",
                ),
                procedimentos_json=procedimentos,
            )

        self._executar(
            "Registro completo de atendimento",
            operacao,
        )

    def _reajustar_escala(self) -> None:
        def operacao() -> list[dict]:
            return servicos.reajustar_escala(
                id_residente=self._pedir_inteiro(
                    "Reajuste de escala",
                    "ID do residente:",
                ),
                dia_origem=self._pedir(
                    "Reajuste de escala",
                    "Dia de origem:",
                ).lower(),
                turno_origem=self._pedir(
                    "Reajuste de escala",
                    "Turno de origem:",
                ).lower(),
                dia_destino=self._pedir(
                    "Reajuste de escala",
                    "Dia de destino:",
                ).lower(),
                turno_destino=self._pedir(
                    "Reajuste de escala",
                    "Turno de destino:",
                ).lower(),
            )

        self._executar(
            "Reajuste da escala",
            operacao,
        )

    def _iniciar_concorrencia(self) -> None:
        self.status.configure(
            text="Executando simulação de concorrência...",
            text_color=self.COR_DESTAQUE,
        )

        thread = threading.Thread(
            target=self._executar_concorrencia,
            daemon=True,
        )
        thread.start()

    def _executar_concorrencia(self) -> None:
        try:
            registros = servicos.simular_concorrencia()

            self.after(
                0,
                lambda: self._mostrar_resultados(
                    "Simulação de concorrência",
                    registros,
                ),
            )

        except Exception as erro:
            self.after(
                0,
                lambda: messagebox.showerror(
                    "Erro na concorrência",
                    str(erro),
                    parent=self,
                ),
            )


def main() -> None:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    aplicacao = AplicacaoHospital()
    aplicacao.mainloop()


if __name__ == "__main__":
    main()