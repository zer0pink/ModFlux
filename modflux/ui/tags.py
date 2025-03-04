from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
)
from PySide6.QtCore import Qt
from typing import Set

from modflux.db import Mod


class TagDialog(QDialog):
    def __init__(self, mod: Mod, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Edit Tags - {mod.name}")
        self.setMinimumWidth(400)
        self.mod = mod
        
        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Tag input
        input_layout = QHBoxLayout()
        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText("Enter new tag...")
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_tag)
        input_layout.addWidget(self.tag_input)
        input_layout.addWidget(self.add_button)
        layout.addLayout(input_layout)

        # Current tags list
        layout.addWidget(QLabel("Current Tags:"))
        self.current_tags = QListWidget()
        self.current_tags.setSelectionMode(QListWidget.ExtendedSelection)
        layout.addWidget(self.current_tags)

        # Existing tags list
        layout.addWidget(QLabel("Existing Tags:"))
        self.existing_tags = QListWidget()
        layout.addWidget(self.existing_tags)
        
        # Load tags
        self.load_tags()

        # Buttons
        button_layout = QHBoxLayout()
        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.clicked.connect(self.remove_selected_tags)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.remove_button)
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        # Connect double-click on existing tags
        self.existing_tags.itemDoubleClicked.connect(self.add_existing_tag)
        
        # Connect enter key in tag input
        self.tag_input.returnPressed.connect(self.add_tag)

    def load_tags(self):
        # Load current mod's tags
        current_tags = set(self.mod.tags.split(',')) if self.mod.tags else set()
        for tag in sorted(current_tags):
            if tag:  # Skip empty tags
                self.current_tags.addItem(tag)

        # Load all existing tags from database
        existing_tags = set()
        for mod in Mod.select():
            if mod.tags:
                existing_tags.update(mod.tags.split(','))
        
        # Remove current mod's tags from existing tags
        existing_tags.difference_update(current_tags)
        
        # Add to list widget
        for tag in sorted(existing_tags):
            if tag:  # Skip empty tags
                self.existing_tags.addItem(tag)

    def add_tag(self):
        tag = self.tag_input.text().strip().lower()
        if tag:
            # Check if tag already exists in current tags
            existing_items = self.current_tags.findItems(tag, Qt.MatchExactly)
            if not existing_items:
                self.current_tags.addItem(tag)
            self.tag_input.clear()

    def add_existing_tag(self, item: QListWidgetItem):
        tag = item.text()
        # Check if tag already exists in current tags
        existing_items = self.current_tags.findItems(tag, Qt.MatchExactly)
        if not existing_items:
            self.current_tags.addItem(tag)

    def remove_selected_tags(self):
        for item in self.current_tags.selectedItems():
            self.current_tags.takeItem(self.current_tags.row(item))

    def get_tags(self) -> Set[str]:
        """Return the current set of tags"""
        tags = set()
        for i in range(self.current_tags.count()):
            tags.add(self.current_tags.item(i).text())
        return tags 