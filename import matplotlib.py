import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import data_handler  # Import the shared_data module
from data_handler import DataHandler

class ClusterWindow(tk.Toplevel, DataHandler):
    def __init__(self, parent):
        super().__init__(parent)
        DataHandler.__init__(self)  # Initialize the base class
        self.title("New Window - Visualisation")
        self.geometry("800x600")

        self.plot_frame = tk.Frame(self)
        self.plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)

        self.scale_clusters = {}

        self.load_data()  # Load data from file
        self.detecter_clusters_dbscan()  # Detect clusters using DBSCAN
        self.plot3d_clusters()

    def detecter_clusters_dbscan(self):
        print("Running DBSCAN to detect clusters")
        for key in self.coefs_x_y.keys():
            print(f"Processing key: {key}")
            if not self.coefs_x_y[key]:
                continue
            data = np.array(self.coefs_x_y[key])
            if data.shape[0] < 5:  # Not enough data to form clusters
                continue
            
            # Use x, y, and amplitude for clustering
            clustering_data = data[:, :3]
            
            # Scale the clustering data
            scaler = StandardScaler()
            data_scaled = scaler.fit_transform(clustering_data)
            
            # DBSCAN with adjusted parameters
            dbscan = DBSCAN(eps=0.5, min_samples=10)
            labels = dbscan.fit_predict(data_scaled)
            
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
        
        for key in self.coefs_x_y.keys():
            scale_clusters = self.coefs_x_y[key]
            colormap = plt.get_cmap("rainbow", len(scale_clusters))
            colors = [colormap(i) for i in range(len(scale_clusters))]
            for (cluster, color) in zip(scale_clusters.values(), colors):
                x_data = [item[1] for item in cluster]
                y_data = [item[2] for item in cluster]
                z_data = [item[0] for item in cluster]
                ax.scatter(x_data, y_data, z_data, color=color, s=50, alpha=0.5)

        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
        ax.set_zlabel("Amplitude")
        ax.set_zscale("log")
        ax.set_title("Clusters of the Selected Frequency Range")
        
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClusterWindow(root)
    root.mainloop()
