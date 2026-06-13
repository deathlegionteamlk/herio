import pytest
from herio.components import Textbox, Number, Slider, Checkbox, Dropdown, Image, Text, Markdown, Audio, Video

def test_textbox():
    comp = Textbox(label="Name", default="User")
    assert comp.get_type() == "textbox"
    assert comp.to_dict() == {"type": "textbox", "label": "Name", "default": "User"}
    assert comp.preprocess("Hello") == "Hello"

def test_number():
    comp = Number(label="Age", default=25)
    assert comp.get_type() == "number"
    assert comp.preprocess("30") == 30.0
    assert comp.preprocess("") == 25
    assert comp.preprocess(None) == 25
    assert comp.preprocess("abc") == 0

def test_slider():
    comp = Slider(minimum=0, maximum=10, step=0.5, label="Value", default=5)
    assert comp.get_type() == "slider"
    d = comp.to_dict()
    assert d["min"] == 0
    assert d["max"] == 10
    assert d["step"] == 0.5
    assert comp.preprocess("7.5") == 7.5

def test_checkbox():
    comp = Checkbox(label="Agree")
    assert comp.get_type() == "checkbox"
    assert comp.preprocess(True) is True
    assert comp.preprocess(False) is False

def test_dropdown():
    comp = Dropdown(choices=["A", "B", "C"], label="Choose")
    assert comp.get_type() == "dropdown"
    assert comp.to_dict()["choices"] == ["A", "B", "C"]
    assert comp.to_dict()["default"] == "A"

def test_image():
    comp = Image(label="Upload")
    assert comp.get_type() == "image"
    base64_img = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    processed = comp.preprocess(base64_img)
    assert not processed.startswith("data:image")
    assert processed.startswith("iVBORw")

def test_markdown():
    comp = Markdown(label="Doc")
    assert comp.get_type() == "markdown"

def test_media():
    audio = Audio()
    assert audio.get_type() == "audio"
    assert audio.preprocess("data:audio/wav;base64,UklGR") == "UklGR"
    
    video = Video()
    assert video.get_type() == "video"
    assert video.preprocess("data:video/mp4;base64,AAAA") == "AAAA"
