FROM python:3.13.7-slim

WORKDIR /app

RUN python -m pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python --version

RUN pip install -e .


# Expose the port your NiceGUI app runs on (default is 8080)
EXPOSE 8001

# Set the default command to run the NiceGUI app
CMD ["python", "src/project/main.py"]

# docker build -t fearless_ferns_image .
# docker run -dit --name fearless_ferns -p8081:8081 fearless_ferns_image
