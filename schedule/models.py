from django.db import models

class Disciplina(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    quantidade_de_aulas_semana = models.IntegerField()
    aula_dividida = models.BooleanField()

    def __str__(self):
        return self.name

class Turma(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10) #campo de string
    disciplinas = models.ManyToManyField(Disciplina, related_name='disciplinas')

    def __str__(self):
        return self.name

class WeekDay(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    aulas_diarias = models.IntegerField()

    def __str__(self):
        return self.name

class Professor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    disciplina = models.ManyToManyField(Disciplina, related_name='disciplina')
    disponibilidade = models.ManyToManyField(WeekDay, related_name='disponibilidade')
    turmas = models.ManyToManyField(Turma, related_name='turmas')

    def __str__(self):
        return self.name