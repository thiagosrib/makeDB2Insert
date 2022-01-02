# -*- coding: utf-8 -*-
import os, datetime, glob
from   subprocess import Popen, call
from   getpass    import getpass
from   time       import sleep, gmtime, time
from   Diretorio  import *
from   Tkinter    import *
import pdb

global tabela

def get_tabela():
    global tabela

    tabela = 'DB2PRD.' + e1.get().upper().replace('\n', '')
    master.quit()

    return tabela

def trata_colunas(linha = ''):
    if  not linha.strip():
        print
        print '**********************************************'
        print '* Erro na rotina trata_colunas. Linha vazia. *'
        print '**********************************************'
        print
        return False

    indIni   = 0
    indFim   = 0
    ind      = 0
    qtdeCols = len(linha.rstrip().split(' -')) - 1

    while ind <= qtdeCols:
        ind += 1

        if  ind > qtdeCols:
            break

        indIni = indIni + linha[indIni:].find(' --') + 1
        indFim = linha[indIni:].find('-- ') + 2 + indIni
        indice = 'col' + str(ind)
        defColunas[indice] = {'ini': indIni, 'fim': indFim}

    return defColunas

def is_int_or_float(vlr):
    try:
        if  int(vlr):
            return True
        else:
            if  vlr.replace('.', '', 1).isdigit():
                return True
            else:
                return False
    except ValueError:
        try:
            if  float(vlr):
                return True
            else:
                if  vlr.replace('.', '', 1).isdigit():
                    return True
                else:
                    return False
        except ValueError:
            return False

def gera_Insert(defColunas = {}, linha = '', tabela = ''):
# ini  para verificar se um campo eh numerico (int ou float)
    import re
    p = re.compile('\d+(\.\d+)?')
# fim

    if  not linha.strip():
        print
        print '**********************************************'
        print '*  Erro na rotina gera_Insert. Linha vazia.  *'
        print '**********************************************'
        print
        return False

    if  not defColunas:
        print
        print '***********************************************************'
        print '* Erro na rotina gera_Insert. Definicao de colunas vazia. *'
        print '***********************************************************'
        print
        return False

    ind      = 0
    linhaN   = []
    linha_N  = []
    qtdeCols = len(defColunas.keys())
    linhaN.append('INSERT INTO {0} VALUES ('.format(tabela))

    while ind <= qtdeCols:
        ind += 1

        if  ind > qtdeCols:
            break
        
        indice = 'col' + str(ind)
        coluna = linha[defColunas[indice]['ini']:defColunas[indice]['fim']].replace("'", '').replace('"', '')

        if  len(coluna.strip()) < 1:
            coluna = ' '

        if  (len(', '.join(linha_N)) + len(', ' + coluna)) > 65:
            linhaN.append(', '.join(linha_N) + ',')
            linha_N = []

# alterar para efetuar o tratamento do proprio campo ser maior que 72 posicioes (quebrar linha)
        if  len(coluna) > 72:
            i = 0
            coluna_N = ''
            col_Prim = True

            while i < len(coluna):
                if  col_Prim:
                    coluna_N += coluna[:72] + '\n'
                    col_Prim  = False
                    i += 71
                else:
                    coluna_N += coluna[i:i+73] + '\n'
                    i += 72

            coluna   = coluna_N
            coluna_N = ''

        coluna = coluna.replace(',', '.')

# ini - valida se campo eh numerico (int ou float)
##        if  p.match(coluna.strip()):
# fim
        if  is_int_or_float(coluna.strip()):
            if  len(coluna.strip().split('.')) > 2    or \
                coluna[0]                     == '0'  or \
                coluna[-1]                    == ' '  or \
                coluna[-1]                    == '\n' or \
                coluna.find('-')              != -1   or \
               (coluna[0]  in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and \
               (coluna[-1] == ' ' or coluna[-1] == '\n')):
                linha_N.append(("'" + str(coluna.rstrip()) + "'") if coluna.strip() != '-' else 'NULL')
            else:
                linha_N.append(coluna.strip())
        else:
            linha_N.append(("'" + str(coluna.rstrip()) + "'") if coluna.strip() != '-' else 'NULL')

#        if  coluna[0] == ' ':
#            if  coluna[-1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and \
#                coluna.strip().isdigit():
#                coluna = coluna.replace(',', '.')
#                linha_N.append(coluna.strip())
#            else:
#                linha_N.append("'" + str(coluna.rstrip()) + "'")
#        else:
#            if  coluna[0]  in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] and \
#                coluna.strip().isdigit() and \
#                coluna[-1] == ' ':
#                linha_N.append("'" + str(coluna.rstrip()) + "'")
#            else:
#                coluna = coluna.replace(',', '.')
#                linha_N.append("'" + str(coluna.rstrip()) + "'")

    linhaN.append(', '.join(linha_N) + ',')

    if  linhaN[-1][-1] == ',':
        linhaN[-1] = linhaN[-1][:-1]

    linhaN.append(');\n')
    return '\n'.join(linhaN)

if __name__ == "__main__":
    '''
        Script para gerar comandos INSERT a partir de query executada no QMF 
    '''

    global tabela
    tabela = ''

    Tk().withdraw()
    master = Tk()
    Label(master, text='Informe a tabela desejada').grid(row=0, column=1, sticky=W, pady=4)
    Label(master, text='DB2PRD.').grid(row=1)

    e1 = Entry(master)

    e1.grid(row=1, column=1)

    Button(master, text='Cancelar', command=master.quit).grid(row=4, column=0, sticky=W, pady=4)
    Button(master, text='Continuar', command=get_tabela).grid(row=4, column=1, sticky=W, pady=4)

    mainloop()

    if  tabela and tabela != 'DB2PRD.':
        master.quit()
        diretorio  = Diretorio()
        arquivo    = diretorio.selectDirectory(txtDisplay = 'Selecione a pasta onde esta o arquivo', onlyDir = False)
        dados      = False
        defColunas = {}
        ind        = 0
        linhas     = open(arquivo, 'r').readlines()
        diretorio  = '/'.join(arquivo.split('/')[:-1])
        arquivoIns = open(os.path.join(diretorio, 'Insert_' + tabela.split('DB2PRD.')[-1] + '.txt'), 'w')

        while ind <=  (len(linhas) - 1):
            if  ind > (len(linhas) - 1):
                break

            linha = linhas[ind]

            if (linha.find(' ---')  == -1 or \
                linha.find('  ---') == -1 or \
                not linha.strip())       and \
                not dados:
                ind += 1
                continue

            if  not dados:
                defColunas = trata_colunas(linha = linha.replace('\n', ' '))
                dados = True
                ind += 1
                continue

            if  dados         and \
                linha.strip() and \
                linha.find(' END ') == -1:
                linhaN = gera_Insert(defColunas = defColunas, linha = linha, tabela = tabela)
                arquivoIns.writelines(linhaN)

            ind += 1

        arquivoIns.close()

        master = Tk()
        Label(master, text='Comando(s) gerado(s) com sucesso.').grid(row=0, column=0, sticky=W, pady=4)

        Button(master, text=' Ok ', command=master.quit).grid(row=1, column=1, sticky=W, pady=4)
        mainloop()
    else:
        master.quit()
        master = Tk()
        Label(master, text='Nenhuma tabela informada. Execucao cancelada.').grid(row=0, column=1, sticky=W, pady=4)

        Button(master, text=' Ok ', command=master.quit).grid(row=1, column=1, sticky=W, pady=4)
        mainloop()