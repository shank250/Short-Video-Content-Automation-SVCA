# Base image
FROM mcr.microsoft.com/windows/servercore:ltsc2019

# Install Firefox (modify this based on the specific installation method for Windows)

# Install Python and pip
RUN ["powershell", "Invoke-WebRequest", "https://www.python.org/ftp/python/3.9.5/python-3.9.5-amd64.exe", "-OutFile", "python-installer.exe"]
RUN ["powershell", "Start-Process", "python-installer.exe", "/quiet", "/norestart"]
RUN ["powershell", "Remove-Item", "python-installer.exe"]

# Set working directory
WORKDIR C:/app

# Copy project files
COPY . .

# Install Python dependencies
RUN ["powershell", "pip", "install", "-r", "requirements.txt"]

# Set entry point
CMD ["python", "main.py"]
