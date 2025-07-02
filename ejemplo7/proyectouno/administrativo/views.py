from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render

# importar las clases de models.py
from administrativo.models import Matricula, Estudiante
from administrativo.forms import *


# vista que permita presesentar las matriculas
# el nombre de la vista es index.

def index(request):
    """
    """
    matriculas = Matricula.objects.all()

    titulo = "Listado de matriculas"
    informacion_template = {'matriculas': matriculas,
                            'numero_matriculas': len(matriculas), 'mititulo': titulo}
    return render(request, 'index.html', informacion_template)


def detalle_matricula(request, id):
    """

    """

    matricula = Matricula.objects.get(pk=id)
    informacion_template = {'matricula': matricula}
    return render(request, 'detalle_matricula.html', informacion_template)


def crear_matricula(request):
    """
    """
    if request.method == 'POST':
        formulario = MatriculaForm(request.POST)
        print(formulario.errors)
        if formulario.is_valid():
            formulario.save()  # se guarda en la base de datos
            return redirect(index)
    else:
        formulario = MatriculaForm()
    diccionario = {'formulario': formulario}

    return render(request, 'crear_matricula.html', diccionario)


def editar_matricula(request, id):
    """
    """
    matricula = Matricula.objects.get(pk=id)
    print("----------matricula")
    print(matricula)
    print("----------matricula")
    if request.method == 'POST':
        formulario = MatriculaEditForm(request.POST, instance=matricula)
        print(formulario.errors)
        if formulario.is_valid():
            formulario.save()
            return redirect(index)
    else:
        formulario = MatriculaEditForm(instance=matricula)
    diccionario = {'formulario': formulario}

    return render(request, 'crear_matricula.html', diccionario)


def detalle_estudiante(request, id):
    """

    """

    estudiante = Estudiante.objects.get(pk=id)
    informacion_template = {'e': estudiante}
    return render(request, 'detalle_estudiante.html', informacion_template)


def listar_estudiantes(request):
    """
    Muestra los estudiantes con el costo total de sus matrículas.
    """
    estudiantes = Estudiante.objects.annotate(total_costo=Sum("lasmatriculas__costo"))
    contexto = {
        "estudiantes": estudiantes,
        "titulo": "Listado de estudiantes",
        "numero_estudiantes": estudiantes.count(),
    }
    return render(request, "listar_estudiantes.html", contexto)


def crear_estudiante(request):
    if request.method == "POST":
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(listar_estudiantes)
    else:
        form = EstudianteForm()
    return render(request, "crear_estudiante.html", {"formulario": form})


def editar_estudiante(request, id):
    estudiante = get_object_or_404(Estudiante, pk=id)
    if request.method == "POST":
        form = EstudianteEditForm(request.POST, instance=estudiante)
        if form.is_valid():
            form.save()
            return redirect(listar_estudiantes)
    else:
        form = EstudianteEditForm(instance=estudiante)
    return render(request, "crear_estudiante.html", {"formulario": form})


def listar_modulos(request):
    """
    Muestra cada módulo y la suma de los costos de sus matrículas.
    """
    # Anotamos el total a partir del campo `costo` de las matrículas
    modulos = Modulo.objects.annotate(total_valor=Sum("lasmatriculas__costo"))
    contexto = {
        "modulos": modulos,
        "titulo": "Listado de módulos",
        "numero_modulos": modulos.count(),
    }
    return render(request, "listar_modulos.html", contexto)


def crear_modulo(request):
    if request.method == "POST":
        form = ModuloForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(listar_modulos)
    else:
        form = ModuloForm()
    return render(request, "crear_modulo.html", {"formulario": form})


def editar_modulo(request, id):
    modulo = get_object_or_404(Modulo, pk=id)
    if request.method == "POST":
        form = ModuloEditForm(request.POST, instance=modulo)
        if form.is_valid():
            form.save()
            return redirect(listar_modulos)
    else:
        form = ModuloEditForm(instance=modulo)
    return render(request, "crear_modulo.html", {"formulario": form})

# ver los módulos
#    nombre del módulp
#    valor de todas las matriculas del módulo
# ver los estudiantes >> de los estudiantes debo visualizar:
#    nombre
#    apellido
#    cedula
#    edad
#    tipo_estudiante
#    costo de matriculas

# crear módulos
# crear estudiantes
