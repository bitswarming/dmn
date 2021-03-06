# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Ubuntu 18.04 (bionic) from 2018-05-26
# https://github.com/docker-library/official-images/commit/aac6a45b9eb2bffb8102353c350d341a410fb169
#FROM ubuntu:bionic-20180526@sha256:c8c275751219dadad8fa56b3ac41ca6cb22219ff117ca98fe82b42f24e1ba64e
FROM tensorflow/tensorflow:1.7.0-gpu-py3

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

USER root

# Install all OS dependencies for notebook server that starts but lacks all
# features (e.g., download as all possible file formats)
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get -yq dist-upgrade \
 && apt-get install -yq --no-install-recommends \
    wget \
    git \
    bzip2 \
    ca-certificates \
    sudo \
    locales \
    fonts-liberation \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# Install Tini
RUN wget --quiet https://github.com/krallin/tini/releases/download/v0.18.0/tini && \
    echo "12d20136605531b09a2c2dac02ccee85e1b874eb322ef6baf7561cd93f93c855 *tini" | sha256sum -c - && \
    mv tini /usr/local/bin/tini && \
    chmod +x /usr/local/bin/tini

# Configure environment
ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    NB_USER=jovyan \
    NB_UID=1000 \
    NB_GID=100 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8
ENV PATH=$CONDA_DIR/bin:$PATH \
    HOME=/home/$NB_USER

ADD fix-permissions /usr/local/bin/fix-permissions
# Create jovyan user with UID=1000 and in the 'users' group
# and make sure these dirs are writable by the `users` group.
RUN groupadd wheel -g 11 && \
    echo "auth required pam_wheel.so use_uid" >> /etc/pam.d/su && \
    useradd -m -s /bin/bash -N -u $NB_UID $NB_USER && \
    mkdir -p $CONDA_DIR && \
    chown $NB_USER:$NB_GID $CONDA_DIR && \
    chmod g+w /etc/passwd && \
    fix-permissions $HOME && \
    fix-permissions $CONDA_DIR

USER $NB_UID

# Setup work directory for backward-compatibility
RUN mkdir /home/$NB_USER/work && \
    fix-permissions /home/$NB_USER

# Install conda as jovyan and check the md5 sum provided on the download site
ENV MINICONDA_VERSION 4.5.4
RUN cd /tmp && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    echo "a946ea1d0c4a642ddf0c3a26a18bb16d *Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh" | md5sum -c - && \
    /bin/bash Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    $CONDA_DIR/bin/conda config --system --prepend channels conda-forge && \
    $CONDA_DIR/bin/conda config --system --set auto_update_conda false && \
    $CONDA_DIR/bin/conda config --system --set show_channel_urls true && \
    $CONDA_DIR/bin/conda install --quiet --yes conda="${MINICONDA_VERSION%.*}.*" && \
    $CONDA_DIR/bin/conda update --all --quiet --yes && \
    conda clean -tipsy && \
    rm -rf /home/$NB_USER/.cache/yarn && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER
#nbverai
#RUN fix-permissions "/opt"
#ENV INSTALL_PATH="/opt/JupyterLab"
#RUN mkdir -p ${INSTALL_PATH}  && fix-permissions ${INSTALL_PATH}
#COPY nbverai/nbverai  ${INSTALL_PATH}/nbverai
#RUN mkdir -p ${INSTALL_PATH} # && 
#RUN fix-permissions ${INSTALL_PATH}/nbverai
#cp -r ./nbverai ${INSTALL_PATH}
#RUN chown $NB_USER:$NB_GID ${INSTALL_PATH}
#RUN chown $NB_USER:$NB_GID ${INSTALL_PATH}/nbverai
#RUN fix-permissions ${INSTALL_PATH}/nbverai
#RUN fix-permissions ${INSTALL_PATH}
#RUN pip install --no-cache  -e ${INSTALL_PATH}/nbverai
#RUN  conda install --quiet --yes   ${INSTALL_PATH}/nbverai
#jupyter serverextension enable --py nbverai
#jupyter serverextension enable --py nbverai \
# Install Jupyter Notebook and Hub
RUN conda install --quiet --yes \
    'notebook=5.5.*' \
    'jupyterhub=0.8.*' \
    'jupyterlab=0.32.*' && \
    conda clean -tipsy && \
    jupyter labextension install @jupyterlab/hub-extension@^0.8.1 && \
    npm cache clean --force && \
    rm -rf $CONDA_DIR/share/jupyter/lab/staging && \
    rm -rf /home/$NB_USER/.cache/yarn && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

