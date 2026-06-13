import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from jinja2 import Template
from .components import Component
from typing import Callable, List, Union, Optional, Any
import json

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        body { background-color: #f0f2f5; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .app-container { max-width: 1000px; margin: 50px auto; }
        .card { border: none; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .card-header { background-color: #ffffff; border-bottom: 1px solid #eee; border-radius: 15px 15px 0 0 !important; padding: 20px; }
        .card-body { padding: 30px; }
        .component-label { font-weight: 600; color: #4a4a4a; margin-bottom: 8px; }
        .btn-run { background-color: #007bff; border: none; padding: 12px; font-weight: 600; width: 100%; border-radius: 8px; margin-top: 20px; }
        .btn-run:hover { background-color: #0056b3; }
        .output-well { background-color: #f8f9fa; border-radius: 8px; padding: 15px; min-height: 50px; border: 1px solid #e9ecef; }
        .footer { text-align: center; margin-top: 30px; color: #6c757d; font-size: 0.9em; }
        .example-row { cursor: pointer; }
        .example-row:hover { background-color: #f1f3f5; }
    </style>
</head>
<body>
    <div class="container app-container">
        <div class="card">
            <div class="card-header">
                <h2 class="mb-0">{{ title }}</h2>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6 border-end">
                        <h4 class="mb-4">Inputs</h4>
                        <div id="inputs-container">
                            {% for idx, comp in enumerate(inputs) %}
                                <div class="mb-4">
                                    <label class="component-label">{{ comp.label or "Input " + str(idx) }}</label>
                                    {% if comp.type == 'textbox' %}
                                        <input type="text" class="form-control" id="input-{{ idx }}" value="{{ comp.default or '' }}">
                                    {% elif comp.type == 'number' %}
                                        <input type="number" class="form-control" id="input-{{ idx }}" value="{{ comp.default or 0 }}">
                                    {% elif comp.type == 'slider' %}
                                        <input type="range" class="form-range" id="input-{{ idx }}" min="{{ comp.min }}" max="{{ comp.max }}" step="{{ comp.step }}" value="{{ comp.default }}">
                                        <div class="text-center text-muted small"><span id="val-{{ idx }}">{{ comp.default }}</span></div>
                                        <script>
                                            document.getElementById('input-{{ idx }}').oninput = function() {
                                                document.getElementById('val-{{ idx }}').innerText = this.value;
                                            }
                                        </script>
                                    {% elif comp.type == 'checkbox' %}
                                        <div class="form-check">
                                            <input class="form-check-input" type="checkbox" id="input-{{ idx }}" {% if comp.default %}checked{% endif %}>
                                            <label class="form-check-label" for="input-{{ idx }}">Enabled</label>
                                        </div>
                                    {% elif comp.type == 'dropdown' %}
                                        <select class="form-select" id="input-{{ idx }}">
                                            {% for choice in comp.choices %}
                                                <option value="{{ choice }}" {% if choice == comp.default %}selected{% endif %}>{{ choice }}</option>
                                            {% endfor %}
                                        </select>
                                    {% elif comp.type == 'image' %}
                                         <input type="file" class="form-control" id="input-{{ idx }}" accept="image/*">
                                    {% elif comp.type == 'audio' %}
                                         <input type="file" class="form-control" id="input-{{ idx }}" accept="audio/*">
                                    {% elif comp.type == 'video' %}
                                         <input type="file" class="form-control" id="input-{{ idx }}" accept="video/*">
                                    {% endif %}
                                </div>
                            {% endfor %}
                        </div>
                        <button id="submit-btn" class="btn btn-primary btn-run">Run Prediction</button>
                    </div>
                    <div class="col-md-6">
                        <h4 class="mb-4 ps-md-3">Outputs</h4>
                        <div id="outputs-container">
                            {% for idx, comp in enumerate(outputs) %}
                                <div class="mb-4 ps-md-3">
                                    <label class="component-label">{{ comp.label or "Output " + str(idx) }}</label>
                                    <div id="output-{{ idx }}" class="output-well">
                                        {% if comp.type == 'markdown' and comp.default %}
                                            <script>document.getElementById('output-{{ idx }}').innerHTML = marked.parse({{ comp.default | tojson }});</script>
                                        {% elif comp.default %}
                                            {{ comp.default }}
                                        {% endif %}
                                    </div>
                                </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>

                {% if examples %}
                    <div class="mt-5">
                        <h4>Examples</h4>
                        <table class="table table-bordered mt-3">
                            <thead>
                                <tr>
                                    {% for idx, comp in enumerate(inputs) %}
                                        <th>{{ comp.label or "Input " + str(idx) }}</th>
                                    {% endfor %}
                                </tr>
                            </thead>
                            <tbody>
                                {% for example in examples %}
                                    <tr class="example-row" onclick='loadExample({{ example | tojson | replace("'", "\\'") }})'>
                                        {% for val in example %}
                                            <td>{{ val }}</td>
                                        {% endfor %}
                                    </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                {% endif %}
            </div>
        </div>
        <div class="footer">
            Built with <strong>Herio</strong> by Death Legion Team
        </div>
    </div>

    <script>
        function loadExample(example) {
            example.forEach((val, idx) => {
                const el = document.getElementById('input-' + idx);
                if (!el) return;
                if (el.type === 'checkbox') {
                    el.checked = !!val;
                } else if (el.type === 'file') {
                    // Cannot easily set file inputs via JS for security, but we could handle it if we had blobs
                } else {
                    el.value = val;
                    // Trigger input event for sliders
                    el.dispatchEvent(new Event('input'));
                }
            });
        }

        async function getBase64(file) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.readAsDataURL(file);
                reader.onload = () => resolve(reader.result);
                reader.onerror = error => reject(error);
            });
        }

        document.getElementById('submit-btn').onclick = async function() {
            const submitBtn = this;
            submitBtn.disabled = true;
            submitBtn.innerText = "Running...";

            try {
                const inputs = [];
                {% for idx, comp in enumerate(inputs) %}
                    {% if comp.type == 'checkbox' %}
                        inputs.push(document.getElementById('input-{{ idx }}').checked);
                    {% elif comp.type in ['image', 'audio', 'video'] %}
                        const fileInput{{ idx }} = document.getElementById('input-{{ idx }}');
                        if (fileInput{{ idx }}.files.length > 0) {
                            inputs.push(await getBase64(fileInput{{ idx }}.files[0]));
                        } else {
                            inputs.push(null);
                        }
                    {% else %}
                        inputs.push(document.getElementById('input-{{ idx }}').value);
                    {% endif %}
                {% endfor %}

                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ data: inputs })
                });
                const result = await response.json();
                
                result.data.forEach((val, idx) => {
                    const outDiv = document.getElementById('output-' + idx);
                    const compType = {{ outputs_types | tojson }}[idx];
                    
                    if (compType === 'markdown') {
                        outDiv.innerHTML = marked.parse(val);
                    } else if (compType === 'image' || (typeof val === 'string' && (val.startsWith('data:image') || (val.length > 100 && !val.includes(' ')) && !val.startsWith('data:audio') && !val.startsWith('data:video')))) {
                         let src = val;
                         if (!val.startsWith('data:image') && /^[A-Za-z0-9+/=]+$/.test(val)) {
                            src = 'data:image/png;base64,' + val;
                         }
                         outDiv.innerHTML = '<img src="' + src + '" class="img-fluid rounded">';
                    } else if (compType === 'audio' || (typeof val === 'string' && val.startsWith('data:audio'))) {
                         outDiv.innerHTML = '<audio controls src="' + val + '" class="w-100"></audio>';
                    } else if (compType === 'video' || (typeof val === 'string' && val.startsWith('data:video'))) {
                         outDiv.innerHTML = '<video controls src="' + val + '" class="w-100"></video>';
                    } else {
                         outDiv.innerText = val;
                    }
                });
            } catch (err) {
                console.error(err);
                alert("An error occurred during prediction.");
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerText = "Run Prediction";
            }
        };
    </script>
</body>
</html>
"""

class Interface:
    def __init__(
        self,
        fn: Callable,
        inputs: Union[Component, List[Component]],
        outputs: Union[Component, List[Component]],
        title: str = "Herio App",
        examples: Optional[List[List[Any]]] = None
    ):
        self.fn = fn
        self.inputs = inputs if isinstance(inputs, list) else [inputs]
        self.outputs = outputs if isinstance(outputs, list) else [outputs]
        self.title = title
        self.examples = examples
        self.app = FastAPI()
        self.setup_routes()

    def setup_routes(self):
        @self.app.get("/", response_class=HTMLResponse)
        async def index():
            template = Template(HTML_TEMPLATE)
            return template.render(
                title=self.title,
                inputs=[c.to_dict() for c in self.inputs],
                outputs=[c.to_dict() for c in self.outputs],
                outputs_types=[c.get_type() for c in self.outputs],
                examples=self.examples,
                enumerate=enumerate,
                str=str
            )

        @self.app.post("/predict")
        async def predict(request: Request):
            body = await request.json()
            raw_inputs = body.get("data", [])
            
            processed_inputs = []
            for i, comp in enumerate(self.inputs):
                val = raw_inputs[i] if i < len(raw_inputs) else None
                processed_inputs.append(comp.preprocess(val))
            
            if len(self.inputs) == 1:
                result = self.fn(processed_inputs[0])
            else:
                result = self.fn(*processed_inputs)
            
            if not isinstance(result, (list, tuple)):
                result = [result]
            
            processed_outputs = []
            for i, comp in enumerate(self.outputs):
                val = result[i] if i < len(result) else None
                processed_outputs.append(comp.postprocess(val))
                
            return {"data": processed_outputs}

    def launch(self, share: bool = False, port: int = 7860):
        if share:
            try:
                from pyngrok import ngrok
                public_url = ngrok.connect(port).public_url
                print(f" * Public URL: {public_url}")
            except Exception as e:
                print(f"Could not create share link: {e}. Make sure you have set up your ngrok auth token.")

        print(f" * Local URL: http://127.0.0.1:{port}")
        uvicorn.run(self.app, host="127.0.0.1", port=port, log_level="error")
