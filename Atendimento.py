from Banco import Banco
from tkinter import messagebox
from datetime import date

class Atendiemento:
    def __init__(self,local ="",solicitante="",atendimento="",certificado="",meta="",resolvido="",data=""):
        self.Local = local
        self.Solicitante = solicitante
        self.Atendimento = atendimento
        self.Certificado = certificado
        self.Meta = meta
        self.Resolvido = resolvido
        self.Data = date.today().strftime("%d/%m/%Y")
    
    def Salvar(self,banco=None):
        if banco == None:
            self.Banco = Banco()
        else:
            self.Banco = banco

        txt = ""

        lista_Locais = open("Listas/Locais.txt","w")
        lista_Solicitantes = open("Listas/Solicitantes.txt","w")
        lista_Atendimentos = open("Listas/Tipo_Atendimentos.txt","w")
        lista_Certificados = open("Listas/Tipo_Certificados.txt","w")

        if self.Local != "":
            if self.Local not in lista_Locais.split("\n"):
                novo_Local = messagebox.askyesno(title="Aviso!", message="Esse Local Não Está Cadastrado. Deseja Cadastrá-lo?" )
                if novo_Local:
                    lista_Locais.write("\n"+self.Local)
                    lista_Locais.close()
                else:
                    txt += "Local\n"
        else:
             messagebox.showerror(title="Aviso!", message="Favor inserir um Local!")
             txt += "Local\n"
    
        
        if self.Solicitante not in lista_Solicitantes.split("\n"):
            messagebox.showerror(title="Aviso!", message="Esse Solicitante Não Existe!")
            txt += "Solicitante\n"
            lista_Solicitantes.close()
  
        
        if self.Atendimento != "":
            if self.Atendimento not in lista_Atendimentos.split("\n"):
                novo_Atendimento = messagebox.askyesno(title="Aviso!", message="Esse Atendimento Não Está Cadastrado. Deseja Cadastrá-lo?" )
                if novo_Atendimento:
                    lista_Atendimentos.write("\n"+self.Atendimento)
                    lista_Atendimentos.close()
                else:
                    txt += "Atendimento\n"
             
        else:
            txt += "Atendimento\n" 
        
        if self.Certificado not in lista_Certificados.split("\n"):
            messagebox.showerror(title="Aviso!", message="Esse Tipo de Certificado Não Existe!")
            lista_Certificados.close()
            txt += "Tipo de Certificado\n"


        if self.Meta:
            self.Meta = "SIM"
        else:
            self.Meta = "NAO"

        
        if self.Resolvido:
            self.Resolvido = "SIM"
        else:
            self.Resolvido = "NAO"


        if txt == "" :

            ultimo = self.Banco.current
            x = self.Banco.dados["Id"]
            if ultimo:
                self.id_ = str(int(x[ultimo-1]) + 1)
            else:
                self.id_ = str(1)
            nova_linha = [self.id_,self.Local, self.Solicitante, self.Atendimento, self.Certificado, self.Meta, self.Resolvido, self.Data]        
            self.Banco.dados.loc[self.Banco.current] = nova_linha
            self.Banco.Atualiza()

            #MOSTRA MENSAGEM DE SUCESSO
            messagebox.showinfo(title="SUCESSO!", message="Atendimento Cadastrado com Sucesso!")
        else:
            
            messagebox.showerror(title="OPS!!!", message= "Algo deu errado com :\n"+txt)





