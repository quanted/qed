FROM daskdev/dask

RUN apt update && apt install firefox-esr -y
  
RUN pip install selenium matplotlib pymongo distributed bokeh==0.13

CMD ["dask-worker", "dask_scheduler:8786"]
