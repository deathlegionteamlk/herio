# Herio: Instant Web UIs for Python Functions & ML Models

[![PyPI version](https://img.shields.io/pypi/v/herio.svg)](https://pypi.org/project/herio/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Herio** is the fastest way to turn your Python functions into interactive web applications. Designed specifically for machine learning engineers and data scientists, Herio allows you to build and share beautiful demos without writing a single line of HTML, CSS, or JavaScript.

## Why Herio?

- 🚀 **Instant Deployment:** Go from a Python function to a running web app in seconds.
- 🐍 **Pure Python:** Define your entire interface using simple Python components.
- 🔗 **Easy Sharing:** Integrated `ngrok` support for generating public URLs instantly.
- 🎨 **Modern UI:** Clean, responsive interface built with Bootstrap 5.
- 📦 **Feature Rich:** Supports text, sliders, images, audio, video, markdown, and more.

## Installation

Install Herio via pip:

```bash
pip install herio
```

## Quick Start

Create a simple greeting app:

```python
import herio

def greet(name, intensity):
    return "Hello " * int(intensity) + name + "!"

demo = herio.Interface(
    fn=greet,
    inputs=[
        herio.Textbox(label="Name", default="World"),
        herio.Slider(minimum=1, maximum=10, default=3, label="Intensity")
    ],
    outputs=herio.Text(label="Greeting"),
    title="Herio Quickstart"
)

if __name__ == "__main__":
    demo.launch()
```

## Advanced Features

### Media Support
Herio supports rich media inputs and outputs, including Images, Audio, and Video.

### Markdown Rendering
Display formatted text, tables, and documentation using the `Markdown` component.

### Examples
Provide example inputs to help users get started with your demo.

```python
demo = herio.Interface(
    fn=my_model,
    inputs=herio.Textbox(),
    outputs=herio.Markdown(),
    examples=[["Example 1"], ["Example 2"]]
)
```

## Sharing your app

To generate a temporary, public URL for sharing, just set `share=True`:

```python
demo.launch(share=True)
```

## SEO & Keywords
Python Web UI, Machine Learning Demo, Gradio Alternative, Streamlit Alternative, FastAPI Web App, Data Science Tools, ML Deployment, Python Interface, Rapid Prototyping.

## License
MIT © Death Legion Team
