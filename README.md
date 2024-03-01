<div align="center">
    <img width="400" height="350" src="/img/laser.webp">
</div>

<h1 align="center">
  <em>SuperLaser</em>
</h1>



**SuperLaser** offers a comprehensive suite of tools and scripts for deploying Large Language Models (LLMs) to RunPod's serverless infrastructure using Python. This approach facilitates efficient and scalable LLM inference, capitalizing on RunPod's robust serverless architecture. The setup is specifically designed to operate with the vLLM engine, ensuring a seamless integration and high-performance inference capabilities.

While most tutorials emphasize the use of the dashboard console on RunPod's site, this repository offers additional functionalities. It enables users to create templates, generate pods or serverless endpoints, and execute API requests programmatically from Python.

# Features <img align="center" width="30" height="29" src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOTBqaWNrcGxnaTdzMGRzNTN0bGI2d3A4YWkxajhsb2F5MW84Z2dxaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26tOZ42Mg6pbTUPHW/giphy.gif">

- **Scalable Deployment**: Easily scale your LLM inference tasks with RunPod serverless capabilities.
- **Cost-Effective**: Optimize resource usage and reduce costs with serverless architecture.
- **Easy Integration**: Seamless integration with existing LLM workflows.

# Setup RunPod <img align="right" width="75" height="75" src="./img/runpod_logo.png">

Before spinning up a serverless endpoint, let's first create a template that we'll pass into the endpoint during staging. Configure your template with the following attributes:

#### Configure Template
```py
import os
from superlaser import RunpodHandler as runpod

api_key = os.environ.get("RUNPOD_API_KEY")

template_data = runpod.set_template(
    serverless="true",
    template_name="superlaser-inf",
    container_image="runpod/worker-vllm:0.3.1-cuda12.1.0",
    model_name="mistralai/Mistral-7B-v0.1",
    max_model_length=340,
    container_disk=15,
    volume_disk=15,
)

template = runpod(api_key=api_key, data=template_data)
print(template().text)
```
#### Configure Endpoint

After your template is created, it will return a data dicitionary that includes your template ID. We will pass this template id when configuring the serverless endpoint in the section below:

```py
endpoint_data = runpod.create_serverless_endpoint(
    gpu_ids="AMPERE_24", # options for gpuIds are "AMPERE_16,AMPERE_24,AMPERE_48,AMPERE_80,ADA_24"
    idle_timeout=5,
    name="vllm_endpoint",
    scaler_type="QUEUE_DELAY",
    scaler_value=1,
    template_id="template-id",
    workers_max=1,
    workers_min=0,
)

endpoint = runpod(api_key=api_key, data=endpoint_data)
print(endpoint().text)
```

#### Call Endpoint

After your endpoint is staged, we can now make API requests 
```py
superlaser = SuperLaser(endpoint_id="endpoint-id", model_name="mistralai/Mistral-7B-v0.1")
superlaser("Why is SuperLaser awesome?")
```

<!-- ### Prerequisites

Before you begin, ensure you have:

- A RunPod account.
- The Runpod CLI `runpodctl`
    - on Linux:

```bash
wget -qO- cli.runpod.net | sudo bash
```

# Install <img align="center" width="30" height="29" src="https://media.giphy.com/media/sULKEgDMX8LcI/giphy.gif">


```bash
pip install superlaser
```

# Inference <img align="center" width="30" height="29" src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMXV1bWFyMWxkY3JocjE1ZDMxMWZ5OHZtejFkbHpuZXdveTV3Z3BiciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/bGgsc5mWoryfgKBx1u/giphy.gif"> -->


