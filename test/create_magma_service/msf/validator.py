import yaml
from spec.registry import registry
from pydantic import ValidationError

class Validator:
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
