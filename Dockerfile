FROM continuumio/miniconda3

RUN apt-get update && apt-get install -y \
  gcc 
  
RUN git clone https://github.com/yanghaoxixi/Coronavirus_data_visualization

RUN conda install -c conda-forge yarn

RUN cd Coronavirus_data_visualization && yarn install

COPY requirements.txt .

RUN pip install -r requirements.txt

ADD resulting.py /

EXPOSE 5006

WORKDIR Coronavirus_data_visualization

CMD ["bokeh", "serve", "--show", "resulting.py"]
