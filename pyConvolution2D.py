



import tkFileDialog
from Tkinter import *

from PIL import Image, ImageTk
from skimage.exposure import rescale_intensity
import numpy as np

import cv2
import time

"""
    Convolucao 2D
    05/09/2018
    Autor: Diego Andre Sant'Ana
    Disciplina: Visao Computacional
    Baseado na explicação do site http://setosa.io/ev/image-kernels/
"""
class TELA:
    def preencher_matriz(self):
        #valores relativo a cada tipo de convolucao
        m_val=[
            [0.0625,0.125 ,0.0625,0.125,0.25,0.125, 0.0625,0.125 ,0.0625 ],
            [-1 ,-2 ,-1 ,0 ,0 , 0, 1,2 , 1],
            [-2 , -1 , 0 , -1 , 1 , 1,0 ,1 , 2],
            [ 0, 0, 0, 0, 1, 0,0 ,0 ,0 ],
            [ 1, 0 , -1 ,2 ,0 ,-2 ,1 ,0 ,-1 ],
            [ -1 ,-1 , -1 ,-1 ,8 , -1 ,-1 ,-1 , -1],
            [-1 ,0 ,1 ,-2 ,0 ,2 ,-1 ,0 ,1 ],
            [0 ,-1 ,0 ,-1 ,5 , -1, 0, -1,0 ],
            [1 ,2 , 1, 0, 0, 0,-1 ,-2 , -1]
            ]
        m=m_val[self.radio.get()]

        for i,v in enumerate([self.v1,self.v2,self.v3,self.v4,self.v5,self.v6,self.v7,self.v8,self.v9]):
            v.set(m[i])

    ##Inicializacao dds componentes
    def __init__(self):

        self.font10 = "-family {DejaVu Sans} -size 14 -weight normal -slant"  \
            " roman -underline 0 -overstrike 0"


        self.clicked = False
        self.fingerling = {}

        # janela
        self.window = Tk()
        self.window.title("Convolution 2D")
        self.window.attributes('-zoomed', True)

        # lado esquerdo
        self.frameMenuLateral = Frame(self.window)
        self.frameMenuLateral.pack(side=LEFT, anchor=N)
        # controles
        self.frameControls = LabelFrame(self.frameMenuLateral, text="Controls", padx=5, pady=5)
        self.frameControls.pack(anchor=N, pady=5, padx=5, fill=X)

        self.frameControlsOrganize = Frame(self.frameControls)
        self.frameControlsOrganize.pack(fill=X, expand=False)

        #Botao de selecionar a imagem
        self.selecionaImagem = Button(self.frameControlsOrganize, text="Select Image", padx=5, pady=5,
                                      command=self.selecionaImagem)
        self.selecionaImagem.pack(padx=5, pady=5, expand=True, fill=X)


        #Campo que mostra os dados do passo a passo
        self.frameLabelCon = LabelFrame(self.frameControlsOrganize, text="Matrix", padx=5, pady=5)
        self.frameLabelCon.pack(anchor=N, pady=5, padx=5, fill=X)
        self.frameInputConvolucao = Frame(self.frameLabelCon)
        self.frameInputConvolucao.pack(fill=X, expand=False)
        self.frameInputConvolucao.columnconfigure(0, weight=3)
        self.frameInputConvolucao.columnconfigure(1, weight=3)
        self.frameInputConvolucao.columnconfigure(2, weight=3)
        self.frameInputConvolucao.columnconfigure(3, weight=3)
        self.frameInputConvolucao.columnconfigure(4, weight=3)
        self.frameInputConvolucao.columnconfigure(5, weight=3)
        self.frameInputConvolucao.grid(row=0, padx=20, sticky="nsew")
        self.frameInputConvolucao.grid(row=1, padx=20, sticky="nsew")
        self.frameInputConvolucao.grid(row=2, padx=20, sticky="nsew")


        #opcoes radio de convolucao
        MODES = [

                ("Blur", 0),
                ("Bottom Sobel", 1),
                ("Emboss", 2),
                ("Identity", 3),
                ("Left Sobel", 4),
                ("OutLine", 5),
                ("Right Sobel", 6),
                ("Sharpen", 7),
                ("Top Sobel", 8),
                 ("None", -1)
        ]

        self.radio = IntVar()
        self.radio.set(-1) # initialize
        c=3
        r=0
        for text, mode in MODES:
             if(mode==-1):
                 break
             b = Radiobutton(self.frameInputConvolucao, text=text,
                                variable=self.radio, value=mode, command=self.preencher_matriz)
             b.grid(column=c,row=r, padx=10, sticky="nsew")
             r=r+1
             if(r>2):
                 c=c+1
                 r=0


        self.imagemOriginal= None

        #variaveis utilizada pelo spinbox para armazenar os dados
        self.v1=DoubleVar()
        self.v2=DoubleVar()
        self.v3=DoubleVar()
        self.v4=DoubleVar()
        self.v5=DoubleVar()
        self.v6=DoubleVar()
        self.v7=DoubleVar()
        self.v8=DoubleVar()
        self.v9=DoubleVar()

        # Vars Spin
        for v in ([self.v1,self.v2,self.v3,self.v4,self.v5,self.v6,self.v7,self.v8,self.v9]):
            v.set(1)

        # cria os spinbox
        self.spin1=self.create_spinbox(self.v1,0,0)
        self.spin2=self.create_spinbox(self.v2,1,0)
        self.spin3=self.create_spinbox(self.v3,2,0)
        self.spin4=self.create_spinbox(self.v4,0,1)
        self.spin5=self.create_spinbox(self.v5,1,1)
        self.spin6=self.create_spinbox(self.v6,2,1)
        self.spin7=self.create_spinbox(self.v7,0,2)
        self.spin8=self.create_spinbox(self.v8,1,2)
        self.spin9=self.create_spinbox(self.v9,2,2)

        #botoes para iniciar o algoritmo
        self.buttonOpen = Button(self.frameControlsOrganize, text="Run Process", padx=5, pady=5,
                                 command=self.procedimento)
        self.buttonOpen.pack(padx=5, pady=5, expand=True, fill=X)

        self.buttonStep = Button(self.frameControlsOrganize, text="Run Process Slowly", padx=5, pady=5,
                                 command=self.procedimento_devagar)
        self.buttonStep.pack(padx=5, pady=5, expand=True, fill=X)

        # lado direito

        self.frameImages = LabelFrame(self.frameControlsOrganize, text="Images", padx=2, pady=2)
        self.frameImages.pack(padx=5, pady=5, expand=True, fill=X)

        self.frameLabelPix = LabelFrame(self.frameControlsOrganize, text="Pixel by Pyxel", padx=5, pady=5)
        self.frameLabelPix.pack(padx=5, pady=5, expand=True, fill=X)

        self.labelCalc = Label(self.frameLabelPix,text="NEW PIXEL = PIXEL*V1+PIXEL*V2+PIXEL*V3+PIXEL*V4+PIXEL*V5+PIXEL*V6+PIXEL*V7+PIXEL*V8+PIXEL*V9*", padx=5, pady=5)
        self.labelCalc.pack(padx=5, pady=5, expand=True, fill=X)

        #Configura um frame com grid de 1 coluna e 3 linhas
        self.frameControlsOrganize2 = Frame(self.frameImages)
        self.frameControlsOrganize2.pack(fill=X, expand=False)
        self.frameControlsOrganize2.columnconfigure(0, weight=2)
        self.frameControlsOrganize2.columnconfigure(1, weight=2)
        self.frameControlsOrganize2.columnconfigure(2, weight=2)
        self.frameControlsOrganize2.grid(row=0, padx=10, sticky="nsew")

        # Imagem cinza
        self.frameImg1 = LabelFrame(self.frameControlsOrganize2, text="Gray", padx=1, pady=1)
        self.frameImg1['width'] = 600
        self.frameImg1['height'] = 600
        self.frameImg1.grid(column=0, row=0)


        # Imagem Convolucao 2D
        self.frameImg2 = LabelFrame(self.frameControlsOrganize2, text="Convolution 2D", padx=1, pady=1)
        self.frameImg2['width'] = 600
        self.frameImg2['height'] = 600
        self.frameImg2.grid(column=1, row=0)

        # Imagem Convolucao 2D Passo a Passo
        self.frameImg3 = LabelFrame(self.frameControlsOrganize2, text="Convolution 2D Slowly", padx=1, pady=1)
        self.frameImg3['width'] = 600
        self.frameImg3['height'] = 600
        self.frameImg3.grid(column=2, row=0)



        self.window.mainloop()

    def click(self, event):
        self.mouseXClick = event.x
        self.mouseYClick = event.y
        self.clicked = True

    def release(self, event):
        # type: (object) -> object
        self.clicked = False

    #carrega a imagem comum
    def carregaImagem(self, img, frame, op):

        labelImg = Label(frame, width=int(600 - 3), height=int(600 - 3))
        labelImg.pack(expand=True, fill=BOTH, padx=2, pady=2)
        imgResize = Image.fromarray(img).resize((600 - 8, 600 - 8), Image.ADAPTIVE)
        imgtk = ImageTk.PhotoImage(image=imgResize)
        labelImg.imgtk = imgtk
        labelImg.configure(image=imgtk)
        if (op == 1):
            self.labelImg1 = labelImg
        elif (op == 2):
            self.labelImg2 = labelImg
        elif (op == 3):
            self.labelImg3 = labelImg
    ##Carrega a imagem processada no frame
    def carregaImagemProcessada(self, img,frame ):

        for f in frame.winfo_children():
                f.destroy()


        labelImg = Label(frame, width=int(600 - 3), height=int(600 - 3))
        labelImg.pack(expand=True, fill=BOTH, padx=2, pady=2)
        imgResize = Image.fromarray(img).resize((600 - 8, 600 - 8), Image.ADAPTIVE)
        imgtk = ImageTk.PhotoImage(image=imgResize)
        labelImg.imgtk = imgtk
        labelImg.configure(image=imgtk)

    #Executa o procedimento de convolucao 2D
    def procedimento_devagar(self):
        if(self.imagemOriginal is None):
            return

        for w in (
        self.frameImg2,self.frameImg3):
            for f in w.winfo_children():
                f.destroy()
        # converte para cinza
        self.img1= cv2.cvtColor(self.imagemOriginal, cv2.COLOR_BGR2GRAY)
        self.img2 = cv2.cvtColor(self.imagemOriginal, cv2.COLOR_BGR2GRAY)
        self.img3 = cv2.cvtColor(self.imagemOriginal, cv2.COLOR_BGR2GRAY)
        #captura linhas e colunas da imagem
        rows,cols = self.img1.shape
        for r in range(rows-1):
            for c in range(cols-1):
                self.img2[r][c]=self.calcConvolucao(self.img1,r,c)

        self.carregaImagemProcessada(self.img2, self.frameImg2)
        #Atualiza o frame com a foto
        self.frameImages.update()
        for r in range(rows):

            for c in range(cols-1):
                #realiza o calculo para o novo pixel
                self.img3[r][c]=self.calcConvolucao(self.img1,r,c)
                #carrega imagem com o pixel alterado no frame 3
                self.carregaImagemProcessada(self.img3, self.frameImg3)
                #mostra o procedimento passo a passo
                self.labelCalc.configure(text="Linha: "+str(r)+"   Coluna:  "+str(c) +"   Novo Pixel:"+str(self.calcConvolucao(self.img1,r,c))+" = "
                                              +str(self.ajuste( r-1,c-1))+" * "+ str(self.v1.get())+" + "
                                              +str(self.ajuste( r-1,c ))+" * "+ str(self.v2.get())+" + "
                                              +str(self.ajuste( r-1,c+1 ))+" * "+ str(self.v3.get())+" + "
                                              +str(self.ajuste( r,c-1 ))+" * "+ str(self.v4.get())+" + "
                                              +str(self.ajuste( r,c ))+" * "+ str(self.v5.get())+" + "
                                              +str(self.ajuste( r,c+1 ))+" * "+ str(self.v6.get())+" + "
                                              +str(self.ajuste( r+1,c-1 ))+" * "+ str(self.v7.get())+" + "
                                              +str(self.ajuste( r+1,c  ))+" * "+ str(self.v8.get())+" + "
                                              +str(self.ajuste( r+1,c+1 ))+" * "+ str(self.v9.get()))

                #Atualiza o Label com o calculo
                self.labelCalc.update()
                #Atualiza o frame com a foto com o pixel alterado
                self.frameImg3.update()
                #Dorme durante um tempo
                time.sleep(0.7)

    #Executa o procedimento de convolucao 2D
    def procedimento(self):
        if(self.imagemOriginal is None):
            return

        # converte para cinza
        self.img1= cv2.cvtColor(self.imagemOriginal, cv2.COLOR_BGR2GRAY)
        self.img2 = cv2.cvtColor(self.imagemOriginal, cv2.COLOR_BGR2GRAY)
        self.img3 = cv2.cvtColor(self.imagemOriginal, cv2.COLOR_BGR2GRAY)
        for w in (
        self.frameImg2,self.frameImg3):
            for f in w.winfo_children():
                f.destroy()

        #captura linhas e colunas da imagem
        rows,cols = self.img1.shape
        for r in range(rows-1):
            for c in range(cols-1):
                self.img2[r][c]= (self.calcConvolucao(self.img1,r,c)) #realiza a convolucao de cada pixel

        self.carregaImagemProcessada(self.img2, self.frameImg2)


    #imagem original em preto e branco, linha e coluna a ser calculado o valor
    def calcConvolucao(self,val,r,c):
            #multiplicao do pixe pelo valor informado na matriz
            p1= self.ajuste((r-1),(c-1) )*self.v1.get()
            p2= self.ajuste( (r-1),c )*self.v2.get()
            p3= self.ajuste( (r-1),(c+1) )*self.v3.get()
            p4= self.ajuste( r,(c-1) )*self.v4.get()
            p5= self.ajuste( r,c )*self.v5.get()
            p6= self.ajuste( r,(c+1) )*self.v6.get()
            p7= self.ajuste( (r+1),(c-1) )*self.v7.get()
            p8= self.ajuste( (r+1),c )*self.v8.get()
            p9= self.ajuste( (r+1),(c+1) )*self.v9.get()


            sum=(p1+p2+p3+p4+p5+p6+p7+p8+p9)
            return sum

    #ajuste caso o pixel esteja na borda
    def ajuste(self,r,c):
        rows,cols = self.img1.shape
        if(r<0 or c<0 or r>rows or c>cols):
            return 0

        return self.img1[r,c]

    #cria os botoes spinbox
    def create_spinbox(self, var, col, row):

            spinbox = Spinbox(self.frameInputConvolucao, from_=-255.0, to=255.0)

            spinbox .configure(activebackground="#f9f9f9")
            spinbox.configure(background="white")
            spinbox.configure(buttonbackground="wheat")
            spinbox.configure(disabledforeground="#b8a786")
            spinbox.configure(font=self.font10)
            spinbox.configure(from_="-255.0")
            spinbox.configure(highlightbackground="black")
            spinbox.configure(selectbackground="#c4c4c4")
            spinbox.configure(textvariable=var)
            spinbox.configure(to="255.0")
            spinbox.grid(column=col, row=row)

            return spinbox

    #seleciona a imagem
    def selecionaImagem(self):
        options = {

            'title': 'Select type of image permits(JPG or PNG).',
            'filetypes': (("Image JPG", '*.jpg'), ('Image PNG', '*.png'))

        }
        filename = tkFileDialog.askopenfilename(**options)
        if (filename != ''):
            self.file = filename
            self.window.title(self.file)
            self.imagemOriginal = cv2.imread(self.file)

            for w in (
            self.frameImg1, self.frameImg2, self.frameImg3 ):
                for f in w.winfo_children():
                    f.destroy()
             # converte para cinza
            self.img1= cv2.cvtColor(self.imagemOriginal, cv2.COLOR_BGR2GRAY)
            self.img2 = cv2.cvtColor(self.imagemOriginal, cv2.COLOR_BGR2GRAY)
            self.img3 = cv2.cvtColor(self.imagemOriginal, cv2.COLOR_BGR2GRAY)
            self.carregaImagem(self.img1, self.frameImg1, 1)
            self.carregaImagem(self.img1, self.frameImg2, 2)
            self.carregaImagem(self.img1, self.frameImg3, 3)


#instancia a classe
tela = TELA()
tela.mainloop()
