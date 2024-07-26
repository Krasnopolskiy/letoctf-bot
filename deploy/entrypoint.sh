#!/bin/bash

alembic -c bot/alembic.ini upgrade head

exec "$@"
