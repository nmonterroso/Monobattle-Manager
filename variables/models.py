from django.db import models


class Variable(models.Model):
	name = models.CharField(max_length=64, primary_key=True)
	value = models.CharField(max_length=255)

	def __unicode__(self):
		return self.name

	@staticmethod
	def get(name, default_value='', type='str'):
		try:
			var = Variable.objects.get(name=name)
			return Variable.format_output(var.value, type)
		except:
			return default_value

	@staticmethod
	def get_int(name, default_value=0):
		return Variable.get(name, default_value, "int")

	@staticmethod
	def get_bool(name, default_value=False):
		return Variable.get(name, default_value, "bool")

	@staticmethod
	def get_decimal(name, default_value=0):
		return Variable.get(name, default_value, 'decimal')

	@staticmethod
	def set(name, value):
		var = Variable(name=name, value=value)
		var.save()

	@staticmethod
	def format_output(value, type="str"):
		try:
			if type == "bool":
				if value == "True":
					return True
				else:
					return False
			elif type == "int":
				return int(value)
			elif type == 'decimal':
				return Decimal(value)
			else:
				return str(value)
		except:
			return str(value)