import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import time
import AdaptiveSystem
import Ontology

# Define global variables
input_text = None
output_text = None
triples_text = None
improvements_text = None
run_button = None
outputAQG = ""

class AdaptiveSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Adaptive System GUI")
        self.root.geometry("800x600")  # Initial size of the window

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.show_input_and_learner_ability_page()
        self.show_triples_page()
        self.show_improvements_page()

    def show_input_and_learner_ability_page(self):
        input_frame = ttk.Frame(self.notebook)
        self.notebook.add(input_frame, text="Input and Learner Ability")

        input_label = tk.Label(input_frame, text="Input Array:")
        input_label.pack(anchor="w")

        self.input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.NONE, height=10)
        self.input_text.pack(fill=tk.BOTH, expand=True)

        self.output_text = scrolledtext.ScrolledText(input_frame, wrap=tk.NONE, font=("Arial", 12))
        self.output_text.pack(fill=tk.BOTH, expand=True)

        load_button = tk.Button(input_frame, text="Load Array File", command=self.load_array_file, font=("Arial", 12))
        load_button.pack(side=tk.LEFT, padx=5, pady=10)

        self.run_button = tk.Button(input_frame, text="Run Adaptive System", command=self.run_adaptive_system, font=("Arial", 12), state=tk.DISABLED)
        self.run_button.pack(side=tk.LEFT, padx=5, pady=10)

        triples_button = tk.Button(input_frame, text="Triples", command=self.show_triples_page, font=("Arial", 12))
        triples_button.pack(side=tk.LEFT, padx=5, pady=10)

        improvements_button = tk.Button(input_frame, text="Improvements", command=self.show_improvements_page, font=("Arial", 12))
        improvements_button.pack(side=tk.LEFT, padx=5, pady=10)

        self.input_text.bind("<Key>", lambda event: self.update_run_button_state())

    def button_pressed():
        global is_button_pressed
        is_button_pressed = True
        print("Button Pressed")

    def show_triples_page(self):
        triples_frame = ttk.Frame(self.notebook)
        self.notebook.add(triples_frame, text="Triples")

        self.triples_text = scrolledtext.ScrolledText(triples_frame, wrap=tk.NONE, font=("Arial", 12))
        self.triples_text.pack(fill=tk.BOTH, expand=True)

        self.update_triples_text()
    
    def update_triples_text(self):
        # Simulated triples data
        global outputAQG
        triples_output = AdaptiveSystem.getTriples(outputAQG)
        self.triples_text.delete("1.0", tk.END)
        self.triples_text.insert(tk.END, triples_output)

    def show_improvements_page(self):
        improvements_frame = ttk.Frame(self.notebook)
        self.notebook.add(improvements_frame, text="Improvements per Class")

        self.improvements_text = scrolledtext.ScrolledText(improvements_frame, wrap=tk.NONE, font=("Arial", 12))
        self.improvements_text.pack(fill=tk.BOTH, expand=True)

        self.update_improvements_text()

    def run_adaptive_system(self):
        def start_animation():
            for _ in range(5):
                self.output_text.insert(tk.END, ".")
                time.sleep(0.5)

        def adaptive_system(input_str):
            try:
                global outputAQG
                # Parse the input string into a list of lists (simulated)
                outputAQG = eval(input_str)

                testResults = AdaptiveSystem.assessment_unit(outputAQG)
                learnerAbilities = AdaptiveSystem.IRT_unit(testResults)


                learnerAbility_ontology = AdaptiveSystem.getLearnerAbilityOntology()

                # Update the dictionary by calling the method in UpdateOntology
                Ontology.updateDict(learnerAbilities)
                # Simulated AdaptiveSystem function (code from AdaptiveSystem.py)

                # Simulated triples and improvements
                #triples_output = AdaptiveSystem.getTriples(outputAQG)
                improvements_output = AdaptiveSystem.calculateImprovment(learnerAbility_ontology)

                # Update the output text
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, "-"*10 + " RESULTS " + "-"*10 + "\n")
                self.output_text.insert(tk.END, "Learning ability {-2,2} of student for concepts:\n")
                self.output_text.insert(tk.END, str(learnerAbilities) + "\n\n")
                self.output_text.insert(tk.END, "-"*10 + " Triples " + "-"*10 + "\n")
                #self.output_text.insert(tk.END, triples_output + "\n")
                self.output_text.insert(tk.END, "-"*10 + " Improvements per Class " + "-"*10 + "\n")
                self.output_text.insert(tk.END, improvements_output + "\n")

            except Exception as e:
                messagebox.showerror("Error", str(e))

        t1 = threading.Thread(target=start_animation)
        t2 = threading.Thread(target=adaptive_system, args=(self.input_text.get("1.0", tk.END),))

        t1.start()
        t2.start()

    def update_run_button_state(self):
        if self.input_text.get("1.0", tk.END).strip():
            self.run_button.config(state=tk.NORMAL)
        else:
            self.run_button.config(state=tk.DISABLED)

    def load_array_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                input_data = file.read()
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(tk.END, input_data)
                self.update_run_button_state()

    

    def update_improvements_text(self):
        # Simulated improvements data
        improvements_output = "Improvements data goes here"
        self.improvements_text.delete("1.0", tk.END)
        self.improvements_text.insert(tk.END, improvements_output)

def main():
    root = tk.Tk()
    app = AdaptiveSystemApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

