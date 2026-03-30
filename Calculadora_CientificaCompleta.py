import kivy
import threading
import math
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy_garden.graph import Graph, LinePlot
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock


class Calculadora(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="horizontal", **kwargs)
        self.historico = []
        self.criar_calculadora()

    def criar_calculadora(self):
        self.clear_widgets()

        # --- LAYOUT ESQUERDO: DISPLAY + BOTÕES ---
        layout_calc = BoxLayout(orientation="vertical", size_hint=(0.7,1))

        # DISPLAY
        self.display = TextInput(
            multiline=False,
            readonly=True,
            halign="right",
            font_size=50,
            size_hint=(1,0.2),
            background_color=(1,1,1,1),
            foreground_color=(0,0,0,1)
        )
        layout_calc.add_widget(self.display)

        # BOTÕES - tabela personalizada
        botoes = [
            "sin","cos","tan","log",
            "7","8","9","⌫",
            "4","5","6","C",
            "1","2","3",".",
            "0","(",")","=",
            "+","-","*","/",
            "π","x","x²","GRAF"
        ]

        grid = GridLayout(cols=4)
        for b in botoes:
            botao = Button(text=b, font_size=24)
            botao.bind(on_press=self.on_click)
            grid.add_widget(botao)

        layout_calc.add_widget(grid)
        self.add_widget(layout_calc)

        # --- LAYOUT DIREITA: HISTÓRICO VERTICAL COM FUNDO CINZA ---
        self.scroll = ScrollView(size_hint=(0.3,1))
        with self.scroll.canvas.before:
            Color(0.9,0.9,0.9,1)
            self.rect = Rectangle(size=self.scroll.size, pos=self.scroll.pos)
        self.scroll.bind(size=lambda instance, value: setattr(self.rect, 'size', value))
        self.scroll.bind(pos=lambda instance, value: setattr(self.rect, 'pos', value))

        self.historico_box = BoxLayout(orientation="vertical", size_hint_y=None)
        self.historico_box.bind(minimum_height=self.historico_box.setter('height'))
        self.scroll.add_widget(self.historico_box)
        self.add_widget(self.scroll)

        for item in self.historico:
            self.adicionar_historico(item)

    def on_click(self, instance):
        texto = instance.text

        if texto == "C":
            self.display.text = ""
        elif texto == "⌫":
            self.display.text = self.display.text[:-1]
        elif texto == "π":
            self.display.text += str(math.pi)
        elif texto == "x":
            self.display.text += "x"
        elif texto == "x²":
            self.display.text += "**2"
        elif texto in ["sin","cos","tan","log"]:
            self.display.text += texto + "("
        elif texto == "=":
            try:
                resultado = eval(self.display.text, {
                    "sin": lambda x: math.sin(math.radians(x)),
                    "cos": lambda x: math.cos(math.radians(x)),
                    "tan": lambda x: math.tan(math.radians(x)),
                    "log": math.log10
                })
                self.adicionar_historico(self.display.text + " = " + str(resultado))
                self.display.text = str(resultado)
            except:
                self.display.text = "Erro"
        elif texto == "GRAF":
            threading.Thread(target=self.calcular_grafico).start()
        else:
            self.display.text += texto

    def adicionar_historico(self, entrada):
        def usar_resultado(instance):
            self.display.text = entrada.split('=')[-1].strip()
        lbl = Button(text=entrada, size_hint_y=None, height=30)
        lbl.bind(on_press=usar_resultado)
        self.historico_box.add_widget(lbl)
        self.historico.append(entrada)

    # --- THREAD DE CÁLCULO DO GRÁFICO ---
    def calcular_grafico(self):
        pontos = []
        for i in range(-100,100):
            x = i/10  # eixo x em radianos para gráficos
            try:
                # para gráfico usamos radianos, independente do display
                y = eval(self.display.text, {
                    "x": x,
                    "sin": math.sin,
                    "cos": math.cos,
                    "tan": math.tan,
                    "log": math.log10
                })
                pontos.append((x,y))
            except:
                pass
        Clock.schedule_once(lambda dt: self.mostrar_grafico(pontos))

    def mostrar_grafico(self, pontos):
        layout = BoxLayout(orientation="vertical")
        graph = Graph(xlabel='x', ylabel='y', xmin=-10, xmax=10, ymin=-10, ymax=10)
        plot = LinePlot()
        plot.points = pontos
        graph.add_plot(plot)

        botao_voltar = Button(text="Voltar", size_hint=(1,0.1))
        botao_voltar.bind(on_press=lambda x: self.criar_calculadora())

        layout.add_widget(graph)
        layout.add_widget(botao_voltar)

        self.clear_widgets()
        self.add_widget(layout)

class CalcApp(App):
    def build(self):
        self.title = "Calculadora Científica Completa"  # Título da janela
        return Calculadora()

CalcApp().run()
