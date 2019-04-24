# encoding=utf8  
# coding=UTF-8

import zipfile, os, datetime
from os import listdir
from datetime import date

import Constantes, Util

dados = dict()
todosLabels = []
imprimirLog = True 

def main():
    global dados
    p("Início do processamento...")
    if getArquivoZip():
        getArquivosCsv()
    p("Fim do processamento...")
    #imprimeDados()
    gerarRelatorios()

def descompactar(arquivo):
    zip_ref = zipfile.ZipFile(Constantes.pastaArquivoZip+arquivo, 'r')
    zip_ref.extractall(Constantes.pastaArquivoCsv)
    zip_ref.close()

def getArquivoZip():
    retorno = False
    for f in listdir(Constantes.pastaArquivoZip):
        if f[-3:].lower() == "zip":
            p("Descompactando arquivo: " + f)
            descompactar(f)
            #moverArquivo(f, Constantes.pastaArquivoZip, Constantes.pastaArquivoZipProc)
            retorno = True 
            break           
    return retorno

def getArquivosCsv():
    p("Buscando arquivos CSV")    
    for f in listdir(Constantes.pastaArquivoCsv):
        if f[-3:].lower() == "csv":
            p("Tratando arquivo: " + f)
            tratarCsv(f)
            moverArquivo(f, Constantes.pastaArquivoCsv, Constantes.pastaArquivoCsvProc)

def tratarCsv(arquivo):
    global dados
    global todosLabels
    f = open(Constantes.pastaArquivoCsv+arquivo, 'r')
    labels = quebrarLinha(f.readline())
    for linha in f:                      
        addDados(arquivo.split(Constantes.sepNmArq)[0], labels, linha)
    f.close()

def addDados(indicador, labels, linha):
    global dados
    array = quebrarLinha(linha)
    if not dados.get(array[0]):
        dados.update({array[0]:{}})
    if not dados.get(array[0]).get(indicador):
        dados.get(array[0]).update({indicador:{}})    
    if not dados.get(array[0]).get(indicador).get(array[1]):
        dados.get(array[0]).get(indicador).update({array[1]:{}})
    cont = 2
    for coluna in array[2:]:
        dados.get(array[0]).get(indicador).get(array[1]).update({labels[cont]:coluna})
        cont += 1

def addDadosI(indicador, labels, linha):
    global dados
    array = quebrarLinha(linha)
    if not dados.get(indicador):
        dados.update({indicador:{}})
    if not dados.get(indicador).get(array[0]):
        dados.get(indicador).update({array[0]:{}})    
    if not dados.get(indicador).get(array[0]).get(array[1]):
        dados.get(indicador).get(array[0]).update({array[1]:{}})
    cont = 2
    for coluna in array[2:]:
        p("Indicador: " + indicador)
        p(" >>Resp: " + array[0])
        p("  >>Mes: " + array[1])
        p("   >>Label: " + labels[cont] + " - Valor: " + coluna)        
        dados.get(indicador).get(array[0]).get(array[1]).update({labels[cont]:coluna})
        cont += 1

def apagarRelatorios():
    filelist = [ f for f in os.listdir(Constantes.pastaArquivosHTML)]
    for f in filelist:
        os.remove(os.path.join(Constantes.pastaArquivosHTML, f))
       
def gerarRelatorios():
    apagarRelatorios()
    f = open(Constantes.templateBasico, 'r')
    htmlBasico = ""
    for linha in f:
        htmlBasico += linha
    f.close()
    for lotacao, info in dados.iteritems():
        gerarArquivo(lotacao, htmlBasico)

def gerarArquivo(lotacao, htmlBasico):    
    for indicador, meses in dados.get(Constantes.txDepto).iteritems():
        if "<<"+indicador+">>" in htmlBasico:
            htmlBasico = htmlBasico.replace("<<"+indicador+">>",getHtmlIndicador(lotacao, indicador))

    f = open(Constantes.pastaArquivosHTML+lotacao.replace("/","_")+".html", 'w')
    f.write(htmlBasico.replace(Constantes.tagLotacao,lotacao[-5:]))
    f.close()

def getHtmlIndicador(lotacao, indicador):
    p("Lotação: " + lotacao + " - Indicador: " + indicador) 
    htmlLinhas = ""
    for mes, infos in sorted(dados.get(Constantes.txDepto).get(indicador).iteritems()):
        htmlMes = "<td>"+mes+"</td>"
        htmlLabels = ""
        htmlDepto = ""
        htmlLotacao = ""
        quantColunas = 0
        for info, valor in infos.iteritems():
            htmlLabels += "<td><i>"+info+"</i></td>"           
            htmlDepto += "<td>"+valor+"</td>"
            try:
                valorLotacao = dados.get(lotacao).get(indicador).get(mes).get(info)
            except AttributeError:
                valorLotacao = "N/A"
            htmlLotacao += "<td>"+valorLotacao+"</td>"
            quantColunas += 1
        htmlLinhas += "<tr>" + htmlMes + htmlLotacao + htmlDepto + "</tr>"

    htmlTh = "<tr><th colspan="+str(2*quantColunas+1)+">"+indicador+"</th></tr>"
    htmlTit = "<tr><td align=center><b>MÊS</b><td align=center colspan="+str(quantColunas)+"><b>"+lotacao[-5:]+"</b></td>"+\
              "<td align=center colspan="+str(quantColunas)+"><b>"+Constantes.txDepto+"</b></td></tr>"
    htmlCompleto = htmlTh+htmlTit+"<tr><td>&nbsp;</td>"+htmlLabels+htmlLabels+"</tr>"+htmlLinhas
    p(htmlCompleto[:5])
    return htmlCompleto

