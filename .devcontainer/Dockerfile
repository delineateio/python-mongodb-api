ARG VARIANT="3.10-bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

ENV INSTALL_DIR /installs

ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

RUN apt-get update && \
    apt install -y httpie

COPY /.devcontainer/.bash_aliases /home/vscode/

# pip installs --------------------------------------------------------------------

COPY /.devcontainer/requirements.txt /usr/
RUN pip install --upgrade pip && pip install --upgrade pip && pip install -r /usr/requirements.txt

# init ---------------------------------------------------------------------------

RUN echo "task init" | tee -a /home/vscode/.bashrc >> /home/vscode/.zshrc
