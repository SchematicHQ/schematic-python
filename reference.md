# Reference
## accounts
<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">list_api_keys</a>(...)</code></summary>
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
    require_environment=True,
)

```
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">create_api_key</a>(...)</code></summary>
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">get_api_key</a>(...)</code></summary>
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">update_api_key</a>(...)</code></summary>
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">delete_api_key</a>(...)</code></summary>
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">count_api_keys</a>(...)</code></summary>
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
    require_environment=True,
)

```
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">list_api_requests</a>(...)</code></summary>
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
client.accounts.list_api_requests()

```
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">get_api_request</a>(...)</code></summary>
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">count_api_requests</a>(...)</code></summary>
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
client.accounts.count_api_requests()

```
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">list_environments</a>(...)</code></summary>
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
client.accounts.list_environments()

```
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">create_environment</a>(...)</code></summary>
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

**environment_type:** `CreateEnvironmentRequestBodyEnvironmentType` 
    
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">get_environment</a>(...)</code></summary>
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">update_environment</a>(...)</code></summary>
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

**environment_type:** `typing.Optional[UpdateEnvironmentRequestBodyEnvironmentType]` 
    
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

<details><summary><code>client.accounts.<a href="src/schematic/accounts/client.py">delete_environment</a>(...)</code></summary>
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

## features
<details><summary><code>client.features.<a href="src/schematic/features/client.py">count_audience_companies</a>(...)</code></summary>
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
    Schematic,
)

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.features.count_audience_companies(
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
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**condition_groups:** `typing.Sequence[CreateOrUpdateConditionGroupRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**conditions:** `typing.Sequence[CreateOrUpdateConditionRequestBody]` 
    
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

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.features.<a href="src/schematic/features/client.py">count_audience_users</a>(...)</code></summary>
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
    Schematic,
)

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.features.count_audience_users(
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
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**condition_groups:** `typing.Sequence[CreateOrUpdateConditionGroupRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**conditions:** `typing.Sequence[CreateOrUpdateConditionRequestBody]` 
    
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

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.features.<a href="src/schematic/features/client.py">list_audience_companies</a>(...)</code></summary>
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
    Schematic,
)

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.features.list_audience_companies(
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
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**condition_groups:** `typing.Sequence[CreateOrUpdateConditionGroupRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**conditions:** `typing.Sequence[CreateOrUpdateConditionRequestBody]` 
    
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

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.features.<a href="src/schematic/features/client.py">list_audience_users</a>(...)</code></summary>
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
    Schematic,
)

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.features.list_audience_users(
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
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**condition_groups:** `typing.Sequence[CreateOrUpdateConditionGroupRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**conditions:** `typing.Sequence[CreateOrUpdateConditionRequestBody]` 
    
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

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.features.<a href="src/schematic/features/client.py">list_features</a>(...)</code></summary>
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
client.features.list_features()

```
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">create_feature</a>(...)</code></summary>
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

**feature_type:** `CreateFeatureRequestBodyFeatureType` 
    
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

**lifecycle_phase:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**maintainer_id:** `typing.Optional[str]` 
    
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">get_feature</a>(...)</code></summary>
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">update_feature</a>(...)</code></summary>
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

**feature_type:** `typing.Optional[UpdateFeatureRequestBodyFeatureType]` 
    
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

**lifecycle_phase:** `typing.Optional[str]` 
    
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">delete_feature</a>(...)</code></summary>
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">count_features</a>(...)</code></summary>
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
client.features.count_features()

```
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">list_flags</a>(...)</code></summary>
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
client.features.list_flags()

```
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">create_flag</a>(...)</code></summary>
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
    flag_type="flag_type",
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

**flag_type:** `str` 
    
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">get_flag</a>(...)</code></summary>
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">update_flag</a>(...)</code></summary>
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
    flag_type="flag_type",
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

**flag_type:** `str` 
    
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">delete_flag</a>(...)</code></summary>
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">update_flag_rules</a>(...)</code></summary>
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">check_flag</a>(...)</code></summary>
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">check_flags</a>(...)</code></summary>
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

<details><summary><code>client.features.<a href="src/schematic/features/client.py">count_flags</a>(...)</code></summary>
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
client.features.count_flags()

```
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

## billing
<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">list_coupons</a>(...)</code></summary>
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
client.billing.list_coupons()

```
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_billing_coupon</a>(...)</code></summary>
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_billing_customer</a>(...)</code></summary>
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

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">list_customers</a>(...)</code></summary>
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
client.billing.list_customers()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**failed_to_import:** `typing.Optional[bool]` 
    
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">count_customers</a>(...)</code></summary>
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
client.billing.count_customers()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**failed_to_import:** `typing.Optional[bool]` 
    
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">list_invoices</a>(...)</code></summary>
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
    customer_external_id="customer_external_id",
)

```
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

**subscription_external_id:** `typing.Optional[str]` 
    
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_invoice</a>(...)</code></summary>
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">list_meters</a>(...)</code></summary>
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
client.billing.list_meters()

```
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_billing_meter</a>(...)</code></summary>
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">list_payment_methods</a>(...)</code></summary>
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
    customer_external_id="customer_external_id",
)

