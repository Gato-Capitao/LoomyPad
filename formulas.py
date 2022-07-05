
def tp_otherStats(base, up, lvl, prsnlt, final):
    resultado = ((((final*10)*100)-((((((2*base+up)*4)*lvl)/4)+500)*prsnlt))*4)/(lvl*prsnlt)
    
    if resultado >= 0:
        if resultado >=200:
            return 200
        else:
            return round(resultado)
    else:
        return 0
    
def tp_energy(base, up, lvl, prsnlt, final):
    resultado = ((((final*prsnlt)*65)-((((((2*base+up)*4)*lvl)/4)+80*65)*prsnlt))*4)/(lvl*prsnlt)
    
    if resultado >= 0:
        if resultado >=200:
            return 200
        else:
            return round(resultado)
    else:
        return 0

def tp_health(base, up, lvl, final):
    resultado = (((final*100)-(((((2*base+up)*4)*lvl)/4)+((lvl+10)*100)))*4)/lvl
    
    if resultado >= 0:
        if resultado >=200:
            return 200
        else:
            return round(resultado)
    else:
        return 0