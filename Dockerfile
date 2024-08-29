FROM ubuntu:22.04

RUN apt update -y;
RUN apt install python3.10 -y && apt install python3-pip -y && apt install python3-venv -y;

WORKDIR ~/app

COPY . .

RUN python3 -m venv ./venv; python3 -m pip install -r ./requirements.txt;

CMD ["python3", "tui.py"]


