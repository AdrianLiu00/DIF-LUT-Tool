import tkinter as tk
from tkinter import ttk
import subprocess
import os

from typing import Callable

config_path = "template/config.ini"
parameter_list = ["Input_bitwidth", "Input_fraction_bitwidth", "Output_bitwidth", "Output_fraction_bitwidth", "Target_Accuracy"]
func_dict = {"Cosine":'cos', "ELU":'elu', "SiLU":'silu', "Sigmoid":'sigmoid', "Sine":'sin', "Tanh":'tanh'}

def gui(runtime:Callable):

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


    # main window
    root = tk.Tk()
    root.title("DIF-LUT-GUI")

    # grid
    combo_label = tk.Label(root, text="Function select:")
    combo_label.grid(row=0, column=0, padx=10, pady=10)

    combo_var = tk.StringVar()
    combobox = ttk.Combobox(root, textvariable=combo_var, width=15)
    combobox['values'] = ("Cosine", "ELU", "SiLU", "Sigmoid", "Sine", "Tanh")
    combobox.grid(row=0, column=1, padx=10, pady=10)

    # scroll bar
    status_frame = tk.Frame(root)
    status_frame.grid(row=0, column=2, rowspan=7, sticky="NSWE", padx=10)

    status_text = tk.Text(status_frame, width=30, height=10, state=tk.DISABLED, wrap=tk.WORD)
    status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(status_frame, command=status_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    status_text.config(yscrollcommand=scrollbar.set)

    # input bar
    entry1_label = tk.Label(root, text=f"Input bitwidth:")     
    entry1_label.grid(row=1, column=0, padx=10, pady=2)
    entry1_var = tk.StringVar()
    entry1 = tk.Entry(root, textvariable=entry1_var, width=20)
    entry1.grid(row=1, column=1, padx=10, pady=2)

    entry2_label = tk.Label(root, text=f"Input fraction bitwidth:")     
    entry2_label.grid(row=2, column=0, padx=10, pady=2)
    entry2_var = tk.StringVar()
    entry2 = tk.Entry(root, textvariable=entry2_var, width=20)
    entry2.grid(row=2, column=1, padx=10, pady=2)

    entry3_label = tk.Label(root, text=f"Output bitwidth:")     
    entry3_label.grid(row=3, column=0, padx=10, pady=2)
    entry3_var = tk.StringVar()
    entry3 = tk.Entry(root, textvariable=entry3_var, width=20)
    entry3.grid(row=3, column=1, padx=10, pady=2)

    entry4_label = tk.Label(root, text=f"Output fraction bitwidth:")     
    entry4_label.grid(row=4, column=0, padx=10, pady=2)
    entry4_var = tk.StringVar()
    entry4 = tk.Entry(root, textvariable=entry4_var, width=20)
    entry4.grid(row=4, column=1, padx=10, pady=2)

    entry5_label = tk.Label(root, text=f"Target Accuracy:")     
    entry5_label.grid(row=5, column=0, padx=10, pady=2)
    entry5_var = tk.StringVar()
    entry5 = tk.Entry(root, textvariable=entry5_var, width=20)
    entry5.grid(row=5, column=1, padx=10, pady=2)

    update_button = tk.Button(root, text="Update parameter", command=update_status)
    update_button.grid(row=6, column=0, padx=10, pady=10)

    run_button = tk.Button(root, text="Generate HDL", command=save_to_file)
    run_button.grid(row=6, column=1, padx=10, pady=10)



    # adaptive window
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)  # adaptive col
    root.grid_rowconfigure(0, weight=1)  # adaptive row

    root.mainloop()
    return