import requests
import pandas as pd
from bs4 import BeautifulSoup

def webScrapLoomian():
    def limpar(loomian):
        nome = loomian.replace("\xa0", " ")
        
        return nome
    
    pagina = requests.get("https://loomian-legacy.fandom.com/wiki/List_of_Loomians_by_base_stats")
    sopa = BeautifulSoup(pagina.content, "html.parser")
    tabela = sopa.find(id="mw-content-text")

    loomiansDados = []
    primeira = False

    for i in tabela.find_all("tr"):
        dadosModelo = {"id":0, "nome":"", "hp":0, "energy":0, "atkM":0, "defM":0, "atkR":0, "defR":0, "speed":0}
        tds = 0
        
        for a in i.find_all("td"):
            if a.b != None:
                numeracao = str(a.b)
                for caracter in [">", "<", "b", "/"]:
                    numeracao = numeracao.replace(caracter, "")
                dadosModelo["id"] = numeracao
            
            elif a.find("a") != None:
                if not primeira:
                    dadosModelo["nome"] = a.find("a").get("title")
                    primeira = True
                else:
                    primeira = False 
            
            elif a.get("style") != None:
                stats = str(a)[44:-6]
                if tds == 0:
                    dadosModelo["hp"]= stats
                elif tds == 1:
                    dadosModelo["energy"]= stats
                elif tds == 2:
                    dadosModelo["atkM"]= stats
                elif tds == 3:
                    dadosModelo["defM"]= stats
                elif tds == 4:
                    dadosModelo["atkR"]= stats
                elif tds ==5:
                    dadosModelo["defR"]= stats
                else:
                    dadosModelo["speed"]= stats
                tds +=1 
        if dadosModelo["id"] != 0:
            loomiansDados.append(dadosModelo)
            
    return pd.DataFrame({
        "Id":[a["id"] for a in loomiansDados],
        "Loomian":[limpar(a["nome"]) for a in loomiansDados],
        "Health":[a["hp"] for a in loomiansDados],
        "Energy":[a["energy"] for a in loomiansDados],
        "Melee ATK":[a["atkM"] for a in loomiansDados],
        "Melee DEF":[a["defM"] for a in loomiansDados],
        "Ranged ATK":[a["atkR"] for a in loomiansDados],
        "Ranged DEF":[a["defR"] for a in loomiansDados],
        "Speed":[a["speed"] for a in loomiansDados]})
