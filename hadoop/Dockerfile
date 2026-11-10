FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jdk-headless \
    python3 python3-pip \
    openssh-server openssh-client \
    wget curl ca-certificates procps \
    && rm -rf /var/lib/apt/lists/*

ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH

RUN wget -q https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz \
    && tar -xzf hadoop-${HADOOP_VERSION}.tar.gz -C /opt \
    && mv /opt/hadoop-${HADOOP_VERSION} $HADOOP_HOME \
    && rm hadoop-${HADOOP_VERSION}.tar.gz

RUN useradd -m -s /bin/bash hadoop && \
    mkdir -p /home/hadoop/.ssh && \
    chown -R hadoop:hadoop /home/hadoop/.ssh && \
    chmod 700 /home/hadoop/.ssh

RUN mkdir -p /var/run/sshd

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 22

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/usr/sbin/sshd", "-D"]