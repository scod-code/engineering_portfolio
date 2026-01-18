# Detect operating system
ifeq ($(OS),Windows_NT)
    # Windows
    OS_NAME := Windows
    ifeq ($(PROCESSOR_ARCHITECTURE),AMD64)
        # Windows 64-bit
        ARCH := x64
    endif
    ifeq ($(PROCESSOR_ARCHITECTURE),x86)
        # Windows 32-bit
        ARCH := x86
    endif
else
    # macOS or Linux
    OS_NAME := $(shell uname -s)
    ARCH := $(shell uname -m)
endif

# Set the appropriate compiler and flags based on OS and architecture
ifeq ($(OS_NAME),Windows)
    ifeq ($(ARCH),x64)
        CXX := g++
        CXXFLAGS := -Wall -std=c++17 -w -m64
    endif
    ifeq ($(ARCH),x86)
        CXX := g++
        CXXFLAGS := -Wall -std=c++17 -w -m32
    endif
else ifeq ($(OS_NAME),Darwin) # macOS
    CXX := g++
    CXXFLAGS := -Wall -std=c++17 -w
    ifeq ($(ARCH),arm64) # ARM Mac
        CXXFLAGS += -arch arm64
    endif
else
    # Other OS (e.g., Linux)
    CXX := g++
    CXXFLAGS := -Wall -std=c++17 -w
endif

LIBS=
INCLUDES=-I./stb_image
SRC=./src/Image.cpp ./src/Matrix.cpp ./src/main.cpp
OBJS=$(SRC:.cpp=.o)

TARGET=main

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $(INCLUDES) $^ -o $@ $(LIBS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

