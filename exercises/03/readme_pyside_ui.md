# Exercise 3 — PySide6 UI Programming & Embedded Matplotlib

---

## Overview

In this exercise, you will learn how to build a **desktop application** using **PySide6** and integrate it with Matplotlib for signal visualization.

This is a key transition in the course:

* From **scripts → applications**
* From **static plots → interactive UI**
* From **sequential code → event-driven programming**

By the end, you should understand the basic building blocks of a graphical user interface:

* windows
* widgets
* layouts
* buttons
* dropdowns
* sliders
* checkboxes
* radio buttons
* text inputs
* tables
* tabs
* menus
* dialogs
* signals and slots
* embedded plots

---

## Why GUI Programming?

So far, your programs usually:

* run once
* produce output
* exit

Now we want:

* persistent applications
* user interaction
* dynamic updates
* visual feedback
* reusable interfaces

A graphical user interface allows users to control a program without editing the source code.

Example:

Instead of changing this manually:

```python
channel = 3
signal_type = "RMS"
plot_color = "red"
```

we can let the user select these values with:

* a dropdown
* a button
* a slider
* a checkbox

---

## What is PySide6?

PySide6 is the **official Python binding of Qt**, a powerful cross-platform UI framework.

It provides:

* **Widgets** → UI elements such as buttons, dropdowns, labels and sliders
* **Layouts** → rules for arranging widgets
* **Signals & Slots** → communication between UI elements and Python functions
* **Event loop** → continuously listens for user interaction

---

## Structure of a PySide6 Application

Every PySide6 application has the same core structure.

### 1. Import the required classes

```python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
```

---

### 2. Create the application

```python
app = QApplication(sys.argv)
```

The application object:

* manages the event loop
* receives mouse and keyboard events
* keeps the program alive

---

### 3. Create the main window

```python
window = QMainWindow()
```

This is the **top-level container**.

---

### 4. Add a central widget

```python
central_widget = QWidget()
window.setCentralWidget(central_widget)
```

Important:

* `QMainWindow` cannot directly contain layouts
* everything goes inside a `QWidget`
* the `QWidget` receives the layout

---

### 5. Create a layout

```python
layout = QVBoxLayout()
central_widget.setLayout(layout)
```

---

### 6. Show the window

```python
window.show()
app.exec()
```

`app.exec()` starts the event loop.

---

## Minimal PySide6 App

```python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("My First PySide6 App")
window.resize(600, 400)

central_widget = QWidget()
window.setCentralWidget(central_widget)

layout = QVBoxLayout()
central_widget.setLayout(layout)

label = QLabel("Hello PySide6!")
layout.addWidget(label)

window.show()
app.exec()
```

---

## Layouts in Detail

Layouts control how widgets are arranged.

---

### QVBoxLayout — Vertical Layout

Arranges widgets from top to bottom.

```text
+------------------+
|     Widget 1     |
+------------------+
|     Widget 2     |
+------------------+
|     Widget 3     |
+------------------+
```

```python
layout = QVBoxLayout()
layout.addWidget(widget1)
layout.addWidget(widget2)
layout.addWidget(widget3)
```

Typical use:

* main application structure
* forms
* stacked controls

---

### QHBoxLayout — Horizontal Layout

Arranges widgets side by side.

```text
+-------+-------+-------+
|Widget1|Widget2|Widget3|
+-------+-------+-------+
```

```python
layout = QHBoxLayout()
layout.addWidget(widget1)
layout.addWidget(widget2)
layout.addWidget(widget3)
```

Typical use:

* toolbar rows
* buttons next to each other
* label + input pairs

---

### QGridLayout — Grid Layout

Arranges widgets in rows and columns.

```text
+----------+----------+
| Row 0,0  | Row 0,1  |
+----------+----------+
| Row 1,0  | Row 1,1  |
+----------+----------+
```

```python
from PySide6.QtWidgets import QGridLayout, QLabel, QLineEdit

grid = QGridLayout()

grid.addWidget(QLabel("Name:"), 0, 0)
grid.addWidget(QLineEdit(), 0, 1)

grid.addWidget(QLabel("Age:"), 1, 0)
grid.addWidget(QLineEdit(), 1, 1)
```

