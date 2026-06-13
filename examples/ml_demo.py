import herio
import time

def mock_image_classifier(image_b64, model_type):
    # In a real scenario, you would decode image_b64 and pass it to your model
    print(f"Received image of length {len(image_b64) if image_b64 else 0} for model {model_type}")
    
    # Simulate processing time
    time.sleep(1)
    
    results = {
        "ResNet-50": "Golden Retriever (92%)",
        "MobileNet": "Labrador (85%)",
        "EfficientNet": "Beagle (88%)"
    }
    
    return results.get(model_type, "Unknown")

demo = herio.Interface(
    fn=mock_image_classifier,
    inputs=[
        herio.Image(label="Upload Image"),
        herio.Dropdown(choices=["ResNet-50", "MobileNet", "EfficientNet"], label="Select Model")
    ],
    outputs=herio.Text(label="Top Prediction"),
    title="ML Image Classifier Demo"
)

if __name__ == "__main__":
    print("Starting ML Demo...")
    # demo.launch(share=True) # Set share=True to get a public URL
    demo.launch()