def gerarDadosBasicos(lotacao):
    f = open(Constantes.templateBasico, 'r')
    htmlBasico = ""
    for linha in f:
        htmlBasico += linha
    f.close()
    texto = substituirTags(htmlBasico, lotacao)
    f = open(Constantes.pastaArquivosHTML+idLinha+".html", 'w')
    f.write(texto)
    f.close()
    
def substituirTags(texto, idLinha):
    retorno = texto
    for label in todosLabels:
        dado = str(dados.get(idLinha).get(label))
        try:
            dado = float(dado)
            dado = str(dado).rstrip('0').rstrip('.')
        except ValueError:
            pass
        retorno = retorno.replace("<<"+label+">>",dado)
    return retorno

def incluirCamposCalculados(ss):
    global dados
    desvioHH = None
    desvioProd = None
    prodReal = None
    if dados.get(ss).get(Constantes.lbHHReal):
        desvioHH = float(dados.get(ss).get(Constantes.lbHHReal)) - float(dados.get(ss).get(Constantes.lbHHPrev))
        
    if dados.get(ss).get(Constantes.lbPFReal):
        prodReal = float(dados.get(ss).get(Constantes.lbHHReal))/float(dados.get(ss).get(Constantes.lbPFReal))
    elif dados.get(ss).get(Constantes.lbPFPrev):
        prodReal = float(dados.get(ss).get(Constantes.lbHHReal))/float(dados.get(ss).get(Constantes.lbPFPrev))
    
    if prodReal:
        desvioProd = prodReal - float(dados.get(ss).get(Constantes.lbProdPrev))
    dtPrevEnt = dados.get(ss).get(Constantes.lbDtPrevEnt)
    dtUltEnt = dados.get(ss).get(Constantes.lbDtUltEnt)    
    
    if dtPrevEnt and dtUltEnt:
        dtPrevEnt = date(int(dtPrevEnt[0:4]),int(dtPrevEnt[5:7]),int(dtPrevEnt[8:10]))
        dtUltEnt = date(int(dtUltEnt[0:4]),int(dtUltEnt[5:7]),int(dtUltEnt[8:10]))
        desvioPrazo = (dtUltEnt-dtPrevEnt).days
    dados.get(ss).update({Constantes.lbAprop:getTextoApropriacao(ss),\
                            Constantes.lbDesvioHH:desvioHH,\
                            Constantes.lbProdReal:prodReal,\
                            Constantes.lbDesvioProd:desvioProd,\
                            Constantes.lbDesvioPrazo:desvioPrazo})

def getTextoApropriacao(ss):
    retorno = ""
    if dados.get(ss).get(Constantes.dadosAprop):
        for macro, horas in dados.get(ss).get(Constantes.dadosAprop).iteritems():
            retorno += macro + ": <b>" + horas.rstrip(".0") + " HH</b><br>"
    return retorno

def analisarDados(ss):
    analisarEntrega(ss)
    analisarProd(ss)
    
def analisarEntrega(ss):
    texto = "Sem dados para avaliar a Entrega."
    if dados.get(ss).get(Constantes.lbDesvioPrazo) != None:
        texto = ""
        desvioPrazo = int(dados.get(ss).get(Constantes.lbDesvioPrazo))
        if desvioPrazo <= 0:
            f = open(Constantes.templateAnEntregaOK, 'r')
        else:
            f = open(Constantes.templateAnEntregaNOK, 'r')
        for linha in f:
            texto += linha 
        f.close()
    dados.get(ss).update({Constantes.lbAnEntrega:substituirTags(texto,ss)})

def analisarProd(ss):
    texto = "Sem dados para avaliar a Produtividade."
    if dados.get(ss).get(Constantes.lbDesvioProd) != None:
        texto = ""
        desvioProd = int(dados.get(ss).get(Constantes.lbDesvioProd))
        if desvioProd <= 0:
            f = open(Constantes.templateAnProdOK, 'r')
        else:
            f = open(Constantes.templateAnProdNOK, 'r')
        for linha in f:
            texto += linha 
        f.close()
    dados.get(ss).update({Constantes.lbAnProd:substituirTags(texto,ss)})


def quebrarLinha(linha):
    array = linha.replace("|ALM","").replace("\"","").split(Constantes.sep)
    return array[:-1]
                       
def moverArquivo(arquivo, pastaOrigem, pastaDestino):
    os.rename(pastaOrigem+arquivo, pastaDestino+gerarNmArq()+"."+arquivo[-3:])    

def gerarNmArq():
    nmArq = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    return nmArq


def imprimeDados():
    for indicador, resps in dados.iteritems():
        p(">>"+indicador)
        for resp, meses in resps.iteritems():
            p(" >>"+resp)
            for mes, infos in meses.iteritems():
                p("  >>"+mes)
                for info, valor in infos.iteritems():
                    p("   >>"+info+": "+valor)

def p(texto):
    if imprimirLog:
        print texto

main()
