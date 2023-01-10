import pandas as pd
import xlsxwriter

pathTeste = r"C:\Users\e-enzo.ramos\Desktop\Códigos\Python\Testes\%s.xlsx"

numeroDoTopico = 3
subtopicos = 3

#numeros que quero pegar, sendo nums o primeiro termo (o tópico geral) e o range a quantidade de decimais do tópico +1
for decimal in range (1,subtopicos+1):
    nums = numeroDoTopico + (decimal/10)

    #pegando as tabelas de 2010 a 2016
    for ano in range(2010,2017):
        path = r"C:\Users\e-enzo.ramos\Desktop\Dados\ME\INEP\Censo do Ensino Superior - Sinopses\Sinopse_Educacao_Superior_%s\Sinopse_Educacao_Superior_%s.ods"%(ano,ano)
        
        try:
            dados = pd.read_excel(path, sheet_name="%s" %(nums))
            with pd.ExcelWriter(pathTeste %(nums), engine='openpyxl', mode="a", if_sheet_exists="replace") as writer:
                dados.to_excel(writer, sheet_name= "%s" %(ano), header= False, index=False)
        except:
            print("algo deu errado no ano %s e no numero %s" %(ano, nums))
            pass

        finally:

            #pegando as tabelas de 2017 a 2021
            for ano in range (2017,2022):
                path = r"C:\Users\e-enzo.ramos\Desktop\Dados\ME\INEP\Censo do Ensino Superior - Sinopses\Sinopse_Educacao_Superior_%s\Sinopse_Educacao_Superior_%s.xlsx"%(ano,ano)
                
                try:
                    dados = pd.read_excel(path, sheet_name="%s" %(nums))
                    with pd.ExcelWriter(pathTeste %(nums), engine='openpyxl', mode="a", if_sheet_exists="replace") as writer:
                        dados.to_excel(writer, sheet_name= "%s" %(ano), header= False, index=False)
                
                except:
                    print("algo deu errado no ano %s e no numero %s" %(ano, nums))
                    pass