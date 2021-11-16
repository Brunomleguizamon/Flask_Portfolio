from flask import(
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    current_app
)
from flask.helpers import send_file, url_for
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *

bp = Blueprint('portfolio', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def index():
    return render_template('portfolio/index.html')


@bp.route('/mail', methods=['POST', 'GET'])
def mail():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if request.method == 'POST':
        send_email(name, email, message)
        return render_template('portfolio/send_mail.html')
    else:
        return redirect(url_for('portfolio.index'))


def send_email(name, email, message):
    mi_email = 'brunomleguizamon@gmail.com'
    sg = sendgrid .SendGridAPIClient(
        api_key=current_app.config['SENDGRID_KEY'])

    from_email = Email(mi_email)
    to_email = To(mi_email, substitutions={
        "-name-": name,
        "-email-": email,
        "-message-": message,
    })

    html_content = """
        <p>Hola Bruno! tienes un nuevo contacto desde la pagina web </p>
        <p>Nombre: -name- </p>
        <p>Email: -email- </p>
        <p>Mensaje: -message-  </p>
    """

    mail = Mail(mi_email, to_email,
                'Nuevo contacto desde el portfolio', html_content=html_content)
    response = sg.client.mail.send.post(request_body=mail.get())
