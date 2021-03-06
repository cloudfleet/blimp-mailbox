from flask import Flask, request, current_app
import mailbox, email, os, json
import traceback


app = Flask(__name__)
mailboxes = {}

def load_users():
    json_data = open('/opt/cloudfleet/users/users.json')
    return json.load(json_data)["users"]


def resolve_real_recipient(recipient, users):

    for username, userdata in users.items():
        if username.lower() == recipient.lower():
            return username
        else:
            if userdata["aliases"] and recipient.lower() in [alias.lower() for alias in userdata["aliases"]]:
                return username
    return None


@app.route('/raw/<recipient>', methods=['POST'])
def post_message(recipient):
    try:
        current_app.logger.debug("receiving mail for %s" % recipient)
        real_recipient = resolve_real_recipient(recipient, load_users())
        current_app.logger.debug("delivering mail to %s" % real_recipient)



        if not real_recipient:
            abort(404)

        if not real_recipient in mailboxes:
            directory = "/opt/cloudfleet/maildir/%s" % real_recipient
            for subdir in ["cur", "tmp", "new"]:
                subdir_path = "%s/%s" % (directory, subdir)
                if not os.path.exists(subdir_path):
                    os.makedirs(subdir_path)

            mailboxes[real_recipient] = mailbox.Maildir(directory, factory=None)

        new_message = email.message_from_string(request.data)
        recipient_mailbox = mailboxes[real_recipient]
        recipient_mailbox.add(new_message)
    except:
        current_app.logger.error(traceback.format_exc())

    return "success!"


if __name__ == '__main__':
    app.run(port=3000, host="0.0.0.0", debug="True")
