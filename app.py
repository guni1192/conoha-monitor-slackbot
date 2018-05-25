import os
from slackbot.bot import Bot, respond_to
from conoha import ConoHaHandler

conoha = conoha_init()


@respond_to('servers')
def mention_func(message):
    print(conoha.get_vms_detail()['servers'])
    for server in conoha.get_vms_detail()['servers']:
        msg = '```'
        msg += 'hostId: ' + server['hostId'] + '\n'
        msg += 'status: ' + server['status'] + '\n'
        msg += '```'
        message.reply(msg)


def conoha_init():
    username = os.environ['CONOHA_USERNAME']
    password = os.environ['CONOHA_PASSWORD']
    tenant_id = os.environ['CONOHA_TENANT_ID']
    return ConoHaHandler(username, password, tenant_id)


def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    print('RUNNING SLACK BOT')
    main()
