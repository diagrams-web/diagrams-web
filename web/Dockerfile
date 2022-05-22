FROM alpine:3.15

RUN apk update && apk add --no-cache \
  gcc libc-dev g++ graphviz python3 py-pip python3-dev ttf-opensans curl fontconfig npm

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

# add diagrams-xtd
RUN pip3 install diagrams-0.21.1.2.tar.gz

# add fonts to support CJK languages
RUN curl -O https://noto-website.storage.googleapis.com/pkgs/NotoSansCJKjp-hinted.zip \
&& mkdir -p /usr/share/fonts/NotoSansCJKjp \
&& unzip NotoSansCJKjp-hinted.zip -d /usr/share/fonts/NotoSansCJKjp/ \
&& rm NotoSansCJKjp-hinted.zip \
&& fc-cache -fv

# install editor library
RUN npm install --prefix ./static/js ace-builds@1.4.14

ENTRYPOINT ["python3"]
CMD ["app.py"]
