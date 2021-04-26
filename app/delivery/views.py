from io import BytesIO

from PyPDF2 import PdfFileWriter, PdfFileReader
from flask import render_template, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename, redirect

from . import blueprint
from app.delivery.forms import FileForm
from app.emails import send_mail
from app.security import get_password
from config import Config


@blueprint.route('/send-mail', methods=['GET', 'POST'])
@login_required
def delivery():
    file_form = FileForm()
    if file_form.validate_on_submit():
        password = get_password()
        filename = secure_filename(file_form.file.data.filename)

        out = PdfFileWriter()
        file = PdfFileReader(BytesIO(file_form.file.data.read()))

        for page in range(file.numPages):
            out.addPage(file.getPage(page))

        out.encrypt(password)

        attachment = BytesIO()

        out.write(attachment)

        send_mail('Attachment',
                  Config.ADMINS[0],
                  [file_form.email_recipient.data],
                  'Zustellung von ' + filename,
                  filename,
                  attachment.getvalue())

        send_mail('Password',
                  Config.ADMINS[0],
                  [file_form.email_recipient.data],
                  password, None, None)

        return redirect(url_for('.delivery'))
    return render_template('delivery.html', form=file_form)
