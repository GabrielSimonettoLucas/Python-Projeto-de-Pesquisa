import sqlite3
import os
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem, TwoLineListItem, OneLineAvatarIconListItem, TwoLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.screenmanager import ScreenManager, Screen

#============

class firstwindow(Screen):
    pass

class secondwindow(Screen):
    pass


kv = Builder.load_file('gui.kv')

#=============
clear= lambda: os.system('cls')
#=============
conn = sqlite3.connect('Perguntas_Respostas.db')
c = conn.cursor()
#=============
def precioneparacontinuar():
    input("\nPrecione ENTER para Continuar\n")
#=============
def menu_inicial():
    print("██    ██    ████████    ███████    ██████     ██████  ")   
    print("██    ██       ██       ██         ██   ██    ██   ██ ")
    print("██    ██       ██       █████      ██████     ██████  ")
    print("██    ██       ██       ██         ██         ██   ██ ")
    print(" ██████        ██       ██         ██         ██   ██ ")
    clear()
#=============
def selecao():
    print("Selecione a ação desejada:\n")
    print("1-Criar Lista\n")
    print("2-Visualizar as listas criadas\n")
    print("9-Encerrar aplicação\n")
    decisao= int(input(" "))
    precioneparacontinuar
    clear()
    return decisao
#============
def criarpergunta():
    enunciado=input("Informe o enunciado\n")
    colecao=input("Informe o tipo de coleção:\n VI, VC, MI, MC\n")
    tam_x=input("Informe o tamanho de X:\n")
    tam_y=0
    if colecao == "MI" or colecao == "MC":
        tam_y=input("Informe o tamanho de Y:\n")
    tipo_atv=input("Informe o tipo da atividade:\n1,2,3,4")
    dicas=input("informe as dicas")
    c.execute("INSERT INTO atividade (enunciado, tamanho_x, tamanho_y, tipo_colecao, dicas, tipo_atividade) VALUES (?,?,?,?,?,?)",(enunciado,tam_x,tam_y,colecao,dicas,tipo_atv))
    conn.commit
    c.execute("SELECT atividade_id FROM atividade ORDER BY atividade_id DESC LIMIT 1")
    atv_id = c.fetchone()
    return(atv_id)
#============
def relacionar_atv_lista(lista_id, atv_id):
    c.execute("INSERT INTO lista_atividades (atividade_atividade_id, lista_lista_id) VALUES (?,?)", (atv_id, lista_id))
    conn.commit
#============                                                               
def criarlista():
    print("Insira o titulo da lista:\n")
    titulo = input("")
    print("Insira a descrição da lista\n")
    descricao = input()
    c.execute("INSERT INTO lista (titulo, descricao) VALUES (?,?)",(titulo, descricao))
    conn.commit()
    clear()
    print("Lista criada, gostaria de adicionar perguntas a está lista ?\n S & N")
    while True:
        decisao=input("\n")
        match decisao:
            case "S":
                c.execute("SELECT lista_id FROM lista ORDER BY lista_id DESC LIMIT 1")
                lista_id = c.fetchone()
                clear()
                atv_id = criarpergunta()
                relacionar_atv_lista(lista_id[0], atv_id[0])
            case "N":
                break                 
#============
def criarlistagui(tit, desc):
    c.execute("INSERT INTO lista (titulo, descricao) VALUES (?,?)",(tit, desc))
    conn.commit()
#============
def visualizarlistas():
    c.execute("SELECT titulo, lista_id from lista")
    conn.commit()
    print(c.fetchall())
#============
def ultimalistacriada():
    c.execute("SELECT lista_id FROM lista ORDER BY lista_id DESC LIMIT 1")
    lista_id = c.fetchone()
    return lista_id
#============
class GuiProjetoApp(MDApp):    
    sm = ScreenManager()
    sm.add_widget(firstwindow(name='primeira'))
    sm.add_widget(secondwindow(name='segunda'))
    rel_id = list([])
    ultima_lista_id = list([])
    

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return self.sm

    def on_start(self):
        c.execute("SELECT atividade.atividade_id FROM atividade")
        lista_id = c.fetchall()
        c.execute("SELECT enunciado FROM atividade")
        lista_nome = c.fetchall()
        #print(int(z[0]))
        for i in range(len(lista_id)):
            b= lista_nome[i]
            z = lista_id[i]
            self.sm.get_screen("segunda").ids.lista.add_widget(
            #self.root.ids.lista.add_widget(
                TwoLineAvatarIconListItem(id = f"{int(z[0])}", text=f"{str(b[0])}", secondary_text= "Não Selecionado")
            )

    def presser (self, pressed, list_id):
        if pressed.secondary_text != "selecionado":
            pressed.secondary_text="selecionado"
            pressed.secondary_text_color = 1, 0, 0, 1
            self.rel_id.append(list_id)
            print(self.rel_id)
        else:
            pressed.secondary_text="Não selecionado"
            pressed.secondary_text_color = 1, 1, 1, 1
            self.rel_id.remove(list_id)
            print(self.rel_id)


    titulo = ObjectProperty(None)
    descricao = ObjectProperty(None)

    visualizarlistas()

    def press_lista (self):
        #titulo = ObjectProperty(None)
        #descricao = ObjectProperty(None)
        
        titulo = self.sm.get_screen("primeira").ids.titulo.text
        descricao= self.sm.get_screen("primeira").ids.descricao.text

        print(f"{titulo}, {descricao}")
        criarlistagui(titulo, descricao)
        self.ultima_lista_id = ultimalistacriada()
        self.ultima_lista_id = int(self.ultima_lista_id[0])
        print(self.ultima_lista_id)
        self.sm.get_screen("primeira").ids.titulo.text = ""
        self.sm.get_screen("primeira").ids.descricao.text = ""

    def relacionar_lista(self):
        for i in range (len(self.rel_id)):
            id = self.rel_id[i]
            id = int(id[0])
            print(self.ultima_lista_id, id)
            relacionar_atv_lista(self.ultima_lista_id, id)
            pass

    def popup(self, popup):
        popup.ids.label_pop_up.text = "oi"
        popup.open()


#============
#============
if __name__ == '__main__':
    menu_inicial()
    c.execute("INSERT INTO atividade (enunciado, tamanho_x, tamanho_y, tipo_colecao, dicas, tipo_atividade) VALUES ('Declare um vetor de CHARs', 2, 0, 'VI', 'd',1)")
    conn.commit()
    GuiProjetoApp().run()
  
conn.close()
