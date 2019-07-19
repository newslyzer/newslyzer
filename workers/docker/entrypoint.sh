#!/bin/sh

celery worker -A newslyzer.workers.celery $*
