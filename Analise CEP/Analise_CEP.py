# coding=utf-8

# EPM Plugins
import Plugins as ep

import os
import numpy
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

# Reportlab
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
import reportlab.platypus as pp
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from scipy.stats import norm

# Tkinter
from tkinter import *
import tkinter.filedialog as tkFileDialog


@ep.DatasetFunctionPlugin('Visualizar Histograma', 1)
def histograma():
    """
    Essa funcao gera um histograma da pena selecionada no Dataset Analysis, mostrando o resultado na tela.
    """
    # Verifica se existe apenas uma pena selecionada no Dataset Analysis
    if len(ep.EpmDatasetPens.SelectedPens) != 1:
        sr.msgBox("Elipse Plant Manager - CEP", "Por favor, execute a consulta do Dataset Analysis \n e selecione uma pena antes de aplicar a funcao.", "Warning")
        return 0
    
    # Passa para a variavel 'epmTag' a primeira, e única pena nesse caso, da lista.
    epmTag = ep.EpmDatasetPens.SelectedPens[0].Values
    x = epmTag["Value"]
    mu = epmTag["Value"].mean() # Média da distribuição
    sigma = epmTag["Value"].std() # Desvio Padrão da distribuição

    # Quantidade de conjuntos/grupos que desejamos agrupar os valores de torque (barras verdes)
    num_bins = 20
    # Gera o histograma dos dados
    n, bins, ignore = plt.hist(x, num_bins, density=True, facecolor='green', alpha=0.5)
    # Adiciona uma linha indicando a curva de normalidade (vermelha tracejada)
    y = norm.pdf(bins, mu, sigma)
    plt.plot(bins, y, 'r--')
    plt.xlabel('Torque (Nm)')
    plt.title('Histograma de Torques \n $ mu=' + '{:.3f}'.format(mu) + '$, $ sigma=' + '{:.3f}'.format(sigma) + '$')

    # Mostra na tela o gráfico
    plt.subplots_adjust(left=0.15)
    plt.show()
    plt.close("all")


@ep.DatasetFunctionPlugin('Relatorio CEP em PDF', 2)
def report():
    """
    Essa funcao gera um relatorio CEP em arquivo PDF.
    """
    if len(ep.EpmDatasetPens.SelectedPens) != 1:
        sr.msgBox("Elipse Plant Manager", "Por favor, execute a consulta do Dataset Analysis \n e selecione uma pena antes de aplicar a funcao.", "Warning")
        return 0
    epmTag = ep.EpmDatasetPens.SelectedPens[0].Values
    # Cria uma janela usando a biblioteca Tkinter e passa a pena selecionada como parametro.
    window = Tk()
    window.attributes("-topmost", True)
    GUI(window, epmTag)
    window.mainloop()


# Janela de interface com o usuário.
class GUI():
    def __init__(self, janela, epmTag):
        # Inicializa os parametros
        self.epmTag = epmTag
        self.window = janela
        self.window.title('Elipse Plant Manager - Relatório CEP')
        self.reportPath = StringVar()
        self.txtDescricao = None
        # Chama o método para construir a janela
        self.makeScreen()

    def makeScreen(self):
        # Cria um agrupamento de Opções
        margin = LabelFrame(self.window, bd=0, padx=5,pady=5)
        margin.grid()
        fora = LabelFrame(margin, bd=2, padx=5,pady=5)
        fora.grid()
        cabecalho = LabelFrame(fora, text="Opções", bd=2)
        cabecalho.grid(sticky=E+W)

        # Dentro do agrupamento, cria um label "Descrição" e um campo para o usuário digitar o texto com sua conclusão de análise.
        lblDescricao = Label(cabecalho,text='Descrição:')
        lblDescricao.grid(sticky=E)
        self.txtDescricao = Text(cabecalho, width=65, height=5, wrap=WORD, yscrollcommand=True)
        self.txtDescricao.grid(row=0, column=1, sticky=W)

        # Tambem dentro do agrupamento, cria um label "Local do relatório" e um campo para o usuário visualizar ou digitar o path que será salvo o arquivo PDF.
        lblPath = Label(cabecalho, text='Local do relatório:')
        lblPath.grid(sticky=E)
        txtPath = Entry(cabecalho, width=80, textvariable=self.reportPath)
        txtPath.grid(row=1, column=1, sticky=W)
        self.reportPath.set(os.path.dirname(os.path.abspath(__file__)))

        # Adiciona um botão de Browse com seu comando associado ao método "setFilePath" dessa classe.
        Button(cabecalho, text='...', width=5, command=self.setFilePath).grid(row=1, column=2, sticky=W, padx=5)

        # Adiciona os botões OK e Cancel, que estão associados aos métodos "action_OK" e "action_Cancel" respectivamente.
        frame_botoes = LabelFrame(fora, bd=0)
        frame_botoes.grid(sticky=E)
        Button(frame_botoes, text='OK', width=10, command=self.action_OK).grid(row=21, column=0, sticky=W, padx=10, pady=8)
        Button(frame_botoes, text='Cancelar', width=10, command=self.action_Cancel).grid(row=21, column=1, sticky=E, padx=10, pady=8)

    def action_Cancel(self):
        # Apenas fecha a janela, destruindo a mesma.
        self.window.destroy()

    def setFilePath(self):
        # Abre a janela de "Browse File" da biblioteca Tkinter e seta o novo caminho na propriedade reportPath.
        self.reportPath.set(tkFileDialog.askdirectory())

    def action_OK(self):
        # Cria uma instancia da classe "PDF_Report" passando como parametro o path escolhido pelo usuário na janela.
        pdf = PDF_Report(self.reportPath.get())
        # Chama o método que irá criar o relatorio PDF, passando como parametro os dados (pena selecionada no Dataset Analysis) e
        # o texto da descrição digitado pelo usuário na janela. Retorna um codigo de resultado e o path do grafico criado para deleção.
        res, imgPath = pdf.buildFile(self.epmTag, self.txtDescricao.get("0.0", "end"))
        pdf = None
        if res:
            # O código retornado é diferente de zero, o que indica que houve um erro.
            sr.msgBox("Elipse Plant Manager", "Problema na geracao do relatorio!", "Error")
        else:
            # O relatório foi criado com sucesso (res=0), entao o comando abaixo tenta deletar a imagem.
            try:
                os.remove(imgPath)
            except:
                sr.msgBox("Elipse Plant Manager", "Falha ao deletar o arquivo: \n" + imgPath, 'Error')

            sr.msgBox("Elipse Plant Manager", "Relatorio salvo em: \n" + str(self.reportPath.get()), "Information")
        # Fecha a janela, destruindo a mesma.
        self.window.destroy()


