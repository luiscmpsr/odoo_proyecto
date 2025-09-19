from odoo import fields,models

class TCUEstudiante(models.Model):
    _name = "tcu.estudiante"
    _description = "TCU Estudiante"
    
    est_nombre         = fields.Char(string="Nombre",         required=True)
    est_identificacion = fields.Char(string="Identificación", required=True)
    est_carnet         = fields.Char(string="Carnet",         required=True)
    est_correo         = fields.Char(string="Correo",         required=True)
    est_telefono       = fields.Char(string="Teléfono",       required=True)

