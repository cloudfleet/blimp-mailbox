from flask import Flask, request
import mailbox, email
import traceback


app = Flask(__name__)
mailboxes = {}


@app.route('/raw/<recipient>', methods=['POST'])
def post_message(recipient):
    try:
        # TODO resolve alias
        real_recipient = recipient

        if not real_recipient in mailboxes:
            mailboxes[real_recipient] = mailbox.Maildir("/opt/cloudfleet/maildir/%s" % real_recipient, factory=None, create=True)

        new_message = email.message_from_string(request.data)
        mailboxes[real_recipient].add(new_message)
    except:
        print traceback.format_exc()

    return "success!"


if __name__ == '__main__':
    app.run(port=3000, host="0.0.0.0")
