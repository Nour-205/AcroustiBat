import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import data_handler  # Import the shared_data module
from data_handler import DataHandler
import tkinter as tk
from sklearn.cluster import KMeans
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ClusterWindow(DataHandler):
    def __init__(self, parent):
        DataHandler.__init__(self)  # Initialize the base class
        self.parent = parent
        self.parent.title("New Window - Visualisation")
        self.parent.geometry("800x600")

        self.plot_frame = tk.Frame(self.parent)
        self.plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)

        self.scale_clusters = {}

        self.load_data()  # Load data from file
        self.detecter_clusters_dbscan()  # Detect clusters using DBSCAN
        self.plot_clusters_2d()

    def detecter_clusters_dbscan(self):
        print("Running DBSCAN to detect clusters")
        all_data = []
        for key in self.coefs_x_y.keys():
            data = np.array(self.coefs_x_y[key])
            if data.shape[0] >= 3:  # Ensure enough data to form clusters
                all_data.append(data)
            
        if all_data:
            all_data = np.vstack(all_data)
            amplitude_data = all_data[:, 0].reshape(-1, 1)
            
            # Use amplitude (z) for clustering
            scaler = StandardScaler()
            amplitude_data_scaled = scaler.fit_transform(amplitude_data)

            kmeans = KMeans(n_clusters=8, random_state=0)
            labels = kmeans.fit_predict(amplitude_data_scaled)
            # DBSCAN with adjusted parameters
            
            
            clusters = {}
            for label, point in zip(labels, all_data):
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(point)
            self.scale_clusters = clusters
            print("Clusters formed: ", self.scale_clusters.items())  # Debug print
        else:
            print("No data to cluster")

    def plot_clusters_2d(self):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        fig, ax = plt.subplots()

        colormap = plt.get_cmap("rainbow", len(self.scale_clusters))
        colors = [colormap(i) for i in range(len(self.scale_clusters))]
        
        for cluster_label, cluster_points in self.scale_clusters.items():
            cluster_points = np.array(cluster_points)
            amplitudes = cluster_points[:, 0]
            random_x = np.random.rand(len(amplitudes)) * 100  # Random x-values for better cluster visualization
            heart_point = np.mean(amplitudes)
            sorted_indices = np.argsort(np.abs(amplitudes - heart_point))
            sorted_amplitudes = amplitudes[sorted_indices]
            num_points = len(sorted_amplitudes)
            

            random_x = np.random.rand(len(amplitudes)) * 100  # Random x-values for better cluster visualization

            # Plot all points
            plt.scatter(random_x, sorted_amplitudes, color=colors[cluster_label % len(colors)], s=10, alpha=0.5)

            # Highlight the heart point (mean amplitude)
            heart_index = np.argmin(np.abs(sorted_amplitudes - heart_point))
            plt.scatter(random_x[heart_index], sorted_amplitudes[heart_index], color=colors[cluster_label % len(colors)], s=100, edgecolor='black')
        ax.set_xlabel("Random Index")
        ax.set_yscale('log')
        ax.set_ylabel("Amplitude")
        ax.set_title("Clusters of the Selected Frequency Range")

        
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    import tkinter as tk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    root = tk.Tk()
    app = ClusterWindow(root)
    root.mainloop()
