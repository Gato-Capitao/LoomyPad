"""LoomyPad"""

"""
Calcula os Tps de um loomian do jogo Loomian Legacy,
usa web scrapping para pegar os dados base,
é controlado por uma GUI.
"""

#bibliotecas
import PySimpleGUI as sg
import pyperclip as cb
from pickle import load, dump
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from scrapLegacy import webScrapLoomian
from formulas import tp_energy, tp_health, tp_otherStats

#funcoes
def loadPaste():
    """Cria a pasta data caso ela não exista, se o icone não existir também o baixará"""
    endereco = str(os.getcwd())+"\data"
    def baixarIcone(url, endereco):
        """Baixa o icone do programa"""
        pag = requests.get(url)
        with open(endereco+"\loomyPadIcon.ico", "wb") as arquivo:
            arquivo.write(pag.content)
    
    if not "data" in os.listdir(os.getcwd()):
        os.mkdir(endereco)
    if not "loomyPadIcon.ico" in os.listdir(endereco):
        baixarIcone("https://filedropper.com/d/s/download/txeX2OtA6v6bLkCCnkgFF5JSbfAB6I", endereco)


def getVariables():
    """Define os valores das variaveis e retorna se a ação foi concluida com sucesso
    
    return: Valor da personalidade"""
    
    def getPersonality():
        "Retorna o valor da personalidade"
        valuesPersonality = {
            "No effect":10,
            "Bad":9,
            "Very bad":8,
            "Good":11,
            "Very good":12}
        
        return valuesPersonality[valor["list_prsnlt"]]
    
    try:
        if valor["list_prsnlt"] in personalities:
            stats["base"] = int(valor["input_base"])
            stats["final"] = int(valor["input_final"])
            stats["lvl"] = int(valor["input_lvl"])
            stats["prsnlt"] = getPersonality()
            return True
    except ValueError:
        return False


#Carregar data base
loadPaste()
try:#Verifica se já existe um data frame salvo
    with open("data\scrapData.pkl", "rb") as arquivo:
        df = load(arquivo)
except:
    with open("data\scrapData.pkl", "wb") as arquivo:
        df = webScrapLoomian()
        dump(df, arquivo)

#Variaveis
stats = {"prsnlt":10, "base":0, "lvl":45, "tp":0, "final":0}
loomians = {nome:posicao for posicao, nome in enumerate(df["Loomian"])}
listaLoomians = [a for a in df["Loomian"]]
up = [
    {"simbolo":"⋆", "valor":"0", "valores":[0]}, 
    {"simbolo":"☆", "valor":"1-10", "valores":[1, 10]}, 
    {"simbolo":"☆☆", "valor":"11-20", "valores":[11, 20]},
    {"simbolo":"☆☆☆", "valor":"21-30", "valores":[21, 30]},
    {"simbolo":"☆☆☆☆", "valor":"31-38", "valores":[31, 38]},
    {"simbolo":"☆☆☆☆☆", "valor":"39", "valores":[39]},
    {"simbolo":"★★★★★", "valor":"40", "valores":[40]}]
personalities = [
    "No effect", 
    "Very bad", 
    "Bad", 
    "Good", 
    "Very good"]

#Design
grey = {'BACKGROUND': '#0C0D11',
        'TEXT': '#FFFFFF',
        'INPUT': '#FFFFFF',
        'TEXT_INPUT': '#000000',
        'SCROLL': '#070A32',
        'BUTTON': ('white', '#070A32'),
        'PROGRESS': ('#01826B', '#D0D0D0'),
        'BORDER': 1,
        'SLIDER_DEPTH': 0,
        'PROGRESS_DEPTH': 0}
sg.theme_add_new("Cinza", grey)
sg.theme("Cinza")

