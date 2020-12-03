FROM continuumio/miniconda3
EXPOSE 5000
WORKDIR /app
ENV FLASK_APP=app.py
RUN conda install -c conda-forge librosa=0.8.0 
RUN conda install -c conda-forge ffmpeg=4.3.1
RUN conda install -c conda-forge flask=1.1.2
RUN conda install -c conda-forge numpy=1.19.2
RUN conda install pytorch=1.6.0 torchvision=0.7.0 cpuonly -c pytorch
RUN pip install boto3==1.16.6
RUN pip install pywebaudioplayer==0.0.5

RUN echo starting the Flask service...
COPY . /app
ENTRYPOINT [ "flask"]
CMD [ "run", "--host", "0.0.0.0" ]