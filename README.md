# Axiom Scientific Calculator

A polished scientific calculator available as both a browser application and a Python desktop application.

## Features

- Basic arithmetic: addition, subtraction, multiplication, division, powers, and modulo
- Scientific functions: `sin`, `cos`, `tan`, `ln`, `log`, `sqrt`, `abs`, and `exp`
- Constants: `pi`, `e`, and the previous result through `Ans`
- Degree and radian angle modes
- Memory controls: `MC`, `MR`, `M+`, and `M-`
- Calculation history
- Keyboard-friendly input
- Responsive browser interface for desktop and mobile screens
- Safe expression evaluation in the Python application

## Project Files

| File | Description |
| --- | --- |
| `index.html` | Main browser entry point for GitHub Pages or a static web host |
| `calculator.html` | Standalone browser version of the calculator |
| `umair.py` | Python Tkinter desktop version |
| `requirements.txt` | Python dependency reference |

## Run the Web Version

### Directly in a browser

Open `index.html` or `calculator.html` in any modern browser.

### With a local server

From the project folder, run:

```powershell
python -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

## Run the Python Version

Python 3.9 or newer is recommended. Tkinter is included with most standard Python installations.

```powershell
python .\umair.py
```

## Expression Examples

```text
sin(30)
sqrt(81)
2^8
pi*2
Ans+10
```

The default angle mode is `DEG`. Switch to `RAD` when working with radian values.

## GitHub Pages

The repository can be published as a static site because `index.html` contains the complete browser application. In GitHub, open **Settings → Pages**, select the `main` branch and the root folder, then save.

## License

This project is available for personal and educational use.