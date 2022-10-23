ARG VARIANT=1-bullseye
FROM mcr.microsoft.com/devcontainers/go:1.19-bullseye

ENV PYTHONUNBUFFERED=1
ENV INSTALL_DIR /installs
ENV TFENV_VERSION 1.3.1

# nvm -----------------------------------------------------------------------------

ARG NODE_VERSION="lts/*"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c ". /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# program installs ----------------------------------------------------------------

RUN apt update \
    && apt -y install python3-dev python3-pip nodejs npm gcc musl-dev acl
RUN curl -fLSs https://raw.githubusercontent.com/CircleCI-Public/circleci-cli/master/install.sh | bash
RUN bash -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b $INSTALL_DIR

# renames -------------------------------------------------------------------------

RUN ln -sf python3 /usr/bin/python
RUN ln -sf pip3 /usr/bin/pip
RUN ln -sf $INSTALL_DIR/task /usr/bin/task

# pip installs --------------------------------------------------------------------

COPY ./requirements.txt /usr/
RUN pip install --no-cache --upgrade pip setuptools
RUN pip install -r /usr/requirements.txt

# tfenv ---------------------------------------------------------------------------

RUN mkdir -p $INSTALL_DIR
RUN git clone --depth=1 https://github.com/tfutils/tfenv.git $INSTALL_DIR/tfenv
RUN setfacl -R -m u:vscode:rwx $INSTALL_DIR/tfenv
RUN ln -s $INSTALL_DIR/tfenv/bin/* /usr/bin
RUN tfenv install $TFENV_VERSION
RUN tfenv use $TFENV_VERSION

# init ----------------------------------------------------------------------------

RUN echo "source /home/vscode/.devcontainer.env" | tee -a /home/vscode/.bashrc >> /home/vscode/.zshrc
RUN echo "task init" | tee -a /home/vscode/.bashrc >> /home/vscode/.zshrc
