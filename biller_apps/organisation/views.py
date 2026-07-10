import json
import urllib

from django.core.paginator import Paginator
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from biller.constants import Constants
from biller_apps.auth.dataclasses.request.token_payload import Payload
from biller_apps.brand.models import Brand
from biller_apps.category.models import Category
from biller_apps.common.common import Common
from biller_apps.common.dataclasses.get_all import GetAll
from biller_apps.common.dataclasses.search import Search
from biller_apps.common.models.adress import Address
from biller_apps.common.publish import Publish
from biller_apps.common.utils import Utils
from biller_apps.customer.models import Customer
from biller_apps.organisation.dataclasses.request.create import OrganisationRequest
from biller_apps.organisation.dataclasses.request.delete import OrganisationDelete
from biller_apps.organisation.dataclasses.request.delete_many import OrganisationDeleteManyRequest
from biller_apps.organisation.dataclasses.request.get import OrganisationGet
from biller_apps.organisation.es_query import OrganisationEsQuery
from biller_apps.organisation.models import Organisation
from biller_apps.organisation.models import Version
from biller_apps.organisation.utils import OrganisationUtils
from biller_apps.supplier.models import Supplier
from biller_apps.taxes.models import Taxes


class OrganisationViews:
    def __init__(self) -> None:
        self.fetch_data = "Data fetched successfully"
        self.delete_data = "Organisation delete successfully"
        self.update_data = "Organisation updated successfully"
        self.created_data = "Organisation added successfully"
        self.duplicate_error = "Duplicate Key found please try with different name"
        self.get_error = "Provided Key doesnt exist"
        self.data_created = "Version created successfully"
        super().__init__()

    @Common().exception_handler
    @Publish.status_update
    def create_extract(self, params: OrganisationRequest) -> Response:
        if Organisation().get(company_name=params.name, single=True):
            raise ValueError(self.duplicate_error)
        with transaction.atomic():
            address_id = Address().create(street=params.street, state=params.state, country=params.country)
            organisation_id = Organisation().create(owner_name=params.owner_name, company_name=params.name,
                                                    owner_mobile=params.owner_mobile,
                                                    owner_email=params.owner_email,
                                                    shop_count=params.shop_count,
                                                    employee_count=params.employee_count,
                                                    approval=params.approval, plan=params.plan,
                                                    plan_expiry=params.plan_expiry,
                                                    owner_alternate_mobile=params.owner_alternate_mobile,
                                                    address_id=address_id)
            Supplier().create(name="No Supplier", mobile_number=params.owner_mobile,
                              organisation_name=params.name,
                              address_id=address_id, alt_mobile_number="", id_type="PAN", id_number="1234567890",
                              email_id="nosupplier@" + params.name + ".org", photo_url="", id_proof_url="", secure=True,
                              gst_number="1234567890", organisation_id=organisation_id)
            Customer().create(name="No Customer", mobile_number=params.owner_mobile,
                              organisation_name=params.name,
                              organisation_id=organisation_id, address_id=address_id, secure=True)
            Brand().create(name="No Brand", organisation_name=params.name, organisation_id=organisation_id, secure=True)
            Category().create(name="No Category", organisation_name=params.name, organisation_id=organisation_id,
                              secure=True)
            Taxes().create(name="No Tax", total_tax=0.0, tax_splits={'cgst': 0.0, 'sgst': 0.0},
                           organisation_id=organisation_id, organisation_name=params.name, secure=True)

        return Response(status=status.HTTP_201_CREATED, data=Utils.success_response_data(message=self.created_data))

    @Common().exception_handler
    def get_extract(self, params: OrganisationGet) -> Response:
        data = Organisation.get(company_name=params.name)
        if len(data) == 0:
            raise ValueError(self.get_error)
        organisation_utils = OrganisationUtils(columns_required=params.values_list)
        data = json.loads(organisation_utils.mapper(data=data))[0]
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.fetch_data, data=data))

    @Common().exception_handler
    def get_all_extract(self, params: GetAll, token_payload: Payload) -> Response:
        pages = Paginator(Organisation.get_all(organisation_name=token_payload.organisationName, params=params), params.limit)
        if pages.num_pages < params.page_num:
            raise ValueError(Constants.page_num_exceeded)
        data = pages.page(params.page_num)
        organisation_utils = OrganisationUtils(columns_required=params.values_list)
        data = json.loads(organisation_utils.mapper(data=data))

        data = Utils.add_page_parameter(final_data=data, page_num=params.page_num,
                                        present_url=token_payload.present_url,
                                        total_page=pages.num_pages, total_count=pages.count,
                                        next_page_required=True if pages.num_pages != params.page_num else False)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.fetch_data, data=data))

    @Common().exception_handler
    @Publish.status_update
    def delete_extract(self, params: OrganisationDelete) -> Response:
        organisation = Organisation.objects.filter(company_name=urllib.parse.unquote(params.name)).values(
            'organisation_id').first()
        if organisation is None:
            raise ValueError(self.duplicate_error)
        with transaction.atomic():
            Organisation.remove(organisation_id=organisation['organisation_id'])
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.delete_data))

    @Common().exception_handler
    @Publish.status_update
    def delete_many_extract(self, params: OrganisationDeleteManyRequest, token_payload: Payload):
        category_ids = params.organisation_id
        with transaction.atomic():
            Organisation().remove_from_list(organisation_ids=category_ids)
        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.delete_data))

    @Common().exception_handler
    @Publish.status_update
    def update_extract(self, params: OrganisationRequest) -> Response:
        organisation_data = Organisation.get(company_name=urllib.parse.unquote(params.name), single=True)
        if organisation_data is None:
            raise ValueError(self.get_error)

        with transaction.atomic():
            Organisation.update(owner_name=params.owner_name, owner_mobile=params.owner_mobile, company_name=params.name,
                                organisation_id=organisation_data['organisation_id'], shop_count=params.shop_count,
                                employee_count=params.employee_count, approval=params.approval, plan=params.plan,
                                plan_expiry=params.plan_expiry,owner_email=params.owner_email,owner_alternate_mobile=params.owner_alternate_mobile)

        return Response(status=status.HTTP_200_OK, data=Utils.success_response_data(message=self.update_data))

    @Common().exception_handler
    def search_extract(self, params: Search, token_payload: Payload):
        data = OrganisationEsQuery.search_pattern_start_with_query(request_keys=params.key,organisation_id=token_payload.organisation_id)
        return Response(
            status=status.HTTP_200_OK,
            data=Utils.success_response_data(message=self.fetch_data, data=data)
        )

    @Common().exception_handler
    def create_version_extract(self, params:Version):
        Version.create_version(
            repo_url=params.repo_url,
            file_name=params.file_name,
            minimum_version=params.minimum_version,
            latest_stable_version=params.latest_stable_version,
            previous_stable_version=params.previous_stable_version,
            beta_version=params.beta_version if params.beta_version else None,
            other_versions=params.other_versions if params.other_versions else None,
            changes_in_latest_stable=params.changes_in_latest_stable
        )

        return Response(
            status=status.HTTP_201_CREATED,
            data=Utils.success_response_data(
                message=self.data_created
            )
        )
