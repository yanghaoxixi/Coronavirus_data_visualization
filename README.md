# Coronavirus_data_visualization
This is a project about visualization of Covid-19 data.
## Brief intro
- resulting.py is the script to create bokeh visualization.
- requirement.txt is the list of packages that need to install before run the visualization.

## Coronavirus Tracker
### Step 1: create virtual environment and activate it
- `pip install virtualenv` to install package of virtual environment
- `py -m venv dsci560H5` to create a virtual environment called dsci560H5
- `.\dsci560H5\Scripts\activate` to activate the virtual environment for implement scripts.
![screenshot](/screenshot/activate.png)

### Step 2: Install the dependencies and save in requirement.txt
- `pip install pandas` and `pip install bokeh `to install package pandas and bokeh for visualization
![screenshot](/screenshot/bokeh_install.png)
![screenshot](/screenshot/pandas_install.png)
- `pip freeze > requirements.txt` to save dependencies
![screenshot](/screenshot/requirements.png)

### Step 3: Run the script using bokeh serve to do visualization
- `bokeh serve --show resulting.py` to start bokeh server and run scripts.
- screenshot for cmd
![screenshot](/screenshot/run.png)
- Then go to localhost:5006/resulting to see the result of visualization
- screenshot for visualization
![screenshot](/screenshot/visua.png)

## Serving visualization through Docker
- Install docker desktop in https://www.docker.com/products/docker-desktop.
- `docker build -t Coronavirusdatavisualization` to build docker using Dockerfile
- Run docker image and bokeh server
```
docker run -p 5006:5006 -it Coronavirusdatavisualization
```
- Then go to http://localhost:5006/resulting to see the result of visualization
