# 🌋 Magma Service Framework

Magma Service Framework is a dynamic, gRPC-based Python microservice chassis. It automatically generates input validation (using Pydantic) and service handler stubs based on a central registry of specifications (`spec/registry.py`). This allows developers to focus purely on business logic without worrying about boilerplate gRPC server setup, request validation, or routing.

## 📂 Prerequisites: The `spec` folder

Before initializing the framework, you must define your service actions using Pydantic schemas. 

Create a `spec/` folder in the root of your project containing your Pydantic models and a `registry.py` file to map them.

### 📝 Example `spec/schemas.py`
```python
from pydantic import BaseModel

class GitCloneSpec(BaseModel):
    repository_url: str
    branch: str = "main"
```

### 📝 Example `spec/registry.py`
```python
from .schemas import GitCloneSpec

# The registry dictionary maps the string action to its respective Pydantic spec class
registry = {
    "git.clone": GitCloneSpec
}
```

## 🚀 Usage

Magma Service Framework provides a global CLI tool to bootstrap your projects. 

If you haven't installed it yet, make sure the script is globally available:
```bash
sudo curl -L https://raw.githubusercontent.com/bleolab/magma-service-framework/main/magma-service.sh -o /usr/local/bin/magma-service
sudo chmod +x /usr/local/bin/magma-service
```

Once your `spec` folder is ready, initialize the Magma service in your current directory by simply running:

```bash
magma-service
```
