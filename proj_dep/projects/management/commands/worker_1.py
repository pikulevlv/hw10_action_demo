from django.core.management.base import BaseCommand
from projects.models import Staff, StaffListPosition, Direction, Sertificate
from projects.models import Project, Stage, Role
from datetime import date


class Command(BaseCommand):
    help = 'Worker_1 with db'

    def handle(self, *args, **options):
        print('Hello from Worker_1.1')
        # Удаление
        Sertificate.objects.all().delete()
        Direction.objects.all().delete()
        StaffListPosition.objects.all().delete()
        Staff.objects.all().delete()

        # Creation
        sert_1 = Sertificate.objects.create(name='Prof_ERP')
        sert_2 = Sertificate.objects.create(name='Spec_ERP')
        sert_3 = Sertificate.objects.create(name='Expert')
        dir_1 = Direction.objects.create(name='ERP')
        dir_2 = Direction.objects.create(name='ZUP')
        sl_pos_1 = StaffListPosition.objects.create(name='KONS')
        sl_pos_2 = StaffListPosition.objects.create(name='DEV')
        sl_pos_3 = StaffListPosition.objects.create(name='PM')

        # unit #1
        unit_1 = Staff.objects.create(name='Sveta', surname='Molodtsova',
                                      salary=140_000, is_staff=True)
        unit_1.sl_position.add(sl_pos_2)
        unit_1.direct.set([dir_1, dir_2])
        unit_1.serts.set([sert_1, sert_2])
        unit_1.save()
        print(unit_1)

        #unit #2
        unit_2 = Staff.objects.create(name='Andrey', surname='Lobko',
                                      salary=160_000,
                                      is_staff=True)
        unit_2.sl_position.add(sl_pos_1)
        unit_2.direct.add(dir_1)
        unit_2.serts.add(sert_1)
        unit_2.serts.add(sert_2)
        unit_2.serts.add(sert_3)
        unit_2.serts.create(name='Prof_UU')
        unit_2.save()
        print(unit_2)

        # unit #3
        unit_3 = Staff.objects.create(name='Leonid', surname='Pulman',
                                      salary=180_000,
                                      is_staff=True)
        unit_3.sl_position.add(sl_pos_3)
        unit_3.direct.add(dir_1)
        unit_3.save()
        print(unit_3)
        
        # __________________________________________________
        
        print('Hello from Worker_1.2')
        # Удаление
        Project.objects.all().delete()
        Stage.objects.all().delete()
        Role.objects.all().delete()

        # Creation
        proj_1 = Project.objects.create(name="INFAPRIM_ZUP.Project", 
                                        description="new project...")
        proj_2 = Project.objects.create(name="TPE_ERP.Project",
                                        description="yet another project...")
        stage_1 = Stage.objects.create(name="INFAPRIM_ZUP.Project.Stage#1",
                                       proj=proj_1,
                                       start_plan=date(2020, 12, 14),
                                       end_plan=date(2021, 1, 20),
                                       exp_plan=305_000,
                                       is_completed=False
                                       )
        stage_2 = Stage.objects.create(name="INFAPRIM_ZUP.Project.Stage#2",
                                       proj=proj_1,
                                       start_plan=date(2021, 1, 21),
                                       end_plan=date(2021, 3, 20),
                                       exp_plan=405_000,
                                       is_completed=False
                                       )
        role_1 = Role.objects.create(name="PM", proj=proj_1)
        role_1.stages.add(stage_1, stage_2)
        role_1.staff = unit_3
        role_1.save()
        role_2 = Role.objects.create(name="KONS_UU", proj=proj_1)
        role_2.stages.add(stage_2)
        role_2.staff = unit_2
        role_2.save()
        print(proj_1)
        print(stage_1)
        print(stage_2)
        print(role_1, role_1)