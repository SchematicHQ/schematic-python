# Reference
## accounts
<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">list_account_members</a>(...) -> ListAccountMembersResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.accounts.list_account_members(
    ids=[
        "ids"
    ],
    q="q",
    limit=1000000,
    offset=1000000,
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

**q:** `typing.Optional[str]` — Search filter
    
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">get_account_member</a>(...) -> GetAccountMemberResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.accounts.get_account_member(
    account_member_id="account_member_id",
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

**account_member_id:** `str` — account_member_id
    
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">list_api_keys</a>(...) -> ListApiKeysResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.accounts.list_api_keys(
    environment_id="environment_id",
    require_environment=True,
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">create_api_key</a>(...) -> CreateApiKeyResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**readonly:** `typing.Optional[bool]` 
    
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">get_api_key</a>(...) -> GetApiKeyResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">update_api_key</a>(...) -> UpdateApiKeyResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">delete_api_key</a>(...) -> DeleteApiKeyResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">count_api_keys</a>(...) -> CountApiKeysResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.accounts.count_api_keys(
    environment_id="environment_id",
    require_environment=True,
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">list_audit_logs</a>(...) -> ListAuditLogsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment
import datetime

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.accounts.list_audit_logs(
    actor_type="api_key",
    end_time=datetime.datetime.fromisoformat("2024-01-15T09:30:00+00:00"),
    environment_id="environment_id",
    q="q",
    start_time=datetime.datetime.fromisoformat("2024-01-15T09:30:00+00:00"),
    limit=1000000,
    offset=1000000,
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

**actor_type:** `typing.Optional[ActorType]` 
    
</dd>
</dl>

<dl>
<dd>

**end_time:** `typing.Optional[datetime.datetime]` 
    
</dd>
</dl>

<dl>
<dd>

**environment_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**start_time:** `typing.Optional[datetime.datetime]` 
    
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">get_audit_log</a>(...) -> GetAuditLogResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.accounts.get_audit_log(
    audit_log_id="audit_log_id",
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

**audit_log_id:** `str` — audit_log_id
    
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">count_audit_logs</a>(...) -> CountAuditLogsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment
import datetime

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.accounts.count_audit_logs(
    actor_type="api_key",
    end_time=datetime.datetime.fromisoformat("2024-01-15T09:30:00+00:00"),
    environment_id="environment_id",
    q="q",
    start_time=datetime.datetime.fromisoformat("2024-01-15T09:30:00+00:00"),
    limit=1000000,
    offset=1000000,
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

**actor_type:** `typing.Optional[ActorType]` 
    
</dd>
</dl>

<dl>
<dd>

**end_time:** `typing.Optional[datetime.datetime]` 
    
</dd>
</dl>

<dl>
<dd>

**environment_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**start_time:** `typing.Optional[datetime.datetime]` 
    
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">list_environments</a>(...) -> ListEnvironmentsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.accounts.list_environments(
    ids=[
        "ids"
    ],
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">create_environment</a>(...) -> CreateEnvironmentResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">get_environment</a>(...) -> GetEnvironmentResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">update_environment</a>(...) -> UpdateEnvironmentResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">delete_environment</a>(...) -> DeleteEnvironmentResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">quickstart</a>() -> QuickstartResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">get_who_am_i</a>() -> GetWhoAmIResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.accounts.get_who_am_i()

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
<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">list_coupons</a>(...) -> ListCouponsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.billing.list_coupons(
    is_active=True,
    q="q",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_billing_coupon</a>(...) -> UpsertBillingCouponResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.billing.upsert_billing_coupon(
    amount_off=1000000,
    duration="duration",
    duration_in_months=1000000,
    external_id="external_id",
    max_redemptions=1000000,
    name="name",
    percent_off=1.1,
    times_redeemed=1000000,
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_billing_customer</a>(...) -> UpsertBillingCustomerResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.billing.upsert_billing_customer(
    email="email",
    external_id="external_id",
    meta={
        "key": "value"
    },
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">list_customers_with_subscriptions</a>(...) -> ListCustomersWithSubscriptionsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.billing.list_customers_with_subscriptions(
    company_ids=[
        "company_ids"
    ],
    name="name",
    provider_type="orb",
    q="q",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">count_customers</a>(...) -> CountCustomersResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.billing.count_customers(
    company_ids=[
        "company_ids"
    ],
    name="name",
    provider_type="orb",
    q="q",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">list_invoices</a>(...) -> ListInvoicesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.billing.list_invoices(
    company_id="company_id",
    customer_external_id="customer_external_id",
    subscription_external_id="subscription_external_id",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_invoice</a>(...) -> UpsertInvoiceResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.billing.upsert_invoice(
    amount_due=1000000,
    amount_paid=1000000,
    amount_remaining=1000000,
    collection_method="collection_method",
    currency="currency",
    customer_external_id="customer_external_id",
    subtotal=1000000,
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

**due_date:** `typing.Optional[datetime.datetime]` 
    
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

**status:** `typing.Optional[InvoiceStatus]` 
    
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">list_meters</a>(...) -> ListMetersResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.billing.list_meters(
    display_name="display_name",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_billing_meter</a>(...) -> UpsertBillingMeterResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">list_payment_methods</a>(...) -> ListPaymentMethodsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.billing.list_payment_methods(
    company_id="company_id",
    customer_external_id="customer_external_id",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_payment_method</a>(...) -> UpsertPaymentMethodResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">list_billing_prices</a>(...) -> ListBillingPricesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.billing.list_billing_prices(
    currency="currency",
    for_initial_plan=True,
    for_trial_expiry_plan=True,
    ids=[
        "ids"
    ],
    interval="interval",
    is_active=True,
    price=1000000,
    product_id="product_id",
    product_ids=[
        "product_ids"
    ],
    provider_type="orb",
    q="q",
    tiers_mode="graduated",
    usage_type="licensed",
    with_meter=True,
    limit=1000000,
    offset=1000000,
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

**currency:** `typing.Optional[str]` — Filter for prices in a specific currency (e.g. usd, eur)
    
</dd>
</dl>

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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_billing_price</a>(...) -> UpsertBillingPriceResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic, CreateBillingPriceTierRequestBody
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.billing.upsert_billing_price(
    billing_scheme="per_unit",
    currency="currency",
    external_account_id="external_account_id",
    interval="interval",
    is_active=True,
    price=1000000,
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

**price_tiers:** `typing.List[CreateBillingPriceTierRequestBody]` 
    
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

**nickname:** `typing.Optional[str]` 
    
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">delete_billing_product</a>(...) -> DeleteBillingProductResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">list_billing_product_prices</a>(...) -> ListBillingProductPricesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.billing.list_billing_product_prices(
    currency="currency",
    for_initial_plan=True,
    for_trial_expiry_plan=True,
    ids=[
        "ids"
    ],
    interval="interval",
    is_active=True,
    price=1000000,
    product_id="product_id",
    product_ids=[
        "product_ids"
    ],
    provider_type="orb",
    q="q",
    tiers_mode="graduated",
    usage_type="licensed",
    with_meter=True,
    limit=1000000,
    offset=1000000,
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

**currency:** `typing.Optional[str]` — Filter for prices in a specific currency (e.g. usd, eur)
    
</dd>
</dl>

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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">delete_product_price</a>(...) -> DeleteProductPriceResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_billing_product</a>(...) -> UpsertBillingProductResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.billing.upsert_billing_product(
    external_id="external_id",
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

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">list_billing_products</a>(...) -> ListBillingProductsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.billing.list_billing_products(
    ids=[
        "ids"
    ],
    is_active=True,
    name="name",
    price_usage_type="licensed",
    provider_type="orb",
    q="q",
    with_one_time_charges=True,
    with_prices_only=True,
    with_zero_price=True,
    without_linked_to_plan=True,
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">count_billing_products</a>(...) -> CountBillingProductsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.billing.count_billing_products(
    ids=[
        "ids"
    ],
    is_active=True,
    name="name",
    price_usage_type="licensed",
    provider_type="orb",
    q="q",
    with_one_time_charges=True,
    with_prices_only=True,
    with_zero_price=True,
    without_linked_to_plan=True,
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_billing_subscription</a>(...) -> UpsertBillingSubscriptionResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic, BillingSubscriptionDiscount, BillingProductPricing
from schematic.environment import SchematicEnvironment
import datetime

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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
            started_at=datetime.datetime.fromisoformat("2024-01-15T09:30:00+00:00"),
        )
    ],
    expired_at=datetime.datetime.fromisoformat("2024-01-15T09:30:00+00:00"),
    product_external_ids=[
        BillingProductPricing(
            currency="currency",
            interval="interval",
            price=1000000,
            price_external_id="price_external_id",
            product_external_id="product_external_id",
            quantity=1000000,
            usage_type="licensed",
        )
    ],
    subscription_external_id="subscription_external_id",
    total_price=1000000,
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

**discounts:** `typing.List[BillingSubscriptionDiscount]` 
    
</dd>
</dl>

<dl>
<dd>

**expired_at:** `datetime.datetime` 
    
</dd>
</dl>

<dl>
<dd>

**product_external_ids:** `typing.List[BillingProductPricing]` 
    
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

**provider_type:** `typing.Optional[BillingProviderType]` 
    
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
<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">list_billing_credits</a>(...) -> ListBillingCreditsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.credits.list_billing_credits(
    ids=[
        "ids"
    ],
    name="name",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">create_billing_credit</a>(...) -> CreateBillingCreditResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**currency_prices:** `typing.Optional[typing.List[CreditCurrencyPriceRequestBody]]` 
    
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">get_single_billing_credit</a>(...) -> GetSingleBillingCreditResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">update_billing_credit</a>(...) -> UpdateBillingCreditResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**currency_prices:** `typing.Optional[typing.List[CreditCurrencyPriceRequestBody]]` 
    
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">soft_delete_billing_credit</a>(...) -> SoftDeleteBillingCreditResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">list_company_credit_balances</a>(...) -> ListCompanyCreditBalancesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.credits.list_company_credit_balances(
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

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">list_credit_bundles</a>(...) -> ListCreditBundlesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.credits.list_credit_bundles(
    ids=[
        "ids"
    ],
    credit_id="credit_id",
    status="active",
    bundle_type="fixed",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">create_credit_bundle</a>(...) -> CreateCreditBundleResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.credits.create_credit_bundle(
    bundle_name="bundle_name",
    credit_id="credit_id",
    currency="currency",
    price_per_unit=1000000,
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

**currency_prices:** `typing.Optional[typing.List[CreditBundleCurrencyPriceRequestBody]]` 
    
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">get_credit_bundle</a>(...) -> GetCreditBundleResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">update_credit_bundle_details</a>(...) -> UpdateCreditBundleDetailsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.credits.update_credit_bundle_details(
    bundle_id="bundle_id",
    bundle_name="bundle_name",
    price_per_unit=1000000,
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

**currency_prices:** `typing.Optional[typing.List[CreditBundleCurrencyPriceRequestBody]]` 
    
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">delete_credit_bundle</a>(...) -> DeleteCreditBundleResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">count_credit_bundles</a>(...) -> CountCreditBundlesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.credits.count_credit_bundles(
    ids=[
        "ids"
    ],
    credit_id="credit_id",
    status="active",
    bundle_type="fixed",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">count_billing_credits</a>(...) -> CountBillingCreditsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.credits.count_billing_credits(
    ids=[
        "ids"
    ],
    name="name",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">zero_out_grant</a>(...) -> ZeroOutGrantResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">grant_billing_credits_to_company</a>(...) -> GrantBillingCreditsToCompanyResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.credits.grant_billing_credits_to_company(
    company_id="company_id",
    credit_id="credit_id",
    quantity=1000000,
    reason="adjustment",
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

**currency:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**expires_at:** `typing.Optional[datetime.datetime]` 
    
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">count_company_grants</a>(...) -> CountCompanyGrantsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.credits.count_company_grants(
    company_id="company_id",
    order="created_at",
    dir="asc",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">list_company_grants</a>(...) -> ListCompanyGrantsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.credits.list_company_grants(
    company_id="company_id",
    order="created_at",
    dir="asc",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">count_billing_credits_grants</a>(...) -> CountBillingCreditsGrantsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.credits.count_billing_credits_grants(
    credit_id="credit_id",
    ids=[
        "ids"
    ],
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">list_grants_for_credit</a>(...) -> ListGrantsForCreditResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.credits.list_grants_for_credit(
    credit_id="credit_id",
    ids=[
        "ids"
    ],
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">get_enriched_credit_ledger</a>(...) -> GetEnrichedCreditLedgerResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.credits.get_enriched_credit_ledger(
    company_id="company_id",
    billing_credit_id="billing_credit_id",
    feature_id="feature_id",
    period="daily",
    start_time="start_time",
    end_time="end_time",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">count_credit_ledger</a>(...) -> CountCreditLedgerResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.credits.count_credit_ledger(
    company_id="company_id",
    billing_credit_id="billing_credit_id",
    feature_id="feature_id",
    period="daily",
    start_time="start_time",
    end_time="end_time",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">list_billing_plan_credit_grants</a>(...) -> ListBillingPlanCreditGrantsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.credits.list_billing_plan_credit_grants(
    credit_id="credit_id",
    ids=[
        "ids"
    ],
    plan_id="plan_id",
    plan_ids=[
        "plan_ids"
    ],
    plan_version_id="plan_version_id",
    limit=1000000,
    offset=1000000,
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

**plan_version_id:** `typing.Optional[str]` 
    
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">create_billing_plan_credit_grant</a>(...) -> CreateBillingPlanCreditGrantResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.credits.create_billing_plan_credit_grant(
    credit_amount=1000000,
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

**request:** `CreateBillingPlanCreditGrantRequestBody` 
    
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">get_single_billing_plan_credit_grant</a>(...) -> GetSingleBillingPlanCreditGrantResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.credits.get_single_billing_plan_credit_grant(
    plan_grant_id="plan_grant_id",
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

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">update_billing_plan_credit_grant</a>(...) -> UpdateBillingPlanCreditGrantResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**request:** `UpdateBillingPlanCreditGrantRequestBody` 
    
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">delete_billing_plan_credit_grant</a>(...) -> DeleteBillingPlanCreditGrantResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">count_billing_plan_credit_grants</a>(...) -> CountBillingPlanCreditGrantsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.credits.count_billing_plan_credit_grants(
    credit_id="credit_id",
    ids=[
        "ids"
    ],
    plan_id="plan_id",
    plan_ids=[
        "plan_ids"
    ],
    plan_version_id="plan_version_id",
    limit=1000000,
    offset=1000000,
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

**plan_version_id:** `typing.Optional[str]` 
    
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">list_credit_event_ledger</a>(...) -> ListCreditEventLedgerResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.credits.list_credit_event_ledger(
    billing_credit_id="billing_credit_id",
    company_id="company_id",
    end_time="end_time",
    event_type="grant",
    feature_id="feature_id",
    start_time="start_time",
    limit=1000000,
    offset=1000000,
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

**billing_credit_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**end_time:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**event_type:** `typing.Optional[CreditEventType]` 
    
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

<details><summary><code>client.credits.<a href="src/schematic/credits/client.py">count_credit_event_ledger</a>(...) -> CountCreditEventLedgerResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.credits.count_credit_event_ledger(
    billing_credit_id="billing_credit_id",
    company_id="company_id",
    end_time="end_time",
    event_type="grant",
    feature_id="feature_id",
    start_time="start_time",
    limit=1000000,
    offset=1000000,
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

**billing_credit_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**end_time:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**event_type:** `typing.Optional[CreditEventType]` 
    
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
<details><summary><code>client.checkout.<a href="src/schematic/checkout/client.py">internal</a>(...) -> CheckoutInternalResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic, UpdateAddOnRequestBody, UpdateCreditBundleRequestBody, UpdatePayInAdvanceRequestBody
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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
            quantity=1000000,
        )
    ],
    new_plan_id="new_plan_id",
    new_price_id="new_price_id",
    pay_in_advance=[
        UpdatePayInAdvanceRequestBody(
            price_id="price_id",
            quantity=1000000,
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

**request:** `ChangeSubscriptionInternalRequestBody` 
    
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

<details><summary><code>client.checkout.<a href="src/schematic/checkout/client.py">get_checkout_data</a>(...) -> GetCheckoutDataResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.checkout.<a href="src/schematic/checkout/client.py">preview_checkout_internal</a>(...) -> PreviewCheckoutInternalResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic, UpdateAddOnRequestBody, UpdateCreditBundleRequestBody, UpdatePayInAdvanceRequestBody
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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
            quantity=1000000,
        )
    ],
    new_plan_id="new_plan_id",
    new_price_id="new_price_id",
    pay_in_advance=[
        UpdatePayInAdvanceRequestBody(
            price_id="price_id",
            quantity=1000000,
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

**request:** `ChangeSubscriptionInternalRequestBody` 
    
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

<details><summary><code>client.checkout.<a href="src/schematic/checkout/client.py">manage_plan</a>(...) -> ManagePlanResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic, PlanSelection, UpdateCreditBundleRequestBody, UpdatePayInAdvanceRequestBody
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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
            quantity=1000000,
        )
    ],
    pay_in_advance_entitlements=[
        UpdatePayInAdvanceRequestBody(
            price_id="price_id",
            quantity=1000000,
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

**request:** `ManagePlanRequest` 
    
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

<details><summary><code>client.checkout.<a href="src/schematic/checkout/client.py">preview_manage_plan</a>(...) -> PreviewManagePlanResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic, PlanSelection, UpdateCreditBundleRequestBody, UpdatePayInAdvanceRequestBody
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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
            quantity=1000000,
        )
    ],
    pay_in_advance_entitlements=[
        UpdatePayInAdvanceRequestBody(
            price_id="price_id",
            quantity=1000000,
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

**request:** `ManagePlanRequest` 
    
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

<details><summary><code>client.checkout.<a href="src/schematic/checkout/client.py">cancel_subscription</a>(...) -> CancelSubscriptionResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.checkout.<a href="src/schematic/checkout/client.py">update_customer_subscription_trial_end</a>(...) -> UpdateCustomerSubscriptionTrialEndResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**trial_end:** `typing.Optional[datetime.datetime]` 
    
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
<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">list_companies</a>(...) -> ListCompaniesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.list_companies(
    credit_type_ids=[
        "credit_type_ids"
    ],
    has_scheduled_downgrade=True,
    ids=[
        "ids"
    ],
    monetized_subscriptions=True,
    plan_id="plan_id",
    plan_ids=[
        "plan_ids"
    ],
    plan_version_id="plan_version_id",
    q="q",
    sort_order_column="sort_order_column",
    sort_order_direction="asc",
    subscription_statuses=[
        "active"
    ],
    subscription_types=[
        "free"
    ],
    with_entitlement_for="with_entitlement_for",
    without_feature_override_for="without_feature_override_for",
    without_plan=True,
    without_subscription=True,
    with_subscription=True,
    limit=1000000,
    offset=1000000,
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

**credit_type_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter companies by one or more credit type IDs (each ID starts with bcrd_)
    
</dd>
</dl>

<dl>
<dd>

**has_scheduled_downgrade:** `typing.Optional[bool]` — Filter companies that have a pending scheduled downgrade
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter companies by multiple company IDs (starts with comp_)
    
</dd>
</dl>

<dl>
<dd>

**monetized_subscriptions:** `typing.Optional[bool]` — Filter companies that have monetized subscriptions
    
</dd>
</dl>

<dl>
<dd>

**plan_id:** `typing.Optional[str]` — Filter companies by plan ID (starts with plan_)
    
</dd>
</dl>

<dl>
<dd>

**plan_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter companies by one or more plan IDs (each ID starts with plan_)
    
</dd>
</dl>

<dl>
<dd>

**plan_version_id:** `typing.Optional[str]` — Filter companies by plan version ID (starts with plvr_)
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` — Search for companies by name, keys or string traits
    
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

**subscription_statuses:** `typing.Optional[typing.Union[SubscriptionStatus, typing.Sequence[SubscriptionStatus]]]` — Filter companies by one or more subscription statuses
    
</dd>
</dl>

<dl>
<dd>

**subscription_types:** `typing.Optional[typing.Union[SubscriptionType, typing.Sequence[SubscriptionType]]]` — Filter companies by one or more subscription types
    
</dd>
</dl>

<dl>
<dd>

**with_entitlement_for:** `typing.Optional[str]` — Filter companies that have an entitlement (plan entitlement or company override) for the specified feature ID
    
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

**without_subscription:** `typing.Optional[bool]` — Filter out companies that have a subscription
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">upsert_company</a>(...) -> UpsertCompanyResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.upsert_company(
    keys={
        "key": "value"
    },
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

**request:** `UpsertCompanyRequestBody` 
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_company</a>(...) -> GetCompanyResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">delete_company</a>(...) -> DeleteCompanyResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">count_companies</a>(...) -> CountCompaniesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.count_companies(
    credit_type_ids=[
        "credit_type_ids"
    ],
    has_scheduled_downgrade=True,
    ids=[
        "ids"
    ],
    monetized_subscriptions=True,
    plan_id="plan_id",
    plan_ids=[
        "plan_ids"
    ],
    plan_version_id="plan_version_id",
    q="q",
    sort_order_column="sort_order_column",
    sort_order_direction="asc",
    subscription_statuses=[
        "active"
    ],
    subscription_types=[
        "free"
    ],
    with_entitlement_for="with_entitlement_for",
    without_feature_override_for="without_feature_override_for",
    without_plan=True,
    without_subscription=True,
    with_subscription=True,
    limit=1000000,
    offset=1000000,
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

**credit_type_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter companies by one or more credit type IDs (each ID starts with bcrd_)
    
</dd>
</dl>

<dl>
<dd>

**has_scheduled_downgrade:** `typing.Optional[bool]` — Filter companies that have a pending scheduled downgrade
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter companies by multiple company IDs (starts with comp_)
    
</dd>
</dl>

<dl>
<dd>

**monetized_subscriptions:** `typing.Optional[bool]` — Filter companies that have monetized subscriptions
    
</dd>
</dl>

<dl>
<dd>

**plan_id:** `typing.Optional[str]` — Filter companies by plan ID (starts with plan_)
    
</dd>
</dl>

<dl>
<dd>

**plan_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter companies by one or more plan IDs (each ID starts with plan_)
    
</dd>
</dl>

<dl>
<dd>

**plan_version_id:** `typing.Optional[str]` — Filter companies by plan version ID (starts with plvr_)
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` — Search for companies by name, keys or string traits
    
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

**subscription_statuses:** `typing.Optional[typing.Union[SubscriptionStatus, typing.Sequence[SubscriptionStatus]]]` — Filter companies by one or more subscription statuses
    
</dd>
</dl>

<dl>
<dd>

**subscription_types:** `typing.Optional[typing.Union[SubscriptionType, typing.Sequence[SubscriptionType]]]` — Filter companies by one or more subscription types
    
</dd>
</dl>

<dl>
<dd>

**with_entitlement_for:** `typing.Optional[str]` — Filter companies that have an entitlement (plan entitlement or company override) for the specified feature ID
    
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

**without_subscription:** `typing.Optional[bool]` — Filter out companies that have a subscription
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">create_company</a>(...) -> CreateCompanyResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.create_company(
    keys={
        "key": "value"
    },
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

**request:** `UpsertCompanyRequestBody` 
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">delete_company_by_keys</a>(...) -> DeleteCompanyByKeysResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.delete_company_by_keys(
    keys={
        "key": "value"
    },
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

**request:** `KeysRequestBody` 
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">lookup_company</a>(...) -> LookupCompanyResponse</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Company lookup is determined to resolve a company from its keys, similar to how many of our other apis work. 
The following approaches will all work to resolve a company and any of them are appropriate:
1. `/companies/lookup?keys={"foo": "bar", "fizz": "buzz"}`
2. `/companies/lookup?keys[foo]=bar&keys[fizz]=buzz`
2. `/companies/lookup?foo=bar&fizz=buzz`
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.lookup_company(
    keys={
        "keys": "keys"
    },
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">list_company_memberships</a>(...) -> ListCompanyMembershipsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.list_company_memberships(
    company_id="company_id",
    user_id="user_id",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_or_create_company_membership</a>(...) -> GetOrCreateCompanyMembershipResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">delete_company_membership</a>(...) -> DeleteCompanyMembershipResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_active_company_subscription</a>(...) -> GetActiveCompanySubscriptionResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.get_active_company_subscription(
    company_id="company_id",
    company_ids=[
        "company_ids"
    ],
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">upsert_company_trait</a>(...) -> UpsertCompanyTraitResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.upsert_company_trait(
    keys={
        "key": "value"
    },
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

**request:** `UpsertTraitRequestBody` 
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">list_entity_key_definitions</a>(...) -> ListEntityKeyDefinitionsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.list_entity_key_definitions(
    entity_type="company",
    ids=[
        "ids"
    ],
    q="q",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">count_entity_key_definitions</a>(...) -> CountEntityKeyDefinitionsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.count_entity_key_definitions(
    entity_type="company",
    ids=[
        "ids"
    ],
    q="q",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">list_entity_trait_definitions</a>(...) -> ListEntityTraitDefinitionsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.list_entity_trait_definitions(
    entity_type="company",
    ids=[
        "ids"
    ],
    q="q",
    trait_type="boolean",
    trait_types=[
        "boolean"
    ],
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_or_create_entity_trait_definition</a>(...) -> GetOrCreateEntityTraitDefinitionResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.get_or_create_entity_trait_definition(
    entity_type="company",
    hierarchy=[
        "hierarchy"
    ],
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

**hierarchy:** `typing.List[str]` 
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_entity_trait_definition</a>(...) -> GetEntityTraitDefinitionResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">update_entity_trait_definition</a>(...) -> UpdateEntityTraitDefinitionResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">count_entity_trait_definitions</a>(...) -> CountEntityTraitDefinitionsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.count_entity_trait_definitions(
    entity_type="company",
    ids=[
        "ids"
    ],
    q="q",
    trait_type="boolean",
    trait_types=[
        "boolean"
    ],
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_entity_trait_values</a>(...) -> GetEntityTraitValuesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.get_entity_trait_values(
    definition_id="definition_id",
    q="q",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">list_plan_changes</a>(...) -> ListPlanChangesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.list_plan_changes(
    action="checkout",
    base_plan_action="fallback",
    company_id="company_id",
    company_ids=[
        "company_ids"
    ],
    plan_ids=[
        "plan_ids"
    ],
    limit=1000000,
    offset=1000000,
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

**action:** `typing.Optional[PlanChangeAction]` 
    
</dd>
</dl>

<dl>
<dd>

**base_plan_action:** `typing.Optional[PlanChangeBasePlanAction]` 
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_plan_change</a>(...) -> GetPlanChangeResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">list_plan_traits</a>(...) -> ListPlanTraitsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.list_plan_traits(
    ids=[
        "ids"
    ],
    plan_id="plan_id",
    trait_id="trait_id",
    trait_ids=[
        "trait_ids"
    ],
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_plan_trait</a>(...) -> GetPlanTraitResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">update_plan_traits_bulk</a>(...) -> UpdatePlanTraitsBulkResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic, UpdatePlanTraitTraitRequestBody
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**traits:** `typing.List[UpdatePlanTraitTraitRequestBody]` 
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">count_plan_traits</a>(...) -> CountPlanTraitsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.count_plan_traits(
    ids=[
        "ids"
    ],
    plan_id="plan_id",
    trait_id="trait_id",
    trait_ids=[
        "trait_ids"
    ],
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">upsert_user_trait</a>(...) -> UpsertUserTraitResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.upsert_user_trait(
    keys={
        "key": "value"
    },
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

**request:** `UpsertTraitRequestBody` 
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">list_users</a>(...) -> ListUsersResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.list_users(
    company_id="company_id",
    ids=[
        "ids"
    ],
    plan_id="plan_id",
    q="q",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">upsert_user</a>(...) -> UpsertUserResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.upsert_user(
    keys={
        "key": "value"
    },
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

**request:** `UpsertUserRequestBody` 
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_user</a>(...) -> GetUserResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">delete_user</a>(...) -> DeleteUserResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">count_users</a>(...) -> CountUsersResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.count_users(
    company_id="company_id",
    ids=[
        "ids"
    ],
    plan_id="plan_id",
    q="q",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">create_user</a>(...) -> CreateUserResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.create_user(
    keys={
        "key": "value"
    },
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

**request:** `UpsertUserRequestBody` 
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">delete_user_by_keys</a>(...) -> DeleteUserByKeysResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.delete_user_by_keys(
    keys={
        "key": "value"
    },
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

**request:** `KeysRequestBody` 
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">lookup_user</a>(...) -> LookupUserResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.companies.lookup_user(
    keys={
        "keys": "keys"
    },
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
<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">list_company_overrides</a>(...) -> ListCompanyOverridesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.entitlements.list_company_overrides(
    company_id="company_id",
    company_ids=[
        "company_ids"
    ],
    feature_id="feature_id",
    feature_ids=[
        "feature_ids"
    ],
    ids=[
        "ids"
    ],
    without_expired=True,
    q="q",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">create_company_override</a>(...) -> CreateCompanyOverrideResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**expiration_date:** `typing.Optional[datetime.datetime]` 
    
</dd>
</dl>

<dl>
<dd>

**metric_period:** `typing.Optional[MetricPeriod]` 
    
</dd>
</dl>

<dl>
<dd>

**metric_period_month_reset:** `typing.Optional[MetricPeriodMonthReset]` 
    
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">get_company_override</a>(...) -> GetCompanyOverrideResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">update_company_override</a>(...) -> UpdateCompanyOverrideResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**expiration_date:** `typing.Optional[datetime.datetime]` 
    
</dd>
</dl>

<dl>
<dd>

**metric_period:** `typing.Optional[MetricPeriod]` 
    
</dd>
</dl>

<dl>
<dd>

**metric_period_month_reset:** `typing.Optional[MetricPeriodMonthReset]` 
    
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">delete_company_override</a>(...) -> DeleteCompanyOverrideResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">count_company_overrides</a>(...) -> CountCompanyOverridesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.entitlements.count_company_overrides(
    company_id="company_id",
    company_ids=[
        "company_ids"
    ],
    feature_id="feature_id",
    feature_ids=[
        "feature_ids"
    ],
    ids=[
        "ids"
    ],
    without_expired=True,
    q="q",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">list_feature_companies</a>(...) -> ListFeatureCompaniesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.entitlements.list_feature_companies(
    feature_id="feature_id",
    q="q",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">count_feature_companies</a>(...) -> CountFeatureCompaniesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.entitlements.count_feature_companies(
    feature_id="feature_id",
    q="q",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">list_feature_usage</a>(...) -> ListFeatureUsageResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.entitlements.list_feature_usage(
    company_id="company_id",
    feature_ids=[
        "feature_ids"
    ],
    include_usage_aggregation=True,
    q="q",
    without_negative_entitlements=True,
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">get_feature_usage_time_series</a>(...) -> GetFeatureUsageTimeSeriesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment
import datetime

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.entitlements.get_feature_usage_time_series(
    company_id="company_id",
    end_time=datetime.datetime.fromisoformat("2024-01-15T09:30:00+00:00"),
    feature_id="feature_id",
    granularity="daily",
    start_time=datetime.datetime.fromisoformat("2024-01-15T09:30:00+00:00"),
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

**end_time:** `datetime.datetime` 
    
</dd>
</dl>

<dl>
<dd>

**feature_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**start_time:** `datetime.datetime` 
    
</dd>
</dl>

<dl>
<dd>

**granularity:** `typing.Optional[TimeSeriesGranularity]` 
    
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">count_feature_usage</a>(...) -> CountFeatureUsageResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.entitlements.count_feature_usage(
    company_id="company_id",
    feature_ids=[
        "feature_ids"
    ],
    include_usage_aggregation=True,
    q="q",
    without_negative_entitlements=True,
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">list_feature_users</a>(...) -> ListFeatureUsersResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.entitlements.list_feature_users(
    feature_id="feature_id",
    q="q",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">count_feature_users</a>(...) -> CountFeatureUsersResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.entitlements.count_feature_users(
    feature_id="feature_id",
    q="q",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">list_plan_entitlements</a>(...) -> ListPlanEntitlementsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.entitlements.list_plan_entitlements(
    feature_id="feature_id",
    feature_ids=[
        "feature_ids"
    ],
    ids=[
        "ids"
    ],
    plan_id="plan_id",
    plan_ids=[
        "plan_ids"
    ],
    plan_version_id="plan_version_id",
    plan_version_ids=[
        "plan_version_ids"
    ],
    q="q",
    with_metered_products=True,
    limit=1000000,
    offset=1000000,
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

**plan_version_id:** `typing.Optional[str]` — Filter plan entitlements by a single plan version ID (starting with plvr_)
    
</dd>
</dl>

<dl>
<dd>

**plan_version_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter plan entitlements by multiple plan version IDs (starting with plvr_)
    
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">create_plan_entitlement</a>(...) -> CreatePlanEntitlementResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**currency_prices:** `typing.Optional[typing.List[CurrencyPriceRequestBody]]` 
    
</dd>
</dl>

<dl>
<dd>

**metric_period:** `typing.Optional[MetricPeriod]` 
    
</dd>
</dl>

<dl>
<dd>

**metric_period_month_reset:** `typing.Optional[MetricPeriodMonthReset]` 
    
</dd>
</dl>

<dl>
<dd>

**monthly_metered_price_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**monthly_price_tiers:** `typing.Optional[typing.List[CreatePriceTierRequestBody]]` 
    
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

**plan_version_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**price_behavior:** `typing.Optional[EntitlementPriceBehavior]` 
    
</dd>
</dl>

<dl>
<dd>

**price_tiers:** `typing.Optional[typing.List[CreatePriceTierRequestBody]]` — Use MonthlyPriceTiers or YearlyPriceTiers instead
    
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

**yearly_price_tiers:** `typing.Optional[typing.List[CreatePriceTierRequestBody]]` 
    
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">get_plan_entitlement</a>(...) -> GetPlanEntitlementResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">update_plan_entitlement</a>(...) -> UpdatePlanEntitlementResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**currency_prices:** `typing.Optional[typing.List[CurrencyPriceRequestBody]]` 
    
</dd>
</dl>

<dl>
<dd>

**metric_period:** `typing.Optional[MetricPeriod]` 
    
</dd>
</dl>

<dl>
<dd>

**metric_period_month_reset:** `typing.Optional[MetricPeriodMonthReset]` 
    
</dd>
</dl>

<dl>
<dd>

**monthly_metered_price_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**monthly_price_tiers:** `typing.Optional[typing.List[CreatePriceTierRequestBody]]` 
    
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

**price_tiers:** `typing.Optional[typing.List[CreatePriceTierRequestBody]]` — Use MonthlyPriceTiers or YearlyPriceTiers instead
    
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

**yearly_price_tiers:** `typing.Optional[typing.List[CreatePriceTierRequestBody]]` 
    
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">delete_plan_entitlement</a>(...) -> DeletePlanEntitlementResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">upsert_plan_entitlement_for_billing_product</a>(...) -> UpsertPlanEntitlementForBillingProductResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.entitlements.upsert_plan_entitlement_for_billing_product(
    billing_provider="orb",
    external_resource_id="external_resource_id",
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

**billing_provider:** `BillingProviderType` 
    
</dd>
</dl>

<dl>
<dd>

**external_resource_id:** `str` 
    
</dd>
</dl>

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

**currency_prices:** `typing.Optional[typing.List[CurrencyPriceRequestBody]]` 
    
</dd>
</dl>

<dl>
<dd>

**metric_period:** `typing.Optional[MetricPeriod]` 
    
</dd>
</dl>

<dl>
<dd>

**metric_period_month_reset:** `typing.Optional[MetricPeriodMonthReset]` 
    
</dd>
</dl>

<dl>
<dd>

**monthly_metered_price_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**monthly_price_tiers:** `typing.Optional[typing.List[CreatePriceTierRequestBody]]` 
    
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

**plan_version_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**price_behavior:** `typing.Optional[EntitlementPriceBehavior]` 
    
</dd>
</dl>

<dl>
<dd>

**price_tiers:** `typing.Optional[typing.List[CreatePriceTierRequestBody]]` — Use MonthlyPriceTiers or YearlyPriceTiers instead
    
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

**yearly_price_tiers:** `typing.Optional[typing.List[CreatePriceTierRequestBody]]` 
    
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">count_plan_entitlements</a>(...) -> CountPlanEntitlementsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.entitlements.count_plan_entitlements(
    feature_id="feature_id",
    feature_ids=[
        "feature_ids"
    ],
    ids=[
        "ids"
    ],
    plan_id="plan_id",
    plan_ids=[
        "plan_ids"
    ],
    plan_version_id="plan_version_id",
    plan_version_ids=[
        "plan_version_ids"
    ],
    q="q",
    with_metered_products=True,
    limit=1000000,
    offset=1000000,
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

**plan_version_id:** `typing.Optional[str]` — Filter plan entitlements by a single plan version ID (starting with plvr_)
    
</dd>
</dl>

<dl>
<dd>

**plan_version_ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` — Filter plan entitlements by multiple plan version IDs (starting with plvr_)
    
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">duplicate_plan_entitlements</a>(...) -> DuplicatePlanEntitlementsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">get_feature_usage_by_company</a>(...) -> GetFeatureUsageByCompanyResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.entitlements.get_feature_usage_by_company(
    keys={
        "keys": "keys"
    },
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
<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">update_company_plans</a>(...) -> UpdateCompanyPlansResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.plans.update_company_plans(
    company_plan_id="company_plan_id",
    add_on_ids=[
        "add_on_ids"
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

**company_plan_id:** `str` — company_plan_id
    
</dd>
</dl>

<dl>
<dd>

**add_on_ids:** `typing.List[str]` 
    
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

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">list_custom_plan_billings</a>(...) -> ListCustomPlanBillingsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.plans.list_custom_plan_billings(
    company_id="company_id",
    plan_id="plan_id",
    status="active",
    statuses=[
        "active"
    ],
    limit=1000000,
    offset=1000000,
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

**company_id:** `typing.Optional[str]` — Filter by company ID
    
</dd>
</dl>

<dl>
<dd>

**plan_id:** `typing.Optional[str]` — Filter by plan ID
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[CustomPlanBillingStatus]` — Filter by billing status
    
</dd>
</dl>

<dl>
<dd>

**statuses:** `typing.Optional[typing.Union[CustomPlanBillingStatus, typing.Sequence[CustomPlanBillingStatus]]]` — Filter by multiple billing statuses
    
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

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">retry_custom_plan_billing</a>(...) -> RetryCustomPlanBillingResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic, UpdatePayInAdvanceRequestBody
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.plans.retry_custom_plan_billing(
    custom_plan_billing_id="custom_plan_billing_id",
    customer_email="customer_email",
    pay_in_advance=[
        UpdatePayInAdvanceRequestBody(
            price_id="price_id",
            quantity=1000000,
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

**custom_plan_billing_id:** `str` — custom_plan_billing_id
    
</dd>
</dl>

<dl>
<dd>

**customer_email:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**pay_in_advance:** `typing.List[UpdatePayInAdvanceRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**activation_strategy:** `typing.Optional[CustomPlanActivationStrategy]` 
    
</dd>
</dl>

<dl>
<dd>

**days_until_due:** `typing.Optional[int]` 
    
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

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">create_custom_plan</a>(...) -> CreateCustomPlanResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.plans.create_custom_plan(
    company_id="company_id",
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

**company_id:** `str` 
    
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

**copied_from_plan_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**icon:** `typing.Optional[PlanIcon]` 
    
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

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">list_plans</a>(...) -> ListPlansResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.plans.list_plans(
    company_id="company_id",
    exclude_company_scoped=True,
    for_fallback_plan=True,
    for_initial_plan=True,
    for_trial_expiry_plan=True,
    has_product_id=True,
    ids=[
        "ids"
    ],
    include_draft_versions=True,
    plan_type="plan",
    q="q",
    scoped_to_company_id="scoped_to_company_id",
    without_entitlement_for="without_entitlement_for",
    without_paid_product_id=True,
    limit=1000000,
    offset=1000000,
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

**exclude_company_scoped:** `typing.Optional[bool]` — Exclude plans that are scoped to a company (custom plans assigned to a company)
    
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

**include_draft_versions:** `typing.Optional[bool]` — Include billing settings from draft versions for plans which have draft version
    
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

**scoped_to_company_id:** `typing.Optional[str]` — Filter plans scoped to a specific company (custom plans)
    
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

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">create_plan</a>(...) -> CreatePlanResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**request:** `CreatePlanRequestBody` 
    
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

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">get_plan</a>(...) -> GetPlanResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.plans.get_plan(
    plan_id="plan_id",
    plan_version_id="plan_version_id",
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

**plan_version_id:** `typing.Optional[str]` — Fetch billing settings for a specific plan version
    
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

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">update_plan</a>(...) -> UpdatePlanResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**request:** `UpdatePlanRequestBody` 
    
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

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">delete_plan</a>(...) -> DeletePlanResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">upsert_billing_product_plan</a>(...) -> UpsertBillingProductPlanResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**request:** `UpsertBillingProductRequestBody` 
    
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

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">upsert_plan_for_billing_product</a>(...) -> UpsertPlanForBillingProductResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.plans.upsert_plan_for_billing_product(
    billing_provider="orb",
    description="description",
    external_resource_id="external_resource_id",
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

**billing_provider:** `BillingProviderType` 
    
</dd>
</dl>

<dl>
<dd>

**description:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**external_resource_id:** `str` 
    
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

**icon:** `typing.Optional[PlanIcon]` 
    
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

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">list_billing_product_match_companies</a>(...) -> ListBillingProductMatchCompaniesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.plans.list_billing_product_match_companies(
    plan_id="plan_id",
    q="q",
    limit=1000000,
    offset=1000000,
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

**plan_id:** `str` — The plan ID to find billing product match companies for
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` — Search for companies by name, keys or string traits
    
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

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">count_billing_product_match_companies</a>(...) -> CountBillingProductMatchCompaniesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.plans.count_billing_product_match_companies(
    plan_id="plan_id",
    q="q",
    limit=1000000,
    offset=1000000,
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

**plan_id:** `str` — The plan ID to find billing product match companies for
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` — Search for companies by name, keys or string traits
    
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

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">count_plans</a>(...) -> CountPlansResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.plans.count_plans(
    company_id="company_id",
    exclude_company_scoped=True,
    for_fallback_plan=True,
    for_initial_plan=True,
    for_trial_expiry_plan=True,
    has_product_id=True,
    ids=[
        "ids"
    ],
    include_draft_versions=True,
    plan_type="plan",
    q="q",
    scoped_to_company_id="scoped_to_company_id",
    without_entitlement_for="without_entitlement_for",
    without_paid_product_id=True,
    limit=1000000,
    offset=1000000,
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

**exclude_company_scoped:** `typing.Optional[bool]` — Exclude plans that are scoped to a company (custom plans assigned to a company)
    
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

**include_draft_versions:** `typing.Optional[bool]` — Include billing settings from draft versions for plans which have draft version
    
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

**scoped_to_company_id:** `typing.Optional[str]` — Filter plans scoped to a specific company (custom plans)
    
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

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">list_plan_issues</a>(...) -> ListPlanIssuesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.plans.list_plan_issues(
    plan_id="plan_id",
    plan_version_id="plan_version_id",
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

**plan_version_id:** `typing.Optional[str]` 
    
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

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">delete_plan_version</a>(...) -> DeletePlanVersionResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.plans.delete_plan_version(
    plan_id="plan_id",
    promote_archived_version=True,
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

**promote_archived_version:** `typing.Optional[bool]` 
    
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

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">publish_plan_version</a>(...) -> PublishPlanVersionResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic, UpdatePayInAdvanceRequestBody
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.plans.publish_plan_version(
    plan_id="plan_id",
    excluded_company_ids=[
        "excluded_company_ids"
    ],
    migration_strategy="immediate",
    pay_in_advance=[
        UpdatePayInAdvanceRequestBody(
            price_id="price_id",
            quantity=1000000,
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

**plan_id:** `str` — plan_id
    
</dd>
</dl>

<dl>
<dd>

**excluded_company_ids:** `typing.List[str]` 
    
</dd>
</dl>

<dl>
<dd>

**migration_strategy:** `PlanVersionMigrationStrategy` 
    
</dd>
</dl>

<dl>
<dd>

**pay_in_advance:** `typing.List[UpdatePayInAdvanceRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**activation_strategy:** `typing.Optional[CustomPlanActivationStrategy]` 
    
</dd>
</dl>

<dl>
<dd>

**customer_email:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**days_until_due:** `typing.Optional[int]` 
    
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
<details><summary><code>client.components.<a href="src/schematic/components/client.py">list_components</a>(...) -> ListComponentsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.components.list_components(
    q="q",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.components.<a href="src/schematic/components/client.py">create_component</a>(...) -> CreateComponentResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.components.<a href="src/schematic/components/client.py">get_component</a>(...) -> GetComponentResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.components.<a href="src/schematic/components/client.py">update_component</a>(...) -> UpdateComponentResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.components.<a href="src/schematic/components/client.py">delete_component</a>(...) -> DeleteComponentResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.components.<a href="src/schematic/components/client.py">count_components</a>(...) -> CountComponentsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.components.count_components(
    q="q",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.components.<a href="src/schematic/components/client.py">preview_component_data</a>(...) -> PreviewComponentDataResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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
<details><summary><code>client.dataexports.<a href="src/schematic/dataexports/client.py">create_data_export</a>(...) -> CreateDataExportResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**export_type:** `DataExportType` 
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**output_file_type:** `DataExportOutputFileType` 
    
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

<details><summary><code>client.dataexports.<a href="src/schematic/dataexports/client.py">get_data_export_artifact</a>(...) -> typing.Iterator[bytes]</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## events
<details><summary><code>client.events.<a href="src/schematic/events/client.py">create_event_batch</a>(...) -> CreateEventBatchResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic, CreateEventRequestBody
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**events:** `typing.List[CreateEventRequestBody]` 
    
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

<details><summary><code>client.events.<a href="src/schematic/events/client.py">get_event_summaries</a>(...) -> GetEventSummariesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.events.get_event_summaries(
    q="q",
    event_subtypes=[
        "event_subtypes"
    ],
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.events.<a href="src/schematic/events/client.py">list_events</a>(...) -> ListEventsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.events.list_events(
    company_id="company_id",
    event_subtype="event_subtype",
    event_types=[
        "flag_check"
    ],
    flag_id="flag_id",
    user_id="user_id",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.events.<a href="src/schematic/events/client.py">create_event</a>(...) -> CreateEventResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**request:** `CreateEventRequestBody` 
    
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

<details><summary><code>client.events.<a href="src/schematic/events/client.py">get_event</a>(...) -> GetEventResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.events.<a href="src/schematic/events/client.py">get_segment_integration_status</a>() -> GetSegmentIntegrationStatusResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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
<details><summary><code>client.features.<a href="src/schematic/features/client.py">list_features</a>(...) -> ListFeaturesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.features.list_features(
    boolean_require_event=True,
    feature_type=[
        "boolean"
    ],
    ids=[
        "ids"
    ],
    plan_version_id="plan_version_id",
    q="q",
    without_company_override_for="without_company_override_for",
    without_plan_entitlement_for="without_plan_entitlement_for",
    limit=1000000,
    offset=1000000,
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

**boolean_require_event:** `typing.Optional[bool]` — Only return boolean features if there is an associated event. Automatically includes boolean in the feature types filter.
    
</dd>
</dl>

<dl>
<dd>

**feature_type:** `typing.Optional[typing.Union[FeatureType, typing.Sequence[FeatureType]]]` — Filter by one or more feature types (boolean, event, trait)
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**plan_version_id:** `typing.Optional[str]` — Filter by plan version ID when used with without_plan_entitlement_for; if not provided, the latest published version is used
    
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">create_feature</a>(...) -> CreateFeatureResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**maintainer_account_member_id:** `typing.Optional[str]` 
    
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">get_feature</a>(...) -> GetFeatureResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">update_feature</a>(...) -> UpdateFeatureResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**maintainer_account_member_id:** `typing.Optional[str]` 
    
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">delete_feature</a>(...) -> DeleteFeatureResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">upsert_feature_for_billing_product</a>(...) -> UpsertFeatureForBillingProductResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.features.upsert_feature_for_billing_product(
    billing_provider="orb",
    description="description",
    external_resource_id="external_resource_id",
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

**billing_provider:** `BillingProviderType` 
    
</dd>
</dl>

<dl>
<dd>

**description:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**external_resource_id:** `str` 
    
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

**maintainer_account_member_id:** `typing.Optional[str]` 
    
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">count_features</a>(...) -> CountFeaturesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.features.count_features(
    boolean_require_event=True,
    feature_type=[
        "boolean"
    ],
    ids=[
        "ids"
    ],
    plan_version_id="plan_version_id",
    q="q",
    without_company_override_for="without_company_override_for",
    without_plan_entitlement_for="without_plan_entitlement_for",
    limit=1000000,
    offset=1000000,
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

**boolean_require_event:** `typing.Optional[bool]` — Only return boolean features if there is an associated event. Automatically includes boolean in the feature types filter.
    
</dd>
</dl>

<dl>
<dd>

**feature_type:** `typing.Optional[typing.Union[FeatureType, typing.Sequence[FeatureType]]]` — Filter by one or more feature types (boolean, event, trait)
    
</dd>
</dl>

<dl>
<dd>

**ids:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
</dd>
</dl>

<dl>
<dd>

**plan_version_id:** `typing.Optional[str]` — Filter by plan version ID when used with without_plan_entitlement_for; if not provided, the latest published version is used
    
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">list_flags</a>(...) -> ListFlagsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.features.list_flags(
    feature_id="feature_id",
    ids=[
        "ids"
    ],
    q="q",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">create_flag</a>(...) -> CreateFlagResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**request:** `CreateFlagRequestBody` 
    
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">get_flag</a>(...) -> GetFlagResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">update_flag</a>(...) -> UpdateFlagResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**request:** `CreateFlagRequestBody` 
    
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">delete_flag</a>(...) -> DeleteFlagResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">update_flag_rules</a>(...) -> UpdateFlagRulesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic, CreateOrUpdateRuleRequestBody, CreateOrUpdateConditionGroupRequestBody, CreateOrUpdateConditionRequestBody
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.features.update_flag_rules(
    flag_id="flag_id",
    rules=[
        CreateOrUpdateRuleRequestBody(
            condition_groups=[
                CreateOrUpdateConditionGroupRequestBody(
                    conditions=[
                        CreateOrUpdateConditionRequestBody(
                            condition_type="base_plan",
                            operator="eq",
                            resource_ids=[
                                "resource_ids"
                            ],
                        )
                    ],
                )
            ],
            conditions=[
                CreateOrUpdateConditionRequestBody(
                    condition_type="base_plan",
                    operator="eq",
                    resource_ids=[
                        "resource_ids"
                    ],
                )
            ],
            name="name",
            priority=1000000,
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

**rules:** `typing.List[CreateOrUpdateRuleRequestBody]` 
    
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">check_flag</a>(...) -> CheckFlagResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**request:** `CheckFlagRequestBody` 
    
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">check_flags</a>(...) -> CheckFlagsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**request:** `CheckFlagRequestBody` 
    
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">check_flags_bulk</a>(...) -> CheckFlagsBulkResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic, CheckFlagRequestBody
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.features.check_flags_bulk(
    contexts=[
        CheckFlagRequestBody()
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

**contexts:** `typing.List[CheckFlagRequestBody]` 
    
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">count_flags</a>(...) -> CountFlagsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.features.count_flags(
    feature_id="feature_id",
    ids=[
        "ids"
    ],
    q="q",
    limit=1000000,
    offset=1000000,
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

## insights
<details><summary><code>client.insights.<a href="src/schematic/insights/client.py">get_activity</a>(...) -> GetActivityResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.insights.get_activity(
    limit=1000000,
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

**limit:** `typing.Optional[int]` 
    
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

<details><summary><code>client.insights.<a href="src/schematic/insights/client.py">get_environment_feature_usage_time_series</a>(...) -> GetEnvironmentFeatureUsageTimeSeriesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment
import datetime

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.insights.get_environment_feature_usage_time_series(
    end_time=datetime.datetime.fromisoformat("2024-01-15T09:30:00+00:00"),
    feature_id="feature_id",
    granularity="daily",
    start_time=datetime.datetime.fromisoformat("2024-01-15T09:30:00+00:00"),
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

**end_time:** `datetime.datetime` 
    
</dd>
</dl>

<dl>
<dd>

**feature_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**start_time:** `datetime.datetime` 
    
</dd>
</dl>

<dl>
<dd>

**granularity:** `typing.Optional[TimeSeriesGranularity]` 
    
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

<details><summary><code>client.insights.<a href="src/schematic/insights/client.py">get_plan_growth</a>(...) -> GetPlanGrowthResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.insights.get_plan_growth(
    months=1000000,
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

**months:** `typing.Optional[int]` 
    
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

<details><summary><code>client.insights.<a href="src/schematic/insights/client.py">get_summary</a>() -> GetSummaryResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.insights.get_summary()

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

<details><summary><code>client.insights.<a href="src/schematic/insights/client.py">get_top_features_by_usage</a>(...) -> GetTopFeaturesByUsageResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment
import datetime

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.insights.get_top_features_by_usage(
    end_time=datetime.datetime.fromisoformat("2024-01-15T09:30:00+00:00"),
    limit=1000000,
    start_time=datetime.datetime.fromisoformat("2024-01-15T09:30:00+00:00"),
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

**end_time:** `datetime.datetime` 
    
</dd>
</dl>

<dl>
<dd>

**start_time:** `datetime.datetime` 
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` 
    
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

<details><summary><code>client.insights.<a href="src/schematic/insights/client.py">get_environment_trait_usage_time_series</a>(...) -> GetEnvironmentTraitUsageTimeSeriesResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment
import datetime

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.insights.get_environment_trait_usage_time_series(
    end_time=datetime.datetime.fromisoformat("2024-01-15T09:30:00+00:00"),
    feature_id="feature_id",
    granularity="daily",
    start_time=datetime.datetime.fromisoformat("2024-01-15T09:30:00+00:00"),
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

**end_time:** `datetime.datetime` 
    
</dd>
</dl>

<dl>
<dd>

**feature_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**start_time:** `datetime.datetime` 
    
</dd>
</dl>

<dl>
<dd>

**granularity:** `typing.Optional[TimeSeriesGranularity]` 
    
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

## integrationsapi
<details><summary><code>client.integrationsapi.<a href="src/schematic/integrationsapi/client.py">get_integration_webhook_url</a>(...) -> GetIntegrationWebhookUrlResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.integrationsapi.get_integration_webhook_url(
    type="type",
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

**type:** `str` — type
    
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

## planbundle
<details><summary><code>client.planbundle.<a href="src/schematic/planbundle/client.py">create_plan_bundle</a>(...) -> CreatePlanBundleResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic, PlanBundleEntitlementRequestBody
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.planbundle.create_plan_bundle(
    entitlements=[
        PlanBundleEntitlementRequestBody(
            action="create",
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

**entitlements:** `typing.List[PlanBundleEntitlementRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**billing_product:** `typing.Optional[UpsertBillingProductRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**credit_grants:** `typing.Optional[typing.List[PlanBundleCreditGrantRequestBody]]` 
    
</dd>
</dl>

<dl>
<dd>

**plan:** `typing.Optional[CreatePlanRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**traits:** `typing.Optional[typing.List[UpdatePlanTraitTraitRequestBody]]` 
    
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

<details><summary><code>client.planbundle.<a href="src/schematic/planbundle/client.py">update_plan_bundle</a>(...) -> UpdatePlanBundleResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic, PlanBundleEntitlementRequestBody
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.planbundle.update_plan_bundle(
    plan_bundle_id="plan_bundle_id",
    entitlements=[
        PlanBundleEntitlementRequestBody(
            action="create",
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

**plan_bundle_id:** `str` — plan_bundle_id
    
</dd>
</dl>

<dl>
<dd>

**entitlements:** `typing.List[PlanBundleEntitlementRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**billing_product:** `typing.Optional[UpsertBillingProductRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**credit_grants:** `typing.Optional[typing.List[PlanBundleCreditGrantRequestBody]]` 
    
</dd>
</dl>

<dl>
<dd>

**plan:** `typing.Optional[UpdatePlanRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**plan_version_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**traits:** `typing.Optional[typing.List[UpdatePlanTraitTraitRequestBody]]` 
    
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
<details><summary><code>client.plangroups.<a href="src/schematic/plangroups/client.py">get_plan_group</a>(...) -> GetPlanGroupResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.plangroups.get_plan_group(
    include_company_counts=True,
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

**include_company_counts:** `typing.Optional[bool]` 
    
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

<details><summary><code>client.plangroups.<a href="src/schematic/plangroups/client.py">create_plan_group</a>(...) -> CreatePlanGroupResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic, OrderedPlansInGroup, PlanGroupBundleOrder
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.plangroups.create_plan_group(
    add_on_ids=[
        "add_on_ids"
    ],
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
    show_feature_description=True,
    show_hard_limit=True,
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

**add_on_ids:** `typing.List[str]` — Use OrderedAddOns instead
    
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

**ordered_add_ons:** `typing.List[OrderedPlansInGroup]` 
    
</dd>
</dl>

<dl>
<dd>

**ordered_bundle_list:** `typing.List[PlanGroupBundleOrder]` 
    
</dd>
</dl>

<dl>
<dd>

**ordered_plans:** `typing.List[OrderedPlansInGroup]` 
    
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

**show_feature_description:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**show_hard_limit:** `bool` 
    
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

**add_on_compatibilities:** `typing.Optional[typing.List[CompatiblePlans]]` 
    
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

**scheduled_downgrade_behavior:** `typing.Optional[ScheduledDowngradeConfigBehavior]` 
    
</dd>
</dl>

<dl>
<dd>

**scheduled_downgrade_prevent_when_over_limit:** `typing.Optional[bool]` 
    
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

<details><summary><code>client.plangroups.<a href="src/schematic/plangroups/client.py">update_plan_group</a>(...) -> UpdatePlanGroupResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic, OrderedPlansInGroup, PlanGroupBundleOrder
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.plangroups.update_plan_group(
    plan_group_id="plan_group_id",
    add_on_ids=[
        "add_on_ids"
    ],
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
    show_feature_description=True,
    show_hard_limit=True,
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

**add_on_ids:** `typing.List[str]` — Use OrderedAddOns instead
    
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

**ordered_add_ons:** `typing.List[OrderedPlansInGroup]` 
    
</dd>
</dl>

<dl>
<dd>

**ordered_bundle_list:** `typing.List[PlanGroupBundleOrder]` 
    
</dd>
</dl>

<dl>
<dd>

**ordered_plans:** `typing.List[OrderedPlansInGroup]` 
    
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

**show_feature_description:** `bool` 
    
</dd>
</dl>

<dl>
<dd>

**show_hard_limit:** `bool` 
    
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

**add_on_compatibilities:** `typing.Optional[typing.List[CompatiblePlans]]` 
    
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

**scheduled_downgrade_behavior:** `typing.Optional[ScheduledDowngradeConfigBehavior]` 
    
</dd>
</dl>

<dl>
<dd>

**scheduled_downgrade_prevent_when_over_limit:** `typing.Optional[bool]` 
    
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

## planmigrations
<details><summary><code>client.planmigrations.<a href="src/schematic/planmigrations/client.py">list_company_migrations</a>(...) -> ListCompanyMigrationsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.planmigrations.list_company_migrations(
    migration_id="migration_id",
    q="q",
    status="completed",
    limit=1000000,
    offset=1000000,
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

**migration_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[PlanVersionCompanyMigrationStatus]` 
    
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

<details><summary><code>client.planmigrations.<a href="src/schematic/planmigrations/client.py">count_company_migrations</a>(...) -> CountCompanyMigrationsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.planmigrations.count_company_migrations(
    migration_id="migration_id",
    q="q",
    status="completed",
    limit=1000000,
    offset=1000000,
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

**migration_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[PlanVersionCompanyMigrationStatus]` 
    
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

<details><summary><code>client.planmigrations.<a href="src/schematic/planmigrations/client.py">list_migrations</a>(...) -> ListMigrationsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.planmigrations.list_migrations(
    plan_version_id="plan_version_id",
    status="completed",
    limit=1000000,
    offset=1000000,
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

**plan_version_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[PlanVersionMigrationStatus]` 
    
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

<details><summary><code>client.planmigrations.<a href="src/schematic/planmigrations/client.py">get_migration</a>(...) -> GetMigrationResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.planmigrations.get_migration(
    plan_version_migration_id="plan_version_migration_id",
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

**plan_version_migration_id:** `str` — plan_version_migration_id
    
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

<details><summary><code>client.planmigrations.<a href="src/schematic/planmigrations/client.py">count_migrations</a>(...) -> CountMigrationsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.planmigrations.count_migrations(
    plan_version_id="plan_version_id",
    status="completed",
    limit=1000000,
    offset=1000000,
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

**plan_version_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[PlanVersionMigrationStatus]` 
    
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

## componentspublic
<details><summary><code>client.componentspublic.<a href="src/schematic/componentspublic/client.py">get_public_plans</a>() -> GetPublicPlansResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.componentspublic.get_public_plans()

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

## scheduledcheckout
<details><summary><code>client.scheduledcheckout.<a href="src/schematic/scheduledcheckout/client.py">list_scheduled_checkouts</a>(...) -> ListScheduledCheckoutsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.scheduledcheckout.list_scheduled_checkouts(
    company_id="company_id",
    status="cancelled",
    limit=1000000,
    offset=1000000,
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

**status:** `typing.Optional[ScheduledCheckoutStatus]` 
    
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

<details><summary><code>client.scheduledcheckout.<a href="src/schematic/scheduledcheckout/client.py">create_scheduled_checkout</a>(...) -> CreateScheduledCheckoutResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment
import datetime

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.scheduledcheckout.create_scheduled_checkout(
    company_id="company_id",
    execute_after=datetime.datetime.fromisoformat("2024-01-15T09:30:00+00:00"),
    from_plan_id="from_plan_id",
    to_plan_id="to_plan_id",
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

**execute_after:** `datetime.datetime` 
    
</dd>
</dl>

<dl>
<dd>

**from_plan_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**to_plan_id:** `str` 
    
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

<details><summary><code>client.scheduledcheckout.<a href="src/schematic/scheduledcheckout/client.py">get_scheduled_checkout</a>(...) -> GetScheduledCheckoutResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.scheduledcheckout.get_scheduled_checkout(
    scheduled_checkout_id="scheduled_checkout_id",
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

**scheduled_checkout_id:** `str` — scheduled_checkout_id
    
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

<details><summary><code>client.scheduledcheckout.<a href="src/schematic/scheduledcheckout/client.py">update_scheduled_checkout</a>(...) -> UpdateScheduledCheckoutResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.scheduledcheckout.update_scheduled_checkout(
    scheduled_checkout_id="scheduled_checkout_id",
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

**scheduled_checkout_id:** `str` — scheduled_checkout_id
    
</dd>
</dl>

<dl>
<dd>

**execute_after:** `typing.Optional[datetime.datetime]` 
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[ScheduledCheckoutStatus]` 
    
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
<details><summary><code>client.accesstokens.<a href="src/schematic/accesstokens/client.py">issue_temporary_access_token</a>(...) -> IssueTemporaryAccessTokenResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.accesstokens.issue_temporary_access_token(
    lookup={
        "key": "value"
    },
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

**resource_type:** `TemporaryAccessTokenResourceType` 
    
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
<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">list_webhook_events</a>(...) -> ListWebhookEventsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.webhooks.list_webhook_events(
    ids=[
        "ids"
    ],
    q="q",
    webhook_id="webhook_id",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">get_webhook_event</a>(...) -> GetWebhookEventResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">count_webhook_events</a>(...) -> CountWebhookEventsResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.webhooks.count_webhook_events(
    ids=[
        "ids"
    ],
    q="q",
    webhook_id="webhook_id",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">list_webhooks</a>(...) -> ListWebhooksResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.webhooks.list_webhooks(
    q="q",
    limit=1000000,
    offset=1000000,
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

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">create_webhook</a>(...) -> CreateWebhookResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.webhooks.create_webhook(
    name="name",
    request_types=[
        "subscription.trial.ended"
    ],
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

**request_types:** `typing.List[WebhookRequestType]` 
    
</dd>
</dl>

<dl>
<dd>

**url:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**credit_trigger_configs:** `typing.Optional[typing.List[CreditTriggerConfig]]` 
    
</dd>
</dl>

<dl>
<dd>

**entitlement_trigger_configs:** `typing.Optional[typing.List[EntitlementTriggerConfig]]` 
    
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

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">get_webhook</a>(...) -> GetWebhookResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">update_webhook</a>(...) -> UpdateWebhookResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

**credit_trigger_configs:** `typing.Optional[typing.List[CreditTriggerConfig]]` 
    
</dd>
</dl>

<dl>
<dd>

**entitlement_trigger_configs:** `typing.Optional[typing.List[EntitlementTriggerConfig]]` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_types:** `typing.Optional[typing.List[WebhookRequestType]]` 
    
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

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">delete_webhook</a>(...) -> DeleteWebhookResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
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

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">count_webhooks</a>(...) -> CountWebhooksResponse</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from schematic import Schematic
from schematic.environment import SchematicEnvironment

client = Schematic(
    api_key="<value>",
    environment=SchematicEnvironment.DEFAULT,
)

client.webhooks.count_webhooks(
    q="q",
    limit=1000000,
    offset=1000000,
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

