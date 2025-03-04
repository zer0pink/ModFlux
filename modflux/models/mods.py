from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from typing import List

from modflux import mods
from modflux.db import Mod, ModVersion, Game


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
            row_data = self._data[index.row()]

            if index.column() == 0:
                return str(row_data.name)
            if index.column() == 1:
                return str(row_data.load_order)
            elif index.column() == 2:
                return str(row_data.version.version)
            elif index.column() == 3:
                return str(row_data.latest_version)
            elif index.column() == 4:
                return bool(row_data.active)
            elif index.column() == 5:
                return str(row_data.tags)

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

    def add_mod(self, mod: Mod):
        """Add a new mod to the model"""
        self.beginInsertRows(QModelIndex(), len(self._data), len(self._data))
        self._data.append(mod)
        self.endInsertRows()

    def update_mod(self, index: int, mod: Mod):
        """Update an existing mod in the model"""
        if 0 <= index < len(self._data):
            self._data[index] = mod
            self.dataChanged.emit(
                self.index(index, 0), self.index(index, self.columnCount(None) - 1)
            )

    def refresh_data(self):
        """Refresh all data in the model"""
        self.beginResetModel()
        self._data = mods.get_game_mods()
        self.endResetModel()

    def get_mod(self, index: int) -> Mod:
        """Get mod at specified index"""
        return self._data[index]

    def remove_mod(self, index: int):
        """Remove a mod from the model"""
        self.beginRemoveRows(QModelIndex(), index, index)
        self._data.pop(index)
        self.endRemoveRows()

    def toggle_active(self, index: int):
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

    def update_load_orders(self, start_index: int, end_index: int):
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

    def move_mod_to_position(self, from_index: int, to_index: int):
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
        self.update_load_orders(start, end)
