# MEaSUREs Strain Rates
## _Generating Strain Rate Products from MEaSUREs Antarctic data_

[![Dockerized](https://github.com/jlinick/measures_strain_rate/docker/docker_logo.svg)](https://github.com/jlinick/measures_strain_rate)

Repository for retrieving, merging, & generating strain rate data from MEaSUREs data. Uses iceutils [https://github.com/bryanvriel/iceutils](https://github.com/bryanvriel/iceutils) for strain rates.

-----

## 1. Setting Up Your Environment


### Create a Earthdata Account
To download the MEaSUREs data, you need the proper earthdata credentials (even though data is stored at nsidc.org). If you don't have an account, create an Earthdata account at [https://urs.earthdata.nasa.gov/users/new](https://urs.earthdata.nasa.gov/users/new). Edit your netrc file, and add your username and credentials by running:
```sh 
echo machine nsidc.org login YOUR_USERNAME password YOUR_PASSWORD >> ~/.netrc
chmod 600 ~/.netrc
```
With your username and pasword.

### Install Docker/Git
We recommend you install [Docker](https://www.docker.com/) to build your environment. You can run these scripts by installing all the dependencies manually, but this will greatly simplify the process, make things run reliably, and keep your working environment clean. If you have docker and git installed, you can go to the next step.

Install docker for your OS by going to [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/). Install Git by going to [https://git-scm.com/book/en/v2/Getting-Started-Installing-Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)


### Clone & Build
Now we can clone this repository and build the container by running the following:

```sh
git clone https://github.com/jlinick/measures_strain_rate
cd measures_strain_rate
./run_container.sh
```

This should build your docker container, and jump you into it. You should see a terminal prompt similar to the following:

```sh
🐳 root@8bb695fe4064:/measures_strain_rate#
```
You can exit your docker container with the command ```exit```. Once outside the container, you can jump back into a container by running the ```run_container.sh``` script. This mounts all the volumes and the netrc file properly.

## Manual Option

If you want to manually build your container, cd into the repository and run:
```docker build --no-cache -t measures_strain_rate:0.0.1 -f $(pwd)/docker/Dockerfile .```

To manually jump into the container, run:
```docker run --rm -ti -v $(echo ${HOME})/.netrc:/root/.netrc -v $(pwd)/MEaSUREs:/data -v $(pwd):/measures_strain_rate -v $(pwd)/products:/products measures_strain_rate:0.0.1 /bin/bash```


-----

## 2. Retrieving MEaSUREs data

The urls for MEaSUREs Antarctic products are located in MEaSUREs/files.txt. To retrieve all the MEaSUREs products, run
```sh
./download.sh
```

This will retrieve all the products and put them under the MEaSUREs subdirectory. To compile the products in the main subdirectory, run
```sh
./move.sh
```

You should now have a series of Antarctica\*.nc files in your MEaSUREs directory

-----

## 3. Merge Products

To generate a mean product, or merge the series of products into one netcdf, run

```sh
./gen_mean.py
```

This generates a mean.nc file in your products directory. The mean for each variable is taken over the time dimension, unless mean is specified as False. Cropping can be applied by giving ((UL), (LR)) coordinates to the crop_bounds variable (an example is shown).

-----

## 4. Generate Strain Rates

To generate strain rate products, run:

```sh
./gen_strain_rate.py
```

This will use iceutils to generate strain rate, save the output to products/strain.nc, and then generate a series of output plots for various strain rate and velocity products over your region.

