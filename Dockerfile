FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi uvicorn pydantic openai pyyaml
COPY . .
EXPOSE 7860
CMD ["python", "-c", "from server.app import main; main()"]
