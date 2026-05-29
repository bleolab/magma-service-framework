# magma-service-framework

Magma Service Framework is a dynamic, gRPC-based Python microservice chassis. It automatically generates input validation (using Pydantic) and service handler stubs based on a central registry of specifications (`spec/registry.py`). This allows developers to focus purely on business logic without worrying about boilerplate gRPC server setup, request validation, or routing.

## Usage

To initialize a new Magma service in your current directory, run the following commands:

```bash
curl -L https://github.com/bleolab/magma-service-framework/tarball/main -o magma-service-framework.tar.gz
tar -zxvf magma-service-framework.tar.gz --strip-components=1
rm magma-service-framework.tar.gz

magma-service.sh

rm magma-service.sh
rm README.md
rm -rf tests
```
