from dataclasses import dataclass

@dataclass
class PermissionsMaster:
    item: bool
    shop: bool
    supplier: bool
    customer: bool
    create: bool
    employee: bool

@dataclass
class PermissionsInventory:
    inventory: bool

@dataclass
class SalesPermission:
    pos: bool
    return_item: bool
    bill_history: bool

@dataclass
class QuotationsPermission:
    quotations: bool

@dataclass
class PrinterTemplatesPermission:
    printer_templates: bool

@dataclass
class PurchasePermission:
    purchase_list: bool
    return_purchase: bool
    stock: bool


@dataclass
class PermissionsReports:
    general: bool
    overview: bool
    administration: bool
    day_book: bool
    gst: bool

@dataclass
class PermissionsDashboard:
    dashboard: bool



@dataclass
class Permissions:
    master: PermissionsMaster
    inventory: PermissionsInventory
    billing: SalesPermission
    reports: PermissionsReports
    printer_templates: PrinterTemplatesPermission
    dashboard: PermissionsDashboard
    stock: PurchasePermission
    quotations: QuotationsPermission


@dataclass
class EmployeesRequest:
    name: str
    mobile_number: str
    alternate_mobile_number: str
    dob: str
    shop_access: list
    email_id: str
    state: str
    country: str
    street: str
    profile_photo_url: str
    permissions: Permissions
