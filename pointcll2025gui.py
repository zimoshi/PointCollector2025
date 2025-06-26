import tkinter as tk
from tkinter import messagebox, simpledialog
from json import load, dump
from typing import Optional
# import matplotlib.pyplot as plt

class Team:
    def __init__(self, name: str):
        self.name = name
        self.points = 0

    def add_points(self, p: int) -> None:
        self.points += p

    def __str__(self) -> str:
        return f"{self.name}: {self.points} points"

teams: dict[str, Team] = {}

graph_win = None
graph_canvas = None

total_popup = None
total_label = None

def update_display(sorted_view: bool = False) -> None:
    output.delete(0, tk.END)
    items = sorted(teams.values(), key=lambda t: t.points, reverse=True) if sorted_view else teams.values()
    for team in items:
        output.insert(tk.END, str(team))

def get_team_name(prompt: str) -> Optional[str]:
    name = simpledialog.askstring(prompt, "Enter team name:")
    return name.strip() if name else None

def get_point_input(prompt: str) -> Optional[int]:
    val = simpledialog.askstring(prompt, "Enter point value:")
    if val is None:
        return None
    try:
        return int(val)
    except ValueError:
        messagebox.showerror("Error", "Invalid point value.")  # type: ignore[attr-defined]
        return None

def add_team() -> None:
    name = get_team_name("Add Team")
    if not name:
        return
    if name in teams:
        messagebox.showinfo("Info", f"Team '{name}' already exists.")  # type: ignore[attr-defined]
    else:
        teams[name] = Team(name)
        update_display()
        update_total_label()
        update_graph_if_open()

def perform_add_points(name: str) -> None:
    p = get_point_input(f"Add Points to {name}")
    if p is not None:
        teams[name].add_points(p)
        update_display()
        update_total_label()
        update_graph_if_open()

def perform_subtract_points(name: str) -> None:
    p = get_point_input(f"Subtract Points from {name}")
    if p is not None:
        if p <= teams[name].points:
            teams[name].add_points(-p)
            update_display()
            update_total_label()
            update_graph_if_open()
        else:
            messagebox.showerror("Error", "Not enough points.")  # type: ignore[attr-defined]

def perform_edit_name(old_name: str) -> None:
    new_name = get_team_name("New Team Name")
    if not new_name:
        return
    if new_name in teams:
        messagebox.showerror("Error", "Team already exists.")  # type: ignore[attr-defined]
        return
    teams[new_name] = teams.pop(old_name)
    teams[new_name].name = new_name
    update_display()
    update_total_label()
    update_graph_if_open()

def perform_delete_team(name: str) -> None:
    del teams[name]
    update_display()
    update_total_label()
    update_graph_if_open()
    messagebox.showinfo("Deleted", f"Team '{name}' deleted.")  # type: ignore[attr-defined]

def show_context_menu(event: tk.Event) -> None:
    widget = event.widget
    index = widget.nearest(event.y) # type: ignore[attr-defined]
    if index < 0 or index >= len(teams):
        return
    widget.selection_clear(0, tk.END) # type: ignore[attr-defined]
    widget.selection_set(index) # type: ignore[attr-defined]
    selected = widget.get(index).split(":")[0] # type: ignore[attr-defined]
    if selected not in teams:
        return

    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Add Points", command=lambda: perform_add_points(selected)) # type: ignore[attr-defined]
    context_menu.add_command(label="Subtract Points", command=lambda: perform_subtract_points(selected)) # type: ignore[attr-defined]
    context_menu.add_command(label="Edit Name", command=lambda: perform_edit_name(selected)) # type: ignore[attr-defined]
    context_menu.add_command(label="Delete Team", command=lambda: perform_delete_team(selected)) # type: ignore[attr-defined]

    # Show menu (platform-safe)
    try:
        context_menu.tk_popup(event.x_root, event.y_root)
    finally:
        context_menu.grab_release()

# def sum_all_points() -> None:
#     total = sum(team.points for team in teams.values())

#     popup = tk.Toplevel(root)
#     popup.title("🎯 Total Points")
#     popup.geometry("300x120")
#     popup.configure(bg="#f0f8ff")  # AliceBlue

#     tk.Label(popup, text="Team Point Total", font=("Helvetica", 14, "bold"), fg="#00cc1b", bg="#f0f8ff").pack(pady=(15, 5))
#     tk.Label(popup, text=f"{total} points 🎉", font=("Helvetica", 20, "bold"), fg="#007acc", bg="#f0f8ff").pack()

