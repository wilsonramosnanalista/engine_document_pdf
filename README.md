### Prerequisites

1. You need to have **Python** installed on your system.
2. You must open the game_demo.pdf in **Google Chrome or Opera** browser.

### Step 1: Install Python and Verify Setup

1.  **Download and install Python for Windows:**

      * Go to the official Python website.
      * Crucially, during installation, make sure to check the box that says **"Add Python to PATH" or "Add python.exe to PATH".**

2.  **Verify the installation:**

      * Open your Command Prompt (CMD) or PowerShell.
      * Run the command:
        ```bash
        python --version
        ```
      * You should see the installed Python version (e.g., `Python 3.10.6`).
      * *If you encounter an error (e.g., 'python' not recognized), try this fix, although it's usually a Node.js-related command:*
        ```bash
        npm install --legacy-peer-deps
        ```

### Step 2: Download and Extract the Project

1.  **Download the project ZIP file** from the GitHub repository.
2.  **Extract the contents** of the ZIP file to a location on your computer.

### Step 3: Navigate to the Project Folder

1.  Open your Command Prompt (CMD) or PowerShell.
2.  Navigate to the root directory of the extracted project folder using the `cd` command.

    *Example:*

    ```bash
    cd C:\Users\YourUser\Desktop\my-project
    ```

### Step 4: Install Dependencies

1.  Upgrade the `pip` package installer:
    ```bash
    python -m pip install --upgrade pip
    ```
2.  Install the required project dependencies (like `pdfrw`):
    ```bash
    python -m pip install pdfrw
    ```

### Step 5: Apply Code Fix

Remove manually this code. This code snippet is used to automatically open the PDF in the Opera browser on my local machine.

1.  Open the file **`pdf_generator.py`** in VS Code.
2.  **Find and remove** the following block of code:
    ```python
    # Absolute path of the generated PDF
    pdf_path = os.path.abspath("game_demo.pdf")
    
    # Opera browser path
    opera_path = r"C:\Users\Wilson\AppData\Local\Programs\Opera GX\opera.exe"
    
    try:
        # Register Opera as the browser
        webbrowser.register(
            "opera",
            None,
            webbrowser.BackgroundBrowser(opera_path)
        )
    
        # Open PDF in Opera GX
        webbrowser.get("opera").open_new(pdf_path)
        print("Demo game opened in Opera!")
    
    except Exception as e:
        # If it fails, open in the default browser
        print("Could not open in Opera. Opening in default browser instead...")
        webbrowser.open_new(pdf_path)
    ```
4.  **Save** the file.

### Step 6: Run the Script in VS Code

1.  Open Visual Studio Code (VS Code).
2.  Go to **File \> Open Folder** and select the root project folder you extracted in Step 2.
3.  Open the Integrated Terminal in VS Code (Terminal \> New Terminal).
4.  Run the generator script:
    ```bash
    python .\pdf_generator.py
    ```

The script should now execute and generate the intended output file **"game_demo.pdf"** in your project folder.

### Video - Gameplay

Full gameplay video of the game inside a pdf document: https://www.youtube.com/watch?v=bzbTFK3NDpw
