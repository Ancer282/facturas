import os
import math
from datetime import datetime

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, Line
from kivy.core.window import Window

try:
    from plyer import share
except ImportError:
    share = None

Window.clearcolor = (1, 1, 1, 1)
Window.size = (380, 680)

# Diccionario con listas ordenadas por volumen de usuarios en Perú
ENTIDADES_PERU = {
    'Bancos': (
        'BCP',
        'BBVA',
        'Interbank',
        'Scotiabank',
        'Banco de la Nación',
        'Banco Pichincha',
        'BanBif',
        'Mibanco'
    ),
    'Cajas Municipales': (
        'Caja Arequipa',
        'Caja Huancayo',
        'Caja Piura',
        'Caja Cusco',
        'Caja Trujillo',
        'Caja Ica',
        'Caja Maynas'
    ),
    'Financieras': (
        'Financiera Crediscotia',
        'Financiera Confianza',
        'Financiera Compartamos',
        'Financiera Qapaq',
        'Financiera Proempresa',
        'Financiera Surgir'
    )
}

class TicketWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            Color(0.8, 0.8, 0.8, 1)
            self.line = Line(rectangle=(self.x, self.y, self.width, self.height), width=1.2)
        self.bind(pos=self._update, size=self._update)

    def _update(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.line.rectangle = (self.x, self.y, self.width, self.height)


class FormularioScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        lbl_titulo = Label(
            text="EMISIÓN DE FACTURA / TICKET",
            font_size=18,
            bold=True,
            size_hint_y=None,
            height=35,
            color=(0.1, 0.1, 0.1, 1)
        )
        main_layout.add_widget(lbl_titulo)

        form_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        form_grid.bind(minimum_height=form_grid.setter('height'))

        # 1. Selección de Tipo de Entidad (Por defecto: Bancos)
        form_grid.add_widget(Label(
            text="1. Tipo de Entidad:", 
            size_hint_y=None, 
            height=22, 
            color=(0.2, 0.2, 0.2, 1),
            bold=True
        ))
        
        self.spinner_tipo = Spinner(
            text='Bancos',
            values=('Bancos', 'Cajas Municipales', 'Financieras'),
            size_hint_y=None,
            height=40,
            background_normal='',
            background_color=(0.2, 0.3, 0.5, 1),
            color=(1, 1, 1, 1)
        )
        self.spinner_tipo.bind(text=self.actualizar_lista_entidades)
        form_grid.add_widget(self.spinner_tipo)

        # 2. Selección de la Institución Financiera específica
        form_grid.add_widget(Label(
            text="2. Nombre de la Entidad:", 
            size_hint_y=None, 
            height=22, 
            color=(0.2, 0.2, 0.2, 1),
            bold=True
        ))
        
        self.spinner_entidad = Spinner(
            text=ENTIDADES_PERU['Bancos'][0],
            values=ENTIDADES_PERU['Bancos'],
            size_hint_y=None,
            height=40,
            background_normal='',
            background_color=(0.15, 0.45, 0.85, 1),
            color=(1, 1, 1, 1)
        )
        form_grid.add_widget(self.spinner_entidad)

        # 3. Monto de Operación
        form_grid.add_widget(Label(
            text="3. Monto de la Operación (S/):", 
            size_hint_y=None, 
            height=22, 
            color=(0.2, 0.2, 0.2, 1),
            bold=True
        ))
        self.input_monto = TextInput(
            multiline=False,
            input_filter='float',
            hint_text="Ej: 100, 150, 200",
            size_hint_y=None,
            height=40,
            font_size=16
        )
        self.input_monto.bind(text=self.actualizar_comision)
        form_grid.add_widget(self.input_monto)

        self.lbl_comision_info = Label(
            text="Comisión: S/ 0.00\n(Regla: S/ 1.00 por cada S/ 100.00)",
            size_hint_y=None,
            height=40,
            color=(0.3, 0.3, 0.3, 1),
            bold=True
        )
        form_grid.add_widget(self.lbl_comision_info)

        main_layout.add_widget(form_grid)

        btn_preview = Button(
            text="VER VISTA PREVIA DEL TICKET",
            size_hint_y=None,
            height=50,
            background_color=(0.1, 0.65, 0.35, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        btn_preview.bind(on_release=self.ir_a_vista_previa)
        main_layout.add_widget(btn_preview)

        self.add_widget(main_layout)

    def actualizar_lista_entidades(self, spinner, text):
        """Actualiza las opciones del segundo desplegable según el tipo elegido."""
        nuevas_opciones = ENTIDADES_PERU.get(text, ())
        self.spinner_entidad.values = nuevas_opciones
        if nuevas_opciones:
            self.spinner_entidad.text = nuevas_opciones[0]

    def calcular_comision(self, monto):
        if monto <= 0:
            return 0.00
        return float(math.ceil(monto / 100.0))

    def actualizar_comision(self, instance, value):
        try:
            monto = float(value)
            com = self.calcular_comision(monto)
            self.lbl_comision_info.text = f"Comisión: S/ {com:.2f}\n(Regla: S/ 1.00 por cada S/ 100.00)"
        except ValueError:
            self.lbl_comision_info.text = "Comisión: S/ 0.00\n(Regla: S/ 1.00 por cada S/ 100.00)"

    def ir_a_vista_previa(self, instance):
        monto_str = self.input_monto.text.strip()
        if not monto_str:
            return

        try:
            monto = float(monto_str)
            if monto <= 0:
                return
            comision = self.calcular_comision(monto)
            entidad = self.spinner_entidad.text

            vista_screen = self.manager.get_screen('vista_previa')
            vista_screen.cargar_datos(entidad, monto, comision)
            self.manager.current = 'vista_previa'
        except ValueError:
            pass


class VistaPreviaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.monto = 0.0
        self.comision = 0.0
        self.entidad = ""

        layout_principal = BoxLayout(orientation='vertical', padding=15, spacing=10)

        scroll = ScrollView(size_hint=(1, 1))
        self.ticket = TicketWidget(orientation='vertical', padding=20, spacing=8, size_hint_y=None)
        self.ticket.bind(minimum_height=self.ticket.setter('height'))

        self.construir_ticket()
        scroll.add_widget(self.ticket)
        layout_principal.add_widget(scroll)

        grid_acciones = GridLayout(cols=2, spacing=8, size_hint_y=None, height=100)
        
        btn_modificar = Button(text="Modificar", background_color=(0.5, 0.5, 0.5, 1), bold=True)
        btn_modificar.bind(on_release=self.modificar_datos)

        btn_guardar = Button(text="Guardar", background_color=(0.1, 0.6, 0.3, 1), bold=True)
        btn_guardar.bind(on_release=self.guardar_comprobante)

        btn_compartir = Button(text="Compartir", background_color=(0.1, 0.5, 0.85, 1), bold=True)
        btn_compartir.bind(on_release=self.compartir_comprobante)

        btn_imprimir = Button(text="Imprimir", background_color=(0.85, 0.45, 0.1, 1), bold=True)
        btn_imprimir.bind(on_release=self.imprimir_comprobante)

        grid_acciones.add_widget(btn_modificar)
        grid_acciones.add_widget(btn_guardar)
        grid_acciones.add_widget(btn_compartir)
        grid_acciones.add_widget(btn_imprimir)

        layout_principal.add_widget(grid_acciones)
        self.add_widget(layout_principal)

    def construir_ticket(self):
        self.ticket.clear_widgets()

        self.lbl_encabezado = Label(
            text="COMPROBANTE DE FACTURA\n---------------------------------------",
            font_size=15,
            bold=True,
            color=(0, 0, 0, 1),
            halign='center',
            size_hint_y=None,
            height=38
        )
        self.ticket.add_widget(self.lbl_encabezado)

        self.lbl_fecha = Label(
            text="",
            font_size=11,
            color=(0.3, 0.3, 0.3, 1),
            halign='center',
            size_hint_y=None,
            height=20
        )
        self.ticket.add_widget(self.lbl_fecha)

        self.ticket.add_widget(Label(text="- "*22, color=(0.6, 0.6, 0.6, 1), size_hint_y=None, height=15))

        self.lbl_banco_val = Label(text="", color=(0, 0, 0, 1), font_size=13, size_hint_y=None, height=22, halign='left')
        self.lbl_monto_val = Label(text="", color=(0, 0, 0, 1), font_size=13, size_hint_y=None, height=22, halign='left')
        self.lbl_comision_val = Label(text="", color=(0, 0, 0, 1), font_size=13, size_hint_y=None, height=22, halign='left')

        self.ticket.add_widget(self.lbl_banco_val)
        self.ticket.add_widget(self.lbl_monto_val)
        self.ticket.add_widget(self.lbl_comision_val)

        self.ticket.add_widget(Label(text="=======================", color=(0, 0, 0, 1), size_hint_y=None, height=15))

        self.lbl_total_val = Label(
            text="",
            font_size=15,
            bold=True,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=30
        )
        self.ticket.add_widget(self.lbl_total_val)

        lbl_pie = Label(
            text="---------------------------------------\n¡Gracias por su preferencia!",
            font_size=11,
            color=(0.4, 0.4, 0.4, 1),
            halign='center',
            size_hint_y=None,
            height=35
        )
        self.ticket.add_widget(lbl_pie)

    def cargar_datos(self, entidad, monto, comision):
        self.entidad = entidad
        self.monto = monto
        self.comision = comision
        total = monto + comision
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        self.lbl_fecha.text = f"Fecha: {fecha_actual}"
        self.lbl_banco_val.text = f"Entidad: {entidad}"
        self.lbl_monto_val.text = f"Monto Operación: S/ {monto:.2f}"
        self.lbl_comision_val.text = f"Comisión (1 cada 100): S/ {comision:.2f}"
        self.lbl_total_val.text = f"TOTAL A PAGAR: S/ {total:.2f}"

    def obtener_o_generar_imagen(self):
        nombre = f"factura_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        ruta = os.path.abspath(nombre)
        self.ticket.export_to_png(ruta)
        return ruta

    def modificar_datos(self, instance):
        self.manager.current = 'formulario'

    def guardar_comprobante(self, instance):
        ruta = self.obtener_o_generar_imagen()
        self.lbl_fecha.text += f"\n[ Guardado: {os.path.basename(ruta)} ]"

    def compartir_comprobante(self, instance):
        ruta = self.obtener_o_generar_imagen()
        if share:
            share.share_file(filepath=ruta, title="Compartir Factura")
        else:
            self.lbl_fecha.text += f"\n[ Listo para compartir: {os.path.basename(ruta)} ]"

    def imprimir_comprobante(self, instance):
        ruta = self.obtener_o_generar_imagen()
        if os.name == 'posix':
            os.system(f"am start -a android.intent.action.SEND -t image/png --eu android.intent.extra.STREAM file://{ruta}")
        elif os.name == 'nt':
            os.startfile(ruta, "print")


class FacturaApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FormularioScreen(name='formulario'))
        sm.add_widget(VistaPreviaScreen(name='vista_previa'))
        return sm

if __name__ == '__main__':
    FacturaApp().run()