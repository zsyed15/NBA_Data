FROM mageai/mageai:latest

# Install to opt directoyr
ENV INSTALL_DIR=/opt

# Create spark directory for installation
RUN mkdir -p ${INSTALL_DIR}/spark

RUN wget -qO- https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz | tar xvz -C ${INSTALL_DIR}/spark

#Set Java Home and Path for installation
ENV JAVA_HOME=${INSTALL_DIR}/spark/jdk-11.0.2
ENV PATH=${JAVA_HOME}/bin:${PATH}

# Download Spark and set Spark and Path Environment variables
RUN wget -qO- https://archive.apache.org/dist/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz | tar xvz -C ${INSTALL_DIR}/spark
ENV SPARK_HOME=${INSTALL_DIR}/spark/spark-3.3.2-bin-hadoop3
ENV PATH=${SPARK_HOME}/bin:${PATH}

#Set Path for PySpark
ENV  PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
ENV  PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"

COPY requirements.txt ${USER_CODE_PATH}requirements.txt
RUN pip3 install -r ${USER_CODE_PATH}requirements.txt

WORKDIR /home/src
