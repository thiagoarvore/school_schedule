import sqlite3
import random
import numpy

def sortear_dia(dia_da_semana, turma, num_de_aulas, profs_do_dia_na_turma_por_disc, max_aula_disc):
    horario_dia_turma = []
    while num_de_aulas > 0:
        aula = random.choice(profs_do_dia_na_turma_por_disc)
        disc = aula[1]
        count = 1 
        restricao = False
        for a in horario_dia_turma:
            if a[1] == disc:
                count+=1
            if count > 2:
                restricao = True
                break
        if restricao == True:
            restricao = False
            continue
        count = 1
        restricao = False
        for a in horario_dia_turma:
            if a[1] == disc:
                count+=1
            if count > max_aula_disc[disc]:
                restricao = True                    
                break
        if restricao == True:
            restricao = False
            continue
        else:
            horario_dia_turma.append(aula)
            num_de_aulas -= 1
    return f"turma {turma}", horario_dia_turma

def pontuar_comb_dia(horario, num_de_aulas):
    score = 100
    count_aula = num_de_aulas        
    disc = []    
    for a in horario:
        disc.append(a[1])
    #tirar 10 pontos por dobradinha
    while count_aula>0:            
        count_aula = num_de_aulas
        for b in disc:
            count = 0
            for a in horario:                
                count_aula-=1
                if a[1] == b:
                    count += 1
                if count > 1:
                    score-=5
    
    return score, horario

def verificar_otimização(combinacoes):
    for pontos in combinacoes[1]:
        if pontos != 100:
            return False
    return True

def escolher_combinacoes_de_dia():
    combin_dia = []
    comb_desejadas = 3
    otimo = False
    for i in range(0, 100):
        if otimo == True:
            return len(combin_dia), combin_dia
        x = sortear_dia(dia, turma, num_de_aulas, disc_prof, max_aula_dis)          
        comb = pontuar_comb_dia(x[1], num_de_aulas)
        count = 0
        if len(combin_dia) < 1:
            combin_dia.append(comb)            
            continue
        for a in combin_dia:
            if comb[1] == a[1]:
                break
            if len(combin_dia) < comb_desejadas:
                combin_dia.append(comb)
                combin_dia = numpy.unique(combin_dia)
                break 
            for c in combin_dia:                           
                if c[0] > comb[0]:
                    count +- 1
                if count > 30:
                    break
                if len(combin_dia) >= comb_desejadas:
                    if verificar_otimização(combin_dia):
                        otimo = True
                        break
                    for b in combin_dia:
                        if b[0] == 100:
                            continue
                        if b[0] > comb[0]:
                            continue
                        else:
                            combin_dia.remove(b)
                            combin_dia.append(comb)
                            combin_dia = numpy.unique(combin_dia)
                            break
    return combin_dia

#db setup
db = sqlite3.connect("db.sqlite3")
cursor = db.cursor()

#fazer a lista de dias da semana
cursor.execute("SELECT id FROM turmas_weekday")
dias_da_semana = cursor.fetchall()

#fazer a lista de turmas
cursor.execute("SELECT id FROM turmas_turma")
turmas1 = cursor.fetchall()
turmas = []
for a in turmas1:
    turmas.append(a[0])#o banco de dados tá no django e ele retorna o id seguido de uma vírgula, por isso àz vezes pego o primeiro indice

for dia in dias_da_semana:
    #selecionar o número de aulas do dia:
    cursor.execute(f"SELECT aulas_diarias FROM turmas_weekday WHERE id = {dia[0]}")
    num_de_aulas1 = cursor.fetchall()
    num_de_aulas = num_de_aulas1[0][0]

    #selecionar os professores disponíveis no dia:
    cursor.execute(f"SELECT professor_id FROM turmas_professor_disponibilidade WHERE weekday_id = {dia[0]}")    
    prof_dia1 = cursor.fetchall()
    prof_dia = []
    for a in prof_dia1:
        prof_dia.append(a[0])

    #selecionar os professores disponiveis no dia para ESSA turma:
    for turma in turmas:
        cursor.execute(f"SELECT professor_id FROM turmas_professor_turmas WHERE turma_id = {turma}")
        prof_turma1 = cursor.fetchall()
        prof_turma = []
        for prof in prof_turma1:
            prof_turma.append(prof[0])
        prof_dia_turma = []
        for prof in prof_turma:
            if prof in prof_dia:
                prof_dia_turma.append(prof)

        #selecionar as disciplinas para ESSA turma:
        cursor.execute(f"SELECT disciplina_id FROM turmas_turma_disciplinas WHERE turma_id = {turma}")
        disciplina_turma1 = cursor.fetchall()
        disciplina_turma = []
        for a in disciplina_turma1:
            disciplina_turma.append(a[0])

        # calcular o max de cada disciplina para ESSA turma:
        max_aula_dis = {}
        for a in disciplina_turma:
            cursor.execute(f"SELECT quantidade_de_aulas_semana FROM turmas_disciplina WHERE id = {a}")
            max_aulas = cursor.fetchone()
            max_aula_dis[a] = max_aulas[0]
        
        #atrelar o professor da turma à disciplina NESSE dia:
        disc_prof = []
        cursor.execute(f"SELECT professor_id, disciplina_id FROM turmas_professor_disciplina")
        prof_por_disc = cursor.fetchall()
        for a in prof_por_disc:
            if a[0] in prof_dia_turma:
                disc_prof.append((a[0], a[1]))
                
        print(f"turma{turma}", f"dia{dia[0]}", escolher_combinacoes_de_dia())