Typical use:

* settings dialogs
* forms
* structured input panels

---

### QFormLayout — Form Layout

Best for label-input forms.

```python
from PySide6.QtWidgets import QFormLayout, QLineEdit, QSpinBox

form = QFormLayout()
form.addRow("Patient name:", QLineEdit())
form.addRow("Age:", QSpinBox())
```

Typical use:

* parameter input
* configuration panels
* data entry

---

### Nested Layouts

You can combine layouts.

```text
+------------------------------+
|           Plot Area          |
+------------------------------+
| Channel | Signal | Button    |
+------------------------------+
```

```python
main_layout = QVBoxLayout()
controls_layout = QHBoxLayout()

controls_layout.addWidget(channel_combo)
controls_layout.addWidget(signal_combo)
controls_layout.addWidget(color_button)

main_layout.addLayout(controls_layout)
main_layout.addWidget(plot_widget)
```

Standard pattern:

* vertical layout → overall structure
* horizontal layout → control row
* grid or form layout → parameter input

---

# Widget Gallery

The following examples show common widgets used in real applications.

---

## QLabel — Display Text

```python
label = QLabel("Channel:")
```

Useful for:

* titles
* descriptions
* status text
* labels next to inputs

You can update a label dynamically:

```python
label.setText("New value selected")
```

---

## QPushButton — Button

```python
button = QPushButton("Start")
```

Connect the button to a function:

```python
def start_measurement():
    print("Measurement started")

button.clicked.connect(start_measurement)
```

Useful for:

* starting an action
* stopping an action
* saving data
* resetting a view
* opening a file

---

## QComboBox — Dropdown

```python
combo = QComboBox()
combo.addItems(["Original", "Filtered", "RMS"])
```

Read the selected text:

```python
selected = combo.currentText()
```

React to changes:

```python
def selection_changed():
    print(combo.currentText())

combo.currentIndexChanged.connect(selection_changed)
```

Useful for:

* selecting a channel
* selecting a signal type
* selecting a mode
* selecting a device

---

## QSlider — Slider

```python
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSlider

slider = QSlider(Qt.Horizontal)
slider.setMinimum(0)
slider.setMaximum(100)
slider.setValue(50)
```

React to slider movement:

```python
def slider_changed(value):
    print("Slider value:", value)

slider.valueChanged.connect(slider_changed)
```

Useful for:

* amplitude
* frequency
* filter cutoff
* zoom level
* playback position

---

## QSpinBox — Integer Input

```python
from PySide6.QtWidgets import QSpinBox

spinbox = QSpinBox()
spinbox.setMinimum(1)
spinbox.setMaximum(64)
spinbox.setValue(1)
```

React to value changes:

```python
def channel_changed(value):
    print("Channel:", value)

spinbox.valueChanged.connect(channel_changed)
```

Useful for:

* channel number
* repetitions
* sample index
* count values

---

## QDoubleSpinBox — Decimal Input

```python
from PySide6.QtWidgets import QDoubleSpinBox

cutoff_spinbox = QDoubleSpinBox()
cutoff_spinbox.setMinimum(0.1)
cutoff_spinbox.setMaximum(1000.0)
cutoff_spinbox.setValue(20.0)
cutoff_spinbox.setSuffix(" Hz")
```

Useful for:

* frequency values
* gain
* thresholds
* time constants

---

## QCheckBox — On/Off Option

```python
from PySide6.QtWidgets import QCheckBox

checkbox = QCheckBox("Show grid")
checkbox.setChecked(True)
```

React to changes:

```python
def grid_changed(checked):
    print("Grid enabled:", checked)

checkbox.toggled.connect(grid_changed)
```

Useful for:

* show grid
* enable filter
* normalize signal
* display markers

---

## QRadioButton — Choose One Option

Radio buttons are useful when the user should choose **one option from a small group**.

```python
from PySide6.QtWidgets import QRadioButton, QButtonGroup

radio_raw = QRadioButton("Raw")
radio_filtered = QRadioButton("Filtered")
radio_rms = QRadioButton("RMS")

radio_raw.setChecked(True)

group = QButtonGroup()
group.addButton(radio_raw)
group.addButton(radio_filtered)
group.addButton(radio_rms)
```

