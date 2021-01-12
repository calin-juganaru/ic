LDFLAGS = -lcrypto
CXXFLAGS = -std=c++20

.PHONY: all
all: birthday

birthday: birthday.cpp
	g++ $< -o $@ $(CXXFLAGS) $(LDFLAGS)

.PHONY: clean
clean:
	rm -vf *.o birthday
