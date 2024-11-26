import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QTextEdit, QListWidget, QMessageBox, QDialog


class RecipeWindow(QWidget):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Рецепты")
    self.recipe_file = "recipes.json" # Теперь используем JSON
    self.load_recipes() # Загрузка рецептов

    self.recipe_name_label = QLabel("Название рецепта:")
    self.recipe_name_edit = QLineEdit()
    self.recipe_text_label = QLabel("Рецепт:")
    self.recipe_text_edit = QTextEdit()
    self.save_button = QPushButton("Записать рецепт")
    self.save_button.clicked.connect(self.save_recipe)
    self.add_button = QPushButton("Добавить рецепт") # Пока не используется
    self.view_button = QPushButton("Посмотреть рецепты")
    self.view_button.clicked.connect(self.view_recipes)
    self.recipe_list = QListWidget()

    layout = QVBoxLayout()
    layout.addWidget(self.recipe_name_label)
    layout.addWidget(self.recipe_name_edit)
    layout.addWidget(self.recipe_text_label)
    layout.addWidget(self.recipe_text_edit)
    layout.addWidget(self.save_button)
    layout.addWidget(self.add_button)
    layout.addWidget(self.view_button)
    layout.addWidget(self.recipe_list)
    self.setLayout(layout)


  def load_recipes(self):
    try:
      with open(self.recipe_file, "r", encoding="utf-8") as f:
        self.recipes = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
      self.recipes = {} # словарь


  def save_recipe(self):
    recipe_name = self.recipe_name_edit.text()
    recipe_text = self.recipe_text_edit.toPlainText()
    if not recipe_name or not recipe_text:
      QMessageBox.warning(self, "Ошибка", "Введите название и текст рецепта!")
      return

    self.recipes[recipe_name] = recipe_text
    self.save_recipes_to_file()
    self.recipe_name_edit.clear()
    self.recipe_text_edit.clear()
    QMessageBox.information(self, "Успешно", "Рецепт сохранен!")


  def save_recipes_to_file(self):
    try:
      with open(self.recipe_file, "w", encoding="utf-8") as f:
        json.dump(self.recipes, f, indent=4, ensure_ascii=False)
    except Exception as e:
      QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении рецептов: {e}")


  def view_recipes(self):
    self.recipe_list.clear()
    if not self.recipes:
      QMessageBox.information(self, "Информация", "Список рецептов пуст.")
      return

    for recipe_name in self.recipes:
      self.recipe_list.addItem(recipe_name)
    self.recipe_list.itemClicked.connect(self.show_full_recipe)


  def show_full_recipe(self, item):
    recipe_name = item.text()
    recipe_text = self.recipes.get(recipe_name)
    if recipe_text:
      dialog = RecipeDialog(recipe_name, recipe_text)
      dialog.exec_()


class RecipeDialog(QDialog):
  def __init__(self, recipe_name, recipe_text):
    super().__init__()
    self.setWindowTitle(recipe_name)
    layout = QVBoxLayout()
    text_edit = QTextEdit()
    text_edit.setReadOnly(True)
    text_edit.setText(recipe_text)
    layout.addWidget(text_edit)
    self.setLayout(layout)


if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = RecipeWindow()
  window.show()
  sys.exit(app.exec_())
