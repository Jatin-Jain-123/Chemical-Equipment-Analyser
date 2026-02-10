from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import requests
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chemical Equipment Visualizer (Desktop)")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.upload_btn = QPushButton("Upload CSV")
        self.status_label = QLabel("No file uploaded")

        layout.addWidget(self.upload_btn)
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        self.token = None
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Login")

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)
        
        self.latest_dataset_id = None

        self.login_btn.clicked.connect(self.login)
        self.upload_btn.clicked.connect(self.upload_csv)
        self.download_pdf_btn = QPushButton("Download PDF Report")
        layout.addWidget(self.download_pdf_btn)
        self.download_pdf_btn.clicked.connect(self.download_pdf)
    
    def upload_csv(self):
        if not self.token:
            QMessageBox.warning(self, "Auth required", "Please login first")
            return

        file_path, _ = QFileDialog.getOpenFileName(
        self, "Select CSV File", "", "CSV Files (*.csv)"
        )

        if not file_path:
            return

        self.status_label.setText("Uploading...")

        url = "http://127.0.0.1:8000/api/upload/"

        with open(file_path, "rb") as f:
            files = {"file": f}
            headers = {"Authorization": f"Token {self.token}"}
            response = requests.post(url, files=files, headers=headers)

        if response.status_code == 201:
            self.status_label.setText("Upload successful")
            datasets = self.fetch_datasets()
            if datasets:
                latest = datasets[0]
                self.latest_dataset_id = latest["id"]
                self.show_charts(latest)
        else:
            self.status_label.setText("Upload failed")

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Enter credentials")
            return

        response = requests.post(
            "http://127.0.0.1:8000/api/login/",
            json={"username": username, "password": password},
        )

        if response.status_code == 200:
            self.token = response.json()["token"]
            self.status_label.setText("Logged in")
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid credentials")

    def show_charts(self, dataset):
        figure = Figure(figsize=(8, 4))
        canvas = FigureCanvas(figure)

        ax1 = figure.add_subplot(121)
        ax2 = figure.add_subplot(122)

        summary = dataset["summary"]

        # Equipment type distribution
        types = summary["equipment_type_distribution"]
        ax1.bar(types.keys(), types.values())
        ax1.set_title("Equipment Types")

        # Averages
        ax2.bar(
            ["Flowrate", "Pressure", "Temperature"],
            [
                summary["average_flowrate"],
                summary["average_pressure"],
                summary["average_temperature"],
            ],
        )
        ax2.set_title("Average Parameters")

        self.layout().addWidget(canvas)

    def fetch_datasets(self):
        url = "http://127.0.0.1:8000/api/datasets/"
        headers = {"Authorization": f"Token {self.token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return []

    def download_pdf(self):
        if not self.token:
            QMessageBox.warning(self, "Auth required", "Please login first")
            return

        if not self.latest_dataset_id:
            QMessageBox.warning(self, "No dataset", "Upload a CSV first")
            return

        url = f"http://127.0.0.1:8000/api/datasets/{self.latest_dataset_id}/pdf/"
        headers = {"Authorization": f"Token {self.token}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save PDF",
                f"dataset_{self.latest_dataset_id}.pdf",
                "PDF Files (*.pdf)",
            )

            if file_path:
                with open(file_path, "wb") as f:
                    f.write(response.content)

                QMessageBox.information(self, "Success", "PDF downloaded")
        else:
            QMessageBox.critical(self, "Error", "Failed to download PDF")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())