def lGetBase():
    """Retorna a janela que serve para encontrar o valor base
    
    Variaveis:
        list - layout: Layout principal
        list - f_dados: Frame em que fica os valores e os botões para copiar, que ficam dentro do layout principal"""
    f_dados = [
        [sg.Text("Health:", size=(12,1)), sg.Text("", key="text_health", size=(4,1), text_color="green"), sg.Button("Copy", key="button_health")],
        [sg.Text("Energy:", size=(12,1)), sg.Text("", key="text_energy", size=(4,1), text_color="yellow"), sg.Button("Copy",key="button_energy")],
        [sg.Text("Melee ATK:", size=(12,1)), sg.Text("", key="text_matk", size=(4,1), text_color="red"), sg.Button("Copy",key="button_matk")],
        [sg.Text("Melee DEF:", size=(12,1)), sg.Text("", key="text_mdef", size=(4,1), text_color="orange"), sg.Button("Copy",key="button_mdef")],
        [sg.Text("Ranged ATK:", size=(12,1)), sg.Text("", key="text_ratk", size=(4,1), text_color="blue"), sg.Button("Copy",key="button_ratk")],
        [sg.Text("Ranged DEF:", size=(12,1)), sg.Text("", key="text_rdef", size=(4,1), text_color="purple"), sg.Button("Copy",key="button_rdef")],
        [sg.Text("Speed:", size=(12,1)), sg.Text("", key="text_speed", size=(4,1), text_color="pink"), sg.Button("Copy",key="button_speed")],]
    layout = [
        [sg.Text("Loomian:"), sg.Combo(listaLoomians, enable_events=True, key="gcombo")],
        [sg.VPush()],
        [sg.Push(), sg.Frame("Stats", layout=f_dados), sg.Push()],
        [sg.Push(), sg.Button("Load", key="gbutton_carregar"), sg.Button("Update list", key="gbutton_load")]]
    
    return sg.Window("LoomyPad", layout=layout, grab_anywhere=True, finalize=True, icon="data\loomyPadIcon.ico")

def telaPrincipal():
    """Retorna a janela principal
    
    Variaveis:
        list - layout: lista com os elementos do PySimpleGUi que formam layout principal
        list - estrelas/status/formula: Frames que ficam dentro do layout principal"""
    estrelas = [
        [sg.Push(),sg.Text("Stars:", size=(4,1)), sg.Text("★★★★★", key="text_ups", size=(14, 1)), sg.Push()],
        [sg.Text("", size=(5, 1))],
        [sg.Text("Up:"), sg.Text("40", key="text_upValue")],
        [sg.Push(), sg.Button("<", key="button_leftArrow", size=(5, 1), visible=True), sg.Button(">", key="button_rightArrow", size=(5, 1), visible=True), sg.Push()]]
    status = [
        [sg.Text("Level:", size=(9, 1)), sg.Input(key="input_lvl", size=(5, 1))],
        [sg.Text("Base:", size=(9, 1)), sg.Input(key="input_base", size=(5, 1), default_text=""), sg.Button("Get", key="button_get")],
        [sg.Text("Final:", size=(9, 1)), sg.Input(key="input_final", size=(5, 1))],
        [sg.Text("Personality:", size=(9, 1)), sg.Combo(personalities, size=(9, 1), key="list_prsnlt", default_value="No effect")]]
    formulas = [
        [sg.Radio("Health", key="radio_health", group_id="radio_statsgroup", enable_events=True), sg.Radio("Energy", key="radio_energy", group_id="radio_statsgroup", enable_events=True), sg.Radio("Other Stats", key="radio_otherStats", group_id="radio_statsgroup", enable_events=True, default=True)]
    ]
    layout = [
        [sg.Push(), sg.Text("LoomyPad"), sg.Push()],
        [sg.Text("")],
        [sg.Push(), sg.Frame("Values", status), sg.Frame("Ups", estrelas), sg.Push()],
        [sg.Push(), sg.Frame("Stats", formulas), sg.Push()],
        [sg.Push(), sg.Text("Tps ≅"), sg.Text("", key="text_tp", visible=True), sg.Text(""), sg.Push()],
        [sg.Push(), sg.Button("Calculate", key="button_calculate"), sg.Push()]]
    return sg.Window("LoomyPad", layout=layout, grab_anywhere=True, resizable=True, finalize=True, icon="data\loomyPadIcon.ico")

