# ### Initial realase of Haxall https://github.com/haxall/haxall
# ### Create a clean Ubuntu container with Haxall 1.0.76 ###
# ### Author: Chris Weyandt (cweyandt@lbl.gov)
# ### Date: 2021-06-09

# Load base image from Ubuntu
FROM ubuntu

# Basic updating & utility installation
RUN apt update
RUN apt install -y wget unzip vim-tiny default-jdk 
RUN apt install -y git


# Install Fantom
# https://fantom.org/doc/docTools/Setup

WORKDIR /tmp
RUN wget https://github.com/fantom-lang/fantom/releases/download/v1.0.76/fantom-1.0.76.zip
RUN mkdir /apps
RUN unzip fantom-1.0.76.zip -d /apps/
WORKDIR /apps/fantom-1.0.76/
RUN chmod +x ./adm/unixsetup
RUN ./adm/unixsetup
ENV PATH=${PATH}:/apps/fantom-1.0.76/bin


# Build Haystack-Defs
WORKDIR /
RUN git clone https://github.com/Project-Haystack/haystack-defs.git
WORKDIR /haystack-defs
RUN touch fan.props
RUN ./src/build.fan

# Build Haxall
WORKDIR /
RUN git clone https://github.com/haxall/haxall.git
WORKDIR /haxall
RUN echo path=/haystack-defs > fan.props
ENV FAN_BUILD_JDKHOME=/usr/lib/jvm/java-11-openjdk-amd64/
RUN ./src/build.fan

