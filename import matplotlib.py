import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import numpy as np
from scipy.interpolate import griddata
from tkinter import Tk, Frame, Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import mysql.connector as mysql



#visualisation
# graphe des coordonnées x et y des points en fonction de la fréquence 

#on reçoit une liste de tuples (coeff, x, y):

#test: 
liste = [(100,1,5), (0,0,1), (4,5,10), (130, 3, 9), (200, 0, 0), (400, 1, 0), (600, 0, 1), (760, 1, 1), (100,2,1),(480,2,2),(808,1,8) ,(100, 1, 5), (0, 0, 1), (4, 5, 10), (130, 3, 9), (200, 0, 0), (400, 1, 0), (600, 0, 1), (760, 1, 1), (100, 2, 1), (480, 2, 2), (808, 1, 8), (100, 1, 5), (0, 0, 1), (4, 5, 10), (130, 3, 9), (200, 0, 0), (400, 1, 0), (600, 0, 1), (760, 1, 1), (100, 2, 1), (480, 2, 2), (808, 1, 8), (100, 1, 5), (0, 0, 1), (4, 5, 10), (130, 3, 9), (200, 0, 0), (400, 1, 0), (600, 0, 1), (760, 1, 1), (100, 2, 1), (480, 2, 2), (808, 1, 8), (100, 1, 5), (0, 0, 1), (4, 5, 10), (130, 3, 9), (200, 0, 0), (400, 1, 0), (600, 0, 1), (760, 1, 1), (100, 2, 1), (480, 2, 2), (808, 1, 8), (100, 1, 5), (0, 0, 1), (4, 5, 10), (130, 3, 9), (200, 0, 0), (400, 1, 0), (600, 0, 1), (760, 1, 1), (100, 2, 1), (480, 2, 2), (808, 1, 8), (100,3, 1)]


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


# augmentation de nombre de points pour une meilleure visualisation (courbe continue)
xi = np.linspace(min(x), max(x), 500)  
yi = np.linspace(min(y), max(y), 500)  
Xi, Yi = np.meshgrid(xi, yi)

#méthode cubique pour interpolation (courbe de surface continue) + turning Z into a 2D element 
Zi = griddata((x, y), z, (Xi, Yi), method='cubic')

def create3dplot():

    fig = plt.figure()
    axe = fig.add_subplot(111, projection='3d')
    surface = axe.plot_surface(Xi, Yi, Zi, cmap=cm.coolwarm)
    #visualisation des points bruts pour comparer ? (removable feature)
    axe.scatter(x, y, z, color='r', s=10, alpha = 0.5)

    fig.colorbar(surface, shrink=0.5, aspect=5)
    axe.set_xlabel("coordonnée x")
    axe.set_ylabel("coordonnée y")
    axe.set_zlabel("amplitude")
    axe.set_title("Title of the Third Ax")
    return fig


def createboxplot():
    
    fig = plt.figure()
    fig.suptitle('boxplot de la gamme de fréquences', fontsize=14, fontweight='bold')

    ax = fig.add_subplot(111)
    c = 'blue'
    box = ax.boxplot(z, patch_artist = True)
    colors = ['lightblue', 'lightgreen']
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    ax.set_ylabel('amplitudes')
    return fig

class fenetre(tk.Tk):

    __slots__ = [
    "idSerie", "dateJour", "lieu", "coefs_x_y", "temperature", "humidite"
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
        self.temperature = -1
        self.humidite = -1
        bd = self.ouvrir_connexion_bd()
        self.recuperer_id_serie(bd)
        self.recuperer_donnees(bd)
        self.fermer_connexion_bd(bd)




        Button1 = Button(frame, text="Show 3D Plot", command=self.plot3d, width=20, height=2, bg='lightpink')
        Button1.pack(side="left", padx=20, pady=20, expand=True)
        Button2 = Button(frame, text="Show Box Plot", command=self.plotbox, width=20, height=2, bg="lightblue")
        Button2.pack(side="left", padx=20, pady=20, expand=True)


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
                self.temperature = temp
                self.humidite = hum
            if self.coefs_x_y != dict() and self.temperature != -1 and self.humidite != -1:
                print("***********************")
                print("Données récupérées !")
                print("***********************")
            cursor.close()

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


    def plot3d(self):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        fig = create3dplot()
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def plotbox(self):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        fig = createboxplot()
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


app = fenetre()
app.mainloop()