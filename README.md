# Pokemon Crawler

Project started from https://docs.docker.com/compose/django/

Some useful commands:

* `docker-compose up` (1)
* `docker-compose exec web bash` (2)
* `docker-compose exec web python -m pip install -r requirements.txt` (3)

** Alvee's changes **
- Used `aiohttp` to fetch data from the API asynchronously. 
- Stored name, weight, and height for each of the pokemons. For simplicity, decided not to store abilities and other complex attributes.
- Presented the crawled data through Django Administration

** Instructions for running the program ** 
- Execute the commands 1 and 3 from the list of docker-compose commands above.
- Run `python manage.py migrate` to do the migration
- Create a superuser by running `python manage.py createsuperuser` and following the instructions.
- Run `python manage.py catch_pokemons` to start the crawling.
- After the crawling ends with success, find the populated data in DB through Django Admin.

