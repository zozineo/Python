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
pathexcecaoSTEAM = r'C:\Users\e-enzo.ramos\Documents\Critérios de Microdados\Excessões de STEAM.txt'


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
dfBase = pd.read_csv(path2020, sep=';', encoding='latin-1')


#filtros dos cursos:
nomesDosCursos = 'NO_CURSO'
rotulosDosCursos = 'NO_CINE_ROTULO'
areaGeral = 'NO_CINE_AREA_GERAL'
modalidadeDoCurso = 'TP_MODALIDADE_ENSINO'


#definindo as funções que vão ser usadas ao longo do programa
def contarOcorrencias (filtro, variavel, criterio, df=dfBase):
    dfPorAreaGeralEFiltro = df.get([filtro,variavel])
    dfPorCriterioEFiltro = dfPorAreaGeralEFiltro.loc[dfPorAreaGeralEFiltro[filtro].isin(criterio)]
    quantidadeDeOcorrencias = dfPorCriterioEFiltro[variavel].sum()
    return quantidadeDeOcorrencias


def contarOcorrenciasComExcecoes (filtro, variavel, criterio, variavelexcecoes, excecoes, df=dfBase):
    dfPorAreaGeralEFiltro = df.get([filtro,variavel,variavelexcecoes])
    dfPorCriterioEFiltro = dfPorAreaGeralEFiltro[dfPorAreaGeralEFiltro[filtro].isin(criterio)]
    dfPorCriterioFiltroEExcessão = dfPorCriterioEFiltro[~dfPorCriterioEFiltro[variavelexcecoes].isin(excecoes)]
    quantidadeDeOcorrencias = dfPorCriterioFiltroEExcessão[variavel].sum()
    return quantidadeDeOcorrencias


def compilarOcorrencias (filtro, variavel=[], criterio=[], excecao=[], df=dfBase):
    variavel.append(filtro)
    dfPorAreaGeralEFiltro = df[variavel]
    if len(criterio)>=1 and len(excecao)<1:
        dfPorCriterioEFiltro = dfPorAreaGeralEFiltro[dfPorAreaGeralEFiltro[filtro].isin(criterio)]
    if len(criterio)<1 and len(excecao)>=1:
        dfPorCriterioEFiltro = dfPorAreaGeralEFiltro[~dfPorAreaGeralEFiltro[filtro].isin(excecao)]
    variavel.remove(filtro)
    dfCompilada = dfPorCriterioEFiltro[variavel].sum(axis='rows', skipna=True)
    print(dfCompilada)
    return dfPorCriterioEFiltro


def contarOcorrenciasPorPeriodoTemporal (anoInicial, anoFinal, filtro, variavel, criterios):
    quantidadeFinal = 0

    for ano in range (anoInicial, anoFinal+1):
        pathAno = r"C:\Users\e-enzo.ramos\Desktop\Dados\ME\INEP\Censo do Ensino Superior - Microdados\Microdados do Censo da Educação Superior %s\dados\MICRODADOS_CADASTRO_CURSOS_%s.csv" %(ano, ano)
        df = pd.read_csv(pathAno, sep=';', encoding='latin-1')
        
        try:
            qntIngTeste = contarOcorrencias(filtro, variavel, criterios, df)
            quantidadeFinal += qntIngTeste
        except:
            print('algo deu errado no ano %s' %(ano))

    print("a %s de %s é %s" %(variavel, criterios, quantidadeFinal))
    return quantidadeFinal


#tratando os critérios
criterioEngenharias = tratarCriterios(pathRotulosDeEngenharia)
critérioSTEAM = tratarCriterios(pathAreasGeraisSTEAM)
excecoesSTEAM = tratarCriterios(pathexcecaoSTEAM)


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
qMS1 = contarOcorrenciasComExcecoes(areaGeral, 'QT_MAT', critérioSTEAM, rotulosDosCursos, excecoesSTEAM)
qMS2 = contarOcorrencias(rotulosDosCursos, 'QT_MAT', ['Farmácia', 'Biomedicina'])
quantidadeDeMatriculasSTEAM =  qMS1 + qMS2

qIS1 = contarOcorrenciasComExcecoes(areaGeral, 'QT_ING', critérioSTEAM, rotulosDosCursos, excecoesSTEAM)
qIS2 = contarOcorrencias(rotulosDosCursos, 'QT_ING', ['Farmácia', 'Biomedicina'])
quantidadeDeIngressosSTEAM =  qIS1 + qIS2

qCS1 = contarOcorrenciasComExcecoes(areaGeral, 'QT_CONC', critérioSTEAM, rotulosDosCursos, excecoesSTEAM)
qCS2 = contarOcorrencias(rotulosDosCursos, 'QT_CONC', ['Farmácia', 'Biomedicina'])
quantidadeDeConcluintesSTEAM =  qCS1 + qCS2

