import pandas as pd
pathTeste = r"C:\Users\e-enzo.ramos\Desktop\Códigos\Python\Testes\Teste.txt"
pathListaCriterios = r'C:\Users\e-enzo.ramos\Documents\Critérios de Microdados\Cursos de Engenharia 2021.txt'

def tratarCriterios(pathListaCriterios, caixa_alta=False):
    with open(pathListaCriterios, 'r', encoding='utf-8') as documento:
        critério = documento.read().splitlines()
        critério.sort()
    
    listaArrumada = []
    if (caixa_alta):
        [listaArrumada.append(curso.upper()) for curso in critério if curso not in listaArrumada]
    else:
        [listaArrumada.append(curso) for curso in critério if curso not in listaArrumada]

    return listaArrumada

listaArrumada = tratarCriterios(pathListaCriterios)

with open(pathTeste, 'w') as writer:
     for linha in listaArrumada:   
        writer.write(linha + '\n')