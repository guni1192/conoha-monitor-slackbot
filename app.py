import os
from slackbot.bot import Bot, respond_to
from conoha import ConoHaHandler

@respond_to('servers')
def mention_func(message):
    client = conoha_init()
    print(client.get_vms_detail())
    message.reply('hgoe')

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
