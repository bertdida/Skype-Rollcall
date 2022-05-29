# Skype-Rollcall

Main use of this is for workgroups or in a classroom setting, so the Advisor/HR could rollcall without checking each chat to find who did not reply.

## Requirements

- [Python 3.9](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today)
- [PostgreSQL](https://www.postgresql.org/download/)

## Running the app

1. Install dependencies; `pipenv install`.
2. Activate Pipenv shell; `pipenv shell`.
3. In PostgreSQL pgAdmin, create a database named rollcall.
4. Rename `.env.example` to remove _.example_.

   4.1. Set `SKYPE_USERNAME` and `SKYPE_PASSWORD`.

   4.2. Set `DATABASE_URL` to your database's [connection string](https://stackoverflow.com/q/3582552/8062659).

   4.3. Optionally set `COMMAND_PREFIX` to the value you want your command to start with, ex. `COMMAND_PREFIX=:`.

5. Run migration; `alembic upgrade head`.
6. Start the app; `python run.py`.

## Setting up Skype

1. Login to your Skype account, this is the account you used on the `.env` file.
2. Create a group chat and invite users.
3. Send `:ping:`. Your account should send `pong` automatically.
4. By default, your account is the only account that can utilize the commands. You can add others by sending `:admin @firstadmin @secondadmin`.

## Deployment

This app is using Heroku for deployment. Run `git push heroku master` to deploy your changes.

### Relevant Links

- [Installing Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli)
- [Deploying dockerized app using heroku.yml](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml)
- [Adding environment variables in Heroku](https://devcenter.heroku.com/articles/config-vars)
