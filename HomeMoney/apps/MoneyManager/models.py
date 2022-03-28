from django.db import models

class Account(models.Model):
	account_name = models.CharField('name of your account', max_length = 32)
	account_value = models.IntegerField('value')
	account_value_fraction = models.IntegerField('value', default=0)
	last_change = models.DateTimeField('date of last change', null=True)

	def __str__(self):
		return self.account_name

	def test(self):
		return True

class Category(models.Model):
	name = models.CharField('Name of category', max_length = 64)
	is_income = models.BooleanField('Is this income category')
	changed_value = models.IntegerField('changed_value', default=0)
	changed_value_fraction = models.IntegerField('changed_value_fraction', default=0)

class Change(models.Model):
	account = models.ForeignKey(Account, on_delete = models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
	is_income = models.BooleanField('Is this change income')
	comment = models.CharField('Name for change', max_length = 64, default='No comment')
	amount = models.IntegerField('value')
	amount_fraction = models.IntegerField('value', default=0)
	date = models.DateTimeField('date')


"""
CASCADE
SET_NULL
SET_DEFAULT
SET(...): Set a given value
DO_NOTHING
"""
