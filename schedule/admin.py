from django.contrib import admin

from schedule.models import Turma, Disciplina, WeekDay, Professor

class TurmasAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class WeekDayAdmin(admin.ModelAdmin):
    list_display = ('name', 'aulas_diarias',)
    search_fields = ('name',)    

class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantidade_de_aulas_semana', 'aula_dividida',)
    search_fields = ('name',)

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)    


admin.site.register(Turma, TurmasAdmin)
admin.site.register(WeekDay, WeekDayAdmin)
admin.site.register(Disciplina, DisciplinaAdmin)
admin.site.register(Professor, ProfessorAdmin)
