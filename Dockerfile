############################################################
# Dockerfile to build ChronQC container images
# Based on Ubuntu
# docker pull nileshtawari/chronqc
# docker build –t chronqc_1.0.4 .
############################################################

# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER nileshtawari

# Update the repository sources list
RUN apt-get update 
RUN apt-get -y upgrade 
RUN apt-get install -y python3
RUN apt-get install -y python3-tk 
RUN apt-get install -y python3-pip
RUN cd /usr/local/bin \
RUN ln -s /usr/bin/python3 python \
RUN pip3 install --upgrade pip

RUN apt-get install -y git
RUN cd /home
RUN git clone https://github.com/nilesh-tawari/ChronQC.git
RUN pip3 install -r ChronQC/requirements.txt 
RUN pip3 install ChronQC/



#6) Share/Publish new image to Docker Cloud
#login Docker Cloud

###### sudo docker login

#Tag the image
######docker tag chronqc_1.0.4 nileshtawari/chronqc:chronqc_1.0.4
######docker push nileshtawari/chronqc:chronqc_1.0.4

#for latest image
######docker tag chronqc_1.0.4 nileshtawari/chronqc:latest
######docker push nileshtawari/chronqc:latest


