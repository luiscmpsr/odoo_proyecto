 {
    'name': 'TCU Management System',
    'depends': ["base", "mail"],  # <-- mail es obligatorio para mail.mail
    'sequence':1,
    'data':[
                "security\\ir.model.access.csv",
                "views\\tcu_periodo.xml",
                "views\\tcu_estudiante.xml",
                "views\\tcu_solicitud.xml",
                "views\\tcu_management_menus.xml"
            ]
}
