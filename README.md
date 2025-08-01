# PyBucky

A minimal Python project that implements Conway polyhedron notation with support for only the `kis` (`k`) and `dual` (`d`) operations. Named after the buckyball (short for Buckminster Fuller ball) which I sought to prototype for a game concept.

The project includes:

* A **half-edge mesh data structure** for polyhedral manipulation
* Basic built-in polyhedra: **cube** (`C`) and **dodecahedron** (`D`)
* **OpenGL-based rendering** of the resulting shape
* Support for validation via **pytest**
* Command-line interface using Conway notation: `python3 main.py kdC`

---

## 🌀 Conway Notation Support

This project supports a minimal subset of Conway polyhedral operators:

| Operator | Description                |
| -------- | -------------------------- |
| `k`      | Kis (pyramid on each face) |
| `d`      | Dual (face-vertex dual)    |

Example:

```bash
python3 main.py kdC
```

---

## 🧱 Built-In Polyhedra

Only two base polyhedra are supported out-of-the-box:

* `C`: Cube
* `D`: Dodecahedron

## 🔧 Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/jacobdill75/pybucky.git
cd pybucky
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv .env
source .env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

> Make sure you have the appropriate OpenGL drivers and headers installed on your system.

---

## 🚀 Running the App

Use Conway notation directly as a CLI argument:

```bash
python3 main.py kdD
```

This builds a polyhedron by applying:

1. `kis` → adds pyramids to all faces of the dodecahedron
2. `dual` → swaps faces and vertices

The result is rendered in an OpenGL window.

---

## 🧪 Running Tests

Tests are implemented using pytest and validate core geometry invariants such as:

* Half-edge consistency
* Convexity checks
* Face winding
* Euler characteristic preservation

To run tests:
```bash
pytest
```

---

## 📎 Notes

* The implementation focuses on clean architecture and geometry correctness, not performance.
* Additional operators (like truncate or snub) are not supported.
* The rendering is simple and minimalistic but helps visually validate operations.

## 📜 License

MIT License
