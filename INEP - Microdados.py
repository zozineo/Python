import pandas as pd

#caminhos para os arquivos
pathTeste = r"C:\Users\e-enzo.ramos\Desktop\Códigos\Python\Testes\Teste.xlsx"
path2021 = r"C:\Users\e-enzo.ramos\Desktop\Dados\ME\INEP\Censo do Ensino Superior - Microdados\Microdados do Censo da Educação Superior 2021\dados\MICRODADOS_CADASTRO_CURSOS_2021.csv"
path2020 = r"C:\Users\e-enzo.ramos\Desktop\Dados\ME\INEP\Censo do Ensino Superior - Microdados\Microdados do Censo da Educação Superior 2020\dados\MICRODADOS_CADASTRO_CURSOS_2020.csv"
path2019 = r"C:\Users\e-enzo.ramos\Desktop\Dados\ME\INEP\Censo do Ensino Superior - Microdados\Microdados do Censo da Educação Superior 2019\dados\MICRODADOS_CADASTRO_CURSOS_2019.csv"
path2010 = r"C:\Users\e-enzo.ramos\Desktop\Dados\ME\INEP\Censo do Ensino Superior - Microdados\Microdados do Censo da Educação Superior 2010\dados\MICRODADOS_CADASTRO_CURSOS_2010.csv"
path2015 = r"C:\Users\e-enzo.ramos\Desktop\Dados\ME\INEP\Censo do Ensino Superior - Microdados\Microdados do Censo da Educação Superior 2015\dados\MICRODADOS_CADASTRO_CURSOS_2015.csv"
pathAreasGeraisSTEAM = r'C:\Users\e-enzo.ramos\Documents\Critérios de Microdados\Áreas Gerais de STEAM.txt'
pathCursosDeEngenharia2021 = r'C:\Users\e-enzo.ramos\Documents\Critérios de Microdados\Cursos de Engenharia 2021.txt'
pathCursosDeEngenharia2020 = r'C:\Users\e-enzo.ramos\Documents\Critérios de Microdados\Cursos de Engenharia 2020.txt'
pathRotulosDeEngenharia = r'C:\Users\e-enzo.ramos\Documents\Critérios de Microdados\Rótulos de Engenharia.txt'
pathExcecaoSTEAM = r'C:\Users\e-enzo.ramos\Documents\Critérios de Microdados\Exceções de STEAM.txt'
pathRotulosSustentabilidade = r'C:\Users\e-enzo.ramos\Documents\Critérios de Microdados\Rótulos Sustentabilidade.txt'
pathCursosDeSustentabilidade = r'C:\Users\e-enzo.ramos\Documents\Critérios de Microdados\Cursos de Sustentabilidade.txt'

#função para criar e tratar a lista com os critérios
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
    
def tratarPath (ano, categoria):
    pathAno = r"C:\Users\e-enzo.ramos\Desktop\Dados\ME\INEP\Censo do Ensino Superior - Microdados\Microdados do Censo da Educação Superior %s\dados\MICRODADOS_CADASTRO_%s_%s.csv" %(ano, categoria, ano)
    df = pd.read_csv(pathAno, sep=';', encoding='latin-1', low_memory=False)
    return df

#criando os dataframes com os dados escolhidos
dfBaseCursos = pd.read_csv(path2021, sep=';', encoding='latin-1')
dfBaseIES = pd.read_csv(path2021, sep=';', encoding='latin-1')


#colPrincipals dos cursos:
nomesDosCursos = 'NO_CURSO'
rotulosDosCursos = 'NO_CINE_ROTULO'
areaGeral = 'NO_CINE_AREA_GERAL'
modalidadeDoCurso = 'TP_MODALIDADE_ENSINO'
areaEspecifica = 'NO_CINE_AREA_ESPECIFICA'


