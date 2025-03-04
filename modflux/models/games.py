from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from typing import List

from modflux.db import Game

class GameListModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self._data = list(Game.select())


    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._data)

    def columnCount(self, parent=QModelIndex()) -> int:
        return 1

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole or role == Qt.EditRole:
            row_data = self._data[index.row()]

            return str(row_data.name)

    def refreshData(self):
        """Refresh all data in the model"""
        self.beginResetModel()
        self._data = list(Game.select())
        self.endResetModel()


    def getGame(self, row: int) -> Game:
        return self._data[row]