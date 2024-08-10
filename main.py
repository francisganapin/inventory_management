import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import  QApplication

from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6 import  QtWidgets
import sys
from datetime import datetime
import os
import sqlite3
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QDate








class MyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        try:

            uic.loadUi('main.ui',self)
            self.setFixedSize(self.size())

            self.model_stock = QStandardItemModel()
            self.model_stock.setHorizontalHeaderLabels(['Id','Name','Brand','Color','Date','Category','Quantity'])
            self.tableView.setModel(self.model_stock)
            self.show_data()
            self.save_bt.clicked.connect(self.insert_data)
            self.refresh_bt.clicked.connect(self.show_data)
            self.search_bt.clicked.connect(self.search_data)
            self.select_bt.clicked.connect(self.selected_table)
    
            self.delete_bt.clicked.connect(self.remove_item)
            self.update_bt.clicked.connect(self.update_data)



            self.name=self.name_input.text()
            self.brand=self.brand_input.currentText()
            self.color=self.color_input.currentText()
            self.date=self.date_input.text()
            self.catergory=self.category_input.currentText()
            #USE VALUE IF YOU  USE SPINBOX
            self.quantity = self.quantity_input.value()
            #USE TOplaintext if you use  qtextbrowser







            
        except FileNotFoundError:
                print("ok")

    def show_data(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory,'database.db')
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        try:
            cursor.execute('Select id,name,brand,color,date,category,quantity FROM products')
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
         
        
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory,'database.db')
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''INSERT INTO products
                        (name,brand,color, date,category,quantity)
                        VALUES(?,?,?,?,?,?)''', 
                        (self.name,self.brand,self.color, self.date,self.catergory,self.quantity))
            conn.commit()
            self.validator_label.setText(f"subject_value: data was successfully input")
        except sqlite3.IntegrityError:
           
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
            self.validator_label.setText(f"subject_value: {subject_value} was delete")
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



    def get_selected_item(self):
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
            text = selected_item.data(subject_value)
            # Print subject_value to debug its content
            print(text)
            print(f"subject_value: {subject_value}")
            self.validator_label.setText(f"subject_value: {subject_value}")
            # Remove the corresponding item from self.mask
           

            # Remove the row from the table view
            

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

        query = "SELECT id,name,brand,color,date,category,quantity FROM products WHERE 1=1"
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
            self.validator_label.setText('Search Results Fetched Successfully')
        except sqlite3.Error as e:
            print(f'Sqlite error: {e}')
        finally:
            conn.close()

    

    def selected_table(self):
        self.selected_items = self.tableView.selectionModel().selectedRows()
        self.output = []

        for selected_item in self.selected_items:
            row_index = selected_item.row()
            row_data = []

            for column in range(self.model_stock.columnCount()):
                index = self.model_stock.index(row_index,column)
                row_data.append(index.data())
            self.output .append(row_data)

        if self.output:
            self.item = self.output[0]  # Assuming you want to update with the first selected item
            self.name_input.setText(str(self.item[1]))
            self.brand_input.setCurrentText(str(self.item[2]))
            self.color_input.setCurrentText(str(self.item[3]))
            date_str = self.item[4]
            self.date_obj = QDate.fromString(str(date_str), "yyyy-MM-dd")
            self.date_input.setDate(self.date_obj)
            self.category_input.setCurrentText(str(self.item[5]))
            self.quantity_input.setValue(int(self.item[6]))

    def update_data(self):

        # Fetch the current item ID
        item_id = self.item[0]

        # Fetch updated values directly from the input widgets
        name = self.name_input.text()
        brand = self.brand_input.currentText()
        color = self.color_input.currentText()
        date = self.date_input.date().toString("yyyy-MM-dd")
        category = self.category_input.currentText()
        quantity = self.quantity_input.value()

        # Prepare the database connection
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, 'database.db')
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''UPDATE products
                            SET name = ?, brand = ?, color = ?, date = ?, category = ?, quantity = ?
                            WHERE id = ?''', 
                            (name, brand, color, date, category, quantity, item_id))
            conn.commit()
            print('Data updated successfully.')
            self.validator_label.setText('Data updated successfully. click reshresh now')
        except sqlite3.IntegrityError as e:
            print(f'SQLite integrity error: {e}')
        finally:
            conn.close()

    
    

if __name__ == "__main__":
     app = QApplication(sys.argv)
     main_app = MyApp()
     main_app.show()
     sys.exit(app.exec())