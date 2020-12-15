from django.core.management.base import BaseCommand
from projects.models import Staff, StaffListPosition, Direction, Sertificate
from projects.models import Project, Stage, Role
from datetime import date


class Command(BaseCommand):
    help = 'Extractor_1 with db'

    def handle(self, *args, **options):
        print('Hello from Extractor_1.1!\n')

        # Извлечение
        sert_1 = Sertificate.objects.filter(name='Prof_ERP')
        sert_2 = Sertificate.objects.filter(name='Spec_ERP')
        sert_3 = Sertificate.objects.filter(name='Expert')

        dir_1 = Direction.objects.filter(name='ERP')
        dir_2 = Direction.objects.filter(name='ZUP')

        sl_pos_1 = StaffListPosition.objects.filter(name='KONS')
        sl_pos_2 = StaffListPosition.objects.filter(name='DEV')
        sl_pos_3 = StaffListPosition.objects.filter(name='PM')

        # units #1-3
        unit_1 = Staff.objects.get(name='Sveta', surname='Molodtsova',
                                      salary=140_000, is_staff=True)
        unit_2 = Staff.objects.get(name='Andrey', surname='Lobko',
                                      salary=160_000,
                                      is_staff=True)
        unit_3 = Staff.objects.get(name='Leonid', surname='Pulman',
                                      salary=180_000,
                                      is_staff=True)
        proj_1 = Project.objects.get(name="INFAPRIM_ZUP.Project",
                                        description="new project...")
        stage_1 = Stage.objects.get(name="INFAPRIM_ZUP.Project.Stage#1",
                                       proj=proj_1,
                                       start_plan=date(2020, 12, 14),
                                       end_plan=date(2021, 1, 20),
                                       exp_plan=305_000,
                                       is_completed=False)
        stage_2 = Stage.objects.get(name="INFAPRIM_ZUP.Project.Stage#2",
                                       proj=proj_1,
                                       start_plan=date(2021, 1, 21),
                                       end_plan=date(2021, 3, 20),
                                       exp_plan=405_000,
                                       is_completed=False)
        role_1 = Role.objects.get(name="PM", proj__name="INFAPRIM_ZUP.Project")

        # # __________________________________________________
        # Анализ
        print(f"Какие sl_position у unit_1 ({unit_1.name} {unit_1.surname})?")
        for slp in unit_1.sl_position.all():
            print('-', slp.name)
        print("Какие direct у unit_1 ?")
        for d in unit_1.direct.all():
            print('-', d.name)
        print("Какие serts у unit_1 ?")
        for srt in unit_1.serts.all():
            print('-', srt.name)
        print("Какие роли у сотрудника с фамилией Lobko во всех проектах?")
        lobko = Staff.objects.get(surname="Lobko")
        lobko_id = lobko.id
        for r in Role.objects.filter(staff__id=lobko_id):
            print('-', r.name)

        print(f"Перечислите фамилии всех PM.")
        for s in Staff.objects.filter(sl_position__name="PM"):
            print('-', s.surname)
        print("Существует ли сотрудники по направлению 'УХ'?")
        print('-', Direction.objects.filter(name='УХ').exists())
        print("Сколько сотрудников по направлению 'ERP'?")
        print('-', Direction.objects.filter(name='ERP').count())

        print("Какие есть проекты?")
        for p in Project.objects.all():
            print('-', p.name)

        print("Какие этапы в каждом из проектов?")
        for p in Project.objects.all():
            print('В проекте', p.name, 'есть этапы:')
            id_ = p.id
            for s in Stage.objects.filter(proj__id=id_):
                print('--', s.name)

        print("Тот же вопрос, но добавьте роли задействованных "
              " участников в разрезе этапов.")
        for p in Project.objects.all():
            print('В проекте', p.name, 'есть этапы:')
            p_id = p.id
            for s in Stage.objects.filter(proj__id=p_id):
                print('--', s.name, ', в котором задействован(ы):')
                s_id = s.id
                for r in Role.objects.filter(stages__id=s_id):
                    print('----', r.name, r.staff.name, r.staff.surname)

        print("Какова суммарная плановая стоимость этапов "
              "для каждого проекта?")
        for p in Project.objects.all():
            total = Stage.objects.filter(proj__id=p.id).count()
            summa = 0
            for s in Stage.objects.filter(proj__id=p.id):
                summa += s.exp_plan
            print(f'- {p.name} состоит из {total} этапов общей стоимостью '
                  f'{summa} рублей.')

        print("Каковы даты начала и завершения для каждого проекта?")
        for p in Project.objects.all():
            stage_starts = []
            stage_ends = []
            for s in Stage.objects.filter(proj__id=p.id):
                stage_starts.append(s.start_plan)
                stage_ends.append(s.end_plan)
            print(f'- {p.name} стартует {min(stage_starts)} '
                  f'и завершается {max(stage_ends)}.')