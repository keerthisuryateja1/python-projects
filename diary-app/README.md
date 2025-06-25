# Diary App

A simple, user-friendly diary application built with Python and tkinter.

## Features

- 📝 **Write Journal Entries**: Create new diary entries with titles and content
- 📅 **Automatic Date Tracking**: Each entry is automatically timestamped
- 👀 **View Past Entries**: Browse through all your previous journal entries
- ✏️ **Edit Entries**: Select and modify existing entries
- 🗑️ **Delete Entries**: Remove entries with confirmation dialog
- 💾 **Data Persistence**: All entries are saved to a JSON file
- 🎨 **Clean Interface**: Intuitive two-panel design for easy navigation

## Screenshots

The app features a clean, two-panel interface:
- **Left Panel**: List of all your diary entries sorted by date
- **Right Panel**: Writing area with title field and text editor

## How to Run

1. Make sure you have Python 3.6 or higher installed
2. Run the application:
   ```bash
   python diary_app.py
   ```
3. The app will create a `diary_entries.json` file to store your entries

## Usage

1. **Create New Entry**: Click "New Entry" button
2. **Add Title**: Enter a descriptive title for your entry
3. **Write Content**: Type your thoughts in the large text area
4. **Save**: Click "Save Entry" to store your journal entry
5. **View Past Entries**: Click on any entry in the left list to read it
6. **Edit**: Select an entry, make changes, and save again
7. **Delete**: Select an entry and click "Delete Selected"

## Technical Details

- **GUI Framework**: tkinter (included with Python)
- **Data Storage**: JSON format for easy data management
- **File Encoding**: UTF-8 for international character support
- **Error Handling**: User-friendly error messages and confirmations

## Requirements

- Python 3.6+
- tkinter (usually bundled with Python)

## License

This project is open source and available under the MIT License.
