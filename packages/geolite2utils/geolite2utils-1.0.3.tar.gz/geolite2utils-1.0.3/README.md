# geolite2utils

Easily download, extract, and use MaxMind's GeoIP2 Lite database.

```python
from geolite2utils import GeoLite2Utils

license_key = 'YOUR_LICENSE_KEY'
directory = '/local/directory/to/store/geolite/databases'
geolite2 = GeoLite2Utils(license_key, directory)

# download the archive of the database; this might be hundreds of megabytes depending on the db
geolite2.download(geolite2.CITY)

# extract the archive
geolite2.extract(geolite2.CITY)

# clean up the .tar.gz archive so it doesn't waste disk space
geolite2.cleanup(geolite2.CITY) 

# finally, let's query some ip addresses
reader = geolite2.reader()
response = reader.city('128.101.101.101')
print(response.city.name)
# 'Minneapolis'
```

## Generating a license key

1. [Sign up for a GeoLite2 account](https://www.maxmind.com/en/geolite2/signup)
2. [Log in to your GeoLite2 account](https://www.maxmind.com/en/account/login)
3. In the menu on the left, navigate to `Services > My License Key`.
4. Click `Generate new license key`.


## Available Databases

The following databases are available:

- `GeoLite2Utils.CITY`
- `GeoLite2Utils.COUNTRY`
- `GeoLite2Utils.ASN`
