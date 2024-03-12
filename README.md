# drf_api_key
<!-- [pypi](https://pypi.org/project/drf-api-key-auth/) -->

`drf_api_key` is a Django REST Framework library designed for creating, managing, and securing API keys. It provides easy-to-use models, permissions, and throttling classes to manage API access effectively.

## Installation
<!-- Install  `drf_api_key` using pip: -->

<!-- ```bash
pip install drf_api_key
``` -->

```bash
git clone https://www.github/Temi9568/drf_api_key
cd drf_api_key
pip install .
```

## Configuration
After installation, you need to add drf_apikey to your INSTALLED_APPS in the Django settings.

```bash
INSTALLED_APPS = (
    ...
    'api_key_auth',
    ...
)
```

Next, set up the Django REST framework permissions in your Django settings:
```bash
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'drf_apikey.permissions.APIKeyPermission',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'drf_apikey.throttling.APIKeyThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        '<scope>': '5/s',    # Normal limits (i.e 5 reqs per second). Update drf_apikey.throttling.APIKeyThrottle scope attr to the key you set here
        '<sope_long>': '1000'    # Relates to monthly limits, should just be integer (i.e 1000 requests per month). Update drf_apikey.throttling.APIKeyThrottle scope_long attr to the key you set here
    }
}
```

## Example Request
Here's a basic example of making a request to a Django REST Framework view that is protected with drf_apikey permissions:

```bash
import requests

response = requests.get(
    url="http://0.0.0.0:8000/api/your_endpoint",
    headers={
        "X_API_KEY": "fd8b4a98c8f53035aeab410258430e2d86079c93",
    },
)

print(response.json())
```

in this example above, replace "http://0.0.0.0:8000/api/your_endpoint" with the actual endpoint you wish to access, and "fd8b4a98c8f53035aeab410258430e2d86079c93" with a valid API key.


## Contributing
Contributions are welcome. Please read the contributing guide for more information.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
