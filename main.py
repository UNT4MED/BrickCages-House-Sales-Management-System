import sys
import pickle
from datetime import datetime
from PyQt5.QtWidgets import QDialog, QFormLayout,QInputDialog
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,  QMessageBox
class Employee:
    def __init__(self, id, name, department, job_title, number, salary):
        self.id = id
        self.name = name
        self.department = department
        self.job_title = job_title
        self.number = number
        self.salary = salary


# Add a method to SalesManager to manage the team
class SalesManager(Employee):
    def __init__(self, id, name, number, salary):
        super().__init__(id, name, "Sales", "Manager", number, salary)
        self.salespersons = []

    def add_salesperson_to_team(self, salesperson):
        self.salespersons.append(salesperson)

    def view_team(self):
        team_details = []
        for salesperson in self.salespersons:
            team_details.append(
                f"Salesperson ID: {salesperson.id}\nName: {salesperson.name}\nNumber: {salesperson.number}\nSalary: {salesperson.salary}\n"
            )
        return team_details


class Salesperson(Employee):
    def __init__(self, id, name, number, salary, manager_id):
        super().__init__(id, name, "Sales", "Salesperson", number, salary)
        self.manager_id = manager_id


class House:
    def __init__(self, id, name, type, rooms, bathrooms, area, status, declared_price, selling_price, salesperson_id):
        self.id = id
        self.name = name
        self.type = type
        self.rooms = rooms
        self.bathrooms = bathrooms
        self.area = area
        self.status = status
        self.declared_price = declared_price
        self.selling_price = selling_price
        self.salesperson_id = salesperson_id


class Sale:
    def __init__(self, house_id, employee_id, sale_date, actual_price, declared_price, selling_price):
        self.house_id = house_id
        self.employee_id = employee_id
        self.sale_date = sale_date
        self.profit_loss = actual_price - selling_price  # Use selling_price for profit/loss


class RealEstateSystem:
    def __init__(self):
        self.employees = []
        self.houses = []
        self.sales = []

    def add_employee(self, employee):
        self.employees.append(employee)
        return self

    def find_employee_by_id(self, employee_id):
        for employee in self.employees:
            if employee.id == employee_id:
                return employee
        return None

    def find_house_by_id(self, house_id):
        for house in self.houses:
            if house.id == house_id:
                return house
        return None

    def add_house(self, house):
        existing_house = self.find_house_by_id(house.id)
        if existing_house:
            print(f"House with ID {house.id} already exists. Please enter a different House ID.")
        else:
            self.houses.append(house)
            # Save the updated real_estate_system back to the file
            fileobj = open(file, 'wb')
            pickle.dump(self, fileobj)
            fileobj.close()
            print("House added successfully!")

    def make_sale(self, house_id, employee_id, sale_date_str, declared_price_str, selling_price_str):
        # Convert strings to float
        declared_price = float(declared_price_str)
        selling_price = float(selling_price_str)

        # Check if the provided house_id and employee_id exist
        house = self.find_house_by_id(house_id)
        employee = self.find_employee_by_id(employee_id)

        if not house:
            print(f"House with ID {house_id} does not exist. Sale not recorded.")
            return

        if not employee:
            print(f"Employee with ID {employee_id} does not exist. Sale not recorded.")
            return

        # Create a Sale object with calculated profit/loss
        actual_price = declared_price + selling_price  # Calculate actual price
        profit_loss = actual_price - selling_price
        sale = Sale(house_id, employee_id, sale_date_str, actual_price, declared_price, selling_price)

        # Append the sale to the sales list
        self.sales.append(sale)

        # Update the house information
        house.selling_price = selling_price  # Update the selling price of the house

        # Update the employee information
        # Convert salary to float and then add profit_loss
        employee.salary = str(float(employee.salary) + profit_loss)

        # Save the updated real_estate_system back to the file
        with open(file, 'wb') as fileobj:
            pickle.dump(self, fileobj)

    def display_employee_details(self, employee_id):
        for employee in self.employees:
            if employee.id == employee_id:
                return f"Employee ID: {employee.id}\nName: {employee.name}\nDepartment: {employee.department}\nJob Title: {employee.job_title}\nNumber: {employee.number}\nSalary: {employee.salary}"

        # If the loop completes without finding the employee, return a message
        return f"Employee with ID {employee_id} not found."

    def display_house_details(self, house_id):
        for house in self.houses:
            if house.id == house_id:
                return f"House ID: {house.id}\nName: {house.name}\nType: {house.type}\nRooms: {house.rooms}\nBathrooms: {house.bathrooms}\nArea: {house.area} sq. ft.\nStatus: {house.status}\nDeclared Price: ${house.declared_price}\nSelling Price: ${house.selling_price}\nSalesperson: {house.salesperson_id}"

    def display_sales_details(self, employee_id, month):
        details = []
        for sale in self.sales:
            sale_date = datetime.strptime(sale.sale_date, "%Y-%m-%d")
            if sale.employee_id == employee_id and sale_date.month == month:
                house = self.find_house_by_id(sale.house_id)
                salesperson = self.find_employee_by_id(employee_id)

                # Calculate commission
                commission_rate = 0.05  # Assuming a commission rate of 5%
                commission = commission_rate * float(sale.profit_loss)

                # Calculate expected salary
                expected_salary = float(salesperson.salary) + commission

                details.append(
                    f"Sale Date: {sale.sale_date}\nHouse ID: {sale.house_id}\nProfit/Loss: ${sale.profit_loss}\nCommission: ${commission:.2f}\nExpected Salary: ${expected_salary:.2f}")

        return details
