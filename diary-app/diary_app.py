import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime

class DiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My Diary - Journal App")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Data file to store diary entries
        self.data_file = "diary_entries.json"
        self.entries = self.load_entries()
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
        self.refresh_entries_list()
    
    def setup_ui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Left panel for entries list
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, rowspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)
        
        # Entries list label
        ttk.Label(left_frame, text="Previous Entries", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Listbox for entries with scrollbar
        list_frame = ttk.Frame(left_frame)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        self.entries_listbox = tk.Listbox(list_frame, width=25, font=('Arial', 9))
        self.entries_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.entries_listbox.bind('<<ListboxSelect>>', self.on_entry_select)
        
        # Scrollbar for listbox
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.entries_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.entries_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Delete button
        ttk.Button(left_frame, text="Delete Selected", command=self.delete_entry).grid(row=2, column=0, pady=(5, 0))
        
        # Right panel for writing/editing
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, rowspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(2, weight=1)
        
        # Title section
        title_frame = ttk.Frame(right_frame)
        title_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        title_frame.columnconfigure(1, weight=1)
        
        ttk.Label(title_frame, text="Title:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(title_frame, textvariable=self.title_var, font=('Arial', 12))
        self.title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Date label
        self.date_label = ttk.Label(right_frame, text=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 
                                   font=('Arial', 10))
        self.date_label.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        # Text area for writing
        text_frame = ttk.Frame(right_frame)
        text_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, font=('Arial', 11), 
                                                  height=20, width=50)
        self.text_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Buttons frame
        buttons_frame = ttk.Frame(right_frame)
        buttons_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(buttons_frame, text="New Entry", command=self.new_entry).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Save Entry", command=self.save_entry).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Clear", command=self.clear_fields).pack(side=tk.LEFT)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Current entry ID (for editing)
        self.current_entry_id = None
    
    def load_entries(self):
        """Load diary entries from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def save_entries(self):
        """Save diary entries to JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.entries, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save entries: {str(e)}")
            return False
    
    def refresh_entries_list(self):
        """Refresh the entries listbox"""
        self.entries_listbox.delete(0, tk.END)
        
        # Sort entries by date (newest first)
        sorted_entries = sorted(self.entries.items(), key=lambda x: x[1]['timestamp'], reverse=True)
        
        for entry_id, entry in sorted_entries:
            date_str = datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M')
            title = entry['title'][:30] + "..." if len(entry['title']) > 30 else entry['title']
            display_text = f"{date_str} - {title}"
            self.entries_listbox.insert(tk.END, display_text)
    
    def on_entry_select(self, event):
        """Handle entry selection from listbox"""
        selection = self.entries_listbox.curselection()
        if selection:
            index = selection[0]
            # Get the entry ID from sorted entries
            sorted_entries = sorted(self.entries.items(), key=lambda x: x[1]['timestamp'], reverse=True)
            entry_id, entry = sorted_entries[index]
            
            # Load entry into editor
            self.current_entry_id = entry_id
            self.title_var.set(entry['title'])
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, entry['content'])
            
            # Update date label
            date_str = datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M')
            self.date_label.config(text=f"Date: {date_str}")
            
            self.status_var.set(f"Loaded entry: {entry['title']}")
    
    def new_entry(self):
        """Start a new diary entry"""
        self.clear_fields()
        self.current_entry_id = None
        self.date_label.config(text=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        self.status_var.set("New entry ready")
        self.title_entry.focus()
    
    def save_entry(self):
        """Save the current diary entry"""
        title = self.title_var.get().strip()
        content = self.text_area.get(1.0, tk.END).strip()
        
        if not title:
            messagebox.showwarning("Warning", "Please enter a title for your entry.")
            self.title_entry.focus()
            return
        
        if not content:
            messagebox.showwarning("Warning", "Please write something in your diary entry.")
            self.text_area.focus()
            return
        
        # Create or update entry
        timestamp = datetime.now().isoformat()
        entry_data = {
            'title': title,
            'content': content,
            'timestamp': timestamp
        }
        
        if self.current_entry_id:
            # Update existing entry
            self.entries[self.current_entry_id] = entry_data
            self.status_var.set(f"Updated entry: {title}")
        else:
            # Create new entry
            entry_id = f"entry_{int(datetime.now().timestamp())}"
            self.entries[entry_id] = entry_data
            self.current_entry_id = entry_id
            self.status_var.set(f"Saved new entry: {title}")
        
        # Save to file and refresh list
        if self.save_entries():
            self.refresh_entries_list()
            messagebox.showinfo("Success", "Diary entry saved successfully!")
    
    def delete_entry(self):
        """Delete the selected diary entry"""
        selection = self.entries_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry to delete.")
            return
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this diary entry?"):
            index = selection[0]
            sorted_entries = sorted(self.entries.items(), key=lambda x: x[1]['timestamp'], reverse=True)
            entry_id, entry = sorted_entries[index]
            
            # Delete entry
            del self.entries[entry_id]
            
            # If this was the currently loaded entry, clear fields
            if self.current_entry_id == entry_id:
                self.clear_fields()
                self.current_entry_id = None
            
            # Save and refresh
            if self.save_entries():
                self.refresh_entries_list()
                self.status_var.set(f"Deleted entry: {entry['title']}")
                messagebox.showinfo("Success", "Diary entry deleted successfully!")
    
    def clear_fields(self):
        """Clear all input fields"""
        self.title_var.set("")
        self.text_area.delete(1.0, tk.END)
        self.date_label.config(text=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        self.status_var.set("Fields cleared")

def main():
    root = tk.Tk()
    app = DiaryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
