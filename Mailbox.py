from flask import Flask, request
import mailbox, email, os, json
import traceback


app = Flask(__name__)
mailboxes = {}

def resolve_real_recipient(recipient):
    json_data = open('/opt/cloudfleet/users/users.json')
    users = json.load(json_data)["users"].items()

    for username, userdata in users:
        if username.lower() == recipient.lower():
            return username
        else:
            if userdata["aliases"] and recipient.lower() in [alias.lower() for alias in userdata["aliases"]]
                return username
    return None


@app.route('/raw/<recipient>', methods=['POST'])
def post_message(recipient):
    try:
        real_recipient = recipient

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
        print traceback.format_exc()

    return "success!"


if __name__ == '__main__':
    app.run(port=3000, host="0.0.0.0")
