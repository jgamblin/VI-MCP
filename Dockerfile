# Use the official Python 3.13 image as the base image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the MCP server
EXPOSE 8000

# Command to run the MCP server
CMD ["mcpo", "--port", "8000", "--", "python3", "vi-mcp.py"]