#definindo as funções que vão ser usadas ao longo do programa
def contarOcorrencias (colPrincipal, variavel, criterio=[], excecao=[], df=dfBaseCursos):
    
    ''' Soma as ocorrências em um DataFrame contando somente uma coluna principal e uma coluna de variável filtrada por
    critérios. Todas as linhas que tiverem precisamente algum item da lista passada em criterio=[] será incluida no DataFrame
    filtrado, e os valores na coluna passada em variavel serão somados.

    - filtra um DataFrame pela coluna principal e a variável passada
    - filtra esse DataFrame pela presença do critério
    - soma os valores da coluna passada como variável

    retorna somente o valor resultando do último passo como quantidadeDeOcorrencias
    '''

    dfPorVariavelEColPrincipal = df.get([colPrincipal,variavel])

    if len(criterio)>=1 and len(excecao)<1:
        dfPorCriterioEcolPrincipal = dfPorVariavelEColPrincipal.loc[dfPorVariavelEColPrincipal[colPrincipal].isin(criterio)]
    if len(criterio)<1 and len(excecao)>=1:
        dfPorCriterioEcolPrincipal = dfPorVariavelEColPrincipal[~dfPorVariavelEColPrincipal[colPrincipal].isin(excecao)]
    
    quantidadeDeOcorrencias = dfPorCriterioEcolPrincipal[variavel].sum()
    return quantidadeDeOcorrencias


def contarOcorrenciasComplexas (colPrincipal, variavel, criterio, variavelExcecoes, excecoes, df=dfBaseCursos):

    '''Soma as ocorrências em um DataFrame contando uma coluna principal e uma coluna de variável filtrada por
    critérios e uma outra coluna filtrada por exceções. Todas as linhas que tiverem precisamente algum item da lista passada 
    em criterio=[] será incluida num DataFrame filtrado, e todas as linhas em variavelExcecoes que tiverem algum item da lista 
    passada em excecoes=[] serão excluídas. Os valores que restarem na coluna dada em variavel serão contabilizados.
    O nome da função inclui a palavra "complexas" por tratar duas colunas diferentes com critérios/exceções diferentes.

    - filtra um DataFrame em três colunas: a principal, a da variável a ser contabilizada e a que recebrá as exceções
    - filtra esse DataFrame em relação às linhas que possuem algum valor que foi passado na lista criterio=[]
    - filtra ainda mais esse DataFrame em relação às linhas da coluna variavelExcecoes que NÃO possuem o valor dado
    na lista excecoes=[]
    - soma os valores restantes na coluna [variavel]

    retorna somente o valor resultante do último passo como quantidadeDeOcorrencias
    '''

    dfPorVariavelEColPrincipal = df.get([colPrincipal,variavel,variavelExcecoes])
    dfPorCriterioEcolPrincipal = dfPorVariavelEColPrincipal[dfPorVariavelEColPrincipal[colPrincipal].isin(criterio)]
    dfPorCriteriocolPrincipalEExcessão = dfPorCriterioEcolPrincipal[~dfPorCriterioEcolPrincipal[variavelExcecoes].isin(excecoes)]
    quantidadeDeOcorrencias = dfPorCriteriocolPrincipalEExcessão[variavel].sum()
    return quantidadeDeOcorrencias


