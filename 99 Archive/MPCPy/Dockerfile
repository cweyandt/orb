# starting with https://hub.docker.com/r/michaelwetter/ubuntu-1804_jmodelica_trunk
FROM michaelwetter/ubuntu-1604_jmodelica_trunk

ENV ROOT_DIR /usr/local
ENV JMODELICA_HOME $ROOT_DIR/JModelica
ENV IPOPT_HOME $ROOT_DIR/Ipopt-3.12.4
ENV SUNDIALS_HOME $JMODELICA_HOME/ThirdParty/Sundials
ENV SEPARATE_PROCESS_JVM /usr/lib/jvm/java-8-openjdk-amd64/
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
ENV PYTHONPATH $PYTHONPATH:$JMODELICA_HOME/Python:$JMODELICA_HOME/Python/pymodelica

ENV MODELICAPATH=$JMODELICA_HOME/ThirdParty/MSL
# ENV PYTHONPATH=$PYTHONPATH:$JMODELICA_HOME/Python
# ENV PYTHONPATH=$PYTHONPATH:$JMODELICA_HOME/Python/pymodelica
ENV PYTHONPATH=$PYTHONPATH:$HOME/EstimationPy
ENV PYTHONPATH=$PYTHONPATH:$HOME/MPCPy

USER root

WORKDIR $HOME

RUN pip install --user flask-restful

RUN apt update 
RUN apt install -y wget unzip vim-tiny git
RUN apt-get install -y libgeos-dev 
# RUN apt-get install -y texlive texlive-formats-extra latexmk

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN git clone https://github.com/lbl-srg/EstimationPy.git
RUN git clone https://github.com/lbl-srg/MPCPy.git

# COPY . .

# CMD [ "python", "./your-daemon-or-script.py" ]




