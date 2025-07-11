# Vector: A 3D Modeller Built with Python & OpenGL

**Vector** is a lightweight and interactive 3D modelling application built using **Python**, **PyOpenGL**, and **GLFW**. It provides a programmable 3D canvas where users can create, manipulate, and visualize basic 3D objects in real-time. The application is designed for students, hobbyists, and developers learning the fundamentals of 3D graphics programming and OpenGL rendering pipelines.

---

## 🎯 Project Objective

To create an interactive 3D modelling software with the following capabilities:
- Real-time rendering of 3D meshes
- Basic geometric transformations (translate, rotate, scale)
- Camera manipulation for intuitive navigation
- Foundation for future mesh editing, object hierarchy, and export support

---

## 🧰 Tech Stack

- **Python 3.10+**
- **PyOpenGL** – for interfacing with OpenGL
- **GLFW** – window and context creation
- **NumPy** – mathematical computations

---

## 📁 Project Structure

```
vector/
├── main.py              # Entry point for the application
├── camera.py            # Camera movement and view matrix logic
├── mesh.py              # Mesh and object representation
├── models/              # 3D models 
├── textures/            # textures for models
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```
<!---
├── renderer.py          # Shader programs and drawing logic
├── controls.py          # Keyboard/mouse input processing
├── shaders/
│   ├── vertex.glsl      # Vertex shader
│   └── fragment.glsl    # Fragment shader
├── utils.py             # Helper functions and math utils
--->
---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/duttaturja/vector.git
cd vector
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python main.py
```

---

## 🕹️ Controls
- **W/A/S/D** – Move camera forward/left/back/right
- **Arrow Keys / Mouse** – Rotate camera
- **Scroll Wheel** – Zoom in/out
- **Space** – Add or transform object (customizable logic)

---

## 🧠 Features (Implemented & Planned)

### ✅ Implemented
- Real-time rendering of wireframe and solid objects
- Custom camera navigation
- Clean architecture for extensions

### 🛠 Planned
- Object selection and manipulation
- Mesh importing/exporting
- GUI integration with DearPyGui or PyImgui
- Lighting and shading pipeline

---

## 🧑‍💻 Contributing
If you have suggestions or want to help expand Vector’s capabilities:
1. Fork the repo
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes
4. Open a pull request

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Crafted with matrices and shaders by [Turja Dutta](https://github.com/duttaturja) 🧊
