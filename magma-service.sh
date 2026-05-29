#!/bin/bash

echo "[Magma] Baixando e extraindo o framework..."
curl -L -s https://github.com/bleolab/magma-service-framework/tarball/main -o magma-service-framework.tar.gz
tar -zxf magma-service-framework.tar.gz --strip-components=1
rm magma-service-framework.tar.gz

# Limpa arquivos não necessários no projeto final
rm -f magma-service.sh download.sh README.md
rm -rf tests

echo "[Magma] Gerando validator.py e service.py a partir do registry..."
python3 - << 'EOF'
import os
import sys

# Adiciona o diretório atual ao sys.path para conseguir importar de 'spec'
sys.path.insert(0, os.getcwd())

try:
    from spec.registry import registry
except ImportError as e:
    print(f"Erro ao tentar importar 'registry' de 'spec.registry': {e}")
    sys.exit(1)

# 1. Geração do validator.py
validator_code = """import yaml
from abstract_validator import AbstractValidator
from spec.registry import registry
from pydantic import ValidationError

class Validator(AbstractValidator):
    def validate(self, request):
        action = request.action
        if action not in registry:
            raise Exception(f"Action '{action}' not declared in registry")
        
        spec_class = registry[action]
        try:
            payload_dict = yaml.safe_load(request.payload) if request.payload else {}
            return spec_class(**payload_dict)
        except ValidationError as e:
            raise Exception(f"Error validating payload for action '{action}': {e}")
"""
with open("validator.py", "w", encoding="utf-8") as f:
    f.write(validator_code)

# 2. Geração do service.py
imports = set()
handlers = [
    "    def execute(self, request, spec=None):",
    "        handler_name = request.action.replace('.', '_') + '_handler'",
    "        handler = getattr(self, handler_name, None)",
    "        if handler:",
    "            return handler(spec if spec else request)",
    "        raise Exception(f\"Handler for action '{request.action}' not found\")\n"
]
for action, spec_class in registry.items():
    handler_name = action.replace(".", "_") + "_handler"
    spec_name = spec_class.__name__
    imports.add(f"from {spec_class.__module__} import {spec_name}")
    handlers.append(f"    def {handler_name}(self, spec: {spec_name}):\n        pass\n")

service_code = "\n".join(imports) + "\n\nclass Service:\n" + "\n".join(handlers)
with open("service.py", "w", encoding="utf-8") as f:
    f.write(service_code)

print("validator.py and service.py were generated successfully!")
EOF
