from __future__ import annotations

import threading
from datetime import datetime
from tkinter import StringVar, messagebox, ttk
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
            rowheight=40,
            borderwidth=0,
            relief="flat",
            font=("Segoe UI", 12),
        )

        estilo.configure(
            "Treeview.Heading",
            background="#20314B",
            foreground=self.COR_TEXTO,
            relief="flat",
            borderwidth=0,
            padding=(12, 10),
            font=("Segoe UI", 12, "bold"),
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
                "Preceptores de pacientes flamenguistas",
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
                "Carregamento sob demanda x antecipado",
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

    @staticmethod
    def _converter_data_hora_brasileira(valor: str) -> datetime:
        """Converte uma data brasileira em objeto ``datetime``."""
        valor_normalizado = " ".join(valor.strip().split())
        formatos_aceitos = (
            "%d/%m/%Y %H:%M",
            "%d-%m-%Y %H:%M",
        )

        for formato in formatos_aceitos:
            try:
                return datetime.strptime(
                    valor_normalizado,
                    formato,
                )
            except ValueError:
                continue

        raise ValueError(
            "Data e horário inválidos. Use o formato "
            "DD/MM/AAAA HH:MM, por exemplo: "
            "02/08/2026 12:53."
        )

    @staticmethod
    def _localizar_chave_identificador(
        registro: dict,
        chaves_preferidas: tuple[str, ...],
    ) -> str:
        """Localiza a coluna que representa o identificador do registro."""
        for chave in chaves_preferidas:
            if chave in registro:
                return chave

        for chave in registro:
            if chave.lower().startswith("id_"):
                return chave

        if "id" in registro:
            return "id"

        raise ValueError(
            "A consulta não retornou uma coluna de identificador."
        )

    def _resumir_registro(
        self,
        registro: dict,
        chave_identificador: str,
    ) -> str:
        """Produz um resumo legível para a opção selecionada."""
        partes = []

        for chave, valor in registro.items():
            if chave == chave_identificador or valor in (None, ""):
                continue

            partes.append(self._formatar(valor))

            if len(partes) == 3:
                break

        identificador = self._formatar(
            registro[chave_identificador]
        )
        descricao = " — ".join(partes)

        return (
            f"{identificador} — {descricao}"
            if descricao
            else identificador
        )

    def _selecionar_registro(
        self,
        titulo: str,
        registros: list[dict],
        chaves_identificador: tuple[str, ...],
        *,
        janela_pai: ctk.CTkToplevel | None = None,
    ) -> tuple[int, str]:
        """Abre uma janela pesquisável e retorna o ID escolhido."""
        if not registros:
            raise ValueError(
                f"Não existem registros disponíveis para {titulo.lower()}."
            )

        registros_normalizados: list[dict] = []

        for registro in registros:
            if isinstance(registro, dict):
                registros_normalizados.append(
                    dict(registro)
                )
                continue

            if (
                isinstance(registro, tuple)
                and len(registro) == 2
            ):
                identificador, nome = registro

                registros_normalizados.append(
                    {
                        "id": identificador,
                        "nome": nome,
                    }
                )
                continue

            raise TypeError(
                "Formato de registro não suportado "
                "pela janela de seleção."
            )
        chave_identificador = self._localizar_chave_identificador(
            registros_normalizados[0],
            chaves_identificador,
        )

        todas_colunas: list[str] = []
        for registro in registros_normalizados:
            for coluna in registro:
                if coluna not in todas_colunas:
                    todas_colunas.append(coluna)

        prioridades = (
            chave_identificador,
            "nome",
            "descricao",
            "descrição",
            "cpf",
            "codigo",
            "código",
            "registro",
            "titulacao",
            "titulação",
            "unidade",
        )
        colunas = [
            coluna
            for coluna in prioridades
            if coluna in todas_colunas
        ]
        colunas.extend(
            coluna
            for coluna in todas_colunas
            if coluna not in colunas
        )
        colunas = colunas[:6]

        pai = janela_pai or self
        janela = ctk.CTkToplevel(pai)
        janela.title(titulo)
        janela.geometry("900x520")
        janela.minsize(720, 430)
        janela.configure(fg_color=self.COR_FUNDO)
        janela.transient(pai)
        janela.grid_columnconfigure(0, weight=1)
        janela.grid_rowconfigure(2, weight=1)

        resultado: dict[str, object] = {
            "identificador": None,
            "descricao": None,
        }
        mapa_itens: dict[str, dict] = {}

        ctk.CTkLabel(
            janela,
            text=titulo,
            text_color=self.COR_TEXTO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=20,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=0,
            padx=22,
            pady=(18, 6),
            sticky="w",
        )

        variavel_busca = StringVar()
        campo_busca = ctk.CTkEntry(
            janela,
            textvariable=variavel_busca,
            placeholder_text=(
                "Pesquisar por ID, nome ou qualquer informação exibida..."
            ),
            height=40,
            corner_radius=8,
            border_color=self.COR_BORDA,
            fg_color=self.COR_CARTAO,
            text_color=self.COR_TEXTO,
        )
        campo_busca.grid(
            row=1,
            column=0,
            padx=22,
            pady=(4, 12),
            sticky="ew",
        )

        moldura = ctk.CTkFrame(
            janela,
            fg_color=self.COR_SUPERFICIE,
            border_width=1,
            border_color=self.COR_BORDA,
            corner_radius=10,
        )
        moldura.grid(
            row=2,
            column=0,
            padx=22,
            pady=(0, 12),
            sticky="nsew",
        )
        moldura.grid_columnconfigure(0, weight=1)
        moldura.grid_rowconfigure(0, weight=1)

        tabela = ttk.Treeview(
            moldura,
            columns=colunas,
            show="headings",
            selectmode="browse",
        )
        tabela.grid(row=0, column=0, sticky="nsew")

        barra_vertical = ttk.Scrollbar(
            moldura,
            orient="vertical",
            command=tabela.yview,
        )
        barra_vertical.grid(row=0, column=1, sticky="ns")

        barra_horizontal = ttk.Scrollbar(
            moldura,
            orient="horizontal",
            command=tabela.xview,
        )
        barra_horizontal.grid(row=1, column=0, sticky="ew")

        tabela.configure(
            yscrollcommand=barra_vertical.set,
            xscrollcommand=barra_horizontal.set,
        )

        for coluna in colunas:
            titulo_coluna = coluna.replace("_", " ").title()
            valores = [
                self._formatar(registro.get(coluna))
                for registro in registros_normalizados
            ]
            tabela.heading(
                coluna,
                text=titulo_coluna,
                anchor="center",
            )
            tabela.column(
                coluna,
                width=self._calcular_largura_coluna(
                    titulo_coluna,
                    valores,
                ),
                minwidth=110,
                anchor=self._definir_ancora_coluna(coluna),
                stretch=True,
            )

        rodape = ctk.CTkFrame(
            janela,
            fg_color="transparent",
        )
        rodape.grid(
            row=3,
            column=0,
            padx=22,
            pady=(0, 18),
            sticky="ew",
        )
        rodape.grid_columnconfigure(0, weight=1)

        texto_contagem = StringVar()
        ctk.CTkLabel(
            rodape,
            textvariable=texto_contagem,
            text_color=self.COR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12,
            ),
        ).grid(row=0, column=0, sticky="w")

        def carregar_tabela(*_: object) -> None:
            termo = variavel_busca.get().strip().casefold()

            for item in tabela.get_children():
                tabela.delete(item)

            mapa_itens.clear()
            filtrados = []

            for registro in registros_normalizados:
                texto_pesquisa = " ".join(
                    self._formatar(valor)
                    for valor in registro.values()
                ).casefold()

                if termo and termo not in texto_pesquisa:
                    continue

                filtrados.append(registro)
                valores = [
                    self._formatar(registro.get(coluna))
                    for coluna in colunas
                ]
                item = tabela.insert(
                    "",
                    "end",
                    values=valores,
                )
                mapa_itens[item] = registro

            texto_contagem.set(
                f"{len(filtrados)} registro(s) encontrado(s)."
            )

            itens = tabela.get_children()
            if itens:
                tabela.selection_set(itens[0])
                tabela.focus(itens[0])

        def confirmar() -> None:
            selecao = tabela.selection()

            if not selecao:
                messagebox.showwarning(
                    "Seleção necessária",
                    "Selecione um registro para continuar.",
                    parent=janela,
                )
                return

            registro = mapa_itens[selecao[0]]
            identificador = registro.get(chave_identificador)

            try:
                identificador_inteiro = int(identificador)
            except (TypeError, ValueError) as erro:
                raise ValueError(
                    "O identificador selecionado não é numérico."
                ) from erro

            resultado["identificador"] = identificador_inteiro
            resultado["descricao"] = self._resumir_registro(
                registro,
                chave_identificador,
            )
            janela.destroy()

        def cancelar() -> None:
            janela.destroy()

        ctk.CTkButton(
            rodape,
            text="Cancelar",
            command=cancelar,
            width=130,
            height=38,
            fg_color="#334155",
            hover_color="#475569",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
                weight="bold",
            ),
        ).grid(row=0, column=1, padx=(10, 8))

        ctk.CTkButton(
            rodape,
            text="Selecionar",
            command=confirmar,
            width=145,
            height=38,
            fg_color=self.COR_PRIMARIA,
            hover_color=self.COR_PRIMARIA_HOVER,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
                weight="bold",
            ),
        ).grid(row=0, column=2)

        variavel_busca.trace_add("write", carregar_tabela)
        tabela.bind("<Double-1>", lambda _evento: confirmar())
        janela.protocol("WM_DELETE_WINDOW", cancelar)

        carregar_tabela()

        # Garante que a janela de seleção apareça acima do formulário pai.
        janela.update_idletasks()
        janela.deiconify()
        janela.lift()
        janela.wait_visibility()
        janela.grab_set()
        janela.focus_force()
        janela.after(100, campo_busca.focus_set)
        pai.wait_window(janela)

        if resultado["identificador"] is None:
            raise OperacaoCancelada()

        return (
            int(resultado["identificador"]),
            str(resultado["descricao"]),
        )

    def _coletar_dados_atendimento(
        self,
        titulo: str,
    ) -> dict[str, object]:
        """Coleta, em um único formulário, os dados de um atendimento."""
        fontes = {
            "paciente": (
                "Paciente",
                servicos.listar_pacientes_para_selecao(),
                ("id_paciente", "id"),
            ),
            "residente": (
                "Residente",
                servicos.listar_residentes_para_selecao(),
                ("id_residente", "id"),
            ),
            "preceptor": (
                "Preceptor",
                servicos.listar_preceptores_para_selecao(),
                ("id_preceptor", "id"),
            ),
            "unidade": (
                "Unidade",
                servicos.listar_unidades_para_selecao(),
                ("id_unidade", "id"),
            ),
        }

        janela = ctk.CTkToplevel(self)
        janela.title(titulo)
        janela.geometry("760x610")
        janela.minsize(700, 570)
        janela.configure(fg_color=self.COR_FUNDO)
        janela.transient(self)
        janela.grid_columnconfigure(0, weight=1)

        resultado: dict[str, object] | None = None
        identificadores: dict[str, int | None] = {
            nome: None for nome in fontes
        }
        descricoes = {
            nome: StringVar(value="Nenhum registro selecionado")
            for nome in fontes
        }

        ctk.CTkLabel(
            janela,
            text=titulo,
            text_color=self.COR_TEXTO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=22,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=0,
            padx=24,
            pady=(20, 4),
            sticky="w",
        )

        ctk.CTkLabel(
            janela,
            text=(
                "Informe a data no padrão brasileiro e selecione "
                "os registros existentes no banco."
            ),
            text_color=self.COR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
            ),
        ).grid(
            row=1,
            column=0,
            padx=24,
            pady=(0, 14),
            sticky="w",
        )

        formulario = ctk.CTkFrame(
            janela,
            fg_color=self.COR_SUPERFICIE,
            corner_radius=12,
            border_width=1,
            border_color=self.COR_BORDA,
        )
        formulario.grid(
            row=2,
            column=0,
            padx=24,
            pady=(0, 16),
            sticky="nsew",
        )
        formulario.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            formulario,
            text="Data e horário",
            text_color=self.COR_TEXTO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
                weight="bold",
            ),
        ).grid(row=0, column=0, padx=(18, 12), pady=(18, 8), sticky="w")

        campo_data = ctk.CTkEntry(
            formulario,
            placeholder_text="DD/MM/AAAA HH:MM",
            height=38,
            fg_color=self.COR_CARTAO,
            border_color=self.COR_BORDA,
            text_color=self.COR_TEXTO,
        )
        campo_data.grid(
            row=0,
            column=1,
            columnspan=2,
            padx=(0, 18),
            pady=(18, 8),
            sticky="ew",
        )
        campo_data.insert(
            0,
            datetime.now().strftime("%d/%m/%Y %H:%M"),
        )

        ctk.CTkLabel(
            formulario,
            text="Duração (minutos)",
            text_color=self.COR_TEXTO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
                weight="bold",
            ),
        ).grid(row=1, column=0, padx=(18, 12), pady=8, sticky="w")

        campo_duracao = ctk.CTkEntry(
            formulario,
            placeholder_text="Exemplo: 45",
            height=38,
            fg_color=self.COR_CARTAO,
            border_color=self.COR_BORDA,
            text_color=self.COR_TEXTO,
        )
        campo_duracao.grid(
            row=1,
            column=1,
            columnspan=2,
            padx=(0, 18),
            pady=8,
            sticky="ew",
        )

        def selecionar(nome: str) -> None:
            """Abre o seletor correspondente e atualiza o formulário."""
            rotulo, registros, chaves = fontes[nome]

            # Libera temporariamente o bloqueio modal do formulário principal.
            # Isso evita que a janela de seleção seja criada atrás dele no Windows.
            if janela.grab_current() is not None:
                janela.grab_release()

            try:
                identificador, descricao = self._selecionar_registro(
                    f"Selecionar {rotulo.lower()}",
                    registros,
                    chaves,
                    janela_pai=janela,
                )
                identificadores[nome] = identificador
                descricoes[nome].set(descricao)

            except OperacaoCancelada:
                return

            except Exception as erro:
                messagebox.showerror(
                    "Não foi possível abrir a seleção",
                    str(erro),
                    parent=janela,
                )

            finally:
                if janela.winfo_exists():
                    janela.deiconify()
                    janela.lift()
                    janela.focus_force()
                    janela.grab_set()

        for indice, (nome, (rotulo, _registros, _chaves)) in enumerate(
            fontes.items(),
            start=2,
        ):
            ctk.CTkLabel(
                formulario,
                text=rotulo,
                text_color=self.COR_TEXTO,
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=13,
                    weight="bold",
                ),
            ).grid(
                row=indice,
                column=0,
                padx=(18, 12),
                pady=8,
                sticky="w",
            )

            ctk.CTkLabel(
                formulario,
                textvariable=descricoes[nome],
                anchor="w",
                justify="left",
                text_color=self.COR_TEXTO_SECUNDARIO,
                fg_color=self.COR_CARTAO,
                corner_radius=7,
                padx=12,
                height=38,
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=13,
                ),
            ).grid(
                row=indice,
                column=1,
                padx=(0, 10),
                pady=8,
                sticky="ew",
            )

            ctk.CTkButton(
                formulario,
                text="Selecionar",
                command=lambda item=nome: janela.after_idle(
                    lambda: selecionar(item)
                ),
                width=120,
                height=38,
                fg_color=self.COR_PRIMARIA,
                hover_color=self.COR_PRIMARIA_HOVER,
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=12,
                    weight="bold",
                ),
            ).grid(
                row=indice,
                column=2,
                padx=(0, 18),
                pady=8,
            )

        botoes = ctk.CTkFrame(
            janela,
            fg_color="transparent",
        )
        botoes.grid(
            row=3,
            column=0,
            padx=24,
            pady=(0, 20),
            sticky="ew",
        )
        botoes.grid_columnconfigure(0, weight=1)

        def cancelar() -> None:
            janela.destroy()

        def confirmar() -> None:
            nonlocal resultado

            data_hora = self._converter_data_hora_brasileira(
                campo_data.get()
            )

            try:
                duracao = int(campo_duracao.get().strip())
            except ValueError as erro:
                raise ValueError(
                    "A duração deve ser informada em minutos inteiros."
                ) from erro

            if duracao <= 0:
                raise ValueError(
                    "A duração deve ser maior que zero."
                )

            ausentes = [
                fontes[nome][0]
                for nome, identificador in identificadores.items()
                if identificador is None
            ]

            if ausentes:
                raise ValueError(
                    "Selecione os seguintes registros: "
                    + ", ".join(ausentes)
                    + "."
                )

            resultado = {
                "data_hora": data_hora,
                "duracao_minutos": duracao,
                "id_paciente": int(identificadores["paciente"]),
                "id_residente": int(identificadores["residente"]),
                "id_preceptor": int(identificadores["preceptor"]),
                "id_unidade": int(identificadores["unidade"]),
            }
            janela.destroy()

        def confirmar_com_tratamento() -> None:
            try:
                confirmar()
            except Exception as erro:
                messagebox.showerror(
                    "Dados inválidos",
                    str(erro),
                    parent=janela,
                )

        ctk.CTkButton(
            botoes,
            text="Cancelar",
            command=cancelar,
            width=140,
            height=40,
            fg_color="#334155",
            hover_color="#475569",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
                weight="bold",
            ),
        ).grid(row=0, column=1, padx=(10, 8))

        ctk.CTkButton(
            botoes,
            text="Confirmar atendimento",
            command=confirmar_com_tratamento,
            width=210,
            height=40,
            fg_color=self.COR_PRIMARIA,
            hover_color=self.COR_PRIMARIA_HOVER,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
                weight="bold",
            ),
        ).grid(row=0, column=2)

        janela.protocol("WM_DELETE_WINDOW", cancelar)
        janela.grab_set()
        janela.after(100, campo_data.focus_set)
        self.wait_window(janela)

        if resultado is None:
            raise OperacaoCancelada()

        return resultado
    

    def _coletar_atualizacao_paciente(
        self,
    ) -> dict[str, object]:
        """Coleta paciente, endereço e convênio em um formulário único."""
        pacientes = servicos.listar_pacientes_para_selecao()
        convenios = servicos.listar_convenios_para_selecao()

        janela = ctk.CTkToplevel(self)
        janela.title("Atualizar paciente")
        janela.geometry("900x520")
        janela.minsize(780, 470)
        janela.configure(fg_color=self.COR_FUNDO)
        janela.transient(self)
        janela.grid_columnconfigure(0, weight=1)

        resultado: dict[str, object] | None = None
        id_paciente: int | None = None
        convenio_selecionado: str | None = None

        descricao_paciente = StringVar(
            value="Nenhum paciente selecionado"
        )
        texto_convenio = StringVar(
            value="Manter convênio atual"
        )

        ctk.CTkLabel(
            janela,
            text="Atualizar paciente",
            text_color=self.COR_TEXTO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=22,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=0,
            padx=24,
            pady=(20, 4),
            sticky="w",
        )

        ctk.CTkLabel(
            janela,
            text=(
                "Selecione o paciente e informe somente os dados "
                "que deverão ser alterados."
            ),
            text_color=self.COR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
            ),
        ).grid(
            row=1,
            column=0,
            padx=24,
            pady=(0, 14),
            sticky="w",
        )

        formulario = ctk.CTkFrame(
            janela,
            fg_color=self.COR_SUPERFICIE,
            corner_radius=12,
            border_width=1,
            border_color=self.COR_BORDA,
        )
        formulario.grid(
            row=2,
            column=0,
            padx=24,
            pady=(0, 16),
            sticky="nsew",
        )
        formulario.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            formulario,
            text="Paciente",
            text_color=self.COR_TEXTO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=0,
            padx=(18, 12),
            pady=(18, 8),
            sticky="w",
        )

        ctk.CTkLabel(
            formulario,
            textvariable=descricao_paciente,
            anchor="w",
            justify="left",
            text_color=self.COR_TEXTO_SECUNDARIO,
            fg_color=self.COR_CARTAO,
            corner_radius=7,
            padx=12,
            height=38,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
            ),
        ).grid(
            row=0,
            column=1,
            columnspan=2,
            padx=(0, 10),
            pady=(18, 8),
            sticky="ew",
        )

        def selecionar_paciente() -> None:
            """Abre a seleção de pacientes e atualiza o formulário."""
            nonlocal id_paciente

            if janela.grab_current() is not None:
                janela.grab_release()

            try:
                identificador, descricao = self._selecionar_registro(
                    "Selecionar paciente",
                    pacientes,
                    ("id_paciente", "id"),
                    janela_pai=janela,
                )
                id_paciente = identificador
                descricao_paciente.set(descricao)

            except OperacaoCancelada:
                return

            except Exception as erro:
                messagebox.showerror(
                    "Não foi possível selecionar o paciente",
                    str(erro),
                    parent=janela,
                )

            finally:
                if janela.winfo_exists():
                    janela.deiconify()
                    janela.lift()
                    janela.focus_force()
                    janela.grab_set()

        ctk.CTkButton(
            formulario,
            text="Selecionar",
            command=lambda: janela.after_idle(
                selecionar_paciente
            ),
            width=120,
            height=38,
            fg_color=self.COR_PRIMARIA,
            hover_color=self.COR_PRIMARIA_HOVER,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=3,
            padx=(0, 18),
            pady=(18, 8),
        )

        ctk.CTkLabel(
            formulario,
            text="Novo endereço",
            text_color=self.COR_TEXTO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
                weight="bold",
            ),
        ).grid(
            row=1,
            column=0,
            padx=(18, 12),
            pady=8,
            sticky="w",
        )

        campo_endereco = ctk.CTkEntry(
            formulario,
            placeholder_text="Deixe vazio para manter o endereço atual",
            height=38,
            fg_color=self.COR_CARTAO,
            border_color=self.COR_BORDA,
            text_color=self.COR_TEXTO,
        )
        campo_endereco.grid(
            row=1,
            column=1,
            columnspan=3,
            padx=(0, 18),
            pady=8,
            sticky="ew",
        )

        ctk.CTkLabel(
            formulario,
            text="Novo convênio",
            text_color=self.COR_TEXTO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
                weight="bold",
            ),
        ).grid(
            row=2,
            column=0,
            padx=(18, 12),
            pady=(8, 18),
            sticky="w",
        )

        ctk.CTkLabel(
            formulario,
            textvariable=texto_convenio,
            anchor="w",
            justify="left",
            text_color=self.COR_TEXTO_SECUNDARIO,
            fg_color=self.COR_CARTAO,
            corner_radius=7,
            padx=12,
            height=38,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
            ),
        ).grid(
            row=2,
            column=1,
            padx=(0, 10),
            pady=(8, 18),
            sticky="ew",
        )

        def manter_convenio_atual() -> None:
            nonlocal convenio_selecionado
            convenio_selecionado = None
            texto_convenio.set("Manter convênio atual")

        def selecionar_convenio() -> None:
            """Permite escolher um convênio já existente no banco."""
            nonlocal convenio_selecionado

            if not convenios:
                messagebox.showwarning(
                    "Convênios indisponíveis",
                    "Não existem números de convênio cadastrados para seleção.",
                    parent=janela,
                )
                return

            registros_convenios = [
                {
                    "id": indice,
                    "convenio": convenio,
                }
                for indice, convenio in enumerate(convenios, start=1)
            ]

            if janela.grab_current() is not None:
                janela.grab_release()

            try:
                indice, _descricao = self._selecionar_registro(
                    "Selecionar convênio",
                    registros_convenios,
                    ("id",),
                    janela_pai=janela,
                )
                convenio_selecionado = convenios[indice - 1]
                texto_convenio.set(convenio_selecionado)

            except OperacaoCancelada:
                return

            except Exception as erro:
                messagebox.showerror(
                    "Não foi possível selecionar o convênio",
                    str(erro),
                    parent=janela,
                )

            finally:
                if janela.winfo_exists():
                    janela.deiconify()
                    janela.lift()
                    janela.focus_force()
                    janela.grab_set()

        ctk.CTkButton(
            formulario,
            text="Manter atual",
            command=manter_convenio_atual,
            width=115,
            height=38,
            fg_color="#334155",
            hover_color="#475569",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12,
                weight="bold",
            ),
        ).grid(
            row=2,
            column=2,
            padx=(0, 10),
            pady=(8, 18),
        )

        ctk.CTkButton(
            formulario,
            text="Selecionar",
            command=lambda: janela.after_idle(
                selecionar_convenio
            ),
            width=120,
            height=38,
            fg_color=self.COR_PRIMARIA,
            hover_color=self.COR_PRIMARIA_HOVER,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12,
                weight="bold",
            ),
        ).grid(
            row=2,
            column=3,
            padx=(0, 18),
            pady=(8, 18),
        )

        botoes = ctk.CTkFrame(
            janela,
            fg_color="transparent",
        )
        botoes.grid(
            row=3,
            column=0,
            padx=24,
            pady=(0, 20),
            sticky="ew",
        )
        botoes.grid_columnconfigure(0, weight=1)

        def cancelar() -> None:
            janela.destroy()

        def confirmar() -> None:
            nonlocal resultado

            if id_paciente is None:
                raise ValueError(
                    "Selecione um paciente para continuar."
                )

            endereco = campo_endereco.get().strip()

            resultado = {
                "id_paciente": id_paciente,
                "endereco": endereco or None,
                "num_convenio": convenio_selecionado,
            }
            janela.destroy()

        def confirmar_com_tratamento() -> None:
            try:
                confirmar()
            except Exception as erro:
                messagebox.showerror(
                    "Dados inválidos",
                    str(erro),
                    parent=janela,
                )

        ctk.CTkButton(
            botoes,
            text="Cancelar",
            command=cancelar,
            width=140,
            height=40,
            fg_color="#334155",
            hover_color="#475569",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=1,
            padx=(10, 8),
        )

        ctk.CTkButton(
            botoes,
            text="Confirmar atualização",
            command=confirmar_com_tratamento,
            width=210,
            height=40,
            fg_color=self.COR_PRIMARIA,
            hover_color=self.COR_PRIMARIA_HOVER,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=2,
        )

        janela.protocol("WM_DELETE_WINDOW", cancelar)
        janela.grab_set()
        janela.after(100, campo_endereco.focus_set)
        self.wait_window(janela)

        if resultado is None:
            raise OperacaoCancelada()

        return resultado

    def _popular_tabela_dialogo(
        self,
        tabela: ttk.Treeview,
        registros: list[dict],
        colunas: tuple[str, ...],
        mapa_itens: dict[str, dict],
    ) -> None:
        """Preenche uma tabela de diálogo mantendo os registros originais mapeados."""
        for item in tabela.get_children():
            tabela.delete(item)

        mapa_itens.clear()

        for indice, registro in enumerate(registros):
            etiqueta = "linha_par" if indice % 2 == 0 else "linha_impar"
            item = tabela.insert(
                "",
                "end",
                values=[
                    self._formatar(registro.get(coluna))
                    for coluna in colunas
                ],
                tags=(etiqueta,),
            )
            mapa_itens[item] = registro

    def _configurar_colunas_dialogo(
        self,
        tabela: ttk.Treeview,
        colunas: tuple[str, ...],
        registros: list[dict],
    ) -> None:
        """Configura cabeçalhos e larguras das tabelas usadas nos formulários."""
        tabela["columns"] = colunas

        for coluna in colunas:
            titulo = coluna.replace("_", " ").title()
            valores = [
                self._formatar(registro.get(coluna))
                for registro in registros[:100]
            ]
            tabela.heading(
                coluna,
                text=titulo,
                anchor="center",
            )
            tabela.column(
                coluna,
                width=self._calcular_largura_coluna(
                    titulo,
                    valores,
                ),
                minwidth=110,
                anchor=self._definir_ancora_coluna(coluna),
                stretch=True,
            )

    def _abrir_procedimentos_atendimento(self) -> None:
        """Exibe atendimentos e seus procedimentos em uma única janela."""
        try:
            atendimentos = servicos.listar_atendimentos_para_selecao()
        except Exception as erro:
            messagebox.showerror(
                "Não foi possível carregar os atendimentos",
                str(erro),
                parent=self,
            )
            return

        if not atendimentos:
            messagebox.showinfo(
                "Procedimentos do atendimento",
                "Não existem atendimentos cadastrados.",
                parent=self,
            )
            return

        janela = ctk.CTkToplevel(self)
        janela.title("Procedimentos do atendimento")
        janela.geometry("1180x760")
        janela.minsize(960, 640)
        janela.configure(fg_color=self.COR_FUNDO)
        janela.transient(self)
        janela.grid_columnconfigure(0, weight=1)
        janela.grid_rowconfigure(3, weight=1)
        janela.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(
            janela,
            text="Procedimentos do atendimento",
            text_color=self.COR_TEXTO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=22,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=0,
            padx=24,
            pady=(18, 4),
            sticky="w",
        )

        ctk.CTkLabel(
            janela,
            text=(
                "Pesquise e selecione um atendimento para consultar "
                "todos os procedimentos vinculados."
            ),
            text_color=self.COR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
            ),
        ).grid(
            row=1,
            column=0,
            padx=24,
            pady=(0, 10),
            sticky="w",
        )

        busca = StringVar()
        campo_busca = ctk.CTkEntry(
            janela,
            textvariable=busca,
            placeholder_text="Pesquisar por ID, paciente, data ou unidade...",
            height=40,
            fg_color=self.COR_CARTAO,
            border_color=self.COR_BORDA,
            text_color=self.COR_TEXTO,
        )
        campo_busca.grid(
            row=2,
            column=0,
            padx=24,
            pady=(0, 10),
            sticky="ew",
        )

        quadro_atendimentos = ctk.CTkFrame(
            janela,
            fg_color=self.COR_SUPERFICIE,
            border_width=1,
            border_color=self.COR_BORDA,
            corner_radius=10,
        )
        quadro_atendimentos.grid(
            row=3,
            column=0,
            padx=24,
            pady=(0, 12),
            sticky="nsew",
        )
        quadro_atendimentos.grid_columnconfigure(0, weight=1)
        quadro_atendimentos.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            quadro_atendimentos,
            text="Atendimentos disponíveis",
            text_color=self.COR_TEXTO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=15,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=0,
            padx=14,
            pady=(12, 8),
            sticky="w",
        )

        colunas_atendimentos = (
            "id_atendimento",
            "paciente",
            "data_hora",
            "unidade",
        )
        tabela_atendimentos = ttk.Treeview(
            quadro_atendimentos,
            columns=colunas_atendimentos,
            show="headings",
            selectmode="browse",
            height=7,
        )
        tabela_atendimentos.grid(
            row=1,
            column=0,
            sticky="nsew",
        )
        barra_atendimentos = ttk.Scrollbar(
            quadro_atendimentos,
            orient="vertical",
            command=tabela_atendimentos.yview,
        )
        barra_atendimentos.grid(row=1, column=1, sticky="ns")
        tabela_atendimentos.configure(
            yscrollcommand=barra_atendimentos.set,
        )

        quadro_procedimentos = ctk.CTkFrame(
            janela,
            fg_color=self.COR_SUPERFICIE,
            border_width=1,
            border_color=self.COR_BORDA,
            corner_radius=10,
        )
        quadro_procedimentos.grid(
            row=5,
            column=0,
            padx=24,
            pady=(0, 12),
            sticky="nsew",
        )
        quadro_procedimentos.grid_columnconfigure(0, weight=1)
        quadro_procedimentos.grid_rowconfigure(1, weight=1)

        titulo_procedimentos = StringVar(
            value="Procedimentos do atendimento selecionado"
        )
        ctk.CTkLabel(
            quadro_procedimentos,
            textvariable=titulo_procedimentos,
            text_color=self.COR_TEXTO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=15,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=0,
            padx=14,
            pady=(12, 8),
            sticky="w",
        )

        colunas_procedimentos = (
            "id_procedimento",
            "procedimento",
            "quantidade",
            "tempo_real_minutos",
            "faturado",
            "observacao",
        )
        tabela_procedimentos = ttk.Treeview(
            quadro_procedimentos,
            columns=colunas_procedimentos,
            show="headings",
            selectmode="browse",
            height=8,
        )
        tabela_procedimentos.grid(
            row=1,
            column=0,
            sticky="nsew",
        )
        barra_procedimentos = ttk.Scrollbar(
            quadro_procedimentos,
            orient="vertical",
            command=tabela_procedimentos.yview,
        )
        barra_procedimentos.grid(row=1, column=1, sticky="ns")
        tabela_procedimentos.configure(
            yscrollcommand=barra_procedimentos.set,
        )

        mapa_atendimentos: dict[str, dict] = {}
        mapa_procedimentos: dict[str, dict] = {}
        texto_status = StringVar(value="Selecione um atendimento.")

        self._configurar_colunas_dialogo(
            tabela_atendimentos,
            colunas_atendimentos,
            atendimentos,
        )
        self._configurar_colunas_dialogo(
            tabela_procedimentos,
            colunas_procedimentos,
            [],
        )

        def filtrar_atendimentos(*_: object) -> None:
            termo = busca.get().strip().casefold()
            filtrados = [
                atendimento
                for atendimento in atendimentos
                if not termo
                or termo in " ".join(
                    self._formatar(valor)
                    for valor in atendimento.values()
                ).casefold()
            ]
            self._popular_tabela_dialogo(
                tabela_atendimentos,
                filtrados,
                colunas_atendimentos,
                mapa_atendimentos,
            )
            texto_status.set(
                f"{len(filtrados)} atendimento(s) encontrado(s)."
            )

            itens = tabela_atendimentos.get_children()
            if itens:
                tabela_atendimentos.selection_set(itens[0])
                tabela_atendimentos.focus(itens[0])
                carregar_procedimentos()
            else:
                self._popular_tabela_dialogo(
                    tabela_procedimentos,
                    [],
                    colunas_procedimentos,
                    mapa_procedimentos,
                )

        def carregar_procedimentos(_evento: object | None = None) -> None:
            selecao = tabela_atendimentos.selection()
            if not selecao:
                return

            atendimento = mapa_atendimentos.get(selecao[0])
            if atendimento is None:
                return

            id_atendimento = int(atendimento["id_atendimento"])

            try:
                procedimentos = servicos.listar_procedimentos_orm(
                    id_atendimento
                )
            except Exception as erro:
                messagebox.showerror(
                    "Não foi possível consultar os procedimentos",
                    str(erro),
                    parent=janela,
                )
                return

            self._configurar_colunas_dialogo(
                tabela_procedimentos,
                colunas_procedimentos,
                procedimentos,
            )
            self._popular_tabela_dialogo(
                tabela_procedimentos,
                procedimentos,
                colunas_procedimentos,
                mapa_procedimentos,
            )
            titulo_procedimentos.set(
                f"Procedimentos do atendimento {id_atendimento}"
            )
            texto_status.set(
                f"Consulta concluída: {len(procedimentos)} procedimento(s)."
            )
            self.status.configure(
                text=(
                    f"Consulta do atendimento {id_atendimento} concluída."
                ),
                text_color=self.COR_SUCESSO,
            )

        rodape = ctk.CTkFrame(
            janela,
            fg_color="transparent",
        )
        rodape.grid(
            row=6,
            column=0,
            padx=24,
            pady=(0, 18),
            sticky="ew",
        )
        rodape.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            rodape,
            textvariable=texto_status,
            text_color=self.COR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12,
            ),
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            rodape,
            text="Atualizar consulta",
            command=carregar_procedimentos,
            width=160,
            height=40,
            fg_color=self.COR_PRIMARIA,
            hover_color=self.COR_PRIMARIA_HOVER,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
                weight="bold",
            ),
        ).grid(row=0, column=1, padx=(10, 8))

        ctk.CTkButton(
            rodape,
            text="Fechar",
            command=janela.destroy,
            width=130,
            height=40,
            fg_color="#334155",
            hover_color="#475569",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
                weight="bold",
            ),
        ).grid(row=0, column=2)

        busca.trace_add("write", filtrar_atendimentos)
        tabela_atendimentos.bind(
            "<<TreeviewSelect>>",
            carregar_procedimentos,
        )
        janela.protocol("WM_DELETE_WINDOW", janela.destroy)

        filtrar_atendimentos()
        janela.grab_set()
        janela.after(100, campo_busca.focus_set)
        self.wait_window(janela)

    def _abrir_remocao_procedimento(self) -> None:
        """Permite selecionar atendimento e remover procedimento na mesma janela."""
        try:
            atendimentos = servicos.listar_atendimentos_para_selecao()
        except Exception as erro:
            messagebox.showerror(
                "Não foi possível carregar os atendimentos",
                str(erro),
                parent=self,
            )
            return

        if not atendimentos:
            messagebox.showinfo(
                "Remover procedimento",
                "Não existem atendimentos cadastrados.",
                parent=self,
            )
            return

        janela = ctk.CTkToplevel(self)
        janela.title("Remover procedimento")
        janela.geometry("1180x780")
        janela.minsize(960, 660)
        janela.configure(fg_color=self.COR_FUNDO)
        janela.transient(self)
        janela.grid_columnconfigure(0, weight=1)
        janela.grid_rowconfigure(3, weight=1)
        janela.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(
            janela,
            text="Remover procedimento",
            text_color=self.COR_TEXTO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=22,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=0,
            padx=24,
            pady=(18, 4),
            sticky="w",
        )

        ctk.CTkLabel(
            janela,
            text=(
                "Selecione um atendimento e depois um procedimento. "
                "Itens faturados são protegidos contra remoção."
            ),
            text_color=self.COR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
            ),
        ).grid(
            row=1,
            column=0,
            padx=24,
            pady=(0, 10),
            sticky="w",
        )

        busca = StringVar()
        campo_busca = ctk.CTkEntry(
            janela,
            textvariable=busca,
            placeholder_text="Pesquisar atendimento por ID, paciente, data ou unidade...",
            height=40,
            fg_color=self.COR_CARTAO,
            border_color=self.COR_BORDA,
            text_color=self.COR_TEXTO,
        )
        campo_busca.grid(
            row=2,
            column=0,
            padx=24,
            pady=(0, 10),
            sticky="ew",
        )

        quadro_atendimentos = ctk.CTkFrame(
            janela,
            fg_color=self.COR_SUPERFICIE,
            border_width=1,
            border_color=self.COR_BORDA,
            corner_radius=10,
        )
        quadro_atendimentos.grid(
            row=3,
            column=0,
            padx=24,
            pady=(0, 12),
            sticky="nsew",
        )
        quadro_atendimentos.grid_columnconfigure(0, weight=1)
        quadro_atendimentos.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            quadro_atendimentos,
            text="Atendimentos disponíveis",
            text_color=self.COR_TEXTO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=15,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=0,
            padx=14,
            pady=(12, 8),
            sticky="w",
        )

        colunas_atendimentos = (
            "id_atendimento",
            "paciente",
            "data_hora",
            "unidade",
        )
        tabela_atendimentos = ttk.Treeview(
            quadro_atendimentos,
            columns=colunas_atendimentos,
            show="headings",
            selectmode="browse",
            height=7,
        )
        tabela_atendimentos.grid(row=1, column=0, sticky="nsew")
        barra_atendimentos = ttk.Scrollbar(
            quadro_atendimentos,
            orient="vertical",
            command=tabela_atendimentos.yview,
        )
        barra_atendimentos.grid(row=1, column=1, sticky="ns")
        tabela_atendimentos.configure(
            yscrollcommand=barra_atendimentos.set,
        )

        quadro_procedimentos = ctk.CTkFrame(
            janela,
            fg_color=self.COR_SUPERFICIE,
            border_width=1,
            border_color=self.COR_BORDA,
            corner_radius=10,
        )
        quadro_procedimentos.grid(
            row=5,
            column=0,
            padx=24,
            pady=(0, 12),
            sticky="nsew",
        )
        quadro_procedimentos.grid_columnconfigure(0, weight=1)
        quadro_procedimentos.grid_rowconfigure(1, weight=1)

        titulo_procedimentos = StringVar(
            value="Procedimentos do atendimento selecionado"
        )
        ctk.CTkLabel(
            quadro_procedimentos,
            textvariable=titulo_procedimentos,
            text_color=self.COR_TEXTO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=15,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=0,
            padx=14,
            pady=(12, 8),
            sticky="w",
        )

        colunas_procedimentos = (
            "id_procedimento",
            "procedimento",
            "quantidade",
            "tempo_real_minutos",
            "faturado",
            "observacao",
        )
        tabela_procedimentos = ttk.Treeview(
            quadro_procedimentos,
            columns=colunas_procedimentos,
            show="headings",
            selectmode="browse",
            height=8,
        )
        tabela_procedimentos.grid(row=1, column=0, sticky="nsew")
        barra_procedimentos = ttk.Scrollbar(
            quadro_procedimentos,
            orient="vertical",
            command=tabela_procedimentos.yview,
        )
        barra_procedimentos.grid(row=1, column=1, sticky="ns")
        tabela_procedimentos.configure(
            yscrollcommand=barra_procedimentos.set,
        )

        mapa_atendimentos: dict[str, dict] = {}
        mapa_procedimentos: dict[str, dict] = {}
        texto_status = StringVar(
            value="Selecione um atendimento e um procedimento."
        )
        id_atendimento_atual: int | None = None

        self._configurar_colunas_dialogo(
            tabela_atendimentos,
            colunas_atendimentos,
            atendimentos,
        )
        self._configurar_colunas_dialogo(
            tabela_procedimentos,
            colunas_procedimentos,
            [],
        )

        def carregar_procedimentos(_evento: object | None = None) -> None:
            nonlocal id_atendimento_atual

            selecao = tabela_atendimentos.selection()
            if not selecao:
                id_atendimento_atual = None
                return

            atendimento = mapa_atendimentos.get(selecao[0])
            if atendimento is None:
                return

            id_atendimento_atual = int(
                atendimento["id_atendimento"]
            )

            try:
                procedimentos = servicos.listar_procedimentos_orm(
                    id_atendimento_atual
                )
            except Exception as erro:
                messagebox.showerror(
                    "Não foi possível consultar os procedimentos",
                    str(erro),
                    parent=janela,
                )
                return

            self._configurar_colunas_dialogo(
                tabela_procedimentos,
                colunas_procedimentos,
                procedimentos,
            )
            self._popular_tabela_dialogo(
                tabela_procedimentos,
                procedimentos,
                colunas_procedimentos,
                mapa_procedimentos,
            )
            titulo_procedimentos.set(
                f"Procedimentos do atendimento {id_atendimento_atual}"
            )
            texto_status.set(
                f"{len(procedimentos)} procedimento(s) disponível(is)."
            )

            itens = tabela_procedimentos.get_children()
            if itens:
                tabela_procedimentos.selection_set(itens[0])
                tabela_procedimentos.focus(itens[0])

        def filtrar_atendimentos(*_: object) -> None:
            termo = busca.get().strip().casefold()
            filtrados = [
                atendimento
                for atendimento in atendimentos
                if not termo
                or termo in " ".join(
                    self._formatar(valor)
                    for valor in atendimento.values()
                ).casefold()
            ]
            self._popular_tabela_dialogo(
                tabela_atendimentos,
                filtrados,
                colunas_atendimentos,
                mapa_atendimentos,
            )
            texto_status.set(
                f"{len(filtrados)} atendimento(s) encontrado(s)."
            )

            itens = tabela_atendimentos.get_children()
            if itens:
                tabela_atendimentos.selection_set(itens[0])
                tabela_atendimentos.focus(itens[0])
                carregar_procedimentos()
            else:
                self._popular_tabela_dialogo(
                    tabela_procedimentos,
                    [],
                    colunas_procedimentos,
                    mapa_procedimentos,
                )

        def remover() -> None:
            if id_atendimento_atual is None:
                messagebox.showwarning(
                    "Atendimento necessário",
                    "Selecione um atendimento para continuar.",
                    parent=janela,
                )
                return

            selecao = tabela_procedimentos.selection()
            if not selecao:
                messagebox.showwarning(
                    "Procedimento necessário",
                    "Selecione um procedimento para remover.",
                    parent=janela,
                )
                return

            procedimento = mapa_procedimentos.get(selecao[0])
            if procedimento is None:
                return

            if bool(procedimento.get("faturado")):
                messagebox.showwarning(
                    "Remoção não permitida",
                    "O procedimento selecionado já está faturado e não pode ser removido.",
                    parent=janela,
                )
                return

            id_procedimento = int(
                procedimento["id_procedimento"]
            )
            nome = str(
                procedimento.get("procedimento")
                or id_procedimento
            )

            confirmar = messagebox.askyesno(
                "Confirmar remoção",
                (
                    f"Remover o procedimento '{nome}' do atendimento "
                    f"{id_atendimento_atual}?"
                ),
                parent=janela,
            )
            if not confirmar:
                return

            try:
                resultado_remocao = servicos.remover_procedimento_orm(
                    id_atendimento=id_atendimento_atual,
                    id_procedimento=id_procedimento,
                )
            except Exception as erro:
                messagebox.showerror(
                    "Não foi possível remover o procedimento",
                    str(erro),
                    parent=janela,
                )
                return

            self._mostrar_resultados(
                "Remoção condicionada",
                resultado_remocao,
            )
            texto_status.set(
                f"Procedimento {id_procedimento} removido com sucesso."
            )
            messagebox.showinfo(
                "Procedimento removido",
                "A remoção foi concluída com sucesso.",
                parent=janela,
            )
            carregar_procedimentos()

        rodape = ctk.CTkFrame(
            janela,
            fg_color="transparent",
        )
        rodape.grid(
            row=6,
            column=0,
            padx=24,
            pady=(0, 18),
            sticky="ew",
        )
        rodape.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            rodape,
            textvariable=texto_status,
            text_color=self.COR_TEXTO_SECUNDARIO,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12,
            ),
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            rodape,
            text="Cancelar",
            command=janela.destroy,
            width=130,
            height=40,
            fg_color="#334155",
            hover_color="#475569",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
                weight="bold",
            ),
        ).grid(row=0, column=1, padx=(10, 8))

        ctk.CTkButton(
            rodape,
            text="Remover procedimento",
            command=remover,
            width=210,
            height=40,
            fg_color="#B91C1C",
            hover_color="#991B1B",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=13,
                weight="bold",
            ),
        ).grid(row=0, column=2)

        busca.trace_add("write", filtrar_atendimentos)
        tabela_atendimentos.bind(
            "<<TreeviewSelect>>",
            carregar_procedimentos,
        )
        tabela_procedimentos.bind(
            "<Double-1>",
            lambda _evento: remover(),
        )
        janela.protocol("WM_DELETE_WINDOW", janela.destroy)

        filtrar_atendimentos()
        janela.grab_set()
        janela.after(100, campo_busca.focus_set)
        self.wait_window(janela)

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
            dados = self._coletar_dados_atendimento(
                "Cadastrar novo atendimento"
            )

            return servicos.inserir_atendimento_orm(
                data_hora=dados["data_hora"],
                duracao_minutos=dados["duracao_minutos"],
                id_paciente=dados["id_paciente"],
                id_residente=dados["id_residente"],
                id_preceptor=dados["id_preceptor"],
                id_unidade=dados["id_unidade"],
            )

        self._executar(
            "Inserção de atendimento com ORM",
            operacao,
        )

    def _listar_atendimentos(self) -> None:
        def operacao() -> list[dict]:
            id_paciente, _descricao = self._selecionar_registro(
                "Selecionar paciente",
                servicos.listar_pacientes_para_selecao(),
                ("id_paciente", "id"),
            )
            return servicos.listar_atendimentos_orm(id_paciente)

        self._executar(
            "Atendimentos do paciente",
            operacao,
        )

    def _listar_procedimentos(self) -> None:
        """Abre a consulta padronizada de procedimentos por atendimento."""
        self._abrir_procedimentos_atendimento()

    def _atualizar_paciente(self) -> None:
        def operacao() -> list[dict]:
            dados = self._coletar_atualizacao_paciente()

            return servicos.atualizar_paciente_orm(
                id_paciente=int(dados["id_paciente"]),
                endereco=(
                    str(dados["endereco"])
                    if dados["endereco"] is not None
                    else None
                ),
                num_convenio=(
                    str(dados["num_convenio"])
                    if dados["num_convenio"] is not None
                    else None
                ),
            )

        self._executar(
            "Atualização do paciente",
            operacao,
        )

    def _remover_procedimento(self) -> None:
        """Abre o formulário único para remoção condicionada."""
        self._abrir_remocao_procedimento()

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
            dados = self._coletar_dados_atendimento(
                "Registrar atendimento completo"
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
                data_hora=dados["data_hora"],
                duracao_minutos=dados["duracao_minutos"],
                id_paciente=dados["id_paciente"],
                id_residente=dados["id_residente"],
                id_preceptor=dados["id_preceptor"],
                id_unidade=dados["id_unidade"],
                procedimentos_json=procedimentos,
            )

        self._executar(
            "Registro completo de atendimento",
            operacao,
        )

    def _reajustar_escala(self) -> None:
        def operacao() -> list[dict]:
            id_residente, _descricao = self._selecionar_registro(
                "Selecionar residente",
                servicos.listar_residentes_para_selecao(),
                ("id_residente", "id"),
            )

            return servicos.reajustar_escala(
                id_residente=id_residente,
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