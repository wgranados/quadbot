# Testing 

Important notes for testing, since this software makes use of microservices you will likely have to intiate these before running some tests. Likewise a large portion of this is written with asyncio so we've used an asyncio extension of pytest to do our tests. 

## Testing Search 
``docker-compose build searx && docker-compose up -d && python3 -m pytest test``

Note that there might be some slight differences in testing locally and how the software runs in production. An example can be found [here](/test/test_search.py)

## Testing in General 
``python3 -m pytest test``