def compilarOcorrencias (colPrincipal, variavel=[], criterio=[], excecao=[], df=dfBaseCursos):

    '''Função para somar as ocorrências de determinadas variáveis, dadas em forma de lista, com base em uma coluna 
    principal filtrada em critérios ou exceções. Serve para somarmos os números que aparecem nas variáveis condicionados
    à presença de critérios ou ausências das exceções em uma coluna principal. Significa que quando há determinado valor
    na coluna principal, aquelas são as somas das variáveis indicadas. Difere de contarOcorrencias por somar os valores de 
    várias colunas ao mesmo tempo.

    - filtra o DataFrame em colunas específicas (a colPrincipal e as variáveis)
    - aplica o .isin() para encontrar somente as linhas com os critérios ou sem as exceções
    - soma os números das colunas presentes na lista variavel=[] dada como parâmetro
    
    exemplo de saída:

    ocorrências com [1] em TP_MODALIDADE_ENSINO QT_MAT

    QT_MAT                 3716370
    QT_ING                 2477374
    QT_CONC                 485141
    QT_CONC_FEM             304930
    QT_CONC_MASC            180211
    QT_SIT_DESVINCULADO    1284294'''

    variavel.append(colPrincipal)
    dfPorVariavelEColPrincipal = df[variavel]

    if len(criterio)>=1 and len(excecao)<1:
        dfPorCriterioEcolPrincipal = dfPorVariavelEColPrincipal[dfPorVariavelEColPrincipal[colPrincipal].isin(criterio)]
    if len(criterio)<1 and len(excecao)>=1:
        dfPorCriterioEcolPrincipal = dfPorVariavelEColPrincipal[~dfPorVariavelEColPrincipal[colPrincipal].isin(excecao)]
    
    variavel.remove(colPrincipal)
    dfCompilada = dfPorCriterioEcolPrincipal[variavel].sum(axis='rows', skipna=True)

    if len(criterio)>=1 and len(excecao)<1:
        print("ocorrências com %s em %s" %(criterio, colPrincipal), dfCompilada)
    if len(criterio)<1 and len(excecao)>=1:
        print("ocorrências sem %s em %s" %(excecao, colPrincipal), dfCompilada)

    return dfPorCriterioEcolPrincipal


def contarOcorrenciasPorPeriodoTemporal (anoInicial, anoFinal, colPrincipal, variavel, criterios):

    '''Função para contar as ocorrências de uma determinada variável, filtrada por critérios,
    com base em um período temporal dado como parâmetro.

    - inicializa um contador, que será retornado ao final da função após ser adicionado para cada ano do período temporal
    - cria um pathAno para cada dado ano usando formatação de strings
    - incializa um pd.read_csv para cada pathAno criado
    - utiliza a função contarOcorrencias normalmente para encontrar o valor daquele ano específico e soma esse valor cumulativamente
    à variável quantidadeFinal
    -- adiciona um aviso de que algo deu errado em determinado ano caso um erro seja levantado

    retorna a quantidade final da somatória realizada para a variavel passada
    '''

    quantidadeFinal = 0

    for ano in range (anoInicial, anoFinal+1):
        pathAno = r"C:\Users\e-enzo.ramos\Desktop\Dados\ME\INEP\Censo do Ensino Superior - Microdados\Microdados do Censo da Educação Superior %s\dados\MICRODADOS_CADASTRO_CURSOS_%s.csv" %(ano, ano)
        df = pd.read_csv(pathAno, sep=';', encoding='latin-1', low_memory=False)
        
        try:
            qntIngTeste = contarOcorrencias(colPrincipal, variavel, criterios, df)
            quantidadeFinal += qntIngTeste
        except:
            print('algo deu errado no ano %s' %(ano))

    print("-----> a %s de %s é %s <------" %(variavel, criterios, quantidadeFinal))
    return quantidadeFinal


