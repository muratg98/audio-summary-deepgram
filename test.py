import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Sample data for the table
data = [
    ["Symptoms", "Start Date", "End Date", "Duration", "Additional Information"]
]


def display_table():
    # Create a new Tkinter window
    root = tk.Tk()
    root.title("Table Display")

    # Create a Matplotlib figure and axis
    fig = Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)

    # Hide the axis
    ax.axis('off')

    # Plot the table
    ax.table(cellText=data, loc='center')

    # Create a canvas to display the figure
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    root.mainloop()

# Call the function to display the table
display_table()