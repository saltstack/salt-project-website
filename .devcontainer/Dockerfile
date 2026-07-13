FROM python:3.14

RUN apt update && apt upgrade -y && apt install vim -y

# Add dev requirements
#ADD requirements.txt /tmp/
#RUN pip3 install -r /tmp/requirements.txt
#RUN rm /tmp/requirements.txt

# Install Hugo
RUN curl -fsSL https://github.com/gohugoio/hugo/releases/download/v0.163.0/hugo_0.163.0_linux-amd64.deb -o /tmp/hugo.deb
RUN apt-get install /tmp/hugo.deb -y

# Help avoid "unsupported locale setting" in Sphinx
RUN echo "export LC_ALL=C.UTF-8" > ~/.bashrc
