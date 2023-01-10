import pandas as pd

#para atualizar os dados deve-se mudar: pathANO, pathLISTADECRITERIOS e o filtro dos cursos
pathTeste = r"C:\Users\e-enzo.ramos\Desktop\Códigos\Python\Testes\%s.xlsx"
path2021=r"C:\Users\e-enzo.ramos\Desktop\Dados\ME\INEP\Censo do Ensino Superior - Microdados\Microdados do Censo da Educação Superior 2021\dados\MICRODADOS_CADASTRO_CURSOS_2021.csv"
path2020 = r"C:\Users\e-enzo.ramos\Desktop\Dados\ME\INEP\Censo do Ensino Superior - Microdados\Microdados do Censo da Educação Superior 2020\dados\MICRODADOS_CADASTRO_CURSOS_2020.csv"
pathCursosSTEAM = r'C:\Users\e-enzo.ramos\Documents\Critérios de Microdados\Cursos STEAM.txt'
pathCursosDeEngenharia2021 = r'C:\Users\e-enzo.ramos\Documents\Critérios de Microdados\Cursos de Engenharia 2021.txt'
pathCursosDeEngenharia2020 = r'C:\Users\e-enzo.ramos\Documents\Critérios de Microdados\Cursos de Engenharia 2020.txt'
pathRotulosDeEngenharia = r'C:\Users\e-enzo.ramos\Documents\Critérios de Microdados\Rótulos de Engenharia.txt'


#criando e tratando a lista com os critérios
with open(pathCursosDeEngenharia2020, 'r', encoding='utf-8') as documento:
    critério = documento.readlines()
    critério.sort()

for c in critério:
    critério.append(c.replace("\n", ""))
    critério.remove(c)
    

#criando os dataframes com os dados escolhidos
df = pd.read_csv(path2020, sep=';', encoding='latin-1')


#filtros dos cursos, por:
nomesDosCursos = 'NO_CURSO'
rotulosDosCursos = 'NO_CINE_ROTULO'


#gerando os dataframes filtrados e contando as ocorrências
def contarOcorrencias (filtro, variavel, criterio):
    dfPorAreaGeralEFiltro = df.get([filtro,variavel])
    dfPorCriterioEFiltro = dfPorAreaGeralEFiltro.loc[dfPorAreaGeralEFiltro[filtro].isin(criterio)]
    quantidadeDeOcorrencias = dfPorCriterioEFiltro[variavel].sum()
    return quantidadeDeOcorrencias


quantidadeDeIngressos = contarOcorrencias(nomesDosCursos, 'QT_ING', critério)
quantidadeDeConcluintes = contarOcorrencias(nomesDosCursos, 'QT_CONC', critério)
quantidadeDeMatriculas = contarOcorrencias(nomesDosCursos, 'QT_MAT', critério)


print("A quantidade de ingressos em cursos de engenharia foi", quantidadeDeIngressos)
print("A quantidade de matrículas em cursos de engenharia foi", quantidadeDeMatriculas)
print("A quantidade de concluintes em cursos de engenharia foi", quantidadeDeConcluintes)