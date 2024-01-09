import sys
import chat
import llama_cpp
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
							 QLabel, QLineEdit, QPushButton, QSizePolicy, QScrollArea,
							 QSpacerItem, QGroupBox, QGridLayout, QTextEdit, QFileDialog,
							 QRadioButton)
from PyQt5.QtGui import (QFont, QCursor, QFontMetrics, QTextCursor, QIcon)
from PyQt5.QtCore import (QThread, pyqtSignal, Qt, QObject)

class Window(QWidget):
	def __init__(self):
		super().__init__()
		self.messages = [] # array of widgets

		### Create widgets - biggest to smallest
		
		# Top stuff
		self.radio_stuff = QWidget()
		self.radio_stuff.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
		self.options_stuff = QWidget()
		self.options_stuff.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

		# Scroll area for chat messages
		self.scroll_area = QScrollArea(self)
		self.scroll_area_contents = QWidget()
		self.scroll_area.setWidget(self.scroll_area_contents)
		self.scroll_area.setWidgetResizable(True); # <----- IMPORTANT!!

		# Vertical spacer that ensures empty space above all messages
		self.spacer = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)

		# Start message
		self.start_message = QLabel('Select a model above to begin.\n\n\n')
		self.start_message.setWordWrap(True)
		self.start_message.setFont(QFont('Arial', 16))
		self.start_message.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
		self.start_message.setAlignment(Qt.AlignCenter)

		# Input Widgets
		self.input_stuff = QWidget()
		self.input = QTextEdit()
		self.input.setText('')
		self.input.setFont(QFont('Arial', 12))
		self.input.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
		self.input.setAcceptRichText(False)

		self.send_button = QPushButton()
		self.send_button.setFixedSize(40, 40)
		self.send_button.clicked.connect(lambda: self.send_button_clicked())
		self.send_button.setStyleSheet("border-image : url(_internal/svgs/send.svg);")
		self.send_button.setCursor(QCursor(Qt.PointingHandCursor))

		# Top part
		self.radio_option1 = QRadioButton('Local File')
		self.radio_option1.setChecked(True)
		self.radio_option2 = QRadioButton('OpenAI API Key')
		self.radio_option3 = QRadioButton('Mistral API Key')
		self.radio_spacer = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Maximum)

		self.radio_option1.toggled.connect(self.option1_clicked)
		self.radio_option2.toggled.connect(self.option2_clicked)
		self.radio_option3.toggled.connect(self.option3_clicked)

		self.file_button = QPushButton('Select Model')
		self.file_button.clicked.connect(self.open_file_dialog)
		self.file_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
		self.path_label = QLabel('No model selected')

		self.line_edit_2 = QLineEdit()
		self.line_edit_2.textChanged.connect(lambda: self.update_api_keys())
		self.line_edit_2.setFixedWidth(400)
		self.line_edit_2.setVisible(False)

		self.line_edit_3 = QLineEdit()
		self.line_edit_3.textChanged.connect(lambda: self.update_api_keys())
		self.line_edit_3.setFixedWidth(400)
		self.line_edit_3.setVisible(False)

		self.api_label = QLabel('API Key')
		self.api_label.setVisible(False)


		### Create Layouts - biggest to smallest

		# Parent layout holding everything
		self.parent_layout = QVBoxLayout(self)

		# Layout holding everything except for input area	
		self.chat_layout = QVBoxLayout(self.scroll_area_contents)

		# Layout holding input stuff
		self.input_layout = QHBoxLayout(self.input_stuff)

		# Layout holding top stuff
		self.radio_layout = QHBoxLayout(self.radio_stuff)
		self.options_layout = QHBoxLayout(self.options_stuff)
		self.radio_layout.setContentsMargins(0, 0, 0, 0)
		self.options_layout.setContentsMargins(0, 0, 0, 0)


		### Add Widgets to layouts - biggest to smallest
		self.parent_layout.addWidget(self.radio_stuff)
		self.parent_layout.addWidget(self.options_stuff)
		self.parent_layout.addWidget(self.scroll_area)
		self.parent_layout.addWidget(self.input_stuff)

		self.chat_layout.addItem(self.spacer)
		self.chat_layout.addWidget(self.start_message)
		# self.chat_layout.addWidget(self.example_1)
		# self.chat_layout.addWidget(self.example_2)
		# self.chat_layout.addWidget(self.example_3)

		self.input_layout.addWidget(self.input)
		self.input_layout.addWidget(self.send_button)

		self.radio_layout.addWidget(self.radio_option1)
		self.radio_layout.addWidget(self.radio_option2)
		self.radio_layout.addWidget(self.radio_option3)
		self.radio_layout.addItem(self.radio_spacer)

		self.options_layout.addWidget(self.file_button)
		self.options_layout.addWidget(self.path_label)
		self.options_layout.addWidget(self.api_label)
		self.options_layout.addWidget(self.line_edit_2)
		self.options_layout.addWidget(self.line_edit_3)

		# Start
		self.resize(500, 800)
		self.setWindowTitle("LexGUI")
		self.setWindowIcon(QIcon('_internal/icon.ico'))

	def update_api_keys(self):
		new_chat.openai_api_key = self.line_edit_2.text()
		new_chat.mistral_api_key = self.line_edit_3.text()

	def option1_clicked(self):
		"""Run if the local model option is selected"""
		if self.radio_option1.isChecked():
			new_chat.type_of_model = 0
			self.api_label.setVisible(False)
			self.path_label.setVisible(True)
			self.file_button.setVisible(True)
			self.line_edit_2.setVisible(False)
			self.line_edit_3.setVisible(False)
			self.path_label.setMaximumSize(999999,999999)
			self.path_label.setMinimumSize(0, 0)
			self.line_edit_2.setFixedWidth(1)
			self.line_edit_3.setFixedWidth(1)

	def option2_clicked(self):
		"""Run if the OpenAI API option is selected"""
		if self.radio_option2.isChecked():
			new_chat.type_of_model = 1
			self.update_api_keys()
			self.api_label.setVisible(True)
			self.path_label.setVisible(False)
			self.file_button.setVisible(False)
			self.line_edit_2.setVisible(True)
			self.line_edit_3.setVisible(False)
			self.path_label.setFixedWidth(1)
			self.line_edit_2.setFixedWidth(400)
			self.line_edit_3.setFixedWidth(1)
	
	def option3_clicked(self):
		"""Run if the Mistral API option is selected"""
		if self.radio_option3.isChecked():
			new_chat.type_of_model = 2
			self.update_api_keys()
			self.api_label.setVisible(True)
			self.path_label.setVisible(False)
			self.file_button.setVisible(False)
			self.line_edit_2.setVisible(False)
			self.line_edit_3.setVisible(True)
			self.path_label.setFixedWidth(1)
			self.line_edit_2.setFixedWidth(1)
			self.line_edit_3.setFixedWidth(400)

	def open_file_dialog(self):
		"""Open the file dialog screen in another thread, for loading local model."""
		self.file_thread = QThread()
		self.file_worker = Worker2()
		self.file_worker.moveToThread(self.file_thread)

		self.file_thread.started.connect(self.file_worker.run)
		self.file_worker.path_found.connect(lambda path_string: self.path_label.setText(f'Please wait. Loading {path_string}'))
		self.file_worker.loading_finished.connect(lambda: (self.path_label.setText('Running' + self.path_label.text()[20:]), self.file_thread.quit()))
		self.file_thread.start()		

	def send_button_clicked(self):
		try:
			self.start_message.deleteLater()
		except:
			pass

		if new_chat.is_generating == False:
			self.send_button.setStyleSheet("border-image : url(_internal/svgs/stop.svg);")
			self.write_message(self.input.toPlainText(), True)
			self.messages[-1].setStyleSheet("background-color: rgb(209, 209, 209)")	
			new_chat.add_to_context('user', self.input.toPlainText())
			print(new_chat.context)
			self.ask_model()
			self.input.setText('')
		else:
			self.send_button.setStyleSheet("border-image : url(_internal/svgs/send.svg);")
			new_chat.is_generating = False

	def delete_message_button_clicked(self, index):
		for _ in range(index, len(self.messages)):
			self.messages[-1].deleteLater()
			del self.messages[-1]
			del new_chat.context[-1]

	def edit_message_button_clicked(self, index):
		new_chat.is_generating = False
		self.input.setText(self.messages[index].findChild(QLabel).text())
		self.input.setFocus()
		self.input.moveCursor(QTextCursor.End)
		self.delete_message_button_clicked(index)

	def copy_message_button_clicked(self, index):
		clipboard = QApplication.clipboard()
		print(self.messages[index].findChild(QLabel).text())
		clipboard.setText(self.messages[index].findChild(QLabel).text())

	def reload_message_button_clicked(self, index):
		self.send_button.setStyleSheet("border-image : url(_internal/svgs/send.svg);")
		new_chat.is_generating = False
		for _ in range(index, len(self.messages)):
			self.messages[-1].deleteLater()
			del self.messages[-1]
			del new_chat.context[-1]
		self.send_button.setStyleSheet("border-image : url(_internal/svgs/stop.svg);")
		print(new_chat.context)
		self.ask_model()

	def write_message(self, text, from_user = True):
		"""Create a new empty message box. from_user is to make sure correct buttons are loaded"""
		self.messages.append(QWidget(self.scroll_area_contents))
		last_message_widget = self.messages[-1]
		last_message_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
		last_message_layout = QGridLayout(last_message_widget)
		message = QLabel(last_message_widget)
		message.setFont(QFont('Arial', 10))
		message.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
		message.setTextInteractionFlags(Qt.TextSelectableByMouse|Qt.LinksAccessibleByMouse)
		message.setCursor(QCursor(Qt.IBeamCursor))
		message.setWordWrap(True)
		message.setText(text)
		if text == '':
			message.setText('_')
			message.clear()
		last_message_layout.addWidget(message, 0, 1, 4, 1)

		if from_user:
			delete_message_button = QPushButton(last_message_widget)
			delete_message_button.setFixedSize(20, 20)
			delete_message_button.setStyleSheet("border-image : url(_internal/svgs/delete.svg);")
			delete_message_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
			delete_message_button.setCursor(QCursor(Qt.PointingHandCursor))
			i = len(self.messages) - 1
			delete_message_button.clicked.connect(lambda: self.delete_message_button_clicked(i))
			last_message_layout.addWidget(delete_message_button, 3, 0, 1, 1)

			edit_message_button = QPushButton(last_message_widget)
			edit_message_button.setFixedSize(20, 20)
			edit_message_button.setStyleSheet("border-image: url(_internal/svgs/edit.svg);")
			edit_message_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
			edit_message_button.setCursor(QCursor(Qt.PointingHandCursor))
			i = len(self.messages) - 1
			edit_message_button.clicked.connect(lambda: self.edit_message_button_clicked(i))
			last_message_layout.addWidget(edit_message_button, 2, 0, 1, 1)
		else:
			reload_message_button = QPushButton(last_message_widget)
			reload_message_button.setFixedSize(20, 20)
			reload_message_button.setStyleSheet("border-image : url(_internal/svgs/reload.svg);")
			reload_message_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
			reload_message_button.setCursor(QCursor(Qt.PointingHandCursor))
			i = len(self.messages) - 1
			reload_message_button.clicked.connect(lambda: self.reload_message_button_clicked(i))
			last_message_layout.addWidget(reload_message_button, 2, 0, 1, 1)

		copy_message_button = QPushButton(last_message_widget)
		copy_message_button.setFixedSize(20, 20)
		copy_message_button.setStyleSheet("border-image : url(_internal/svgs/copy.svg);")
		copy_message_button.setCursor(QCursor(Qt.PointingHandCursor))
		i = len(self.messages) - 1
		copy_message_button.clicked.connect(lambda: self.copy_message_button_clicked(i))
		last_message_layout.addWidget(copy_message_button, 1, 0, 1, 1)

		
		self.chat_layout.addWidget(last_message_widget)

	def edit_message(self, addition, index = -1):
		"""Create addition on specified message. index specifies index of messages array."""
		self.messages[index].findChild(QLabel).setText(self.messages[index].findChild(QLabel).text() + str(addition))

	def ask_model(self):
		"""Initialize new thread for asking message"""
		self.write_message('', False)
		if new_chat.type_of_model == 0:
			self.messages[-1].setStyleSheet("background-color: rgb(161, 194, 230)")
		elif new_chat.type_of_model == 1:
			self.messages[-1].setStyleSheet("background-color: rgb(166, 255, 163)")
		elif new_chat.type_of_model == 2:
			self.messages[-1].setStyleSheet("background-color: rgb(236, 85, 0)")
		
		self.thread = QThread()
		self.worker = Worker()
		self.worker.moveToThread(self.thread)

		self.thread.started.connect(self.worker.run)
		self.worker.finished.connect(lambda: (self.send_button.setStyleSheet("border-image : url(_internal/svgs/send.svg);"), self.thread.quit()))
		self.worker.progress.connect(lambda chunk: self.edit_message(chunk))
		self.thread.start()