class PDF_Report:
    """
    Esta classe é responsável por criar o arquivo PDF com o conteudo referente a análise CEP.
    Retorna Param1, Param2
    Param1:
        0 = Sem erro.
        1 = Com erro.
    Param2:
        imgPath = Caminho para a imagem gerada do gráfico.
    """
    def __init__(self, folderToSave):
        self.width, self.height = A4
        self.styles = getSampleStyleSheet()
        # Seta a propriodade com p folder onde será salvo o PDF.
        self.folderToSave = folderToSave
        # Pega o caminho da pasta desse plugin para criar o path completo da imagem de cabeçalho do PDF.
        # Exemplo: C:/Users/fulano/Documents/Elipse Software/EPM Studio/Plugins/Analise CEP
        self.logoFile = os.path.dirname(os.path.abspath(__file__)) + "/header.png"
        # Cria o path completo para criar o arquivo PDF.
        self.reportFile = folderToSave + "/EPM - Relatorio CEP.pdf"

    def buildFile(self, epmTag, description):
        if self.folderToSave == "":
            # O usuário nao especificou nenhum caminho para salvar o arquivo, então retorna status de erro.
            return 1, ""
        
        # Cria o objeto "arquivo PDF" com algumas propriedades/opções de formatação.
        # O arquivo, com seu conteudo, só será criado efetivamente no final, ao chamarmos o método build().
        self.doc = pp.SimpleDocTemplate(self.reportFile, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=15, bottomMargin=15)
        # A variavel "story" é uma lista que possuirá todos elementos do relatório (imagens, títulos, parágrafos, textos, etc).
        story=[]
        try:
            # Se a imagem de cabeçalho existir e for aberta com sucesso, a mesma será adicionada na "história".
            logo = pp.Image(self.logoFile, height=25*mm, width=180*mm)
            story.append(logo)
        except:
            # Caso contrário (qualquer erro), não adiciona nenhuma imagem de cabeçalho.
            pass

        # Adiciona alguns Títulos e a descrição informada pelo usuário na janela.
        story.append(pp.Paragraph("Relatório de CEP", self.styles['Heading1']))
        story.append(pp.Paragraph("Descrição da Análise", self.styles['Heading2']))
        story.append(pp.Paragraph(description, self.styles['Normal']))
        
        # Cria uma instância da classe CEP, passando como parâmetro os dados e a pasta para salvar a imagem.
        cep = CEP(epmTag, self.folderToSave)
        # Chama o método da classe responsável por gerar um histograma dos dados. Retorna o caminho da imagem.
        histImgPath = cep.histograma()
        story.append(pp.Paragraph("Histograma", self.styles['Heading2']))
        try:
            # Tenta abrir a imagem gerada do histograma, centraliza a mesma e adiciona na "história".
            imgHist = pp.Image(histImgPath, width=101.6*mm, height=76.2*mm)
            imgHist.hAlign = 'CENTER'
            story.append(imgHist)
        except:
            # Se ocorrer algum erro na abertura da imagem, não faz nada (nenhuma imagem será adicionada).
            pass
        # Agora sim, com a "história" montada, o arquivo PDF é contruido.
        self.doc.build(story)
        self.doc = None
        return 0, histImgPath


# Classe para cálculos de CEP
class CEP:
    """
    Essa classe gera gráficos de CEP e salva como imagem na pasta especificada.
    """
    def __init__(self, epmTag, folderPath):
        self.epmTag = epmTag
        self.folderPath = str(folderPath)

    def histograma(self, figSize=(10.5, 4.5)):
        """
        Cria um histograma dos dados e salva como imagem.
        """
        valores = self.epmTag["Value"]
        media = self.epmTag["Value"].mean() # Média da distribuição
        sigma = self.epmTag["Value"].std() # Desvio Padrão da distribuição

        # Quantidade de conjuntos/grupos que desejamos agrupar os valores de torque (barras verdes)
        num_bins = 20
        # Gera o histograma dos dados
        n, bins, ignore = plt.hist(valores, num_bins, normed=1, facecolor='green', alpha=0.5)
        # Adiciona uma linha indicando a curva de normalidade (vermelha tracejada)
        y = mlab.normpdf(bins, media, sigma)
        plt.plot(bins, y, 'r--')
        plt.xlabel('Torque (Nm)')
        plt.title("Histograma de Torques \n $ mu=" + "{:.3f}".format(media) + "$, $ sigma=" + "{:.3f}".format(sigma) + "$")
        plt.savefig(self.folderPath + "/histograma.png")
        plt.close("all")
        return self.folderPath + "/histograma.png"
