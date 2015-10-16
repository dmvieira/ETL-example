ETL Example
========

### Description


Gather and search...


### Dependencies

Ubuntu 12.04 installation

```
$ sudo apt-get install python-dev
$ sudo apt-get install libxml2-dev
$ sudo apt-get install libxslt1-dev
$ sudo apt-get install python-pip
$ sudo apt-get install catdoc
$ sudo apt-get install wkhtmltopdf
$ sudo apt-get install gtk2-engines-pixbuf

```

Make your virtualenv and...

```
$(env) pip install -r requirements.txt
```

Then run crawlers:

```
$(env) cd crawler && ./run_crawlers.sh
```

Now you can make your database connection model interface in loader/modulers/model.py

And finally load crawlers to database:

```
$(env) cd loader && ./main.py
```