class Worker(QObject):
	"""Worker for running model"""
	finished = pyqtSignal()
	progress = pyqtSignal(str)
	def run(self):
		output = ''
		new_chat.is_generating = True
		for chunk in new_chat.query():
			output += chunk
			self.progress.emit(chunk)

		new_chat.is_generating = False
		new_chat.context.append({'role': 'assistant', 'content': output})
		self.finished.emit()


class Worker2(QObject):
	"""Worker for loading model"""
	path_found = pyqtSignal(str)
	loading_finished = pyqtSignal()
	def run(self):
		file_dialog = QFileDialog()
		file_dialog.exec_()
		file_path = file_dialog.selectedUrls()
		if file_path:
			file_name = file_path[0].fileName()
			self.path_found.emit(file_name)

			path_string = file_path[0].toString()
			if path_string[:8] == 'file:///' or path_string[:8] == 'file:\\\\\\':
				path_string = path_string[8:]
			try:
				new_chat.model = llama_cpp.Llama(model_path = path_string, chat_format = "chatml", n_ctx = 8192)
			except:
				print('Error loading model')
		self.loading_finished.emit()


new_chat = chat.Chat()

app = QApplication(sys.argv)
app.setAttribute(Qt.AA_UseHighDpiPixmaps)
window = Window()
window.show()
sys.exit(app.exec())