import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime
import matplotlib.pyplot as plt

DATA_FILE = "bmi_history.csv"

def calculate_bmi():
    try:
        weight = float(entry_weight.get())
        height = float(entry_height.get())
        if weight <= 0 or height <= 0:
            raise ValueError
        bmi = weight / (height ** 2)
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal weight"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"
        label_result.config(text=f"BMI: {bmi:.2f} ({category})", fg="white", bg="#4CAF50", font=("Arial", 14, "bold"))
        save_data(weight, height, bmi, category)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values for weight and height.")

def save_data(weight, height, bmi, category):
    try:
        with open(DATA_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), weight, height, f"{bmi:.2f}", category])
    except Exception as e:
        messagebox.showerror("File Error", f"Failed to save data: {e}")

def show_history():
    timestamps, bmis = [], []
    try:
        with open(DATA_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                timestamps.append(row[0])
                bmis.append(float(row[3]))
        if not bmis:
            messagebox.showinfo("No Data", "No historical data found.")
            return
        plt.figure(figsize=(10,5))
        plt.plot(timestamps, bmis, marker='o', linestyle='-', color='#FF5722')
        plt.xticks(rotation=45, ha='right')
        plt.xlabel("Date/Time")
        plt.ylabel("BMI")
        plt.title("BMI Trend Over Time")
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()
    except FileNotFoundError:
        messagebox.showinfo("No Data", "No historical data found.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {e}")

root = tk.Tk()
root.title("BMI Calculator")
root.configure(bg="#2E3F4F")
root.geometry("400x300")
root.resizable(False, False)

tk.Label(root, text="BMI Calculator", bg="#2E3F4F", fg="white", font=("Helvetica", 18, "bold")).pack(pady=10)

frame_weight = tk.Frame(root, bg="#2E3F4F")
frame_weight.pack(pady=5)
tk.Label(frame_weight, text="Weight (kg):", bg="#2E3F4F", fg="white", font=("Arial", 12)).pack(side="left")
entry_weight = tk.Entry(frame_weight, width=10, font=("Arial", 12))
entry_weight.pack(side="left", padx=5)

frame_height = tk.Frame(root, bg="#2E3F4F")
frame_height.pack(pady=5)
tk.Label(frame_height, text="Height (m):", bg="#2E3F4F", fg="white", font=("Arial", 12)).pack(side="left")
entry_height = tk.Entry(frame_height, width=10, font=("Arial", 12))
entry_height.pack(side="left", padx=5)

tk.Button(root, text="Calculate BMI", command=calculate_bmi, bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=15)

label_result = tk.Label(root, text="", bg="#2E3F4F")
label_result.pack(pady=10)

tk.Button(root, text="Show BMI History", command=show_history, bg="#2196F3", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

root.mainloop()
