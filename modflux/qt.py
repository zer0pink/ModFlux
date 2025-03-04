from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog,
    QMenu,
    QMessageBox,
    QInputDialog,
)
from PySide6.QtCore import Qt, QModelIndex, QPoint, QTimer, QDir
from PySide6.QtWidgets import QFileDialog
from PySide6.QtNetwork import QLocalServer, QLocalSocket

import os
from pathlib import Path
import webbrowser
import logging
import sys
import sh

import modflux.config

from modflux.db import Mod, Game, Setting
from modflux import mods
from modflux import config

from modflux.models.games import GameListModel
from modflux.models.mods import ModTableModel, ModTableFilterModel

from modflux.ui.game_settings import Ui_GameSettings
from modflux.ui.settings import Ui_Settings
from modflux.ui.games import Ui_Games
from modflux.ui.main import Ui_MainWindow

# Bless me father for I have sinned.. These are AI generated
from modflux.ui.tags import TagDialog
from modflux.ui.download import DownloadDialog


logger = logging.getLogger("modflux")


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self, parent=None, nxm_url=None):
        super().__init__(parent)
        self.setupUi(self)

        # Setup table model data
        self._tableModel = ModTableModel()
        self._proxyModel = ModTableFilterModel()

        self._proxyModel.setSourceModel(self._tableModel)
        self.tableMods.setModel(self._proxyModel)

        # Tweak the table layout
        self.tableMods.setColumnWidth(0, 400)
        self.tableMods.setColumnWidth(4, 50)

        # Setup local server for single instance communication
        self.server = QLocalServer(self)
        self.server.newConnection.connect(self.handleNewConnection)

        # Check to see if its a mount
        if mods.is_active():
            self.buttonActivate.setText("Deactivate")

        # Try to start server - if it fails, another instance exists
        if not self.server.listen("modflux_instance"):
            logger.error("Server already running, this shouldn't happen")
            exit(10)

        # Handle nxm URL if provided
        if nxm_url:
            self.handleNxmUrl(nxm_url)

    def handleMount(self):
        if mods.is_active():
            if mods.unmount():
                self.buttonActivate.setText("Activate")
            else:
                QMessageBox.critical(
                    self,
                    "Failed to unmount",
                    "There was a problem unmounting the game directory",
                )
        else:
            if mods.mount():
                self.buttonActivate.setText("Deactivate")
            else:
                QMessageBox.critical(
                    self,
                    "Failed to mount",
                    "There was a problem mounting the game directory",
                )

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

    def download(self):
        dialog = DownloadDialog(self)
        if dialog.exec() == QDialog.Accepted:
            nexusDownload = dialog.getNexusDownload()
            if nexusDownload:
                mod = mods.process_download(nexusDownload)
                self._tableModel.addMod(mod)

    def importMod(self):
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
            self._tableModel.addMod(mod)

        except Exception as e:
            logger.error(e)

            QMessageBox.critical(self, "Problem Importing", "Could not import mod!")
            return None

    def settings(self):
        settings = SettingsDialog(self)
        settings.show()

    def game(self):
        dialog = GameSettingsDialog(self, config.GAME)
        dialog.exec()

    def refreshTableData(self):
        """Refresh the table model with latest data from database"""
        self._tableModel.refreshData()

    def updateModListFilter(self, string: str):
        self._proxyModel.setFilterRegularExpression(string)
        pass

    def contextMenu(self, position: QPoint):
        tableIndex = self.tableMods.indexAt(position)
        if not tableIndex.isValid():
            return

        # Map from proxy index
        index = self._proxyModel.mapToSource(tableIndex)
        
        mod = self._tableModel.getMod(index.row())
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

        action = menu.exec(self.tableMods.viewport().mapToGlobal(position))

        if not action:
            return

        if action == move_to_start:
            self.moveModToPosition(index.row(), 0)
        elif action == move_to_end:
            self.moveModToPosition(index.row(), len(self._tableModel._data) - 1)
        elif action == edit_load_order:
            self.editLoadOrder(mod, index.row())
        elif action == delete_action:
            self.deleteMod(index.row())
        elif action == toggle_action:
            # TODO Clean this up
            selectedIndexes = self.tableMods.selectionModel().selectedIndexes()
            logger.debug(selectedIndexes)
            if selectedIndexes and len(selectedIndexes) > 1:
                logger.debug("Got multiple mods selected")

                for selected in selectedIndexes:
                    index = self._proxyModel.mapToSource(selected)
                    self.toggleMod(index.row())
            else:
                self.toggleMod(index.row())
        elif mod.nexus_mod_id and action == visit_nexus:
            self.visitModOnNexus(mod)
        elif action == edit_tags:
            self.editTags(mod)
        elif action == browse_path:
            self.browseMod(mod)

    def browseMod(self, mod: Mod):
        sh.xdg_open(
            os.path.join(modflux.config.MANAGED_MOD_DIR, mod.version.path), _bg=True
        )

    def moveModToPosition(self, from_index: int, to_index: int):
        """Move a mod to a new position in the load order"""
        self._tableModel.moveModToPosition(from_index, to_index)

    def editLoadOrder(self, mod: Mod, currentRow: int):
        """Show dialog to manually edit load order"""
        max_order = len(self._tableModel._data) - 1
        newPosition, ok = QInputDialog.getInt(
            self,
            "Edit Load Order",
            f"Enter new position (0-{max_order}):",
            currentRow,
            0,
            max_order,
        )

        if ok and newPosition != currentRow:
            self.moveModToPosition(currentRow, newPosition)

    def deleteMod(self, row: int):
        mod = self._tableModel.getMod(row)

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
            self._tableModel.removeMod(row)

    def toggleMod(self, row: int):
        self._tableModel.toggleActive(row)

    def visitModOnNexus(self, mod: Mod):
        url = f"https://www.nexusmods.com/{mod.game.game_id}/mods/{mod.nexus_mod_id}"
        webbrowser.open(url)

    def editTags(self, mod: Mod):
        dialog = TagDialog(mod, self)
        if dialog.exec() == QDialog.Accepted:
            # Get new tags and update mod
            newTags = dialog.get_tags()
            mod.tags = ",".join(sorted(newTags))
            mod.save()

            # Update the model
            # Find the mod's index
            for i, m in enumerate(self._tableModel._data):
                if m.id == mod.id:
                    self._tableModel.updateMod(i, mod)
                    break

    def handleTableDoubleClick(self, tableIndex: QModelIndex):
        index = self._proxyModel.mapToSource(tableIndex)
        if index.column() == 5:  # Tags column
            mod = self._tableModel.getMod(index.row())
            self.editTags(mod)

    # TODO This nxm handling stuff seems janky at best and I should probably
    # skim through it a bit to clean it up
    def handleNxmUrl(self, url: str):
        """Handle an NXM URL by initiating download"""
        if url.startswith("nxm://"):
            dialog = DownloadDialog(self)
            dialog.url_input.setText(url)
            dialog.show()
            # Use QTimer to start download after dialog is shown
            QTimer.singleShot(0, dialog.start_download)
            if dialog.exec() == QDialog.Accepted:
                nexus_download = dialog.getNexusDownload()
                if nexus_download:
                    mod = mods.process_download(nexus_download)
                    self._tableModel.addMod(mod)

    def handleNewConnection(self):
        """Handle connection from new instance"""
        socket = self.server.nextPendingConnection()
        socket.waitForReadyRead(1000)

        # Read the URL from the socket
        data = socket.readAll().data().decode()
        if data.startswith("nxm://"):
            self.handleNxmUrl(data)

        # Bring window to front
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.activateWindow()
        self.raise_()


