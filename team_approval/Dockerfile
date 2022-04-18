FROM ubuntu:latest

COPY team_approval/apt-requirements.txt /tmp/apt-requirements.txt
COPY team_approval/python-requirements.txt /tmp/python-requirements.txt

RUN apt-get update -y
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install -y `cat /tmp/apt-requirements.txt`

RUN python3.10 -m ensurepip --upgrade
RUN python3.10 -m pip install -r /tmp/python-requirements.txt

RUN mkdir -p /workdir
COPY team_approval/get_team_approval_status.py /workdir/get_team_approval_status.py
WORKDIR /workdir

ENTRYPOINT ["python3.10", "get_team_approval_status.py"]
