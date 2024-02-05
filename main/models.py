from django.db import models

# Create your models here.


class Department(models.Model):
    department_id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "الدوائرة"
        verbose_name_plural = "الدوائرة"


class Person(models.Model):
    person_id = models.AutoField(primary_key=True, editable=False)
    folder_id = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    debtor = models.CharField(max_length=150)
    p_num = models.CharField(max_length=32)
    kind_file = models.CharField(max_length=150)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    note = models.TextField()

    def __str__(self) -> str:
        return self.debtor

    class Meta:
        verbose_name = "الاضبارة"
        verbose_name_plural = "الاضبارة"


class Item(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name="اسم الدائن")
    menu = models.ForeignKey("Menu", on_delete=models.CASCADE)
    money = models.IntegerField(verbose_name="المبلغ")

    @property
    def tax(self):
        if self.money is not None:
            if (self.money * 0.03) % 1 == 0:
                return int(self.money * 0.03)
            return round(self.money * 0.03, 2)
        return None

    tax.fget.short_description = "الرسم"

    @property
    def total(self):
        if self.money is not None:
            if (self.money + self.tax) % 1 == 0:
                return int(self.money - self.tax)
            return round(self.money - self.tax, 2)
        return None

    total.fget.short_description = "الامانة"

    def __str__(self) -> str:
        return self.person.name

    class Meta:
        verbose_name = "الاسماء"
        verbose_name_plural = "الاسماء"


class Menu(models.Model):
    menu_id = models.AutoField(primary_key=True, editable=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    month = models.DateField()

    class Meta:
        verbose_name = "القوائم"
        verbose_name_plural = "القوائم"
