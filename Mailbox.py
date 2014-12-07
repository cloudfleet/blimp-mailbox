from flask import Flask, request
import mailbox, email, os
import traceback


app = Flask(__name__)
mailboxes = {}


@app.route('/raw/<recipient>', methods=['POST'])
def post_message(recipient):
    try:
        # TODO resolve alias
        real_recipient = recipient

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
