[![codecov](https://codecov.io/gh/kumy/docker-leash/branch/master/graph/badge.svg)](https://codecov.io/gh/kumy/docker-leash)
[![Build Status](https://travis-ci.org/kumy/docker-leash.svg?branch=master)](https://travis-ci.org/kumy/docker-leash)
[![Documentation Status](https://readthedocs.org/projects/docker-leash/badge/?version=latest)](http://docker-leash.readthedocs.io/en/latest/?badge=latest)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/444467f3204246318ddc8a1af5af89bc)](https://www.codacy.com/app/docker-leash/docker-leash?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=kumy/docker-leash&amp;utm_campaign=Badge_Grade)

# docker-leash
An AuthZ plugin to enforce granular rules for a Docker multiuser environment

# Launch the server

  gunicorn --workers=1 --bind=0.0.0.0:65000 --chdir=/srv/docker-leash --reload app.leash_server:app  

# Run the tests

  nosetests -v --with-coverage --cover-inclusive --cover-html --cover-package=app --with-watch tests/
