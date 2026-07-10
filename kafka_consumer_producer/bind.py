# from rest_framework.request import Request
#
# from biller_apps.brand.views import BrandView
# from biller_apps.employees.views import EmployeesView
# from biller_apps.item.views import ItemView
# from biller_apps.organisation.views import OrganisationViews
# from biller_apps.shops.views import ShopsView
#
#
# class Binder:
#
#     @staticmethod
#     def bind(key: str, request: Request, uuid: str):
#         binder_dict = {
#             'OrganisationViews().create(request)': OrganisationViews().create_extract,
#             'OrganisationViews().delete(request)': OrganisationViews().create_extract,
#             'OrganisationViews().update(request)': OrganisationViews().create_extract,
#             'ShopsView().create(request)': ShopsView().create_extract,
#             'ShopsView().delete(request)': ShopsView().create_extract,
#             'ShopsView().update(request)': ShopsView().create_extract,
#             'EmployeesView().create(request)': EmployeesView().create_extract,
#             'EmployeesView().update(request)': EmployeesView().create_extract,
#             'EmployeesView().delete(request)': EmployeesView().create_extract,
#             'ItemView().create(request)': ItemView().create_extract,
#             'BrandView().delete(request)': BrandView().create_extract,
#             'BrandView().create(request)': BrandView().create_extract
#         }
#         request.uuid = uuid
#         return binder_dict[key](request)
