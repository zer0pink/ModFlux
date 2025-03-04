from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QProgressBar,
    QLabel,
)
from PySide6.QtCore import Qt, Signal, QThread
import httpx
from pathlib import Path

from modflux import utils


class DownloadWorker(QThread):
    progress = Signal(int)
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, url: str, download_path: Path):
        super().__init__()
        self.url = url
        self.download_path = download_path

    def run(self):
        try:
            with httpx.stream('GET', self.url) as response:
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                
                with open(self.download_path, 'wb') as f:
                    if total_size == 0:  # No content length header
                        for chunk in response.iter_bytes():
                            f.write(chunk)
                    else:
                        downloaded = 0
                        for chunk in response.iter_bytes(chunk_size=8192):
                            downloaded += len(chunk)
                            f.write(chunk)
                            progress = int((downloaded / total_size) * 100)
                            self.progress.emit(progress)

            self.finished.emit(str(self.download_path))
        except Exception as e:
            self.error.emit(str(e))


class DownloadDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Download Mod")
        self.setMinimumWidth(400)
        self.download_path = None
        
        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # URL input
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter mod URL...")
        url_layout.addWidget(QLabel("URL:"))
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)

        # Progress bar (hidden initially)
        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # Buttons
        button_layout = QHBoxLayout()
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.start_download)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.download_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        # Status label
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

    def start_download(self):
        """Start the download process"""
        url = self.url_input.text().strip()
        if not url:
            self.status_label.setText("Please enter a URL")
            return

        self.nexus_download = utils.nxm_process(url)

        # Setup and start download worker
        self.download_button.setEnabled(False)
        self.url_input.setEnabled(False)
        self.progress_bar.show()
        self.progress_bar.setValue(0)

        self.worker = DownloadWorker(
            self.nexus_download["download_url"],
            self.nexus_download["archive_path"],
        )
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.download_finished)
        self.worker.error.connect(self.download_error)
        self.worker.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def download_finished(self, path):
        self.download_path = path
        self.status_label.setText("Download completed!")
        self.accept()

    def download_error(self, error_msg):
        self.status_label.setText(f"Error: {error_msg}")
        self.download_button.setEnabled(True)
        self.url_input.setEnabled(True)
        self.progress_bar.hide()

    def get_nexus_download(self):
        return self.nexus_download