#     # # Optional: Auto-close after 3 seconds
#     # popup.after(3000, popup.destroy)

# def update_total_label() -> None:
#     global total_label
#     if total_label:
#         total = sum(team.points for team in teams.values())
#         total_label.config(text=f"{total} points 🎉")

def update_total_label() -> None:
    global total_label, total_popup
    if total_label and total_popup and tk.Toplevel.winfo_exists(total_popup):
        total = sum(team.points for team in teams.values())
        total_label.config(text=f"{total} points 🎉")

def sum_all_points() -> None:
    global total_popup, total_label

    if total_popup and tk.Toplevel.winfo_exists(total_popup):
        return  # Already open

    total_popup = tk.Toplevel(root)
    total_popup.title("🎯 Total Points")
    total_popup.geometry("300x120")
    total_popup.configure(bg="#f0f8ff")

    tk.Label(total_popup, text="Team Point Total", font=("Helvetica", 14, "bold"), fg="#00cc1b", bg="#f0f8ff").pack(pady=(15, 5))

    total_label = tk.Label(total_popup, font=("Helvetica", 20, "bold"), fg="#007acc", bg="#f0f8ff")
    total_label.pack()

    update_total_label()

def save_teams() -> None:
    with open("teams.json", "w") as f:
        dump({name: t.points for name, t in teams.items()}, f)
    messagebox.showinfo("Saved", "Teams saved to 'teams.json'.")  # type: ignore[attr-defined]

def load_teams() -> None:
    try:
        with open("teams.json", "r") as f:
            data = load(f)
            teams.clear()
            for name, points in data.items():
                t = Team(name)
                t.add_points(points)
                teams[name] = t
            update_display()
            update_graph_if_open()
            update_total_label()
    except FileNotFoundError:
        messagebox.showerror("Error", "No save file found.")  # type: ignore[attr-defined]

# def show_graph() -> None:
#     if not teams:
#         messagebox.showinfo("No Data", "No teams to display.")  # type: ignore[attr-defined]
#         return
#     names = [team.name for team in teams.values()]
#     points = [team.points for team in teams.values()]
    
#     plt.figure(figsize=(8, 5)) # type: ignore[attr-defined]
#     plt.bar(names, points, color='skyblue') # type: ignore[attr-defined]
#     plt.xlabel("Teams") # type: ignore[attr-defined]
#     plt.ylabel("Points") # type: ignore[attr-defined]
#     plt.title("Team Points Overview") # type: ignore[attr-defined]
#     plt.xticks(rotation=45) # type: ignore[attr-defined]
#     plt.tight_layout() # type: ignore[attr-defined]
#     plt.show() # type: ignore[attr-defined]

def animate_bar(canvas, x0, y1, x1, target_y0, steps=20, delay=20): # type: ignore[attr-defined]
    def grow(step=0): # type: ignore[attr-defined]
        current_y0 = y1 - ((step / steps) * (y1 - target_y0)) # type: ignore[attr-defined]
        canvas.coords(bar_id, x0, current_y0, x1, y1) # type: ignore[attr-defined]
        if step < steps:
            canvas.after(delay, grow, step + 1) # type: ignore[attr-defined]

    bar_id = canvas.create_rectangle(x0, y1, x1, y1, fill="skyblue", outline="black") # type: ignore[attr-defined]
    grow()

# def show_graph_canvas() -> None:
#     if not teams:
#         messagebox.showinfo("No Data", "No teams to display.")  # type: ignore[attr-defined]
#         return

#     graph_win = tk.Toplevel(root)
#     graph_win.title("Team Points Graph")

#     width, height = 640, 360
#     canvas = tk.Canvas(graph_win, width=width, height=height, bg="white")
#     canvas.pack()

#     names = list(teams.keys())
#     points = [teams[n].points for n in names]
#     max_points = max(points) if points else 1

#     # Title
#     canvas.create_text(width // 2, 20, text="📊 Team Points Overview",
#                     font=("Helvetica", 16, "bold"), fill="black")

#     # Y-axis label
#     canvas.create_text(20, height // 2, text="Points", angle=90,
#                     font=("Helvetica", 10), fill="black")

#     # X-axis label
#     canvas.create_text(width // 2, height - 10, text="Teams",
#                     font=("Helvetica", 10), fill="black")

#     # Draw bars
#     bar_width = 40
#     spacing = 20
#     start_x = 60
#     bar_bottom = height - 40
#     bar_max_height = 200