```
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

**subscription_external_id:** `typing.Optional[str]` 
    
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_payment_method</a>(...)</code></summary>
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

**subscription_external_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">search_billing_prices</a>(...)</code></summary>
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
client.billing.search_billing_prices()

```
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

**interval:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**usage_type:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**price:** `typing.Optional[int]` 
    
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_billing_price</a>(...)</code></summary>
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
client.billing.upsert_billing_price(
    currency="currency",
    interval="interval",
    is_active=True,
    price=1,
    price_external_id="price_external_id",
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

**currency:** `str` 
    
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

**product_external_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**usage_type:** `CreateBillingPriceRequestBodyUsageType` 
    
</dd>
</dl>

<dl>
<dd>

**meter_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">list_product_prices</a>(...)</code></summary>
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
client.billing.list_product_prices()

```
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

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**price_usage_type:** `typing.Optional[ListProductPricesRequestPriceUsageType]` 
    
</dd>
</dl>

<dl>
<dd>

**without_linked_to_plan:** `typing.Optional[bool]` — Filter products that are not linked to any plan
    
</dd>
</dl>

<dl>
<dd>

**with_zero_price:** `typing.Optional[bool]` — Filter products that have zero price for free subscription type
    
</dd>
</dl>

<dl>
<dd>

**with_prices_only:** `typing.Optional[bool]` — Filter products that have prices
    
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">delete_product_price</a>(...)</code></summary>
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_billing_product</a>(...)</code></summary>
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
    currency="currency",
    external_id="external_id",
    name="name",
    price=1.1,
    quantity=1,
)

```
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

**quantity:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">list_billing_products</a>(...)</code></summary>
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
client.billing.list_billing_products()

```
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

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**price_usage_type:** `typing.Optional[ListBillingProductsRequestPriceUsageType]` 
    
</dd>
</dl>

<dl>
<dd>

**without_linked_to_plan:** `typing.Optional[bool]` — Filter products that are not linked to any plan
    
</dd>
</dl>

<dl>
<dd>

**with_zero_price:** `typing.Optional[bool]` — Filter products that have zero price for free subscription type
    
</dd>
</dl>

<dl>
<dd>

**with_prices_only:** `typing.Optional[bool]` — Filter products that have prices
    
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">count_billing_products</a>(...)</code></summary>
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
client.billing.count_billing_products()

```
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

**q:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**price_usage_type:** `typing.Optional[CountBillingProductsRequestPriceUsageType]` 
    
</dd>
</dl>

<dl>
<dd>

**without_linked_to_plan:** `typing.Optional[bool]` — Filter products that are not linked to any plan
    
</dd>
</dl>

<dl>
<dd>

**with_zero_price:** `typing.Optional[bool]` — Filter products that have zero price for free subscription type
    
</dd>
</dl>

<dl>
<dd>

**with_prices_only:** `typing.Optional[bool]` — Filter products that have prices
    
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

<details><summary><code>client.billing.<a href="src/schematic/billing/client.py">upsert_billing_subscription</a>(...)</code></summary>
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
            usage_type="usage_type",
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

**interval:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**metadata:** `typing.Optional[typing.Dict[str, typing.Optional[typing.Any]]]` 
    
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

**trial_end_setting:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
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
<details><summary><code>client.checkout.<a href="src/schematic/checkout/client.py">internal</a>(...)</code></summary>
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
    new_plan_id="new_plan_id",
    new_price_id="new_price_id",
    pay_in_advance=[
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

<details><summary><code>client.checkout.<a href="src/schematic/checkout/client.py">get_checkout_data</a>(...)</code></summary>
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

<details><summary><code>client.checkout.<a href="src/schematic/checkout/client.py">preview_checkout_internal</a>(...)</code></summary>
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
    new_plan_id="new_plan_id",
    new_price_id="new_price_id",
    pay_in_advance=[
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

<details><summary><code>client.checkout.<a href="src/schematic/checkout/client.py">update_customer_subscription_trial_end</a>(...)</code></summary>
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
<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">list_companies</a>(...)</code></summary>
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
client.companies.list_companies()

```
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">upsert_company</a>(...)</code></summary>
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

**keys:** `typing.Dict[str, str]` 
    
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

**traits:** `typing.Optional[typing.Dict[str, typing.Optional[typing.Any]]]` — A map of trait names to trait values
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_company</a>(...)</code></summary>
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">delete_company</a>(...)</code></summary>
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
)

```
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">count_companies</a>(...)</code></summary>
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
client.companies.count_companies()

```
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">create_company</a>(...)</code></summary>
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

**keys:** `typing.Dict[str, str]` 
    
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

**traits:** `typing.Optional[typing.Dict[str, typing.Optional[typing.Any]]]` — A map of trait names to trait values
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">delete_company_by_keys</a>(...)</code></summary>
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">lookup_company</a>(...)</code></summary>
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
    keys={"keys": {"key": "value"}},
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**keys:** `typing.Dict[str, typing.Optional[typing.Any]]` — Key/value pairs
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_active_deals</a>(...)</code></summary>
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
client.companies.get_active_deals(
    company_id="company_id",
    deal_stage="deal_stage",
)

```
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

**deal_stage:** `str` 
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">list_company_memberships</a>(...)</code></summary>
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
client.companies.list_company_memberships()

```
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_or_create_company_membership</a>(...)</code></summary>
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">delete_company_membership</a>(...)</code></summary>
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_active_company_subscription</a>(...)</code></summary>
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
client.companies.get_active_company_subscription()

```
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">upsert_company_trait</a>(...)</code></summary>
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

**keys:** `typing.Dict[str, str]` — Key/value pairs too identify a company or user
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">list_entity_key_definitions</a>(...)</code></summary>
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
client.companies.list_entity_key_definitions()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**entity_type:** `typing.Optional[ListEntityKeyDefinitionsRequestEntityType]` 
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">count_entity_key_definitions</a>(...)</code></summary>
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
client.companies.count_entity_key_definitions()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**entity_type:** `typing.Optional[CountEntityKeyDefinitionsRequestEntityType]` 
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">list_entity_trait_definitions</a>(...)</code></summary>
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
client.companies.list_entity_trait_definitions()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**entity_type:** `typing.Optional[ListEntityTraitDefinitionsRequestEntityType]` 
    
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

**trait_type:** `typing.Optional[ListEntityTraitDefinitionsRequestTraitType]` 
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_or_create_entity_trait_definition</a>(...)</code></summary>
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

**entity_type:** `CreateEntityTraitDefinitionRequestBodyEntityType` 
    
</dd>
</dl>

<dl>
<dd>

**hierarchy:** `typing.Sequence[str]` 
    
</dd>
</dl>

<dl>
<dd>

**trait_type:** `CreateEntityTraitDefinitionRequestBodyTraitType` 
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_entity_trait_definition</a>(...)</code></summary>
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">update_entity_trait_definition</a>(...)</code></summary>
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

**trait_type:** `UpdateEntityTraitDefinitionRequestBodyTraitType` 
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">count_entity_trait_definitions</a>(...)</code></summary>
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
client.companies.count_entity_trait_definitions()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**entity_type:** `typing.Optional[CountEntityTraitDefinitionsRequestEntityType]` 
    
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

**trait_type:** `typing.Optional[CountEntityTraitDefinitionsRequestTraitType]` 
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_entity_trait_values</a>(...)</code></summary>
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
)

```
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">upsert_user_trait</a>(...)</code></summary>
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

**keys:** `typing.Dict[str, str]` — Key/value pairs too identify a company or user
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">list_users</a>(...)</code></summary>
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
client.companies.list_users()

```
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">upsert_user</a>(...)</code></summary>
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
    company={"key": "value"},
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

**company:** `typing.Dict[str, str]` — Optionally specify company using key/value pairs
    
</dd>
</dl>

<dl>
<dd>

**keys:** `typing.Dict[str, str]` 
    
</dd>
</dl>

<dl>
<dd>

**company_id:** `typing.Optional[str]` — Optionally specify company using Schematic company ID
    
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

**traits:** `typing.Optional[typing.Dict[str, typing.Optional[typing.Any]]]` — A map of trait names to trait values
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">get_user</a>(...)</code></summary>
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">delete_user</a>(...)</code></summary>
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">count_users</a>(...)</code></summary>
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
client.companies.count_users()

```
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">create_user</a>(...)</code></summary>
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
    company={"key": "value"},
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

**company:** `typing.Dict[str, str]` — Optionally specify company using key/value pairs
    
</dd>
</dl>

<dl>
<dd>

**keys:** `typing.Dict[str, str]` 
    
</dd>
</dl>

<dl>
<dd>

**company_id:** `typing.Optional[str]` — Optionally specify company using Schematic company ID
    
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

**traits:** `typing.Optional[typing.Dict[str, typing.Optional[typing.Any]]]` — A map of trait names to trait values
    
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">delete_user_by_keys</a>(...)</code></summary>
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

<details><summary><code>client.companies.<a href="src/schematic/companies/client.py">lookup_user</a>(...)</code></summary>
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
    keys={"keys": {"key": "value"}},
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**keys:** `typing.Dict[str, typing.Optional[typing.Any]]` — Key/value pairs
    
</dd>
</dl>

<dl>
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
<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">list_company_overrides</a>(...)</code></summary>
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
client.entitlements.list_company_overrides()

```
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">create_company_override</a>(...)</code></summary>
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

**value_type:** `CreateCompanyOverrideRequestBodyValueType` 
    
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

**value_bool:** `typing.Optional[bool]` 
    
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">get_company_override</a>(...)</code></summary>
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">update_company_override</a>(...)</code></summary>
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

**value_type:** `UpdateCompanyOverrideRequestBodyValueType` 
    
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

**value_bool:** `typing.Optional[bool]` 
    
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">delete_company_override</a>(...)</code></summary>
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">count_company_overrides</a>(...)</code></summary>
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
client.entitlements.count_company_overrides()

```
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">list_feature_companies</a>(...)</code></summary>
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
)

```
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">count_feature_companies</a>(...)</code></summary>
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
)

```
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">list_feature_usage</a>(...)</code></summary>
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
client.entitlements.list_feature_usage()

```
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">count_feature_usage</a>(...)</code></summary>
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
client.entitlements.count_feature_usage()

```
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">list_feature_users</a>(...)</code></summary>
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
)

```
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">count_feature_users</a>(...)</code></summary>
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
)

