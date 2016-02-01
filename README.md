SocialCode DR Insights

Getting Started:

1. Make sure you have the [docker toolbox](https://www.docker.com/products/docker-toolbox) installed.

2. Install `scarab` (`npm install -g jesseditson/scarab`)

3. Run `scarab hosts` to add `socialcode.dev` to your hostsfile and initialize the socialcode docker machine

4. Copy `.env.example` to `.env`, and add a valid google client id

5. Run `scarab start && scarab logs django`

6. Open http://socialcode.dev

Running:

- To start, run `scarab start`
- To stop, run `scarab stop`
- To tail the django logs, run `scarab logs django`
- To tail the logs from the proxy, run `scarab logs scarab`
- To tail the full logs, run `scarab compose logs`

Troubleshooting:

- Server isn't starting

> Try shutting down the server, and running `scarab compose up` - this will start the server in the foreground, so you can see all the logs. Likely an exception is thrown.

- Google login doesn't work

> Make sure you specify a valid client ID in .env. When you change `.env`, you'll need to restart the docker container by running `scarab stop` then starting the server again.

> Note that the google client ID must allow socialcode.dev as a valid client app. The first client ID in the chef config files should work.

- Can't run (some docker command)

> To run standard docker commands, first associate with the socialcode docker-machine by running `eval $(scarab env)`. Then you should be able to run things like `docker ps` or `docker images` to see the generated containers and images. To run compose commands, just use `scarab compose` instead of `docker-compose`.
