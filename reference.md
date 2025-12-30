# Reference
<details><summary><code>client.<a href="src/schematic/base_client.py">put_plan_audiences_plan_audience_id</a>(...) -> AsyncHttpResponse[None]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.put_plan_audiences_plan_audience_id(
    plan_audience_id="plan_audience_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**plan_audience_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.<a href="src/schematic/base_client.py">delete_plan_audiences_plan_audience_id</a>(...) -> AsyncHttpResponse[None]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.delete_plan_audiences_plan_audience_id(
    plan_audience_id="plan_audience_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**plan_audience_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## accounts
<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">list_api_keys</a>(...) -> AsyncHttpResponse[ListApiKeysResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.accounts.list_api_keys(
    environment_id="environment_id",
    require_environment=True,
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**require_environment:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**environment_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">create_api_key</a>(...) -> AsyncHttpResponse[CreateApiKeyResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.accounts.create_api_key(
    name="name",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**environment_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">get_api_key</a>(...) -> AsyncHttpResponse[GetApiKeyResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.accounts.get_api_key(
    api_key_id="api_key_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**api_key_id:** `str` — api_key_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">update_api_key</a>(...) -> AsyncHttpResponse[UpdateApiKeyResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.accounts.update_api_key(
    api_key_id="api_key_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**api_key_id:** `str` — api_key_id
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">delete_api_key</a>(...) -> AsyncHttpResponse[DeleteApiKeyResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.accounts.delete_api_key(
    api_key_id="api_key_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**api_key_id:** `str` — api_key_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">count_api_keys</a>(...) -> AsyncHttpResponse[CountApiKeysResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.accounts.count_api_keys(
    environment_id="environment_id",
    require_environment=True,
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**require_environment:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**environment_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">list_api_requests</a>(...) -> AsyncHttpResponse[ListApiRequestsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.accounts.list_api_requests(
    q="q",
    request_type="request_type",
    environment_id="environment_id",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_type:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**environment_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">get_api_request</a>(...) -> AsyncHttpResponse[GetApiRequestResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.accounts.get_api_request(
    api_request_id="api_request_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**api_request_id:** `str` — api_request_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">count_api_requests</a>(...) -> AsyncHttpResponse[CountApiRequestsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.accounts.count_api_requests(
    q="q",
    request_type="request_type",
    environment_id="environment_id",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_type:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**environment_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">list_environments</a>(...) -> AsyncHttpResponse[ListEnvironmentsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.accounts.list_environments(
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">create_environment</a>(...) -> AsyncHttpResponse[CreateEnvironmentResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.accounts.create_environment(
    environment_type="development",
    name="name",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**environment_type:** `EnvironmentType` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">get_environment</a>(...) -> AsyncHttpResponse[GetEnvironmentResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.accounts.get_environment(
    environment_id="environment_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**environment_id:** `str` — environment_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">update_environment</a>(...) -> AsyncHttpResponse[UpdateEnvironmentResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.accounts.update_environment(
    environment_id="environment_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**environment_id:** `str` — environment_id
    
</dd>
</dl>

<dl>
<dd>

**environment_type:** `typing.Optional[EnvironmentType]` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">delete_environment</a>(...) -> AsyncHttpResponse[DeleteEnvironmentResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.accounts.delete_environment(
    environment_id="environment_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**environment_id:** `str` — environment_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">quickstart</a>() -> AsyncHttpResponse[QuickstartResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.accounts.quickstart()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## billing
<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">list_coupons</a>(...) -> AsyncHttpResponse[ListCouponsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.billing.list_coupons(
    is_active=True,
    q="q",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**is_active:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_billing_coupon</a>(...) -> AsyncHttpResponse[UpsertBillingCouponResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.billing.upsert_billing_coupon(
    amount_off=1,
    duration="duration",
    duration_in_months=1,
    external_id="external_id",
    max_redemptions=1,
    name="name",
    percent_off=1.1,
    times_redeemed=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**amount_off:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**duration:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**duration_in_months:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**external_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**max_redemptions:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**percent_off:** `float` 
    
</dd>
</dl>

<dl>
<dd>

**times_redeemed:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**currency:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_billing_customer</a>(...) -> AsyncHttpResponse[UpsertBillingCustomerResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.billing.upsert_billing_customer(
    email="email",
    external_id="external_id",
    failed_to_import=True,
    meta={"key": "value"},
    name="name",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**email:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**external_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**failed_to_import:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**meta:** `typing.Dict[str, str]` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**company_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**default_payment_method_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**provider_type:** `typing.Optional[BillingProviderType]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">list_customers_with_subscriptions</a>(...) -> AsyncHttpResponse[ListCustomersWithSubscriptionsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.billing.list_customers_with_subscriptions(
    failed_to_import=True,
    name="name",
    provider_type="schematic",
    q="q",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**failed_to_import:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**provider_type:** `typing.Optional[BillingProviderType]` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">count_customers</a>(...) -> AsyncHttpResponse[CountCustomersResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.billing.count_customers(
    failed_to_import=True,
    name="name",
    provider_type="schematic",
    q="q",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**failed_to_import:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**provider_type:** `typing.Optional[BillingProviderType]` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">list_invoices</a>(...) -> AsyncHttpResponse[ListInvoicesResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.billing.list_invoices(
    company_id="company_id",
    customer_external_id="customer_external_id",
    subscription_external_id="subscription_external_id",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**customer_external_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**subscription_external_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**company_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_invoice</a>(...) -> AsyncHttpResponse[UpsertInvoiceResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.billing.upsert_invoice(
    amount_due=1,
    amount_paid=1,
    amount_remaining=1,
    collection_method="collection_method",
    currency="currency",
    customer_external_id="customer_external_id",
    subtotal=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**amount_due:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**amount_paid:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**amount_remaining:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**collection_method:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**currency:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**customer_external_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**subtotal:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**due_date:** `typing.Optional[dt.datetime]` 
    
</dd>
</dl>

<dl>
<dd>

**external_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**payment_method_external_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**subscription_external_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**url:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">list_meters</a>(...) -> AsyncHttpResponse[ListMetersResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.billing.list_meters(
    display_name="display_name",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**display_name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_billing_meter</a>(...) -> AsyncHttpResponse[UpsertBillingMeterResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.billing.upsert_billing_meter(
    display_name="display_name",
    event_name="event_name",
    event_payload_key="event_payload_key",
    external_id="external_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**display_name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**event_name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**event_payload_key:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**external_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">list_payment_methods</a>(...) -> AsyncHttpResponse[ListPaymentMethodsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.billing.list_payment_methods(
    company_id="company_id",
    customer_external_id="customer_external_id",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**customer_external_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**company_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_payment_method</a>(...) -> AsyncHttpResponse[UpsertPaymentMethodResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.billing.upsert_payment_method(
    customer_external_id="customer_external_id",
    external_id="external_id",
    payment_method_type="payment_method_type",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**customer_external_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**external_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**payment_method_type:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**account_last_4:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**account_name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**bank_name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**billing_email:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**billing_name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**card_brand:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**card_exp_month:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**card_exp_year:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**card_last_4:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">list_billing_prices</a>(...) -> AsyncHttpResponse[ListBillingPricesResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.billing.list_billing_prices(
    for_initial_plan=True,
    for_trial_expiry_plan=True,
    interval="interval",
    is_active=True,
    price=1,
    product_id="product_id",
    provider_type="schematic",
    q="q",
    tiers_mode="graduated",
    usage_type="licensed",
    with_meter=True,
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**for_initial_plan:** `typing.Optional[bool]` — Filter for prices valid for initial plans (free prices only)
    
</dd>
</dl>

<dl>
<dd>

**for_trial_expiry_plan:** `typing.Optional[bool]` — Filter for prices valid for trial expiry plans (free prices only)
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**interval:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**is_active:** `typing.Optional[bool]` — Filter for active prices on active products (defaults to true if not specified)
    
</dd>
</dl>

<dl>
<dd>

**price:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**product_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**product_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**provider_type:** `typing.Optional[BillingProviderType]` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**tiers_mode:** `typing.Optional[BillingTiersMode]` 
    
</dd>
</dl>

<dl>
<dd>

**usage_type:** `typing.Optional[BillingPriceUsageType]` 
    
</dd>
</dl>

<dl>
<dd>

**with_meter:** `typing.Optional[bool]` — Filter for prices with a meter
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_billing_price</a>(...) -> AsyncHttpResponse[UpsertBillingPriceResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import CreateBillingPriceTierRequestBody, Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.billing.upsert_billing_price(
    billing_scheme="per_unit",
    currency="currency",
    external_account_id="external_account_id",
    interval="interval",
    is_active=True,
    price=1,
    price_external_id="price_external_id",
    price_tiers=[
        CreateBillingPriceTierRequestBody(
            price_external_id="price_external_id",
        )
    ],
    product_external_id="product_external_id",
    usage_type="licensed",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**billing_scheme:** `BillingPriceScheme` 
    
</dd>
</dl>

<dl>
<dd>

**currency:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**external_account_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**interval:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**is_active:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**price:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**price_external_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**price_tiers:** `typing.Sequence[CreateBillingPriceTierRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**product_external_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**usage_type:** `BillingPriceUsageType` 
    
</dd>
</dl>

<dl>
<dd>

**meter_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**package_size:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**price_decimal:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**provider_type:** `typing.Optional[BillingProviderType]` 
    
</dd>
</dl>

<dl>
<dd>

**tiers_mode:** `typing.Optional[BillingTiersMode]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">delete_billing_product</a>(...) -> AsyncHttpResponse[DeleteBillingProductResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.billing.delete_billing_product(
    billing_id="billing_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**billing_id:** `str` — billing_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">list_billing_product_prices</a>(...) -> AsyncHttpResponse[ListBillingProductPricesResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.billing.list_billing_product_prices(
    for_initial_plan=True,
    for_trial_expiry_plan=True,
    interval="interval",
    is_active=True,
    price=1,
    product_id="product_id",
    provider_type="schematic",
    q="q",
    tiers_mode="graduated",
    usage_type="licensed",
    with_meter=True,
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**for_initial_plan:** `typing.Optional[bool]` — Filter for prices valid for initial plans (free prices only)
    
</dd>
</dl>

<dl>
<dd>

**for_trial_expiry_plan:** `typing.Optional[bool]` — Filter for prices valid for trial expiry plans (free prices only)
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**interval:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**is_active:** `typing.Optional[bool]` — Filter for active prices on active products (defaults to true if not specified)
    
</dd>
</dl>

<dl>
<dd>

**price:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**product_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**product_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**provider_type:** `typing.Optional[BillingProviderType]` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**tiers_mode:** `typing.Optional[BillingTiersMode]` 
    
</dd>
</dl>

<dl>
<dd>

**usage_type:** `typing.Optional[BillingPriceUsageType]` 
    
</dd>
</dl>

<dl>
<dd>

**with_meter:** `typing.Optional[bool]` — Filter for prices with a meter
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">delete_product_price</a>(...) -> AsyncHttpResponse[DeleteProductPriceResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.billing.delete_product_price(
    billing_id="billing_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**billing_id:** `str` — billing_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_billing_product</a>(...) -> AsyncHttpResponse[UpsertBillingProductResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.billing.upsert_billing_product(
    external_id="external_id",
    name="name",
    price=1.1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**external_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**price:** `float` 
    
</dd>
</dl>

<dl>
<dd>

**is_active:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**provider_type:** `typing.Optional[BillingProviderType]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">list_billing_products</a>(...) -> AsyncHttpResponse[ListBillingProductsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.billing.list_billing_products(
    is_active=True,
    name="name",
    price_usage_type="licensed",
    provider_type="schematic",
    q="q",
    with_one_time_charges=True,
    with_prices_only=True,
    with_zero_price=True,
    without_linked_to_plan=True,
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**is_active:** `typing.Optional[bool]` — Filter products that are active. Defaults to true if not specified
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**price_usage_type:** `typing.Optional[BillingPriceUsageType]` 
    
</dd>
</dl>

<dl>
<dd>

**provider_type:** `typing.Optional[BillingProviderType]` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**with_one_time_charges:** `typing.Optional[bool]` — Filter products that are one time charges
    
</dd>
</dl>

<dl>
<dd>

**with_prices_only:** `typing.Optional[bool]` — Filter products that have prices
    
</dd>
</dl>

<dl>
<dd>

**with_zero_price:** `typing.Optional[bool]` — Filter products that have zero price for free subscription type
    
</dd>
</dl>

<dl>
<dd>

**without_linked_to_plan:** `typing.Optional[bool]` — Filter products that are not linked to any plan
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">count_billing_products</a>(...) -> AsyncHttpResponse[CountBillingProductsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.billing.count_billing_products(
    is_active=True,
    name="name",
    price_usage_type="licensed",
    provider_type="schematic",
    q="q",
    with_one_time_charges=True,
    with_prices_only=True,
    with_zero_price=True,
    without_linked_to_plan=True,
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**is_active:** `typing.Optional[bool]` — Filter products that are active. Defaults to true if not specified
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**price_usage_type:** `typing.Optional[BillingPriceUsageType]` 
    
</dd>
</dl>

<dl>
<dd>

**provider_type:** `typing.Optional[BillingProviderType]` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**with_one_time_charges:** `typing.Optional[bool]` — Filter products that are one time charges
    
</dd>
</dl>

<dl>
<dd>

**with_prices_only:** `typing.Optional[bool]` — Filter products that have prices
    
</dd>
</dl>

<dl>
<dd>

**with_zero_price:** `typing.Optional[bool]` — Filter products that have zero price for free subscription type
    
</dd>
</dl>

<dl>
<dd>

**without_linked_to_plan:** `typing.Optional[bool]` — Filter products that are not linked to any plan
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_billing_subscription</a>(...) -> AsyncHttpResponse[UpsertBillingSubscriptionResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
import datetime

from schematic import (
    BillingProductPricing,
    BillingSubscriptionDiscount,
    Schematic,
)

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.billing.upsert_billing_subscription(
    cancel_at_period_end=True,
    currency="currency",
    customer_external_id="customer_external_id",
    discounts=[
        BillingSubscriptionDiscount(
            coupon_external_id="coupon_external_id",
            external_id="external_id",
            is_active=True,
            started_at=datetime.datetime.fromisoformat(
                "2024-01-15 09:30:00+00:00",
            ),
        )
    ],
    expired_at=datetime.datetime.fromisoformat(
        "2024-01-15 09:30:00+00:00",
    ),
    product_external_ids=[
        BillingProductPricing(
            currency="currency",
            interval="interval",
            price=1,
            price_external_id="price_external_id",
            product_external_id="product_external_id",
            quantity=1,
            usage_type="licensed",
        )
    ],
    subscription_external_id="subscription_external_id",
    total_price=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**cancel_at_period_end:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**currency:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**customer_external_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**discounts:** `typing.Sequence[BillingSubscriptionDiscount]` 
    
</dd>
</dl>

<dl>
<dd>

**expired_at:** `dt.datetime` 
    
</dd>
</dl>

<dl>
<dd>

**product_external_ids:** `typing.Sequence[BillingProductPricing]` 
    
</dd>
</dl>

<dl>
<dd>

**subscription_external_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**total_price:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**application_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**cancel_at:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**default_payment_method_external_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**default_payment_method_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**interval:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[typing.Dict[str, typing.Any]]` 
    
</dd>
</dl>

<dl>
<dd>

**period_end:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**period_start:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**trial_end:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**trial_end_setting:** `typing.Optional[BillingSubscriptionTrialEndSetting]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## credits
<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">list_billing_credits</a>(...) -> AsyncHttpResponse[ListBillingCreditsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.list_billing_credits(
    name="name",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">create_billing_credit</a>(...) -> AsyncHttpResponse[CreateBillingCreditResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.create_billing_credit(
    currency="currency",
    description="description",
    name="name",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**currency:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**description:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**burn_strategy:** `typing.Optional[BillingCreditBurnStrategy]` 
    
</dd>
</dl>

<dl>
<dd>

**default_expiry_unit:** `typing.Optional[BillingCreditExpiryUnit]` 
    
</dd>
</dl>

<dl>
<dd>

**default_expiry_unit_count:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**default_rollover_policy:** `typing.Optional[BillingCreditRolloverPolicy]` 
    
</dd>
</dl>

<dl>
<dd>

**icon:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**per_unit_price:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**per_unit_price_decimal:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**plural_name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**singular_name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">get_single_billing_credit</a>(...) -> AsyncHttpResponse[GetSingleBillingCreditResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.get_single_billing_credit(
    credit_id="credit_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**credit_id:** `str` — credit_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">update_billing_credit</a>(...) -> AsyncHttpResponse[UpdateBillingCreditResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.update_billing_credit(
    credit_id="credit_id",
    description="description",
    name="name",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**credit_id:** `str` — credit_id
    
</dd>
</dl>

<dl>
<dd>

**description:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**burn_strategy:** `typing.Optional[BillingCreditBurnStrategy]` 
    
</dd>
</dl>

<dl>
<dd>

**default_expiry_unit:** `typing.Optional[BillingCreditExpiryUnit]` 
    
</dd>
</dl>

<dl>
<dd>

**default_expiry_unit_count:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**default_rollover_policy:** `typing.Optional[BillingCreditRolloverPolicy]` 
    
</dd>
</dl>

<dl>
<dd>

**icon:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**per_unit_price:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**per_unit_price_decimal:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**plural_name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**singular_name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">soft_delete_billing_credit</a>(...) -> AsyncHttpResponse[SoftDeleteBillingCreditResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.soft_delete_billing_credit(
    credit_id="credit_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**credit_id:** `str` — credit_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">list_credit_bundles</a>(...) -> AsyncHttpResponse[ListCreditBundlesResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.list_credit_bundles(
    credit_id="credit_id",
    status="active",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**credit_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[BillingCreditBundleStatus]` 
    
</dd>
</dl>

<dl>
<dd>

**bundle_type:** `typing.Optional[BillingCreditBundleType]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">create_credit_bundle</a>(...) -> AsyncHttpResponse[CreateCreditBundleResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.create_credit_bundle(
    bundle_name="bundle_name",
    credit_id="credit_id",
    currency="currency",
    price_per_unit=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**bundle_name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**credit_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**currency:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**price_per_unit:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**bundle_type:** `typing.Optional[BillingCreditBundleType]` 
    
</dd>
</dl>

<dl>
<dd>

**expiry_type:** `typing.Optional[BillingCreditExpiryType]` 
    
</dd>
</dl>

<dl>
<dd>

**expiry_unit:** `typing.Optional[BillingCreditExpiryUnit]` 
    
</dd>
</dl>

<dl>
<dd>

**expiry_unit_count:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**price_per_unit_decimal:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**quantity:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[BillingCreditBundleStatus]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">get_credit_bundle</a>(...) -> AsyncHttpResponse[GetCreditBundleResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.get_credit_bundle(
    bundle_id="bundle_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**bundle_id:** `str` — bundle_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">update_credit_bundle_details</a>(...) -> AsyncHttpResponse[UpdateCreditBundleDetailsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.update_credit_bundle_details(
    bundle_id="bundle_id",
    bundle_name="bundle_name",
    price_per_unit=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**bundle_id:** `str` — bundle_id
    
</dd>
</dl>

<dl>
<dd>

**bundle_name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**price_per_unit:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**expiry_type:** `typing.Optional[BillingCreditExpiryType]` 
    
</dd>
</dl>

<dl>
<dd>

**expiry_unit:** `typing.Optional[BillingCreditExpiryUnit]` 
    
</dd>
</dl>

<dl>
<dd>

**expiry_unit_count:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**price_per_unit_decimal:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**quantity:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[BillingCreditBundleStatus]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">delete_credit_bundle</a>(...) -> AsyncHttpResponse[DeleteCreditBundleResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.delete_credit_bundle(
    bundle_id="bundle_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**bundle_id:** `str` — bundle_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">count_credit_bundles</a>(...) -> AsyncHttpResponse[CountCreditBundlesResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.count_credit_bundles(
    credit_id="credit_id",
    status="active",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**credit_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[BillingCreditBundleStatus]` 
    
</dd>
</dl>

<dl>
<dd>

**bundle_type:** `typing.Optional[BillingCreditBundleType]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">count_billing_credits</a>(...) -> AsyncHttpResponse[CountBillingCreditsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.count_billing_credits(
    name="name",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">zero_out_grant</a>(...) -> AsyncHttpResponse[ZeroOutGrantResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.zero_out_grant(
    grant_id="grant_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**grant_id:** `str` — grant_id
    
</dd>
</dl>

<dl>
<dd>

**reason:** `typing.Optional[BillingCreditGrantZeroedOutReason]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">grant_billing_credits_to_company</a>(...) -> AsyncHttpResponse[GrantBillingCreditsToCompanyResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.grant_billing_credits_to_company(
    company_id="company_id",
    credit_id="credit_id",
    quantity=1,
    reason="billing_credit_auto_topup",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**credit_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**quantity:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**reason:** `BillingCreditGrantReason` 
    
</dd>
</dl>

<dl>
<dd>

**billing_periods_count:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**expires_at:** `typing.Optional[dt.datetime]` 
    
</dd>
</dl>

<dl>
<dd>

**expiry_type:** `typing.Optional[BillingCreditExpiryType]` 
    
</dd>
</dl>

<dl>
<dd>

**expiry_unit:** `typing.Optional[BillingCreditExpiryUnit]` 
    
</dd>
</dl>

<dl>
<dd>

**expiry_unit_count:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**renewal_enabled:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**renewal_period:** `typing.Optional[BillingPlanCreditGrantResetStart]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">list_company_grants</a>(...) -> AsyncHttpResponse[ListCompanyGrantsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.list_company_grants(
    company_id="company_id",
    order="created_at",
    dir="asc",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**order:** `typing.Optional[CreditGrantSortOrder]` 
    
</dd>
</dl>

<dl>
<dd>

**dir:** `typing.Optional[SortDirection]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">count_billing_credits_grants</a>(...) -> AsyncHttpResponse[CountBillingCreditsGrantsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.count_billing_credits_grants(
    credit_id="credit_id",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**credit_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">list_grants_for_credit</a>(...) -> AsyncHttpResponse[ListGrantsForCreditResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.list_grants_for_credit(
    credit_id="credit_id",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**credit_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">get_enriched_credit_ledger</a>(...) -> AsyncHttpResponse[GetEnrichedCreditLedgerResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.get_enriched_credit_ledger(
    company_id="company_id",
    billing_credit_id="billing_credit_id",
    feature_id="feature_id",
    period="daily",
    start_time="start_time",
    end_time="end_time",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**period:** `CreditLedgerPeriod` 
    
</dd>
</dl>

<dl>
<dd>

**billing_credit_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**feature_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**start_time:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**end_time:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">count_credit_ledger</a>(...) -> AsyncHttpResponse[CountCreditLedgerResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.count_credit_ledger(
    company_id="company_id",
    billing_credit_id="billing_credit_id",
    feature_id="feature_id",
    period="daily",
    start_time="start_time",
    end_time="end_time",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**period:** `CreditLedgerPeriod` 
    
</dd>
</dl>

<dl>
<dd>

**billing_credit_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**feature_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**start_time:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**end_time:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">list_billing_plan_credit_grants</a>(...) -> AsyncHttpResponse[ListBillingPlanCreditGrantsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.list_billing_plan_credit_grants(
    credit_id="credit_id",
    plan_id="plan_id",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**credit_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**plan_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**plan_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">create_billing_plan_credit_grant</a>(...) -> AsyncHttpResponse[CreateBillingPlanCreditGrantResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.create_billing_plan_credit_grant(
    credit_amount=1,
    credit_id="credit_id",
    plan_id="plan_id",
    reset_cadence="daily",
    reset_start="billing_period",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**credit_amount:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**credit_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**plan_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**reset_cadence:** `BillingPlanCreditGrantResetCadence` 
    
</dd>
</dl>

<dl>
<dd>

**reset_start:** `BillingPlanCreditGrantResetStart` 
    
</dd>
</dl>

<dl>
<dd>

**apply_to_existing:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**auto_topup_amount:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**auto_topup_amount_type:** `typing.Optional[CreditAutoTopupAmountType]` 
    
</dd>
</dl>

<dl>
<dd>

**auto_topup_enabled:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**auto_topup_expiry_type:** `typing.Optional[BillingCreditExpiryType]` 
    
</dd>
</dl>

<dl>
<dd>

**auto_topup_expiry_unit:** `typing.Optional[BillingCreditExpiryUnit]` 
    
</dd>
</dl>

<dl>
<dd>

**auto_topup_expiry_unit_count:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**auto_topup_threshold_percent:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**expiry_type:** `typing.Optional[BillingCreditExpiryType]` 
    
</dd>
</dl>

<dl>
<dd>

**expiry_unit:** `typing.Optional[BillingCreditExpiryUnit]` 
    
</dd>
</dl>

<dl>
<dd>

**expiry_unit_count:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**reset_type:** `typing.Optional[BillingPlanCreditGrantResetType]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">update_billing_plan_credit_grant</a>(...) -> AsyncHttpResponse[UpdateBillingPlanCreditGrantResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.update_billing_plan_credit_grant(
    plan_grant_id="plan_grant_id",
    reset_cadence="daily",
    reset_start="billing_period",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**plan_grant_id:** `str` — plan_grant_id
    
</dd>
</dl>

<dl>
<dd>

**reset_cadence:** `BillingPlanCreditGrantResetCadence` 
    
</dd>
</dl>

<dl>
<dd>

**reset_start:** `BillingPlanCreditGrantResetStart` 
    
</dd>
</dl>

<dl>
<dd>

**apply_to_existing:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**auto_topup_amount:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**auto_topup_amount_type:** `typing.Optional[CreditAutoTopupAmountType]` 
    
</dd>
</dl>

<dl>
<dd>

**auto_topup_enabled:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**auto_topup_expiry_type:** `typing.Optional[BillingCreditExpiryType]` 
    
</dd>
</dl>

<dl>
<dd>

**auto_topup_expiry_unit:** `typing.Optional[BillingCreditExpiryUnit]` 
    
</dd>
</dl>

<dl>
<dd>

**auto_topup_expiry_unit_count:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**auto_topup_threshold_percent:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**credit_amount:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**expiry_type:** `typing.Optional[BillingCreditExpiryType]` 
    
</dd>
</dl>

<dl>
<dd>

**expiry_unit:** `typing.Optional[BillingCreditExpiryUnit]` 
    
</dd>
</dl>

<dl>
<dd>

**expiry_unit_count:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**reset_type:** `typing.Optional[BillingPlanCreditGrantResetType]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">delete_billing_plan_credit_grant</a>(...) -> AsyncHttpResponse[DeleteBillingPlanCreditGrantResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.delete_billing_plan_credit_grant(
    plan_grant_id="plan_grant_id",
    apply_to_existing=True,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**plan_grant_id:** `str` — plan_grant_id
    
</dd>
</dl>

<dl>
<dd>

**apply_to_existing:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">count_billing_plan_credit_grants</a>(...) -> AsyncHttpResponse[CountBillingPlanCreditGrantsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.credits.count_billing_plan_credit_grants(
    credit_id="credit_id",
    plan_id="plan_id",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**credit_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**plan_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**plan_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## checkout
<details><summary><code>client.checkout.<a href="src/schematic/checkout/client.py">internal</a>(...) -> AsyncHttpResponse[CheckoutInternalResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import (
    Schematic,
    UpdateAddOnRequestBody,
    UpdateCreditBundleRequestBody,
    UpdatePayInAdvanceRequestBody,
)

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.checkout.internal(
    add_on_ids=[
        UpdateAddOnRequestBody(
            add_on_id="add_on_id",
            price_id="price_id",
        )
    ],
    company_id="company_id",
    credit_bundles=[
        UpdateCreditBundleRequestBody(
            bundle_id="bundle_id",
            quantity=1,
        )
    ],
    new_plan_id="new_plan_id",
    new_price_id="new_price_id",
    pay_in_advance=[
        UpdatePayInAdvanceRequestBody(
            price_id="price_id",
            quantity=1,
        )
    ],
    skip_trial=True,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**add_on_ids:** `typing.Sequence[UpdateAddOnRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**company_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**credit_bundles:** `typing.Sequence[UpdateCreditBundleRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**new_plan_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**new_price_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**pay_in_advance:** `typing.Sequence[UpdatePayInAdvanceRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**skip_trial:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**coupon_external_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**payment_method_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**promo_code:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.checkout.<a href="src/schematic/checkout/client.py">get_checkout_data</a>(...) -> AsyncHttpResponse[GetCheckoutDataResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.checkout.get_checkout_data(
    company_id="company_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**selected_plan_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.checkout.<a href="src/schematic/checkout/client.py">preview_checkout_internal</a>(...) -> AsyncHttpResponse[PreviewCheckoutInternalResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import (
    Schematic,
    UpdateAddOnRequestBody,
    UpdateCreditBundleRequestBody,
    UpdatePayInAdvanceRequestBody,
)

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.checkout.preview_checkout_internal(
    add_on_ids=[
        UpdateAddOnRequestBody(
            add_on_id="add_on_id",
            price_id="price_id",
        )
    ],
    company_id="company_id",
    credit_bundles=[
        UpdateCreditBundleRequestBody(
            bundle_id="bundle_id",
            quantity=1,
        )
    ],
    new_plan_id="new_plan_id",
    new_price_id="new_price_id",
    pay_in_advance=[
        UpdatePayInAdvanceRequestBody(
            price_id="price_id",
            quantity=1,
        )
    ],
    skip_trial=True,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**add_on_ids:** `typing.Sequence[UpdateAddOnRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**company_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**credit_bundles:** `typing.Sequence[UpdateCreditBundleRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**new_plan_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**new_price_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**pay_in_advance:** `typing.Sequence[UpdatePayInAdvanceRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**skip_trial:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**coupon_external_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**payment_method_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**promo_code:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.checkout.<a href="src/schematic/checkout/client.py">manage_plan</a>(...) -> AsyncHttpResponse[ManagePlanResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import (
    PlanSelection,
    Schematic,
    UpdateCreditBundleRequestBody,
    UpdatePayInAdvanceRequestBody,
)

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.checkout.manage_plan(
    add_on_selections=[
        PlanSelection(
            plan_id="plan_id",
        )
    ],
    company_id="company_id",
    credit_bundles=[
        UpdateCreditBundleRequestBody(
            bundle_id="bundle_id",
            quantity=1,
        )
    ],
    pay_in_advance_entitlements=[
        UpdatePayInAdvanceRequestBody(
            price_id="price_id",
            quantity=1,
        )
    ],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**add_on_selections:** `typing.Sequence[PlanSelection]` 
    
</dd>
</dl>

<dl>
<dd>

**company_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**credit_bundles:** `typing.Sequence[UpdateCreditBundleRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**pay_in_advance_entitlements:** `typing.Sequence[UpdatePayInAdvanceRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**base_plan_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**base_plan_price_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**cancel_immediately:** `typing.Optional[bool]` — If false, subscription cancels at period end. Only applies when removing all plans. Defaults to true.
    
</dd>
</dl>

<dl>
<dd>

**coupon_external_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**payment_method_external_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**promo_code:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**prorate:** `typing.Optional[bool]` — If true and cancel_immediately is true, issue prorated credit. Only applies when removing all plans. Defaults to true.
    
</dd>
</dl>

<dl>
<dd>

**trial_end:** `typing.Optional[dt.datetime]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.checkout.<a href="src/schematic/checkout/client.py">preview_manage_plan</a>(...) -> AsyncHttpResponse[PreviewManagePlanResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import (
    PlanSelection,
    Schematic,
    UpdateCreditBundleRequestBody,
    UpdatePayInAdvanceRequestBody,
)

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.checkout.preview_manage_plan(
    add_on_selections=[
        PlanSelection(
            plan_id="plan_id",
        )
    ],
    company_id="company_id",
    credit_bundles=[
        UpdateCreditBundleRequestBody(
            bundle_id="bundle_id",
            quantity=1,
        )
    ],
    pay_in_advance_entitlements=[
        UpdatePayInAdvanceRequestBody(
            price_id="price_id",
            quantity=1,
        )
    ],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**add_on_selections:** `typing.Sequence[PlanSelection]` 
    
</dd>
</dl>

<dl>
<dd>

**company_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**credit_bundles:** `typing.Sequence[UpdateCreditBundleRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**pay_in_advance_entitlements:** `typing.Sequence[UpdatePayInAdvanceRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**base_plan_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**base_plan_price_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**cancel_immediately:** `typing.Optional[bool]` — If false, subscription cancels at period end. Only applies when removing all plans. Defaults to true.
    
</dd>
</dl>

<dl>
<dd>

**coupon_external_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**payment_method_external_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**promo_code:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**prorate:** `typing.Optional[bool]` — If true and cancel_immediately is true, issue prorated credit. Only applies when removing all plans. Defaults to true.
    
</dd>
</dl>

<dl>
<dd>

**trial_end:** `typing.Optional[dt.datetime]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.checkout.<a href="src/schematic/checkout/client.py">cancel_subscription</a>(...) -> AsyncHttpResponse[CancelSubscriptionResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.checkout.cancel_subscription(
    company_id="company_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**cancel_immediately:** `typing.Optional[bool]` — If false, subscription cancels at period end. Defaults to true.
    
</dd>
</dl>

<dl>
<dd>

**prorate:** `typing.Optional[bool]` — If true and cancel_immediately is true, issue prorated credit. Defaults to true.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.checkout.<a href="src/schematic/checkout/client.py">update_customer_subscription_trial_end</a>(...) -> AsyncHttpResponse[UpdateCustomerSubscriptionTrialEndResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.checkout.update_customer_subscription_trial_end(
    subscription_id="subscription_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**subscription_id:** `str` — subscription_id
    
</dd>
</dl>

<dl>
<dd>

**trial_end:** `typing.Optional[dt.datetime]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## companies
<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">list_companies</a>(...) -> AsyncHttpResponse[ListCompaniesResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.list_companies(
    plan_id="plan_id",
    q="q",
    without_feature_override_for="without_feature_override_for",
    without_plan=True,
    with_subscription=True,
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter companies by multiple company IDs (starts with comp_)
    
</dd>
</dl>

<dl>
<dd>

**plan_id:** `typing.Optional[str]` — Filter companies by plan ID (starts with plan_)
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` — Search for companies by name, keys or string traits
    
</dd>
</dl>

<dl>
<dd>

**without_feature_override_for:** `typing.Optional[str]` — Filter out companies that already have a company override for the specified feature ID
    
</dd>
</dl>

<dl>
<dd>

**without_plan:** `typing.Optional[bool]` — Filter out companies that have a plan
    
</dd>
</dl>

<dl>
<dd>

**with_subscription:** `typing.Optional[bool]` — Filter companies that have a subscription
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">upsert_company</a>(...) -> AsyncHttpResponse[UpsertCompanyResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.upsert_company(
    keys={"key": "value"},
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**keys:** `typing.Dict[str, str]` — See [Key Management](https://docs.schematichq.com/developer_resources/key_management) for more information
    
</dd>
</dl>

<dl>
<dd>

**id:** `typing.Optional[str]` — If you know the Schematic ID, you can use that here instead of keys
    
</dd>
</dl>

<dl>
<dd>

**last_seen_at:** `typing.Optional[dt.datetime]` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**traits:** `typing.Optional[typing.Dict[str, typing.Any]]` — A map of trait names to trait values
    
</dd>
</dl>

<dl>
<dd>

**update_only:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_company</a>(...) -> AsyncHttpResponse[GetCompanyResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.get_company(
    company_id="company_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_id:** `str` — company_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">delete_company</a>(...) -> AsyncHttpResponse[DeleteCompanyResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.delete_company(
    company_id="company_id",
    cancel_subscription=True,
    prorate=True,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_id:** `str` — company_id
    
</dd>
</dl>

<dl>
<dd>

**cancel_subscription:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**prorate:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">count_companies</a>(...) -> AsyncHttpResponse[CountCompaniesResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.count_companies(
    plan_id="plan_id",
    q="q",
    without_feature_override_for="without_feature_override_for",
    without_plan=True,
    with_subscription=True,
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter companies by multiple company IDs (starts with comp_)
    
</dd>
</dl>

<dl>
<dd>

**plan_id:** `typing.Optional[str]` — Filter companies by plan ID (starts with plan_)
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` — Search for companies by name, keys or string traits
    
</dd>
</dl>

<dl>
<dd>

**without_feature_override_for:** `typing.Optional[str]` — Filter out companies that already have a company override for the specified feature ID
    
</dd>
</dl>

<dl>
<dd>

**without_plan:** `typing.Optional[bool]` — Filter out companies that have a plan
    
</dd>
</dl>

<dl>
<dd>

**with_subscription:** `typing.Optional[bool]` — Filter companies that have a subscription
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">count_companies_for_advanced_filter</a>(...) -> AsyncHttpResponse[CountCompaniesForAdvancedFilterResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.count_companies_for_advanced_filter(
    monetized_subscriptions=True,
    q="q",
    without_plan=True,
    without_subscription=True,
    sort_order_column="sort_order_column",
    sort_order_direction="asc",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter companies by multiple company IDs (starts with comp_)
    
</dd>
</dl>

<dl>
<dd>

**plan_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter companies by one or more plan IDs (each ID starts with plan_)
    
</dd>
</dl>

<dl>
<dd>

**feature_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter companies by one or more feature IDs (each ID starts with feat_)
    
</dd>
</dl>

<dl>
<dd>

**credit_type_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter companies by one or more credit type IDs (each ID starts with bcrd_)
    
</dd>
</dl>

<dl>
<dd>

**subscription_statuses:** `typing.Optional[
    typing.Union[SubscriptionStatus, typing.Sequence[SubscriptionStatus]]
]` — Filter companies by one or more subscription statuses (active, canceled, expired, incomplete, incomplete_expired, past_due, paused, trialing, unpaid)
    
</dd>
</dl>

<dl>
<dd>

**subscription_types:** `typing.Optional[
    typing.Union[SubscriptionType, typing.Sequence[SubscriptionType]]
]` — Filter companies by one or more subscription types (paid, free, trial)
    
</dd>
</dl>

<dl>
<dd>

**monetized_subscriptions:** `typing.Optional[bool]` — Filter companies that have monetized subscriptions
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` — Search for companies by name, keys or string traits
    
</dd>
</dl>

<dl>
<dd>

**without_plan:** `typing.Optional[bool]` — Filter out companies that have a plan
    
</dd>
</dl>

<dl>
<dd>

**without_subscription:** `typing.Optional[bool]` — Filter out companies that have a subscription
    
</dd>
</dl>

<dl>
<dd>

**sort_order_column:** `typing.Optional[str]` — Column to sort by (e.g. name, created_at, last_seen_at)
    
</dd>
</dl>

<dl>
<dd>

**sort_order_direction:** `typing.Optional[SortDirection]` — Direction to sort by (asc or desc)
    
</dd>
</dl>

<dl>
<dd>

**display_properties:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Select the display columns to return (e.g. plan, subscription, users, last_seen_at)
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">create_company</a>(...) -> AsyncHttpResponse[CreateCompanyResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.create_company(
    keys={"key": "value"},
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**keys:** `typing.Dict[str, str]` — See [Key Management](https://docs.schematichq.com/developer_resources/key_management) for more information
    
</dd>
</dl>

<dl>
<dd>

**id:** `typing.Optional[str]` — If you know the Schematic ID, you can use that here instead of keys
    
</dd>
</dl>

<dl>
<dd>

**last_seen_at:** `typing.Optional[dt.datetime]` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**traits:** `typing.Optional[typing.Dict[str, typing.Any]]` — A map of trait names to trait values
    
</dd>
</dl>

<dl>
<dd>

**update_only:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">delete_company_by_keys</a>(...) -> AsyncHttpResponse[DeleteCompanyByKeysResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.delete_company_by_keys(
    keys={"key": "value"},
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**keys:** `typing.Dict[str, str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">list_companies_for_advanced_filter</a>(...) -> AsyncHttpResponse[ListCompaniesForAdvancedFilterResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.list_companies_for_advanced_filter(
    monetized_subscriptions=True,
    q="q",
    without_plan=True,
    without_subscription=True,
    sort_order_column="sort_order_column",
    sort_order_direction="asc",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter companies by multiple company IDs (starts with comp_)
    
</dd>
</dl>

<dl>
<dd>

**plan_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter companies by one or more plan IDs (each ID starts with plan_)
    
</dd>
</dl>

<dl>
<dd>

**feature_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter companies by one or more feature IDs (each ID starts with feat_)
    
</dd>
</dl>

<dl>
<dd>

**credit_type_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter companies by one or more credit type IDs (each ID starts with bcrd_)
    
</dd>
</dl>

<dl>
<dd>

**subscription_statuses:** `typing.Optional[
    typing.Union[SubscriptionStatus, typing.Sequence[SubscriptionStatus]]
]` — Filter companies by one or more subscription statuses (active, canceled, expired, incomplete, incomplete_expired, past_due, paused, trialing, unpaid)
    
</dd>
</dl>

<dl>
<dd>

**subscription_types:** `typing.Optional[
    typing.Union[SubscriptionType, typing.Sequence[SubscriptionType]]
]` — Filter companies by one or more subscription types (paid, free, trial)
    
</dd>
</dl>

<dl>
<dd>

**monetized_subscriptions:** `typing.Optional[bool]` — Filter companies that have monetized subscriptions
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` — Search for companies by name, keys or string traits
    
</dd>
</dl>

<dl>
<dd>

**without_plan:** `typing.Optional[bool]` — Filter out companies that have a plan
    
</dd>
</dl>

<dl>
<dd>

**without_subscription:** `typing.Optional[bool]` — Filter out companies that have a subscription
    
</dd>
</dl>

<dl>
<dd>

**sort_order_column:** `typing.Optional[str]` — Column to sort by (e.g. name, created_at, last_seen_at)
    
</dd>
</dl>

<dl>
<dd>

**sort_order_direction:** `typing.Optional[SortDirection]` — Direction to sort by (asc or desc)
    
</dd>
</dl>

<dl>
<dd>

**display_properties:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Select the display columns to return (e.g. plan, subscription, users, last_seen_at)
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">lookup_company</a>(...) -> AsyncHttpResponse[LookupCompanyResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.lookup_company(
    keys={"keys": "keys"},
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**keys:** `typing.Dict[str, str]` — Key/value pairs
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">list_company_memberships</a>(...) -> AsyncHttpResponse[ListCompanyMembershipsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.list_company_memberships(
    company_id="company_id",
    user_id="user_id",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**user_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_or_create_company_membership</a>(...) -> AsyncHttpResponse[GetOrCreateCompanyMembershipResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.get_or_create_company_membership(
    company_id="company_id",
    user_id="user_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**user_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">delete_company_membership</a>(...) -> AsyncHttpResponse[DeleteCompanyMembershipResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.delete_company_membership(
    company_membership_id="company_membership_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_membership_id:** `str` — company_membership_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_active_company_subscription</a>(...) -> AsyncHttpResponse[GetActiveCompanySubscriptionResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.get_active_company_subscription(
    company_id="company_id",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**company_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">upsert_company_trait</a>(...) -> AsyncHttpResponse[UpsertCompanyTraitResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.upsert_company_trait(
    keys={"key": "value"},
    trait="trait",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**keys:** `typing.Dict[str, str]` — Key/value pairs to identify a company or user
    
</dd>
</dl>

<dl>
<dd>

**trait:** `str` — Name of the trait to update
    
</dd>
</dl>

<dl>
<dd>

**incr:** `typing.Optional[int]` — Amount to increment the trait by (positive or negative)
    
</dd>
</dl>

<dl>
<dd>

**set_:** `typing.Optional[str]` — Value to set the trait to
    
</dd>
</dl>

<dl>
<dd>

**update_only:** `typing.Optional[bool]` — Unless this is set, the company or user will be created if it does not already exist
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">list_entity_key_definitions</a>(...) -> AsyncHttpResponse[ListEntityKeyDefinitionsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.list_entity_key_definitions(
    entity_type="company",
    q="q",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**entity_type:** `typing.Optional[EntityType]` 
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">count_entity_key_definitions</a>(...) -> AsyncHttpResponse[CountEntityKeyDefinitionsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.count_entity_key_definitions(
    entity_type="company",
    q="q",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**entity_type:** `typing.Optional[EntityType]` 
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">list_entity_trait_definitions</a>(...) -> AsyncHttpResponse[ListEntityTraitDefinitionsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.list_entity_trait_definitions(
    entity_type="company",
    q="q",
    trait_type="boolean",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**entity_type:** `typing.Optional[EntityType]` 
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**trait_type:** `typing.Optional[TraitType]` 
    
</dd>
</dl>

<dl>
<dd>

**trait_types:** `typing.Optional[typing.Union[TraitType, typing.Sequence[TraitType]]]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_or_create_entity_trait_definition</a>(...) -> AsyncHttpResponse[GetOrCreateEntityTraitDefinitionResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.get_or_create_entity_trait_definition(
    entity_type="company",
    hierarchy=["hierarchy"],
    trait_type="boolean",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**entity_type:** `EntityType` 
    
</dd>
</dl>

<dl>
<dd>

**hierarchy:** `typing.Sequence[str]` 
    
</dd>
</dl>

<dl>
<dd>

**trait_type:** `TraitType` 
    
</dd>
</dl>

<dl>
<dd>

**display_name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_entity_trait_definition</a>(...) -> AsyncHttpResponse[GetEntityTraitDefinitionResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.get_entity_trait_definition(
    entity_trait_definition_id="entity_trait_definition_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**entity_trait_definition_id:** `str` — entity_trait_definition_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">update_entity_trait_definition</a>(...) -> AsyncHttpResponse[UpdateEntityTraitDefinitionResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.update_entity_trait_definition(
    entity_trait_definition_id="entity_trait_definition_id",
    trait_type="boolean",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**entity_trait_definition_id:** `str` — entity_trait_definition_id
    
</dd>
</dl>

<dl>
<dd>

**trait_type:** `TraitType` 
    
</dd>
</dl>

<dl>
<dd>

**display_name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">count_entity_trait_definitions</a>(...) -> AsyncHttpResponse[CountEntityTraitDefinitionsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.count_entity_trait_definitions(
    entity_type="company",
    q="q",
    trait_type="boolean",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**entity_type:** `typing.Optional[EntityType]` 
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**trait_type:** `typing.Optional[TraitType]` 
    
</dd>
</dl>

<dl>
<dd>

**trait_types:** `typing.Optional[typing.Union[TraitType, typing.Sequence[TraitType]]]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_entity_trait_values</a>(...) -> AsyncHttpResponse[GetEntityTraitValuesResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.get_entity_trait_values(
    definition_id="definition_id",
    q="q",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**definition_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">list_plan_changes</a>(...) -> AsyncHttpResponse[ListPlanChangesResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.list_plan_changes(
    action="action",
    base_plan_action="base_plan_action",
    company_id="company_id",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**action:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**base_plan_action:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**company_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**company_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**plan_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_plan_change</a>(...) -> AsyncHttpResponse[GetPlanChangeResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.get_plan_change(
    plan_change_id="plan_change_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**plan_change_id:** `str` — plan_change_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">list_plan_traits</a>(...) -> AsyncHttpResponse[ListPlanTraitsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.list_plan_traits(
    plan_id="plan_id",
    trait_id="trait_id",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**plan_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**trait_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**trait_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">create_plan_trait</a>(...) -> AsyncHttpResponse[CreatePlanTraitResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.create_plan_trait(
    plan_id="plan_id",
    trait_id="trait_id",
    trait_value="trait_value",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**plan_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**trait_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**trait_value:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_plan_trait</a>(...) -> AsyncHttpResponse[GetPlanTraitResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.get_plan_trait(
    plan_trait_id="plan_trait_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**plan_trait_id:** `str` — plan_trait_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">update_plan_trait</a>(...) -> AsyncHttpResponse[UpdatePlanTraitResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.update_plan_trait(
    plan_trait_id="plan_trait_id",
    plan_id="plan_id",
    trait_value="trait_value",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**plan_trait_id:** `str` — plan_trait_id
    
</dd>
</dl>

<dl>
<dd>

**plan_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**trait_value:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">delete_plan_trait</a>(...) -> AsyncHttpResponse[DeletePlanTraitResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.delete_plan_trait(
    plan_trait_id="plan_trait_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**plan_trait_id:** `str` — plan_trait_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">update_plan_traits_bulk</a>(...) -> AsyncHttpResponse[UpdatePlanTraitsBulkResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic, UpdatePlanTraitTraitRequestBody

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.update_plan_traits_bulk(
    apply_to_existing_companies=True,
    plan_id="plan_id",
    traits=[
        UpdatePlanTraitTraitRequestBody(
            trait_id="trait_id",
            trait_value="trait_value",
        )
    ],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**apply_to_existing_companies:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**plan_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**traits:** `typing.Sequence[UpdatePlanTraitTraitRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">count_plan_traits</a>(...) -> AsyncHttpResponse[CountPlanTraitsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.count_plan_traits(
    plan_id="plan_id",
    trait_id="trait_id",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**plan_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**trait_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**trait_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">upsert_user_trait</a>(...) -> AsyncHttpResponse[UpsertUserTraitResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.upsert_user_trait(
    keys={"key": "value"},
    trait="trait",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**keys:** `typing.Dict[str, str]` — Key/value pairs to identify a company or user
    
</dd>
</dl>

<dl>
<dd>

**trait:** `str` — Name of the trait to update
    
</dd>
</dl>

<dl>
<dd>

**incr:** `typing.Optional[int]` — Amount to increment the trait by (positive or negative)
    
</dd>
</dl>

<dl>
<dd>

**set_:** `typing.Optional[str]` — Value to set the trait to
    
</dd>
</dl>

<dl>
<dd>

**update_only:** `typing.Optional[bool]` — Unless this is set, the company or user will be created if it does not already exist
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">list_users</a>(...) -> AsyncHttpResponse[ListUsersResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.list_users(
    company_id="company_id",
    plan_id="plan_id",
    q="q",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_id:** `typing.Optional[str]` — Filter users by company ID (starts with comp_)
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter users by multiple user IDs (starts with user_)
    
</dd>
</dl>

<dl>
<dd>

**plan_id:** `typing.Optional[str]` — Filter users by plan ID (starts with plan_)
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` — Search for users by name, keys or string traits
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">upsert_user</a>(...) -> AsyncHttpResponse[UpsertUserResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.upsert_user(
    keys={"key": "value"},
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**keys:** `typing.Dict[str, str]` — See [Key Management](https://docs.schematichq.com/developer_resources/key_management) for more information
    
</dd>
</dl>

<dl>
<dd>

**companies:** `typing.Optional[typing.Sequence[typing.Dict[str, str]]]` — Optionally specify companies using array of key/value pairs
    
</dd>
</dl>

<dl>
<dd>

**company:** `typing.Optional[typing.Dict[str, str]]` — Add user to this company. Takes priority over companies. For exhaustive list of companies, use companies
    
</dd>
</dl>

<dl>
<dd>

**company_id:** `typing.Optional[str]` — Add user to this company. Takes priority over company_ids. For exhaustive list of companies, use company_ids
    
</dd>
</dl>

<dl>
<dd>

**company_ids:** `typing.Optional[typing.Sequence[str]]` — Optionally specify companies using Schematic company ID
    
</dd>
</dl>

<dl>
<dd>

**id:** `typing.Optional[str]` — If you know the Schematic ID, you can use that here instead of keys
    
</dd>
</dl>

<dl>
<dd>

**last_seen_at:** `typing.Optional[dt.datetime]` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**traits:** `typing.Optional[typing.Dict[str, typing.Any]]` — A map of trait names to trait values
    
</dd>
</dl>

<dl>
<dd>

**update_only:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_user</a>(...) -> AsyncHttpResponse[GetUserResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.get_user(
    user_id="user_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**user_id:** `str` — user_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">delete_user</a>(...) -> AsyncHttpResponse[DeleteUserResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.delete_user(
    user_id="user_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**user_id:** `str` — user_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">count_users</a>(...) -> AsyncHttpResponse[CountUsersResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.count_users(
    company_id="company_id",
    plan_id="plan_id",
    q="q",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_id:** `typing.Optional[str]` — Filter users by company ID (starts with comp_)
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter users by multiple user IDs (starts with user_)
    
</dd>
</dl>

<dl>
<dd>

**plan_id:** `typing.Optional[str]` — Filter users by plan ID (starts with plan_)
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` — Search for users by name, keys or string traits
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">create_user</a>(...) -> AsyncHttpResponse[CreateUserResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.create_user(
    keys={"key": "value"},
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**keys:** `typing.Dict[str, str]` — See [Key Management](https://docs.schematichq.com/developer_resources/key_management) for more information
    
</dd>
</dl>

<dl>
<dd>

**companies:** `typing.Optional[typing.Sequence[typing.Dict[str, str]]]` — Optionally specify companies using array of key/value pairs
    
</dd>
</dl>

<dl>
<dd>

**company:** `typing.Optional[typing.Dict[str, str]]` — Add user to this company. Takes priority over companies. For exhaustive list of companies, use companies
    
</dd>
</dl>

<dl>
<dd>

**company_id:** `typing.Optional[str]` — Add user to this company. Takes priority over company_ids. For exhaustive list of companies, use company_ids
    
</dd>
</dl>

<dl>
<dd>

**company_ids:** `typing.Optional[typing.Sequence[str]]` — Optionally specify companies using Schematic company ID
    
</dd>
</dl>

<dl>
<dd>

**id:** `typing.Optional[str]` — If you know the Schematic ID, you can use that here instead of keys
    
</dd>
</dl>

<dl>
<dd>

**last_seen_at:** `typing.Optional[dt.datetime]` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**traits:** `typing.Optional[typing.Dict[str, typing.Any]]` — A map of trait names to trait values
    
</dd>
</dl>

<dl>
<dd>

**update_only:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">delete_user_by_keys</a>(...) -> AsyncHttpResponse[DeleteUserByKeysResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.delete_user_by_keys(
    keys={"key": "value"},
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**keys:** `typing.Dict[str, str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">lookup_user</a>(...) -> AsyncHttpResponse[LookupUserResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.companies.lookup_user(
    keys={"keys": "keys"},
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**keys:** `typing.Dict[str, str]` — Key/value pairs
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## entitlements
<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">list_company_overrides</a>(...) -> AsyncHttpResponse[ListCompanyOverridesResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.entitlements.list_company_overrides(
    company_id="company_id",
    feature_id="feature_id",
    without_expired=True,
    q="q",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_id:** `typing.Optional[str]` — Filter company overrides by a single company ID (starting with comp_)
    
</dd>
</dl>

<dl>
<dd>

**company_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter company overrides by multiple company IDs (starting with comp_)
    
</dd>
</dl>

<dl>
<dd>

**feature_id:** `typing.Optional[str]` — Filter company overrides by a single feature ID (starting with feat_)
    
</dd>
</dl>

<dl>
<dd>

**feature_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter company overrides by multiple feature IDs (starting with feat_)
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter company overrides by multiple company override IDs (starting with cmov_)
    
</dd>
</dl>

<dl>
<dd>

**without_expired:** `typing.Optional[bool]` — Filter company overrides by whether they have not expired
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` — Search for company overrides by feature or company name
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">create_company_override</a>(...) -> AsyncHttpResponse[CreateCompanyOverrideResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.entitlements.create_company_override(
    company_id="company_id",
    feature_id="feature_id",
    value_type="boolean",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**feature_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**value_type:** `EntitlementValueType` 
    
</dd>
</dl>

<dl>
<dd>

**credit_consumption_rate:** `typing.Optional[float]` 
    
</dd>
</dl>

<dl>
<dd>

**expiration_date:** `typing.Optional[dt.datetime]` 
    
</dd>
</dl>

<dl>
<dd>

**metric_period:** `typing.Optional[CreateCompanyOverrideRequestBodyMetricPeriod]` 
    
</dd>
</dl>

<dl>
<dd>

**metric_period_month_reset:** `typing.Optional[CreateCompanyOverrideRequestBodyMetricPeriodMonthReset]` 
    
</dd>
</dl>

<dl>
<dd>

**note:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**value_bool:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**value_credit_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**value_numeric:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**value_trait_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">get_company_override</a>(...) -> AsyncHttpResponse[GetCompanyOverrideResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.entitlements.get_company_override(
    company_override_id="company_override_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_override_id:** `str` — company_override_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">update_company_override</a>(...) -> AsyncHttpResponse[UpdateCompanyOverrideResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.entitlements.update_company_override(
    company_override_id="company_override_id",
    value_type="boolean",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_override_id:** `str` — company_override_id
    
</dd>
</dl>

<dl>
<dd>

**value_type:** `EntitlementValueType` 
    
</dd>
</dl>

<dl>
<dd>

**credit_consumption_rate:** `typing.Optional[float]` 
    
</dd>
</dl>

<dl>
<dd>

**expiration_date:** `typing.Optional[dt.datetime]` 
    
</dd>
</dl>

<dl>
<dd>

**metric_period:** `typing.Optional[UpdateCompanyOverrideRequestBodyMetricPeriod]` 
    
</dd>
</dl>

<dl>
<dd>

**metric_period_month_reset:** `typing.Optional[UpdateCompanyOverrideRequestBodyMetricPeriodMonthReset]` 
    
</dd>
</dl>

<dl>
<dd>

**note:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**value_bool:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**value_credit_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**value_numeric:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**value_trait_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">delete_company_override</a>(...) -> AsyncHttpResponse[DeleteCompanyOverrideResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.entitlements.delete_company_override(
    company_override_id="company_override_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_override_id:** `str` — company_override_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">count_company_overrides</a>(...) -> AsyncHttpResponse[CountCompanyOverridesResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.entitlements.count_company_overrides(
    company_id="company_id",
    feature_id="feature_id",
    without_expired=True,
    q="q",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_id:** `typing.Optional[str]` — Filter company overrides by a single company ID (starting with comp_)
    
</dd>
</dl>

<dl>
<dd>

**company_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter company overrides by multiple company IDs (starting with comp_)
    
</dd>
</dl>

<dl>
<dd>

**feature_id:** `typing.Optional[str]` — Filter company overrides by a single feature ID (starting with feat_)
    
</dd>
</dl>

<dl>
<dd>

**feature_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter company overrides by multiple feature IDs (starting with feat_)
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter company overrides by multiple company override IDs (starting with cmov_)
    
</dd>
</dl>

<dl>
<dd>

**without_expired:** `typing.Optional[bool]` — Filter company overrides by whether they have not expired
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` — Search for company overrides by feature or company name
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">list_feature_companies</a>(...) -> AsyncHttpResponse[ListFeatureCompaniesResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.entitlements.list_feature_companies(
    feature_id="feature_id",
    q="q",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**feature_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">count_feature_companies</a>(...) -> AsyncHttpResponse[CountFeatureCompaniesResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.entitlements.count_feature_companies(
    feature_id="feature_id",
    q="q",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**feature_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">list_feature_usage</a>(...) -> AsyncHttpResponse[ListFeatureUsageResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.entitlements.list_feature_usage(
    company_id="company_id",
    include_usage_aggregation=True,
    q="q",
    without_negative_entitlements=True,
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**company_keys:** `typing.Optional[typing.Dict[str, str]]` 
    
</dd>
</dl>

<dl>
<dd>

**feature_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**include_usage_aggregation:** `typing.Optional[bool]` — Include time-bucketed usage aggregation (today, this week, this month, billing period) for credit-based entitlements. Defaults to false for performance.
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**without_negative_entitlements:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">count_feature_usage</a>(...) -> AsyncHttpResponse[CountFeatureUsageResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.entitlements.count_feature_usage(
    company_id="company_id",
    include_usage_aggregation=True,
    q="q",
    without_negative_entitlements=True,
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**company_keys:** `typing.Optional[typing.Dict[str, str]]` 
    
</dd>
</dl>

<dl>
<dd>

**feature_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**include_usage_aggregation:** `typing.Optional[bool]` — Include time-bucketed usage aggregation (today, this week, this month, billing period) for credit-based entitlements. Defaults to false for performance.
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**without_negative_entitlements:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">list_feature_users</a>(...) -> AsyncHttpResponse[ListFeatureUsersResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.entitlements.list_feature_users(
    feature_id="feature_id",
    q="q",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**feature_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">count_feature_users</a>(...) -> AsyncHttpResponse[CountFeatureUsersResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.entitlements.count_feature_users(
    feature_id="feature_id",
    q="q",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**feature_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">list_plan_entitlements</a>(...) -> AsyncHttpResponse[ListPlanEntitlementsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.entitlements.list_plan_entitlements(
    feature_id="feature_id",
    plan_id="plan_id",
    q="q",
    with_metered_products=True,
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**feature_id:** `typing.Optional[str]` — Filter plan entitlements by a single feature ID (starting with feat_)
    
</dd>
</dl>

<dl>
<dd>

**feature_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter plan entitlements by multiple feature IDs (starting with feat_)
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter plan entitlements by multiple plan entitlement IDs (starting with pltl_)
    
</dd>
</dl>

<dl>
<dd>

**plan_id:** `typing.Optional[str]` — Filter plan entitlements by a single plan ID (starting with plan_)
    
</dd>
</dl>

<dl>
<dd>

**plan_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter plan entitlements by multiple plan IDs (starting with plan_)
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` — Search for plan entitlements by feature or company name
    
</dd>
</dl>

<dl>
<dd>

**with_metered_products:** `typing.Optional[bool]` — Filter plan entitlements only with metered products
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">create_plan_entitlement</a>(...) -> AsyncHttpResponse[CreatePlanEntitlementResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.entitlements.create_plan_entitlement(
    feature_id="feature_id",
    plan_id="plan_id",
    value_type="boolean",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**feature_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**plan_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**value_type:** `EntitlementValueType` 
    
</dd>
</dl>

<dl>
<dd>

**billing_product_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**billing_threshold:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**credit_consumption_rate:** `typing.Optional[float]` 
    
</dd>
</dl>

<dl>
<dd>

**currency:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**metric_period:** `typing.Optional[CreatePlanEntitlementRequestBodyMetricPeriod]` 
    
</dd>
</dl>

<dl>
<dd>

**metric_period_month_reset:** `typing.Optional[CreatePlanEntitlementRequestBodyMetricPeriodMonthReset]` 
    
</dd>
</dl>

<dl>
<dd>

**monthly_metered_price_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**monthly_price_tiers:** `typing.Optional[typing.Sequence[CreatePriceTierRequestBody]]` 
    
</dd>
</dl>

<dl>
<dd>

**monthly_unit_price:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**monthly_unit_price_decimal:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**overage_billing_product_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**price_behavior:** `typing.Optional[EntitlementPriceBehavior]` 
    
</dd>
</dl>

<dl>
<dd>

**price_tiers:** `typing.Optional[typing.Sequence[CreatePriceTierRequestBody]]` — Use MonthlyPriceTiers or YearlyPriceTiers instead
    
</dd>
</dl>

<dl>
<dd>

**soft_limit:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**tier_mode:** `typing.Optional[BillingTiersMode]` 
    
</dd>
</dl>

<dl>
<dd>

**value_bool:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**value_credit_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**value_numeric:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**value_trait_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**yearly_metered_price_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**yearly_price_tiers:** `typing.Optional[typing.Sequence[CreatePriceTierRequestBody]]` 
    
</dd>
</dl>

<dl>
<dd>

**yearly_unit_price:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**yearly_unit_price_decimal:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">get_plan_entitlement</a>(...) -> AsyncHttpResponse[GetPlanEntitlementResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.entitlements.get_plan_entitlement(
    plan_entitlement_id="plan_entitlement_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**plan_entitlement_id:** `str` — plan_entitlement_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">update_plan_entitlement</a>(...) -> AsyncHttpResponse[UpdatePlanEntitlementResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.entitlements.update_plan_entitlement(
    plan_entitlement_id="plan_entitlement_id",
    value_type="boolean",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**plan_entitlement_id:** `str` — plan_entitlement_id
    
</dd>
</dl>

<dl>
<dd>

**value_type:** `EntitlementValueType` 
    
</dd>
</dl>

<dl>
<dd>

**billing_product_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**billing_threshold:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**credit_consumption_rate:** `typing.Optional[float]` 
    
</dd>
</dl>

<dl>
<dd>

**currency:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**metric_period:** `typing.Optional[UpdatePlanEntitlementRequestBodyMetricPeriod]` 
    
</dd>
</dl>

<dl>
<dd>

**metric_period_month_reset:** `typing.Optional[UpdatePlanEntitlementRequestBodyMetricPeriodMonthReset]` 
    
</dd>
</dl>

<dl>
<dd>

**monthly_metered_price_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**monthly_price_tiers:** `typing.Optional[typing.Sequence[CreatePriceTierRequestBody]]` 
    
</dd>
</dl>

<dl>
<dd>

**monthly_unit_price:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**monthly_unit_price_decimal:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**overage_billing_product_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**price_behavior:** `typing.Optional[EntitlementPriceBehavior]` 
    
</dd>
</dl>

<dl>
<dd>

**price_tiers:** `typing.Optional[typing.Sequence[CreatePriceTierRequestBody]]` — Use MonthlyPriceTiers or YearlyPriceTiers instead
    
</dd>
</dl>

<dl>
<dd>

**soft_limit:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**tier_mode:** `typing.Optional[BillingTiersMode]` 
    
</dd>
</dl>

<dl>
<dd>

**value_bool:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**value_credit_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**value_numeric:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**value_trait_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**yearly_metered_price_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**yearly_price_tiers:** `typing.Optional[typing.Sequence[CreatePriceTierRequestBody]]` 
    
</dd>
</dl>

<dl>
<dd>

**yearly_unit_price:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**yearly_unit_price_decimal:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">delete_plan_entitlement</a>(...) -> AsyncHttpResponse[DeletePlanEntitlementResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.entitlements.delete_plan_entitlement(
    plan_entitlement_id="plan_entitlement_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**plan_entitlement_id:** `str` — plan_entitlement_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">count_plan_entitlements</a>(...) -> AsyncHttpResponse[CountPlanEntitlementsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.entitlements.count_plan_entitlements(
    feature_id="feature_id",
    plan_id="plan_id",
    q="q",
    with_metered_products=True,
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**feature_id:** `typing.Optional[str]` — Filter plan entitlements by a single feature ID (starting with feat_)
    
</dd>
</dl>

<dl>
<dd>

**feature_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter plan entitlements by multiple feature IDs (starting with feat_)
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter plan entitlements by multiple plan entitlement IDs (starting with pltl_)
    
</dd>
</dl>

<dl>
<dd>

**plan_id:** `typing.Optional[str]` — Filter plan entitlements by a single plan ID (starting with plan_)
    
</dd>
</dl>

<dl>
<dd>

**plan_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter plan entitlements by multiple plan IDs (starting with plan_)
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` — Search for plan entitlements by feature or company name
    
</dd>
</dl>

<dl>
<dd>

**with_metered_products:** `typing.Optional[bool]` — Filter plan entitlements only with metered products
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">duplicate_plan_entitlements</a>(...) -> AsyncHttpResponse[DuplicatePlanEntitlementsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.entitlements.duplicate_plan_entitlements(
    source_plan_id="source_plan_id",
    target_plan_id="target_plan_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**source_plan_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**target_plan_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">get_feature_usage_by_company</a>(...) -> AsyncHttpResponse[GetFeatureUsageByCompanyResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.entitlements.get_feature_usage_by_company(
    keys={"keys": "keys"},
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**keys:** `typing.Dict[str, str]` — Key/value pairs
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## plans
<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">update_company_plans</a>(...) -> AsyncHttpResponse[UpdateCompanyPlansResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.plans.update_company_plans(
    company_plan_id="company_plan_id",
    add_on_ids=["add_on_ids"],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_plan_id:** `str` — company_plan_id
    
</dd>
</dl>

<dl>
<dd>

**add_on_ids:** `typing.Sequence[str]` 
    
</dd>
</dl>

<dl>
<dd>

**base_plan_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">list_plans</a>(...) -> AsyncHttpResponse[ListPlansResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.plans.list_plans(
    company_id="company_id",
    for_fallback_plan=True,
    for_initial_plan=True,
    for_trial_expiry_plan=True,
    has_product_id=True,
    plan_type="plan",
    q="q",
    without_entitlement_for="without_entitlement_for",
    without_paid_product_id=True,
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**for_fallback_plan:** `typing.Optional[bool]` — Filter for plans valid as fallback plans (not linked to billing)
    
</dd>
</dl>

<dl>
<dd>

**for_initial_plan:** `typing.Optional[bool]` — Filter for plans valid as initial plans (not linked to billing, free, or auto-cancelling trial)
    
</dd>
</dl>

<dl>
<dd>

**for_trial_expiry_plan:** `typing.Optional[bool]` — Filter for plans valid as trial expiry plans (not linked to billing or free)
    
</dd>
</dl>

<dl>
<dd>

**has_product_id:** `typing.Optional[bool]` — Filter out plans that do not have a billing product ID
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**plan_type:** `typing.Optional[PlanType]` — Filter by plan type
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**without_entitlement_for:** `typing.Optional[str]` — Filter out plans that already have a plan entitlement for the specified feature ID
    
</dd>
</dl>

<dl>
<dd>

**without_paid_product_id:** `typing.Optional[bool]` — Filter out plans that have a paid billing product ID
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">create_plan</a>(...) -> AsyncHttpResponse[CreatePlanResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.plans.create_plan(
    description="description",
    name="name",
    plan_type="plan",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**description:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**plan_type:** `PlanType` 
    
</dd>
</dl>

<dl>
<dd>

**icon:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">get_plan</a>(...) -> AsyncHttpResponse[GetPlanResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.plans.get_plan(
    plan_id="plan_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**plan_id:** `str` — plan_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">update_plan</a>(...) -> AsyncHttpResponse[UpdatePlanResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.plans.update_plan(
    plan_id="plan_id",
    name="name",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**plan_id:** `str` — plan_id
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**icon:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">delete_plan</a>(...) -> AsyncHttpResponse[DeletePlanResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.plans.delete_plan(
    plan_id="plan_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**plan_id:** `str` — plan_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">upsert_billing_product_plan</a>(...) -> AsyncHttpResponse[UpsertBillingProductPlanResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.plans.upsert_billing_product_plan(
    plan_id="plan_id",
    charge_type="free",
    is_trialable=True,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**plan_id:** `str` — plan_id
    
</dd>
</dl>

<dl>
<dd>

**charge_type:** `ChargeType` 
    
</dd>
</dl>

<dl>
<dd>

**is_trialable:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**billing_product_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**currency:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**monthly_price:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**monthly_price_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**one_time_price:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**one_time_price_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**trial_days:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**yearly_price:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**yearly_price_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">count_plans</a>(...) -> AsyncHttpResponse[CountPlansResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.plans.count_plans(
    company_id="company_id",
    for_fallback_plan=True,
    for_initial_plan=True,
    for_trial_expiry_plan=True,
    has_product_id=True,
    plan_type="plan",
    q="q",
    without_entitlement_for="without_entitlement_for",
    without_paid_product_id=True,
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**for_fallback_plan:** `typing.Optional[bool]` — Filter for plans valid as fallback plans (not linked to billing)
    
</dd>
</dl>

<dl>
<dd>

**for_initial_plan:** `typing.Optional[bool]` — Filter for plans valid as initial plans (not linked to billing, free, or auto-cancelling trial)
    
</dd>
</dl>

<dl>
<dd>

**for_trial_expiry_plan:** `typing.Optional[bool]` — Filter for plans valid as trial expiry plans (not linked to billing or free)
    
</dd>
</dl>

<dl>
<dd>

**has_product_id:** `typing.Optional[bool]` — Filter out plans that do not have a billing product ID
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**plan_type:** `typing.Optional[PlanType]` — Filter by plan type
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**without_entitlement_for:** `typing.Optional[str]` — Filter out plans that already have a plan entitlement for the specified feature ID
    
</dd>
</dl>

<dl>
<dd>

**without_paid_product_id:** `typing.Optional[bool]` — Filter out plans that have a paid billing product ID
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">list_plan_issues</a>(...) -> AsyncHttpResponse[ListPlanIssuesResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.plans.list_plan_issues(
    plan_id="plan_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**plan_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## components
<details><summary><code>client.components.<a href="src/schematic/components/client.py">list_components</a>(...) -> AsyncHttpResponse[ListComponentsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.components.list_components(
    q="q",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.components.<a href="src/schematic/components/client.py">create_component</a>(...) -> AsyncHttpResponse[CreateComponentResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.components.create_component(
    entity_type="billing",
    name="name",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**entity_type:** `ComponentEntityType` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**ast:** `typing.Optional[typing.Dict[str, float]]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.components.<a href="src/schematic/components/client.py">get_component</a>(...) -> AsyncHttpResponse[GetComponentResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.components.get_component(
    component_id="component_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**component_id:** `str` — component_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.components.<a href="src/schematic/components/client.py">update_component</a>(...) -> AsyncHttpResponse[UpdateComponentResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.components.update_component(
    component_id="component_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**component_id:** `str` — component_id
    
</dd>
</dl>

<dl>
<dd>

**ast:** `typing.Optional[typing.Dict[str, float]]` 
    
</dd>
</dl>

<dl>
<dd>

**entity_type:** `typing.Optional[ComponentEntityType]` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**state:** `typing.Optional[ComponentState]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.components.<a href="src/schematic/components/client.py">delete_component</a>(...) -> AsyncHttpResponse[DeleteComponentResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.components.delete_component(
    component_id="component_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**component_id:** `str` — component_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.components.<a href="src/schematic/components/client.py">count_components</a>(...) -> AsyncHttpResponse[CountComponentsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.components.count_components(
    q="q",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.components.<a href="src/schematic/components/client.py">preview_component_data</a>(...) -> AsyncHttpResponse[PreviewComponentDataResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.components.preview_component_data(
    company_id="company_id",
    component_id="component_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**component_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## dataexports
<details><summary><code>client.dataexports.<a href="src/schematic/dataexports/client.py">create_data_export</a>(...) -> AsyncHttpResponse[CreateDataExportResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.dataexports.create_data_export(
    metadata="metadata",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**metadata:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.dataexports.<a href="src/schematic/dataexports/client.py">get_data_export_artifact</a>(...) -> typing.AsyncIterator[AsyncHttpResponse[typing.AsyncIterator[bytes]]]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.dataexports.get_data_export_artifact(
    data_export_id="data_export_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**data_export_id:** `str` — data_export_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## events
<details><summary><code>client.events.<a href="src/schematic/events/client.py">create_event_batch</a>(...) -> AsyncHttpResponse[CreateEventBatchResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import CreateEventRequestBody, Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.events.create_event_batch(
    events=[
        CreateEventRequestBody(
            event_type="flag_check",
        )
    ],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**events:** `typing.Sequence[CreateEventRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.events.<a href="src/schematic/events/client.py">get_event_summaries</a>(...) -> AsyncHttpResponse[GetEventSummariesResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.events.get_event_summaries(
    q="q",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**event_subtypes:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.events.<a href="src/schematic/events/client.py">list_events</a>(...) -> AsyncHttpResponse[ListEventsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.events.list_events(
    company_id="company_id",
    event_subtype="event_subtype",
    flag_id="flag_id",
    user_id="user_id",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**event_subtype:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**event_types:** `typing.Optional[typing.Union[EventType, typing.Sequence[EventType]]]` 
    
</dd>
</dl>

<dl>
<dd>

**flag_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**user_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.events.<a href="src/schematic/events/client.py">create_event</a>(...) -> AsyncHttpResponse[CreateEventResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.events.create_event(
    event_type="flag_check",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**event_type:** `EventType` 
    
</dd>
</dl>

<dl>
<dd>

**body:** `typing.Optional[EventBody]` 
    
</dd>
</dl>

<dl>
<dd>

**sent_at:** `typing.Optional[dt.datetime]` — Optionally provide a timestamp at which the event was sent to Schematic
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.events.<a href="src/schematic/events/client.py">get_event</a>(...) -> AsyncHttpResponse[GetEventResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.events.get_event(
    event_id="event_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**event_id:** `str` — event_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.events.<a href="src/schematic/events/client.py">get_segment_integration_status</a>() -> AsyncHttpResponse[GetSegmentIntegrationStatusResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.events.get_segment_integration_status()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## features
<details><summary><code>client.features.<a href="src/schematic/features/client.py">list_features</a>(...) -> AsyncHttpResponse[ListFeaturesResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.features.list_features(
    q="q",
    without_company_override_for="without_company_override_for",
    without_plan_entitlement_for="without_plan_entitlement_for",
    boolean_require_event=True,
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` — Search by feature name or ID
    
</dd>
</dl>

<dl>
<dd>

**without_company_override_for:** `typing.Optional[str]` — Filter out features that already have a company override for the specified company ID
    
</dd>
</dl>

<dl>
<dd>

**without_plan_entitlement_for:** `typing.Optional[str]` — Filter out features that already have a plan entitlement for the specified plan ID
    
</dd>
</dl>

<dl>
<dd>

**feature_type:** `typing.Optional[typing.Union[FeatureType, typing.Sequence[FeatureType]]]` — Filter by one or more feature types (boolean, event, trait)
    
</dd>
</dl>

<dl>
<dd>

**boolean_require_event:** `typing.Optional[bool]` — Only return boolean features if there is an associated event. Automatically includes boolean in the feature types filter.
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.features.<a href="src/schematic/features/client.py">create_feature</a>(...) -> AsyncHttpResponse[CreateFeatureResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.features.create_feature(
    description="description",
    feature_type="boolean",
    name="name",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**description:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**feature_type:** `FeatureType` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**event_subtype:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**flag:** `typing.Optional[CreateOrUpdateFlagRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**icon:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**lifecycle_phase:** `typing.Optional[FeatureLifecyclePhase]` 
    
</dd>
</dl>

<dl>
<dd>

**maintainer_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**plural_name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**singular_name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**trait_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.features.<a href="src/schematic/features/client.py">get_feature</a>(...) -> AsyncHttpResponse[GetFeatureResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.features.get_feature(
    feature_id="feature_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**feature_id:** `str` — feature_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.features.<a href="src/schematic/features/client.py">update_feature</a>(...) -> AsyncHttpResponse[UpdateFeatureResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.features.update_feature(
    feature_id="feature_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**feature_id:** `str` — feature_id
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**event_subtype:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**feature_type:** `typing.Optional[FeatureType]` 
    
</dd>
</dl>

<dl>
<dd>

**flag:** `typing.Optional[CreateOrUpdateFlagRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**icon:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**lifecycle_phase:** `typing.Optional[FeatureLifecyclePhase]` 
    
</dd>
</dl>

<dl>
<dd>

**maintainer_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**plural_name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**singular_name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**trait_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.features.<a href="src/schematic/features/client.py">delete_feature</a>(...) -> AsyncHttpResponse[DeleteFeatureResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.features.delete_feature(
    feature_id="feature_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**feature_id:** `str` — feature_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.features.<a href="src/schematic/features/client.py">count_features</a>(...) -> AsyncHttpResponse[CountFeaturesResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.features.count_features(
    q="q",
    without_company_override_for="without_company_override_for",
    without_plan_entitlement_for="without_plan_entitlement_for",
    boolean_require_event=True,
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` — Search by feature name or ID
    
</dd>
</dl>

<dl>
<dd>

**without_company_override_for:** `typing.Optional[str]` — Filter out features that already have a company override for the specified company ID
    
</dd>
</dl>

<dl>
<dd>

**without_plan_entitlement_for:** `typing.Optional[str]` — Filter out features that already have a plan entitlement for the specified plan ID
    
</dd>
</dl>

<dl>
<dd>

**feature_type:** `typing.Optional[typing.Union[FeatureType, typing.Sequence[FeatureType]]]` — Filter by one or more feature types (boolean, event, trait)
    
</dd>
</dl>

<dl>
<dd>

**boolean_require_event:** `typing.Optional[bool]` — Only return boolean features if there is an associated event. Automatically includes boolean in the feature types filter.
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.features.<a href="src/schematic/features/client.py">list_flags</a>(...) -> AsyncHttpResponse[ListFlagsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.features.list_flags(
    feature_id="feature_id",
    q="q",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**feature_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` — Search by flag name, key, or ID
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.features.<a href="src/schematic/features/client.py">create_flag</a>(...) -> AsyncHttpResponse[CreateFlagResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.features.create_flag(
    default_value=True,
    description="description",
    key="key",
    name="name",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**default_value:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**description:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**key:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**feature_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**maintainer_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.features.<a href="src/schematic/features/client.py">get_flag</a>(...) -> AsyncHttpResponse[GetFlagResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.features.get_flag(
    flag_id="flag_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**flag_id:** `str` — flag_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.features.<a href="src/schematic/features/client.py">update_flag</a>(...) -> AsyncHttpResponse[UpdateFlagResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.features.update_flag(
    flag_id="flag_id",
    default_value=True,
    description="description",
    key="key",
    name="name",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**flag_id:** `str` — flag_id
    
</dd>
</dl>

<dl>
<dd>

**default_value:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**description:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**key:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**feature_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**maintainer_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.features.<a href="src/schematic/features/client.py">delete_flag</a>(...) -> AsyncHttpResponse[DeleteFlagResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.features.delete_flag(
    flag_id="flag_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**flag_id:** `str` — flag_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.features.<a href="src/schematic/features/client.py">update_flag_rules</a>(...) -> AsyncHttpResponse[UpdateFlagRulesResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import (
    CreateOrUpdateConditionGroupRequestBody,
    CreateOrUpdateConditionRequestBody,
    CreateOrUpdateRuleRequestBody,
    Schematic,
)

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.features.update_flag_rules(
    flag_id="flag_id",
    rules=[
        CreateOrUpdateRuleRequestBody(
            condition_groups=[
                CreateOrUpdateConditionGroupRequestBody(
                    conditions=[
                        CreateOrUpdateConditionRequestBody(
                            condition_type="company",
                            operator="eq",
                            resource_ids=["resource_ids"],
                        )
                    ],
                )
            ],
            conditions=[
                CreateOrUpdateConditionRequestBody(
                    condition_type="company",
                    operator="eq",
                    resource_ids=["resource_ids"],
                )
            ],
            name="name",
            priority=1,
            value=True,
        )
    ],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**flag_id:** `str` — flag_id
    
</dd>
</dl>

<dl>
<dd>

**rules:** `typing.Sequence[CreateOrUpdateRuleRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.features.<a href="src/schematic/features/client.py">check_flag</a>(...) -> AsyncHttpResponse[CheckFlagResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.features.check_flag(
    key="key",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**key:** `str` — key
    
</dd>
</dl>

<dl>
<dd>

**company:** `typing.Optional[typing.Dict[str, str]]` 
    
</dd>
</dl>

<dl>
<dd>

**user:** `typing.Optional[typing.Dict[str, str]]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.features.<a href="src/schematic/features/client.py">check_flags</a>(...) -> AsyncHttpResponse[CheckFlagsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.features.check_flags()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**company:** `typing.Optional[typing.Dict[str, str]]` 
    
</dd>
</dl>

<dl>
<dd>

**user:** `typing.Optional[typing.Dict[str, str]]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.features.<a href="src/schematic/features/client.py">check_flags_bulk</a>(...) -> AsyncHttpResponse[CheckFlagsBulkResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import CheckFlagRequestBody, Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.features.check_flags_bulk(
    contexts=[CheckFlagRequestBody()],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**contexts:** `typing.Sequence[CheckFlagRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.features.<a href="src/schematic/features/client.py">count_flags</a>(...) -> AsyncHttpResponse[CountFlagsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.features.count_flags(
    feature_id="feature_id",
    q="q",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**feature_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` — Search by flag name, key, or ID
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## plangroups
<details><summary><code>client.plangroups.<a href="src/schematic/plangroups/client.py">get_plan_group</a>() -> AsyncHttpResponse[GetPlanGroupResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.plangroups.get_plan_group()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.plangroups.<a href="src/schematic/plangroups/client.py">create_plan_group</a>(...) -> AsyncHttpResponse[CreatePlanGroupResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import OrderedPlansInGroup, PlanGroupBundleOrder, Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.plangroups.create_plan_group(
    add_on_ids=["add_on_ids"],
    checkout_collect_address=True,
    checkout_collect_email=True,
    checkout_collect_phone=True,
    enable_tax_collection=True,
    ordered_add_ons=[
        OrderedPlansInGroup(
            plan_id="plan_id",
        )
    ],
    ordered_bundle_list=[
        PlanGroupBundleOrder(
            bundle_id="bundleId",
        )
    ],
    ordered_plans=[
        OrderedPlansInGroup(
            plan_id="plan_id",
        )
    ],
    prevent_downgrades_when_over_limit=True,
    prevent_self_service_downgrade=True,
    proration_behavior="create_prorations",
    show_as_monthly_prices=True,
    show_credits=True,
    show_period_toggle=True,
    show_zero_price_as_free=True,
    sync_customer_billing_details=True,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**add_on_ids:** `typing.Sequence[str]` — Use OrderedAddOns instead
    
</dd>
</dl>

<dl>
<dd>

**checkout_collect_address:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**checkout_collect_email:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**checkout_collect_phone:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**enable_tax_collection:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**ordered_add_ons:** `typing.Sequence[OrderedPlansInGroup]` 
    
</dd>
</dl>

<dl>
<dd>

**ordered_bundle_list:** `typing.Sequence[PlanGroupBundleOrder]` 
    
</dd>
</dl>

<dl>
<dd>

**ordered_plans:** `typing.Sequence[OrderedPlansInGroup]` 
    
</dd>
</dl>

<dl>
<dd>

**prevent_downgrades_when_over_limit:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**prevent_self_service_downgrade:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**proration_behavior:** `ProrationBehavior` 
    
</dd>
</dl>

<dl>
<dd>

**show_as_monthly_prices:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**show_credits:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**show_period_toggle:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**show_zero_price_as_free:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**sync_customer_billing_details:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**add_on_compatibilities:** `typing.Optional[typing.Sequence[CompatiblePlans]]` 
    
</dd>
</dl>

<dl>
<dd>

**custom_plan_config:** `typing.Optional[CustomPlanConfig]` 
    
</dd>
</dl>

<dl>
<dd>

**custom_plan_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**fallback_plan_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**initial_plan_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**initial_plan_price_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**prevent_self_service_downgrade_button_text:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**prevent_self_service_downgrade_url:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**trial_days:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**trial_expiry_plan_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**trial_expiry_plan_price_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**trial_payment_method_required:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.plangroups.<a href="src/schematic/plangroups/client.py">update_plan_group</a>(...) -> AsyncHttpResponse[UpdatePlanGroupResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import OrderedPlansInGroup, PlanGroupBundleOrder, Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.plangroups.update_plan_group(
    plan_group_id="plan_group_id",
    add_on_ids=["add_on_ids"],
    checkout_collect_address=True,
    checkout_collect_email=True,
    checkout_collect_phone=True,
    enable_tax_collection=True,
    ordered_add_ons=[
        OrderedPlansInGroup(
            plan_id="plan_id",
        )
    ],
    ordered_bundle_list=[
        PlanGroupBundleOrder(
            bundle_id="bundleId",
        )
    ],
    ordered_plans=[
        OrderedPlansInGroup(
            plan_id="plan_id",
        )
    ],
    prevent_downgrades_when_over_limit=True,
    prevent_self_service_downgrade=True,
    proration_behavior="create_prorations",
    show_as_monthly_prices=True,
    show_credits=True,
    show_period_toggle=True,
    show_zero_price_as_free=True,
    sync_customer_billing_details=True,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**plan_group_id:** `str` — plan_group_id
    
</dd>
</dl>

<dl>
<dd>

**add_on_ids:** `typing.Sequence[str]` — Use OrderedAddOns instead
    
</dd>
</dl>

<dl>
<dd>

**checkout_collect_address:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**checkout_collect_email:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**checkout_collect_phone:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**enable_tax_collection:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**ordered_add_ons:** `typing.Sequence[OrderedPlansInGroup]` 
    
</dd>
</dl>

<dl>
<dd>

**ordered_bundle_list:** `typing.Sequence[PlanGroupBundleOrder]` 
    
</dd>
</dl>

<dl>
<dd>

**ordered_plans:** `typing.Sequence[OrderedPlansInGroup]` 
    
</dd>
</dl>

<dl>
<dd>

**prevent_downgrades_when_over_limit:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**prevent_self_service_downgrade:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**proration_behavior:** `ProrationBehavior` 
    
</dd>
</dl>

<dl>
<dd>

**show_as_monthly_prices:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**show_credits:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**show_period_toggle:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**show_zero_price_as_free:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**sync_customer_billing_details:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**add_on_compatibilities:** `typing.Optional[typing.Sequence[CompatiblePlans]]` 
    
</dd>
</dl>

<dl>
<dd>

**custom_plan_config:** `typing.Optional[CustomPlanConfig]` 
    
</dd>
</dl>

<dl>
<dd>

**custom_plan_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**fallback_plan_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**initial_plan_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**initial_plan_price_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**prevent_self_service_downgrade_button_text:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**prevent_self_service_downgrade_url:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**trial_days:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**trial_expiry_plan_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**trial_expiry_plan_price_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**trial_payment_method_required:** `typing.Optional[bool]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## accesstokens
<details><summary><code>client.accesstokens.<a href="src/schematic/accesstokens/client.py">issue_temporary_access_token</a>(...) -> AsyncHttpResponse[IssueTemporaryAccessTokenResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.accesstokens.issue_temporary_access_token(
    lookup={"key": "value"},
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**lookup:** `typing.Dict[str, str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## webhooks
<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">list_webhook_events</a>(...) -> AsyncHttpResponse[ListWebhookEventsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.webhooks.list_webhook_events(
    q="q",
    webhook_id="webhook_id",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**webhook_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">get_webhook_event</a>(...) -> AsyncHttpResponse[GetWebhookEventResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.webhooks.get_webhook_event(
    webhook_event_id="webhook_event_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**webhook_event_id:** `str` — webhook_event_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">count_webhook_events</a>(...) -> AsyncHttpResponse[CountWebhookEventsResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.webhooks.count_webhook_events(
    q="q",
    webhook_id="webhook_id",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**webhook_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">list_webhooks</a>(...) -> AsyncHttpResponse[ListWebhooksResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.webhooks.list_webhooks(
    q="q",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">create_webhook</a>(...) -> AsyncHttpResponse[CreateWebhookResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.webhooks.create_webhook(
    name="name",
    request_types=["subscription.trial.ended"],
    url="url",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_types:** `typing.Sequence[WebhookRequestType]` 
    
</dd>
</dl>

<dl>
<dd>

**url:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**credit_trigger_configs:** `typing.Optional[typing.Sequence[CreditTriggerConfig]]` 
    
</dd>
</dl>

<dl>
<dd>

**entitlement_trigger_configs:** `typing.Optional[typing.Sequence[EntitlementTriggerConfig]]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">get_webhook</a>(...) -> AsyncHttpResponse[GetWebhookResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.webhooks.get_webhook(
    webhook_id="webhook_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**webhook_id:** `str` — webhook_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">update_webhook</a>(...) -> AsyncHttpResponse[UpdateWebhookResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.webhooks.update_webhook(
    webhook_id="webhook_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**webhook_id:** `str` — webhook_id
    
</dd>
</dl>

<dl>
<dd>

**credit_trigger_configs:** `typing.Optional[typing.Sequence[CreditTriggerConfig]]` 
    
</dd>
</dl>

<dl>
<dd>

**entitlement_trigger_configs:** `typing.Optional[typing.Sequence[EntitlementTriggerConfig]]` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_types:** `typing.Optional[typing.Sequence[WebhookRequestType]]` 
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[WebhookStatus]` 
    
</dd>
</dl>

<dl>
<dd>

**url:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">delete_webhook</a>(...) -> AsyncHttpResponse[DeleteWebhookResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.webhooks.delete_webhook(
    webhook_id="webhook_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**webhook_id:** `str` — webhook_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">count_webhooks</a>(...) -> AsyncHttpResponse[CountWebhooksResponse]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.webhooks.count_webhooks(
    q="q",
    limit=1,
    offset=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Page limit (default 100)
    
</dd>
</dl>

<dl>
<dd>

**offset:** `typing.Optional[int]` — Page offset (default 0)
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

