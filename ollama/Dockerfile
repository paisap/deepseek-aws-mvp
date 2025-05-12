FROM nvidia/cuda:12.2.2-base-ubuntu22.04

RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://ollama.com/install.sh | sh

# Pre-descargar el modelo (opcional)
#COPY ./models /root/.ollama/models
#RUN ollama pull deepseek-r1:14b

EXPOSE 11434
CMD ["ollama", "serve"]