Useful for:

* display mode
* acquisition mode
* analysis method

---

## QLineEdit — Single-Line Text Input

```python
from PySide6.QtWidgets import QLineEdit

name_input = QLineEdit()
name_input.setPlaceholderText("Enter participant name")
```

Read the text:

```python
name = name_input.text()
```

React when the user presses Enter:

```python
def name_entered():
    print(name_input.text())

name_input.returnPressed.connect(name_entered)
```

Useful for:

* names
* IDs
* file names
* short parameters

---

## QTextEdit — Multi-Line Text Input

```python
from PySide6.QtWidgets import QTextEdit

notes = QTextEdit()
notes.setPlaceholderText("Write notes here...")
```

Read the text:

```python
text = notes.toPlainText()
```

Useful for:

* comments
* experiment notes
* logs
* descriptions

---

## QListWidget — Simple List

```python
from PySide6.QtWidgets import QListWidget

list_widget = QListWidget()
list_widget.addItems(["Trial 1", "Trial 2", "Trial 3"])
```

React to selection:

```python
def trial_selected():
    item = list_widget.currentItem()
    if item is not None:
        print(item.text())

list_widget.currentItemChanged.connect(trial_selected)
```

Useful for:

* trial lists
* file lists
* selected channels
* measurement sessions

---

## QTableWidget — Table

```python
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

table = QTableWidget()
table.setRowCount(3)
table.setColumnCount(2)
table.setHorizontalHeaderLabels(["Channel", "RMS"])

table.setItem(0, 0, QTableWidgetItem("1"))
table.setItem(0, 1, QTableWidgetItem("0.24"))
```

Useful for:

* measurement results
* channel values
* configuration tables
* summary statistics

---

## QProgressBar — Progress Indicator

```python
from PySide6.QtWidgets import QProgressBar

progress = QProgressBar()
progress.setMinimum(0)
progress.setMaximum(100)
progress.setValue(25)
```

Useful for:

* loading data
* processing signals
* recording progress
* export progress

---

## QTabWidget — Tabs

```python
from PySide6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLabel

tabs = QTabWidget()

page1 = QWidget()
page1_layout = QVBoxLayout()
page1_layout.addWidget(QLabel("Signal view"))
page1.setLayout(page1_layout)

page2 = QWidget()
page2_layout = QVBoxLayout()
page2_layout.addWidget(QLabel("Settings"))
page2.setLayout(page2_layout)

tabs.addTab(page1, "Plot")
tabs.addTab(page2, "Settings")
```

Useful for:

* separating views
* settings pages
* plots vs results
* simple multi-page applications

---

## QMessageBox — Dialog Window

```python
from PySide6.QtWidgets import QMessageBox

QMessageBox.information(window, "Info", "Data saved successfully.")
```

Useful for:

* warnings
* errors
* confirmations
* short feedback

---

## QFileDialog — Open or Save Files

```python
from PySide6.QtWidgets import QFileDialog

filename, _ = QFileDialog.getOpenFileName(
    window,
    "Open File",
    "",
    "CSV Files (*.csv);;All Files (*)"
)

if filename:
    print(filename)
```

Useful for:

* opening CSV files
* loading signal data
* saving results
* exporting plots

---

# Signals and Slots

This is the most important concept in GUI programming.

Instead of calling functions directly:

```python
do_something()
```

we connect events to functions:

```python
button.clicked.connect(do_something)
```

Meaning:

> When this event happens, execute this function.

---

## Signals vs Slots

| Concept | Meaning | Example |
| ------- | ------- | ------- |
| Signal | Something happened | `button.clicked` |
| Slot | Function that reacts | `update_plot` |

---

## Common Signals

| Widget | Common signal | Meaning |
| ------ | ------------- | ------- |
| `QPushButton` | `clicked` | Button was clicked |
| `QComboBox` | `currentIndexChanged` | Selection changed |
| `QSlider` | `valueChanged` | Slider moved |
| `QSpinBox` | `valueChanged` | Number changed |
| `QCheckBox` | `toggled` | Checkbox changed |
| `QLineEdit` | `textChanged` | Text changed |
| `QLineEdit` | `returnPressed` | Enter was pressed |
| `QListWidget` | `currentItemChanged` | Selected item changed |

