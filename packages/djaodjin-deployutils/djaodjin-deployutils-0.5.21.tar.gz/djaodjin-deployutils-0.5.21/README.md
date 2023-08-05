DjaoDjin deployutils
====================

This Django app enables a Django project to seamlessly integrate behind
the [DjaoDjin HTTP session manager reverse proxy](https://github.com/djaodjin/djaoapp).
It will replace the default ``django.contrib.sessions``
and ``AUTHENTICATION_BACKENDS`` to decode sessions forwarded to your Django
project by the HTTP session manager.

[More technical documentation](https://djaodjin.com/docs/technical/)

Install
-------

Install deployutils into your environment


    $ pip install djaodjin-deployutils


Create a ``credentials`` file that contains the ``DJAODJIN_SECRET_KEY``.
(You can also pass ``DJAODJIN_SECRET_KEY`` as a shell environment variable.)


    $ cat ./credentials
    # Authentication for djaodjin firewall
    DJAODJIN_SECRET_KEY = "__your_secret_key__"


(for stand-alone testing) Add the mockup views in urls.py


Development
-----------

Clone the repository in a virtualenv and install the prerequisites


    $ virtualenv _installTop_
    $ cd _installTop_
    $ source bin/activate
    $ git clone https://github.com/djaodjin/djaodjin-deployutils.git
    $ cd djaodjin-deployutils
    $ pip install -r testsite/requirements.txt


Create the credentials file with a ``DJAODJIN_SECRET_KEY`` and the empty db.


    $ make initdb


Run the web application


    $ python manage.py runserver


Browse to http://localhost:8000



Bonus commands
--------------

Commands to upload/download resources
-------------------------------------


    $ python manage.py download_resources
    $ python manage.py upload_resources


Not all assets are stored under source control. Images, videos, etc. are
better kept outside the git repository. These two commands are used to
download the extra resources into the webapp htdocs/ directory from
the stage server and upload them from the webapp htdocs/ directory to
the stage server respectively.

Commands to setup on deployed servers
-------------------------------------


    $ python manage.py pullapp


Fetch/merge from the remote git repository and downlad the extra resources
from the stage server.

Using configuration files from a S3 bucket
------------------------------------------


    $ python manage.py upload_configs --location s3://__example__ credentials site.conf
