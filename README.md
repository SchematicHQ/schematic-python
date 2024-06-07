# Schematic Python Library

The Schematic Python Library provides convenient access to the Schematic API from
applications written in Python.

The library includes type definitions for all
request and response fields, and offers both synchronous and asynchronous clients powered by httpx.

## Installation and Setup

1. Add this dependency to your project's build file:

```bash
pip install schematichq
# or
poetry add schematichq
```

2. [Issue an API key](https://docs.schematichq.com/quickstart#create-an-api-key) for the appropriate environment using the [Schematic app](https://app.schematichq.com/settings/api-keys).

3. Using this secret key, initialize a client in your application:

```python
from schematic.client import Schematic

client = Schematic("YOUR_API_KEY")
```

## Async Client
The SDK also exports an async client so that you can make non-blocking calls to our API.

```python
from schematic.client import AsyncSchematic

client = AsyncSchematic("YOUR_API_KEY")
async def main() -> None:
    await client.companies.get_company(
        company_id="company_id",
    )

asyncio.run(main())
```

## Exception Handling
All errors thrown by the SDK will be subclasses of [`ApiError`](./src/schematic/core/api_error.py).

```python
try:
    client.companies.get_company(
        company_id="company_id",
    )
except schematic.core.ApiError as e: # Handle all errors
  print(e.status_code)
  print(e.body)
```

## Usage examples

### Sending identify events

Create or update users and companies using identify events.

```python
from schematic import EventBodyIdentifyCompany
from schematic.client import Schematic

client = Schematic("YOUR_API_KEY")

client.identify(
    keys={
        "email": "wcoyote@acme.net",
        "user_id": "your-user-id",
    },
    company=EventBodyIdentifyCompany(
        keys={"id": "your-company-id"},
        name="Acme Widgets, Inc.",
        traits={
          "city": "Atlanta",
        },
    ),
    name="Wile E. Coyote",
    traits={
        "login_count": 24,
        "is_staff": false,
    },
)
```

This call is non-blocking and there is no response to check.

### Sending track events

Track activity in your application using track events; these events can later be used to produce metrics for targeting.

```python
from schematic.client import Schematic

client = Schematic("YOUR_API_KEY")

client.track(
    event="some-action",
    user={"user_id": "your-user-id"},
    company={"id": "your-company-id"},
)
```

This call is non-blocking and there is no response to check.

### Creating and updating companies

Although it is faster to create companies and users via identify events, if you need to handle a response, you can use the companies API to upsert companies. Because you use your own identifiers to identify companies, rather than a Schematic company ID, creating and updating companies are both done via the same upsert operation:

```python
from schematic.client import Schematic

client = Schematic("YOUR_API_KEY")

client.companies.upsert_company(
    keys={"id": "your-company-id"},
    name="Acme Widgets, Inc.",
    traits={
        "city": "Atlanta",
        "high_score": 25,
        "is_active": true,
    },
)
```

You can define any number of company keys; these are used to address the company in the future, for example by updating the company's traits or checking a flag for the company.

You can also define any number of company traits; these can then be used as targeting parameters.

### Creating and updating users

Similarly, you can upsert users using the Schematic API, as an alternative to using identify events. Because you use your own identifiers to identify users, rather than a Schematic user ID, creating and updating users are both done via the same upsert operation:

```python
from schematic.client import Schematic

client = Schematic("YOUR_API_KEY")

client.companies.upsert_user(
    keys={
        "email": "wcoyote@acme.net",
        "user_id": "your-user-id",
    },
    name="Wile E. Coyote",
    traits={
        "city": "Atlanta",
        "high_score": 25,
        "is_active": true,
    },
    company={"id": "your-company-id"},
)
```

You can define any number of user keys; these are used to address the user in the future, for example by updating the user's traits or checking a flag for the user.

You can also define any number of user traits; these can then be used as targeting parameters.

### Checking flags

When checking a flag, you'll provide keys for a company and/or keys for a user. You can also provide no keys at all, in which case you'll get the default value for the flag.

```python
from schematic.client import Schematic

client = Schematic("YOUR_API_KEY")

client.check_flag(
    "some-flag-key",
    company={"id": "your-company-id"},
    user={"user_id": "your-user-id"},
)
```

## Advanced

### Flag Check Options

By default, the client will do some local caching for flag checks. If you would like to change this behavior, you can do so using an initialization option to specify the max size of the cache (in bytes) and the max age of the cache (in seconds):

```python
from schematic.client import LocalCache, Schematic

cache_size_bytes = 1000000
cache_ttl = 1000  # in milliseconds
config = SchematicConfig(
    cache_providers=[LocalCache[bool](cache_size_bytes, cache_ttl)],
)
client = Schematic("YOUR_API_KEY", config)
```

You can also disable local caching entirely with an initialization option; bear in mind that, in this case, every flag check will result in a network request:

```python
from schematic.client import Schematic

config = SchematicConfig(cache_providers=[])
client = Schematic("YOUR_API_KEY", config)
```

You may want to specify default flag values for your application, which will be used if there is a service interruption or if the client is running in offline mode (see below). You can do this using an initialization option:

```python
from schematic.client import Schematic

config = SchematicConfig(flag_defaults={"some-flag-key": True})
client = Schematic("YOUR_API_KEY", config)
```

### Offline Mode

In development or testing environments, you may want to avoid making network requests to the Schematic API. You can run Schematic in offline mode by specifying the `offline` option; in this case, it does not matter what API key you specify:

```python
from schematic.client import Schematic

config = SchematicConfig(offline=True)
client = Schematic("", config)
```

Offline mode works well with flag defaults:

```python
from schematic.client import Schematic

config = SchematicConfig(
    flag_defaults={"some-flag-key": True},
    offline=True,
)
client = Schematic("", config)
client.check_flag("some-flag-key") # Returns True
```

### Timeouts
By default, requests time out after 60 seconds. You can configure this with a
timeout option at the client or request level.

```python
from schematic.client import Schematic

client = Schematic(
    # All timeouts are 20 seconds
    timeout=20.0,
)

# Override timeout for a specific method
client.companies.get_company(..., {
    timeout_in_seconds=20.0
})
```

### Retries
The SDK is instrumented with automatic retries with exponential backoff. A request will be
retried as long as the request is deemed retriable and the number of retry attempts has not grown larger
than the configured retry limit (default: 2).

A request is deemed retriable when any of the following HTTP status codes is returned:

- [408](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/408) (Timeout)
- [429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) (Too Many Requests)
- [5XX](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500) (Internal Server Errors)

Use the `max_retries` request option to configure this behavior.

```python
# Override timeout for a specific method
client.companies.get_company(..., {
    max_retries=1 # Only retry once on failure
})
```

### Custom HTTP client
You can override the httpx client to customize it for your use-case. Some common use-cases
include support for proxies and transports.

```python
import httpx

from schematic.client import Schematic

client = Schematic(
    http_client=httpx.Client(
        proxies="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

## Beta Status

This SDK is in **Preview**, and there may be breaking changes between versions without a major
version update.

To ensure a reproducible environment (and minimize risk of breaking changes), we recommend pinning a specific package version.

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically.
Additions made directly to this library would have to be moved over to our generation code,
otherwise they would be overwritten upon the next generated release. Feel free to open a PR as
 a proof of concept, but know that we will not be able to merge it as-is. We suggest opening
an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
