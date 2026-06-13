import herio

def media_process(text, mode):
    if mode == "Markdown":
        return f"# Output\n\nYou entered: **{text}**"
    elif mode == "Audio":
        # Mock base64 audio
        return "data:audio/wav;base64,UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YTBmYmZmYmZmYmZmYmZmYmZmYmZmYmZmYmZmYmZmYmZmYmZmYmZmYmZmYmZmYmZmYmZmYmZmYmZmYmZmYmZm"
    else:
        return f"Normal text: {text}"

demo = herio.Interface(
    fn=media_process,
    inputs=[
        herio.Textbox(label="Input Text", default="Hello Herio"),
        herio.Dropdown(choices=["Markdown", "Audio", "Text"], label="Output Mode")
    ],
    outputs=[
        herio.Markdown(label="Rich Output"),
        herio.Audio(label="Audio Output")
    ],
    examples=[
        ["Hello World", "Markdown"],
        ["Music", "Audio"]
    ],
    title="Herio Media & Examples Demo"
)

if __name__ == "__main__":
    demo.launch()
