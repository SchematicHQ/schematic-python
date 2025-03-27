# This file was auto-generated by Fern from our API Definition.

import typing
from ..core.client_wrapper import SyncClientWrapper
from ..types.update_add_on_request_body import UpdateAddOnRequestBody
from ..types.update_pay_in_advance_request_body import UpdatePayInAdvanceRequestBody
from ..core.request_options import RequestOptions
from .types.checkout_internal_response import CheckoutInternalResponse
from ..core.serialization import convert_and_respect_annotation_metadata
from ..core.pydantic_utilities import parse_obj_as
from ..errors.bad_request_error import BadRequestError
from ..types.api_error import ApiError as types_api_error_ApiError
from ..errors.unauthorized_error import UnauthorizedError
from ..errors.forbidden_error import ForbiddenError
from ..errors.internal_server_error import InternalServerError
from json.decoder import JSONDecodeError
from ..core.api_error import ApiError as core_api_error_ApiError
from .types.get_checkout_data_response import GetCheckoutDataResponse
from .types.preview_checkout_internal_response import PreviewCheckoutInternalResponse
import datetime as dt
from .types.update_customer_subscription_trial_end_response import (
    UpdateCustomerSubscriptionTrialEndResponse,
)
from ..core.jsonable_encoder import jsonable_encoder
from ..errors.not_found_error import NotFoundError
from ..core.client_wrapper import AsyncClientWrapper

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class CheckoutClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def internal(
        self,
        *,
        add_on_ids: typing.Sequence[UpdateAddOnRequestBody],
        company_id: str,
        new_plan_id: str,
        new_price_id: str,
        pay_in_advance: typing.Sequence[UpdatePayInAdvanceRequestBody],
        coupon_external_id: typing.Optional[str] = OMIT,
        payment_method_id: typing.Optional[str] = OMIT,
        promo_code: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> CheckoutInternalResponse:
        """
        Parameters
        ----------
        add_on_ids : typing.Sequence[UpdateAddOnRequestBody]

        company_id : str

        new_plan_id : str

        new_price_id : str

        pay_in_advance : typing.Sequence[UpdatePayInAdvanceRequestBody]

        coupon_external_id : typing.Optional[str]

        payment_method_id : typing.Optional[str]

        promo_code : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        CheckoutInternalResponse
            Created

        Examples
        --------
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
        """
        _response = self._client_wrapper.httpx_client.request(
            "checkout-internal",
            method="POST",
            json={
                "add_on_ids": convert_and_respect_annotation_metadata(
                    object_=add_on_ids,
                    annotation=typing.Sequence[UpdateAddOnRequestBody],
                    direction="write",
                ),
                "company_id": company_id,
                "coupon_external_id": coupon_external_id,
                "new_plan_id": new_plan_id,
                "new_price_id": new_price_id,
                "pay_in_advance": convert_and_respect_annotation_metadata(
                    object_=pay_in_advance,
                    annotation=typing.Sequence[UpdatePayInAdvanceRequestBody],
                    direction="write",
                ),
                "payment_method_id": payment_method_id,
                "promo_code": promo_code,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    CheckoutInternalResponse,
                    parse_obj_as(
                        type_=CheckoutInternalResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 400:
                raise BadRequestError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 401:
                raise UnauthorizedError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 403:
                raise ForbiddenError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 500:
                raise InternalServerError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise core_api_error_ApiError(status_code=_response.status_code, body=_response.text)
        raise core_api_error_ApiError(status_code=_response.status_code, body=_response_json)

    def get_checkout_data(
        self,
        *,
        company_id: str,
        selected_plan_id: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> GetCheckoutDataResponse:
        """
        Parameters
        ----------
        company_id : str

        selected_plan_id : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        GetCheckoutDataResponse
            OK

        Examples
        --------
        from schematic import Schematic

        client = Schematic(
            api_key="YOUR_API_KEY",
        )
        client.checkout.get_checkout_data(
            company_id="company_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "checkout-internal/data",
            method="POST",
            json={
                "company_id": company_id,
                "selected_plan_id": selected_plan_id,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    GetCheckoutDataResponse,
                    parse_obj_as(
                        type_=GetCheckoutDataResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 400:
                raise BadRequestError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 401:
                raise UnauthorizedError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 403:
                raise ForbiddenError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 500:
                raise InternalServerError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise core_api_error_ApiError(status_code=_response.status_code, body=_response.text)
        raise core_api_error_ApiError(status_code=_response.status_code, body=_response_json)

    def preview_checkout_internal(
        self,
        *,
        add_on_ids: typing.Sequence[UpdateAddOnRequestBody],
        company_id: str,
        new_plan_id: str,
        new_price_id: str,
        pay_in_advance: typing.Sequence[UpdatePayInAdvanceRequestBody],
        coupon_external_id: typing.Optional[str] = OMIT,
        payment_method_id: typing.Optional[str] = OMIT,
        promo_code: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> PreviewCheckoutInternalResponse:
        """
        Parameters
        ----------
        add_on_ids : typing.Sequence[UpdateAddOnRequestBody]

        company_id : str

        new_plan_id : str

        new_price_id : str

        pay_in_advance : typing.Sequence[UpdatePayInAdvanceRequestBody]

        coupon_external_id : typing.Optional[str]

        payment_method_id : typing.Optional[str]

        promo_code : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        PreviewCheckoutInternalResponse
            OK

        Examples
        --------
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
        """
        _response = self._client_wrapper.httpx_client.request(
            "checkout-internal/preview",
            method="POST",
            json={
                "add_on_ids": convert_and_respect_annotation_metadata(
                    object_=add_on_ids,
                    annotation=typing.Sequence[UpdateAddOnRequestBody],
                    direction="write",
                ),
                "company_id": company_id,
                "coupon_external_id": coupon_external_id,
                "new_plan_id": new_plan_id,
                "new_price_id": new_price_id,
                "pay_in_advance": convert_and_respect_annotation_metadata(
                    object_=pay_in_advance,
                    annotation=typing.Sequence[UpdatePayInAdvanceRequestBody],
                    direction="write",
                ),
                "payment_method_id": payment_method_id,
                "promo_code": promo_code,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    PreviewCheckoutInternalResponse,
                    parse_obj_as(
                        type_=PreviewCheckoutInternalResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 400:
                raise BadRequestError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 401:
                raise UnauthorizedError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 403:
                raise ForbiddenError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 500:
                raise InternalServerError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise core_api_error_ApiError(status_code=_response.status_code, body=_response.text)
        raise core_api_error_ApiError(status_code=_response.status_code, body=_response_json)

    def update_customer_subscription_trial_end(
        self,
        subscription_id: str,
        *,
        trial_end: typing.Optional[dt.datetime] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> UpdateCustomerSubscriptionTrialEndResponse:
        """
        Parameters
        ----------
        subscription_id : str
            subscription_id

        trial_end : typing.Optional[dt.datetime]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        UpdateCustomerSubscriptionTrialEndResponse
            OK

        Examples
        --------
        from schematic import Schematic

        client = Schematic(
            api_key="YOUR_API_KEY",
        )
        client.checkout.update_customer_subscription_trial_end(
            subscription_id="subscription_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"subscription/{jsonable_encoder(subscription_id)}/edit-trial-end",
            method="PUT",
            json={
                "trial_end": trial_end,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    UpdateCustomerSubscriptionTrialEndResponse,
                    parse_obj_as(
                        type_=UpdateCustomerSubscriptionTrialEndResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 400:
                raise BadRequestError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 401:
                raise UnauthorizedError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 403:
                raise ForbiddenError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 404:
                raise NotFoundError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 500:
                raise InternalServerError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise core_api_error_ApiError(status_code=_response.status_code, body=_response.text)
        raise core_api_error_ApiError(status_code=_response.status_code, body=_response_json)


class AsyncCheckoutClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def internal(
        self,
        *,
        add_on_ids: typing.Sequence[UpdateAddOnRequestBody],
        company_id: str,
        new_plan_id: str,
        new_price_id: str,
        pay_in_advance: typing.Sequence[UpdatePayInAdvanceRequestBody],
        coupon_external_id: typing.Optional[str] = OMIT,
        payment_method_id: typing.Optional[str] = OMIT,
        promo_code: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> CheckoutInternalResponse:
        """
        Parameters
        ----------
        add_on_ids : typing.Sequence[UpdateAddOnRequestBody]

        company_id : str

        new_plan_id : str

        new_price_id : str

        pay_in_advance : typing.Sequence[UpdatePayInAdvanceRequestBody]

        coupon_external_id : typing.Optional[str]

        payment_method_id : typing.Optional[str]

        promo_code : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        CheckoutInternalResponse
            Created

        Examples
        --------
        import asyncio

        from schematic import (
            AsyncSchematic,
            UpdateAddOnRequestBody,
            UpdatePayInAdvanceRequestBody,
        )

        client = AsyncSchematic(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.checkout.internal(
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


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "checkout-internal",
            method="POST",
            json={
                "add_on_ids": convert_and_respect_annotation_metadata(
                    object_=add_on_ids,
                    annotation=typing.Sequence[UpdateAddOnRequestBody],
                    direction="write",
                ),
                "company_id": company_id,
                "coupon_external_id": coupon_external_id,
                "new_plan_id": new_plan_id,
                "new_price_id": new_price_id,
                "pay_in_advance": convert_and_respect_annotation_metadata(
                    object_=pay_in_advance,
                    annotation=typing.Sequence[UpdatePayInAdvanceRequestBody],
                    direction="write",
                ),
                "payment_method_id": payment_method_id,
                "promo_code": promo_code,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    CheckoutInternalResponse,
                    parse_obj_as(
                        type_=CheckoutInternalResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 400:
                raise BadRequestError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 401:
                raise UnauthorizedError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 403:
                raise ForbiddenError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 500:
                raise InternalServerError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise core_api_error_ApiError(status_code=_response.status_code, body=_response.text)
        raise core_api_error_ApiError(status_code=_response.status_code, body=_response_json)

    async def get_checkout_data(
        self,
        *,
        company_id: str,
        selected_plan_id: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> GetCheckoutDataResponse:
        """
        Parameters
        ----------
        company_id : str

        selected_plan_id : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        GetCheckoutDataResponse
            OK

        Examples
        --------
        import asyncio

        from schematic import AsyncSchematic

        client = AsyncSchematic(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.checkout.get_checkout_data(
                company_id="company_id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "checkout-internal/data",
            method="POST",
            json={
                "company_id": company_id,
                "selected_plan_id": selected_plan_id,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    GetCheckoutDataResponse,
                    parse_obj_as(
                        type_=GetCheckoutDataResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 400:
                raise BadRequestError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 401:
                raise UnauthorizedError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 403:
                raise ForbiddenError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 500:
                raise InternalServerError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise core_api_error_ApiError(status_code=_response.status_code, body=_response.text)
        raise core_api_error_ApiError(status_code=_response.status_code, body=_response_json)

    async def preview_checkout_internal(
        self,
        *,
        add_on_ids: typing.Sequence[UpdateAddOnRequestBody],
        company_id: str,
        new_plan_id: str,
        new_price_id: str,
        pay_in_advance: typing.Sequence[UpdatePayInAdvanceRequestBody],
        coupon_external_id: typing.Optional[str] = OMIT,
        payment_method_id: typing.Optional[str] = OMIT,
        promo_code: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> PreviewCheckoutInternalResponse:
        """
        Parameters
        ----------
        add_on_ids : typing.Sequence[UpdateAddOnRequestBody]

        company_id : str

        new_plan_id : str

        new_price_id : str

        pay_in_advance : typing.Sequence[UpdatePayInAdvanceRequestBody]

        coupon_external_id : typing.Optional[str]

        payment_method_id : typing.Optional[str]

        promo_code : typing.Optional[str]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        PreviewCheckoutInternalResponse
            OK

        Examples
        --------
        import asyncio

        from schematic import (
            AsyncSchematic,
            UpdateAddOnRequestBody,
            UpdatePayInAdvanceRequestBody,
        )

        client = AsyncSchematic(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.checkout.preview_checkout_internal(
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


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "checkout-internal/preview",
            method="POST",
            json={
                "add_on_ids": convert_and_respect_annotation_metadata(
                    object_=add_on_ids,
                    annotation=typing.Sequence[UpdateAddOnRequestBody],
                    direction="write",
                ),
                "company_id": company_id,
                "coupon_external_id": coupon_external_id,
                "new_plan_id": new_plan_id,
                "new_price_id": new_price_id,
                "pay_in_advance": convert_and_respect_annotation_metadata(
                    object_=pay_in_advance,
                    annotation=typing.Sequence[UpdatePayInAdvanceRequestBody],
                    direction="write",
                ),
                "payment_method_id": payment_method_id,
                "promo_code": promo_code,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    PreviewCheckoutInternalResponse,
                    parse_obj_as(
                        type_=PreviewCheckoutInternalResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 400:
                raise BadRequestError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 401:
                raise UnauthorizedError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 403:
                raise ForbiddenError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 500:
                raise InternalServerError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise core_api_error_ApiError(status_code=_response.status_code, body=_response.text)
        raise core_api_error_ApiError(status_code=_response.status_code, body=_response_json)

    async def update_customer_subscription_trial_end(
        self,
        subscription_id: str,
        *,
        trial_end: typing.Optional[dt.datetime] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> UpdateCustomerSubscriptionTrialEndResponse:
        """
        Parameters
        ----------
        subscription_id : str
            subscription_id

        trial_end : typing.Optional[dt.datetime]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        UpdateCustomerSubscriptionTrialEndResponse
            OK

        Examples
        --------
        import asyncio

        from schematic import AsyncSchematic

        client = AsyncSchematic(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.checkout.update_customer_subscription_trial_end(
                subscription_id="subscription_id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"subscription/{jsonable_encoder(subscription_id)}/edit-trial-end",
            method="PUT",
            json={
                "trial_end": trial_end,
            },
            headers={
                "content-type": "application/json",
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    UpdateCustomerSubscriptionTrialEndResponse,
                    parse_obj_as(
                        type_=UpdateCustomerSubscriptionTrialEndResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            if _response.status_code == 400:
                raise BadRequestError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 401:
                raise UnauthorizedError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 403:
                raise ForbiddenError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 404:
                raise NotFoundError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            if _response.status_code == 500:
                raise InternalServerError(
                    typing.cast(
                        types_api_error_ApiError,
                        parse_obj_as(
                            type_=types_api_error_ApiError,  # type: ignore
                            object_=_response.json(),
                        ),
                    )
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise core_api_error_ApiError(status_code=_response.status_code, body=_response.text)
        raise core_api_error_ApiError(status_code=_response.status_code, body=_response_json)
