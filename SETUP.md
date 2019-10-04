# Setup 

If you're fortunate enough to have found this website, then you're one of the select few who may be intersted in running it and seeing it in action! (I hope). Thankfully if you have docker installed and follow some simple steps, you too can now run a quadbot!

## Dependencies

### Docker
This project wraps core components in docker and makes use of other useful components as microservces.
### Python
- Python 3.5+. No plans are made to make this support earlier versions. We make use of async
- [PIP](https://pip.pypa.io/en/stable/). Package manager for python
## Guide
1. Follow the instructions in `details-example.yaml` to configure your bot for login
2. Build searx using `docker-compose build searx`
2. Run using `docker-compose up -d searx quadbot_ps`


# Documentation
Several things are documented on [this website](https://wgma.ca/quadbot), you can update this documention by installing the pydocmd depedency in ``requirements.txt`` and updating the respective yaml file. Then you can finally use ``pydocmd serve`` to see your changes.