---

## Multiple Signals Can Trigger the Same Function

```python
channel_combo.currentIndexChanged.connect(update_plot)
signal_combo.currentIndexChanged.connect(update_plot)
amplitude_slider.valueChanged.connect(update_plot)
grid_checkbox.toggled.connect(update_plot)
```

This is powerful because:

* the UI can change in many ways
* the plot update logic is written only once
* the program remains easier to maintain

---

## Important Mental Model

GUI code works like this:

```text
WAIT → EVENT → FUNCTION → UPDATE UI
```

Not like this:

```text
RUN → FINISH
```

---

# Event-Driven Programming

Unlike normal scripts, GUI code does not simply run once from top to bottom.

Instead:

1. the application starts
2. the window appears
3. the program waits
4. the user interacts
5. a signal is emitted
6. a connected function runs
7. the UI updates
8. the program waits again

Examples of events:

* button click
* dropdown change
* slider movement
* checkbox toggle
* text input
* file selection

---

# Integrating Matplotlib into PySide6

Normally, Matplotlib opens its own window.

In this exercise, we embed the plot into the PySide6 application.

```python
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
```

---

## Setup

```python
fig = Figure()
canvas = FigureCanvas(fig)
ax = fig.add_subplot(111)
```

Add the canvas to a layout:

```python
layout.addWidget(canvas)
```

---

## Updating the Plot

```python
ax.clear()
ax.plot(x, y)
canvas.draw()
```

Important:

* `ax.clear()` removes the old plot
* `ax.plot(x, y)` draws the new plot
* `canvas.draw()` updates the visible UI

---

# Mini Examples for Class Demonstration

The following examples are intentionally small. They are useful for live coding before building the full application.

---

## Mini Example 1 — Button Changes Label Text

```python
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Button Example")

layout = QVBoxLayout()
window.setLayout(layout)

label = QLabel("Click the button")
button = QPushButton("Click me")

layout.addWidget(label)
layout.addWidget(button)

def on_button_clicked():
    label.setText("Button was clicked")

button.clicked.connect(on_button_clicked)

window.show()
app.exec()
```

Concepts:

* button
* label update
* signal-slot connection

---

## Mini Example 2 — Dropdown Changes Label Text

```python
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Dropdown Example")

layout = QVBoxLayout()
window.setLayout(layout)

label = QLabel("Select a signal type")
combo = QComboBox()
combo.addItems(["Original", "Filtered", "RMS"])

layout.addWidget(combo)
layout.addWidget(label)

def on_selection_changed():
    label.setText("Selected: " + combo.currentText())

combo.currentIndexChanged.connect(on_selection_changed)

window.show()
app.exec()
```

Concepts:

* dropdown
* selected text
* automatic UI update

---

## Mini Example 3 — Slider Controls a Number

```python
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Slider Example")

layout = QVBoxLayout()
window.setLayout(layout)

label = QLabel("Value: 50")
slider = QSlider(Qt.Horizontal)
slider.setMinimum(0)
slider.setMaximum(100)
slider.setValue(50)

layout.addWidget(label)
layout.addWidget(slider)

def on_slider_changed(value):
    label.setText(f"Value: {value}")

slider.valueChanged.connect(on_slider_changed)

window.show()
app.exec()
```

Concepts:

* slider
* signal with a value argument
* dynamic text update

---

## Mini Example 4 — Checkbox Shows or Hides Text

```python
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QCheckBox

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Checkbox Example")

layout = QVBoxLayout()
window.setLayout(layout)

checkbox = QCheckBox("Show details")
label = QLabel("These are additional details.")
label.setVisible(False)

layout.addWidget(checkbox)
layout.addWidget(label)

def on_checkbox_toggled(checked):
    label.setVisible(checked)

checkbox.toggled.connect(on_checkbox_toggled)

window.show()
app.exec()
```

Concepts:

* checkbox
* boolean state
* showing and hiding widgets

---

## Mini Example 5 — Input Field and Button

