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
    QComboBox,
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chemical Equipment Analyser (Desktop)")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.upload_btn = QPushButton("Upload CSV")
        self.status_label = QLabel("No file uploaded")

        self.setLayout(layout)
        self.token = None
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Login")

        self.latest_dataset_id = None

        self.login_btn.clicked.connect(self.login)
        self.upload_btn.clicked.connect(self.upload_csv)
        self.download_pdf_btn = QPushButton("Download PDF Report")
        self.download_pdf_btn.clicked.connect(self.download_pdf)
        self.dataset_dropdown = QComboBox()
        self.dataset_dropdown.currentIndexChanged.connect(self.on_dataset_change)
        self.datasets = []
        self.current_dataset = None
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.dataset_dropdown)
        layout.addWidget(self.upload_btn)
        layout.addWidget(self.download_pdf_btn)
        layout.addWidget(self.status_label)

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

        try:
            with open(file_path, "rb") as f:
                files = {"file": f}
                headers = {"Authorization": f"Token {self.token}"}
                response = requests.post(url, files=files, headers=headers, timeout=30)
        except requests.RequestException:
            self.server_unreachable()
            return

        if response.status_code == 201:
            self.status_label.setText("Upload successful")
            datasets = self.fetch_datasets()
            if datasets:
                latest = datasets[0]
                self.latest_dataset_id = latest["id"]
                self.refresh_datasets()
        else:
            try:
                error = response.json().get("error", "Upload failed")
            except ValueError:
                error = "Upload failed"
            self.status_label.setText(error)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Enter credentials")
            return

        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/login/",
                json={"username": username, "password": password},
                timeout=10,
            )
        except requests.RequestException:
            self.server_unreachable()
            return

        if response.status_code == 200:
            self.token = response.json()["token"]
            self.status_label.setText("Logged in")
            datasets = self.fetch_datasets()
            if datasets:
                self.latest_dataset_id = datasets[0]["id"]
                self.refresh_datasets()
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

    def server_unreachable(self):
        self.status_label.setText("Cannot reach the server")
        QMessageBox.critical(
            self,
            "Server not running",
            "Cannot reach the backend at http://127.0.0.1:8000.\n"
            "Start it with: python manage.py runserver",
        )

    def fetch_datasets(self):
        url = "http://127.0.0.1:8000/api/datasets/"
        headers = {"Authorization": f"Token {self.token}"}
        try:
            response = requests.get(url, headers=headers, timeout=10)
        except requests.RequestException:
            self.server_unreachable()
            return []
        if response.status_code == 200:
            return response.json()
        return []

    def download_pdf(self):
        if not self.token:
            QMessageBox.warning(self, "Auth required", "Please login first")
            return

        if not self.current_dataset:
            QMessageBox.warning(self, "No dataset", "Select a dataset first")
            return

        dataset_id = self.current_dataset["id"]
        url = f"http://127.0.0.1:8000/api/datasets/{dataset_id}/pdf/"
        headers = {"Authorization": f"Token {self.token}"}

        try:
            response = requests.get(url, headers=headers, stream=True, timeout=30)
        except requests.RequestException:
            self.server_unreachable()
            return

        if response.status_code == 200:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save PDF",
                f"dataset_{dataset_id}.pdf",
                "PDF Files (*.pdf)",
            )

            if file_path:
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(8192):
                        if chunk:
                            f.write(chunk)

                QMessageBox.information(self, "Success", "PDF downloaded")
        else:
            QMessageBox.critical(self, "Error", "Failed to download PDF")

    def refresh_datasets(self):
        self.datasets = self.fetch_datasets()
        self.dataset_dropdown.clear()

        for dataset in self.datasets:
            label = f"Dataset {dataset['id']} - {dataset['uploaded_at']}"
            self.dataset_dropdown.addItem(label, dataset)

        if self.datasets:
            self.dataset_dropdown.setCurrentIndex(0)
    def on_dataset_change(self, index):
        if index < 0:
            return

        dataset = self.dataset_dropdown.itemData(index)
        self.current_dataset = dataset

        self.clear_charts()
        self.show_charts(dataset)

    def clear_charts(self):
        layout = self.layout()
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, FigureCanvas):
                widget.setParent(None)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())