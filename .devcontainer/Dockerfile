FROM python:3.14

RUN apt update && apt upgrade -y && apt install vim -y

# Add dev requirements
#ADD requirements.txt /tmp/
#RUN pip3 install -r /tmp/requirements.txt
#RUN rm /tmp/requirements.txt

# Install Hugo (extended). Version is pinned in .hugo-version at the repo
# root — the same file .github/actions/setup-hugo reads in CI — so the
# devcontainer and GitHub Actions never drift apart.
COPY .hugo-version /tmp/.hugo-version
RUN HUGO_VERSION="$(cat /tmp/.hugo-version)" \
    && curl -fsSL "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb" -o /tmp/hugo.deb \
    && apt-get install /tmp/hugo.deb -y \
    && rm /tmp/hugo.deb /tmp/.hugo-version

# Help avoid "unsupported locale setting" in Sphinx
RUN echo "export LC_ALL=C.UTF-8" > ~/.bashrc