```python
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Text Input Example")

layout = QVBoxLayout()
window.setLayout(layout)

input_field = QLineEdit()
input_field.setPlaceholderText("Enter your name")

button = QPushButton("Submit")
label = QLabel("Waiting for input...")

layout.addWidget(input_field)
layout.addWidget(button)
layout.addWidget(label)

def on_submit():
    name = input_field.text()
    label.setText(f"Hello, {name}!")

button.clicked.connect(on_submit)
input_field.returnPressed.connect(on_submit)

window.show()
app.exec()
```

Concepts:

* text input
* button interaction
* Enter key interaction

---

# Full Demo Application — Interactive Signal Viewer

This example combines several UI elements:

* dropdowns
* buttons
* sliders
* checkboxes
* spin boxes
* tabs
* embedded Matplotlib plot
* status label

Students can use this as a reference for what is possible with PySide6.

---

## Complete Example Code

```python
import sys
import numpy as np

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QSlider,
    QCheckBox,
    QSpinBox,
    QDoubleSpinBox,
    QLineEdit,
    QTextEdit,
    QListWidget,
    QTableWidget,
    QTableWidgetItem,
    QProgressBar,
    QTabWidget,
    QMessageBox,
    QFileDialog,
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class SignalViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interactive Signal Viewer")
        self.resize(1100, 750)

        self.colors = ["tab:blue", "tab:red", "tab:green", "tab:orange", "tab:purple"]
        self.color_index = 0

        self.x = np.linspace(0, 2 * np.pi, 1000)

        self.setup_ui()
        self.connect_signals()
        self.update_plot()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.plot_page = QWidget()
        self.settings_page = QWidget()
        self.results_page = QWidget()

        self.tabs.addTab(self.plot_page, "Plot")
        self.tabs.addTab(self.settings_page, "Settings")
        self.tabs.addTab(self.results_page, "Results")

        self.setup_plot_page()
        self.setup_settings_page()
        self.setup_results_page()

    def setup_plot_page(self):
        layout = QVBoxLayout()
        self.plot_page.setLayout(layout)

        controls_layout = QHBoxLayout()

        self.channel_combo = QComboBox()
        self.channel_combo.addItems([f"Channel {i}" for i in range(1, 9)])

        self.signal_combo = QComboBox()
        self.signal_combo.addItems(["Original", "Filtered", "RMS", "Absolute"])

        self.color_button = QPushButton("Change Color")
        self.reset_button = QPushButton("Reset")
        self.info_button = QPushButton("Info")
        self.open_file_button = QPushButton("Open File")

        controls_layout.addWidget(QLabel("Channel:"))
        controls_layout.addWidget(self.channel_combo)
        controls_layout.addWidget(QLabel("Signal:"))
        controls_layout.addWidget(self.signal_combo)
        controls_layout.addWidget(self.color_button)
        controls_layout.addWidget(self.reset_button)
        controls_layout.addWidget(self.info_button)
        controls_layout.addWidget(self.open_file_button)

        layout.addLayout(controls_layout)

        parameter_layout = QHBoxLayout()

        self.amplitude_slider = QSlider(Qt.Horizontal)
        self.amplitude_slider.setMinimum(1)
        self.amplitude_slider.setMaximum(100)
        self.amplitude_slider.setValue(50)

        self.frequency_spinbox = QDoubleSpinBox()
        self.frequency_spinbox.setMinimum(0.1)
        self.frequency_spinbox.setMaximum(20.0)
        self.frequency_spinbox.setValue(1.0)
        self.frequency_spinbox.setSingleStep(0.1)
        self.frequency_spinbox.setSuffix(" Hz")

        self.noise_spinbox = QDoubleSpinBox()
        self.noise_spinbox.setMinimum(0.0)
        self.noise_spinbox.setMaximum(1.0)
        self.noise_spinbox.setValue(0.1)
        self.noise_spinbox.setSingleStep(0.05)

        self.grid_checkbox = QCheckBox("Show grid")
        self.grid_checkbox.setChecked(True)

        self.markers_checkbox = QCheckBox("Show markers")
        self.markers_checkbox.setChecked(False)

        parameter_layout.addWidget(QLabel("Amplitude:"))
        parameter_layout.addWidget(self.amplitude_slider)
        parameter_layout.addWidget(QLabel("Frequency:"))
        parameter_layout.addWidget(self.frequency_spinbox)
        parameter_layout.addWidget(QLabel("Noise:"))
        parameter_layout.addWidget(self.noise_spinbox)
        parameter_layout.addWidget(self.grid_checkbox)
        parameter_layout.addWidget(self.markers_checkbox)

        layout.addLayout(parameter_layout)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        layout.addWidget(self.canvas)

        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

    def setup_settings_page(self):
        layout = QGridLayout()
        self.settings_page.setLayout(layout)

        self.participant_input = QLineEdit()
        self.participant_input.setPlaceholderText("Enter participant name")

        self.trial_spinbox = QSpinBox()
        self.trial_spinbox.setMinimum(1)
        self.trial_spinbox.setMaximum(100)
        self.trial_spinbox.setValue(1)

        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Write experiment notes here...")

        layout.addWidget(QLabel("Participant:"), 0, 0)
        layout.addWidget(self.participant_input, 0, 1)
        layout.addWidget(QLabel("Trial:"), 1, 0)
        layout.addWidget(self.trial_spinbox, 1, 1)
        layout.addWidget(QLabel("Notes:"), 2, 0)
        layout.addWidget(self.notes_edit, 2, 1)

    def setup_results_page(self):
        layout = QVBoxLayout()
        self.results_page.setLayout(layout)

        self.trial_list = QListWidget()
        self.trial_list.addItems(["Trial 1", "Trial 2", "Trial 3"])

        self.results_table = QTableWidget()
        self.results_table.setRowCount(8)
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Channel", "Mean", "RMS"])

        for row in range(8):
            self.results_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self.results_table.setItem(row, 1, QTableWidgetItem("0.00"))
            self.results_table.setItem(row, 2, QTableWidgetItem("0.00"))

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

        layout.addWidget(QLabel("Recorded trials:"))
        layout.addWidget(self.trial_list)
        layout.addWidget(QLabel("Results:"))
        layout.addWidget(self.results_table)
        layout.addWidget(QLabel("Processing progress:"))
        layout.addWidget(self.progress_bar)

    def connect_signals(self):
        self.channel_combo.currentIndexChanged.connect(self.update_plot)
        self.signal_combo.currentIndexChanged.connect(self.update_plot)
        self.amplitude_slider.valueChanged.connect(self.update_plot)
        self.frequency_spinbox.valueChanged.connect(self.update_plot)
        self.noise_spinbox.valueChanged.connect(self.update_plot)
        self.grid_checkbox.toggled.connect(self.update_plot)
        self.markers_checkbox.toggled.connect(self.update_plot)

        self.color_button.clicked.connect(self.change_color)
        self.reset_button.clicked.connect(self.reset_controls)
        self.info_button.clicked.connect(self.show_info)
        self.open_file_button.clicked.connect(self.open_file)

        self.participant_input.textChanged.connect(self.update_status)
        self.trial_spinbox.valueChanged.connect(self.update_status)
        self.trial_list.currentItemChanged.connect(self.trial_selected)

    def generate_signal(self):
        channel = self.channel_combo.currentIndex() + 1
        amplitude = self.amplitude_slider.value() / 50
        frequency = self.frequency_spinbox.value()
        noise_level = self.noise_spinbox.value()

        signal = amplitude * np.sin(frequency * self.x + channel * 0.4)
        noise = noise_level * np.random.randn(len(self.x))
        signal = signal + noise

        signal_type = self.signal_combo.currentText()

        if signal_type == "Filtered":
            kernel = np.ones(25) / 25
            signal = np.convolve(signal, kernel, mode="same")
        elif signal_type == "RMS":
            window_size = 50
            squared = signal ** 2
            kernel = np.ones(window_size) / window_size
            signal = np.sqrt(np.convolve(squared, kernel, mode="same"))
        elif signal_type == "Absolute":
            signal = np.abs(signal)

        return signal

    def update_plot(self):
        y = self.generate_signal()
        color = self.colors[self.color_index]

        self.ax.clear()

        if self.markers_checkbox.isChecked():
            self.ax.plot(self.x, y, color=color, marker="o", markevery=50)
        else:
            self.ax.plot(self.x, y, color=color)

        self.ax.set_title(
            f"{self.channel_combo.currentText()} — {self.signal_combo.currentText()}"
        )
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Amplitude")
        self.ax.grid(self.grid_checkbox.isChecked())

        self.canvas.draw()

        self.update_results_table(y)
        self.status_label.setText(
            f"Updated plot: {self.channel_combo.currentText()}, {self.signal_combo.currentText()}"
        )

    def update_results_table(self, y):
        selected_channel = self.channel_combo.currentIndex()
        mean_value = np.mean(y)
        rms_value = np.sqrt(np.mean(y ** 2))

        self.results_table.setItem(
            selected_channel,
            1,
            QTableWidgetItem(f"{mean_value:.3f}")
        )
        self.results_table.setItem(
            selected_channel,
            2,
            QTableWidgetItem(f"{rms_value:.3f}")
        )

        progress = int((selected_channel + 1) / 8 * 100)
        self.progress_bar.setValue(progress)

    def change_color(self):
        self.color_index = (self.color_index + 1) % len(self.colors)
        self.update_plot()

    def reset_controls(self):
        self.channel_combo.setCurrentIndex(0)
        self.signal_combo.setCurrentIndex(0)
        self.amplitude_slider.setValue(50)
        self.frequency_spinbox.setValue(1.0)
        self.noise_spinbox.setValue(0.1)
        self.grid_checkbox.setChecked(True)
        self.markers_checkbox.setChecked(False)
        self.status_label.setText("Controls reset")
        self.update_plot()

    def show_info(self):
        QMessageBox.information(
            self,
            "About this app",
            "This demo shows common PySide6 widgets and an embedded Matplotlib plot."
        )

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Signal File",
            "",
            "CSV Files (*.csv);;Text Files (*.txt);;All Files (*)"
        )

        if filename:
            self.status_label.setText(f"Selected file: {filename}")

    def update_status(self):
        participant = self.participant_input.text()
        trial = self.trial_spinbox.value()

        if participant:
            self.status_label.setText(f"Participant: {participant}, Trial: {trial}")
        else:
            self.status_label.setText(f"Trial: {trial}")

    def trial_selected(self):
        item = self.trial_list.currentItem()
        if item is not None:
            self.status_label.setText(f"Selected {item.text()}")


app = QApplication(sys.argv)
window = SignalViewer()
window.show()
app.exec()
```

