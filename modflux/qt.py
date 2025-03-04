from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QTableView,
    QDialog,
    QHeaderView,
    QMenu,
    QMenuBar,
    QMessageBox,
    QInputDialog,
)
from PySide6.QtCore import Qt, QModelIndex, QPoint, QTimer, QDir
from PySide6.QtWidgets import QFileDialog
from PySide6.QtNetwork import QLocalServer, QLocalSocket
from PySide6.QtGui import QAction

import os
from pathlib import Path
from peewee import fn
import webbrowser
import logging
import sys
import sh

import modflux.config

from modflux.db import Mod, Game, Setting
from modflux import mods

from modflux.models.games import GameListModel
from modflux.models.mods import ModTableModel

from modflux.ui.download import DownloadDialog
from modflux.ui.game_settings import Ui_GameSettings
from modflux.ui.settings import Ui_Settings
from modflux.ui.games import Ui_Games
from modflux.ui.tags import TagDialog


logger = logging.getLogger("modflux")


class SettingsDialog(Ui_Settings, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        settings = Setting.select()

        for setting in settings:
            if setting.key == 'nexus_api_key':
                self.nexusAPIKeyLineEdit.setText(setting.value)

    def accept(self):
        Setting.replace(
            key="nexus_api_key", value=self.nexusAPIKeyLineEdit.text().strip()
        ).execute()
        super().accept()


class GamesDialog(Ui_Games, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.accepted.connect(self.on_accept)

        self.createGameButton.clicked.connect(self.create)

        self._gamesModel = GameListModel()

        self.gamesList.setModel(self._gamesModel)

    def create(self):
        d = GameSettingsDialog(self)

        result = d.exec()
        if result == QDialog.Accepted:
            self._gamesModel.refresh_data()

    def on_accept(self):
        self._game = self._gamesModel.get_game(self.gamesList.currentIndex().row())

    def on_double_click(self, index: QModelIndex):
        self._game = self._gamesModel.get_game(index.row())
        self.accept()

    def get_game(self) -> Game:
        return self._game


class GameSettingsDialog(Ui_GameSettings, QDialog):
    def __init__(self, parent=None, game=None):
        super().__init__(parent)
        self.setupUi(self)
        if game:
            self._game = Game.get_by_id(1)
        else:
            logger.debug("creating new game")
            self._game = Game()
            self._game.game_id = ""

        self.gameNameEdit.setPlainText(self._game.name)
        self.gameIdEdit.setPlainText(self._game.game_id)
        self.gamePathEdit.setPlainText(self._game.game_path)
        self.downloadPathEdit.setPlainText(self._game.download_path)
        self.modPathEdit.setPlainText(self._game.mod_path)

        self.workPathEdit.setPlainText(self._game.work_path)
        self.overwritePathEdit.setPlainText(self._game.overwrite_path)

        self.accepted.connect(self.on_accept)

        self.gamePathBrowse.clicked.connect(self.selectDirectory)

    def on_accept(self):
        self._game.name = self.gameNameEdit.toPlainText()
        self._game.game_id = self.gameIdEdit.toPlainText()
        self._game.game_path = self.gamePathEdit.toPlainText()
        self._game.download_path = self.downloadPathEdit.toPlainText()
        self._game.mod_path = self.modPathEdit.toPlainText()
        self._game.overwrite_path = self.overwritePathEdit.toPlainText()
        self._game.work_path = self.workPathEdit.toPlainText()

        self._game.save()

        self.close()

        return True

    def selectDirectory(self):
        path = QFileDialog.getExistingDirectory(
            self, "Select directory", QDir.currentPath()
        )

        if self.sender().objectName() == "gamePathBrowse":
            self.gamePathEdit.setPlainText(path)
        elif self.sender().objectName() == "downloadPathBrowse":
            self.downloadPathEdit.setPlainText(path)
        elif self.sender().objectName() == "modPathBrowse":
            self.modPathEdit.setPlainText(path)
        elif self.sender().objectName() == "workPathBrowse":
            self.workPathEdit.setPlainText(path)
        elif self.sender().objectName() == "overwritePathBrowse":
            self.workPathEdit.setPlainText(path)
        else:
            logger.error(self.sender().objectName())

    def get_game(self) -> Game:
        return self._game


class MainWindow(QMainWindow):
    def __init__(self, nxm_url=None):
        super().__init__()
        self.setWindowTitle("ModFlux")
        self.setMinimumSize(800, 600)

        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Menu bar
        action_exit = QAction("Exit")
        action_exit.triggered.connect(self.quit)

        menu_bar = QMenuBar()
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(action_exit)
        menu_bar.addMenu("&About")

        self.setMenuBar(menu_bar)

        # Create table view and model
        self.table_view = QTableView()
        self.table_model = ModTableModel()
        self.table_view.setModel(self.table_model)

        # Adjust table properties
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table_view.setColumnWidth(0, 400)
        self.table_view.setColumnWidth(4, 50)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.setSelectionMode(QTableView.SingleSelection)
        self.table_view.setEditTriggers(QTableView.DoubleClicked)

        main_layout.addWidget(self.table_view, stretch=80)

        # Create button container and layout
        button_container = QWidget()
        button_layout = QVBoxLayout()
        button_container.setLayout(button_layout)

        activation_text = "Deactivate" if mods.is_active() else "Activate"
        self.button_activation = QPushButton(activation_text)
        self.button_download = QPushButton("Download")
        self.button_import = QPushButton("Import")
        self.button_profile = QPushButton("Profile")
        self.button_settings = QPushButton("Settings")
        self.button_quit = QPushButton("Quit")

        self.button_quit.clicked.connect(self.quit)
        self.button_activation.clicked.connect(self.activate)
        self.button_download.clicked.connect(self.download)
        self.button_import.clicked.connect(self.import_mod)
        self.button_profile.clicked.connect(self.profile)
        self.button_settings.clicked.connect(self.settings)

        button_layout.addWidget(self.button_activation)
        button_layout.addWidget(self.button_download)
        button_layout.addWidget(self.button_import)
        button_layout.addWidget(self.button_settings)
        button_layout.addWidget(self.button_profile)
        button_layout.addWidget(self.button_quit)

        # Add stretch to push buttons to the top
        button_layout.addStretch()

        # Add button container to main layout
        main_layout.addWidget(button_container, stretch=30)

        # Setup context menu
        self.table_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_view.customContextMenuRequested.connect(self.show_context_menu)

        # Connect double click handler
        self.table_view.doubleClicked.connect(self.handle_double_click)

        # Setup local server for single instance communication
        self.server = QLocalServer(self)
        self.server.newConnection.connect(self.handle_new_connection)

        # Try to start server - if it fails, another instance exists
        if not self.server.listen("modflux_instance"):
            logger.error("Server already running, this shouldn't happen")
            exit(10)

        # Handle nxm URL if provided
        if nxm_url:
            self.handle_nxm_url(nxm_url)

    def settings(self):
        settings = SettingsDialog(self)
        settings.show()

    def profile(self):
        dialog = GameSettingsDialog(self)
        dialog.exec()

    def refresh_table_data(self):
        """Refresh the table model with latest data from database"""
        self.table_model.refresh_data()

    def activate(self):
        if mods.is_active():
            if mods.unmount():
                self.button_activation.setText("Activate")
            else:
                QMessageBox.critical(
                    self,
                    "Failed to unmount",
                    "There was a problem unmounting the game directory",
                )
        else:
            if mods.mount():
                self.button_activation.setText("Deactivate")
            else:
                QMessageBox.critical(
                    self,
                    "Failed to mount",
                    "There was a problem mounting the game directory",
                )

    def import_mod(self):
        """
        Open a file picker and import the selected mod archive.
        Returns the imported Mod object if successful, None otherwise.
        """
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Mod Archive",
            str(Path.home()),
            "Archive Files (*.zip *.rar *.7z);;All Files (*.*)",
        )

        if not file_name:
            return None

        try:
            mod = mods.import_mod(file_name)
            self.table_model.add_mod(mod)

        except Exception as e:
            # You might want to show an error dialog here
            print(f"Error importing mod: {e}")
            return None

    def download(self):
        dialog = DownloadDialog(self)
        if dialog.exec() == QDialog.Accepted:
            nexus_download = dialog.get_nexus_download()
            if nexus_download:
                mod = mods.process_download(nexus_download)
                self.table_model.add_mod(mod)

    def quit(self):
        reply = QMessageBox.question(
            self,
            "Quit",
            "Are you sure you want to quit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            exit(0)

    def show_context_menu(self, position: QPoint):
        index = self.table_view.indexAt(position)
        if not index.isValid():
            return

        mod = self.table_model.get_mod(index.row())
        menu = QMenu(self)

        # Add load order submenu
        load_order_menu = menu.addMenu("Load Order")
        move_to_start = load_order_menu.addAction("Move to Start")
        move_to_end = load_order_menu.addAction("Move to End")
        edit_load_order = load_order_menu.addAction("Edit Load Order...")

        # Add existing actions
        browse_path = menu.addAction("Browse")

        if mod.nexus_mod_id:
            visit_nexus = menu.addAction("Visit on Nexus")
        toggle_action = menu.addAction("Disable" if mod.active else "Enable")
        delete_action = menu.addAction("Delete")
        edit_tags = menu.addAction("Edit Tags")

        action = menu.exec(self.table_view.viewport().mapToGlobal(position))

        if not action:
            return

        if action == move_to_start:
            self.move_mod_to_position(index.row(), 0)
        elif action == move_to_end:
            self.move_mod_to_position(index.row(), len(self.table_model._data) - 1)
        elif action == edit_load_order:
            self.edit_load_order(mod, index.row())
        elif action == delete_action:
            self.delete_mod(index.row())
        elif action == toggle_action:
            self.toggle_mod(index.row())
        elif mod.nexus_mod_id and action == visit_nexus:
            self.visit_nexus(mod)
        elif action == edit_tags:
            self.edit_tags(mod)
        elif action == browse_path:
            self.browse_mod(mod)

    def browse_mod(self, mod: Mod):
        sh.xdg_open(
            os.path.join(modflux.config.MANAGED_MOD_DIR, mod.version.path), _bg=True
        )

    def move_mod_to_position(self, from_index: int, to_index: int):
        """Move a mod to a new position in the load order"""
        self.table_model.move_mod_to_position(from_index, to_index)

    def edit_load_order(self, mod: Mod, current_row: int):
        """Show dialog to manually edit load order"""
        max_order = len(self.table_model._data) - 1
        new_position, ok = QInputDialog.getInt(
            self,
            "Edit Load Order",
            f"Enter new position (0-{max_order}):",
            current_row,
            0,
            max_order,
        )

        if ok and new_position != current_row:
            self.move_mod_to_position(current_row, new_position)

    def delete_mod(self, row: int):
        mod = self.table_model.get_mod(row)

        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete {mod.name}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            # Delete from database
            mod.delete_instance()
            mod.version.delete_instance()

            # TODO Delete from file system?

            # Remove from model
            self.table_model.remove_mod(row)

    def toggle_mod(self, row: int):
        self.table_model.toggle_active(row)

    def visit_nexus(self, mod: Mod):
        url = f"https://www.nexusmods.com/{mod.game.game_id}/mods/{mod.nexus_mod_id}"
        webbrowser.open(url)

    def edit_tags(self, mod: Mod):
        dialog = TagDialog(mod, self)
        if dialog.exec() == QDialog.Accepted:
            # Get new tags and update mod
            new_tags = dialog.get_tags()
            mod.tags = ",".join(sorted(new_tags))
            mod.save()

            # Update the model
            # Find the mod's index
            for i, m in enumerate(self.table_model._data):
                if m.id == mod.id:
                    self.table_model.update_mod(i, mod)
                    break

    def handle_double_click(self, index: QModelIndex):
        if index.column() == 5:  # Tags column
            mod = self.table_model.get_mod(index.row())
            self.edit_tags(mod)

    # TODO This nxm handling stuff seems janky at best and I should probably
    # skim through it a bit to clean it up
    def handle_nxm_url(self, url: str):
        """Handle an NXM URL by initiating download"""
        if url.startswith("nxm://"):
            dialog = DownloadDialog(self)
            dialog.url_input.setText(url)
            dialog.show()
            # Use QTimer to start download after dialog is shown
            QTimer.singleShot(0, dialog.start_download)
            if dialog.exec() == QDialog.Accepted:
                nexus_download = dialog.get_nexus_download()
                if nexus_download:
                    mod = mods.process_download(nexus_download)
                    self.table_model.add_mod(mod)

    def handle_new_connection(self):
        """Handle connection from new instance"""
        socket = self.server.nextPendingConnection()
        socket.waitForReadyRead(1000)

        # Read the URL from the socket
        data = socket.readAll().data().decode()
        if data.startswith("nxm://"):
            self.handle_nxm_url(data)

        # Bring window to front
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.activateWindow()
        self.raise_()


def is_instance_running():
    """Check if another instance is running by trying to connect to its server"""
    socket = QLocalSocket()
    socket.connectToServer("modflux_instance")
    return socket.waitForConnected(1000)


def send_url_to_running_instance(url: str) -> bool:
    """Send URL to running instance"""
    socket = QLocalSocket()
    socket.connectToServer("modflux_instance")
    if socket.waitForConnected(1000):
        socket.write(url.encode())
        socket.waitForBytesWritten(1000)
        socket.disconnectFromServer()
        return True
    return False


def app_main():
    logging.basicConfig(level=logging.DEBUG)

    app = QApplication(sys.argv)

    # Check for nxm URL in arguments
    nxm_url = None
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.startswith("nxm://"):
            nxm_url = arg

            # If there's already an instance running, send URL to it and exit
            if is_instance_running():
                if send_url_to_running_instance(nxm_url):
                    return 0
                else:
                    print("Failed to send URL to running instance")

    # No instance running or no URL to send, start normally

    # TODO Default profile
    selectGame = GamesDialog()
    if selectGame.exec() == QDialog.Accepted:
        game = selectGame.get_game()
        logging.info(f"loading profile {game.name}")
        modflux.config.initialize(game)

        window = MainWindow(nxm_url)
        window.show()
    else:
        exit(0)

    return app.exec()


if __name__ == "__main__":
    sys.exit(app_main())