#matriculas, ingressos e concluintes dos cursos STEAM por sexo
qMFS1 = contarOcorrenciasComExcecoes(areaGeral,'QT_MAT_FEM', critérioSTEAM, rotulosDosCursos, excecoesSTEAM)
qMFS2 = contarOcorrencias(rotulosDosCursos, 'QT_MAT_FEM', ['Farmácia', 'Biomedicina'])
quantidadeDeMatriculasFemininasSTEAM = qMFS1 + qMFS2
qMMS1 = contarOcorrenciasComExcecoes(areaGeral,'QT_MAT_MASC', critérioSTEAM, rotulosDosCursos, excecoesSTEAM)
qMMS2 = contarOcorrencias(rotulosDosCursos, 'QT_MAT_MASC', ['Farmácia', 'Biomedicina'])
quantidadeDeMatriculasMasculinasSTEAM = qMMS1 + qMMS2

qIFS1 = contarOcorrenciasComExcecoes(areaGeral, 'QT_ING_FEM', critérioSTEAM, rotulosDosCursos, excecoesSTEAM)
qIFS2 = contarOcorrencias(rotulosDosCursos, 'QT_ING_FEM', ['Farmácia', 'Biomedicina'])
quantidadeDeIngressosFemininosSTEAM =  qIFS1 + qIFS2
qIMS1 = contarOcorrenciasComExcecoes(areaGeral, 'QT_ING_MASC', critérioSTEAM, rotulosDosCursos, excecoesSTEAM)
qIMS2 = contarOcorrencias(rotulosDosCursos, 'QT_ING_MASC', ['Farmácia', 'Biomedicina'])
quantidadeDeIngressosMasculinosSTEAM =  qIMS1 + qIMS2

qCFS1 = contarOcorrenciasComExcecoes(areaGeral, 'QT_CONC_FEM', critérioSTEAM, rotulosDosCursos, excecoesSTEAM)
qCFS2 = contarOcorrencias(rotulosDosCursos, 'QT_CONC_FEM', ['Farmácia', 'Biomedicina'])
quantidadeDeConcluintesFemininosSTEAM =  qCFS1 + qCFS2
qCMS1 = contarOcorrenciasComExcecoes(areaGeral, 'QT_CONC_MASC', critérioSTEAM, rotulosDosCursos, excecoesSTEAM)
qCMS2 = contarOcorrencias(rotulosDosCursos, 'QT_CONC_MASC', ['Farmácia', 'Biomedicina'])
quantidadeDeConcluintesMasculinosSTEAM =  qCMS1 + qCMS2


#GERAL

#matriculas, ingressos e concluintes gerais (de todos os cursos) por sexo
quantidadeTotalDeMatriculasFemininas = dfBase['QT_MAT_FEM'].sum()
quantidadeTotalDeMatriculasMasculinas = dfBase['QT_MAT_MASC'].sum()
quantidadeTotalDeIngressosFemininos = dfBase['QT_ING_FEM'].sum()
quantidadeTotalDeIngressosMasculinos = dfBase['QT_ING_MASC'].sum()
quantidadeTotalDeConcluintesFemininos = dfBase['QT_CONC_FEM'].sum()
quantidadeTotalDeConcluintesMasculinos = dfBase['QT_CONC_MASC'].sum()
quantidadeTotalDeConcluintes = dfBase['QT_CONC'].sum()


#MODALIDADE DOS CURSOS (EAD OU PRESENCIAL)
compilarOcorrencias(modalidadeDoCurso, ['QT_MAT', 'QT_ING', 'QT_CONC', 'QT_CONC_FEM', 'QT_CONC_MASC', 'QT_SIT_DESVINCULADO'], excecao=[1])
dadosGeraisPresenciais = compilarOcorrencias(modalidadeDoCurso, ['QT_MAT', 'QT_ING', 'QT_CONC', 'QT_CONC_FEM', 'QT_CONC_MASC', 'QT_SIT_DESVINCULADO'], [1])


#ESPAÇOS TEMPORAIS (2010-202?)

#contando as ocorrências dos cursos específicos em 2021
tabelaFiltrada = compilarOcorrencias(rotulosDosCursos, ['QT_ING', 'QT_ING_FEM', 'QT_ING_MASC', 'QT_CONC', 'QT_CONC_FEM',	'QT_CONC_MASC'], criterioEngenharias)
for curso in criterioEngenharias:
    critCurso = []
    critCurso.append(curso)
    qntCurso = contarOcorrencias(rotulosDosCursos, 'QT_ING', critCurso)
    print("%s tem %s ingressos" %(curso, qntCurso))


#pegando espaços temporais específicos
listaDeVariaveis = ['QT_ING', 'QT_ING_FEM', 'QT_ING_MASC', 'QT_CONC', 'QT_CONC_FEM', 'QT_CONC_MASC']
for variavel in listaDeVariaveis:
    contarOcorrenciasPorPeriodoTemporal(2010, 2020, rotulosDosCursos, variavel, ['Biomedicina'])