```
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">list_plan_entitlements</a>(...)</code></summary>
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
client.entitlements.list_plan_entitlements()

```
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">create_plan_entitlement</a>(...)</code></summary>
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

**value_type:** `CreatePlanEntitlementRequestBodyValueType` 
    
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

**price_behavior:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**value_bool:** `typing.Optional[bool]` 
    
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

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">get_plan_entitlement</a>(...)</code></summary>
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">update_plan_entitlement</a>(...)</code></summary>
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

**value_type:** `UpdatePlanEntitlementRequestBodyValueType` 
    
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

**price_behavior:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**value_bool:** `typing.Optional[bool]` 
    
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

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">delete_plan_entitlement</a>(...)</code></summary>
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">count_plan_entitlements</a>(...)</code></summary>
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
client.entitlements.count_plan_entitlements()

```
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

<details><summary><code>client.entitlements.<a href="src/schematic/entitlements/client.py">get_feature_usage_by_company</a>(...)</code></summary>
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
    keys={"keys": {"key": "value"}},
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**keys:** `typing.Dict[str, typing.Optional[typing.Any]]` — Key/value pairs
    
</dd>
</dl>

<dl>
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
<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">update_company_plans</a>(...)</code></summary>
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

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">get_audience</a>(...)</code></summary>
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
client.plans.get_audience(
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

**plan_audience_id:** `str` — plan_audience_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">update_audience</a>(...)</code></summary>
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
    Schematic,
)

client = Schematic(
    api_key="YOUR_API_KEY",
)
client.plans.update_audience(
    plan_audience_id="plan_audience_id",
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
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**plan_audience_id:** `str` — plan_audience_id
    
</dd>
</dl>

<dl>
<dd>

**condition_groups:** `typing.Sequence[CreateOrUpdateConditionGroupRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**conditions:** `typing.Sequence[CreateOrUpdateConditionRequestBody]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">delete_audience</a>(...)</code></summary>
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
client.plans.delete_audience(
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

**plan_audience_id:** `str` — plan_audience_id
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">list_plans</a>(...)</code></summary>
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
client.plans.list_plans()

```
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

**plan_type:** `typing.Optional[ListPlansRequestPlanType]` — Filter by plan type
    
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

**without_product_id:** `typing.Optional[bool]` — Filter out plans that have a billing product ID
    
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

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">create_plan</a>(...)</code></summary>
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

**plan_type:** `CreatePlanRequestBodyPlanType` 
    
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

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">get_plan</a>(...)</code></summary>
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

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">update_plan</a>(...)</code></summary>
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

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">delete_plan</a>(...)</code></summary>
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

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">upsert_billing_product_plan</a>(...)</code></summary>
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
    is_free_plan=True,
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

**is_free_plan:** `bool` 
    
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

**monthly_price_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**trial_days:** `typing.Optional[int]` 
    
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

<details><summary><code>client.plans.<a href="src/schematic/plans/client.py">count_plans</a>(...)</code></summary>
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
client.plans.count_plans()

```
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

**plan_type:** `typing.Optional[CountPlansRequestPlanType]` — Filter by plan type
    
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

**without_product_id:** `typing.Optional[bool]` — Filter out plans that have a billing product ID
    
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

## components
<details><summary><code>client.components.<a href="src/schematic/components/client.py">list_components</a>(...)</code></summary>
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
client.components.list_components()

```
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

<details><summary><code>client.components.<a href="src/schematic/components/client.py">create_component</a>(...)</code></summary>
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
    entity_type="entitlement",
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

**entity_type:** `CreateComponentRequestBodyEntityType` 
    
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

<details><summary><code>client.components.<a href="src/schematic/components/client.py">get_component</a>(...)</code></summary>
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

<details><summary><code>client.components.<a href="src/schematic/components/client.py">update_component</a>(...)</code></summary>
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

**entity_type:** `typing.Optional[UpdateComponentRequestBodyEntityType]` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**state:** `typing.Optional[UpdateComponentRequestBodyState]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.components.<a href="src/schematic/components/client.py">delete_component</a>(...)</code></summary>
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

<details><summary><code>client.components.<a href="src/schematic/components/client.py">count_components</a>(...)</code></summary>
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
client.components.count_components()

```
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

<details><summary><code>client.components.<a href="src/schematic/components/client.py">preview_component_data</a>(...)</code></summary>
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
client.components.preview_component_data()

```
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

## crm
<details><summary><code>client.crm.<a href="src/schematic/crm/client.py">upsert_deal_line_item_association</a>(...)</code></summary>
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
client.crm.upsert_deal_line_item_association(
    deal_external_id="deal_external_id",
    line_item_external_id="line_item_external_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**deal_external_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**line_item_external_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.crm.<a href="src/schematic/crm/client.py">upsert_line_item</a>(...)</code></summary>
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
client.crm.upsert_line_item(
    amount="amount",
    interval="interval",
    line_item_external_id="line_item_external_id",
    product_external_id="product_external_id",
    quantity=1,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**amount:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**interval:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**line_item_external_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**product_external_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**quantity:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**discount_percentage:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**term_month:** `typing.Optional[int]` 
    
</dd>
</dl>

<dl>
<dd>

**total_discount:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.crm.<a href="src/schematic/crm/client.py">upsert_crm_deal</a>(...)</code></summary>
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
client.crm.upsert_crm_deal(
    crm_company_key="crm_company_key",
    crm_type="crm_type",
    deal_external_id="deal_external_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**crm_company_key:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**crm_type:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**deal_external_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**arr:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**crm_company_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**crm_product_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**deal_name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**deal_stage:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**mrr:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.crm.<a href="src/schematic/crm/client.py">list_crm_products</a>(...)</code></summary>
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
client.crm.list_crm_products()

```
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

<details><summary><code>client.crm.<a href="src/schematic/crm/client.py">upsert_crm_product</a>(...)</code></summary>
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
client.crm.upsert_crm_product(
    currency="currency",
    description="description",
    external_id="external_id",
    interval="interval",
    name="name",
    price="price",
    quantity=1,
    sku="sku",
)

```
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

**external_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**interval:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**price:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**quantity:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**sku:** `str` 
    
</dd>
</dl>

<dl>
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
<details><summary><code>client.events.<a href="src/schematic/events/client.py">create_event_batch</a>(...)</code></summary>
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
            event_type="identify",
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

<details><summary><code>client.events.<a href="src/schematic/events/client.py">get_event_summaries</a>(...)</code></summary>
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
client.events.get_event_summaries()

```
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

<details><summary><code>client.events.<a href="src/schematic/events/client.py">list_events</a>(...)</code></summary>
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
client.events.list_events()

```
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

**event_types:** `typing.Optional[typing.Union[str, typing.Sequence[str]]]` 
    
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

<details><summary><code>client.events.<a href="src/schematic/events/client.py">create_event</a>(...)</code></summary>
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
    event_type="identify",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**event_type:** `CreateEventRequestBodyEventType` — Either 'identify' or 'track'
    
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

<details><summary><code>client.events.<a href="src/schematic/events/client.py">get_event</a>(...)</code></summary>
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

<details><summary><code>client.events.<a href="src/schematic/events/client.py">get_segment_integration_status</a>()</code></summary>
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

## plangroups
<details><summary><code>client.plangroups.<a href="src/schematic/plangroups/client.py">get_plan_group</a>()</code></summary>
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

<details><summary><code>client.plangroups.<a href="src/schematic/plangroups/client.py">create_plan_group</a>(...)</code></summary>
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
client.plangroups.create_plan_group(
    add_on_ids=["add_on_ids"],
    plan_ids=["plan_ids"],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**add_on_ids:** `typing.Sequence[str]` 
    
</dd>
</dl>

<dl>
<dd>

**plan_ids:** `typing.Sequence[str]` 
    
</dd>
</dl>

<dl>
<dd>

**default_plan_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**trial_days:** `typing.Optional[int]` 
    
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

<details><summary><code>client.plangroups.<a href="src/schematic/plangroups/client.py">update_plan_group</a>(...)</code></summary>
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
client.plangroups.update_plan_group(
    plan_group_id="plan_group_id",
    add_on_ids=["add_on_ids"],
    plan_ids=["plan_ids"],
)

```
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

**add_on_ids:** `typing.Sequence[str]` 
    
</dd>
</dl>

<dl>
<dd>

**plan_ids:** `typing.Sequence[str]` 
    
</dd>
</dl>

<dl>
<dd>

**default_plan_id:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**trial_days:** `typing.Optional[int]` 
    
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
<details><summary><code>client.accesstokens.<a href="src/schematic/accesstokens/client.py">issue_temporary_access_token</a>(...)</code></summary>
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
    resource_type="resource_type",
)