---

# Your Task in This Exercise

You will implement the UI by completing the TODOs.

---

## Basic Task

### 1. Window Setup

* Set the window title
* Set the window size

---

### 2. Central Widget

* Create a `QWidget`
* Assign it using `setCentralWidget()`

---

### 3. Layouts

Create:

* `QVBoxLayout` → main layout
* `QHBoxLayout` → control layout

---

### 4. Channel Selection

Create:

* `QLabel("Channel:")`
* `QComboBox`

Fill the dropdown with:

```text
Channel 1, Channel 2, Channel 3, ...
```

---

### 5. Signal Selection

Create a dropdown with:

```text
Original, Filtered, RMS
```

---

### 6. Button

Create:

```python
QPushButton("Change Color")
```

---

### 7. Layout Assembly

* Add all controls to the horizontal layout
* Add the horizontal layout to the vertical layout

---

### 8. Matplotlib Integration

Create:

* `Figure`
* `FigureCanvas`
* `Axes`

Add the canvas to the layout.

---

### 9. Connect Signals

Connect:

```python
channel_combo.currentIndexChanged.connect(update_plot)
signal_combo.currentIndexChanged.connect(update_plot)
color_button.clicked.connect(change_color)
```

---

### 10. Initial Plot

Call:

```python
update_plot()
```

