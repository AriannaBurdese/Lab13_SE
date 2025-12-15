import flet as ft
from UI.alert import AlertManager

class View:
    def __init__(self, page: ft.Page):
        # Page
        self.page = page
        self.page.title = "Lab13_SE"
        self.page.horizontal_alignment = "center"
        self.page.theme_mode = ft.ThemeMode.DARK

        # Alert
        self.alert = AlertManager(page)

        # Controller
        self.controller = None

    def show_alert(self, messaggio):
        self.alert.show_alert(messaggio)

    def set_controller(self, controller):
        self.controller = controller

    def update(self):
        self.page.update()

    def load_interface(self):
        """ Crea e aggiunge gli elementi di UI alla pagina e la aggiorna. """
        # Intestazione
        self.txt_titolo = ft.Text(value="Analisi Cromosomi", size=38, weight=ft.FontWeight.BOLD)

        # Sezione 1
        self.btn_grafo = ft.ElevatedButton(text="Crea Grafo", on_click=self.controller.handle_graph)
        self.lista_visualizzazione_1 = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        # Sezione 2
        self.txt_name = ft.TextField(
            label="Soglia",
            width=200,
            hint_text="Soglia (s)"
        )
        self.btn_conta_edges = ft.ElevatedButton(text="Conta Archi", on_click=self.controller.handle_conta_edges)
        row2 = ft.Row([self.txt_name, self.btn_conta_edges],
                      alignment=ft.MainAxisAlignment.CENTER)

        self.lista_visualizzazione_2 = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        # Sezione 3
        self.btn_ricerca = ft.ElevatedButton(text="Cerca Cammino", on_click=self.controller.handle_ricerca)
        self.lista_visualizzazione_3 = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        # --- Toggle Tema ---
        self.toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=self.cambia_tema)

        # --- Layout della pagina ---
        self.page.add(
            self.toggle_cambia_tema,

            # Titolo
            self.txt_titolo,
            ft.Divider(),

            # Sezione 1
            self.btn_grafo,
            self.lista_visualizzazione_1,
            ft.Divider(),

            # Sezione 2
            row2,
            self.lista_visualizzazione_2,
            ft.Divider(),

            # Sezione 3
            self.btn_ricerca,
            self.lista_visualizzazione_3
        )

        self.page.scroll = "adaptive"
        self.page.update()

    def cambia_tema(self, e):
        """ Cambia tema scuro/chiaro """
        self.page.theme_mode = ft.ThemeMode.DARK if self.toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        self.toggle_cambia_tema.label = "Tema scuro" if self.toggle_cambia_tema.value else "Tema chiaro"
        self.page.update()
