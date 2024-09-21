import tkinter as tk
from tkinter import ttk
import subprocess
import os

from typing import Callable

config_path = "template/config.ini"
parameter_list = ["Input_bitwidth", "Input_fraction_bitwidth", "Output_bitwidth", "Output_fraction_bitwidth", "Target_Accuracy"]
func_dict = {"Cosine": 'cos', "ELU": 'elu', "GELU": 'gelu', "SiLU": 'silu', "Sigmoid": 'sigmoid', "Sine": 'sin', "Tanh": 'tanh'}

def gui(runtime: Callable):

    def save_to_file():
        # input verified (int for the first four, float for the last one)
        errors = []
        input_values = [entry1_var.get(), entry2_var.get(), entry3_var.get(), entry4_var.get(), entry5_var.get()]
        for i, value in enumerate(input_values[:4]):
            try:
                int(value)
            except ValueError:
                errors.append(f"The type of {parameter_list[i]} is wrong, int only.")
        
        try:
            float(input_values[4])
        except ValueError:
            errors.append(f"The type of {parameter_list[4]} is wrong, float only.")

        if combo_var.get() in ["Cosine", "Sine"]:
            input_bitwidth = int(entry1_var.get())
            input_fraction_bitwidth = int(entry2_var.get())
            if (input_bitwidth - input_fraction_bitwidth) > 2:
                errors.append("For Cosine and Sine, (Input bitwidth - Input fraction bitwidth) must be <= 2.")

        if errors:
            # print error message
            status_text.config(state=tk.NORMAL)
            status_text.delete(1.0, tk.END)
            status_text.insert(tk.END, "Error: " + "; ".join(errors))
            status_text.config(state=tk.DISABLED)
        else:
            # save file
            with open(config_path, "w") as file:
                file.write("[Para]\n")
                file.write("Func = " + func_dict[combo_var.get()] + "\n")
                for i, value in enumerate(input_values):
                    file.write(f"{parameter_list[i]} = {value}\n")
                file.write(f"visualize = {1 if visualize_var.get() else 0}\n")
                if customize_key_var.get():
                    file.write(f"Customize_Key_Bit = {entry6_var.get()}\n")
                if customize_word_var.get():
                    file.write(f"Customize_Word_Bit = {entry7_var.get()}\n")

            status_text.config(state=tk.NORMAL)
            status_text.delete(1.0, tk.END)
            status_text.insert(tk.END, "Successful Configuration!\n")
            status_text.config(state=tk.DISABLED)

            # run target python file
            try:
                status_text.config(state=tk.NORMAL)
                status_text.insert(tk.END, "-----------------------\n")
                status_text.insert(tk.END, "Run DIF-LUT Tools...\n")
                # subprocess.run(["python", 'execute.py'], check=True)
                runtime(config_path)
                status_text.insert(tk.END, "Done, check the output!")
                status_text.config(state=tk.DISABLED)
            except subprocess.CalledProcessError as e:
                status_text.config(state=tk.NORMAL)
                status_text.insert(tk.END, "-----------------------\n")
                status_text.insert(tk.END, f"\nFailed to run:\n    {e}")
                status_text.config(state=tk.DISABLED)


    def update_status(*args):
        # function update
        status_text.config(state=tk.NORMAL)
        status_text.delete(1.0, tk.END)
        status_text.insert(tk.END, "Parameters are updated")
        status_text.config(state=tk.DISABLED)
        return

    def toggle_entry6():
        if customize_key_var.get():
            entry6.config(state=tk.NORMAL)
        else:
            entry6_var.set("")
            entry6.config(state=tk.DISABLED)
    
    def toggle_entry7():
        if customize_word_var.get():
            entry7.config(state=tk.NORMAL)
        else:
            entry7_var.set("")
            entry7.config(state=tk.DISABLED)

    # main window
    root = tk.Tk()
    root.title("DIF-LUT-GUI")

    # grid
    combo_label = tk.Label(root, text="Function select:")
    combo_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    combo_var = tk.StringVar()
    combobox = ttk.Combobox(root, textvariable=combo_var, width=15)
    combobox['values'] = ("Cosine", "ELU", "GELU", "SiLU", "Sigmoid", "Sine", "Tanh")
    combobox.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    # scroll bar
    status_frame = tk.Frame(root)
    status_frame.grid(row=0, column=2, rowspan=13, sticky="NSWE", padx=10)

    status_text = tk.Text(status_frame, width=30, height=10, state=tk.DISABLED, wrap=tk.WORD)
    status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(status_frame, command=status_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    status_text.config(yscrollcommand=scrollbar.set)

    # input bar
    entry1_label = tk.Label(root, text=f"Input bitwidth:")     
    entry1_label.grid(row=1, column=0, padx=10, pady=2, sticky="e")
    entry1_var = tk.StringVar()
    entry1 = tk.Entry(root, textvariable=entry1_var, width=20)
    entry1.grid(row=1, column=1, padx=10, pady=2)

    entry2_label = tk.Label(root, text=f"Input fraction bitwidth:")     
    entry2_label.grid(row=2, column=0, padx=10, pady=2, sticky="e")
    entry2_var = tk.StringVar()
    entry2 = tk.Entry(root, textvariable=entry2_var, width=20)
    entry2.grid(row=2, column=1, padx=10, pady=2)

    entry3_label = tk.Label(root, text=f"Output bitwidth:")     
    entry3_label.grid(row=3, column=0, padx=10, pady=2, sticky="e")
    entry3_var = tk.StringVar()
    entry3 = tk.Entry(root, textvariable=entry3_var, width=20)
    entry3.grid(row=3, column=1, padx=10, pady=2)

    entry4_label = tk.Label(root, text=f"Output fraction bitwidth:")     
    entry4_label.grid(row=4, column=0, padx=10, pady=2, sticky="e")
    entry4_var = tk.StringVar()
    entry4 = tk.Entry(root, textvariable=entry4_var, width=20)
    entry4.grid(row=4, column=1, padx=10, pady=2)

    entry5_label = tk.Label(root, text=f"Target Accuracy:")     
    entry5_label.grid(row=5, column=0, padx=10, pady=2, sticky="e")
    entry5_var = tk.StringVar()
    entry5 = tk.Entry(root, textvariable=entry5_var, width=20)
    entry5.grid(row=5, column=1, padx=10, pady=2)

    # custom boxes
    customize_key_var = tk.BooleanVar()
    customize_key_check = tk.Checkbutton(root, text="Custom Key Bit:", variable=customize_key_var, command=toggle_entry6)
    customize_key_check.grid(row=6, column=0, padx=10, pady=2, sticky="w")
    entry6_var = tk.StringVar()
    entry6 = tk.Entry(root, textvariable=entry6_var, width=20, state=tk.DISABLED)
    entry6.grid(row=6, column=1, padx=10, pady=2)

    customize_word_var = tk.BooleanVar()
    customize_word_check = tk.Checkbutton(root, text="Custom Word Bit:", variable=customize_word_var, command=toggle_entry7)
    customize_word_check.grid(row=7, column=0, padx=10, pady=2, sticky="w")
    entry7_var = tk.StringVar()
    entry7 = tk.Entry(root, textvariable=entry7_var, width=20, state=tk.DISABLED)
    entry7.grid(row=7, column=1, padx=10, pady=2)

    visualize_var = tk.BooleanVar()
    visualize_check = tk.Checkbutton(root, text="Visualize", variable=visualize_var)
    visualize_check.grid(row=8, column=0, padx=10, pady=2, sticky="w")

    update_button = tk.Button(root, text="Update parameter", command=update_status)
    update_button.grid(row=9, column=0, padx=10, pady=10)

    run_button = tk.Button(root, text="Generate HDL", command=save_to_file)
    run_button.grid(row=9, column=1, padx=10, pady=10)

    # adaptive window
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)  # adaptive col
    root.grid_rowconfigure(0, weight=1)  # adaptive row

    root.mainloop()
    return


def example_runtime(config_path):
    print(f"Configuration saved to {config_path}")
    print("Running the process...")


if __name__ == '__main__':
    # Call the GUI function with the example runtime function
    gui(example_runtime)