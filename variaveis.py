from Banco import Banco
from datetime import date
from tkinter import PhotoImage

#DATA
data = date.today().strftime("%d/%m/%Y")



#TAMANHO DA JANELA PRINCIPAL
largura = 1024
altura = 600

#COORDENADAS DOS TEXTOS DAS CAIXAS DE ENTRADA E DAS CAIXAS
xLabels = 40
xEntrys = 165
yInicialCadastro = 50

#TAMANHO DA CAIXA DE ENTRADA
entrysWidth = 30

#CORES
cor_principal = "grey13" 
cor_secundaria = "grey8"
cor_contraste = "white"
cor_meta = "orange red"
cor_destaque = "red"

#FONTES
fonte_Titulos = ("Century Gothic",32)
fonte_Destaques = ("Century Gothic",24)
fonte_Textos = ("Century Gothic",12)

#TEXTOS PADROES
titulo = "META CERTIFICADO DIGITAL "

# LISTAS
lista_locais = []

lista_certificados = [
    'A1',
    'A3 - TOKEN',
    'A3 - CARTAO',
    'A3 - TOKEN E CARTAO',
    'NENHUM'
    ] 

lista_solicitantes = [
    'AGR',
    'CLIENTE'
    ]

lista_atendimentos = [
    "INSTALAÇÃO DRIVE",
    "INSTALAÇÃO CERTIFICADO",
    "PARAMETRIZAÇÃO",
    "EMISSÃO DE CERTIFICADO",
    "DESBLOQUEIO DE MÁQUINA",
    "DESBLOQUEIO PIN",
    "INICIALIZAÇÃO DE DISPOSITIVO",
    "SISAGR",
    "INVENTÁRIO DE MÁQUINA",
    "CRM",
    "JAVA",
    "MANUTENÇÕES",
    "CONECTIVIDADE",
    "E-SAJ",
    "PJE",
    "TJ",
    "IDENTIFICAÇÃO DE MÍDIA",
    "BIRDID",
    "ALTERAR SENHA",
    "A1 NÃO CONSTA",
    "EMISSOR DE NOTA",
    "DÚVIDA CERTIFICADO",
    "INSTALAÇÃO APLICATIVOS",
    "PERDA DE CERTIFICADO"
    ]