def rankear (colPrincipal, variavel=[], criterio=[], excecao=[], colunaDosCriterios='', colunaDasExcecoes='', colunaDeRankeamento='', crescente=True, df=dfBaseCursos, tamanho=10):
    
    '''Função para rankear valores somados em função de uma coluna principal.

    - filtra um DataFrame pela colPrincipal e pelo conjunto de variáveis passado em variavel=[]
    -- caso sejam passados critérios, escolhe as linhas nas quais aparece algum valor da lista passada em criterio=[]
    -- caso sejam passadas exceções, escolhe as linhas nas quais não aparece nenhum valor da lista passada em excecao=[]
    - agrupa pelos valores presentes na colPrincipal e soma as linhas do DataFrame agrupado
    -- o dfGrupada representa o DataFrame filtrado pelos critérios ou exceções reorganizados agrupando as ocorrências que estão
    na colPrincipal
    - rankeia a coluna passada em colunaDeRankeamento, baseando-se nos valores somados
    - limita o tamanho da resposta (tanto print quanto return) ao tamanho passado
    '''
    
    variavel.append(colPrincipal)
    dfPorVariavelEColPrincipal = df.get(variavel)

    if len(criterio) >= 1 and len(excecao) < 1:
        dfPorCriterioEcolPrincipal = dfPorVariavelEColPrincipal[dfPorVariavelEColPrincipal[colunaDosCriterios].isin(criterio)]
        dfGrupada = dfPorCriterioEcolPrincipal.groupby(colPrincipal, dropna=False).sum()
    elif len(excecao) >= 1 and len(criterio) < 1:
        dfPorCriterioEcolPrincipal = dfPorVariavelEColPrincipal[~dfPorVariavelEColPrincipal[colunaDasExcecoes].isin(excecao)]
        dfGrupada = dfPorCriterioEcolPrincipal.groupby(colPrincipal, dropna=False).sum()
    else:
        dfGrupada = dfPorVariavelEColPrincipal.groupby(colPrincipal, dropna=False).sum()

    dfSorted = dfGrupada.sort_values(axis=0, by=colunaDeRankeamento, ascending= not(crescente))
    
    print(dfSorted.head(tamanho))
    return dfSorted.head(tamanho)
    

#tratando os critérios e exceções
criterioEngenharias = tratarCriterios(pathRotulosDeEngenharia)
critérioSTEAM = tratarCriterios(pathAreasGeraisSTEAM)
excecoesSTEAM = tratarCriterios(pathExcecaoSTEAM)
rotulosSustentabilidade = tratarCriterios(pathRotulosSustentabilidade)
cursosSustentabilidade = tratarCriterios(pathCursosDeSustentabilidade)




########################################### RETIRANDO E ARMAZENANDO OS DADOS ###########################################




#ENGENHARIAS

#matriculas, ingressos e concluintes totais e divididos por sexo dos cursos de engenharia
listaDeVariaveis=['QT_ING', 'QT_CONC', 'QT_MAT', 'QT_ING_FEM', 'QT_ING_MASC', 'QT_CONC_FEM', 'QT_CONC_MASC',
'QT_MAT_FEM', 'QT_MAT_MASC']

for variavel in listaDeVariaveis:
    res = contarOcorrencias(rotulosDosCursos, variavel, criterioEngenharias)
    print('A %s de Engenharias é %s' %(variavel, res))



#STEAM

#matriculas, ingressos e concluintes dos cursos STEAM
'''qMS1 = contarOcorrenciasComplexas(areaGeral, 'QT_MAT', critérioSTEAM, rotulosDosCursos, excecoesSTEAM)
qMS2 = contarOcorrencias(rotulosDosCursos, 'QT_MAT', ['Farmácia', 'Biomedicina'])
quantidadeDeMatriculasSTEAM =  qMS1 + qMS2

qIS1 = contarOcorrenciasComplexas(areaGeral, 'QT_ING', critérioSTEAM, rotulosDosCursos, excecoesSTEAM)
qIS2 = contarOcorrencias(rotulosDosCursos, 'QT_ING', ['Farmácia', 'Biomedicina'])
quantidadeDeIngressosSTEAM =  qIS1 + qIS2

qCS1 = contarOcorrenciasComplexas(areaGeral, 'QT_CONC', critérioSTEAM, rotulosDosCursos, excecoesSTEAM)
qCS2 = contarOcorrencias(rotulosDosCursos, 'QT_CONC', ['Farmácia', 'Biomedicina'])
quantidadeDeConcluintesSTEAM =  qCS1 + qCS2
print('ingressos: %s   matrículas: %s    concluintes: %s' %(quantidadeDeIngressosSTEAM, quantidadeDeMatriculasSTEAM, quantidadeDeConcluintesSTEAM))
'''

