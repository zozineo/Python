import pandas as pd

#para atualizar os dados deve-se mudar: pathANO, pathLISTADECRITERIOS e o filtro dos cursos
pathTeste = r"C:\Users\e-enzo.ramos\Desktop\Códigos\Python\Testes\Teste.xlsx"
path2021 = r"C:\Users\e-enzo.ramos\Desktop\Dados\ME\INEP\Censo do Ensino Superior - Microdados\Microdados do Censo da Educação Superior 2021\dados\MICRODADOS_CADASTRO_CURSOS_2021.csv"
path2020 = r"C:\Users\e-enzo.ramos\Desktop\Dados\ME\INEP\Censo do Ensino Superior - Microdados\Microdados do Censo da Educação Superior 2020\dados\MICRODADOS_CADASTRO_CURSOS_2020.csv"
path2019 = r"C:\Users\e-enzo.ramos\Desktop\Dados\ME\INEP\Censo do Ensino Superior - Microdados\Microdados do Censo da Educação Superior 2019\dados\MICRODADOS_CADASTRO_CURSOS_2019.csv"
pathAreasGeraisSTEAM = r'C:\Users\e-enzo.ramos\Documents\Critérios de Microdados\Áreas Gerais de STEAM.txt'
pathCursosDeEngenharia2021 = r'C:\Users\e-enzo.ramos\Documents\Critérios de Microdados\Cursos de Engenharia 2021.txt'
pathCursosDeEngenharia2020 = r'C:\Users\e-enzo.ramos\Documents\Critérios de Microdados\Cursos de Engenharia 2020.txt'
pathRotulosDeEngenharia = r'C:\Users\e-enzo.ramos\Documents\Critérios de Microdados\Rótulos de Engenharia.txt'
pathExcessaoSTEAM = r'C:\Users\e-enzo.ramos\Documents\Critérios de Microdados\Excessões de STEAM.txt'


#criando e tratando a lista com os critérios
def tratarCriterios(pathListaCriterios, caixa_alta=False):
    with open(pathListaCriterios, 'r', encoding='utf-8') as documento:
        critério = documento.read().splitlines()
        critério.sort()
    
    listaArrumada = []
    if (caixa_alta):
        [listaArrumada.append(curso.upper()) for curso in critério if curso not in listaArrumada]
    else:
        [listaArrumada.append(curso) for curso in critério if curso not in listaArrumada]

    #print(listaArrumada)
    return listaArrumada
    

#criando os dataframes com os dados escolhidos
df = pd.read_csv(path2020, sep=';', encoding='latin-1')


#filtros dos cursos:
nomesDosCursos = 'NO_CURSO'
rotulosDosCursos = 'NO_CINE_ROTULO'
areaGeral = 'NO_CINE_AREA_GERAL'
modalidadeDoCurso = 'TP_MODALIDADE_ENSINO'


#gerando os dataframes filtrados e contando as ocorrências
def contarOcorrencias (filtro, variavel, criterio):
    dfPorAreaGeralEFiltro = df.get([filtro,variavel])
    dfPorCriterioEFiltro = dfPorAreaGeralEFiltro.loc[dfPorAreaGeralEFiltro[filtro].isin(criterio)]
    quantidadeDeOcorrencias = dfPorCriterioEFiltro[variavel].sum()
    return quantidadeDeOcorrencias


def contarOcorrenciasComExcessoes (filtro, variavel, criterio, variavelExcessoes, excessoes):
    dfPorAreaGeralEFiltro = df.get([filtro,variavel,variavelExcessoes])
    dfPorCriterioEFiltro = dfPorAreaGeralEFiltro[dfPorAreaGeralEFiltro[filtro].isin(criterio)]
    dfPorCriterioFiltroEExcessão = dfPorCriterioEFiltro[~dfPorCriterioEFiltro[variavelExcessoes].isin(excessoes)]
    quantidadeDeOcorrencias = dfPorCriterioFiltroEExcessão[variavel].sum()
    return quantidadeDeOcorrencias