once at the end of the setup.

---

# Optional Extension Tasks

Students who finish early can add more widgets.

---

## Extension 1 — Add a Slider

Add an amplitude slider:

```python
amplitude_slider = QSlider(Qt.Horizontal)
amplitude_slider.setMinimum(1)
amplitude_slider.setMaximum(100)
amplitude_slider.setValue(50)
```

Connect it to:

```python
amplitude_slider.valueChanged.connect(update_plot)
```

Use the slider value to scale the signal amplitude.

---

## Extension 2 — Add a Checkbox

Add a checkbox:

```python
grid_checkbox = QCheckBox("Show grid")
grid_checkbox.setChecked(True)
```

Connect it to:

```python
grid_checkbox.toggled.connect(update_plot)
```

Use it inside `update_plot()`:

```python
ax.grid(grid_checkbox.isChecked())
```

---

## Extension 3 — Add a Frequency Spin Box

Add:

```python
frequency_spinbox = QDoubleSpinBox()
frequency_spinbox.setMinimum(0.1)
frequency_spinbox.setMaximum(20.0)
frequency_spinbox.setValue(1.0)
frequency_spinbox.setSuffix(" Hz")
```

Use this value to change the plotted signal frequency.

---

## Extension 4 — Add a Reset Button

Add:

```python
reset_button = QPushButton("Reset")
```

