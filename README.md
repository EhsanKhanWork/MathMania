# MathMania

MathMania is a simple maths I game made in Python using Pygame.  

The objective is to answer maths questions correctly to score points and survive as long as you can.

---

## What You Need (Windows)

- Windows 10 or Windows 11  
- Python 3.7 or newer  

### 1. Install Python (Windows)

1. Go to https://www.python.org/downloads/
2. Download the latest version of Python 3.
3. Run the installer.
4. IMPORTANT: Tick the box that says **"Add Python to PATH"** before clicking Install.

To check Python is installed, open **Command Prompt** and type:

python --version

If it shows a version number, it is installed correctly.

---

### 2. Install Pygame

Open **Command Prompt** and type:

pip install pygame

---

## How to Run the Game

1. Download or clone the project:

git clone https://github.com/EhsanKhanWork/MathMania.git

2. Go into the project folder:

cd MathMania

3. Run the game:

python main.py

---

## How to Play

- Log in or create an account.
- Use **Left/Right arrow keys** (or A/D) to move.
- Press **Space** to jump.
- Jump on the platform with the correct answer.
- The game ends if you choose the wrong answer or run out of time.

---

## Notes

- Do not delete the `assets` folder.
- Make sure all `.json` and `.txt` files stay in the main folder or the game may not work.

---

## Project Structure

MathMania/
│
├── main.py            # Starts the game  
├── gameplay.py        # Main game logic  
├── login.py           # Login and account system  
├── main_menu.py       # Menu screens  
├── loading.py         # Loading screen  
├── background.py      # Background visuals  
├── assets/            # Images and sound files  
├── settings.json      # Game settings  
├── users.json         # Saved user accounts  
├── save.txt           # High score  
├── time.txt           # Best survival time  
└── README.md  

---

Made as a Computer Science A Level project by Ehsan Khan studying at Morpeth 6th Form.
