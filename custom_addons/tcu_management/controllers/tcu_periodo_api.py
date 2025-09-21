from odoo import http
from odoo.http import request, Response
import json

class PeriodoAPI(http.Controller):
    @http.route('/api/get_periodos_api', type='http', auth='public', methods=['GET'], csrf=False)
    def get_periodos(self, **kwargs):
        """
        Devuelve una lista de nombres de todos los periodos.
        """
        periodos = request.env['tcu.periodo'].sudo().search([])

        if not periodos:
            return json.dumps({"error": "No existen periodos registrados"})

        lista_nombres = [p.per_nombre for p in periodos]

        #return json.dumps(lista_nombres, ensure_ascii=False)
        return Response(
                    json.dumps(lista_nombres, ensure_ascii=False),
                    content_type='application/json',
                    headers={'Access-Control-Allow-Origin': '*'}
        )

    @http.route('/api/get_periodoinfo_api', type='http', auth='public', methods=['GET'], csrf=False)
    def get_periodo_info(self, **kwargs):
        """
        Devuelve la información de un periodo específico por nombre.
        """
        nombre = kwargs.get("nombre")
        if not nombre:
            return json.dumps({"error": "Debe indicar el nombre del periodo como parámetro 'nombre'"})

        periodo = request.env['tcu.periodo'].sudo().search([('per_nombre', '=', nombre)], limit=1)
        if not periodo:
            return json.dumps({"error": f"No existe un periodo con nombre '{nombre}'"})

        data = {
            "nombre": periodo.per_nombre,
            "activo": periodo.per_activo,
            "anno": periodo.per_anno,
            "fecha_inicio": str(periodo.per_fechainicio),
            "fecha_final": str(periodo.per_fechaFinal),
        }

        #return json.dumps(data, ensure_ascii=False)
        return Response(
                    json.dumps(data, ensure_ascii=False),
                    content_type='application/json',
                    headers={'Access-Control-Allow-Origin': '*'}
        )
