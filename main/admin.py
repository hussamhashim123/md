import csv
from django.contrib import admin
from .models import Department, Person, Item, Menu
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponse


# Register your models here.
admin.site.site_header = "System"
admin.site.site_title = "System"
admin.site.index_title = "Welcome to System"

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = [
        "department_id",
        "name",
    ]
    search_fields = ["department_id", "name"]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = [
        "person_id",
        "folder_id",
        "name",
        "debtor",
        "p_num",
        "kind_file",
        "department",
        "note",
    ]
    search_fields = [
        "person_id",
        "name",
        "folder_id",
        "debtor",
        "p_num",
        "kind_file",
    ]


class ItemInline(admin.TabularInline):
    model = Item
    extra = 0
    fields = [
        "person",
        "menu",
        "money",
        "tax",
        "total",
    ]
    readonly_fields = ["tax", "total"]


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ["menu_id", "department", "month"]
    search_fields = ["menu_id", "month", "department__name"]
    inlines = [ItemInline]

    class Media:
        js = ["/static/admin/js/vendor/jquery/jquery.min.js", "admin/total.js"]
        css = {"all": ["admin/row-counter.css"]}

    def export_to_pdf(self, request, id):
        menu = Menu.objects.get(menu_id=id)
        return render(request, "pdf_form.html", {"menu": menu})

    def export_to_csv(self, request, id):
        menu = Menu.objects.get(menu_id=id)
        items = menu.item_set.all()

        total_money = sum(item.money for item in items)
        total_tax = sum(item.tax for item in items)
        total_total = sum(item.total for item in items)

        response = HttpResponse(content_type='text/csv', charset='utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="menu_data.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "Menu ID",
                "Department",
                "Month",
                "Folder ID",
                "Name",
                "Debtor",
                "Privet Number",
                "Kind File",
                "Money",
                "Tax",
                "Total",
            ]
        )

        for item in menu.item_set.all():
            writer.writerow(
                [
                    menu.menu_id,
                    menu.department.name,
                    menu.month,
                    item.person.folder_id,
                    item.person.name,
                    item.person.debtor,
                    item.person.p_num,
                    item.person.kind_file,
                    item.money,
                    item.tax,
                    item.total,
                ]
            )
        writer.writerow([])
        writer.writerow(
            ["Total", "", "", "", "", "", "", "", total_money, total_tax, total_total]
        )

        return response


    def get_urls(self):
        return super().get_urls() + [
            path("<int:id>/print", self.export_to_pdf, name="print"),
            path("<int:id>/export", self.export_to_csv, name="export"),
        ]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    search_fields = [
        "person__name",
        "menu__menu_id",
        "person__debtor",
        "person__folder_id",
        "menu__month",
        "menu__department__name",
    ]
    list_filter = [
        "person",
        "menu__menu_id",
        "person__debtor",
        "person__folder_id",
        "menu__month",
        "menu__department",
    ]
    list_display = [
        "id",
        "money",
        "tax",
        "total",
        "person_name",
        "person_folder_id",
        "person_debtor",
        "department_name",
        "menu_id",
        "menu_month",
    ]

    def person_name(self, obj):
        if obj:
            return obj.person.name
        else:
            return None

    def person_folder_id(self, obj):
        if obj:
            return obj.person.folder_id
        else:
            return None

    def person_debtor(self, obj):
        if obj:
            return obj.person.debtor
        else:
            return None

    def department_name(self, obj):
        if obj:
            return obj.menu.department.name
        else:
            return None

    def menu_month(self, obj):
        if obj:
            return obj.menu.month
        else:
            return None

    def menu_id(self, obj):
        if obj:
            return obj.menu.menu_id
        else:
            return None

    actions = ["export_pdf"]

    @admin.action(description="Export to PDF")
    def export_pdf(self, request, queryset):
        return render(request, "items_form.html", {"items": queryset})
