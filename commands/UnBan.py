import time
import config
import functions


def cmd(api, message, args):
    for_all = None if message['from_id'] == message['peer_id'] else True

    if message.get('reply_message') is not None:
        target = api.users.get(
            user_ids=message['reply_message']['from_id']
        )
    else:
        try:
            target = api.users.get(
                user_ids=functions.getUserId(args[1])
            )
        except:
            api.messages.edit(
                peer_id=message['peer_id'],
                message_id=message['id'],
                message=f"{config.prefixes['error']} Необходимо ответить на сообщение пользователя или указать на него ссылку: /unban [пользователь]"
            )
            time.sleep(3)
            api.messages.delete(
                message_ids=message['id'],
                delete_for_all=for_all
            )
            return

    banned = functions.getData('banned')
    if banned is None: banned = []

    target = target[0]
    if not (target['id'] in banned):
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['invalid']} [id{target['id']}|{target['first_name']} {target['last_name']}] не заблокирован."
        )
        return

    banned.remove(target['id'])
    edit = functions.editData('banned', banned)

    if edit:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['success']} [id{target['id']}|{target['first_name']} {target['last_name']}] был разблокирован!"
        )
    else:
        api.messages.edit(
            peer_id=message['peer_id'],
            message_id=message['id'],
            message=f"{config.prefixes['error']} Пользователя [id{target['id']}|{target['first_name']} {target['last_name']}] не получилось разблокировать. Возможно данные повреждены."
        )

    return
