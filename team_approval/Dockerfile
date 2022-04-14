FROM rockylinux:latest

COPY team_approval/yum-requirements.txt /tmp/yum-requirements.txt
COPY team_approval/python-requirements.txt /tmp/python-requirements.txt

RUN yum update -y
RUN yum install -y epel-release
RUN yum install -y `cat /tmp/yum-requirements.txt`

RUN python3 -m ensurepip --upgrade
RUN python3 -m pip install -r /tmp/python-requirements.txt

COPY team_approval/get_team_approval_status.py /usr/bin/

ENTRYPOINT ["get_team_approval_status.py"]