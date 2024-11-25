import grpc_tools.protoc
grpc_tools.protoc.main(['protoc', '-I.', '--python_out=./pb', '--grpc_python_out=./pb', 'auth.proto'])