Then create:

```python
def reset_controls():
    channel_combo.setCurrentIndex(0)
    signal_combo.setCurrentIndex(0)
    amplitude_slider.setValue(50)
```

Connect:

```python
reset_button.clicked.connect(reset_controls)
```

---

## Extension 5 — Add a Status Label

Add a label at the bottom:

```python
status_label = QLabel("Ready")
```

Update it whenever something changes:

```python
status_label.setText("Plot updated")
```

---

## Extension 6 — Add Tabs

Create tabs for:

* Plot
* Settings
* Results

```python
tabs = QTabWidget()
tabs.addTab(plot_page, "Plot")
tabs.addTab(settings_page, "Settings")
tabs.addTab(results_page, "Results")
```

---

## Extension 7 — Add a Table

Use a table to display calculated values:

* channel number
* mean
* RMS

```python
table = QTableWidget()
table.setRowCount(8)
table.setColumnCount(3)
table.setHorizontalHeaderLabels(["Channel", "Mean", "RMS"])
```

---

## Extension 8 — Add a File Dialog

Add a button that opens a file dialog:

```python
filename, _ = QFileDialog.getOpenFileName(
    window,
    "Open File",
    "",
    "CSV Files (*.csv);;All Files (*)"
)
```

---

# Suggested Teaching Sequence

For a 90-minute lesson:

| Time | Topic |
| ---- | ----- |
| 0–10 min | Why GUI programming? Scripts vs applications |
| 10–20 min | Minimal PySide6 application |
| 20–35 min | Layouts: vertical, horizontal, grid |
| 35–50 min | Buttons, labels, dropdowns, signals and slots |
| 50–65 min | Sliders, checkboxes, spin boxes |
| 65–80 min | Embedded Matplotlib plot |
| 80–90 min | Extension ideas and student experimentation |

For a shorter lesson, focus only on:

1. minimal app
2. layouts
3. button
4. dropdown
5. embedded plot

---

# Common Mistakes

## Mistake 1 — Forgetting `app.exec()`

Without this, the window may open and immediately close.

---

## Mistake 2 — Adding a Layout Directly to `QMainWindow`

Wrong:

```python
window.setLayout(layout)
```

Correct:

```python
central_widget = QWidget()
window.setCentralWidget(central_widget)
central_widget.setLayout(layout)
```

---

## Mistake 3 — Calling the Function Instead of Connecting It

Wrong:

```python
button.clicked.connect(update_plot())
```

Correct:

```python
button.clicked.connect(update_plot)
```

The first version calls the function immediately.
The second version connects the function to the button click.

---

## Mistake 4 — Forgetting `canvas.draw()`

If the plot does not update, check whether you called:

```python
canvas.draw()
```

---

## Mistake 5 — Using Local Variables That Are Needed Later

If a widget is needed in another method, store it as `self.widget_name`.

Example:

```python
self.channel_combo = QComboBox()
```

instead of:

```python
channel_combo = QComboBox()
```

---

# Key Takeaways

* A GUI application stays open and waits for user interaction.
* PySide6 applications are event-driven.
* Widgets are the visible UI elements.
* Layouts define how widgets are arranged.
* Signals and slots connect user actions to Python functions.
* Matplotlib plots can be embedded directly into PySide6 applications.
* Small widgets can be combined into powerful applications.

Most important mental model:

```text
WAIT → EVENT → FUNCTION → UPDATE UI
```
