from django.shortcuts import render
from django.http import  Http404, HttpResponseRedirect
from .models import Account, Change, Category
from django.utils import timezone
from django.urls import reverse
from . import constants
from datetime import datetime


def get_date(request):
	date_string = request.POST['date'][2::] + ' ' + request.POST['time']
	return datetime.strptime(date_string, '%y-%m-%d %H:%M')

def value_operation(account, val, typ='add'): #add substract
	value = '%.2f' % eval(val)
	amount = int(value.split('.')[0])
	amount_fraction = 0

	if len(value.split('.')) > 1:
		amount_fraction = int(value.split('.')[1])

	if typ == 'add':
		account.account_value += amount
		account.account_value_fraction += amount_fraction
		if account.account_value_fraction >= 100:
			account.account_value_fraction -= 100
			account.account_value += 1
	elif typ == 'substract':
		account.account_value -= amount
		account.account_value_fraction -= amount_fraction
		if account.account_value_fraction < 0:
			account.account_value_fraction += 100
			account.account_value -= 1

	account.save()
	return (amount, amount_fraction)

def check_categories():
	categories = Category.objects.all()
	if len(categories) == 0:
		Category.objects.create(name=constants.noname_income_category, is_income=True, changed_value=0)
		Category.objects.create(name=constants.noname_spend_category, is_income=False, changed_value=0)

def check_changes():
	changes = Change.objects.all()

	for change in changes:
		if change.category == None:
			if change.is_income:
				category = Category.objects.get(name = constants.noname_income_category)
			else:
				category = Category.objects.get(name = constants.noname_spend_category)

			change.category = category
			change.save()

def index(request):
	check_categories()
	accounts_list = Account.objects.all()
	categories = Category.objects.all()
	last_five_changes = Change.objects.all()[max(len(Change.objects.all())-5, 0)::-1]
	last_month_changes = Change.objects.filter(date__month = datetime.now().month)[::-1]
	#print(accounts_list)
	all_cash = 0
	for i in accounts_list:
		all_cash += i.account_value
		all_cash += float(f'0.{i.account_value_fraction}')
	all_cash = '%.2f' % all_cash
	return render(request, 'MoneyManager/list.html', {'accounts_list':accounts_list, 'all_cash':all_cash, 
		'categories':categories, 'last_five_changes':last_five_changes, 'last_month_changes':last_month_changes})

def accounts_categories_changes(request):
	accounts_list = Account.objects.all()
	categories = Category.objects.all()
	last_five_changes = Change.objects.all()[max(len(Change.objects.all())-5, 0)::-1]

	all_cash = 0
	for i in accounts_list:
		all_cash += i.account_value
		all_cash += float(f'0.{i.account_value_fraction}')
	all_cash = '%.2f' % all_cash

	return render(request, 'MoneyManager/accounts_categories_changes.html', {'accounts_list':accounts_list, 'all_cash':all_cash, 'categories':categories, 'last_five_changes':last_five_changes})

def detail(request, account_id):
	try:
		a = Account.objects.get(id = account_id)
	except:
		raise Http404('account not found')

	income_categories = Category.objects.filter(is_income=True)
	spend_categories = Category.objects.filter(is_income=False)
	changes_list = (list(Change.objects.filter(account=a)) + list(Change.objects.filter(transfer_getter=a)))[::-1]

	return render(request, 'MoneyManager/detail.html', {'account': a, 'changes_list':changes_list, "income_categories":income_categories, 'spend_categories':spend_categories})

def detail_categories(request, category_id):
	try:
		category = Category.objects.get(id = category_id)
	except:
		raise Http404('something wrong with category')
	changes = Change.objects.filter(category = category)[::-1]

	return render(request, 'MoneyManager/detail_categories.html', {'category':category, 'changes':changes, 'constants':constants})

def remove_category(request, category_id):
	try:
		category = Category.objects.get(id = category_id)
	except:
		raise Http404('something wrong with category')

	if category.is_income:
		default = Category.objects.get(name = constants.noname_income_category, is_income=True)
	else:
		default = Category.objects.get(name = constants.noname_spend_category, is_income=False)
	default.changed_value += category.changed_value
	default.save()

	category.delete()
	check_changes()
	return HttpResponseRedirect('/MoneyManager/accounts_categories_changes')

def add_change(request):
	try:
		a = Account.objects.get(id = int(request.POST['account']))
	except:
		raise Http404('account not found')

	date = get_date(request)
	value = '%.2f' % eval(request.POST['value'])
	amount = int(value.split('.')[0])
	if len(value.split('.')) > 1:
		amount_fraction = int(value.split('.')[1])
	else:
		amount_fraction = 0

	category = Category.objects.get(id=request.POST['category'])
	if not category.is_income:
		amount = -amount

	category.changed_value += amount
	category.changed_value_fraction += amount_fraction
	
	if category.changed_value_fraction >= 100:
		category.changed_value += 1
		category.changed_value_fraction -= 100

	a.account_value += amount
	a.account_value_fraction += amount_fraction

	if a.account_value_fraction >= 100:
		a.account_value += 1
		a.account_value_fraction -= 100

	a.last_change = date
	Change.objects.create(account=a, category=category, is_income=category.is_income, comment = request.POST['comment'], amount = amount, amount_fraction=amount_fraction, date=date)
	
	a.save()
	category.save()

	return HttpResponseRedirect('/MoneyManager')

def create_account(request):
	Account.objects.create(account_name=request.POST['name'], account_value=request.POST['value'])
	return HttpResponseRedirect('/MoneyManager/accounts_categories_changes')

def remove_account(request, account_id):
	try:
		a = Account.objects.get(id=account_id)

	except:
		return HttpResponseRedirect('/MoneyManager/accounts_categories_changes')

	for change in Change.objects.filter(account=a):
		change.category.changed_value -= change.amount
		change.category.save()
		change.save()

	a.delete()

	return HttpResponseRedirect('/MoneyManager/accounts_categories_changes')

def create_category(request):
	Category.objects.create(name=request.POST['name'], is_income=bool(int(request.POST['income'])))
	return HttpResponseRedirect('/MoneyManager/accounts_categories_changes')

def transfer(request):
	if request.POST['from'] == request.POST['to']:
		return HttpResponseRedirect('/MoneyManager/')

	account_from = Account.objects.get(id=int(request.POST['from']))
	account_to = Account.objects.get(id=int(request.POST['to']))

	substract = value_operation(account_from, request.POST['value'], 'substract')
	add = value_operation(account_to, request.POST['value'], 'add')

	date = timezone.now() # get_date(request)

	Change.objects.create(account=account_from, is_income=False, comment=request.POST['comment'], amount=substract[0],
		amount_fraction=substract[1], date=date, transfer=True, transfer_getter=account_to)

	return HttpResponseRedirect('/MoneyManager/')