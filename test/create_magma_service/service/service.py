from spec.sample_spec import SampleSpec

class Service:
    def execute(self, request, spec=None):
        handler_name = request.action.replace('.', '_') + '_handler'
        handler = getattr(self, handler_name, None)
        if handler:
            return handler(spec if spec else request)
        raise Exception(f"Handler for action '{request.action}' not found")

    def sample_spec_handler(self, spec: SampleSpec):
        pass
