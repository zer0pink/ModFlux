from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QSortFilterProxyModel
from typing import List

from modflux import mods
from modflux.db import Mod, ModVersion, Game


class ModTableFilterModel(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()

    def filterAcceptsRow(self, source_row, source_parent):
        # Get the index for the column we want to filter on
        nameIndex = self.sourceModel().index(source_row, 0, source_parent)
        tagsIndex = self.sourceModel().index(source_row, 5, source_parent)

        # Get the data for that cell
        nameData = self.sourceModel().data(nameIndex, Qt.DisplayRole)
        tagData = self.sourceModel().data(tagsIndex, Qt.DisplayRole)

        # Check if it matches our filter pattern
        pattern = self.filterRegularExpression().pattern().casefold()
        if not pattern:
            return True

        return pattern in str(nameData).casefold() or pattern in str(tagData).casefold()

class ModTableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self._data = mods.get_game_mods()

        self._headers = [
            "Name",
            "Load Order",
            "Version",
            "Latest Version",
            "Active",
            "Tags",
        ]
        self._columns = [
            "name",
            "load_order",
            "version",
            "latest_version",
            "active",
            "tags",
        ]

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._data)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self._columns)

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole or role == Qt.EditRole:
            rowData = self._data[index.row()]

            if index.column() == 0:
                return str(rowData.name)
            if index.column() == 1:
                return str(rowData.load_order)
            elif index.column() == 2:
                return str(rowData.version.version)
            elif index.column() == 3:
                return str(rowData.latest_version)
            elif index.column() == 4:
                return bool(rowData.active)
            elif index.column() == 5:
                if rowData.tags:
                    return str(rowData.tags)
                else:
                    return ""

        return None

    def headerData(
        self, section: int, orientation: Qt.Orientation, role=Qt.DisplayRole
    ):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return None

    def flags(self, index: QModelIndex):
        flags = super().flags(index)
        if index.column() == 0 or index.column() == 5:  # Name or Tags column
            flags |= Qt.ItemIsEditable
        return flags

    def setData(self, index: QModelIndex, value, role=Qt.EditRole) -> bool:
        if not index.isValid():
            return False

        if role == Qt.EditRole:
            mod = self._data[index.row()]
            try:
                if index.column() == 0:  # Name column
                    # Update the database
                    mod.name = value
                    mod.save()

                    # Update the model
                    self._data[index.row()] = mod

                    # Emit signal that data changed
                    self.dataChanged.emit(index, index, [Qt.DisplayRole])
                    return True
                elif index.column() == 5:  # Tags column
                    # This will be handled by the MainWindow's edit_tags method
                    return False

            except Exception as e:
                print(f"Error updating mod: {e}")
                return False

        return False

    def addMod(self, mod: Mod):
        """Add a new mod to the model"""
        self.beginInsertRows(QModelIndex(), len(self._data), len(self._data))
        self._data.append(mod)
        self.endInsertRows()

    def updateMod(self, index: int, mod: Mod):
        """Update an existing mod in the model"""
        if 0 <= index < len(self._data):
            self._data[index] = mod
            self.dataChanged.emit(
                self.index(index, 0), self.index(index, self.columnCount(None) - 1)
            )

    def refreshData(self):
        """Refresh all data in the model"""
        self.beginResetModel()
        self._data = mods.get_game_mods()
        self.endResetModel()

    def getMod(self, index: int) -> Mod:
        """Get mod at specified index"""
        return self._data[index]

    def removeMod(self, index: int):
        """Remove a mod from the model"""
        self.beginRemoveRows(QModelIndex(), index, index)
        self._data.pop(index)
        self.endRemoveRows()

    def toggleActive(self, index: int):
        """Toggle the active state of a mod"""
        mod = self._data[index]
        mod.active = not mod.active
        mod.save()

        # Update the model
        self._data[index] = mod
        self.dataChanged.emit(
            self.index(index, 4),  # Active column
            self.index(index, 4),
            [Qt.DisplayRole],
        )

    def updateLoadOrders(self, start_index: int, end_index: int):
        """Update load orders for all mods between start and end index"""
        # Sort the affected mods by their current position in the model
        affected_mods = self._data[start_index : end_index + 1]

        # Update load orders sequentially
        for i, mod in enumerate(affected_mods, start=start_index):
            # Update the load order in the database
            mod.load_order = i
            mod.save()

            # Update the model's data
            self._data[i] = mod

        # Notify view of the changes
        self.dataChanged.emit(
            self.index(start_index, 1),  # Load Order column
            self.index(end_index, 1),
            [Qt.DisplayRole],
        )

    def moveModToPosition(self, from_index: int, to_index: int):
        """Move a mod to a new position and update all affected load orders"""
        if from_index == to_index:
            return

        # Get the mod to move
        mod = self._data[from_index]

        # Remove from current position
        self.beginRemoveRows(QModelIndex(), from_index, from_index)
        self._data.pop(from_index)
        self.endRemoveRows()

        # Insert at new position
        self.beginInsertRows(QModelIndex(), to_index, to_index)
        self._data.insert(to_index, mod)
        self.endInsertRows()

        # Update load orders in database and model
        start, end = min(from_index, to_index), max(from_index, to_index)
        self.updateLoadOrders(start, end)
