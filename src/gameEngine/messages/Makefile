# brew install protobuf  (this command will install protoc, allowing you to compile the protobuf files)
protobuf: pacmanState.proto lightState.proto
	protoc -I=./ --python_out=./ ./pacmanState.proto
	protoc -I=./ --python_out=./ ./lightState.proto
