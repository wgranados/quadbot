# Setup 

## Depedendecies
### Docker
This project wraps core components in docker and makes use of other useful components as microservces.
### Python
- Python 3.5+. No plans are made to make this support earlier versions. We make use of async
- [PIP](https://pip.pypa.io/en/stable/). Package manager for python
## Guide
1. Follow the instructions in `details-example.yaml` to configure your bot for login
2. Build searx using `docker-compose build searx`
2. Run using `docker-compose up -d`

## Testing
3. (optional) Test for errors you can run ``test.sh`` using ``chmod +x test.sh && ./test.sh``