def tela():
    """
    Observa eventos que acontecem na GUI, faz as GUI rodar
    O while observa a todo momento se alguma atualização foi feita
    e entra na condicional correspondente com o evento
    """
    global evento, valor, up, df, stars
    stars = 6
    formula = "otherStats"
    def changeStars():
        """Muda o simbolo das estrelas no layout, e o valor dos ups também
        Variaveis:
            int - stars:Variavel usada para encontrar o id do simbolo da estrela
            dict - up: Dicionario que armazena os simbolos e valores das estrelas que representam os ups"""
        
        janela["text_ups"].update(up[stars].get("simbolo"))
        janela["text_upValue"].update(up[stars].get("valor"))

    while True:
        janela, evento, valor = sg.read_all_windows()
        if evento == sg.WIN_CLOSED:
            """
            Se o botão da GUI X de fechar for ativado, deverá quebrar o laço de repetição
            """
            break
        
        elif janela == jjanela:
            if evento == "button_leftArrow" or evento=="button_rightArrow":
                """Muda os simbolos das estrelas que representam os Up de acordo com o botão pressionado"""
                if evento=="button_leftArrow" and stars > 0:
                    stars-=1
                    changeStars()
                elif evento=="button_rightArrow" and stars < 6:
                    stars+=1
                    changeStars()
            elif evento == "button_get":
                """Esconde a janela principal e abre a janela dos stats"""
                janela.hide()
                try:
                    jGetBase.UnHide()
                except:
                    jGetBase = lGetBase()
            elif evento == "button_calculate":
                """
                Pega as variaveis, executa o calculo e atualiza os valores na GUI     
                
                Variaveis:
                    bool - variaveis: Se a função getVariables der erro terá valor False, senão, True. 
                                    Previne que o código não dê erro se o úsuario digitar algo de errado na GUI.
                    
                    str - formula: Representa qual formula deve ser usada.
                """
                variavies = getVariables()
                if variavies:#Verifica se todos os valores estão ok
                    resultsTps = ""
                    if formula == "otherStats":
                        for pup in up[stars].get("valores"):
                            resultsTps+= str(tp_otherStats(stats["base"], pup, stats["lvl"], stats["prsnlt"], stats["final"])) + " - "
                    elif formula == "health":
                        for pup in up[stars].get("valores"):
                            resultsTps+= str(tp_health(stats["base"], pup, stats["lvl"], stats["final"])) + " - "
                    else:
                        for pup in up[stars].get("valores"):
                            resultsTps+= str(tp_energy(stats["base"], pup, stats["lvl"], stats["prsnlt"], stats["final"])) + " - "
                    
                    janela["text_tp"].update(resultsTps.strip()[:len(resultsTps)-2])
            elif evento == "radio_otherStats" or evento == "radio_energy" or evento == "radio_health":
                """Define o valor da variavel formula de acordo com o evento"""
                formula = {"radio_otherStats":"otherStats", "radio_energy":"energy", "radio_health":"health"}[evento]
        
        elif janela == jGetBase:
            
            if evento == "gbutton_carregar" and valor["gcombo"].capitalize() in listaLoomians:
                """
                Define os valores base e os mostra na tela, atualizando os valores na janela
                
                Variaveis:
                    dict - baseStats: Carrega os valores base, que se liga com o botão
                """
                
                loomianId = loomians[str(valor["gcombo"]).capitalize()]
                
                baseStats = {
                "button_health":str(df["Health"].get(loomianId)), 
                "button_energy":str(df["Energy"].get(loomianId)),
                "button_matk":str(df["Melee ATK"].get(loomianId)),
                "button_mdef":str(df["Melee DEF"].get(loomianId)),
                "button_ratk":str(df["Ranged ATK"].get(loomianId)),
                "button_rdef":str(df["Ranged DEF"].get(loomianId)),
                "button_speed":str(df["Speed"].get(loomianId))}
                janela["text_health"].update(str(baseStats["button_health"]))
                janela["text_energy"].update(str(baseStats["button_energy"]))
                janela["text_matk"].update(str(baseStats["button_matk"]))
                janela["text_mdef"].update(str(baseStats["button_mdef"]))
                janela["text_ratk"].update(str(baseStats["button_ratk"]))
                janela["text_rdef"].update(str(baseStats["button_rdef"]))
                janela["text_speed"].update(str(baseStats["button_speed"]))
            elif evento == "button_health" or evento == "button_energy" or evento == "button_matk" or evento == "button_mdef" or evento == "button_ratk" or evento == "button_rdef" or evento == "button_speed":
                """
                Copiar valor que está ligado com o evento, no dicionario baseStats
                
                Variaveis:
                    dict - baseStats: Usado para buscar o valor de acordo com o evento
                """
                jGetBase.hide()
                jjanela.UnHide()
                cb.copy(baseStats[evento])        
            elif evento == "gbutton_load":
                """
                Salva um data frame com os dados dos loomians que foram buscados usando Web Scrapping
                """
                loadPaste()
                with open("data\scrapData.pkl", "wb") as arquivo:
                    df = webScrapLoomian()
                    dump(df, arquivo)

#Processos
jjanela, jGetBase = telaPrincipal(), []
tela()
