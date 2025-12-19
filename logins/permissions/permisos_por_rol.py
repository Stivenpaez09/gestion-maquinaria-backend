ROLE_PERMISSIONS = {
    "ADMIN": {
        # -------------------------------------------------------
        #                 LOGIN
        # -------------------------------------------------------
        "login:list",
        "login:retrieve",
        "login:create",
        "login:update",
        "login:partial_update",
        "login:destroy",
        "login:obtener_por_usuario",

        # -------------------------------------------------------
        #                 USUARIO
        # -------------------------------------------------------
        "usuario:list",
        "usuario:retrieve",
        "usuario:create",
        "usuario:update",
        "usuario:partial_update",
        "usuario:destroy",

        # -------------------------------------------------------
        #                 MAQUINARIA
        # -------------------------------------------------------
        "maquinaria:list",
        "maquinaria:retrieve",
        "maquinaria:create",
        "maquinaria:update",
        "maquinaria:partial_update",
        "maquinaria:destroy",
        "maquinaria:resumen_maquinarias",
        "maquinaria:maquinarias_en_operacion",
        "maquinaria:maquinarias_vencidas",
        "maquinaria:maquinarias_pendientes",
        "maquinaria:maquinarias_al_dia",
        "maquinaria:ultimas_maquinarias",

        # -------------------------------------------------------
        #                 CONDUCTOR
        # -------------------------------------------------------
        "conductor:list",
        "conductor:retrieve",
        "conductor:create",
        "conductor:update",
        "conductor:partial_update",
        "conductor:destroy",

        # -------------------------------------------------------
        #                 CURSO
        # -------------------------------------------------------
        "curso:list",
        "curso:retrieve",
        "curso:create",
        "curso:update",
        "curso:partial_update",
        "curso:destroy",
        "curso:cursos_por_usuario",

        # -------------------------------------------------------
        #                 PROYECTO
        # -------------------------------------------------------
        "proyecto:list",
        "proyecto:retrieve",
        "proyecto:create",
        "proyecto:update",
        "proyecto:partial_update",
        "proyecto:destroy",
        "proyecto:listar_por_empresa",

        # -------------------------------------------------------
        #                 MANTENIMIENTO PROGRAMADO
        # -------------------------------------------------------
        "mantenimiento_programado:list",
        "mantenimiento_programado:retrieve",
        "mantenimiento_programado:create",
        "mantenimiento_programado:update",
        "mantenimiento_programado:partial_update",
        "mantenimiento_programado:destroy",
        "mantenimiento_programado:mantenimientos_por_maquina",

        # -------------------------------------------------------
        #                 MANTENIMIENTO
        # -------------------------------------------------------
        "mantenimiento:list",
        "mantenimiento:retrieve",
        "mantenimiento:create",
        "mantenimiento:update",
        "mantenimiento:partial_update",
        "mantenimiento:destroy",
        "mantenimiento:mantenimientos_por_maquina",
        "mantenimiento:mantenimientos_por_usuario",

        # -------------------------------------------------------
        #                 HOJA DE VIDA
        # -------------------------------------------------------
        "hoja_vida:list",
        "hoja_vida:retrieve",
        "hoja_vida:create",
        "hoja_vida:update",
        "hoja_vida:partial_update",
        "hoja_vida:destroy",

        # -------------------------------------------------------
        #                 PROYECTO MAQUINARIA
        # -------------------------------------------------------
        "proyecto_maquinaria:list",
        "proyecto_maquinaria:retrieve",
        "proyecto_maquinaria:create",
        "proyecto_maquinaria:update",
        "proyecto_maquinaria:partial_update",
        "proyecto_maquinaria:destroy",
        "proyecto_maquinaria:asignaciones_por_proyecto",
        "proyecto_maquinaria:asignaciones_por_maquina",

        # -------------------------------------------------------
        #                 REGISTRO HORAS MAQUINARIA
        # -------------------------------------------------------
        "registro_horas_maquinaria:list",
        "registro_horas_maquinaria:retrieve",
        "registro_horas_maquinaria:create",
        "registro_horas_maquinaria:update",
        "registro_horas_maquinaria:partial_update",
        "registro_horas_maquinaria:destroy",
        "registro_horas_maquinaria:registros_por_maquinas",

        # -------------------------------------------------------
        #                 ALARMA
        # -------------------------------------------------------
        "alarma:list",
        "alarma:retrieve",
        "alarma:marcar_como_vista",
        "alarma:cantidad_no_vistas",

    },
    "RESPONSABLE_DE_MANTENIMIENTO": {
        # -------------------------------------------------------
        #                 MAQUINARIA
        # -------------------------------------------------------
        "maquinaria:list",
        "maquinaria:retrieve",
        "maquinaria:resumen_maquinarias",
        "maquinaria:maquinarias_en_operacion",
        "maquinaria:maquinarias_vencidas",
        "maquinaria:maquinarias_pendientes",
        "maquinaria:maquinarias_al_dia",
        "maquinaria:ultimas_maquinarias",

        # -------------------------------------------------------
        #                 MANTENIMIENTO PROGRAMADO
        # -------------------------------------------------------
        "mantenimiento_programado:list",
        "mantenimiento_programado:retrieve",
        "mantenimiento_programado:create",
        "mantenimiento_programado:update",
        "mantenimiento_programado:partial_update",
        "mantenimiento_programado:destroy",
        "mantenimiento_programado:mantenimientos_por_maquina",

        # -------------------------------------------------------
        #                 MANTENIMIENTO
        # -------------------------------------------------------
        "mantenimiento:list",
        "mantenimiento:retrieve",
        "mantenimiento:create",
        "mantenimiento:update",
        "mantenimiento:partial_update",
        "mantenimiento:destroy",
        "mantenimiento:mantenimientos_por_maquina",
        "mantenimiento:mantenimientos_por_usuario",

        # -------------------------------------------------------
        #                 HOJA DE VIDA
        # -------------------------------------------------------
        "hoja_vida:list",
        "hoja_vida:retrieve",

        # -------------------------------------------------------
        #                 ALARMA
        # -------------------------------------------------------
        "alarma:list",
        "alarma:retrieve",
        "alarma:cantidad_no_vistas",
    },
    "OPERADOR": {
        # -------------------------------------------------------
        #                 MAQUINARIA
        # -------------------------------------------------------
        "maquinaria:list",
        "maquinaria:retrieve",
        "maquinaria:resumen_maquinarias",
        "maquinaria:maquinarias_en_operacion",
        "maquinaria:maquinarias_vencidas",
        "maquinaria:maquinarias_pendientes",
        "maquinaria:maquinarias_al_dia",
        "maquinaria:ultimas_maquinarias",

        # -------------------------------------------------------
        #                 REGISTRO HORAS MAQUINARIA
        # -------------------------------------------------------
        "registro_horas_maquinaria:list",
        "registro_horas_maquinaria:retrieve",
        "registro_horas_maquinaria:create",
        "registro_horas_maquinaria:update",
        "registro_horas_maquinaria:partial_update",
        "registro_horas_maquinaria:destroy",
        "registro_horas_maquinaria:registros_por_maquinas",

        # -------------------------------------------------------
        #                 MANTENIMIENTO PROGRAMADO
        # -------------------------------------------------------
        "mantenimiento_programado:retrieve",
        "mantenimiento_programado:mantenimientos_por_maquina",

        # -------------------------------------------------------
        #                 HOJA DE VIDA
        # -------------------------------------------------------
        "hoja_vida:list",
        "hoja_vida:retrieve",

        # -------------------------------------------------------
        #                 USUARIO
        # -------------------------------------------------------
        "usuario:list",
        "usuario:retrieve",

        # -------------------------------------------------------
        #                 PROYECTO
        # -------------------------------------------------------
        "proyecto:list",
        "proyecto:retrieve",

        # -------------------------------------------------------
        #                 ALARMA
        # -------------------------------------------------------
        "alarma:list",
        "alarma:retrieve",
        "alarma:cantidad_no_vistas",
    },
    "TECNICO_DE_MANTENIMIENTO": {
        # -------------------------------------------------------
        #                 MAQUINARIA
        # -------------------------------------------------------
        "maquinaria:list",
        "maquinaria:retrieve",
        "maquinaria:resumen_maquinarias",
        "maquinaria:maquinarias_en_operacion",
        "maquinaria:maquinarias_vencidas",
        "maquinaria:maquinarias_pendientes",
        "maquinaria:maquinarias_al_dia",
        "maquinaria:ultimas_maquinarias",

        # -------------------------------------------------------
        #                 HOJA DE VIDA
        # -------------------------------------------------------
        "hoja_vida:list",
        "hoja_vida:retrieve",

        # -------------------------------------------------------
        #                 MANTENIMIENTO PROGRAMADO
        # -------------------------------------------------------
        "mantenimiento_programado:list",
        "mantenimiento_programado:retrieve",
        "mantenimiento_programado:mantenimientos_por_maquina",

        # -------------------------------------------------------
        #                 USUARIO
        # -------------------------------------------------------
        "usuario:list",

        # -------------------------------------------------------
        #                 MANTENIMIENTO
        # -------------------------------------------------------
        "mantenimiento:list",
        "mantenimiento:retrieve",
        "mantenimiento:create",
        "mantenimiento:update",
        "mantenimiento:partial_update",
        "mantenimiento:destroy",
        "mantenimiento:mantenimientos_por_maquina",
        "mantenimiento:mantenimientos_por_usuario",

        # -------------------------------------------------------
        #                 ALARMA
        # -------------------------------------------------------
        "alarma:list",
        "alarma:retrieve",
        "alarma:cantidad_no_vistas",
    }
}