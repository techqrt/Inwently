from django.db import models

class DashboardPermission(models.Model):
    permission_id = models.AutoField(primary_key=True)
    dashboard = models.BooleanField(default=False, null=True)

    class Meta:
        db_table = 'dashboard_permissions'

    
    def create(self, dashboard: bool):
        self.dashboard = dashboard
        self.save()
        return self.permission_id
    
    @staticmethod
    def update(permission_id: int, dashboard: bool):

        instance = DashboardPermission.objects.get(permission_id=permission_id)
        
        instance.dashboard = dashboard
        
        instance.save()
        
        return instance.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        DashboardPermission.objects.get(permission_id=permission_id).delete()


class MasterDataPermission(models.Model):
    permission_id = models.AutoField(primary_key=True)
    item = models.BooleanField(default=False, null=True)
    supplier = models.BooleanField(default=False, null=True)
    shop = models.BooleanField(default=False, null=True)
    customer = models.BooleanField(default=False, null=True)
    employee = models.BooleanField(default=False, null=True)
    creating = models.BooleanField(default=False, null=True)

    class Meta:
        db_table = 'master_data_permissions'

    def create(self, item: bool, supplier: bool, shop: bool, customer: bool, employee: bool, create: bool):
        self.item = item
        self.supplier = supplier
        self.shop = shop
        self.customer = customer
        self.employee = employee
        self.creating = create
        self.save()
        return self.permission_id

    @staticmethod
    def update(permission_id: int, item: bool, supplier: bool, shop: bool, customer: bool, employee: bool, create: bool):
        
        instance = MasterDataPermission.objects.get(permission_id=permission_id)
        
        
        instance.item = item
        instance.supplier = supplier
        instance.shop = shop
        instance.customer = customer
        instance.employee = employee
        instance.creating = create
        
        
        instance.save()
        
        
        return instance.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        MasterDataPermission.objects.get(permission_id=permission_id).delete()


class InventoryPermission(models.Model):
    permission_id = models.AutoField(primary_key=True)
    inventory = models.BooleanField(default=False, null=True)

    class Meta:
        db_table = 'inventory_permissions'

    def create(self, inventory: bool):
        self.inventory = inventory
        self.save()
        return self.permission_id

    @staticmethod
    def update(permission_id: int, inventory: bool):
        
        instance = InventoryPermission.objects.get(permission_id=permission_id)
        
        
        instance.inventory = inventory
        
        
        instance.save()
        
        
        return instance.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        InventoryPermission.objects.get(permission_id=permission_id).delete()


class DispatchPermission(models.Model):
    permission_id = models.AutoField(primary_key=True)
    dispatch = models.BooleanField(default=False, null=True)

    class Meta:
        db_table = 'dispatch_permissions'

    def create(self, dispatch: bool):
        self.dispatch = dispatch
        self.save()
        return self.permission_id

    @staticmethod
    def update(permission_id: int, dispatch: bool):

        instance = DispatchPermission.objects.get(permission_id=permission_id)

        instance.dispatch = dispatch

        instance.save()

        return instance.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        DispatchPermission.objects.get(permission_id=permission_id).delete()


class SalesPermission(models.Model):
    permission_id = models.AutoField(primary_key=True)
    pos = models.BooleanField(default=False, null=True)
    return_item = models.BooleanField(default=False, null=True)
    bill_history = models.BooleanField(default=False, null=True)

    class Meta:
        db_table = 'sales_permissions'

    def create(self, pos: bool, return_item: bool, bill_history: bool) -> int:
        self.pos = pos
        self.return_item = return_item
        self.bill_history = bill_history
        self.save()
        return self.permission_id

    @staticmethod
    def update(permission_id: int, pos: bool, return_item: bool, bill_history: bool) -> int:
        
        sales_permission = SalesPermission.objects.get(permission_id=permission_id)
        
        
        sales_permission.pos = pos
        sales_permission.return_item = return_item
        sales_permission.bill_history = bill_history
        
        
        sales_permission.save()
        
        
        return sales_permission.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        SalesPermission.objects.get(permission_id=permission_id).delete()


