from tkinter import *
from myRSA import *
import tkinter.messagebox
import time

def RSA_window():
    def RSA_PairKey_Get():
        RSA = myRSA()
        E,D,N = RSA.RSA_PairKey_Get()
        E_Text.delete('1.0', END)
        D_Text.delete('1.0',END)
        E_Text.insert(INSERT, str(E)+str(N))
        D_Text.insert(INSERT,str(D)+str(N))

    def RSA_Message_Enc():
        RSA = myRSA()
        text = Key_Text.get('1.0', END)
        M = M_Text.get('1.0', END)
        C_Text.delete('1.0', END)
        E = int(text[0:len(text)-32-1])
        N = int(text[-33:-1])
        res = RSA.Win_Message_Enc(M, E, N)
        C_Text.insert(INSERT,res)

    def RSA_Message_Dec():
        RSA = myRSA()
        text = Key_Text.get('1.0', END)
        C = C_Text.get('1.0', END)
        M_Text.delete('1.0', END)
        E = int(text[0:len(text)-32-1])
        N = int(text[-33:-1])
        res = RSA.Win_Message_Dec(C, E, N)
        M_Text.insert(INSERT,res)


    master = Tk()
    master.title("MXQX_RSA128")
    label1 = Label(master,text = 'RSA公钥')
    label1.grid(row = 0, column = 0)
    E_Text = Text(master,width = 30, height = 3)
    E_Text.grid(row = 1, column = 0)

    label1 = Label(master,text = 'RSA私钥')
    label1.grid(row = 2, column = 0)
    D_Text = Text(master,width = 30, height = 3)
    D_Text.grid(row = 3, column = 0)

    Get_Key = Button(master,text = '生成密钥对',command = lambda:RSA_PairKey_Get())
    Get_Key.grid(row=4, column=0)

    label1 = Label(master,text = '原文')
    label1.grid(row = 5, column = 0)
    M_Text = Text(master,width = 48, height = 10)
    M_Text.grid(row = 6, column = 0)

    label1 = Label(master,text = '密文')
    label1.grid(row = 7, column = 0)
    C_Text = Text(master,width = 48, height = 10)
    C_Text.grid(row = 8, column = 0)

    label1 = Label(master,text = '密钥')
    label1.grid(row = 9, column = 0)
    Key_Text = Text(master,width = 30, height = 3)
    Key_Text.grid(row = 10, column = 0)

    Enc_Dec = Frame(width=220, height=30)
    Enc = Button(Enc_Dec, text='加密', command=lambda: RSA_Message_Enc())
    Dec = Button(Enc_Dec, text='解密', command=lambda: RSA_Message_Dec())
    Enc_Dec.grid(row = 11, column = 0, columnspan = 2, padx = 1, pady = 3)
    Enc_Dec.grid_propagate(0)
    Enc.grid(row = 0,column = 1,padx = 47, pady = 0)
    Dec.grid(row = 0,column = 2,padx = 0, pady = 0)

    master.mainloop()

if __name__ == "__main__":
    RSA_window()
