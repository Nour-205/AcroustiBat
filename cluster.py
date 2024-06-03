import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import numpy as np
from scipy.interpolate import griddata
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import mysql.connector as mysql
from tkinter import *
from sklearn.preprocessing import StandardScaler
from statistics import mean as avg
from sklearn.cluster import DBSCAN
import data_handler  # Import the shared_data module
from data_handler import DataHandler
import pandas as pd



class ClusterWindow(tk.Toplevel, DataHandler):
    def __init__(self, parent):
        super().__init__(parent)
        DataHandler.__init__(self)  # Initialize the base class
        self.title("New Window - Visualisation")
        self.geometry("800x600")

        self.plot_frame = tk.Frame(self)
        self.plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)

        self.scale = 1

        self.load_data()  # Load data from file
        self.detecter_clusters_dbscan()  # Detect clusters using DBSCAN

        self.plot3d_clusters()
        self.plot3d()


    def detecter_clusters_dbscan(self):
        print("Running DBSCAN to detect clusters")
        for key in self.coefs_x_y.keys():
            print(f"Processing key: {key}")
            if not self.coefs_x_y[key]:
                continue
            data = np.array(self.coefs_x_y[key])
            if data.shape[0] < 5:  # Not enough data to form clusters
                continue
            dbscan = DBSCAN(eps=0.5, min_samples=5)
            labels = dbscan.fit_predict(data[:, :2])  # Use only x and y for clustering
            clusters = {}
            for label, point in zip(labels, data):
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(point)
            self.coefs_x_y[key] = clusters
        print(f"Completed DBSCAN, coefs_x_y keys: {self.coefs_x_y.keys()}")

    def plot3d_clusters(self):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        for self.scale in self.coefs_x_y.keys():
            colors = plt.cm.rainbow(np.linspace(0, 1, len(self.coefs_x_y[str(self.scale)])))

            for (cluster, color) in zip(self.coefs_x_y[str(self.scale)].values(), colors):
                x_data = [item[1] for item in cluster]
                y_data = [item[2] for item in cluster]
                z_data = [item[0] for item in cluster]
                ax.scatter(x_data, y_data, z_data, color=color, s=10, alpha=0.5)

        ax.set_xlabel("coordonnée x")
        ax.set_ylabel("coordonnée y")
        ax.set_zlabel("amplitude")
        ax.set_title("Clusters de la gamme de fréquences sélectionnée")
        
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def plot3d(self):
        self.plot3d_clusters()































    # def detecter_clusters_dbscan(self):
    #     for key in self.coefs_x_y.keys():
    #         if not self.coefs_x_y[key]:
    #             continue
    #         data = np.array(self.coefs_x_y[key])
    #         if data.shape[0] < 5:  # Not enough data to form clusters
    #             continue
    #         dbscan = DBSCAN(eps=0.5, min_samples=5)
    #         labels = dbscan.fit_predict(data[:, :2])  # Use only x and y for clustering
    #         clusters = {}
    #         for label, point in zip(labels, data):
    #             if label not in clusters:
    #                 clusters[label] = []
    #             clusters[label].append(point)
    #         self.coefs_x_y[key] = clusters

    # def plot_clusters(self):
    #     if not self.coefs_x_y:
    #         print("No data to plot.")
    #         return
    #     for widget in self.plot_frame.winfo_children():
    #         widget.destroy()
    #     fig = plt.figure()
    #     ax = fig.add_subplot(111, projection='3d')

    #     # Assuming we are using the first frequency band for demonstration
    #     frequency_band = 0

    #     colors = plt.cm.rainbow(np.linspace(0, 1, len(self.coefs_x_y[frequency_band])))

    #     for (cluster, color) in zip(self.coefs_x_y[frequency_band].values(), colors):
    #         x_data = [item[1] for item in cluster]
    #         y_data = [item[2] for item in cluster]
    #         z_data = [item[0] for item in cluster]
    #         ax.scatter(x_data, y_data, z_data, color=color, s=10, alpha=0.5)

    #     ax.set_xlabel("coordonnée x")
    #     ax.set_ylabel("coordonnée y")
    #     ax.set_zlabel("amplitude")
    #     ax.set_title("Clusters de la gamme de fréquences sélectionnée")

    #     canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
    #     canvas.draw()
    #     canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = ClusterWindow(root)
    root.mainloop()