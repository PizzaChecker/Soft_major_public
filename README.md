**Disclaimer:**  
This project is for educational purposes only. Do not use it in production environments without proper security review and testing. The author(s) are not responsible for any misuse or damages resulting from the use of this code.

If any part of the project donsen't work it may be because of improper transfering of files done by me. If this occured please contact me and I will try to rectify the issue.

**Contains un-licensed copyright material (images)**
### Environment Setup

1. **Create a virtual environment**:
   ```bash
   python3 -m venv env
   ```

2. **Set execution policy (Windows only)**:
   Temporarily allow script execution for the current terminal session:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

3. **Activate the virtual environment**:
   ```bash
   env\Scripts\Activate  # Windows
   source env/bin/activate  # macOS/Linux
   ```

4. **Create a `.gitignore` file**:
   Use the following command to create a `.gitignore` file:
   ```bash
   touch .gitignore
   ```
   Add the following lines to the `.gitignore` file to prevent uploading sensitive files:
   ```
   env/
   .env
   ```

5. **Set environment variables**:
   Add the following environment variables (replace `put_secret_key_here` with your actual secret keys):
   ```powershell
   Windows
   $env:VSCODE_DOM="put_secret_key_here" (1) 
   $env:VSCODE_SK_='put_secret_key_here' (2)
   ```
   ```zsh
   Mac (Unsure if works)
   export VSCODE_DOM="put_secret_key_here"   
   export VSCODE_SK_="put_secret_key_here"
   ```
   Example values:
   ```
   CajnoXYH-sBaXYYlgznRUfGolxVklLR-GpebSEUSnkg= (1)
   _5#y2L"F4Q8z\n\xec]/ (2)
   ```

6. **View all environment variables** (optional):
   ```powershell
   Get-ChildItem Env:
   ```

7. **Install required Python packages**:
   Run the following commands to install all necessary dependencies:
   ```bash
   pip install flask
   pip install flask-csp
   pip install pillow
   pip install bcrypt
   pip install cryptography
   pip install Flask-WTF
   pip install Flask-Limiter
   pip install pytest
   pip install sqlalchemy
   pip install flask_sqlalchemy
   pip install pytz
   pip install requests
   pip install werkzeug (Should be included with flask)
   pip install jinja2 (Should be included with flask)
   ```

8. **Verify installation**:
   Ensure all packages are installed correctly by running:
   ```bash
   pip list
   ```

9. **Intilise DB & Input Products**:
   Create the DB by running init_db.py
   Then insert the defualt products into the database, comment out the line at the bottom where it says (if not alredy done):
   ```bash
   if __name__ == '__main__':
      input_prod() 
	```
   So it only runs
   ```bash
   bulk_insert_products()
   ```

### Notes
- Ensure Python 3 is installed on your system.
- Use a secure method to store and manage secret keys (e.g., `.env` file or environment variables).
