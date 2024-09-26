# Instructions

## Prerequisites

1. Install Docker
    - [Windows](https://docs.docker.com/desktop/install/windows-install/)
    - [Mac](https://docs.docker.com/desktop/install/mac-install/)
    - [Linux](https://docs.docker.com/desktop/install/linux-install/)


## Set your SnowCLI connection (optional)

We use your default connection to connect to Snowflake and deploy the images / app. Set your
default connection by modifying your `config.toml` file or by exporting the following environment variable:

```sh
export SNOWFLAKE_DEFAULT_CONNECTION_NAME=<your connection name>
```

## Create image repository, build and push your local service image

The [service/](service/) directory contains a [Dockerfile](service/Dockerfile) that builds a
simple Python server that responds to GET health checks, a GET for `/index.html`, as well as
POSTing to `/echo` in the Snowflake External Function payload format. You can build it and
push it to an image repository called `SPCS_NA.PUBLIC.IMAGES` in your account like so:

```sh
./build-and-push.sh
```

This command will always use your default SnowCLI connection.

## Deploy the application

Deploy the app package and instance as such:

```sh
snow app run
```

> Take note of the name of the application, which is based on the name you chose when you initialized this project. The application object and package are, by default, automatically suffixed by your (local) user name (i.e. `$USER`).

## Setup the application

When the application is opened for the first time, you will be prompted to grant the following account-level privileges to it:

- CREATE COMPUTE POOL
- BIND SERVICE ENDPOINT

Click on the `Grant` button to proceed.

## Activate the application

Once privileges are granted, a new `Activate` button should appear. Click the button and wait until the application is fully activated.
The `Activate` button invokes the `grant_callback` defined in the [manifest.yml](app/manifest.yml) file, which then creates the `COMPUTE POOL` and `SERVICE` needed to launch the application.

## Launch the application

Once all services and pools are created, you will be able to launch the app by clicking on the `Launch App` button. This will navigate to the URL provided by the `Service` and `Endpoint` defined in the `default_web_endpoint` in the [manifest.yml](app/manifest.yml). You will see the contents of [index.html](service/index.html) as served by the application container.

## Test out the echo service

```sh
snow sql -q "select <app name>.services.echo('Hello world!')"
```

You should see the same text back (Hello world!).

## Clean up

You can stop the service and drop the compute pool without dropping the application by running the following statement:

```sh
snow sql -q "call <app name>.setup.drop_service_and_pool()"
```

Optionally, you can remove the app + package altogether afterwards:

```sh
snow app teardown --cascade
```
> Version `2.4.0+` of Snowflake CLI should be installed in order to execute `--cascade` command.
