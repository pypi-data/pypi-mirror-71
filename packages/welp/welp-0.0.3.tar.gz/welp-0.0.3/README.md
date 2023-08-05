# welp

## Development

### Get a Yelp! fusion API key

[here](https://www.yelp.com/fusion)

Add it to your .env file

```
echo "YELP_API_KEY=<api_key>" >> .env
```

### Get a Google Maps Geolocation API Key. Should be free for most general users.

### Use Pyenv

Yeah just do it. 3.8.2.

### Install pipenv using brew on mac or linux
```bash
brew install pipenv
```

### Enter the pipenv virtual environment
```bash
pipenv shell
```

### Install and build welp app in venv
```bash
pipenv install      # installs python dependencies
pipenv run build    # builds the python project
pipenv run install  # installs the project locally
```

### Run it!
```bash
welp
```