#cursos em stem que mais receberam ingressos
'''
listaDeCursosSTEAM= ['Biomedicina', 'Farmácia', 'Biologia', 'Química', 
'Programas interdisciplinares abrangendo ciências naturais, matemática e estatística', 
'Gestão da tecnologia da informação', 'Ciência da computação', 'Redes de computadores', 'Automação industrial', 
'Engenharia de alimentos', 'Engenharia química', 'Engenharia ambiental e sanitária', 'Engenharia ambiental',
'Engenharia de produção', 'Engenharia civil', 'Engenharia elétrica', 'Engenharia de computação (DCN Engenharia)', 
'Engenharia de computação (DCN Computação)', 'Engenharia de controle e automação', 
'Engenharia mecânica', 'Engenharia eletrônica']

df2020 = tratarPath(2020, 'CURSOS')
for curso in listaDeCursosSTEAM:
    qting2021 = contarOcorrencias(rotulosDosCursos, 'QT_ING', criterio=[curso])
    qting2020 = contarOcorrencias(rotulosDosCursos, 'QT_ING', criterio=[curso], df=df2020)
    aumentoqting = qting2020 - qting2021
    print ('o aumento na quantidade de ingressos em %s é %s' %(curso, aumentoqting))
'''


#matriculas, ingressos e concluintes dos cursos STEAM por sexo
'''qMFS1 = contarOcorrenciasComplexas(areaGeral,'QT_MAT_FEM', critérioSTEAM, rotulosDosCursos, excecoesSTEAM)
qMFS2 = contarOcorrencias(rotulosDosCursos, 'QT_MAT_FEM', ['Farmácia', 'Biomedicina'])
quantidadeDeMatriculasFemininasSTEAM = qMFS1 + qMFS2
qMMS1 = contarOcorrenciasComplexas(areaGeral,'QT_MAT_MASC', critérioSTEAM, rotulosDosCursos, excecoesSTEAM)
qMMS2 = contarOcorrencias(rotulosDosCursos, 'QT_MAT_MASC', ['Farmácia', 'Biomedicina'])
quantidadeDeMatriculasMasculinasSTEAM = qMMS1 + qMMS2

qIFS1 = contarOcorrenciasComplexas(areaGeral, 'QT_ING_FEM', critérioSTEAM, rotulosDosCursos, excecoesSTEAM)
qIFS2 = contarOcorrencias(rotulosDosCursos, 'QT_ING_FEM', ['Farmácia', 'Biomedicina'])
quantidadeDeIngressosFemininosSTEAM =  qIFS1 + qIFS2
qIMS1 = contarOcorrenciasComplexas(areaGeral, 'QT_ING_MASC', critérioSTEAM, rotulosDosCursos, excecoesSTEAM)
qIMS2 = contarOcorrencias(rotulosDosCursos, 'QT_ING_MASC', ['Farmácia', 'Biomedicina'])
quantidadeDeIngressosMasculinosSTEAM =  qIMS1 + qIMS2

qCFS1 = contarOcorrenciasComplexas(areaGeral, 'QT_CONC_FEM', critérioSTEAM, rotulosDosCursos, excecoesSTEAM)
qCFS2 = contarOcorrencias(rotulosDosCursos, 'QT_CONC_FEM', ['Farmácia', 'Biomedicina'])
quantidadeDeConcluintesFemininosSTEAM =  qCFS1 + qCFS2
qCMS1 = contarOcorrenciasComplexas(areaGeral, 'QT_CONC_MASC', critérioSTEAM, rotulosDosCursos, excecoesSTEAM)
qCMS2 = contarOcorrencias(rotulosDosCursos, 'QT_CONC_MASC', ['Farmácia', 'Biomedicina'])
quantidadeDeConcluintesMasculinosSTEAM =  qCMS1 + qCMS2
'''


#GERAL

