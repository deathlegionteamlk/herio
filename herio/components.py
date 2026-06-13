from abc import ABC, abstractmethod
from typing import Any, List, Optional

class Component(ABC):
    def __init__(self, label: str = None, default: Any = None):
        self.label = label
        self.default = default

    @abstractmethod
    def get_type(self) -> str:
        pass

    def to_dict(self) -> dict:
        return {
            "type": self.get_type(),
            "label": self.label,
            "default": self.default,
        }

    def preprocess(self, x: Any) -> Any:
        return x

    def postprocess(self, x: Any) -> Any:
        return x

class Textbox(Component):
    def get_type(self) -> str:
        return "textbox"

class Number(Component):
    def get_type(self) -> str:
        return "number"

    def preprocess(self, x: Any) -> Any:
        if x is None or x == "":
            return self.default if self.default is not None else 0
        try:
            return float(x)
        except (ValueError, TypeError):
            return 0

class Slider(Component):
    def __init__(self, minimum: float = 0, maximum: float = 100, step: float = 1, label: str = None, default: Any = None):
        super().__init__(label, default if default is not None else minimum)
        self.minimum = minimum
        self.maximum = maximum
        self.step = step

    def get_type(self) -> str:
        return "slider"

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({
            "min": self.minimum,
            "max": self.maximum,
            "step": self.step,
        })
        return d

    def preprocess(self, x: Any) -> Any:
        try:
            return float(x)
        except (ValueError, TypeError):
            return self.default

class Checkbox(Component):
    def get_type(self) -> str:
        return "checkbox"

    def preprocess(self, x: Any) -> Any:
        return bool(x)

class Dropdown(Component):
    def __init__(self, choices: List[str], label: str = None, default: str = None):
        super().__init__(label, default if default is not None else (choices[0] if choices else None))
        self.choices = choices

    def get_type(self) -> str:
        return "dropdown"

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({"choices": self.choices})
        return d

class Image(Component):
    def get_type(self) -> str:
        return "image"
    
    def preprocess(self, x: Any) -> Any:
        if isinstance(x, str) and x.startswith("data:image"):
            return x.split(",")[1]
        return x

class Audio(Component):
    def get_type(self) -> str:
        return "audio"
    
    def preprocess(self, x: Any) -> Any:
        if isinstance(x, str) and x.startswith("data:audio"):
            return x.split(",")[1]
        return x

class Video(Component):
    def get_type(self) -> str:
        return "video"
    
    def preprocess(self, x: Any) -> Any:
        if isinstance(x, str) and x.startswith("data:video"):
            return x.split(",")[1]
        return x

class Label(Component):
    def get_type(self) -> str:
        return "label"

class Text(Label):
    pass

class Markdown(Component):
    def get_type(self) -> str:
        return "markdown"
