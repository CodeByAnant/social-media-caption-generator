import tkinter as tk
from tkinter import scrolledtext, messagebox
from main import generate_social_media_post  # Replace with your actual Python file name (without .py)

def generate_post():
    topic = topic_entry.get()
    keywords = keywords_entry.get()
    
    if not topic.strip():
        messagebox.showerror("Error", "Please enter a topic.")
        return

    result = generate_social_media_post(topic, keywords)

    if result:
        output_box.config(state='normal')
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, result["post_text"] + "\n\n" + " ".join(result["hashtags"]))
        output_box.config(state='disabled')
    else:
        messagebox.showerror("Error", "Failed to generate post. Check API or try again.")

# Create GUI window
window = tk.Tk()
window.title("AI Social Media Post Generator")
window.geometry("600x500")
window.resizable(False, False)

# Input Fields
tk.Label(window, text="Topic:").pack(pady=(10, 0))
topic_entry = tk.Entry(window, width=60)
topic_entry.pack(pady=(0, 10))

tk.Label(window, text="Keywords (optional):").pack()
keywords_entry = tk.Entry(window, width=60)
keywords_entry.pack(pady=(0, 10))

# Generate Button
tk.Button(window, text="Generate Post", command=generate_post, bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=10)

# Output Box
tk.Label(window, text="Generated Post:").pack()
output_box = scrolledtext.ScrolledText(window, width=70, height=15, wrap=tk.WORD)
output_box.pack(pady=10)
output_box.config(state='disabled')

window.mainloop()