#matriculas, ingressos e concluintes gerais (de todos os cursos) por sexo
'''quantidadeTotalDeMatriculasFemininas = dfBaseCursos['QT_MAT_FEM'].sum()
quantidadeTotalDeMatriculasMasculinas = dfBaseCursos['QT_MAT_MASC'].sum()
quantidadeTotalDeIngressosFemininos = dfBaseCursos['QT_ING_FEM'].sum()
quantidadeTotalDeIngressosMasculinos = dfBaseCursos['QT_ING_MASC'].sum()
quantidadeTotalDeConcluintesFemininos = dfBaseCursos['QT_CONC_FEM'].sum()
quantidadeTotalDeConcluintesMasculinos = dfBaseCursos['QT_CONC_MASC'].sum()
quantidadeTotalDeConcluintes = dfBaseCursos['QT_CONC'].sum()'''


#MODALIDADE DOS CURSOS (EAD OU PRESENCIAL)

'''ompilarOcorrencias(modalidadeDoCurso, ['QT_MAT', 'QT_ING', 'QT_CONC', 'QT_CONC_FEM', 'QT_CONC_MASC', 'QT_SIT_DESVINCULADO'], excecao=[1])
dadosGeraisPresenciais = compilarOcorrencias(modalidadeDoCurso, ['QT_MAT', 'QT_ING', 'QT_CONC', 'QT_CONC_FEM', 'QT_CONC_MASC', 'QT_SIT_DESVINCULADO'], [1])
'''

#ESPAÇOS TEMPORAIS (2010-202?)

#contando as ocorrências dos cursos específicos em 2021
'''tabelaDosCriterios = compilarOcorrencias(rotulosDosCursos, ['QT_ING', 'QT_ING_FEM', 'QT_ING_MASC', 'QT_CONC', 'QT_CONC_FEM',	'QT_CONC_MASC'], criterioEngenharias)
for curso in criterioEngenharias:
    critCurso = []
    critCurso.append(curso)
    qntCurso = contarOcorrencias(rotulosDosCursos, 'QT_ING', critCurso)
    print("%s tem %s ingressos" %(curso, qntCurso))'''


#pegando espaços temporais específicos

#Engenharias
listaDeVariaveis = ['QT_ING', 'QT_ING_FEM', 'QT_ING_MASC', 'QT_CONC', 'QT_CONC_FEM', 'QT_CONC_MASC']
'''listaDeCursos = ['Engenharia de produção', 'Engenharia de petróleo', 'Engenharia de minas', 'Engenharia civil',
'Engenharia metalúrgica', 'Engenharia de telecomunicações', 'Engenharia elétrica', 'Engenharia de controle e automação',
'Engenharia mecânica', 'Engenharia eletrônica', 'Engenharia mecatrônica']
for variavel in listaDeVariaveis:
    for curso in listaDeCursos:
        contarOcorrenciasPorPeriodoTemporal(2010, 2021, rotulosDosCursos, variavel, [curso])'''

##Engenharia Ambiental e Sanitária
'''for variavel in listaDeVariaveis:
    qnt1 = contarOcorrenciasPorPeriodoTemporal(2010, 2021, rotulosDosCursos, variavel, ['Engenharia ambiental'])
    qnt2 = contarOcorrenciasPorPeriodoTemporal(2010, 2021, rotulosDosCursos, variavel, ['Engenharia ambiental e sanitária'])
    print('A %s de engenharia ambiental e sanitária é %s' %(variavel, (qnt1+qnt2)))'''

##Engenharia de computação
'''for variavel in listaDeVariaveis:
    qnt1 = contarOcorrenciasPorPeriodoTemporal(2010, 2021, rotulosDosCursos, variavel, ['Engenharia de computação (DCN Engenharia)'])
    qnt2 = contarOcorrenciasPorPeriodoTemporal(2010, 2021, rotulosDosCursos, variavel, ['Engenharia de computação (DCN Computação)'])
    print('A %s de engenharia de computação é %s' %(variavel, (qnt1+qnt2)))'''

