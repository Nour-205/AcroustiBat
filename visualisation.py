import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import numpy as np
from scipy.interpolate import griddata
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import mysql.connector as mysql
from tkinter import *


class fenetre(tk.Tk):

    __slots__ = [
    "idSerie", "dateJour", "lieu", "coefs_x_y", "temperature", "humidite", "liste", 'scale'
  ]
    #coefxy dico : coeff x y 

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Visualisation")
        self.geometry("800x600")
        frame = tk.Frame(self)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
        self.plot_frame = tk.Frame(frame)
        self.plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
        self.configure(background="white")

        #recup donnees
        self.coefs_x_y = dict()
        self.liste = []
        self.temperature = -1
        self.humidite = -1
        bd = self.ouvrir_connexion_bd()
        self.recuperer_id_serie(bd)
        self.recuperer_donnees(bd)
        self.fermer_connexion_bd(bd)
        

        self.scale = tk.Scale(self, from_=0, to=23, orient=tk.HORIZONTAL, length = 10, width=20, activebackground='lightpink', label = 'choisir la gamme de fréquences',font = ('Helvetica', 10), command=self.update_plot)
        self.scale.bind("<ButtonRelease-1>", self.update_plot)
        self.scale.pack(side=tk.TOP, fill=tk.X)
        self.plot_type = tk.IntVar()
        self.plot_type.set(0)  # Default to 3D plot

        #style = tk.Style()
        #style.configure('TRadiobutton', foreground=[('disabled', 'grey'),('selected', 'lightpink'),('!selected', 'gray')])
        rb_3d = tk.Radiobutton(self, text="3D Plot", variable=self.plot_type, value=0, command=self.update_plot)
        rb_box = tk.Radiobutton(self, text="Box Plot", variable=self.plot_type, value=1, command=self.update_plot)
        rb_3d.pack(side=tk.LEFT, padx=10)
        rb_box.pack(side=tk.LEFT, padx=10)

        self.update_plot(None)

        label_lieu = Button(frame, text=f"Lieu : {self.lieu} \n Date : {self.dateJour} \n Temperature : {self.temperature} °C \n Humidité : {self.humidite} % " ,bg = "#f7f3e1", font = ("Helvetica", 20))
        label_lieu.pack(side="top", padx=20, pady=20, expand=True)
        # Button1 = Button(frame, text="Show 3D Plot", command=self.plot3d, width=20, height=2, bg='lightpink')
        # Button1.pack(side="left", padx=20, pady=20, expand=True)
        # Button2 = Button(frame, text="Show Box Plot", command=self.plotbox, width=20, height=2, bg="lightblue")
        # Button2.pack(side="left", padx=20, pady=20, expand=True)

    def recuperer_id_serie(self, bd):
        cursor = bd.cursor()
        nombat = input("Nom du batiment : ")
        numsalle = input("Numéro de la salle : ")
        self.lieu = nombat + " " + numsalle
        print("***********************")
        cursor.execute("SELECT s.idSerie, s.dateJour FROM SERIE s, LIEU l WHERE s.idLieu = l.idLieu and l.nomBatiment = %s and l.numeroSalle = %s", [nombat, numsalle])
        for idSerie, date in cursor:
            print(f"idSerie : {idSerie}, date : {date}")
        self.idSerie = input("Choisissez l'idSerie souhaité : ")
        cursor.execute("SELECT s.dateJour FROM SERIE s, LIEU l WHERE s.idSerie = %s and s.idLieu = l.idLieu and l.nomBatiment = %s and l.numeroSalle = %s", [self.idSerie, nombat, numsalle])
        for date in cursor:
            self.dateJour = date[0].strftime("%d/%m/%y")
        cursor.close()
    

    def recuperer_donnees(self, bd):
            cursor = bd.cursor()
            fmin = 0
            fmax = 100
            i = 0
            while fmax < 22101:
                cursor.execute("SELECT AVG(c.coefficient), m.positionx, m.positiony FROM MESURE m, COEFFICIENT c WHERE m.idMesure = c.idMesure and m.idSerie = %s and %s <= c.frequence and c.frequence <= %s GROUP BY m.positionx, m.positiony", [self.idSerie, fmin, fmax])
                liste = []
                for coef, x, y in cursor:
                    liste.append((float(coef),x,y))
                self.coefs_x_y[i] = liste
                i += 1
                fmin = fmax
                fmax += 100
            cursor.execute("SELECT AVG(temperature), AVG(humidite) FROM MESURE WHERE idSerie = %s", [self.idSerie])
            for temp, hum in cursor:
                self.temperature = round(temp, 2)
                self.humidite = round(hum, 2)
            if self.coefs_x_y != dict() and self.temperature != -1 and self.humidite != -1:
                print("***********************")
                print("Données récupérées !")
                print("***********************")
            cursor.close()

    def update_plot(self, event = None):
        val = self.scale.get()
        self.liste = self.coefs_x_y[int(val)]

        if self.plot_type.get() == 0:
            self.plot3d()
        else:
            self.plotbox()

    
    def create3dplot(self):
        liste = self.liste
        gamme = self.scale
        x_data = []
        y_data = []
        z_data = []
        for tuple in liste : 
            x = tuple[1]
            y = tuple[2]
            z = tuple[0]
            x_data.append(x)
            y_data.append(y)
            z_data.append(z)

        #creation de arrays contenant les valeurs de x, y et z
        x = np.array(x_data)
        y = np.array(y_data)
        z = np.array(z_data)

        if np.all(z == z[0]):
            z = z + np.random.normal(0, 1e-5, z.shape)
        if np.all(y == y[0]):
            y = y + np.random.normal(0, 1e-5, y.shape)
        if np.all(x == x[0]):
            x = x + np.random.normal(0, 1e-5, x.shape)

        # augmentation de nombre de points pour une meilleure visualisation (courbe continue)
        xi = np.linspace(min(x, default = 0), max(x, default=0) , 300)  
        yi = np.linspace(min(y, default = 0), max(y), 300)  
        Xi, Yi = np.meshgrid(xi, yi)

        #méthode cubique pour interpolation (courbe de surface continue) + turning Z into a 2D element 
        Zi = griddata((x, y), z, (Xi, Yi), method='cubic')

        fig = plt.figure()
        axe = fig.add_subplot(111, projection='3d')
        surface = axe.plot_surface(Xi, Yi, Zi, cmap=cm.coolwarm)
        #   visualisation des points bruts pour comparer ? (removable feature)
        axe.scatter(x, y, z, color='r', s=10, alpha = 0.5)

        fig.colorbar(surface, shrink=0.5, aspect=5)
        axe.set_xlabel("coordonnée x")
        axe.set_ylabel("coordonnée y")
        axe.set_zlabel("amplitude")
        axe.set_title("Amplitudes de la gamme de fréquences sélectionnée")
        return fig
    
    def createboxplot(self):
        gamme = self.scale
        liste = self.liste
        z_data = []
        for tuple in liste : 
            z = tuple[0]
            z_data.append(z)

        z = np.array(z_data)

        fig = plt.figure()
        fig.suptitle('boxplot de la gamme de fréquences sélectionnée')

        ax = fig.add_subplot(111)
        box = ax.boxplot(z, patch_artist = True)
        colors = ['lightblue', 'lightgreen']
        for patch, color in zip(box['boxes'], colors):
            patch.set_facecolor(color)
        ax.set_ylabel('amplitudes')
        return fig




    def ouvrir_connexion_bd(self):
     
        print("***********************")
        print("** Connexion à la BD **")
        print("***********************")
   
        connexion_bd = None
        try:
            connexion_bd = mysql.connect(
                host="fimi-bd-srv1.insa-lyon.fr",
                port=3306,
                user="G221_D", 
                password="G221_D",  
                database="G221_D_BD3" 
                )
        except Exception as e:
            if type(e) == NameError and str(e).startswith("name 'mysql'"):
                    print("[ERROR] MySQL: Driver 'mysql' not installed ? (Python Exception: " + str(e) + ")")
                    print("[ERROR] MySQL:" +
                        " Package MySQL Connector should be installed [Terminal >> pip install mysql-connector-python ]" +
                        " and imported in the script [import mysql.connector as mysql]")
            else:
                print("[ERROR] MySQL: " + str(e))
   
        if connexion_bd is not None:
            print("=> Connexion établie...")
        else:
            print("=> Connexion échouée...")
        print("***********************")
        return connexion_bd

    def fermer_connexion_bd(self, connexion_bd):
        print("Fermeture de la connexion à la BD :")
        if connexion_bd is not None:
            try:
                connexion_bd.close()
                print("=> Connexion fermée...")
            except Exception as e:
                print("[ERROR] MySQL: "+str(e))
        else:
            print("=> Pas de connexion ouverte")

    #partie visualisation 

    def plot3d(self):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        fig = self.create3dplot()
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def plotbox(self):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        fig = self.createboxplot()
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = fenetre()
app.mainloop()