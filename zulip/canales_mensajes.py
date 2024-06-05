import zulip

try:
    client = zulip.Client(config_file="zuliprc")
except zulip.ConfigNotFoundError:
    print("Falta descargar el archivo .zuliprc con tu sesion de Zulip")
    print("Se descarga de https://famaf.zulipchat.com/#settings/account-and-privacy")
    print('Abajo hay un boton que dice "Mostrar clave de API" y tiene la opcion de descargar el zuliprc')
    exit(1)  # Termina la ejecución si no encuentra el archivo de configuración.

members = client.get_members()["members"]

def get_user_id(emails):
    """
    Devuelve una lista de IDs de usuarios basada en sus emails.
    """
    ids = []
    for m in members:
        if m["delivery_email"] in emails:
            emails.remove(m["delivery_email"])
            ids.append(m["user_id"])
    return ids

def get_name(user_ids):
    """
    Devuelve una lista de nombres completos basada en los IDs de usuarios.
    """
    names = []
    for user_id in user_ids:
        result = client.get_user_by_id(user_id)
        if result['result'] == 'success':
            names.append(result["user"]["full_name"])
        else:
            print(f"Error obteniendo el nombre para el user_id {user_id}")
    return names

def tag_mail(email):
    """
    Devuelve una etiqueta de mención para un email específico.
    """
    user_ids = get_user_id([email])
    if user_ids:
        name = get_name(user_ids)[0]
        return f"@**{name}**"
    else:
        return f"@**{email}**"

def create_private_stream(stream_name, emails):
    """
    Crea un canal privado con el nombre especificado y añade a los usuarios con los emails dados.
    """
    user_ids = get_user_id(emails)
    result = client.add_subscriptions(
        streams=[
            {
                "name": stream_name,
                "description": "New stream for testing",
            },
        ],
        invite_only=True,
        principals=user_ids,
    )

    if result['result'] == 'success':
        subscriptions = client.get_subscriptions()

        for subscription in subscriptions["subscriptions"]:
            if subscription["name"] == stream_name:
                print(f"El canal {stream_name} fue creado con éxito y su stream_id es {subscription['stream_id']}")
                result = client.get_subscribers(stream=stream_name)
                if result['result'] == 'success':
                    print(f"Los miembros del canal son: {get_name(result['subscribers'])}")
                else:
                    print(f"Error obteniendo los miembros del canal {stream_name}")
        return result
    else:
        print(f"Error creando el canal {stream_name}: {result['msg']}")
        return None

def send_message(stream_name, subject, content):
    """
    Envía un mensaje al canal especificado con el asunto y contenido dados.
    """
    request = {
        "type": "stream",
        "to": stream_name,
        "subject": subject,
        "content": content
    }

    response = client.send_message(request)
    if response['result'] == 'success':
        print("Mensaje enviado con éxito")
    else:
        print(f"Error enviando mensaje: {response['msg']}")
    return response

def get_subscribed_streams():
    """
    Devuelve una lista de todos los canales a los que el usuario está suscripto.
    """
    result = client.get_subscriptions()
    if result['result'] == 'success':
        streams = [subscription['name'] for subscription in result['subscriptions']]
        return streams
    else:
        print(f"Error obteniendo suscripciones: {result['msg']}")
        return []

# Ejemplo de uso
if __name__ == "__main__":
    streams = get_subscribed_streams()
    print("Estás suscripto a los siguientes canales:")
    result = []
    for stream in streams:
        if "REDES" in stream.upper():
            result.append(stream)
    print(result)

#La siguiente linea crea un stream privado que se llama "Canal de prueba" con los usuarios de esos mails suscriptos
#create_private_stream("Canal-de-prueba",["otro@gmail.com", "yo@gmail.com"])

# La siguiente linea envia un mensaje al stream con "Asunto" como asunto y como mensaje "Hola " junto con el tag al usuario del mail otro@gmail.com
#send_message("Canal-de-prueba", "Asunto", f"Hola {tag_mail('otro@gmail.com')}?")
