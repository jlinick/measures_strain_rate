FROM osgeo/gdal:latest
MAINTAINER jlinick@mit.edu

ENV DEBIAN_FRONTEND=non-interactive

# Set the working directory
ENV CODE=/measures_strain_rate
ENV DATA=/data
ENV PRODUCTS=/products
ENV WORKDIR=${CODE}

WORKDIR ${WORKDIR}
#ENV HOME=${WORKDIR}

# Set the data directory
ENV DATA=/data

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y \
     python3-pip coreutils zip unzip git \
     vim imagemagick ffmpeg libgeos-dev

# clone and build iceutils repo and requirements
ENV ICEUTILS=/iceutils
RUN git clone https://github.com/bryanvriel/iceutils.git ${ICEUTILS}

RUN pip3 install numpy scipy matplotlib h5py pyproj \
    scikit-learn scikit-image tqdm pint pymp-pypi \ 
    pint xarray pylint pandas simplekml pillow geopandas \
    netcdf4 setuptools dask toolz opencv-python basemap \
    cartopy datashader h5netcdf numba bokeh cvxopt

RUN pip3 install ${ICEUTILS}

RUN echo "PS1='🐳 \e[1;32m\]\u@\e[m\]\e[1;31m\]\h\e[m\]:\e[1;34m\]\w\e[m\]\\$ '" >> ~/.bashrc