class QuotationsPermission(models.Model):
    permission_id = models.AutoField(primary_key=True)
    quotations = models.BooleanField(default=False, null=True)

    class Meta:
        db_table = 'quotations_permissions'

    def create(self, quotations: bool):
        self.quotations = quotations
        self.save()
        return self.permission_id
    
    @staticmethod
    def update(permission_id: int, quotations: bool) -> int:
        
        quotations_permission = QuotationsPermission.objects.get(permission_id=permission_id)
        
        
        quotations_permission.quotations = quotations
        
        
        quotations_permission.save()
        
        
        return quotations_permission.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        QuotationsPermission.objects.get(permission_id=permission_id).delete()


class PrinterTemplatesPermission(models.Model):
    permission_id = models.AutoField(primary_key=True)
    printer_templates = models.BooleanField(default=False, null=True)

    class Meta:
        db_table = 'printer_templates_permissions'
    

    def create(self, printer_templates: bool):
        self.printer_templates = printer_templates
        self.save()
        return self.permission_id
    
    @staticmethod
    def update(permission_id: int, printer_templates: bool) -> int:
        
        printer_templates_permission = PrinterTemplatesPermission.objects.get(permission_id=permission_id)
        
        
        printer_templates_permission.printer_templates = printer_templates
        
        
        printer_templates_permission.save()
        
        
        return printer_templates_permission.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        PrinterTemplatesPermission.objects.get(permission_id=permission_id).delete()


class PurchasePermission(models.Model):
    permission_id = models.AutoField(primary_key=True)
    purchase_list = models.BooleanField(default=False, null=True)
    return_purchase = models.BooleanField(default=False, null=True)
    stock = models.BooleanField(default=False, null=True)

    class Meta:
        db_table = 'purchase_permissions'
    

    def create(self, purchase_list: bool, return_purchase: bool, stock: bool):
        self.purchase_list = purchase_list
        self.return_purchase = return_purchase
        self.stock = stock
        self.save()
        return self.permission_id
    
    @staticmethod
    def update(permission_id: int, purchase_list: bool, return_purchase: bool, stock: bool) -> int:
        
        purchase_permission = PurchasePermission.objects.get(permission_id=permission_id)
        
        
        purchase_permission.purchase_list = purchase_list
        purchase_permission.return_purchase = return_purchase
        purchase_permission.stock = stock
        
        
        purchase_permission.save()
        
        
        return purchase_permission.permission_id

    @staticmethod
    def remove(permission_id: int) -> None:
        PurchasePermission.objects.get(permission_id=permission_id).delete()


class ReportsPermission(models.Model):
    permission_id = models.AutoField(primary_key=True)
    general = models.BooleanField(default=False, null=True)
    overview = models.BooleanField(default=False, null=True)
    administration = models.BooleanField(default=False, null=True)
    day_book = models.BooleanField(default=False, null=True)
    gst = models.BooleanField(default=False, null=True)

    class Meta:
        db_table = 'reports_permissions'
    
    
    def create(self, general: bool, overview: bool, administration: bool, day_book: bool, gst: bool):
        self.general = general
        self.overview = overview
        self.administration = administration
        self.day_book = day_book
        self.gst = gst
        self.save()
        return self.permission_id
    
    @staticmethod
    def update(permission_id: int, general: bool, overview: bool, administration: bool, day_book: bool, gst: bool) -> int:
        
        reports_permission = ReportsPermission.objects.get(permission_id=permission_id)
        
        
        reports_permission.general = general
        reports_permission.overview = overview
        reports_permission.administration = administration
        reports_permission.day_book = day_book
        reports_permission.gst = gst
        
        
        reports_permission.save()
        
        
        return reports_permission.permission_id
    
    @staticmethod
    def remove(permission_id: int) -> None:
        ReportsPermission.objects.get(permission_id=permission_id).delete()
