FROM ubuntu:16.04

MAINTAINER AMIGOML

ENV TZ=Europe/Moscow
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
  && apt-get update -q && apt-get upgrade -y -q \
  && apt-get install -y -q --no-install-recommends libcurl4-openssl-dev \
                                              libssl1.0.0 \
                                              build-essential \
                                              cmake \
                                              curl \
                                              wget \
                                              vim \
                                              ca-certificates \
  && apt-get clean \
  && rm -rf /tmp/* /var/tmp/* \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
RUN chmod -R 777 /workspace
COPY ../requirements.txt /workspace

RUN curl -o ~/miniconda.sh -O  https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh  && \
     chmod +x ~/miniconda.sh && \
     ~/miniconda.sh -b -p /usr/conda && \
     rm ~/miniconda.sh && \
     ln -s /usr/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
     echo ". /usr/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
     /usr/conda/bin/conda create -y --name py3 python=3.6 numpy scipy pandas scikit-learn matplotlib joblib tqdm ipython pip && \
     /usr/conda/bin/conda clean -ya && \
     /usr/conda/envs/py3/bin/pip install -r /workspace/requirements.txt && \
     echo "conda activate py3" >> ~/.bashrc

CMD ["/bin/bash"]