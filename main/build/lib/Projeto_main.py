import sqlite3
import os
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import builder

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
class LayoutGrade(Widget):

    titulo = ObjectProperty(None)
    descricao = ObjectProperty

    def press (self):
        titulo = self.titulo.text
        descricao= self.descricao.text

        print(f"{titulo}, {descricao}")
        criarlistagui(titulo, descricao)
        self.titulo.text = ""
        self.titulo.descricao = ""

        visualizarlistas()


    pass
#============
class GuiApp(App):
    def build(self):
        return LayoutGrade()
#============
if __name__ == '__main__':
    menu_inicial()
    GuiApp().run()
'''
while True:

    decisao=selecao()
    match decisao:
        case 1:
            criarlista()
            precioneparacontinuar()
            clear()
        case 2:
            visualizarlistas()
            precioneparacontinuar()
            clear()
        case 9:
            break
'''        
conn.close()
