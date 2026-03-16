import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import math


class Calculadora(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1  # layout principal

        # DISPLAY GRANDE
        self.display = TextInput(
            multiline=False,
            readonly=True,
            halign="right",
            font_size=60,
            size_hint=(1, 0.2)
        )

        self.add_widget(self.display)

        # GRID DOS BOTÕES
        grid = GridLayout(cols=4)

        botoes = [
            "7","8","9","/",
            "4","5","6","*",
            "1","2","3","-",
            "0",".","=","+",
            "(" ,")","C","⌫",
            "sin","cos","tan","log"
        ]

        for b in botoes:
            botao = Button(text=b, font_size=24)
            botao.bind(on_press=self.on_click)
            grid.add_widget(botao)

        self.add_widget(grid)


    def on_click(self, instance):

        texto = instance.text

        if texto == "C":
            self.display.text = ""

        elif texto == "⌫":
            self.display.text = self.display.text[:-1]

        elif texto == "=":
            try:
                expressao = self.display.text

                resultado = eval(expressao, {
                    "sin": math.sin,
                    "cos": math.cos,
                    "tan": math.tan,
                    "log": math.log10
                })

                self.display.text = str(resultado)

            except:
                self.display.text = "Erro"

        elif texto in ["sin","cos","tan","log"]:
            self.display.text += texto + "("

        else:
            self.display.text += texto


class CalculadoraApp(App):
    def build(self):
        return Calculadora()


CalculadoraApp().run()