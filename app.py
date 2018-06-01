import os
import json
from slackbot.bot import Bot, respond_to
from conoha import ConoHaHandler


def conoha_init():
    username = os.environ['CONOHA_USERNAME']
    password = os.environ['CONOHA_PASSWORD']
    tenant_id = os.environ['CONOHA_TENANT_ID']
    return ConoHaHandler(username, password, tenant_id)


conoha = conoha_init()


@respond_to('servers')
def servers(message):

    fields = []
    for server in conoha.get_vms_detail()['servers']:
        fields.append({'title': server['name'], 'value': server['status']})

    attachments = [
        {
            'pretext': 'Instance List',
            'fallback': 'Fallback text',
            'author_name': 'Instance List',
            'fields': fields,
            'color': '#59afe1'
        }]
    message.send_webapi('', json.dumps(attachments))


def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    print('RUNNING SLACK BOT')
    main()
