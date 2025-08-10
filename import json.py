import json
import os
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox

FILENAME = "plant_data.json"

plants_template = {
    "cactus": {"water_days": 7, "fertilize_days": 30, "last_watered": None, "last_fertilized": None},
    "fern": {"water_days": 3, "fertilize_days": 15, "last_watered": None, "last_fertilized": None},
    "aloe vera": {"water_days": 14, "fertilize_days": 45, "last_watered": None, "last_fertilized": None}
}

# Load plant data
def load_data():
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, 'r') as f:
                data = json.load(f)
                # Ensure all plants exist
                for plant, defaults in plants_template.items():
                    if plant not in data:
                        data[plant] = defaults.copy()
                return data
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Data file is corrupted. Resetting data.")
            return plants_template.copy()
    else:
        return plants_template.copy()

# Save plant data
def save_data(data):
    with open(FILENAME, 'w') as f:
        json.dump(data, f, indent=4)

# Update watering/fertilizing
def update_plant(plant, action):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if action == "water":
        plant_data[plant]["last_watered"] = now
    elif action == "fertilize":
        plant_data[plant]["last_fertilized"] = now
    save_data(plant_data)
    refresh_status()
    messagebox.showinfo("Success", f"{plant.capitalize()} has been {action}ed!")

# Refresh status labels
def refresh_status():
    for plant, info in plant_data.items():
        watered_text = info["last_watered"] if info["last_watered"] else "Never"
        fertilized_text = info["last_fertilized"] if info["last_fertilized"] else "Never"
        plant_labels[plant].config(
            text=f"{plant.capitalize()} → Last Watered: {watered_text}, Last Fertilized: {fertilized_text}"
        )

# GUI
root = tk.Tk()
root.title("Virtual Plant Caretaker")
root.geometry("500x400")
root.config(bg="#e6ffe6")

plant_data = load_data()
plant_labels = {}

for i, plant in enumerate(plant_data):
    tk.Label(root, text=plant.capitalize(), font=("Arial", 14, "bold"), bg="#e6ffe6").grid(row=i*2, column=0, pady=5)

    plant_labels[plant] = tk.Label(root, text="", font=("Arial", 10), bg="#e6ffe6")
    plant_labels[plant].grid(row=i*2, column=1, columnspan=2, pady=5)

    tk.Button(root, text="Water", command=lambda p=plant: update_plant(p, "water")).grid(row=i*2+1, column=0, padx=5)
    tk.Button(root, text="Fertilize", command=lambda p=plant: update_plant(p, "fertilize")).grid(row=i*2+1, column=1, padx=5)

refresh_status()
root.mainloop()
