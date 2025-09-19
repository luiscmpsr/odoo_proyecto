from odoo import fields,models
from datetime import datetime

class TCUPeriodo(models.Model):
    _name = "tcu.periodo"
    _description = "TCU Periodo"
    
    per_nombre      = fields.Char(string="Nombre",       required=True)
    per_activo      = fields.Boolean(string="Activo",    required=True)
    per_anno        = fields.Selection(string="Año",     required=True, selection=_get_year_selection)
    per_fechainicio = fields.Date(string="Fecha Inicio", required=True)
    per_fechaFinal  = fields.Date(string="Fecha Final",  required=True)
        
    # Me da el año actual más los 5 siguientes
    def _get_year_selection(self):
        actual = datetime.today().year
        return [(str(y), str(y)) for y in range(actual, actual + 5)]