# This file was auto-generated by Fern from our API Definition.

import typing
from .environment import SchematicEnvironment
import httpx
from .core.client_wrapper import SyncClientWrapper
from .accounts.client import AccountsClient
from .features.client import FeaturesClient
from .billing.client import BillingClient
from .checkout.client import CheckoutClient
from .companies.client import CompaniesClient
from .entitlements.client import EntitlementsClient
from .plans.client import PlansClient
from .components.client import ComponentsClient
from .crm.client import CrmClient
from .events.client import EventsClient
from .plangroups.client import PlangroupsClient
from .accesstokens.client import AccesstokensClient
from .webhooks.client import WebhooksClient
from .core.client_wrapper import AsyncClientWrapper
from .accounts.client import AsyncAccountsClient
from .features.client import AsyncFeaturesClient
from .billing.client import AsyncBillingClient
from .checkout.client import AsyncCheckoutClient
from .companies.client import AsyncCompaniesClient
from .entitlements.client import AsyncEntitlementsClient
from .plans.client import AsyncPlansClient
from .components.client import AsyncComponentsClient
from .crm.client import AsyncCrmClient
from .events.client import AsyncEventsClient
from .plangroups.client import AsyncPlangroupsClient
from .accesstokens.client import AsyncAccesstokensClient
from .webhooks.client import AsyncWebhooksClient


class BaseSchematic:
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propagate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : SchematicEnvironment
        The environment to use for requests from the client. from .environment import SchematicEnvironment



        Defaults to SchematicEnvironment.DEFAULT



    api_key : str
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 60 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.Client]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from schematic import Schematic

    client = Schematic(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: SchematicEnvironment = SchematicEnvironment.DEFAULT,
        api_key: str,
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.Client] = None,
    ):
        _defaulted_timeout = timeout if timeout is not None else 60 if httpx_client is None else None
        self._client_wrapper = SyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            api_key=api_key,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.Client(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.Client(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
        )
        self.accounts = AccountsClient(client_wrapper=self._client_wrapper)
        self.features = FeaturesClient(client_wrapper=self._client_wrapper)
        self.billing = BillingClient(client_wrapper=self._client_wrapper)
        self.checkout = CheckoutClient(client_wrapper=self._client_wrapper)
        self.companies = CompaniesClient(client_wrapper=self._client_wrapper)
        self.entitlements = EntitlementsClient(client_wrapper=self._client_wrapper)
        self.plans = PlansClient(client_wrapper=self._client_wrapper)
        self.components = ComponentsClient(client_wrapper=self._client_wrapper)
        self.crm = CrmClient(client_wrapper=self._client_wrapper)
        self.events = EventsClient(client_wrapper=self._client_wrapper)
        self.plangroups = PlangroupsClient(client_wrapper=self._client_wrapper)
        self.accesstokens = AccesstokensClient(client_wrapper=self._client_wrapper)
        self.webhooks = WebhooksClient(client_wrapper=self._client_wrapper)


class AsyncBaseSchematic:
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propagate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : SchematicEnvironment
        The environment to use for requests from the client. from .environment import SchematicEnvironment



        Defaults to SchematicEnvironment.DEFAULT



    api_key : str
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 60 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.AsyncClient]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from schematic import AsyncSchematic

    client = AsyncSchematic(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: SchematicEnvironment = SchematicEnvironment.DEFAULT,
        api_key: str,
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.AsyncClient] = None,
    ):
        _defaulted_timeout = timeout if timeout is not None else 60 if httpx_client is None else None
        self._client_wrapper = AsyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            api_key=api_key,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
        )
        self.accounts = AsyncAccountsClient(client_wrapper=self._client_wrapper)
        self.features = AsyncFeaturesClient(client_wrapper=self._client_wrapper)
        self.billing = AsyncBillingClient(client_wrapper=self._client_wrapper)
        self.checkout = AsyncCheckoutClient(client_wrapper=self._client_wrapper)
        self.companies = AsyncCompaniesClient(client_wrapper=self._client_wrapper)
        self.entitlements = AsyncEntitlementsClient(client_wrapper=self._client_wrapper)
        self.plans = AsyncPlansClient(client_wrapper=self._client_wrapper)
        self.components = AsyncComponentsClient(client_wrapper=self._client_wrapper)
        self.crm = AsyncCrmClient(client_wrapper=self._client_wrapper)
        self.events = AsyncEventsClient(client_wrapper=self._client_wrapper)
        self.plangroups = AsyncPlangroupsClient(client_wrapper=self._client_wrapper)
        self.accesstokens = AsyncAccesstokensClient(client_wrapper=self._client_wrapper)
        self.webhooks = AsyncWebhooksClient(client_wrapper=self._client_wrapper)


def _get_base_url(*, base_url: typing.Optional[str] = None, environment: SchematicEnvironment) -> str:
    if base_url is not None:
        return base_url
    elif environment is not None:
        return environment.value
    else:
        raise Exception("Please pass in either base_url or environment to construct the client")
