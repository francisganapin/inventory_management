import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import  QApplication

from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6 import  QtWidgets
import sys
from datetime import datetime
import os
import sqlite3
from PyQt6.QtWidgets import QMessageBox


class MyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        try:

            uic.loadUi('main.ui',self)
            self.setFixedSize(self.size())

            self.model_stock = QStandardItemModel()
            self.model_stock.setHorizontalHeaderLabels(['Id','Name','Brand','Color','Date','Category','Quantity','Decription'])
            self.tableView.setModel(self.model_stock)
            self.show_data()
            self.save_bt.clicked.connect(self.insert_data)
            self.refresh_bt.clicked.connect(self.show_data)
            self.search_bt.clicked.connect(self.search_data)
            self.delete_bt.clicked.connect(self.remove_item)
            
        except FileNotFoundError:
                print("ok")

    def show_data(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory,'database.db')
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        try:
            cursor.execute('Select id,name,brand,color,date,category,quantity,description FROM products')
            rows = cursor.fetchall()
            self.model_stock.removeRows(0, self.model_stock.rowCount())

            for row_data in rows:
                  items = [QStandardItem(str(data))for data in row_data]
                  self.model_stock.appendRow(items)
            print('ok')
        except sqlite3.Error as e:
            print(f'Sqlite error: {e}')
        finally:
            conn.close()

    def insert_data(self):
         
        name=self.name_input.text()
        brand=self.brand_input.currentText()
        color=self.color_input.currentText()
        date=self.date_input.text()
        catergory=self.category_input.currentText()
        #USE VALUE IF YOU  USE SPINBOX
        quantity = self.quantity_input.value()
        #USE TOplaintext if you use  qtextbrowser
        description = self.description_input.toPlainText()

        
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory,'database.db')
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''INSERT INTO products
                        (name,brand,color, date,category,quantity,description)
                        VALUES(?,?,?,?,?,?,?)''', 
                        (name,brand,color, date,catergory,quantity,description))
            conn.commit()
            print('ok na po na insert na')
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Duplicate Id", f"An entry with ID {name} is already exists.")
        finally:
            conn.close()
    


    def remove_item(self):
        """delete data on the tree view"""
        #https://www.reddit.com/r/learnpython/comments/6723eq/deleting_selected_items_from_the_treeview_and/ <-this one is souce that i use
        
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, 'database.db')

        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        selected_items = self.tableView.selectionModel().selectedRows()

        self.mask = []

        for selected_item in selected_items:
            row_index = selected_item.row()

            # Get the value of the first column in the selected row
            subject_value = self.tableView.model().index(row_index, 0).data()

            # Print subject_value to debug its content
            print(f"subject_value: {subject_value}")

            # Remove the corresponding item from self.mask
            for i, mask in enumerate(self.mask):
                if mask.subject == subject_value:
                    self.mask.pop(i)
                    break

            # Remove the row from the table view
            self.tableView.model().removeRow(row_index)

            # Delete the corresponding row from the database
            cursor.execute("DELETE FROM products WHERE Id=?", (subject_value,))

        conn.commit()
        conn.close()

    def search_data(self):
        """
        Search the data in the second tab. 
        You can choose to search by name or ID.
        """
        search_name = self.search_name_input.text()
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, 'database.db')
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        query = "SELECT id,name,brand,color,date,category,quantity,description Address FROM products WHERE 1=1"
        params = []

        if search_name:
            query += " AND Name LIKE ?"
            params.append(f"%{search_name}%")

        try:
            cursor.execute(query, params)
            rows = cursor.fetchall()

            self.model_stock.removeRows(0, self.model_stock.rowCount())  # Clear the model

            for row_data in rows:
                items = [QStandardItem(str(data)) for data in row_data]
                self.model_stock.appendRow(items)

            print('Search Results Fetched Successfully')
        except sqlite3.Error as e:
            print(f'Sqlite error: {e}')
        finally:
            conn.close()






if __name__ == "__main__":
     app = QApplication(sys.argv)
     main_app = MyApp()
     main_app.show()
     sys.exit(app.exec())