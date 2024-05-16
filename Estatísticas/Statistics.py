# coding=utf-8

# EPM Plugins
import Plugins as ep

import numpy as np
import pandas as pd
import tkinter as tk

@ep.DatasetFunctionPlugin('Média móvel', 1)
def mediaMovel():
    '''
    Faz o cálculo de média móvel e plota no dataset.
    '''
    # Verifica se existe apenas uma pena selecionada no Dataset Analysis
    if len(ep.EpmDatasetPens.SelectedPens) != 1:
        ep.showMsgBox("EPM - Estatísticas", "Por favor, execute a consulta do Dataset Analysis \n e selecione uma pena antes de aplicar a função.", "Warning")
        return 0
    
    global windowsize
    windowsize = 0
    Get_WindowSize()
    
    if (windowsize > 0):
        penResult = ep.EpmDatasetPens.SelectedPens[0].Values
        penResult['Value'] = pd.Series(penResult['Value'].byteswap().newbyteorder()).rolling(windowsize).mean()
        penResult = np.delete(penResult, range(windowsize))
        
        ep.plotValues(ep.EpmDatasetPens.SelectedPens[0].Name + '_MovAvg', penResult)













#-----------------------------------Dialogs----------------------------------#
def Get_WindowSize():
    window = tk.Tk()
    window.attributes("-topmost", True)
    DlgWindowSize(window)
    window.mainloop()
    
    
class DlgWindowSize():
    def __init__(self, janela):
        # Inicializa os parametros
        self.window = janela
        self.window.title('EPM - Janela de média móvel')
        # Chama o método para construir a janela
        self.makeScreen()
        
    def makeScreen(self):
        self.wsValue = tk.StringVar()
        # Cria um agrupamento de Opções
        margin = tk.LabelFrame(self.window, bd=0, padx=5,pady=5)
        margin.grid()
        fora = tk.LabelFrame(margin, bd=2, padx=50,pady=5)
        fora.grid()
        cabecalho = tk.LabelFrame(fora, text="Opções", bd=2, padx=40, pady=5)
        cabecalho.grid(sticky = tk.E + tk.W)

        # Dentro do agrupamento, cria um label "Descrição" e um campo para o usuário digitar o texto com sua conclusão de análise.
        lblDescricao = tk.Label(cabecalho,text='Tamanho da janela:')
        lblDescricao.grid(sticky = tk.E)
        
        self.wsValueEdit = tk.Entry(cabecalho, width=10, textvariable=self.wsValue).grid(row=0, column=1, sticky=tk.W)
        self.wsValue.set(str(windowsize))
        
        # Adiciona os botões OK e Cancel, que estão associados aos métodos "action_OK" e "action_Cancel" respectivamente.
        frame_botoes = tk.LabelFrame(fora, bd=0)
        frame_botoes.grid(sticky=tk.E)
        tk.Button(frame_botoes, text='OK', width=10, command=self.action_OK).grid(row=21, column=0, sticky=tk.W, padx=10, pady=8)
        tk.Button(frame_botoes, text='Cancelar', width=10, command=self.action_Cancel).grid(row=21, column=1, sticky=tk.E, padx=10, pady=8)

    def action_Cancel(self):
        # Apenas fecha a janela, destruindo a mesma.
        self.window.destroy()

    def action_OK(self):
        global windowsize
        windowsize = int(self.wsValue.get())
        self.window.destroy()