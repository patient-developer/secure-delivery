from io import BytesIO

from PyPDF2 import PdfFileWriter
from flask import render_template, url_for, flash
from flask_login import login_required
from werkzeug.utils import secure_filename, redirect

from app.delivery.forms import FileForm
from app.emails import send_mail
from app.security import get_password
from config import Config
from . import blueprint
from ..pdfhelper import provide_pdf_file_reader


@blueprint.route('/send-mail', methods=['GET', 'POST'])
@login_required
def delivery():
    file_form = FileForm()
    if file_form.validate_on_submit():

        reader, is_ok = provide_pdf_file_reader(BytesIO(file_form.file.data.read()))

        if not is_ok:
            flash('Invalid pdf file provided.')
            return render_template('delivery.html', form=file_form)

        out = PdfFileWriter()

        for page in range(reader.numPages):
            out.addPage(reader.getPage(page))

        password = get_password()
        filename = secure_filename(str(file_form.file.data.filename).strip())

        out.encrypt(password)

        attachment = BytesIO()

        out.write(attachment)

        email_recipient = str(file_form.email_recipient.data).strip()

        send_mail('Attachment',
                  Config.ADMINS[0],
                  [email_recipient],
                  'Zustellung von ' + filename,
                  filename,
                  attachment.getvalue())

        send_mail('Password',
                  Config.ADMINS[0],
                  [email_recipient],
                  password, None, None)

        flash('Successfully delivered ' + filename + ' to ' + email_recipient + '.')

        return redirect(url_for('.delivery'))

    if len(file_form.errors) > 0:
        for error in file_form.errors.values():
            flash(str(error))

    return render_template('delivery.html', form=file_form)