def compilarOcorrencias (filtro, variavel=[], criterio=[], excessao=[]):
    variavel.append(filtro)
    dfPorAreaGeralEFiltro = df[variavel]
    if len(criterio)>=1 and len(excessao)<1:
        dfPorCriterioEFiltro = dfPorAreaGeralEFiltro[dfPorAreaGeralEFiltro[filtro].isin(criterio)]
    if len(criterio)<1 and len(excessao)>=1:
        dfPorCriterioEFiltro = dfPorAreaGeralEFiltro[~dfPorAreaGeralEFiltro[filtro].isin(excessao)]
    variavel.remove(filtro)
    dfCompilada = dfPorCriterioEFiltro[variavel].sum(axis='rows', skipna=True)
    print(dfCompilada)


#tratando os critérios
criterioEngenharias = tratarCriterios(pathRotulosDeEngenharia)
critérioSTEAM = tratarCriterios(pathAreasGeraisSTEAM)
excessoesSTEAM = tratarCriterios(pathExcessaoSTEAM)


#retirando e armazenando os dados


#ENGENHARIAS

#matriculas, ingressos e concluintes dos cursos de engenharia
quantidadeDeIngressosEngenharias = contarOcorrencias(rotulosDosCursos, 'QT_ING', criterioEngenharias)
quantidadeDeConcluintesEngenharias = contarOcorrencias(rotulosDosCursos, 'QT_CONC', criterioEngenharias)
quantidadeDeMatriculasEngenharias = contarOcorrencias(rotulosDosCursos, 'QT_MAT', criterioEngenharias)

#matriculas, ingressos e concluintes dos cursos de engenharia por sexo
quantidadeDeIngressosFemininosEngenharias = contarOcorrencias(rotulosDosCursos, 'QT_ING_FEM', criterioEngenharias)
quantidadeDeConcluintesFemininosEngenharias = contarOcorrencias(rotulosDosCursos, 'QT_CONC_FEM', criterioEngenharias)
quantidadeDeMatriculasFemininasEngenharias = contarOcorrencias(rotulosDosCursos, 'QT_MAT_FEM', criterioEngenharias)

quantidadeDeIngressosMasculinosEngenharias = contarOcorrencias(rotulosDosCursos, 'QT_ING_MASC', criterioEngenharias)
quantidadeDeConcluintesMasculinosEngenharias = contarOcorrencias(rotulosDosCursos, 'QT_CONC_MASC', criterioEngenharias)
quantidadeDeMatriculasMasculinasEngenharias = contarOcorrencias(rotulosDosCursos, 'QT_MAT_MASC', criterioEngenharias)


#STEAM

#matriculas, ingressos e concluintes dos cursos STEAM
qMS1 = contarOcorrenciasComExcessoes(areaGeral, 'QT_MAT', critérioSTEAM, rotulosDosCursos, excessoesSTEAM)
qMS2 = contarOcorrencias(rotulosDosCursos, 'QT_MAT', ['Farmácia', 'Biomedicina'])
quantidadeDeMatriculasSTEAM =  qMS1 + qMS2

qIS1 = contarOcorrenciasComExcessoes(areaGeral, 'QT_ING', critérioSTEAM, rotulosDosCursos, excessoesSTEAM)
qIS2 = contarOcorrencias(rotulosDosCursos, 'QT_ING', ['Farmácia', 'Biomedicina'])
quantidadeDeIngressosSTEAM =  qIS1 + qIS2

qCS1 = contarOcorrenciasComExcessoes(areaGeral, 'QT_CONC', critérioSTEAM, rotulosDosCursos, excessoesSTEAM)
qCS2 = contarOcorrencias(rotulosDosCursos, 'QT_CONC', ['Farmácia', 'Biomedicina'])
quantidadeDeConcluintesSTEAM =  qCS1 + qCS2

