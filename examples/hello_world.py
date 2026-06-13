import herio

def greet(name, intensity):
    return "Hello " * int(intensity) + name + "!"

demo = herio.Interface(
    fn=greet,
    inputs=[
        herio.Textbox(label="Name", default="World"),
        herio.Slider(minimum=1, maximum=10, default=3, label="Intensity")
    ],
    outputs=herio.Label(label="Greeting")
)

if __name__ == "__main__":
    # We won't actually run launch() in the test script to avoid blocking
    print("Demo created successfully")
    # demo.launch()
