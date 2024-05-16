# Elipse Plant Manager - EPM Dataset Analysis Python Plugins

 Exemplo de um plugin em linguagem Python (v.3.12) para uso no ambiente *Dataset Analysis* do **EPM Studio** - ferramenta do sistema **EPM v.3+**.

## INSTALAÇÃO

Para usar este plugin, basta colocar os arquivos: *Statistics.py* e *0_pluginIcon.png* dentro do diretório: *C:\Users\ ... \My Documents\ ... \Elipse Software\EPM Studio\Plugins\Estatísticas*

No Python utilizado, devem ser instaladas as bibliotecas utilizadas por este plugin, que são:
- [Numpy](https://numpy.org/)
- [Pandas](https://pandas.pydata.org/)
- [TKInter](https://docs.python.org/3/library/tkinter.html)

Depois, é só abrir um **Dataset** no **EPM Studio** e expandir a área de *scripts* em linguagem Python.
Além de carregar os módulos (bibliotecas) configurados no arquivo de inicialização deste ambiente, todos os plugins em Python encontrados no diretório Plugins (mencionado anteriormente) serão carregados e apresentados na *ribbon* (faixa de opções) do ambiente *Dataset Analysis* do **EPM Studio**.

Para mais detalhes de como fazer plugins para o ambiente *Dataset Analysis* do **EPM Studio** utilizando a linguagem Python, conferir o artigo [Agilizando análises no EPM Studio Dataset Analysis (EPM 3) através de plugins](../KB5435/README.md)
