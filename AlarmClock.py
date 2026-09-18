from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QTableWidgetItem, QLCDNumber, QTableWidget, QDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from AddAlarm import UI_Dialog
from PyQt5.QtCore import QTime, QTimer
from datetime import datetime
from PyQt5.QtMultimedia import QSound
import sys

class UI(QMainWindow):
	def __init__(self):
		super(UI, self).__init__()

		# Load the ui file
		uic.loadUi("AlarmClock.ui", self)
		self.setWindowTitle("Alarm Clock")
		
        # define widgets
		self.clockLCD = self.findChild(QLCDNumber, "ClockLCD")
		self.appLabel = self.findChild(QLabel, "AppLabel")
		self.addAlarmButton = self.findChild(QPushButton, "AddAlarmButton")
		self.alarmTable = self.findChild(QTableWidget, "alarmTable")
		self.alarmTable.setColumnWidth(0,70)
		self.alarmTable.setColumnWidth(1,120)
		self.alarmTable.setColumnWidth(2,70)
		self.alarmTable.setColumnWidth(3,50)
		self.alarmTable.setColumnWidth(4,60)

		# signals and slots
		self.addAlarmButton.clicked.connect(self.add_Alarm)

        # create timer
		self.timer = QTimer()
		self.timer.timeout.connect(self.lcd_clock)
		# connect check_alarms to the timer
		self.timer.timeout.connect(self.check_Alarms)
		# start the timer and update every second
		self.timer.start(1000)
		# call the lcd clock function
		self.lcd_clock()
		# alarm ringing one time
		self.triggered_alarms = set()
		# show the app
		self.show()
		
	def lcd_clock(self):
		# get the time
		time = datetime.now()
		formatted_time = time.strftime("%I:%M:%S %p")
		# set number of lcd digits
		self.clockLCD.setDigitCount(12)
		self.clockLCD.display(formatted_time)

		
	def add_Alarm(self):
		dialog = UI_Dialog()
		result = dialog.exec_()
		if result == QDialog.Accepted:
			row = self.alarmTable.rowCount()
			self.alarmTable.insertRow(row)
			self.alarmTable.setItem(row, 0, QTableWidgetItem(dialog.selectedTime))
			self.alarmTable.setItem(row, 1, QTableWidgetItem(dialog.selectedRepeat))
			status = "ON" if dialog.selectedEnable else "OFF"
			self.alarmTable.setItem(row, 2, QTableWidgetItem(status))
			editButton= QPushButton()
			editButton.setIcon(QIcon("icons/icons8-edit-24.png"))
			deleteButton= QPushButton()
			deleteButton.setIcon(QIcon("icons/icons8-trash-26.png"))
			self.alarmTable.setCellWidget(row, 3, editButton)
			self.alarmTable.setCellWidget(row, 4, deleteButton)
			editButton.clicked.connect(self.edit_Alarm)
			deleteButton.clicked.connect(self.delete_Alarm)
		    

		
	def check_Alarms(self):
		currentTime = QTime.currentTime().toString("HH:mm")
		rows = self.alarmTable.rowCount()
		for row in range(rows):
			alarmTime = self.alarmTable.item(row, 0).text()
			repeat = self.alarmTable.item(row,1).text()
			status = self.alarmTable.item(row, 2).text()
			today = datetime.now().strftime("%A")
			if repeat != "Everyday" and repeat != today:
				continue
			alarm_key = f"{row}-{alarmTime}"  
			if currentTime == alarmTime and status == "ON":
				if alarm_key not in self.triggered_alarms:
					self.triggered_alarms.add(alarm_key)
					QSound.play("sounds/alarm.wav")
					QMessageBox.information(self,"Alarm",f"Alarm {alarmTime}")
			if currentTime != alarmTime:
				self.triggered_alarms.discard(alarm_key)                    


	def delete_Alarm(self):
		button = self.sender()
		index = self.alarmTable.indexAt(button.pos())
		row = index.row()


	def edit_Alarm(self, row):
		dialog = UI_Dialog()
		time = self.alarmTable.item(row,0).text()
		repeat = self.alarmTable.item(row,1).text()
		status = self.alarmTable.item(row,2).text()
		dialog.alarmTimeEdit.setTime(QTime.fromString(time, "HH:mm"))
		dialog.repeatComboBox.setCurrentText(repeat)
		dialog.activityCheckBox.setChecked(status == "ON")
		result = dialog.exec_()
		if result == QDialog.Accepted:
			self.alarmTable.item(row, 0).setText(dialog.selectedTime)
			self.alarmTable.item(row, 1).setText(dialog.selectedRepeat)
			status = "ON" if dialog.selectedEnable else "OFF"
			self.alarmTable.item(row, 2).setText(status)
		

# Initialize The App
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()

