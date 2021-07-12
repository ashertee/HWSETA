from odoo import _, api, fields, models

class Learners(models.Model):
	_name = 'hwseta.learners'

	def _check_id(self):
		p =self.env['hwseta.learners'].search([])
		self.id_check = ''
		for each in p:
			if each.id_number == self.id_number:
				self.id_check = f"Duplicate ID {self.id_number} for learner {each.name}"
			else:
				self.id_check = 'OK'
		return self.id_check

	name = fields.Char()
	id_number = fields.Char()
	qualifications = fields.Char()
	id_check = fields.Char(compute=_check_id)



class Qualifications(models.Model):
	_name = 'hwseta.qualifications'

	@api.depends('units')
	def _get_total_credits(self):
		total_credit = 0
		x = {}
		for credit in self:
			x = (credit.units.read())
			for i in x:
				credit.total_credit = credit.total_credit + i['credit']
		return credit.total_credit

	name = fields.Char()
	# min credit required to pass
	min_credit = fields.Integer()
	units = fields.Many2many('hwseta.units')
	total_credit = fields.Integer(compute=_get_total_credits)


class Units(models.Model):
	_name = 'hwseta.units'

	name = fields.Char()
	credit = fields.Integer()

class LearnerQualifications(models.Model):
	_name = 'learner.qualifications'

	def _get_status(self):
		passed = False
		if self.achieved_units >= self.required_credit:
			passed = True
		return passed

	qualification = fields.Many2one('hwseta.qualifications')
	learner = fields.Many2one('hwseta.learners')
	units = fields.Many2many('hwseta.units', related='qualification.units')
	learner_achieve = fields.Many2many('learner.units')
	achieved_units = fields.Integer(string = 'Achieved Credit', related='learner_achieve.total_achieved')
	required_credit = fields.Integer(string = 'Minimum credit Required', related='qualification.min_credit')
	Pass = fields.Boolean()
	passed = fields.Boolean(string="Qualification Status", compute=_get_status)




class LearnerUnits(models.Model):
	_name = 'learner.units'

	@api.depends('master_unit')
	def _get_achieved_credits(self):
		x = {}
		for credit in self:
			x = (credit.master_unit.read())
			for i in x:
				credit.total_achieved = i['credit']*len(self)
		return credit.total_achieved

	master_unit = fields.Many2one('hwseta.units')
	learner = fields.Many2one('hwseta.learners')
	total_achieved = fields.Integer(compute=_get_achieved_credits)
	achieved = fields.Boolean()

