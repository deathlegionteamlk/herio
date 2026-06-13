<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=2,6,18&height=220&section=header&text=Herio&fontSize=90&fontColor=ffffff&fontAlignY=38&desc=Python%20function%20%E2%86%92%20web%20app.%20No%20HTML%20required.&descAlignY=60&descSize=20&animation=fadeIn" width="100%"/>

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&duration=2800&pause=900&color=10B981&center=true&vCenter=true&multiline=true&width=680&height=80&lines=Wrap+any+Python+function+in+a+UI.+In+minutes.;Text%2C+sliders%2C+images%2C+audio%2C+video+%E2%80%94+all+built+in.;Share+publicly+with+one+flag." alt="Typing animation"/>

<br/><br/>

[![PyPI](https://img.shields.io/pypi/v/herio?style=for-the-badge&logo=python&logoColor=white&color=10b981)](https://pypi.org/project/herio/)
[![License: MIT](https://img.shields.io/badge/License-MIT-6366f1?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3b82f6?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Bootstrap](https://img.shields.io/badge/UI-Bootstrap%205-7c3aed?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com)
[![Built by](https://img.shields.io/badge/💀-Death%20Legion%20Team-1a1a1a?style=for-the-badge)](https://github.com/deathlegionteamlk)

</div>

---

## 🤔 What is Herio?

You trained a model. Or wrote a function that does something useful. Now someone wants to try it — and they don't have Python installed, don't want to touch the terminal, and just want a text box and a button.

Herio is for that moment.

You define inputs and outputs in Python, point it at your function, and call `.launch()`. Herio starts a local web server with a working UI — no HTML, no CSS, no JavaScript written by you. Add `share=True` and it tunnels the app to a public URL via ngrok so anyone can reach it.

It's closer in spirit to Gradio than Streamlit — you're wrapping a function, not building a full page — and if you've used either of those, Herio's API will take about five minutes to learn.

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/212284158-e840e285-664b-44d7-b79b-e264b5e54825.gif" width="400"/>
</div>

---

## ✨ What's included

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/212257467-871d32b7-e401-42e8-a166-fcfd7baa4c6b.gif" width="80"/>
</div>

<table>
<tr>
<td width="50%">

### ⚡ Zero-config UI
Pass inputs and outputs to `herio.Interface`, call `.launch()`. Herio generates the entire frontend from your component definitions — layout, styling, wiring between inputs and your function output.

### 🐍 Pure Python components
Every UI element — text boxes, sliders, image uploaders, audio players — is a Python class. No templates, no YAML, no frontend framework to learn.

### 🔗 Instant public sharing
`demo.launch(share=True)` tunnels your local app through ngrok and prints a public URL. Useful for demos, quick testing with non-technical collaborators, or sharing notebooks.

</td>
<td width="50%">

### 🎨 Modern responsive UI
The frontend is Bootstrap 5 — clean, mobile-friendly, and consistent across browsers without you touching a stylesheet.

### 📁 Rich media support
Input and output components for text, images, audio, video, sliders, checkboxes, dropdowns, and markdown. If your model takes an image and returns text, there's a component pair for that already.

### 📋 Example rows
Provide example inputs and they show up as clickable rows below the interface. Users can run your demo on real inputs without typing anything.

</td>
</tr>
</table>

---

## 📦 Install

```bash
pip install herio
```

For public sharing support:

```bash
pip install herio[share]
```

---

## 🚀 Quickstart

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/212257454-16e3712e-945a-4ca2-b238-408ad0bf87e6.gif" width="80"/>
</div>

The simplest case — a function, two inputs, one output:

```python
import herio

def greet(name, intensity):
    return "Hello " * int(intensity) + name + "!"

demo = herio.Interface(
    fn=greet,
    inputs=[
        herio.Textbox(label="Name", default="World"),
        herio.Slider(minimum=1, maximum=10, default=3, label="Intensity"),
    ],
    outputs=herio.Text(label="Greeting"),
    title="Herio Quickstart",
)

if __name__ == "__main__":
    demo.launch()
```

Open `http://localhost:7860` and you have a working app.

---

## 🖼️ Media inputs and outputs

Image classification, audio transcription, video processing — Herio has components for all of them. Your function receives Python objects (PIL images, numpy arrays, file paths) and returns the same. Herio handles the browser ↔ Python conversion.

```python
import herio
from PIL import Image
import numpy as np

def grayscale(image):
    # image arrives as a PIL Image
    gray = np.mean(np.array(image), axis=2, keepdims=True)
    return Image.fromarray(gray.squeeze().astype(np.uint8))

demo = herio.Interface(
    fn=grayscale,
    inputs=herio.Image(label="Upload an image"),
    outputs=herio.Image(label="Grayscale output"),
    title="Image → Grayscale",
)

demo.launch()
```

---

## 📝 Markdown output

Return formatted text, tables, or documentation from your function and render it with the `Markdown` component:

```python
import herio

def analyze(text):
    word_count = len(text.split())
    char_count = len(text)
    return f"""
## Analysis

| Metric     | Value        |
|------------|-------------|
| Words      | {word_count} |
| Characters | {char_count} |

**Summary:** Your text has {word_count} words across {char_count} characters.
"""

demo = herio.Interface(
    fn=analyze,
    inputs=herio.Textbox(label="Paste your text", lines=6),
    outputs=herio.Markdown(label="Results"),
    title="Text Analyzer",
)

demo.launch()
```

---

## 📋 Example rows

Clickable example inputs let users try your demo without typing anything. Pass a list of lists — one list per example, matching the order of your inputs:

```python
demo = herio.Interface(
    fn=my_model,
    inputs=herio.Textbox(label="Input"),
    outputs=herio.Markdown(label="Output"),
    examples=[
        ["A quick brown fox"],
        ["The model does better with longer inputs"],
        ["Try something specific to your domain"],
    ],
)

demo.launch()
```

---

## 🌐 Public sharing

```python
demo.launch(share=True)
```

Herio tunnels your local server through ngrok and prints a public URL:

```
Running on local:  http://localhost:7860
Running on public: https://xxxx-xx-xx-xxx-xx.ngrok.io
```

The link works for anyone with it — no account, no deploy step. It stays live while your script runs.

---

## 🤖 Wrapping an ML model

A more realistic example — load a model, wrap the inference call:

```python
import herio
from transformers import pipeline

classifier = pipeline("sentiment-analysis")

def predict(text):
    result = classifier(text)[0]
    label = result["label"]
    score = result["score"]
    return f"**{label}** ({score:.1%} confidence)"

demo = herio.Interface(
    fn=predict,
    inputs=herio.Textbox(
        label="Text to classify",
        placeholder="Type something here...",
        lines=3,
    ),
    outputs=herio.Markdown(label="Prediction"),
    title="Sentiment Classifier",
    examples=[
        ["I absolutely loved this movie."],
        ["The service was slow and the food was cold."],
        ["It was fine, nothing special."],
    ],
)

demo.launch()
```

---

## 📋 Component reference

### Input components

| Component | What it gives your function |
|---|---|
| `Textbox(label, default, lines)` | `str` |
| `Slider(minimum, maximum, default, label)` | `float` |
| `Image(label)` | `PIL.Image` |
| `Audio(label)` | `(sample_rate, np.ndarray)` |
| `Video(label)` | file path `str` |
| `Checkbox(label)` | `bool` |
| `Dropdown(choices, label)` | `str` |

### Output components

| Component | Renders |
|---|---|
| `Text(label)` | Plain string |
| `Markdown(label)` | Rendered markdown |
| `Image(label)` | `PIL.Image` or numpy array |
| `Audio(label)` | `(sample_rate, np.ndarray)` |
| `Video(label)` | File path |

---

## 🏗️ How it works

```
demo.launch()
      │
      ▼
Herio starts a local Flask server
      │
      ▼
Browser loads Bootstrap 5 frontend
      │
      ▼
User fills in inputs → submits
      │
      ▼
Frontend POSTs to /predict
      │
      ▼
Herio deserializes inputs → calls your fn()
      │
      ▼
Return value serialized → sent back to browser
      │
      ▼
Output component renders the result
```

Everything your function receives is already the right Python type. Everything it returns gets serialized automatically. You don't touch the request/response cycle.

---

## 🤝 Contributing

<div align="center">
<img src="https://user-images.githubusercontent.com/74038190/212284115-f47cd8ff-2ffb-4b04-b5bf-4d1c14c0247f.gif" width="400"/>
</div>

Issues and PRs welcome. Open an issue before starting on anything large.

```bash
git clone https://github.com/deathlegionteamlk/herio.git
cd herio
pip install -e ".[dev]"
pytest
```

---

## 🛡️ License

MIT © [Death Legion Team](https://github.com/deathlegionteamlk)

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=2,6,18&height=100&section=footer&animation=fadeIn" width="100%"/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=13&duration=4000&pause=1000&color=10B981&center=true&vCenter=true&width=540&lines=Python+function+%E2%86%92+working+web+app.;No+HTML.+No+JS.+No+config.;💀+Built+by+Death+Legion+Team." alt="Footer typing"/>

</div>
