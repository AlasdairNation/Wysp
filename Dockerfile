# Building -> docker build -t <name> .
# Running ->  xhost +local:docker
#               docker run -it <name>:latest

# Use an official Python runtime as a parent image
FROM python:3.6.9

# Install Java 11 (specific version)
RUN apt-get update && apt-get install -y wget gnupg2 \
    && apt-get install -y openjdk-11-jdk \
    && apt-get clean

# Install Wine and mingw-w64 for cross-compilation
# RUN dpkg --add-architecture i386 && apt-get update && apt-get install -y \
#     wine32 \
#     wine64 \
#     wine \
#     wine-development \
#     mingw-w64 \
#     && apt-get clean

# Install required packages including Qt, Xvfb, and xcb dependencies
RUN apt-get update && apt-get install -y \
    qt5-default \
    libx11-xcb1 \
    libxrender1 \
    libxcb1 \
    libxcb-glx0 \
    libxcb-shm0 \
    libxcb-xfixes0 \
    libxcb-shape0 \
    libxcb-randr0 \
    libxcb-image0 \
    libxcb-icccm4 \
    libxcb-sync1 \
    libxcb-xinerama0 \
    libxcb-keysyms1 \
    libxcb-xkb1 \
    libqt5x11extras5 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean

# Install PyInstaller to package Python applications into .exe files
RUN pip install pyinstaller

# Set the environment variable for Java 11
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Make sure Java is in the PATH
ENV PATH="$JAVA_HOME/bin:$PATH"

# Set the working directory to /app/Main
WORKDIR /app/Main

# Copy the contents of the Main directory into /app/Main in the container
COPY Main /app/Main

# Copy requirements.txt if it exists in the root
COPY requirements.txt /app

# For windows .exe file
# COPY dockerWindows.spec /app/Main
# For linux executable
# COPY dockerLinux.spec /app/Main

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt


# Use PyInstaller to generate a Windows executable
#RUN pyinstaller --onefile --noconsole main.py

# Run the app
# Set the correct Qt plugin path
ENV QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/x86_64-linux-gnu/qt5/plugins/platforms

# Set XDG_RUNTIME_DIR to avoid warnings
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
RUN mkdir -p /tmp/runtime-root && chmod 700 /tmp/runtime-root


# Command to run the Python application
CMD ["python", "main.py"]
# Command to run the generated Windows .exe (if needed)
# You can specify a command to run the generated .exe, 
# for example to test it using Wine inside the container.
# CMD ["wine", "/app/Main/dist/main.exe"]

# Alternatively, to extract the .exe after building the container, 
# use 'docker cp' to copy the .exe from the container to your host system.
