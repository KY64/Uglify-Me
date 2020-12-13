FROM fedora:31

RUN dnf install -y cmake g++ wget unzip python3-pip \
  gtk3-devel gstreamer1-devel clutter-devel \
  && wget -O opencv.zip https://github.com/opencv/opencv/archive/master.zip \
  && unzip opencv.zip && mkdir -p build && cd build \
  && cmake  ../opencv-master \
  && cmake --build . \
  && cmake --build . --target install

WORKDIR root

COPY . .

RUN pip install -r requirements.txt \
    && cd processor \
    && cmake . \
    && make

CMD ["python3", "app.py"]
