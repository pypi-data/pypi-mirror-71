# pypi versions

Reads dependencies from local projects' requirements files and compares against the most recent version available.





The recommended way is to compile a `requirements.txt` from a `requirements.in` using `pip-compile` (`pip-tools`). later on `requirements.txt` will be install using `pip-sync`.

## Usage

Run it like this:
```
pypi_versions --requirements 1.txt 2.txt 3.txt
```

Possible output:
```
INFO:PypiVersions:Checking /.../requirements.txt.
INFO:PypiVersions:Get remote version for 'django'.
INFO:PypiVersions:'django': Major version difference. Local version '2.2.13' and remote version '3.0.7' differ.
INFO:PypiVersions:'django': Version '2.2.13'.
INFO:PypiVersions:Get remote version for 'djangorestframework'.
INFO:PypiVersions:'djangorestframework': Version '3.11.0'.
INFO:PypiVersions:Get remote version for 'psycopg2-binary'.
INFO:PypiVersions:'psycopg2-binary': Version '2.8.5'.
INFO:PypiVersions:Get remote version for 'requests'.
INFO:PypiVersions:'requests': Version '2.23.0'.
INFO:PypiVersions:Get remote version for 'uWSGI'.
INFO:PypiVersions:'uWSGI': Version '2.0.18'.
INFO:PypiVersions:Get remote version for 'django-ratelimit'.
INFO:PypiVersions:'django-ratelimit': Version '2.0.0'.
INFO:PypiVersions:Get remote version for 'django-environ'.
INFO:PypiVersions:'django-environ': Version '0.4.5'.
INFO:PypiVersions:Get remote version for 'python-monerorpc'.
INFO:PypiVersions:'python-monerorpc': Version '0.5.13'.
INFO:PypiVersions:Get remote version for 'monero'.
INFO:PypiVersions:'monero': Version '0.7.3'.
INFO:PypiVersions:Get remote version for 'gevent'.
INFO:PypiVersions:'gevent': Major version difference. Local version '1.4.0' and remote version '20.6.1' differ.
INFO:PypiVersions:'gevent': Version '1.5.0'.

'psycopg2-binary': Local version '2.8.4' and remote version '2.8.5' differ.
'python-monerorpc': Local version '0.5.10' and remote version '0.5.13' differ.
'gevent': Local version '1.4.0' and remote version '1.5.0' differ. There is a more recent major version available: '20.6.1'.
```

Return the result in JSON format:
```
pypi_versions --requirements 1.txt 2.txt 3.txt ... --json
```

Possible output:
```
INFO:PypiVersions:Checking /.../requirements.txt.
INFO:PypiVersions:Get remote version for 'django'.
INFO:PypiVersions:'django': Major version difference. Local version '2.2.13' and remote version '3.0.7' differ.
INFO:PypiVersions:'django': Version '2.2.13'.
INFO:PypiVersions:Get remote version for 'djangorestframework'.
INFO:PypiVersions:'djangorestframework': Version '3.11.0'.
INFO:PypiVersions:Get remote version for 'psycopg2-binary'.
INFO:PypiVersions:'psycopg2-binary': Version '2.8.5'.
INFO:PypiVersions:Get remote version for 'requests'.
INFO:PypiVersions:'requests': Version '2.23.0'.
INFO:PypiVersions:Get remote version for 'uWSGI'.
INFO:PypiVersions:'uWSGI': Version '2.0.18'.
INFO:PypiVersions:Get remote version for 'django-ratelimit'.
INFO:PypiVersions:'django-ratelimit': Version '2.0.0'.
INFO:PypiVersions:Get remote version for 'django-environ'.
INFO:PypiVersions:'django-environ': Version '0.4.5'.
INFO:PypiVersions:Get remote version for 'python-monerorpc'.
INFO:PypiVersions:'python-monerorpc': Version '0.5.13'.
INFO:PypiVersions:Get remote version for 'monero'.
INFO:PypiVersions:'monero': Version '0.7.3'.
INFO:PypiVersions:Get remote version for 'gevent'.
INFO:PypiVersions:'gevent': Major version difference. Local version '1.4.0' and remote version '20.6.1' differ.
INFO:PypiVersions:'gevent': Version '1.5.0'.

{'psycopg2-binary': {'local_version': '2.8.4', 'remote_version': '2.8.5'}, 'python-monerorpc': {'local_version': '0.5.10', 'remote_version': '0.5.13'}, 'gevent': {'local_version': '1.4.0', 'more_recent_major_version': '20.6.1', 'remote_version': '1.5.0'}}
```

`--debug` shows some debug information.
