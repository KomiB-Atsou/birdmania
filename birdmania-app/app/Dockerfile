# https://docs.anaconda.com/working-with-conda/applications/docker/
FROM continuumio/miniconda3
EXPOSE 5000
WORKDIR /app
ENV FLASK_APP=app.py
# RUN conda config --set solver classic
RUN conda update conda
# RUN conda install -c conda-forge conda-libmamba-solver libarchive
# RUN conda install -c conda-forge librosa
# RUN conda install -c conda-forge ffmpeg
# RUN conda install -c conda-forge libarchive
RUN conda install -c conda-forge flask=1.1.2
RUN conda install -c conda-forge numpy
RUN conda install pytorch torchvision torchaudio cpuonly -c pytorch
RUN pip install boto3
RUN pip install pywebaudioplayer

RUN echo starting the Flask service...
COPY . /app
ENTRYPOINT [ "flask"]
CMD [ "run", "--host", "0.0.0.0" ]