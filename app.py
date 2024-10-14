import json
import math
from pprint import pprint

def primero(): 
    todo = []
    with open('ejercicio.json', 'r+') as f: 
        try: 
            todo = json.load(f)
        except: 
            todo = f.readlines()
            todo = list(todo)
        if len(todo) == 0: 
            try: 
                r = str(input('Por favor, escribe la lista de los intervalos separados por espacios: \n'))
                r = r.split(' ')
                r = list(map(lambda x: int(x), r))
            except: 
                print('¡Oh no! Ingresaste un dato que no era un número, ¡No te equivoques!')
                return
            minimo = min(r)
            maximo = max(r)
            n = len(r)
            rango = maximo - minimo 
            k = 1 + 3.3 * math.log(n, 10)
            amplitud = rango / k
            if amplitud > int(amplitud): 
                amplitud += 1
                amplitud = int(amplitud)
            lista = {}
            for esto in r: 
                try: lista[esto] += 1
                except: lista[esto] = 1
            real = []
            para = 0
            while True: 
                if minimo > maximo: break
                para = minimo + amplitud - 1
                clase = {
                    'minimo': minimo, 
                    'maximo': para
                }
                minimo = para + 1
                real.append(clase)
            oficial = [{'clase': real}]
            oficial[0]['fi'] = []
            for esto in real: 
                numero = 0
                for i in range(esto['minimo'], esto['maximo'] + 1): 
                    try: numero += lista[i]
                    except: continue
                oficial[0]['fi'].append(numero)
            parte = []
            for esto in oficial[0]['fi']: 
                if len(parte) >= 1: parte.append(esto + parte[-1])
                else: parte.append(esto)
            oficial[0]['fa'] = parte
            oficial[0]['xi'] = list(map(lambda x: (x['minimo'] + x['maximo']) / 2, oficial[0]['clase']))
            oficial[0]['fi.xi'] = [(xi * fi) for xi, fi in zip(oficial[0]['fi'], oficial[0]['xi'])]
            oficial[0]['fsr'] = list(map(lambda x: x / oficial[0]['fa'][-1], oficial[0]['fi']))
            oficial[0]['far'] = list(map(lambda x: x / oficial[0]['fa'][-1], oficial[0]['fa']))
            oficial[0]['fsr%'] = list(map(lambda x: x * 100, oficial[0]['fsr']))
            oficial[0]['far%'] = list(map(lambda x: x * 100, oficial[0]['far']))
            oficial[0]['fi.xi^2'] = [(xi * fixi) for xi, fixi in zip(oficial[0]['fi.xi'], oficial[0]['xi'])]
            todo = oficial
            json.dump(oficial, f, indent=4)
    mostrar_tabla(todo[0])
    total = todo[0]['fa'][-1]
    a = todo[0]['clase'][0]['maximo'] - todo[0]['clase'][0]['minimo'] + 1
    media = sum(todo[0]['fi.xi']) / total
    print(f'Media aritmética: {media}')
    calculo = total / 2
    fa = 0
    for esto in todo[0]['fa']: 
        if esto >= calculo: 
            fa = esto
            break
    indice = todo[0]['fa'].index(fa)
    li = todo[0]['clase'][indice]['minimo']
    fi_menos = todo[0]['fa'][indice - 1]
    fi = todo[0]['fi'][indice]
    mediana = li + ((calculo - fi_menos) / fi) * a
    print(f'Mediana: {mediana}')
    lugares_modales = buscar_modales(todo[0]['fi'])
    modales = []
    for esto in lugares_modales: 
        li = todo[0]['clase'][esto]['minimo']
        fi = todo[0]['fi'][esto]
        try: fi_menos = todo[0]['fi'][esto - 1]
        except: fi_menos = 0
        try: fi_mas = todo[0]['fi'][esto + 1]
        except: fi_mas = 0
        d1 = fi - fi_menos
        d2 = fi - fi_mas
        modal = li + (d1 / (d1 + d2)) * a
        modales.append(modal)
    print(f'Modales: {modales}')
    varianza = (sum(todo[0]['fi.xi^2']) / total) - (media**2)
    print(f'Varianza: {varianza}')
    desviacion = math.sqrt(varianza)
    print(f'Desviación estándar: {desviacion}')
    cuartiles = []
    for i in range(1, 5): 
        q = obtencion(todo[0], ((25 * i) / 100) * total)
        cuartiles.append(q)
    intercuartil = cuartiles[2] - cuartiles[0]
    gran_total = total[0]['fa'][-1]
    p75 = obtencion(total[0], (75 / 100) * gran_total)
    p25 = obtencion(total[0], (25 / 100) * gran_total)
    p90 = obtencion(total[0], (90 / 100) * gran_total)
    p10 = obtencion(total[0], (10 / 100) * gran_total)
    curtosis = ((p75 - p25) / (p90 - p10)) * 0.5
    p65 = obtencion(total[0], (65 / 100) * gran_total)
    print(f'P65: {round(p65, 4)}')
    
    print(f'Rango intercuartil: {round(intercuartil, 4)}')
    print('++++++++++++++++++++++++++++++++++++++++++++')
    print('**********************************************')
    print('Clases: ')
    pprint(todo[0]["clase"])
    print('Frecuencias: ')
    pprint(todo[0]["fi"])
    print('**********************************************')

def buscar_modales(fi : list): 
    lista = []
    maximo = max(fi)
    for i in range(len(fi)): 
        if fi[i] == maximo: 
            lista.append(i)
    return lista

def obtencion(lista, numero): 
    fa = lista['fa']
    fi = lista['fi']
    clase = lista['clase']
    indice = 0
    for esto in fa: 
        if esto >= numero: 
            indice = fa.index(esto)
            break
    fa_numero = fa[indice - 1]
    fi_numero = fi[indice]
    li = clase[indice]['minimo']
    amplitud = clase[0]['maximo'] - clase[0]['minimo']
    esto = li + ((numero - fa_numero) / fi_numero) * amplitud
    return esto

def mostrar_tabla(todo : dict): 
    total = len(todo['clase'])
    llaves = todo.keys()
    texto = '|'
    for esto in llaves: texto += f' {esto} |'
    print(len(texto) * '-')
    print(texto)
    for i in range(total): 
        texto = '|'
        for esto in llaves: 
            if esto == 'clase': 
                minimo = todo[esto][i]['minimo']
                maximo = todo[esto][i]['maximo']
                texto += f' {minimo}-{maximo} |'
            else: texto += f' {todo[esto][i]} |'
        print(len(texto) * '-')
        print(texto)
    print(len(texto) * '-')


def main(): 
    primero()

if __name__ == '__main__': 
    main()