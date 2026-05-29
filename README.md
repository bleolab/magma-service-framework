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

Once your `spec` folder is ready, initialize the Magma service in your current directory by running the following commands:

```bash
# 1. Download and extract the Magma Service Framework
curl -L https://github.com/bleolab/magma-service-framework/tarball/main -o magma-service-framework.tar.gz
tar -zxvf magma-service-framework.tar.gz --strip-components=1
rm magma-service-framework.tar.gz

# 2. Execute the setup script to generate validator.py and service.py based on your specs
magma-service.sh

# 3. Clean up the installation and leftover files
rm magma-service.sh
rm README.md
rm -rf tests
```
