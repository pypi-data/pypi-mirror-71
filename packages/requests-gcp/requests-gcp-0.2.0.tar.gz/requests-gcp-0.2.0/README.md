# requests-gcp

Python requests wrapper for service-to-service authentication on GCP. Drop-in replacement with support for `get, head, post, put, patch, delete, options`.

Adds `Authorization` header with a Google-signed OAuth ID token for the receiving URL. The JWT tokens are cached for subsequent requests and automatically renewed (they usually expire within 1h).

## Install

```
pip3 install requests-gcp
```

## Usage

```python
import requestsgcp as requests

# Request to a private Cloud Run service
requests.get("https://<service>.run.app")

# External request
requests.get("https://yahoo.com", gcp_auth=False)
```
