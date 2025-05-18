FROM continuumio/miniconda3

RUN apt-get update && apt-get install -y \
    bash \
    curl \
    grep \
    coreutils \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN conda create -n bio -y \
    python=3.10 \
    blast \
    bwa \
    samtools \
    bowtie2 \
    hisat2 \
    salmon \
    kallisto \
    fastqc \
    cutadapt \
    && conda clean -a

SHELL ["conda", "run", "-n", "bio", "/bin/bash", "-c"]

WORKDIR /workspace

CMD [ "bash" ] 
