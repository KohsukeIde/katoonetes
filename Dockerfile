# Use the python base image
FROM python:3.10.5-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY . .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which FastAPI runs (by default, it's 8000)
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