```
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

**resource_type:** `str` 
    
</dd>
</dl>

<dl>
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
<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">list_webhook_events</a>(...)</code></summary>
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
client.webhooks.list_webhook_events()

```
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

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">get_webhook_event</a>(...)</code></summary>
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

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">count_webhook_events</a>(...)</code></summary>
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
client.webhooks.count_webhook_events()

```
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

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">list_webhooks</a>(...)</code></summary>
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
client.webhooks.list_webhooks()

```
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

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">create_webhook</a>(...)</code></summary>
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
    request_types=["company.updated"],
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

**request_types:** `typing.Sequence[CreateWebhookRequestBodyRequestTypesItem]` 
    
</dd>
</dl>

<dl>
<dd>

**url:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">get_webhook</a>(...)</code></summary>
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

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">update_webhook</a>(...)</code></summary>
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

**name:** `typing.Optional[str]` 
    
</dd>
</dl>

<dl>
<dd>

**request_types:** `typing.Optional[typing.Sequence[UpdateWebhookRequestBodyRequestTypesItem]]` 
    
</dd>
</dl>

<dl>
<dd>

**status:** `typing.Optional[UpdateWebhookRequestBodyStatus]` 
    
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

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">delete_webhook</a>(...)</code></summary>
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

<details><summary><code>client.webhooks.<a href="src/schematic/webhooks/client.py">count_webhooks</a>(...)</code></summary>
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
client.webhooks.count_webhooks()

```
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

