from tkinter import Tk, StringVar, Frame,Entry,Label,Button,Menu,BooleanVar,Checkbutton,PhotoImage,END,RIGHT,LEFT,TOP,BOTTOM,CENTER,VERTICAL,Y,HORIZONTAL,X
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
import numpy as np
import datetime
import calendar
import pandas as pd
from Classes import AutocompleteCombobox 
from variaveis import *

class Janela:
    def __init__(self, master=None):

        #BARRA DE MENUS
        menubar = Menu(master)
        master.config(menu=menubar)

        #MENU OPCOES
        opmenu = Menu(menubar,tearoff=0)
        opmenu.add_command(label="Visualizar Atendimentos", command=self.Visualizar)
        menubar.add_cascade(label="Opções", menu=opmenu)

        #MENUN SOBRE
        sobremenu = Menu(menubar,tearoff=0)
        sobremenu.add_command(label="Sobre", command=self.Sobre)
        menubar.add_cascade(label = "?", menu = sobremenu)

        #INICIA BANCO DE DADOS
        self.banco = Banco()
        self.dia = False

        #TITULO
        self.TopFrame = Frame(master, width = largura, height = 100, bg = cor_principal, relief = "raise" )
        self.TopFrame.pack(side=TOP)

        #Logo da Meta e Titulo do programa
        self.logo = PhotoImage(file="icons/logo_.png")
        self.logo_meta = Label(self.TopFrame, image=self.logo,bg=cor_principal)
        self.logo_meta.place(x=5,y=5)
        self.meta = Label(self.TopFrame,text = "Controle de Atendimentos",font=fonte_Titulos, fg= cor_contraste, bg=cor_principal)
        self.meta.place(x=280,y=25)

        #AMBIENTE DE INFORMACOES 1
        self.infosFrame = Frame(master, width = 450, height = 150, bg=cor_principal,relief="raise")
        self.infosFrame.place(x = 540,y=150)

        #Data 
        self.date = Label(self.infosFrame,text=data,fg=cor_contraste,bg=cor_principal,font=fonte_Destaques)
        self.date.place(x=140,y=5)

        #Quantidade de Atendimentos
        self.qtd_atendimentos = self.banco.current 
        self.dados = self.banco.dados
        self.n_atendiLabel = Label(self.infosFrame, text="Atendimentos Realizados", fg = cor_contraste, bg=cor_principal, font=fonte_Textos)
        self.n_atendiLabel.place(x=15,y=50)
        self.frame_aux = Frame(self.infosFrame, width = 200, height = 50, bg = cor_secundaria, relief="raise")
        self.frame_aux.place(x=15, y=85)
        self.qtd = Label(self.frame_aux,text=self.qtd_atendimentos, bg = cor_secundaria , fg=cor_destaque, font=fonte_Destaques)
        self.qtd.place(relx=0.5, rely=0.5,anchor=CENTER)

        #Quantidade de Atendimentos do Dia
        self.qtd_h = self.dados.loc[self.dados["Data"] == data].count()
        self.n_atendiHLabel = Label(self.infosFrame, text="Atendimentos de Hoje", fg = cor_contraste, bg=cor_principal, font=fonte_Textos)
        self.n_atendiHLabel.place(x=235,y=50)
        self.frame_auxH = Frame(self.infosFrame, width = 200, height = 50, bg = cor_secundaria, relief="raise")
        self.frame_auxH.place(x=235, y=85)
        self.qtd_hj = Label(self.frame_auxH,text=self.qtd_h[0], bg = cor_secundaria , fg=cor_destaque, font=fonte_Destaques)
        self.qtd_hj.place(relx=0.5, rely=0.5,anchor=CENTER)

        #AMBIENTE DE INFORMACOES 2
        self.infos_2Frame = Frame(master, width = 450, height = 225, bg=cor_principal,relief="raise")
        self.infos_2Frame.place(x = 540,y=325)

        #VISUALIZACAO RAPIDA DE CADASTROS 
        self.dadosCols = tuple(self.banco.dados.columns)
        self.listagem = ttk.Treeview(self.infos_2Frame,columns = self.dadosCols, show='headings', height = 10, selectmode='extended')

        self.listagem.bind('<Double-1>',self.Mostrar)

        self.listagem.column("Id", width = 25)
        self.listagem.heading("Id",text="ID")

        self.listagem.column("Local", width = 70)
        self.listagem.heading("Local",text="Local")

        self.listagem.column("Solicitante", width = 70)
        self.listagem.heading("Solicitante",text="Solicitante")

        self.listagem.column("Atendimento", width = 70)
        self.listagem.heading("Atendimento",text="Atendimento")

        self.listagem.column("Certificado", width = 70)
        self.listagem.heading("Certificado",text="Certificado")

        self.listagem.column("Meta", width = 35)
        self.listagem.heading("Meta",text="Meta")

        self.listagem.column("Resolvido", width = 35)
        self.listagem.heading("Resolvido",text="Resolvido")

        self.listagem.column("Data", width = 70)
        self.listagem.heading("Data",text="Data")

        self.listagem.pack(side=LEFT)

        #BARRAS DE ROLAGEM DA VISUALIZACAO
        self.ysb = ttk.Scrollbar(self.infos_2Frame, orient=VERTICAL, command=self.listagem.yview)
        self.listagem['yscroll'] = self.ysb.set
        self.ysb.pack(side = RIGHT, fill = Y)

        # TEXTOS DOS CABEÇALHO
        for c in self.dadosCols:
            self.listagem.heading(c, text=c.title())

        # INSRINDO OS ITENS
        for item in self.dados.loc[self.dados["Data"]==data].values:
            self.listagem.insert('', 'end', values=tuple(item))

        #AMBIENTE DE CADASTRO
        self.cadastroFrame = Frame(jan, width = 450, height = altura-200, bg=cor_principal,relief="raise")
        self.cadastroFrame.place(x = 40,y=150)

        #LOCAL
        self.localLabel = Label(self.cadastroFrame,text = "Local: ",font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_principal)
        self.localLabel.place(x = xLabels,y = yInicialCadastro )
        self.localEntry = AutocompleteCombobox(self.cadastroFrame, width = entrysWidth)
        lista_locais = list(self.banco.dados["Local"].drop_duplicates())
        self.localEntry.set_completion_list(lista_locais)
        self.localEntry.place(x = xEntrys, y = yInicialCadastro)

        #SOLICITANTE
        self.solLabel = Label(self.cadastroFrame,text = "Solicitante: ",font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_principal)
        self.solLabel.place(x = xLabels,y =yInicialCadastro + 70 )
        self.solEntry = AutocompleteCombobox(self.cadastroFrame, width = entrysWidth)
        self.solEntry.set_completion_list(lista_solicitantes)
        self.solEntry.place(x = xEntrys, y = yInicialCadastro + 70 )

        #ATENDIMENTO
        self.atendLabel = Label(self.cadastroFrame,text = "Atendimento: ",font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_principal)
        self.atendLabel.place(x = xLabels,y = yInicialCadastro + 140 )
        self.atendEntry = AutocompleteCombobox(self.cadastroFrame, width = entrysWidth)
        self.atendEntry.set_completion_list(lista_atendimentos)
        self.atendEntry.place(x = xEntrys, y = yInicialCadastro + 140 )

        #CERTIFICADO
        self.certLabel = Label(self.cadastroFrame,text = "Certificado: ",font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_principal)
        self.certLabel.place(x = xLabels,y = yInicialCadastro + 210 )
        self.certEntry = AutocompleteCombobox(self.cadastroFrame, width = entrysWidth)
        self.certEntry.set_completion_list(lista_certificados)
        self.certEntry.place(x = xEntrys, y = yInicialCadastro + 210 )

        #META
        self.chkValueMeta = BooleanVar() 
        self.chkValueMeta.set(False)
        self.chkMeta = Checkbutton(self.cadastroFrame, text='Dispostivo da Meta',var = self.chkValueMeta,bg=cor_principal, activebackground = cor_principal, fg=cor_contraste, selectcolor= cor_principal)
        self.chkMeta.place(x= xLabels,y = yInicialCadastro + 260)

        #RESOLVIDO
        self.chkValueResol = BooleanVar() 
        self.chkValueResol.set(False)
        self.chkResolv = Checkbutton(self.cadastroFrame, text='Problema Resolvido',var = self.chkValueResol,bg=cor_principal, activebackground = cor_principal, fg=cor_contraste, selectcolor = cor_principal)
        self.chkResolv.place(x = xEntrys + 100 ,y = yInicialCadastro + 260 )

        #BOTAO DE INSERIR
        self.cadastroButton = Button(self.cadastroFrame, text = "Inserir Atendimento", bg=cor_principal, fg=cor_contraste, width = entrysWidth,command = self.Inserir)
        self.cadastroButton.place(x = xEntrys - 50, y = yInicialCadastro + 300)
    
    def Calendar(self) :
        
            # Create a GUI window
        self.new_gui = Tk()
        
        # Set the background colour of GUI window
        self.new_gui.config(background = cor_principal)
        
        #self.new_gui.resizable(width = False, height = False)
        #Transparencia
        self.new_gui.attributes("-alpha",0.95)
    
        # set the name of tkinter GUI window
        self.new_gui.title("CALENDARIO")
    
        # Set the configuration of GUI window
        self.new_gui.geometry("250x300")

        def Proximo_Mes():
            self.fetch_month += 1
            if self.fetch_month == 13:
                self.fetch_year += 1
                self.fetch_month = 1
            self.cal_content = calendar.month(self.fetch_year,self.fetch_month)
            self.call_cal["text"] = self.cal_content
        
        def Volta_Mes():
            self.fetch_month -= 1
            if self.fetch_month == 0:
                self.fetch_year -= 1
                self.fetch_month = 12
            self.cal_content = calendar.month(self.fetch_year,self.fetch_month)
            self.call_cal["text"] = self.cal_content

        # get method returns current text as string
        self.fetch_year = 2021
        self.fetch_month = 1
    
        # calendar method of calendar module return
        # the calendar of the given year .
        self.cal_content = calendar.month(self.fetch_year,self.fetch_month)

        self.Frame_But = Frame(self.new_gui,width = 250, height = 40, bg=cor_principal,relief="raise")
        self.Frame_But.pack(side=TOP)
        self.Frame_Calen = Frame(self.new_gui,width = 250, height = 300, bg=cor_principal,relief="raise")
        self.Frame_Calen.pack(side=TOP)
    
        self.ant_but = Button(self.Frame_But, text="Anterior", width = 10, command = Volta_Mes, bg=cor_principal, fg = cor_contraste)
        #self.ant_but.grid(row = 1,column = 0,padx=1)
        self.ant_but.place(x=20,y=15)

        self.next_but = Button(self.Frame_But, text="Proximo", width = 10, command = Proximo_Mes, bg=cor_principal, fg = cor_contraste)
        self.next_but.place(x=150,y=15)
        #self.next_but.grid(row = 1, column = 0, padx=0.5)
        
        # Create a label for showing the content of the calender
        self.call_cal = Label(self.Frame_Calen, text = self.cal_content, font = "Consolas 15 bold", anchor="e",justify=LEFT,bg=cor_principal, fg = cor_contraste)
        # grid method is used for placing
        # the widgets at respective positions
        # in table like structure.
        self.call_cal.place(x=10,y=20)
        #self.call_cal.grid(row = 3, column = 0, padx = 10)
        
        # start the GUI
        self.new_gui.mainloop()
    
    def Selecionar_Data(self):
        def Data_escolhida():
            self.data = cal.selection_get()
            cal.see(datetime.date(year=2016, month=2, day=5))
            for item in self.banco.dados.loc[self.banco.dados["Data"]==self.dia].values:
                self.listagem_v.insert('', 'end', values=tuple(item))

        jan_cal = Tk()
        
        try:
            primeira_data = self.banco.dados["Data"].iloc[0]
            primeira_data = primeira_data.split("/")
            primeira_data = datetime.date(int(primeira_data[2]),int(primeira_data[1]),int(primeira_data[0]))
        except:
            primeira_data = datetime.date.today()

        data_ = data.split("/")
        ultima_data = datetime.date(int(data_[2]),int(data_[1]),int(data_[0])) + datetime.timedelta(days=1)

        print(primeira_data, ultima_data)

        cal = Calendar(jan_cal, font=fonte_Textos, locale='pt_BR',
                    mindate=primeira_data, maxdate=ultima_data, bg = "grey10",fg='grey8',
                    year=2018, month=2)
        cal.pack(fill="both", expand=True)

        ttk.Button(jan_cal, text="ok", command=Data_escolhida).pack()
    
    def to_datetime(x=""):
        x = x.split("/")
        return datetime.date(int(x[2]),int(x[1]),int(x[0]))
         
    def to_data(x):
        return x.strftime("%d/%m/%Y")

    def Visualizar(self):
        #banco = Banco()
        #Abre a nova janela
        self.visualizar_janela = Tk()

        #CONFIGURACOES ----
        #Titulo
        self.visualizar_janela.title(titulo)
        #Tamanho da janela
        self.visualizar_janela.geometry("{}x{}".format(largura,altura))
        #Cor de Fundo
        self.visualizar_janela.configure(background = cor_principal)
        #Nao redimensionar
        self.visualizar_janela.resizable(width = False, height = False)
        #Transparencia
        self.visualizar_janela.attributes("-alpha",0.95)
        #Icone
        self.visualizar_janela.iconbitmap(default="Icons/icon.ico")

        self.frame_opcoes = Frame(self.visualizar_janela, borderwidth = 2,width = largura-60, height = 100, bg=cor_principal,relief="raise")
        self.frame_opcoes.place(x=30, y=10)

        self.frame_list = Frame(self.visualizar_janela, borderwidth = 2,width = largura, height = altura-150, bg=cor_principal,relief="raise")
        self.frame_list.place(x=30, y=150)

        #self.sel_data = ttk.Button(self.frame_opcoes,text="Selecionar Data",command = self.Selecionar_Data).pack()
        
        dadosCols = tuple(self.banco.dados.columns)
        self.listagem_v = ttk.Treeview(self.frame_list,columns = dadosCols, show='headings', height = 20)

        self.listagem_v.bind('<Double-1>',self.Mostrar)

        self.listagem_v.column("Id", width = 25,anchor=CENTER)
        self.listagem_v.heading("Id",text="ID",anchor=CENTER)

        self.listagem_v.column("Local", width = 170,anchor=CENTER)
        self.listagem_v.heading("Local",text="Local",anchor=CENTER)

        self.listagem_v.column("Solicitante", width = 100,anchor=CENTER)
        self.listagem_v.heading("Solicitante",text="Solicitante",anchor=CENTER)

        self.listagem_v.column("Atendimento", width = 250,anchor=CENTER)
        self.listagem_v.heading("Atendimento",text="Atendimento",anchor=CENTER)

        self.listagem_v.column("Certificado", width = 150,anchor=CENTER)
        self.listagem_v.heading("Certificado",text="Certificado",anchor=CENTER)

        self.listagem_v.column("Meta", width = 70,anchor=CENTER)
        self.listagem_v.heading("Meta",text="Meta",anchor=CENTER)

        self.listagem_v.column("Resolvido", width = 70,anchor=CENTER)
        self.listagem_v.heading("Resolvido",text="Resolvido",anchor=CENTER)

        self.listagem_v.column("Data", width = 100,anchor=CENTER)
        self.listagem_v.heading("Data",text="Data",anchor=CENTER)

        #self.listagem_v.place(x=45,y=150)
        self.listagem_v.pack(side=LEFT)

        #BARRAS DE ROLAGEM DA VISUALIZACAO
        self.ysb = ttk.Scrollbar(self.frame_list, orient=VERTICAL, command=self.listagem_v.yview)
        self.listagem_v['yscroll'] = self.ysb.set
        self.ysb.pack(side = LEFT, fill = Y)

        # TEXTOS DOS CABEÇALHO
        for c in self.dadosCols:
            self.listagem_v.heading(c, text=c.title())

        # INSRINDO OS ITENS
        if self.dia == False:
            for item in self.banco.dados.values:
                self.listagem_v.insert('', 'end', values=tuple(item))
        else:
            for item in self.banco.dados.loc[self.banco.dados["Data"]==self.dia].values:
                self.listagem_v.insert('', 'end', values=tuple(item))
        
        self.visualizar_janela.mainloop()
    def Mostrar(self,event):
        try:
            #global listagem, lista_atendimentos,lista_certificados,lista_locais,lista_solicitantes
            #Pega o item selecionado
            self.nodeId_1 = self.listagem.focus()
            
            #Pega as informacoes do item
            self.id_ = self.listagem.item(self.nodeId_1)['values'][0]
            local = self.listagem.item(self.nodeId_1)['values'][1]
            solicitante = self.listagem.item(self.nodeId_1)['values'][2]
            atendimento = self.listagem.item(self.nodeId_1)['values'][3]
            certificado = self.listagem.item(self.nodeId_1)['values'][4]
            meta = self.listagem.item(self.nodeId_1)['values'][5]
            resolvido = self.listagem.item(self.nodeId_1)['values'][6]
            data = self.listagem.item(self.nodeId_1)['values'][7]
            
            #Abre a nova janela
            self.mostrar_jan = Tk()

            #CONFIGURACOES ----
            #Titulo
            self.mostrar_jan.title(titulo)
            #Tamanho da self.mostrar_janela
            self.mostrar_jan.geometry("500x450")
            #Cor de Fundo
            self.mostrar_jan.configure(background = cor_principal)
            #Nao redimensionar
            self.mostrar_jan.resizable(width = False, height = False)
            #Transparencia
            self.mostrar_jan.attributes("-alpha",0.95)
            #Icone
            self.mostrar_jan.iconbitmap(default="Icons/icon.ico")

            x_l = 40
            x_e = 200
            y_i = 30

            #Insere as labels de Informacoes
            #Local
            self.localLabel_ = Label(self.mostrar_jan,text="Local: ",font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_principal)
            self.localLabel_.place(x=x_l, y = y_i)
            self.localEntry_ = Label(self.mostrar_jan,text=local,font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_secundaria)
            self.localEntry_.place(x=x_e, y = y_i)
            #Solicitante
            self.solLabel_ = Label(self.mostrar_jan,text ="Solicitante: ",font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_principal)
            self.solLabel_.place(x=x_l, y = y_i+50)
            self.solEntry_ = Label(self.mostrar_jan,text=solicitante,font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_secundaria)
            self.solEntry_.place(x=x_e, y = y_i+50)
            #Atendimento
            self.atendLabel_ = Label(self.mostrar_jan,text="Atendiemento: ",font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_principal)
            self.atendLabel_.place(x=x_l, y = y_i+100)
            self.atendEntry_ = Label(self.mostrar_jan,text = atendimento,font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_secundaria)
            self.atendEntry_.place(x=x_e, y = y_i+100)
            #Certificado
            self.certLabel_ = Label(self.mostrar_jan,text="Certificado: ",font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_principal)
            self.certLabel_.place(x=x_l, y = y_i+150)
            self.certEntry_ = Label(self.mostrar_jan,text = certificado,font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_secundaria)
            self.certEntry_.place(x=x_e, y = y_i+150)
            #Dispositivo Meta
            self.metaLabel_ = Label(self.mostrar_jan,text="Dispositivo Meta: ",font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_principal)
            self.metaLabel_.place(x=x_l, y = y_i+200)
            self.meta_Entry_ = Label(self.mostrar_jan,text=meta,font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_secundaria)
            self.meta_Entry_.place(x=x_e, y = y_i+200)
            #Problema Resolvido
            self.resolv_Label_ = Label(self.mostrar_jan,text="Resolvido: ",font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_principal)
            self.resolv_Label_.place(x=x_l, y = y_i+250)
            self.resolv_Entry_ = Label(self.mostrar_jan,text = resolvido,font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_secundaria)
            self.resolv_Entry_.place(x=x_e, y = y_i+250)
            #Data
            self.data_Label_ = Label(self.mostrar_jan,text="Data: ",font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_principal)
            self.data_Label_.place(x=x_l, y = y_i+300)
            self.data_Entry_ = Label(self.mostrar_jan,text = data,font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_secundaria)
            self.data_Entry_.place(x=x_e, y = y_i+300)

            #Botao de excluir
            self.ex_button = Button(self.mostrar_jan,text="Excluir" , width = 20,bg=cor_principal, fg=cor_contraste,relief="raise",command=self.Excluir)
            self.ex_button.place(x=x_e-25,y = y_i+350)

            self.mostrar_jan.mainloop()
        except:
            pass
    def Sobre(self):
        messagebox.showinfo(title="SOBRE",message="Software para controle de Suporte\n2021\nMeta Certificado Digital")
    def Excluir(self):
        #Abre o banco
        #self.banco = Banco()

        #Encontra o item no banco com base na ID do item selecionado
        x = self.banco.dados.query("Id == {} ".format(self.id_))

        #Exlui o item do banco
        self.banco.dados = self.banco.dados.drop(x.index)
        self.banco.Atualiza()
        
        #Atualiza q quantidade de atendimentos
        self.qtd_atendimentos = self.banco.current 
        self.qtd['text'] = self.qtd_atendimentos

        self.qtd_h = self.banco.dados.loc[self.banco.dados["Data"] == data].count()
        self.qtd_hj['text'] = self.qtd_h[0]
        
        #Atualiza a lista
        self.listagem.delete(self.nodeId_1)
        self.listagem.pack(side=LEFT)
        
        #Salva o banco
        self.banco.Save()

        #mensagem de sucesso
        messagebox.showinfo(title="Sucesso!", message="Cadastro Removido com Sucesso!")
        #Fecha a janela
        self.mostrar_jan.destroy()
    def Inserir(self):
        txt = ""
        #LOCAL
        local = self.localEntry.get().upper()
        if local == "":
            txt += "Local Inválido!\n"
        elif local not in lista_locais :
            add_local = messagebox.askyesno(title="Aviso!", message="Esse Local Não Está Cadastrado. Deseja Cadastrá-lo?" )
            if add_local: 
                lista_locais.append(local)
                self.localEntry.set_completion_list(lista_locais)
            else:
                self.localEntry.delete(0,END)
                return 

        #SOLICITANTE
        solicitante = self.solEntry.get().upper()
        if solicitante not in lista_solicitantes:
            txt = txt + "Solicitante Inválido!\n"

        #ATENDIMENTO
        atendimento = self.atendEntry.get().upper()
        if atendimento == "":
            txt += "Atendimento Inválido!\n"
        elif atendimento not in lista_atendimentos:
            add_atend = messagebox.askyesno(title="Aviso!", message="Esse Atendimento Não Está Cadastrado. Deseja Cadastrá-lo?" )
            if add_atend: 
                lista_atendimentos.append(atendimento)
                self.atendEntry.set_completion_list(lista_atendimentos)
            else:
                self.atendEntry.delete(0,END)
        
        #TIPO DE CERTIFICADO
        certificado = self.certEntry.get().upper()
        if certificado not in lista_certificados:
            txt = txt + "Tipo de Certificado Inválido!\n"

        #DISPOSITIVO DA META
        meta = "SIM"
        if not self.chkValueMeta.get():
            meta = "NAO"

        #PROBLEMA RESOLVIDO
        resolv = "SIM"
        if not self.chkValueResol.get():
            resolv = "NAO"

        #CASO TUDO ESTEJA CORRETO
        if txt == "":
            
            #CADASTRA NO BANCO DE DADOS
            #banco = Banco()
            ultimo = self.banco.current
            x = self.banco.dados["Id"]
            if ultimo:
                self.id_ = str(int(x[ultimo-1]) + 1)
            else:
                self.id_ = str(1)
            nova_linha = [self.id_,local, solicitante, atendimento, certificado, meta, resolv, data]        
            self.banco.dados.loc[self.banco.current] = nova_linha
            self.banco.Atualiza()
            #banco.Save()

            #MOSTRA MENSAGEM DE SUCESSO
            messagebox.showinfo(title="SUCESSO!", message="Atendimento Cadastrado com Sucesso!")

            #LIMPA AS SELEÇÕES E TEXTOS
            self.localEntry.delete(0,END)
            self.solEntry.delete(0,END)
            self.atendEntry.delete(0,END)
            self.certEntry.delete(0,END)
            self.chkValueMeta.set(False)
            self.chkValueResol.set(False)
            
            #ALTERA A QUANTIDADE DE ATENDIMENTOS
            self.qtd_atendimentos = self.banco.current 
            self.qtd['text'] = self.qtd_atendimentos
            self.qtd.place(relx=0.5, rely=0.5,anchor=CENTER)

            self.qtd_h = self.banco.dados.loc[self.banco.dados["Data"] == data].count()
            self.qtd_hj['text'] = self.qtd_h[0]
            self.qtd_hj.place(relx=0.5, rely=0.5,anchor=CENTER)

            #ALTERA A LISTAGEM
            self.listagem.insert('', 'end', values=tuple(self.banco.dados.loc[self.qtd_atendimentos-1]))
            self.listagem.pack(side=LEFT)
        else:
            #CASO DE ERRADO
            messagebox.showerror(title="Impossível Cadastrar Atendimento", message= txt)

jan = Tk()

Janela(jan)


jan.geometry(str(largura)+"x"+str(altura))
#CONFIGURACOES ----
#Titulo
jan.title(titulo)
#Cor de Fundo
jan.configure(background = cor_meta)
#Nao redimensionar
jan.resizable(width = False, height = False)
#Transparencia
jan.attributes("-alpha",0.95)
#Icone
jan.iconbitmap(default="Icons/icon.ico")

jan.mainloop()  

