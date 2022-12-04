FROM python:3.8.15-slim-buster
WORKDIR /home
COPY ./requirements.txt ./
RUN \
apt-get update && \
apt-get upgrade -y && \
apt-get autoremove -y && \
apt-get clean -y && \
pip install --upgrade pip && \
pip install wheel && \
pip install -r requirements.txt
EXPOSE 8500
CMD ["streamlit", "run", "src/streamlit.py", "--server.port", "8500"]