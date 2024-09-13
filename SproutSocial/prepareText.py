def preparar_texto(clip_info):
    titulo = clip_info['titulo']
    descripcion = clip_info['descripcion']
    pregunta = clip_info['pregunta']
    canal = clip_info['canal']
    tags = ' '.join(['#' + tag for tag in clip_info['tags']])

    contenido = f"{titulo}\n\n{descripcion}\n{pregunta}\n\nCréditos a {canal}\n\n{tags}"
    print(contenido)
    return contenido
