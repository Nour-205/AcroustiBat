import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import numpy as np
from scipy.interpolate import griddata
from tkinter import Tk, Frame, Button
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk



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
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Visualisation")
        self.geometry("800x600")
        frame = tk.Frame(self)
        frame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
        self.plot_frame = tk.Frame(frame)
        self.plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)

        Button1 = Button(frame, text="Show 3D Plot", command=self.plot3d, width=20, height=2, bg='lightpink')
        Button1.pack(side="left", padx=20, pady=20, expand=True)
        Button2 = Button(frame, text="Show Box Plot", command=self.plotbox, width=20, height=2, bg="lightblue")
        Button2.pack(side="left", padx=20, pady=20, expand=True)

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