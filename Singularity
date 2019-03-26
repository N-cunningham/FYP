Bootstrap: docker
From: tensorflow/tensorflow:1.9.0-gpu-py3

%environment
  # use bash as default shell
  SHELL=/bin/bash
  export SHELL

%setup
  # runs on host - the path to the image is $SINGULARITY_ROOTFS

%post
  # post-setup script

  # load environment variables
  . /environment

  # use bash as default shell
  echo 'SHELL=/bin/bash' >> /environment

  # make environment file executable
  chmod +x /environment

  # default mount paths
  mkdir /scratch /data

  # additional packages
  apt-get update
  apt-get install -y python-tk
  apt-get install -y python3-numpy python3-scipy
  apt-get install -y python3-pip python3-dev build-essential


  pip install scikit-learn
  pip install nltk
  pip install matplotlib

%runscript
  # executes with the singularity run command
  # delete this section to use existing docker ENTRYPOINT command

%test
  # test that script is a success
