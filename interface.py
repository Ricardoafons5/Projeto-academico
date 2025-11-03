import flet as ft
from database import Database
import logging

# Configura logging para capturar erros
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def criar_interface(page: ft.Page):
    db = Database()

    try:
        # Criar tabelas na inicialização
        db.criar_tabela_aluno()
        db.criar_tabela_visitante()
        db.criar_tabela_expositor()
        db.criar_tabela_professor()
    except Exception as e:
        logging.error(f"Erro ao criar tabelas: {e}")
        page.add(ft.Text(f"Erro ao iniciar o banco de dados: {e}", color=ft.Colors.RED))
        page.update()
        return

    page.title = "Sistema de Gerenciamento de Usuários"
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.PURPLE_700,
            on_primary=ft.Colors.WHITE,
            secondary=ft.Colors.PURPLE_300,
            background=ft.Colors.GREY_900,
        ),
        font_family="Roboto"
    )
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.GREY_900
    page.scroll = ft.ScrollMode.AUTO

    # Elementos do formulário
    nome = ft.TextField(
        label="Nome completo",
        width=250,
        border=ft.InputBorder.UNDERLINE,
        text_style=ft.TextStyle(color=ft.Colors.BLACK, size=14),
        label_style=ft.TextStyle(color=ft.Colors.PURPLE_300, size=12),
        prefix_icon=ft.Icons.PERSON,
    )
    email = ft.TextField(
        label="Email",
        width=250,
        border=ft.InputBorder.UNDERLINE,
        text_style=ft.TextStyle(color=ft.Colors.BLACK, size=14),
        label_style=ft.TextStyle(color=ft.Colors.PURPLE_300, size=12),
        prefix_icon=ft.Icons.EMAIL,
    )
    ra = ft.TextField(
        label="RA (se for da faculdade)",
        width=250,
        border=ft.InputBorder.UNDERLINE,
        text_style=ft.TextStyle(color=ft.Colors.BLACK, size=14),
        label_style=ft.TextStyle(color=ft.Colors.PURPLE_300, size=12),
        keyboard_type=ft.KeyboardType.NUMBER,
        prefix_icon=ft.Icons.BADGE,
        visible=True,
    )
    senha = ft.TextField(
        label="Senha",
        width=250,
        password=True,
        border=ft.InputBorder.UNDERLINE,
        text_style=ft.TextStyle(color=ft.Colors.BLACK, size=14),
        label_style=ft.TextStyle(color=ft.Colors.PURPLE_300, size=12),
        prefix_icon=ft.Icons.LOCK,
    )
    uc = ft.TextField(
        label="UC (unidade curricular)",
        width=250,
        border=ft.InputBorder.UNDERLINE,
        text_style=ft.TextStyle(color=ft.Colors.BLACK, size=14),
        label_style=ft.TextStyle(color=ft.Colors.PURPLE_300, size=12),
        prefix_icon=ft.Icons.BOOK,
        visible=True,
    )
    tipo_usuario = ft.RadioGroup(
        content=ft.Column(
            [
                ft.Radio(value="Estudante", label="Estudante", label_style=ft.TextStyle(color=ft.Colors.PURPLE_300, size=12)),
                ft.Radio(value="Visitante", label="Visitante", label_style=ft.TextStyle(color=ft.Colors.PURPLE_300, size=12)),
                ft.Radio(value="Docente", label="Docente", label_style=ft.TextStyle(color=ft.Colors.PURPLE_300, size=12)),
                ft.Radio(value="Expositor", label="Expositor", label_style=ft.TextStyle(color=ft.Colors.PURPLE_300, size=12)),
            ],
            tight=True,
            spacing=5,
        ),
        value="Estudante",
    )
    campo_excluir = ft.TextField(
        label="RA para excluir",
        width=250,
        border=ft.InputBorder.UNDERLINE,
        text_style=ft.TextStyle(color=ft.Colors.BLACK, size=14),
        label_style=ft.TextStyle(color=ft.Colors.PURPLE_300, size=12),
        prefix_icon=ft.Icons.DELETE,
    )
    feedback_text = ft.Text("", color=ft.Colors.PURPLE_300, size=14)

    # Tabela de usuários
    tabela_dados = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", color=ft.Colors.WHITE, size=12)),
            ft.DataColumn(ft.Text("Nome", color=ft.Colors.WHITE, size=12)),
            ft.DataColumn(ft.Text("Email", color=ft.Colors.WHITE, size=12)),
            ft.DataColumn(ft.Text("RA", color=ft.Colors.WHITE, size=12)),
            ft.DataColumn(ft.Text("UC", color=ft.Colors.WHITE, size=12)),
        ],
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        border=ft.border.all(1, ft.Colors.GREY_300),
        heading_text_style=ft.TextStyle(size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
        data_text_style=ft.TextStyle(size=12, color=ft.Colors.BLACK),
    )

    def on_tipo_usuario_change(e):
        try:
            is_academic = tipo_usuario.value in ["Estudante", "Docente"]
            ra.visible = is_academic
            uc.visible = is_academic
            campo_excluir.label = "RA" if is_academic else "Email"
            atualizar_tabela()
            page.update()
        except Exception as e:
            logging.error(f"Erro em on_tipo_usuario_change: {e}")
            feedback_text.value = f"Erro ao alterar tipo: {e}"
            feedback_text.color = ft.Colors.RED
            page.update()

    tipo_usuario.on_change = on_tipo_usuario_change

    def atualizar_tabela():
        try:
            tabela_dados.rows.clear()
            tipo = tipo_usuario.value
            row_bgcolor = "#f9f9f9"

            if tipo == "Estudante":
                tabela_dados.columns = [
                    ft.DataColumn(ft.Text("ID", color=ft.Colors.WHITE, size=12)),
                    ft.DataColumn(ft.Text("Nome", color=ft.Colors.WHITE, size=12)),
                    ft.DataColumn(ft.Text("Email", color=ft.Colors.WHITE, size=12)),
                    ft.DataColumn(ft.Text("RA", color=ft.Colors.WHITE, size=12)),
                    ft.DataColumn(ft.Text("UC", color=ft.Colors.WHITE, size=12)),
                ]
                registros = db.lista_aluno()
                for i, reg in enumerate(registros):
                    tabela_dados.rows.append(ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(reg[0]), color=ft.Colors.BLACK, size=12)),
                            ft.DataCell(ft.Text(reg[1], color=ft.Colors.BLACK, size=12)),
                            ft.DataCell(ft.Text(reg[2], color=ft.Colors.BLACK, size=12)),
                            ft.DataCell(ft.Text(str(reg[4]), color=ft.Colors.BLACK, size=12)),
                            ft.DataCell(ft.Text(reg[5] or "", color=ft.Colors.BLACK, size=12)),
                        ],
                        color=row_bgcolor if i % 2 == 0 else ft.Colors.WHITE
                    ))
            elif tipo == "Docente":
                tabela_dados.columns = [
                    ft.DataColumn(ft.Text("ID", color=ft.Colors.WHITE, size=12)),
                    ft.DataColumn(ft.Text("Nome", color=ft.Colors.WHITE, size=12)),
                    ft.DataColumn(ft.Text("Email", color=ft.Colors.WHITE, size=12)),
                    ft.DataColumn(ft.Text("RA", color=ft.Colors.WHITE, size=12)),
                    ft.DataColumn(ft.Text("UC", color=ft.Colors.WHITE, size=12)),
                ]
                registros = db.listar_professor()
                for i, reg in enumerate(registros):
                    tabela_dados.rows.append(ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(reg[0]), color=ft.Colors.BLACK, size=12)),
                            ft.DataCell(ft.Text(reg[1], color=ft.Colors.BLACK, size=12)),
                            ft.DataCell(ft.Text(reg[2], color=ft.Colors.BLACK, size=12)),
                            ft.DataCell(ft.Text(str(reg[4]), color=ft.Colors.BLACK, size=12)),
                            ft.DataCell(ft.Text(reg[5] or "", color=ft.Colors.BLACK, size=12)),
                        ],
                        color=row_bgcolor if i % 2 == 0 else ft.Colors.WHITE
                    ))
            elif tipo == "Visitante":
                tabela_dados.columns = [
                    ft.DataColumn(ft.Text("ID", color=ft.Colors.WHITE, size=12)),
                    ft.DataColumn(ft.Text("Nome", color=ft.Colors.WHITE, size=12)),
                    ft.DataColumn(ft.Text("Email", color=ft.Colors.WHITE, size=12)),
                ]
                registros = db.listar_visitantes()
                for i, reg in enumerate(registros):
                    tabela_dados.rows.append(ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(reg[0]), color=ft.Colors.BLACK, size=12)),
                            ft.DataCell(ft.Text(reg[1], color=ft.Colors.BLACK, size=12)),
                            ft.DataCell(ft.Text(reg[2], color=ft.Colors.BLACK, size=12)),
                        ],
                        color=row_bgcolor if i % 2 == 0 else ft.Colors.WHITE
                    ))
            elif tipo == "Expositor":
                tabela_dados.columns = [
                    ft.DataColumn(ft.Text("ID", color=ft.Colors.WHITE, size=12)),
                    ft.DataColumn(ft.Text("Nome", color=ft.Colors.WHITE, size=12)),
                    ft.DataColumn(ft.Text("Email", color=ft.Colors.WHITE, size=12)),
                ]
                registros = db.listar_expositor()
                for i, reg in enumerate(registros):
                    tabela_dados.rows.append(ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(reg[0]), color=ft.Colors.BLACK, size=12)),
                            ft.DataCell(ft.Text(reg[1], color=ft.Colors.BLACK, size=12)),
                            ft.DataCell(ft.Text(reg[2], color=ft.Colors.BLACK, size=12)),
                        ],
                        color=row_bgcolor if i % 2 == 0 else ft.Colors.WHITE
                    ))

            if not tabela_dados.rows:
                feedback_text.value = f"Nenhum {tipo.lower()} encontrado."
                feedback_text.color = ft.Colors.YELLOW
            else:
                feedback_text.value = ""
            page.update()
        except Exception as e:
            logging.error(f"Erro em atualizar_tabela: {e}")
            feedback_text.value = f"Erro ao listar: {e}"
            feedback_text.color = ft.Colors.RED
            page.update()

    def excluir_registro(e):
        try:
            tipo = tipo_usuario.value
            identificador = campo_excluir.value.strip()

            if not identificador:
                feedback_text.value = "Digite um RA ou Email para excluir."
                feedback_text.color = ft.Colors.RED
                page.update()
                return

            success, message = False, ""
            if tipo == "Estudante":
                success, message = db.excluir_aluno(identificador)
            elif tipo == "Docente":
                success, message = db.excluir_professor(identificador)
            elif tipo == "Visitante":
                success, message = db.excluir_visitante(identificador)
            elif tipo == "Expositor":
                success, message = db.excluir_expositor(identificador)

            feedback_text.value = message
            feedback_text.color = ft.Colors.GREEN if success else ft.Colors.RED
            if success:
                campo_excluir.value = ""
                atualizar_tabela()
            page.update()
        except Exception as e:
            logging.error(f"Erro em excluir_registro: {e}")
            feedback_text.value = f"Erro ao excluir: {e}"
            feedback_text.color = ft.Colors.RED
            page.update()

    def on_finalizar_click(e):
        try:
            nome_value = nome.value.strip()
            email_value = email.value.strip()
            senha_value = senha.value.strip()
            ra_value = ra.value.strip() if ra.visible else ""
            uc_value = uc.value.strip() if uc.visible else ""
            tipo = tipo_usuario.value

            if not nome_value or not email_value or not senha_value:
                feedback_text.value = "Preencha todos os campos obrigatórios."
                feedback_text.color = ft.Colors.RED
                page.update()
                return

            if tipo in ["Estudante", "Docente"]:
                if not ra_value or not ra_value.isdigit():
                    feedback_text.value = "Preencha o RA com um valor numérico."
                    feedback_text.color = ft.Colors.RED
                    page.update()
                    return
                ra_value = int(ra_value)

            success, message = False, ""
            if tipo == "Estudante":
                success, message = db.adicionar_aluno(nome_value, email_value, senha_value, ra_value, uc_value)
            elif tipo == "Docente":
                success, message = db.adicionar_professor(nome_value, email_value, senha_value, ra_value, uc_value)
            elif tipo == "Visitante":
                success, message = db.adicionar_visitante(nome_value, email_value, senha_value)
            elif tipo == "Expositor":
                success, message = db.adicionar_expositor(nome_value, email_value, senha_value)

            feedback_text.value = message
            feedback_text.color = ft.Colors.GREEN if success else ft.Colors.RED
            if success:
                nome.value = ""
                email.value = ""
                senha.value = ""
                ra.value = ""
                uc.value = ""
                atualizar_tabela()
            page.update()
        except Exception as e:
            logging.error(f"Erro em on_finalizar_click: {e}")
            feedback_text.value = f"Erro ao adicionar: {e}"
            feedback_text.color = ft.Colors.RED
            page.update()

    # Layout principal
    page.clean()
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            # Formulário à esquerda
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("Cadastro", size=18, color=ft.Colors.PURPLE_300, weight=ft.FontWeight.BOLD),
                                        nome,
                                        email,
                                        ra,
                                        senha,
                                        uc,
                                        ft.Text("Tipo de Usuário", size=14, color=ft.Colors.PURPLE_300),
                                        tipo_usuario,
                                        ft.Row(
                                            [
                                                ft.ElevatedButton(
                                                    text="Adicionar",
                                                    bgcolor=ft.Colors.PURPLE_600,
                                                    color=ft.Colors.WHITE,
                                                    width=120,
                                                    height=40,
                                                    on_click=on_finalizar_click,
                                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                                                ),
                                                ft.ElevatedButton(
                                                    text="Excluir",
                                                    bgcolor=ft.Colors.PURPLE_600,
                                                    color=ft.Colors.WHITE,
                                                    width=120,
                                                    height=40,
                                                    on_click=excluir_registro,
                                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            spacing=10,
                                        ),
                                        campo_excluir,
                                        feedback_text,
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=15,
                                ),
                                width=350,
                                padding=20,
                                bgcolor=ft.Colors.WHITE,
                                border_radius=10,
                            ),
                            # Tabela à direita
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("Lista de Usuários", size=18, color=ft.Colors.PURPLE_300, weight=ft.FontWeight.BOLD),
                                        ft.ListView(
                                            controls=[tabela_dados],
                                            expand=True,
                                            padding=10,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    spacing=10,
                                ),
                                width=400,
                                padding=20,
                                bgcolor=ft.Colors.WHITE,
                                border_radius=10,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                        expand=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=[ft.Colors.PURPLE_700, ft.Colors.PINK_500],
            ),
            padding=20,
            expand=True,
        )
    )

    # Inicializar a tabela
    atualizar_tabela()
    page.update()

ft.app(target=criar_interface)
