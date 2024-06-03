class DataHandler:
    def __init__(self):
        self.coefs_x_y = dict()

    def save_data(self, file_path='shared_data.json'):
        import json
        with open(file_path, 'w') as f:
            json.dump(self.coefs_x_y, f)

    def load_data(self, file_path='shared_data.json'):
        import json
        with open(file_path, 'r') as f:
            self.coefs_x_y = json.load(f)