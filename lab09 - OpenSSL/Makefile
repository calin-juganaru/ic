LDFLAGS = -lcrypto -ldl
CPPFLAGS = -std=c++17 -O3 -Wall -g

build: lab9.cpp
	g++ $(CPPFLAGS) $< -o aesgcm $(LDFLAGS)

.PHONY: clean
clean:
	rm -vf *.o aesgcm