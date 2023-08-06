[![Build Status](https://travis-ci.com/accorvin/es-template-manager.png)](https://travis-ci.com/accorvin/es-template-manager)

# es-template-manager
A utility for managing Elasticsearch index templates in source control

# Template Directory

The utility expects to be passed the path to a directory containing
Elasticsearch index template files. The utility will iterate over each
file, using the name of the file as the name of the index template. The
contents of each index template file should be a JSON payload defining the
index template.

# Usage

```bash
python es-template-manager.py $ARGUMENTS
```

Run `python es-template-manager.py -h` to see a full list of arguments.

## Required Arguments

  * `--es-hostname`: The Elasticsearch hostname. Do not prefix with http/https

  * `--es-port`: The Elasticsearch port number

  * `--template-directory`: The path to the directory containing the index
    template files

## Optional Arguments

  * `--debug`: Enable debug logging

  * `--es-use-ssl`: Use SSL/TLS when connecting to Elasticsearch

  * `--es-cacert`: The path to a CA certificate file for verifying the
    Elasticsearch server certificate's authenticity

  * `--es-cert`: The path to a certificate file for authencating against the
    Elasticsearch server

  * `--es-key`: The path to a key file for authenticating against the
    Elasticsearch server

  * `--overwrite-templates`: Whether to overwrite any templates that already
    exist

  * `--pushgateway_enpoint`: If you want to push the final status of the job
    to a pushgateway endpoint
