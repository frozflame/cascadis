Cascadis
=========

A simple content-addressed storage service.

Install with `pip`:

    pip install cascadis

For deployment, you may want to use `gunicorn`:

    pip install gunicorn
    gunicorn -w 8 cascadis.api:app -b 0.0.0.0:16000 