USER root

EXPOSE 8888
WORKDIR $HOME

# Configure container startup
ENTRYPOINT ["tini", "-g", "--"]
CMD ["start-notebook.sh"]

# Add local files as late as possible to avoid cache busting
COPY start.sh /usr/local/bin/
COPY start-notebook.sh /usr/local/bin/
COPY start-singleuser.sh /usr/local/bin/
COPY jupyter_notebook_config.py /etc/jupyter/
RUN fix-permissions /etc/jupyter/

# Switch back to jovyan to avoid accidental container runs as root
USER $NB_UID
#
USER root
RUN fix-permissions  /home/jovyan/.cache
#sudo chmod -R  777 /usr/local/lib/python3.5/dist-packages
ENV GRANT_SUDO=yes
ENV VERAI_DAEMON_HOST=daemon1_dev
RUN pip install numpy grpcio grpcio-tools futures gitpython
#RUN jupyter serverextension enable nbverai
#/home/joyvan/cache
#RUN pip install --upgrade pip
RUN python3 -m pip install --no-cache jupyterhub==0.8.1
RUN mkdir -p /jlab/nbverai # && fix-permissions /jlab/nbverai
#RUN chown $NB_USER:$NB_GID /jlab/nbverai
COPY jupyterLab/nbverai /jlab/nbverai
COPY jupyterLab/front-extension /jlab/front-extension
COPY localpip /veraipip
RUN chmod -R 777 /jlab
RUN chmod -R 777 /veraipip
RUN cd /jlab/front-extension && npm i
RUN cd /jlab && jupyter labextension install front-extension
#xtest
#RUN fix-permissions /jlab/nbverai
RUN cd /veraipip && pip install   -e /veraipip/pip_package/verai
RUN cd /jlab && pip install   -e /jlab/nbverai
#RUN cd /jlab && pip install  -e /jlab/nbverai
#RUN pip3 install  -e /jlab/nbverai
#RUN cd /jlab && jupyter serverextension enable --py nbverai --sys-prefix
#RUN cd /jlab && jupyter serverextension enable nbverai --sys-prefix
#RUN cd /jlab && jupyter serverextension enable --py nbverai
RUN chmod -R  777 /usr/local/lib/python3.5
RUN chmod -R  777 /opt/conda/lib
RUN chmod -R  777 /jlab
RUN chmod -R 777 /veraipip
#RUN jupyter serverextension enable  nbverai
USER $NB_UID
#RUN cd /veraipip && pip install --no-cache  -e /veraipip/pip_package/verai
#RUN cd /jlab && jupyter serverextension enable nbverai --sys-prefix
#RUN fix-permissions /jlab
#RUN fix-permissions /jlab/nbverai
#RUN cd /jlab && pip install --no-cache  -e /jlab/nbverai
#RUN cd /jlab && jupyter serverextension enable --py nbverai
#RUN fix-permissions /jlab
#RUN fix-permissions /jlab/nbverai
#RUN fix-permissions /veraipip
#RUN cd /veraipip && pip install --no-cache  -e /veraipip/pip_package/verai
#RUN jupyter serverextension enable nbverai --sys-prefix
RUN pip3 install  -e /veraipip/pip_package/verai
#RUN pip3 install  -e /jlab/nbverai
#RUN jupyter serverextension enable  nbverai
#RUN jupyter serverextension enable --py  nbverai
RUN jupyter labextension enable front-extension
USER root
RUN curl -O -L https://www.dropbox.com/s/nt7664ih508bly1/install_verai.sh?dl=0 && mv ./install_verai.sh\?dl\=0 ./install_verai.sh && chmod +x ./install_verai.sh
RUN ./install_verai.sh
RUN rm install_verai.sh
RUN python -m pip install --no-cache tensorflow-gpu
RUN pip install --no-cache tensorflow-gpu
#jlab
#/opt/conda
#/home/jovyan/.cache
