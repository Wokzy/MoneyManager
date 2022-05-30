from django.db import models

"""
class User(models.Model):
	name = models.CharField('Name', max_length = 32)
	password = models.CharField('Name', max_length = 256)
"""
class Account(models.Model):
	#user = models.ForeignKey(User, on_delete = models.CASCADE)
	account_name = models.CharField('name of your account', max_length = 32)
	account_value = models.IntegerField('value', default=0)
	beginning_value = models.IntegerField('value', default=0)
	account_value_fraction = models.IntegerField('value', default=0)
	last_change = models.DateTimeField('date of last change', null=True)

	def __str__(self):
		return self.account_name

	def test(self):
		return True

class Category(models.Model):
	#user = models.ForeignKey(User, on_delete = models.CASCADE)
	name = models.CharField('Name of category', max_length = 64)
	is_income = models.BooleanField('Is this income category')
	changed_value = models.IntegerField('changed_value', default=0)
	changed_value_fraction = models.IntegerField('changed_value_fraction', default=0)

class Change(models.Model):
	#user = models.ForeignKey(User, on_delete = models.CASCADE)
	account = models.ForeignKey(Account, on_delete = models.CASCADE, related_name='%(class)s_account')
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
	is_income = models.BooleanField('Is this change income')
	comment = models.CharField('Name for change', max_length = 64, default='No comment')
	amount = models.IntegerField('value')
	amount_fraction = models.IntegerField('value', default=0)
	date = models.DateTimeField('date')
	transfer = models.BooleanField('If transfer', default=False)
	transfer_getter = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True , related_name='%(class)s_transfer_getter')


"""
CASCADE
SET_NULL
SET_DEFAULT
SET(...): Set a given value
DO_NOTHING
"""
