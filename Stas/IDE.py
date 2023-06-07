from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.scrolledtext import ScrolledText

class IDE:
    def __init__(self):
        self.root = Tk()

        self.root.geometry("800x600")
        self.root.title("Python IDE with PyCharm functionality")

        self.text_editor = ScrolledText(self.root, bg='white')
        self.text_editor.pack(fill=BOTH, expand=True)

        self.run_button = Button(self.root, text="Run", command=self.run_code)
        self.run_button.pack(side=LEFT)

        self.clear_button = Button(self.root, text="Clear", command=self.clear_code)
        self.clear_button.pack(side=LEFT)

        self.open_button = Button(self.root, text="Open", command=self.open_file)
        self.open_button.pack(side=LEFT)

        self.save_button = Button(self.root, text="Save", command=self.save_file)
        self.save_button.pack(side=LEFT)

        self.console = ScrolledText(self.root, bg="black", fg="white")
        self.console.pack(fill=BOTH, expand=True)

        self.input_frame = Frame(self.root)
        self.input_frame.pack(fill=X, side=BOTTOM)

        self.input = Entry(self.input_frame)
        self.input.pack(side=LEFT, fill=X, expand=True)

        self.send_button = Button(self.input_frame, text="Send", command=self.handle_input)
        self.send_button.pack(side=RIGHT)

        self.root.mainloop()

    def run_code(self):
        code = self.text_editor.get('1.0', END)
        exec(code)
    
    def clear_code(self):
        self.text_editor.delete('1.0', END)

    def open_file(self):
        file_name = askopenfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_name:
            self.text_editor.delete('1.0', END)
            with open(file_name, 'r') as f:
                self.text_editor.insert('1.0', f.read())

    def save_file(self):
        file_name = asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_name:
            with open(file_name, 'w') as f:
                f.write(self.text_editor.get('1.0', END))

    def handle_input(self):
        command = self.input.get()
        console_output = exec(command)
        self.console.insert(END, f"\n{command}\n{console_output}\n")

IDE()