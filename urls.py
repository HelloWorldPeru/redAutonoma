import connection as cn
from views import dashboard
from views import home
from views import phonegap

app = cn.app

#Website
app.add_url_rule('/', view_func=home.index)
app.add_url_rule('/login', view_func=home.log, methods=['GET', 'POST'])
app.add_url_rule('/logout', view_func=home.logout)

#Dashboard
app.add_url_rule('/dashboard', view_func=dashboard.dashboard)
app.add_url_rule('/dashboard/carreras-list', view_func=dashboard.carreras)
app.add_url_rule('/dashboard/criterios-list', view_func=dashboard.criterios)
app.add_url_rule('/dashboard/profesor-list', view_func=dashboard.profesores)
app.add_url_rule('/dashboard/turno-list', view_func=dashboard.turnos)
app.add_url_rule('/dashboard/usuarios-list', view_func=dashboard.usuarios)
app.add_url_rule('/dashboard/usuarios-detail/<int:token_user>', view_func=dashboard.detale_usuario)
app.add_url_rule('/dashboard/cursos-list', view_func=dashboard.cursos)

#WebService (Phonegap)
app.add_url_rule('/login-ajax', view_func=phonegap.login_ajax, methods=['POST'])
app.add_url_rule('/actualizar', view_func=phonegap.update_information, methods=['POST'])
app.add_url_rule('/perfil', view_func=phonegap.get_current_user, methods=['POST'])
app.add_url_rule('/carrera', view_func=phonegap.get_current_carreras)
app.add_url_rule('/turno', view_func=phonegap.get_current_turno)
app.add_url_rule('/curso', view_func=phonegap.get_curso, methods=['POST'])

#Ejecutando servidor
if __name__ == "__main__":
    app.run(debug=True)