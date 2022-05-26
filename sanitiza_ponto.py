##################################################################################
###### Script de sanitização dos arquivos TXTs - HENRYAFD                        #
###### Escrito por Paulo Bini em 10/03/2022                                      #
###### Modificado em 08/04/2022                                                  #
##################################################################################

import glob
import os
import datetime
import re
import platform

#Dias preservados nos TXTs
lastxdias = 7

#Definição do diretório HENRYAFD, tamanho da string totalizadora e range de caracteres que contém a data
#AMBIENTE WINDOWS
if platform.system() == 'Windows':
    henryafd_dir = 'C:/henryafd/'
    sizestringtotalizador = 279
    rangeinit = 258
    rangeend = 266

#AMBIENTE LINUX
if platform.system() == 'Linux':
    henryafd_dir = (os.path.join(os.getcwd(),'henryafd/'))
    sizestringtotalizador = 278
    rangeinit = 257
    rangeend = 265

diff_dir = (os.path.join(henryafd_dir,'diff/'))

dia = []
dias = 0

#Cria a lista dos dias que serão preservados
while dias <= lastxdias:
    diabase = datetime.date.today()
    diasubtracao = datetime.timedelta(days=dias)
    diaresultado = diabase - diasubtracao
    dia.append(str(diaresultado.strftime('%d')+diaresultado.strftime('%m')+diaresultado.strftime('%Y')))
    dias = int(dias)+1

#Varre os txts do diretório henryafd e cria um arquivo diff vazio equivalente
for arquivos in (glob.glob(henryafd_dir+"*.txt")):
    arquivo = os.path.split(arquivos)
    arquivo_diff = os.path.join(diff_dir,arquivo[1])
    if os.path.exists(arquivo_diff):
        os.remove(arquivo_diff)
    with open(arquivo_diff, 'w') as f:
        f.write('')
    diff = open(arquivo_diff,'a')
    contlinha = 0
    hit = 0

#Abre arquivo por arquivo e faz a leitura linha por linha
    for linha in open (arquivos):
        contlinha = contlinha+1
        datatotalizador = None
        registro = None

#Procura pela linha totalizadora dentro dos dias abrangidos na lista
        if len(linha) == sizestringtotalizador:
            datatotalizador = linha[rangeinit:rangeend]
#Guarda a primeira linha do arquivo
        if contlinha ==1:
            registro = linha
        elif hit == 0:
#Se encontra um totalizador de data válida, aciona o hit e copia todas as linhas abaixo para o diff
            if datatotalizador:
                for i in range(len(dia)):
                    achou = re.match(dia[i], datatotalizador)
                    if achou:
                        hit = 1
        else:
            registro = linha
        if registro != None:
            diff.write(registro)
    diff.close()