##Engenharias de Agrimensura e Cartográficas
'''for variavel in listaDeVariaveis:
    qnt1 = contarOcorrenciasPorPeriodoTemporal(2010, 2021, rotulosDosCursos, variavel, ['Engenharia de agrimensura'])
    qnt2 = contarOcorrenciasPorPeriodoTemporal(2010, 2021, rotulosDosCursos, variavel, ['Engenharia cartográfica'])
    qnt3 = contarOcorrenciasPorPeriodoTemporal(2010, 2021, rotulosDosCursos, variavel, ['Engenharia de agrimensura e cartográfica'])
    print('A %s de engenharia de agrimensura e cartográfica é %s' %(variavel, (qnt1+qnt2+qnt3)))'''

#Geral
'''listaDeCursosGeral = ['Pedagogia', 'Serviço social', 'Enfermagem', 'Psicologia', 'Gestão de pessoas', 'Fisioterapia',
'Farmácia', 'Arquitetura e urbanismo', 'Contabilidade', 'Administração', 'Publicidade e propaganda', 'Direito', 'Medicina',
'Gestão de negócios', 'Educação física formação de professor', 'Educação física', 'Engenharia de produção', 'Engenharia civil',
'Logística', 'Sistemas de informação']
for variavel in listaDeVariaveis:
    for curso in listaDeCursosGeral:
        contarOcorrenciasPorPeriodoTemporal(2010, 2021, rotulosDosCursos, variavel, [curso])'''

#STEAM

'''listaQuantidadeFinal =[]
listaDeCursosSTEAM = ['Biomedicina', 'Farmácia', 'Biologia', 'Química', 
'Programas interdisciplinares abrangendo ciências naturais, matemática e estatística', 'Gestão da tecnologia da informação', 
'Ciência da computação', 'Redes de computadores', 'Automação industrial']
for variavel in listaDeVariaveis:
    for curso in listaDeCursosSTEAM:
        qf = contarOcorrenciasPorPeriodoTemporal(2010, 2021, rotulosDosCursos, variavel, [curso])
        quantFinal = "-----> a %s de %s é %s <------" %(variavel, curso, qf)
        listaQuantidadeFinal.append(quantFinal)'''


#RANKEANDO CURSOS

#for ano in [2010, 2015, 2020, 2021]:
#    pathAno = r"C:\Users\e-enzo.ramos\Desktop\Dados\ME\INEP\Censo do Ensino Superior - Microdados\Microdados do Censo da Educação Superior %s\dados\MICRODADOS_CADASTRO_CURSOS_%s.csv" %(ano, ano)
#    dfAno = pd.read_csv(pathAno, sep=';', encoding='latin-1')
#    print('------------------> TABELAS DO ANO %s <------------------' %(ano))
#    rankear(rotulosDosCursos, 'QT_ING_FEM', df=dfAno)
#    rankear(rotulosDosCursos, 'QT_CONC_FEM', df=dfAno)


#BUSCANDO DADOS SOBRE SUSTENTABILIDADE

'''print("POR AREA DETALHADA") #--> 2º
rankear('SG_UF', ['NO_CINE_AREA_DETALHADA', 'QT_ING'], criterio=["Ciências ambientais", "Tecnologia de proteção ambiental"], colunaDosCriterios='NO_CINE_AREA_DETALHADA', colunaDeRankeamento='QT_ING')

print("POR AREA ESPECIFICA") #--> 4º
rankear('SG_UF', [areaEspecifica, 'QT_ING'], criterio=["Meio ambiente"], colunaDosCriterios=areaEspecifica, colunaDeRankeamento='QT_ING')
'''

'''
print("POR NOME DO CURSO") #--> 1º
rankear('SG_UF', [nomesDosCursos, 'QT_ING'], criterio=cursosSustentabilidade, colunaDosCriterios=nomesDosCursos, colunaDeRankeamento='QT_ING')
'''

'''
print("POR ROTULO DO CURSO") #--> 3º
rankear('SG_UF', [rotulosDosCursos, 'QT_ING'], criterio= rotulosSustentabilidade, colunaDosCriterios=rotulosDosCursos, colunaDeRankeamento='QT_ING')
'''

