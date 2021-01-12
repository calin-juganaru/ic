CC = g++ -std=c++20
FLAGS = -I/usr/local/include/openssl -L/usr/local/lib64  -lssl -lcrypto

all:
	$(CC) dhe.cpp -o dhe $(FLAGS)
	$(CC) dhe_server.cpp -o dhe_server $(FLAGS)

start_client:
	./dhe

start_server:
	./dhe_server

clean:
	rm dhe dhe_server


