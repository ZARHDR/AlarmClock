from PyQt5.QtWidgets import QDialog, QTimeEdit, QLabel, QComboBox, QCheckBox, QDialogButtonBox
from PyQt5 import uic


class UI_Dialog(QDialog):
	def __init__(self):
		super(UI_Dialog, self).__init__()
		
        	# Load the ui file
		uic.loadUi("AddAlarm.ui", self)
		self.setWindowTitle("Add Alarm")
		
        # add widgets
		self.alarmTimeEdit = self.findChild(QTimeEdit, "alarmTimeEdit")
		self.repeatLabel = self.findChild(QLabel, "repeatLabel")
		self.statuenableLabelsLabel = self.findChild(QLabel, "enableLabel")
		self.repeatComboBox = self.findChild(QComboBox, "repeatComboBox")
		self.activityCheckBox = self.findChild(QCheckBox, "ActivityCheckBox")
		self.saveDialogButton = self.findChild(QDialogButtonBox, "saveDialogButton")
		# combobox
		dayItems = ["Everyday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
		self.repeatComboBox.addItems(dayItems)

		# signals
		self.saveDialogButton.accepted.connect(self.saveAlarm)
		self.saveDialogButton.rejected.connect(self.reject)
		
	def reject(self):
		super().reject()
		
	def saveAlarm(self):
		alarmTime = self.alarmTimeEdit.time()
		repeat = self.repeatComboBox.currentText()
		enable = self.activityCheckBox.isChecked()
	
		self.selectedTime = alarmTime.toString("HH:mm")
		self.selectedRepeat = repeat
		self.selectedEnable = enable
		self.accept()