class SettingsDialog(Ui_Settings, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        settings = Setting.select()

        for setting in settings:
            if setting.key == "nexus_api_key":
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

        self.createGameButton.clicked.connect(self.create)

        self._gamesModel = GameListModel()

        self.gamesList.setModel(self._gamesModel)

    def create(self):
        d = GameSettingsDialog(self)

        result = d.exec()
        if result == QDialog.Accepted:
            self._gamesModel.refreshData()

    def accept(self):
        self._game = self._gamesModel.getGame(self.gamesList.currentIndex().row())

        super().accept()

    def on_double_click(self, index: QModelIndex):
        self._game = self._gamesModel.getGame(index.row())
        self.accept()

    def getGame(self) -> Game:
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

        self.gamePathBrowse.clicked.connect(self.selectDirectory)

    def accept(self):
        self._game.name = self.gameNameEdit.toPlainText()
        self._game.game_id = self.gameIdEdit.toPlainText()
        self._game.game_path = self.gamePathEdit.toPlainText()
        self._game.download_path = self.downloadPathEdit.toPlainText()
        self._game.mod_path = self.modPathEdit.toPlainText()
        self._game.overwrite_path = self.overwritePathEdit.toPlainText()
        self._game.work_path = self.workPathEdit.toPlainText()

        self._game.save()

        self.close()

        super().accept()

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

    def getGame(self) -> Game:
        return self._game


def isInstanceRunning():
    """Check if another instance is running by trying to connect to its server"""
    socket = QLocalSocket()
    socket.connectToServer("modflux_instance")
    return socket.waitForConnected(1000)


def sendURLtoRunningInstance(url: str) -> bool:
    """Send URL to running instance"""
    socket = QLocalSocket()
    socket.connectToServer("modflux_instance")
    if socket.waitForConnected(1000):
        socket.write(url.encode())
        socket.waitForBytesWritten(1000)
        socket.disconnectFromServer()
        return True
    return False


def appMain():
    logging.basicConfig(level=logging.DEBUG)

    app = QApplication(sys.argv)

    # Check for nxm URL in arguments
    nxmUrl = None
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.startswith("nxm://"):
            nxmUrl = arg

            # If there's already an instance running, send URL to it and exit
            if isInstanceRunning():
                if sendURLtoRunningInstance(nxmUrl):
                    return 0
                else:
                    print("Failed to send URL to running instance")

    # TODO Allow setting a default game
    selectGame = GamesDialog()
    if selectGame.exec() == QDialog.Accepted:
        game = selectGame.getGame()
        logging.info(f"loading profile {game.name}")
        modflux.config.initialize(game)

        window = MainWindow(nxmUrl)
        window.show()
    else:
        exit(0)

    return app.exec()


if __name__ == "__main__":
    sys.exit(appMain())
