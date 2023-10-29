from datetime import time, timedelta

class Turma:
    def __init__(self, nome, professor, horario):
        self.nome = nome
        self.professor = professor
        self.horario = horario

# Interval Scheduling
tempoAula = timedelta(minutes=55)
tempoAulaNoite = timedelta(minutes=50)

horarios = {
    "M": [timedelta(hours=8, minutes=0), timedelta(hours=8, minutes=55), timedelta(hours=10, minutes=0), timedelta(hours=10, minutes=55), timedelta(hours=12, minutes=55)],
    "T": [timedelta(hours=12, minutes=55), timedelta(hours=14, minutes=0), timedelta(hours=14, minutes=55), timedelta(hours=16, minutes=0), timedelta(hours=16, minutes=55), timedelta(hours=18, minutes=0), timedelta(hours=18, minutes=55)],
    "N": [timedelta(hours=19, minutes=0), timedelta(hours=19, minutes=50), timedelta(hours=20, minutes=50), timedelta(hours=21, minutes=40)]
}

def converteTempo(materia):
    dias = ""
    i = 0
    while materia[i].isdigit():
        dias += materia[i]
        i += 1
    periodo = materia[i]
    hora = materia[i + 1:]
    return dias, periodo, hora

def ordenaMaterias(grade: Turma):
    materias = []
    for turma in grade:
        dias, periodo, hora = converteTempo(turma.horario)
        hora = hora.strip()
        # print(f"'{turma.horario}'", f"'{dias}'", f"'{periodo}'", f"'{hora}'")
        horaInicio = horarios[periodo][int(hora[0]) - 1]
        horaFim = horarios[periodo][int(hora[1]) - 1] + (tempoAulaNoite if periodo == "N" else tempoAula)
        turma.horario = [dias, periodo, horaInicio, horaFim]
        materias.append(turma)
    return sorted(materias, key=lambda x: x.horario[3])

def interval_scheduling(grade):
    grade = ordenaMaterias(grade)
    gradeOtima = []
    ultimoHorarioFim = None
    ultimoDiasAula = ""
    for turma in grade:
        horario_inicio = turma.horario[2]
        diasAula = turma.horario[0]
        if ultimoHorarioFim is None or horario_inicio >= ultimoHorarioFim or ultimoDiasAula != diasAula:
            gradeOtima.append(turma)
            ultimoHorarioFim = turma.horario[3]
            ultimoDiasAula = diasAula
    return gradeOtima