class EmployeeInputDialog(QDialog):
    def __init__(self, parent=None):
        super(EmployeeInputDialog, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.employee_id_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.department_edit = QLineEdit()
        self.job_title_edit = QLineEdit()
        self.number_edit = QLineEdit()
        self.salary_edit = QLineEdit()
        self.date_of_birth_edit = QLineEdit()
        self.passport_details_edit = QLineEdit()

        layout.addRow("Employee ID:", self.employee_id_edit)
        layout.addRow("Name:", self.name_edit)
        layout.addRow("Department:", self.department_edit)
        layout.addRow("Job Title:", self.job_title_edit)
        layout.addRow("Employee Number:", self.number_edit)
        layout.addRow("Salary:", self.salary_edit)
        layout.addRow("Date of Birth (YYYY-MM-DD):", self.date_of_birth_edit)
        layout.addRow("Passport Details:", self.passport_details_edit)

        self.ok_button = QPushButton('Add Employee')
        self.ok_button.clicked.connect(self.accept)

        layout.addRow(self.ok_button)

        self.setLayout(layout)

    def get_employee_data(self):
        return {
            'id': self.employee_id_edit.text(),
            'name': self.name_edit.text(),
            'department': self.department_edit.text(),
            'job_title': self.job_title_edit.text(),
            'number': self.number_edit.text(),
            'salary': self.salary_edit.text(),
            'date_of_birth': self.date_of_birth_edit.text(),
            'passport_details': self.passport_details_edit.text(),
        }


class ModifyEmployeeDialog(EmployeeInputDialog):
    def __init__(self, existing_employee, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Modify Employee')
        self.ok_button.setText('Modify Employee')

        # Set the existing employee data
        self.employee_id_edit.setText(existing_employee.id)
        self.name_edit.setText(existing_employee.name)
        self.department_edit.setText(existing_employee.department)
        self.job_title_edit.setText(existing_employee.job_title)
        self.number_edit.setText(existing_employee.number)
        self.salary_edit.setText(existing_employee.salary)

    def get_employee_data(self):
        return {
            'employee_id': self.employee_id_edit.text(),
            'name': self.name_edit.text(),
            'department': self.department_edit.text(),
            'job_title': self.job_title_edit.text(),
            'number': self.number_edit.text(),
            'salary': self.salary_edit.text(),
        }

    def get_modified_data(self):
        # This method provides the modified data
        return self.get_employee_data()
class HouseInputDialog(QDialog):
    def __init__(self, parent=None):
        super(HouseInputDialog, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.house_id_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.type_edit = QLineEdit()
        self.rooms_edit = QLineEdit()
        self.bathrooms_edit = QLineEdit()
        self.area_edit = QLineEdit()
        self.status_edit = QLineEdit()
        self.salesperson_id_edit = QLineEdit()
        self.declared_price_edit = QLineEdit()
        self.selling_price_edit = QLineEdit()

        layout.addRow("House ID:", self.house_id_edit)
        layout.addRow("Name:", self.name_edit)
        layout.addRow("Type:", self.type_edit)
        layout.addRow("Rooms:", self.rooms_edit)
        layout.addRow("Bathrooms:", self.bathrooms_edit)
        layout.addRow("Area:", self.area_edit)
        layout.addRow("Status:", self.status_edit)
        layout.addRow("Salesperson ID:", self.salesperson_id_edit)
        layout.addRow("Declared Price:", self.declared_price_edit)
        layout.addRow("Selling Price:", self.selling_price_edit)

        self.ok_button = QPushButton('Add House')
        self.ok_button.clicked.connect(self.accept)

        layout.addRow(self.ok_button)

        self.setLayout(layout)

    def get_house_data(self):
        return {
            'house_id': self.house_id_edit.text(),
            'name': self.name_edit.text(),
            'type': self.type_edit.text(),
            'rooms': self.rooms_edit.text(),
            'bathrooms': self.bathrooms_edit.text(),
            'area': self.area_edit.text(),
            'status': self.status_edit.text(),
            'salesperson_id': self.salesperson_id_edit.text(),
            'declared_price': self.declared_price_edit.text(),
            'selling_price': self.selling_price_edit.text(),
        }
class SaleInputDialog(QDialog):
    def __init__(self, parent=None):
        super(SaleInputDialog, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.house_id_edit = QLineEdit()
        self.employee_id_edit = QLineEdit()
        self.sale_date_edit = QLineEdit()
        self.declared_price_edit = QLineEdit()
        self.selling_price_edit = QLineEdit()

        layout.addRow("House ID:", self.house_id_edit)
        layout.addRow("Employee ID:", self.employee_id_edit)
        layout.addRow("Sale Date (YYYY-MM-DD):", self.sale_date_edit)
        layout.addRow("Declared Price:", self.declared_price_edit)
        layout.addRow("Selling Price:", self.selling_price_edit)

        self.ok_button = QPushButton('Make Sale')
        self.ok_button.clicked.connect(self.accept)

        layout.addRow(self.ok_button)

        self.setLayout(layout)

    def get_sale_data(self):
        return {
            'house_id': self.house_id_edit.text(),
            'employee_id': self.employee_id_edit.text(),
            'sale_date': self.sale_date_edit.text(),
            'declared_price': self.declared_price_edit.text(),
            'selling_price': self.selling_price_edit.text(),
        }
class DisplayEmployeeDetailsDialog(QDialog):
    def __init__(self, parent=None):
        super(DisplayEmployeeDetailsDialog, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.employee_id_edit = QLineEdit()
        layout.addRow("Employee ID:", self.employee_id_edit)

        self.ok_button = QPushButton('Display Details')
        self.ok_button.clicked.connect(self.accept)

        layout.addRow(self.ok_button)

        self.setLayout(layout)

    def get_employee_id(self):
        return self.employee_id_edit.text()
class DisplayHouseDetailsDialog(QDialog):
    def __init__(self, parent=None):
        super(DisplayHouseDetailsDialog, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.house_id_edit = QLineEdit()
        layout.addRow("House ID:", self.house_id_edit)

        self.ok_button = QPushButton('Display Details')
        self.ok_button.clicked.connect(self.accept)

        layout.addRow(self.ok_button)

        self.setLayout(layout)

    def get_house_id(self):
        return self.house_id_edit.text()
class DisplaySalesDetailsDialog(QDialog):
    def __init__(self, parent=None):
        super(DisplaySalesDetailsDialog, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.employee_id_edit = QLineEdit()
        self.month_edit = QLineEdit()

        layout.addRow("Employee ID:", self.employee_id_edit)
        layout.addRow("Month:", self.month_edit)

        self.ok_button = QPushButton('Display Details')
        self.ok_button.clicked.connect(self.accept)

        layout.addRow(self.ok_button)

        self.setLayout(layout)

    def get_employee_id_and_month(self):
        return self.employee_id_edit.text(), int(self.month_edit.text())
class RealEstateApp(QWidget):
    def __init__(self, real_estate_system):
        super().__init__()

        self.real_estate_system = real_estate_system

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create widgets
        self.label = QLabel('Real Estate System')
        self.add_employee_button = QPushButton('Add Employee')
        self.modify_employee_button = QPushButton('Modify Employee')
        self.add_house_button = QPushButton('Add House')
        self.make_sale_button = QPushButton('Make Sale')
        self.display_employee_button = QPushButton('Display Employee Details')
        self.display_house_button = QPushButton('Display House Details')
        self.display_sales_button = QPushButton('Display Sales Details')
        self.exit_button = QPushButton('Exit')

        # Connect buttons to functions
        self.add_employee_button.clicked.connect(self.add_employee)
        self.modify_employee_button.clicked.connect(self.modify_employee)
        self.add_house_button.clicked.connect(self.add_house)
        self.make_sale_button.clicked.connect(self.make_sale)
        self.display_employee_button.clicked.connect(self.display_employee_details)
        self.display_house_button.clicked.connect(self.display_house_details)
        self.display_sales_button.clicked.connect(self.display_sales_details)
        self.exit_button.clicked.connect(self.close)

        # Add widgets to layout
        layout.addWidget(self.label)
        layout.addWidget(self.add_employee_button)
        layout.addWidget(self.modify_employee_button)
        layout.addWidget(self.add_house_button)
        layout.addWidget(self.make_sale_button)
        layout.addWidget(self.display_employee_button)
        layout.addWidget(self.display_house_button)
        layout.addWidget(self.display_sales_button)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

        self.setWindowTitle('Real Estate System')
        self.show()

    def add_employee(self):
        employee_dialog = EmployeeInputDialog(self)
        result = employee_dialog.exec_()

        if result == QDialog.Accepted:
            employee_data = employee_dialog.get_employee_data()

            existing_employee = self.real_estate_system.find_employee_by_id(employee_data['employee_id'])
            if existing_employee:
                print("Employee with the given ID already exists. Please enter a different Employee ID.")
                return

            # Check if the employee is a SalesManager
            if employee_data['job_title'].lower() == "manager":
                employee = SalesManager(**employee_data)
                self.real_estate_system.add_employee(employee)
                print("SalesManager added successfully!")

                # Assign salespersons to the SalesManager
                while True:
                    employee_dialog.employee_id_edit.clear()
                    employee_dialog.employee_id_edit.setPlaceholderText('Salesperson ID (enter "done" to finish):')
                    result = employee_dialog.exec_()
                    salesperson_id = employee_dialog.employee_id_edit.text()

                    if result == QDialog.Accepted and salesperson_id.lower() == "done":
                        break

                    salesperson = self.real_estate_system.find_employee_by_id(salesperson_id)
                    if salesperson and isinstance(salesperson, Salesperson):
                        employee.add_salesperson_to_team(salesperson)
                        print(f"Salesperson {salesperson_id} added to the team.")
                    else:
                        print(f"Invalid Salesperson ID: {salesperson_id}. Please enter a valid Salesperson ID.")
            else:
                employee = Employee(**employee_data)
                self.real_estate_system.add_employee(employee)

            # Save the updated real_estate_system back to the file
            with open(file, 'wb') as fileobj:
                pickle.dump(self.real_estate_system, fileobj)

            print("Employee added successfully!")

    def modify_employee(self):
        employee_id, ok = QInputDialog.getText(self, 'Enter Employee ID to modify:', 'Employee ID:')
        if ok:
            existing_employee = self.real_estate_system.find_employee_by_id(employee_id)

            if existing_employee:
                modify_dialog = ModifyEmployeeDialog(existing_employee, self)
                result = modify_dialog.exec_()

                if result == QDialog.Accepted:
                    modified_data = modify_dialog.get_modified_data()

                    # Update employee data
                    existing_employee.id = modified_data['employee_id']
                    existing_employee.name = modified_data['name']
                    existing_employee.department = modified_data['department']
                    existing_employee.job_title = modified_data['job_title']
                    existing_employee.number = modified_data['number']
                    existing_employee.salary = modified_data['salary']

                    # Save the updated real_estate_system back to the file
                    with open(file, 'wb') as fileobj:
                        pickle.dump(self.real_estate_system, fileobj)

                    print("Employee data modified successfully!")
                else:
                    print("Modification canceled.")
            else:
                print("Employee not found. Please enter a valid Employee ID.")

    def add_house(self):
        house_dialog = HouseInputDialog(self)
        result = house_dialog.exec_()

        if result == QDialog.Accepted:
            house_data = house_dialog.get_house_data()

            existing_house = self.real_estate_system.find_house_by_id(house_data['house_id'])
            if existing_house:
                print(f"House with ID {house_data['house_id']} already exists. Please enter a different House ID.")
                return

            house = House(
                house_data['house_id'],
                house_data['name'],
                house_data['type'],
                house_data['rooms'],
                house_data['bathrooms'],
                house_data['area'],
                house_data['status'],
                house_data['declared_price'],
                house_data['selling_price'],
                house_data['salesperson_id']
            )

            self.real_estate_system.houses.append(house)

            # Save the updated real_estate_system back to the file
            with open(file, 'wb') as fileobj:
                pickle.dump(self.real_estate_system, fileobj)

            print("House added successfully!")

    def make_sale(self):
        sale_dialog = SaleInputDialog(self)
        result = sale_dialog.exec_()

        if result == QDialog.Accepted:
            sale_data = sale_dialog.get_sale_data()

            self.real_estate_system.make_sale(
                sale_data['house_id'],
                sale_data['employee_id'],
                sale_data['sale_date'],
                sale_data['declared_price'],
                sale_data['selling_price']
            )
            print("Sale recorded successfully!")

    def display_employee_details(self):
        display_dialog = DisplayEmployeeDetailsDialog(self)
        result = display_dialog.exec_()

        if result == QDialog.Accepted:
            employee_id = display_dialog.get_employee_id()
            details = self.real_estate_system.display_employee_details(employee_id)

            message_box = QMessageBox()
            message_box.setWindowTitle("Employee Details")
            message_box.setText(details)
            message_box.exec_()

    def display_house_details(self):
        display_dialog = DisplayHouseDetailsDialog(self)
        result = display_dialog.exec_()

        if result == QDialog.Accepted:
            house_id = display_dialog.get_house_id()
            details = self.real_estate_system.display_house_details(house_id)
            message_box = QMessageBox()
            message_box.setWindowTitle("House Details")
            message_box.setText(details)
            message_box.exec_()

    def display_sales_details(self):
        display_dialog = DisplaySalesDetailsDialog(self)
        result = display_dialog.exec_()

        if result == QDialog.Accepted:
            employee_id, month = display_dialog.get_employee_id_and_month()
            details = self.real_estate_system.display_sales_details(employee_id, month)
            for detail in details:
                message_box = QMessageBox()
                message_box.setWindowTitle("Sale Details")
                message_box.setText(detail)
                message_box.exec_()

if __name__ == '__main__':
    app = QApplication([])

    file = "realEstate.pkl"
    try:
        fileobj = open(file, 'rb')
        real_estate_system = pickle.load(fileobj)
        fileobj.close()
    except FileNotFoundError:
        real_estate_system = RealEstateSystem()

    ex = RealEstateApp(real_estate_system)
    app.exec_()