#     for i, (name, value) in enumerate(zip(names, points)):
#         x0 = start_x + i * (bar_width + spacing)
#         x1 = x0 + bar_width
#         y1 = bar_bottom
#         y0 = y1 - (value / max_points * bar_max_height)

#         animate_bar(canvas, x0, y1, x1, y0)
#         canvas.create_text((x0 + x1) // 2, y1 + 10, text=name,
#                         anchor="n", font=("Helvetica", 9), fill="black")
#         canvas.create_text((x0 + x1) // 2, y0 - 10, text=str(value),
#                         anchor="s", font=("Helvetica", 9), fill="black")

def draw_bars_animated(canvas: tk.Canvas) -> None:
    names = list(teams.keys())
    points = [teams[n].points for n in names]
    max_points = max(points) if points else 1

    width, height = 640, 360
    canvas_height = height - 40
    bar_width = 40
    spacing = 20
    start_x = 60
    bar_max_height = 200

    # Title and axis
    canvas.create_text(width // 2, 20, text="📊 Team Points Overview", font=("Helvetica", 16, "bold"), fill="black")
    canvas.create_text(20, height // 2, text="Points", angle=90, font=("Helvetica", 10), fill="black")
    canvas.create_text(width // 2, height - 10, text="Teams", font=("Helvetica", 10), fill="black")

    for i, (name, value) in enumerate(zip(names, points)):
        x0 = start_x + i * (bar_width + spacing)
        x1 = x0 + bar_width
        y1 = canvas_height
        y0 = y1 - (value / max_points * bar_max_height)

        # Animate each bar
        animate_bar(canvas, x0, y1, x1, y0)

        # Static labels
        canvas.create_text((x0 + x1) // 2, y1 + 10, text=name, anchor="n", font=("Helvetica", 9), fill="black")
        canvas.create_text((x0 + x1) // 2, y0 - 10, text=str(value), anchor="s", font=("Helvetica", 9), fill="black")

def update_graph_if_open() -> None:
    if graph_win and tk.Toplevel.winfo_exists(graph_win):
        graph_canvas.delete("all") # type: ignore[attr-defined]
        draw_bars_animated(graph_canvas) # type: ignore[attr-defined]

# def show_graph_canvas() -> None:
#     global graph_win, graph_canvas
#     if not teams:
#         messagebox.showinfo("No Data", "No teams to display.")  # type: ignore[attr-defined]
#         return
    
#     if graph_win and tk.Toplevel.winfo_exists(graph_win):
#         if graph_win and tk.Toplevel.winfo_exists(graph_win):
#             graph_canvas.delete("all")  # type: ignore[attr-defined] Reuse canvas
#         else:
#             graph_win = tk.Toplevel(root)
#             graph_win.title("Team Points Graph")
#             graph_canvas = tk.Canvas(graph_win, width=640, height=360, bg="white")
#             graph_canvas.pack()

#         draw_bars_animated(graph_canvas) # type: ignore[attr-defined]

def show_graph_canvas() -> None:
    global graph_win, graph_canvas
    if not teams:
        return

    if graph_win and tk.Toplevel.winfo_exists(graph_win):
        graph_canvas.delete("all")  # type: ignore[attr-defined] Reuse existing canvas
    else:
        graph_win = tk.Toplevel(root)
        graph_win.title("Team Points Graph")
        graph_canvas = tk.Canvas(graph_win, width=640, height=360, bg="white")
        graph_canvas.pack()

    draw_bars_animated(graph_canvas) # type: ignore[attr-defined]

# GUI Setup
root = tk.Tk()
root.title("PointCollector 2025")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Button(frame, text="Add Team", width=15, command=add_team).grid(row=0, column=0)
tk.Button(frame, text="Save", width=15, command=save_teams).grid(row=0, column=1)
tk.Button(frame, text="Load", width=15, command=load_teams).grid(row=0, column=2)
tk.Button(frame, text="Sort by Points", width=15, command=lambda: update_display(True)).grid(row=0, column=3)
tk.Button(frame, text="Show Graph", width=15, command=show_graph_canvas).grid(row=0, column=4)
tk.Button(frame, text="Sum Points", width=15, command=sum_all_points).grid(row=0, column=5)

output = tk.Listbox(root, width=50, height=15)
output.pack(pady=10)

# Right-click / Ctrl+Click (macOS compatible)
import platform

if platform.system() == "Darwin":
    output.bind("<Button-2>", show_context_menu)  # macOS
    output.bind("<Control-Button-1>", show_context_menu)  # macOS ctrl+click
else:
    output.bind("<Button-3>", show_context_menu)  # Windows/Linux


root.mainloop()
