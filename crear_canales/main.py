import zulip

client = zulip.Client(config_file=".zuliprc")

members = client.get_members()["members"]

def get_user_id(emails, name=None):
    ids = []
    for m in members:
        if emails:
            if m["delivery_email"] in emails:
                emails.remove(m["delivery_email"])
                ids.append(m["user_id"])
        else:
            return ids

def get_name(user_ids):
    names =[]
    for user_id in user_ids:
        result = client.get_user_by_id(user_id)
        names.append(result["user"]["full_name"])
    return names

def tag_mail(email):
    name = get_name(get_user_id([email]))[0]
    return f"@**{name}**"

def create_private_stream(stream_name, emails):
    result = client.add_subscriptions(
        streams=[
            {
                "name": stream_name,
                "description": "New stream for testing",
            },
        ],
        invite_only=True,
        principals=get_user_id(emails),
    )

    subscriptions = client.get_subscriptions()

    for subscription in subscriptions["subscriptions"]:
        if subscription["name"] == stream_name:
            print(f"El canal {stream_name} fue creado con éxito y su stream_id es {subscription['stream_id']}")
            result = client.get_subscribers(stream=stream_name)
            print(f"Los miembros del canal son: {get_name(result['subscribers'])}")
    
    return result


def send_message(stream_name, subject, content):

    request = {
        "type": "stream",
        "to": stream_name,
        "subject": subject,
        "content": content
    }

    response = client.send_message(request)
    return response

#La siguiente linea crea un stream privado que se llama "Canal de prueba" con los usuarios de esos mails suscriptos
#create_private_stream("Canal-de-prueba",["otro@gmail.com", "yo@gmail.com"])

# La siguiente linea envia un mensaje al stream con "Asunto" como asunto y como mensaje "Hola " junto con el tag al usuario del mail otro@gmail.com
#send_message("Canal-de-prueba", "Asunto", f"Hola {tag_mail('otro@gmail.com')}?")