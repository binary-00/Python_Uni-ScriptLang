import tkinter as tk
import tkinter.simpledialog as sd
import sqlite3
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Connect to the SQLite database
conn = sqlite3.connect("data.db")
c = conn.cursor()

# Query the database for all questions
c.execute("SELECT DISTINCT response FROM data")
rows = c.fetchall()
questions = [row[0] for row in rows]

# Create the main window
root = tk.Tk()
root.title("Questions")

# Prompt the user for their name
name = sd.askstring("Name", "Enter your name:")

# Create the greeting label
greeting_label = tk.Label(root, text="Hello " + name, font=("Arial", 24))
greeting_label.pack(side=tk.TOP, anchor=tk.W)

# Create the history frame
history_frame = tk.Frame(root)
history_frame.pack(side=tk.RIGHT, fill=tk.Y)

# Create the history label
history_label = tk.Label(history_frame, text="History", font=("Arial", 18))
history_label.pack(side=tk.TOP)

# Create the history listbox
history_listbox = tk.Listbox(history_frame)
history_listbox.pack(side=tk.TOP, fill=tk.Y, expand=True)

# Create the history scrollbar
history_scrollbar = tk.Scrollbar(history_frame, command=history_listbox.yview)
history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
history_listbox["yscrollcommand"] = history_scrollbar.set

# Function to handle history clicks
def handle_history(event):
    # Get the selected answer
    index = history_listbox.curselection()[0]
    answer = history_listbox.get(index)

    # Get the question number
    question_number = int(answer.split(".")[0])

    # Get the question and answer from the database
    c.execute(
        "SELECT context, knowledge FROM data WHERE response = ?",
        (questions[question_number - 1],),
    )
    row = c.fetchone()
    situation = row[0]
    comment = row[1]

    # Display the situation and comment
    messagebox.showinfo("Details", "Situation: " + situation + "\nComment: " + comment)


# Bind the double-click event to the handle_history function
history_listbox.bind("<Double-Button-1>", handle_history)

# Create the questions frame
questions_frame = tk.Frame(root)
questions_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Function to update the questions frame
def update_questions(start):
    # Clear the questions frame
    for widget in questions_frame.winfo_children():
        widget.destroy()

    # Display 10 questions starting from the given index
    for i in range(start, min(start + 10, len(questions))):
        question_number = i + 1
        question_text = str(question_number) + ". " + questions[i]

        # Check if the response ends with a question mark
        if question_text.endswith("?"):
            # Create the question button
            button = tk.Button(
                questions_frame,
                text=question_text,
                command=lambda q=question_number: handle_question(q),
            )
            button.pack(fill=tk.X)

    # Create the navigation buttons
    if start > 0:
        prev_button = tk.Button(
            questions_frame, text="<", command=lambda: update_questions(start - 10)
        )
        prev_button.pack(side=tk.LEFT)
    if start + 10 < len(questions):
        next_button = tk.Button(
            questions_frame, text=">", command=lambda: update_questions(start + 10)
        )
        next_button.pack(side=tk.RIGHT)


# Function to handle question clicks
def handle_question(question_number):
    # Prompt the user for their answer
    answer = sd.askstring("Answer", "Your answer:")

    # Check if the user entered an answer
    if answer is not None:
        # Add the answer to the history listbox
        history_listbox.insert(tk.END, str(question_number) + ". " + answer)

        # Update status line
        status_line["text"] = f"Answered question {question_number}"


# Update the questions frame with the first 10 questions
update_questions(0)


def show_average_response_length():
    c.execute("SELECT AVG(LENGTH(Response)) FROM data")
    avg_length = c.fetchone()[0]
    messagebox.showinfo(
        "Average Response Length",
        f"The average response length is {avg_length:.2f} characters.",
    )


avg_button = tk.Button(
    root, text="Show Average Response Length", command=show_average_response_length
)
avg_button.pack(side=tk.BOTTOM)


def show_knowledge_chart():
    # Query the database for the number of responses for each unique value in the Knowledge column
    c.execute("SELECT Knowledge, COUNT(*) FROM data GROUP BY Knowledge")
    rows = c.fetchall()
    knowledge = [row[0] for row in rows]
    counts = [row[1] for row in rows]

    # Create a new window to display the chart
    chart_window = tk.Toplevel(root)
    chart_window.title("Knowledge Chart")

    # Create the chart
    fig = plt.Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(knowledge, counts)
    ax.set_xlabel("Knowledge")
    ax.set_ylabel("Number of Responses")

    # Display the chart in the new window
    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack()


chart_button = tk.Button(
    root, text="Show Knowledge Chart", command=show_knowledge_chart
)
chart_button.pack(side=tk.BOTTOM)

# Create the status line
status_line = tk.Label(root, text="", font=("Arial", 12))
status_line.pack(side=tk.BOTTOM)

# Create the show database button
def show_database():
    # Retrieve all the data from the database
    c.execute("SELECT * FROM data")
    rows = c.fetchall()

    # Create a new window to display the database content
    db_window = tk.Toplevel(root)
    db_window.title("Database Content")

    # Create a text widget to display the content
    text_widget = tk.Text(db_window, font=("Arial", 12))
    text_widget.pack()

    # Insert the content into the text widget
    for row in rows:
        text_widget.insert(
            tk.END,
            f"Question: {row[0]}\nContext: {row[1]}\nKnowledge: {row[2]}\nResponse: {row[3]}\n\n",
        )


# Create the show database button
show_database_button = tk.Button(root, text="Show Database", command=show_database)
show_database_button.pack(side=tk.BOTTOM)

# Create the exit button
exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.pack(side=tk.BOTTOM)

# Run the main loop
root.mainloop()

# Close the database connection
conn.close()
