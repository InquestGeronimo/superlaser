<div align="center">
    <img width="400" height="350" src="/img/laser.webp">
</div>

<h1 align="center">
  <em>SuperLaser</em>
</h1>

<h5 align="center">
  ⚠️<em>Not yet eady for primetime</em> ⚠️
</h5>

**SuperLaser** provides a comprehensive suite of tools and scripts designed for deploying Large Language Models (LLMs) onto [RunPod's](https://github.com/runpod) pod and serverless infrastructure. Additionally, the deployment utilizes the [vLLM](https://github.com/vllm-project/vllm) engine as the backend during runtime, ensuring memory-efficient and high-performance inference capabilities.

While most tutorials emphasize the use of RunPod's console to configure a deployment, this repository offers additional functionalities. It enables users to create templates, configure pods and/or serverless endpoints, and execute API requests programmatically from Python.


# Features <img align="center" width="30" height="29" src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOTBqaWNrcGxnaTdzMGRzNTN0bGI2d3A4YWkxajhsb2F5MW84Z2dxaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26tOZ42Mg6pbTUPHW/giphy.gif">

- **Scalable Deployment**: Easily scale your LLM inference tasks with RunPod serverless capabilities.
- **Cost-Effective**: Optimize resource usage and reduce costs with serverless architecture.
- **Easy Integration**: Seamless integration with existing LLM workflows.

# RunPod Config <img align="right" width="75" height="75" src="./img/runpod-logo.png">

First step is to obtain an API key from RunPod. Go to your account's console, in the `Settings` section, click on `API Keys`.

After obtaining a key, set it as an environment variable:

```bash
export RUNPOD_API_KEY=<YOUR-API-KEY>
```
#### Configure Template

Before spinning up a serverless endpoint, let's first create a template that we'll pass into the endpoint during staging. Configure your template with the following attributes:

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
```
Push template to your RunPod account:
```py
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
```

Boot up your endpoint on RunPod:
```py
endpoint = runpod(api_key=api_key, data=endpoint_data)
print(endpoint().text)
```

# Call Endpoint <img align="right" width="225" height="75" src="./img/vllm-logo.png">

After your endpoint is staged, it will return a dictionary with your endpoint ID. Pass this endpoint ID to the `SuperLaser` client and start making API requests!
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