#matriculas, ingressos e concluintes dos cursos STEAM por sexo
qMFS1 = contarOcorrenciasComExcessoes(areaGeral,'QT_MAT_FEM', critérioSTEAM, rotulosDosCursos, excessoesSTEAM)
qMFS2 = contarOcorrencias(rotulosDosCursos, 'QT_MAT_FEM', ['Farmácia', 'Biomedicina'])
quantidadeDeMatriculasFemininasSTEAM = qMFS1 + qMFS2
qMMS1 = contarOcorrenciasComExcessoes(areaGeral,'QT_MAT_MASC', critérioSTEAM, rotulosDosCursos, excessoesSTEAM)
qMMS2 = contarOcorrencias(rotulosDosCursos, 'QT_MAT_MASC', ['Farmácia', 'Biomedicina'])
quantidadeDeMatriculasMasculinasSTEAM = qMMS1 + qMMS2

qIFS1 = contarOcorrenciasComExcessoes(areaGeral, 'QT_ING_FEM', critérioSTEAM, rotulosDosCursos, excessoesSTEAM)
qIFS2 = contarOcorrencias(rotulosDosCursos, 'QT_ING_FEM', ['Farmácia', 'Biomedicina'])
quantidadeDeIngressosFemininosSTEAM =  qIFS1 + qIFS2
qIMS1 = contarOcorrenciasComExcessoes(areaGeral, 'QT_ING_MASC', critérioSTEAM, rotulosDosCursos, excessoesSTEAM)
qIMS2 = contarOcorrencias(rotulosDosCursos, 'QT_ING_MASC', ['Farmácia', 'Biomedicina'])
quantidadeDeIngressosMasculinosSTEAM =  qIMS1 + qIMS2

qCFS1 = contarOcorrenciasComExcessoes(areaGeral, 'QT_CONC_FEM', critérioSTEAM, rotulosDosCursos, excessoesSTEAM)
qCFS2 = contarOcorrencias(rotulosDosCursos, 'QT_CONC_FEM', ['Farmácia', 'Biomedicina'])
quantidadeDeConcluintesFemininosSTEAM =  qCFS1 + qCFS2
qCMS1 = contarOcorrenciasComExcessoes(areaGeral, 'QT_CONC_MASC', critérioSTEAM, rotulosDosCursos, excessoesSTEAM)
qCMS2 = contarOcorrencias(rotulosDosCursos, 'QT_CONC_MASC', ['Farmácia', 'Biomedicina'])
quantidadeDeConcluintesMasculinosSTEAM =  qCMS1 + qCMS2


#GERAL

#matriculas, ingressos e concluintes gerais (de todos os cursos) por sexo
quantidadeTotalDeMatriculasFemininas = df['QT_MAT_FEM'].sum()
quantidadeTotalDeMatriculasMasculinas = df['QT_MAT_MASC'].sum()
quantidadeTotalDeIngressosFemininos = df['QT_ING_FEM'].sum()
quantidadeTotalDeIngressosMasculinos = df['QT_ING_MASC'].sum()
quantidadeTotalDeConcluintesFemininos = df['QT_CONC_FEM'].sum()
quantidadeTotalDeConcluintesMasculinos = df['QT_CONC_MASC'].sum()
quantidadeTotalDeConcluintes = df['QT_CONC'].sum()


#MODALIDADE DOS CURSOS (EAD OU PRESENCIAL)
compilarOcorrencias(modalidadeDoCurso, ['QT_MAT', 'QT_ING', 'QT_CONC', 'QT_CONC_FEM', 'QT_CONC_MASC', 'QT_SIT_DESVINCULADO'], excessao=[1])
dadosGeraisPresenciais = compilarOcorrencias(modalidadeDoCurso, ['QT_MAT', 'QT_ING', 'QT_CONC', 'QT_CONC_FEM', 'QT_CONC_MASC', 'QT_SIT_DESVINCULADO'], [1])


#ESPAÇOS TEMPORAIS (2010-202?)
