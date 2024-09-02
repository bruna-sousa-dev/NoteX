import flet as ft
from typing import Dict
import datetime
import locale

# locale.locale_alias
locale.setlocale(locale.LC_ALL, 'pt_BR')

class App:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.page.scroll = ft.ScrollMode.HIDDEN
        self.page.title = 'NoteX'
        self.page.theme_mode = ft.ThemeMode.DARK
        self.main()

    def main(self):        

        def go_to_home(e):
            self.page.controls.pop()
            layout.content.controls[-1] = notes()
            self.page.add(layout)

        def note_details(note: Dict[str, str] = dict()):
            if note.get('date'):
                date = note['date'].strftime('%b. %d, %Y')
            else:
                date = datetime.datetime.today().strftime('%b. %d, %Y')
            
            def change_note(e):
                if e.control.data is not None:
                    for sn in saved_notes:
                        if sn['id'] == e.control.data:
                            sn['title'] = title.value
                            sn['content'] = content.value
                            sn['date'] = datetime.datetime.today()
                else:
                    saved_notes.append(
                        {
                            'id': saved_notes[-1]['id'] + 1,
                            'title': title.value,
                            'date': datetime.datetime.today(),
                            'content': content.value,
                            'color': 'amber',
                            'expand': False,
                        }
                    )
            
            def enable_save_button(e):
                save_button.disabled = False
                save_button.update()

            return ft.Container(
                expand = True,
                padding = ft.padding.all(20),
                content = ft.Column(
                    controls = [
                        ft.IconButton(
                            icon = ft.icons.ARROW_BACK, 
                            on_click = go_to_home
                        ),
                        title := ft.TextField(
                            value = note.get('title'), 
                            max_length = 50, 
                            text_style = ft.TextStyle(size = 20, weight = ft.FontWeight.BOLD), 
                            border = ft.InputBorder.UNDERLINE, 
                            hint_text = 'Qual será o título da sua nota?', 
                            hint_style = ft.TextStyle(italic = True), 
                            content_padding = ft.padding.only(bottom = 20), 
                            on_change = enable_save_button
                        ),
                        ft.Text(value = date),
                        content := ft.TextField(
                            value = note.get('content'), 
                            text_style = ft.TextStyle(size = 20), 
                            border = ft.InputBorder.NONE, 
                            multiline = True, 
                            min_lines = 5, 
                            hint_text = 'Digite sua anotação aqui...', 
                            hint_style = ft.TextStyle(italic = True), 
                            on_change = enable_save_button
                        ),
                        save_button := ft.ElevatedButton(
                            text = 'Salvar alterações', 
                            disabled = True, 
                            data = note.get('id'), 
                            on_click = change_note
                        ),
                    ],
                ),
            )
        
        def apply_shadow(e):
            if e.control.shadow:
                e.control.shadow = None
            else:
                e.control.shadow = ft.BoxShadow(
                    blur_radius = 20,
                    color = e.control.bgcolor,
                    blur_style = ft.ShadowBlurStyle.OUTER,
                )
            e.control.update()

        def open_note(e):
            self.page.controls.pop()

            for sn in saved_notes:
                if sn['id'] == e.control.data:
                    self.page.add(note_details(note = sn))
                    return

            self.page.add(note_details())

        def notes():
            return ft.ResponsiveRow(
                columns = 2,
                controls = [
                    ft.Container(
                        col = 2 if sn['expand'] else 1,
                        bgcolor = sn['color'],
                        padding = ft.padding.all(20),
                        border_radius = ft.border_radius.all(10),
                        shadow = None,
                        content = ft.Column(
                            controls = [
                                ft.Text(
                                    value = sn['title'], 
                                    style = ft.TextThemeStyle.HEADLINE_SMALL, 
                                    max_lines = 2, 
                                    overflow = ft.TextOverflow.ELLIPSIS
                                ),
                                ft.Text(
                                    value = sn['date'].strftime('%b. %d, %Y'), 
                                    style = ft.TextThemeStyle.BODY_SMALL
                                ),
                            ],
                        ),
                        on_hover = apply_shadow,
                        data = sn['id'],
                        on_click = open_note
                    ) for sn in saved_notes
                ],
            )
        
        # Lista de notas pré criadas simulando nosso banco de dados
        saved_notes = [
            {
                'id': 1,
                'title': 'Lista de Compras',
                'date': datetime.date(2023, 12, 24),
                'content': 'Comprar itens essenciais para a semana: leite, pão, ovos, frutas.',
                'color': 'blue',
                'expand': True,
            },
            {
                'id': 2,
                'title': 'Ideias para o Projeto',
                'date': datetime.date(2023, 12, 25),
                'content': '1. Pesquisar tendências de design.\n2. Esboçar layouts iniciais.\n3. Definir tecnologias a serem utilizadas.',
                'color': 'green',
                'expand': False,
            },
            {
                'id': 3,
                'title': 'Reunião com a Equipe',
                'date': datetime.date(2023, 12, 26),
                'content': 'Agendar reunião com a equipe para discutir os progressos do projeto.',
                'color': 'indigo',
                'expand': False,
            },
            {
                'id': 4,
                'title': 'Aniversário da Maria',
                'date': datetime.date(2024, 1, 10),
                'content': 'Comprar presente e preparar surpresa para a festa de aniversário da Maria.',
                'color': 'purple',
                'expand': False,
            },
            {
                'id': 5,
                'title': 'Leitura Recomendada',
                'date': datetime.date(2024, 1, 15),
                'content': 'Livro recomendado: "A Arte da Guerra" de Sun Tzu.',
                'color': 'orange',
                'expand': False,
            },
            {
                'id': 6,
                'title': 'Metas para o Ano Novo',
                'date': datetime.date(2024, 1, 1),
                'content': '1. Fazer exercícios regularmente.\n2. Aprender uma nova habilidade.\n3. Viajar para um lugar diferente.',
                'color': 'pink',
                'expand': True,
            },
            {
                'id': 7,
                'title': 'Ligar para o Dentista',
                'date': datetime.date(2024, 1, 5),
                'content': 'Marcar consulta para check-up odontológico.',
                'color': 'cyan',
                'expand': True,
            },
            {
                'id': 8,
                'title': 'Pensamentos do Dia',
                'date': datetime.date(2024, 1, 2),
                'content': 'Refletir sobre as conquistas do ano passado e definir novos objetivos para o futuro.',
                'color': 'brown',
                'expand': True,
            },
            {
                'id': 9,
                'title': 'Receita de Jantar',
                'date': datetime.date(2024, 1, 8),
                'content': 'Experimentar a nova receita de risoto de cogumelos para o jantar.',
                'color': 'grey',
                'expand': False,
            },
            {
                'id': 10,
                'title': 'Agradecimentos',
                'date': datetime.date(2023, 12, 31),
                'content': 'Agradecer pelas experiências do ano que passou e expressar gratidão aos amigos e familiares.',
                'color': 'indigo',
                'expand': False,
            },
        ]

        layout = ft.Container(
            padding = ft.padding.all(20),
            content = ft.Column(
                controls = [
                    ft.Text(
                        value = 'NoteX', 
                        style = ft.TextThemeStyle.DISPLAY_LARGE
                    ),
                    ft.Column(
                        controls = [notes()],
                    ),
                ]
            ),
        )

        self.page.floating_action_button = ft.FloatingActionButton(
            icon = ft.icons.ADD,
            shape = ft.CircleBorder(),
            tooltip = 'Adicionar uma nota',
            bgcolor = ft.colors.INDIGO,
            on_click = open_note,
        )

        self.page.add(layout)

if __name__ == '__main__':
    ft.app(target = App, assets_dir = 'assets')
 