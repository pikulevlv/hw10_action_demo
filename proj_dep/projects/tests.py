from django.test import TestCase, Client
from .models import Staff, StaffListPosition, Direction, \
    Sertificate, Project, Stage, Role
from django.contrib.auth.models import User
from django.urls import reverse

import datetime


class TestModels(TestCase):
    # Что желательно проверить в models
    # 1. 100% методов классов
    # 2. Проверка создаваемых инстансов
    def setUp(self):
        self.sert_1 = Sertificate.objects.create(name='Prof_ERP')
        self.sert_2 = Sertificate.objects.create(name='Spec_ERP')
        self.sert_3 = Sertificate.objects.create(name='Expert')
        self.dir_1 = Direction.objects.create(name='ERP')
        self.dir_2 = Direction.objects.create(name='ZUP')
        self.dir_3 = Direction.objects.create(name='DO')
        self.sl_pos_1 = StaffListPosition.objects.create(name='KONS')
        self.sl_pos_2 = StaffListPosition.objects.create(name='DEV')
        self.sl_pos_3 = StaffListPosition.objects.create(name='PM')

        # staff_1
        self.staff_1 = Staff.objects.create(name='Inna', surname='Petrova',
                                      salary=140_000, is_staff=True)
        self.staff_1.sl_position.add(self.sl_pos_1)
        self.staff_1.direct.set([self.dir_1, self.dir_3])
        self.staff_1.serts.set([self.sert_1, self.sert_2])
        self.staff_1.serts.create(name='Prof_UU')
        self.staff_1.save()

        # staff_2
        self.staff_2 = Staff.objects.create(name='Andrey', surname='Mirzaev',
                                      salary=160_000,
                                      is_staff=True)
        self.staff_2.sl_position.add(self.sl_pos_2)
        self.staff_2.direct.set([self.dir_1, self.dir_2, self.dir_3])
        self.staff_2.serts.add(self.sert_1)
        self.staff_2.serts.add(self.sert_2)
        self.staff_2.serts.add(self.sert_3)
        self.staff_2.save()

        # staff_3
        self.staff_3 = Staff.objects.create(name='Leonid', surname='Pulman',
                                      salary=180_000,
                                      is_staff=True)
        self.staff_3.sl_position.add(self.sl_pos_3)
        self.staff_3.direct.set([self.dir_1, self.dir_3])
        self.staff_3.save()

        # proj_1
        self.proj_1 = Project.objects.create(name='Project_Alpha',
                                             description='A - description...')
        self.proj_1.direction.set([self.dir_1])
        self.stage_1_1 = Stage.objects.create(name='Stage_1_Alpha',
                                              proj=self.proj_1,
                                              start_plan=datetime.date(2020, 10, 1),
                                              start_fact=datetime.date(2020, 10, 5),
                                              end_plan=datetime.date(2020, 10, 25),
                                              end_fact=datetime.date(2020, 10, 28),
                                              exp_plan=500_000,
                                              exp_fact=515_000,
                                              is_completed=True)
        self.stage_1_2 = Stage.objects.create(name='Stage_2_Alpha',
                                              proj=self.proj_1,
                                              start_plan=datetime.date(2020, 11, 1),
                                              start_fact=datetime.date(2020, 11, 1),
                                              end_plan=datetime.date(2020, 11, 30),
                                              # end_fact=datetime.date(2020, 11, 30),
                                              exp_plan=800_000,
                                              # exp_fact= 800_000,
                                              is_completed=False)
        self.role_1_pm = Role.objects.create(name='PM in Alpha',
                                        proj=self.proj_1,
                                        staff=self.staff_3)
        self.role_1_pm.stages.set([self.stage_1_1, self.stage_1_2])

        self.role_1_kons = Role.objects.create(name='KONS in Alpha',
                                        proj=self.proj_1,
                                        staff=self.staff_1)
        self.role_1_kons.stages.set([self.stage_1_1, self.stage_1_2])

        self.role_1_dev = Role.objects.create(name='DEV in Alpha',
                                        proj=self.proj_1,
                                        staff=self.staff_2)
        self.role_1_dev.stages.set([self.stage_1_2])

    def tearDown(self):
        return

    def test_str(self):
        self.assertEqual(str(self.sert_1), self.sert_1.name)
        self.assertEqual(str(self.sert_2), self.sert_2.name)
        self.assertEqual(str(self.sert_3), self.sert_3.name)
        self.assertEqual(str(self.dir_1), self.dir_1.name)
        self.assertEqual(str(self.dir_2), self.dir_2.name)
        self.assertEqual(str(self.dir_3), self.dir_3.name)
        self.assertEqual(str(self.sl_pos_1), self.sl_pos_1.name)
        self.assertEqual(str(self.sl_pos_2), self.sl_pos_2.name)
        self.assertEqual(str(self.sl_pos_3), self.sl_pos_3.name)
        self.assertEqual(str(self.staff_1), f"{self.staff_1.name} "
                                            f"{self.staff_1.surname} "
                                            f"(id# {self.staff_1.id})")
        self.assertEqual(str(self.staff_2), f"{self.staff_2.name} "
                                            f"{self.staff_2.surname} "
                                            f"(id# {self.staff_2.id})")
        self.assertEqual(str(self.staff_3), f"{self.staff_3.name} "
                                            f"{self.staff_3.surname} "
                                            f"(id# {self.staff_3.id})")
        self.assertEqual(str(self.proj_1), self.proj_1.name)
        self.assertEqual(str(self.stage_1_1), f"{self.stage_1_1.name} "
                                            f"of {self.stage_1_1.proj}")
        self.assertEqual(str(self.stage_1_2), f"{self.stage_1_2.name} "
                                            f"of {self.stage_1_2.proj}")
        self.assertEqual(str(self.role_1_pm), f"{self.role_1_pm.name} "
                                            f"in {self.stage_1_1.proj}")
        self.assertEqual(str(self.role_1_kons), f"{self.role_1_kons.name} "
                                            f"in {self.role_1_kons.proj}")
        self.assertEqual(str(self.role_1_dev), f"{self.role_1_dev.name} "
                                            f"in {self.role_1_dev.proj}")

    def test_project_resource_count(self):
        self.assertEqual(self.proj_1.project_resource_count(), 3)


class TestViews(TestCase):
    """Testing Views with Client without launching server"""

    # Что желательно проверить в views
    # 1. status code для разных пользователей
    # 2. Проверка создаваемых из форм объектов
    # 3. Контекст
    # 3. Права

    def setUp(self):
        # Тест-клиент позволяет не поднимать сервер для выполнения запросов
        self.client = Client()
        # Создаем 3 пользователя с разными правами
        self.admin = User.objects.create_superuser('admin', 'test@test.com',
                                      '12345678qwerty')
        User.objects.create_user('staff', 'staff@test.com',
                                 '12345678qwerty', is_staff=True)
        User.objects.create_user('user', 'user@test.com',
                                 '12345678qwerty', is_staff=False)
        # Создаем атрибуты класса - инстансы Sertificate
        self.sert_1 = Sertificate.objects.create(name='Prof_ERP')
        self.sert_2 = Sertificate.objects.create(name='Spec_ERP')
        self.sert_3 = Sertificate.objects.create(name='Expert')
        # Создаем атрибуты класса - инстансы Direction
        self.dir_1 = Direction.objects.create(name='ERP')
        self.dir_2 = Direction.objects.create(name='ZUP')
        self.dir_3 = Direction.objects.create(name='DO')
        # Создаем атрибуты класса - инстансы StaffListPosition
        self.sl_pos_1 = StaffListPosition.objects.create(name='KONS')
        self.sl_pos_2 = StaffListPosition.objects.create(name='DEV')
        self.sl_pos_3 = StaffListPosition.objects.create(name='PM')

        # Создаем атрибут класса - инстанс Staff (staff_1)
        self.staff_1 = Staff.objects.create(name='Inna', surname='Petrova',
                                      salary=140_000, is_staff=True)
        self.staff_1.sl_position.add(self.sl_pos_1)
        self.staff_1.direct.set([self.dir_1, self.dir_3])
        self.staff_1.serts.set([self.sert_1, self.sert_2])
        self.staff_1.serts.create(name='Prof_UU')
        self.staff_1.save()

        # Создаем атрибут класса - инстанс Staff (staff_2)
        self.staff_2 = Staff.objects.create(name='Andrey', surname='Mirzaev',
                                      salary=160_000,
                                      is_staff=True)
        self.staff_2.sl_position.add(self.sl_pos_2)
        self.staff_2.direct.set([self.dir_1, self.dir_2, self.dir_3])
        self.staff_2.serts.add(self.sert_1)
        self.staff_2.serts.add(self.sert_2)
        self.staff_2.serts.add(self.sert_3)
        self.staff_2.save()

        # Создаем атрибут класса - инстанс Staff (staff_3)
        self.staff_3 = Staff.objects.create(name='Leonid', surname='Pulman',
                                      salary=180_000,
                                      is_staff=True)
        self.staff_3.sl_position.add(self.sl_pos_3)
        self.staff_3.direct.set([self.dir_1, self.dir_3])
        self.staff_3.save()

        # Создаем атрибут класса - инстанс Project (proj_1)
        self.proj_1 = Project.objects.create(name='Project_Alpha',
                                             description='A - description...')
        self.proj_1.direction.set([self.dir_1])
        # Создаем атрибут класса - инстанс Stage
        # (stage_1_1 - первый этап проекта)
        self.stage_1_1 = Stage.objects.create(name='Stage_1_Alpha',
                                              proj=self.proj_1,
                                              start_plan=datetime.date(2020, 10, 1),
                                              start_fact=datetime.date(2020, 10, 5),
                                              end_plan=datetime.date(2020, 10, 25),
                                              end_fact=datetime.date(2020, 10, 28),
                                              exp_plan=500_000,
                                              exp_fact=515_000,
                                              is_completed=True)
        # Создаем атрибут класса - инстанс Stage (stage_1_2 - второй этап проекта)
        self.stage_1_2 = Stage.objects.create(name='Stage_2_Alpha',
                                              proj=self.proj_1,
                                              start_plan=datetime.date(2020, 11, 1),
                                              start_fact=datetime.date(2020, 11, 1),
                                              end_plan=datetime.date(2020, 11, 30),
                                              # end_fact=datetime.date(2020, 11, 30),
                                              exp_plan=800_000,
                                              # exp_fact= 800_000,
                                              is_completed=False)
        # Создаем атрибут класса - инстанс Role
        # (роль в первом проекте для сотрудника)
        self.role_1_pm = Role.objects.create(name='PM in Alpha',
                                        proj=self.proj_1,
                                        staff=self.staff_3)
        # Связываем роль со стадиями проекта (в каких этапах проекта участвует)
        self.role_1_pm.stages.set([self.stage_1_1, self.stage_1_2])
        # Создаем атрибут класса - инстанс Role
        # (роль в первом проекте для сотрудника)
        self.role_1_kons = Role.objects.create(name='KONS in Alpha',
                                        proj=self.proj_1,
                                        staff=self.staff_1)
        # Связываем роль со стадиями проекта (в каких этапах проекта участвует)
        self.role_1_kons.stages.set([self.stage_1_1, self.stage_1_2])
        # Создаем атрибут класса - инстанс Role
        # (роль в первом проекте для сотрудника)
        self.role_1_dev = Role.objects.create(name='DEV in Alpha',
                                        proj=self.proj_1,
                                        staff=self.staff_2)
        # Связываем роль со стадиями проекта (в каких этапах проекта участвует)
        self.role_1_dev.stages.set([self.stage_1_2])

    def test_index(self):
        url = reverse('projects:index')
        response = self.client.get(url)
        # проверка кода ответа
        self.assertEqual(response.status_code, 200)
        # проверка содержимого в html-коде
        encoding = 'utf-8'
        text = response.content.decode(encoding)
        searched = '<h4><b>Team:</b>'
        self.assertTrue(searched in text)
        # проверка контекста на наличие и на тип
        self.assertTrue('staff_units' in response.context.keys())
        self.assertTrue(isinstance(response.context['staff_units'], (int)))
        self.assertTrue('proj_units' in response.context.keys())
        self.assertTrue(isinstance(response.context['proj_units'], (int)))
        self.assertTrue('dir_units' in response.context.keys())
        self.assertTrue(isinstance(response.context['dir_units'], (int)))
        self.assertTrue('sl_units' in response.context.keys())
        self.assertTrue(isinstance(response.context['sl_units'], (int)))
        self.assertTrue('sert_units' in response.context.keys())
        self.assertTrue(isinstance(response.context['sert_units'], (int)))
        self.assertTrue('active_page' in response.context.keys())
        self.assertTrue(isinstance(response.context['active_page'], (str)))
        self.assertEqual(response.context['active_page'], "1")

    def test_staff(self):
        url = reverse('projects:staff')
        response = self.client.get(url)
        # проверка кода ответа
        self.assertEqual(response.status_code, 200)
        # доступность кнопки под админом
        self.client.logout()
        # self.client.login(username='admin', password='12345678qwerty')
        # используем force_login(), чтобы не зависеть от логина и пароля
        self.client.force_login(self.admin)
        response = self.client.get(url)
        encoding = 'utf-8'
        text = response.content.decode(encoding)
        searched = 'class="btn btn-primary">Hair a new employee</a>'
        self.assertTrue(searched in text)
        self.client.logout()

        self.client.login(username='staff', password='12345678qwerty')
        response = self.client.get(url)
        text = response.content.decode(encoding)
        self.assertTrue(searched in text)
        self.client.logout()

        self.client.login(username='user', password='12345678qwerty')
        response = self.client.get(url)
        text = response.content.decode(encoding)
        self.assertTrue(searched in text)
        self.client.logout()

        # проверка контекста на наличие и на тип
        self.assertTrue('active_page' in response.context.keys())
        self.assertTrue(isinstance(response.context['active_page'], (str)))
        self.assertEqual(response.context['active_page'], "1")

    """Написать тесты для update, delete, staff_detail, staff, 
    registry, login, logout, create_staff, update_project, 
    delete_project, projects_detail, projects_page, update_role, 
    delete_role, roles_detail, roles_page, contact_page"""

    def test_permissions(self):
        """Authotization tests"""
        # Создаем словарь: ключ - адрес, значение - код ответа
        url_dict = {'/': 200,
                    f'/staff/{self.staff_1.id}/update/': 200,
                    f'/staff/{self.staff_1.id}/delete/': 200,
                    f'/staff/{self.staff_1.id}/': 200,
                    '/staff/': 200,
                    '/registry/': 200,
                    '/login/': 200,
                    '/create_staff/': 200,
                    f'/projects_page/{self.proj_1.id}/update/': 200,
                    f'/projects_page/{self.proj_1.id}/delete/': 200,
                    f'/projects_page/{self.proj_1.id}/': 200,
                    '/projects_page/': 200,
                    f'/roles_page/{self.role_1_pm.id}/update/': 200,
                    f'/roles_page/{self.role_1_pm.id}/delete/': 200,
                    f'/roles_page/{self.role_1_pm.id}/': 200,
                    '/roles_page/': 200,
                    '/contact_page/': 200}

        # for anonimous
        url_dict_anonimous = url_dict.copy()
        url_dict_anonimous[f'/staff/{self.staff_1.id}/update/'] = 302
        url_dict_anonimous[f'/staff/{self.staff_1.id}/delete/'] = 302
        url_dict_anonimous[f'/staff/{self.staff_1.id}/'] = 302
        url_dict_anonimous['/create_staff/'] = 302
        url_dict_anonimous[f'/projects_page/{self.proj_1.id}/update/'] = 302
        url_dict_anonimous[f'/projects_page/{self.proj_1.id}/delete/'] = 302
        url_dict_anonimous[f'/projects_page/{self.proj_1.id}/'] = 302
        url_dict_anonimous[f'/roles_page/{self.role_1_pm.id}/update/'] = 302
        url_dict_anonimous[f'/roles_page/{self.role_1_pm.id}/delete/'] = 302
        url_dict_anonimous[f'/roles_page/{self.role_1_pm.id}/'] = 302
        url_dict_anonimous['/contact_page/'] = 302

        self.client.logout()
        for url, code in url_dict_anonimous.items():
            response = self.client.get(url)
            self.assertEqual(response.status_code, code)
        # отельно тестируется logout
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)

        # for admin
        url_dict_admin = url_dict.copy()
        self.client.login(username='admin', password='12345678qwerty')
        for url, code in url_dict_admin.items():
            response = self.client.get(url)
            self.assertEqual(response.status_code, code)

        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        self.client.logout()

        # for staff
        url_dict_staff = url_dict.copy()
        url_dict_staff[f'/staff/{self.staff_1.id}/delete/'] = 403
        url_dict_staff[f'/projects_page/{self.proj_1.id}/delete/'] = 403
        url_dict_staff[f'/roles_page/{self.role_1_pm.id}/delete/'] = 403

        self.client.login(username='staff', password='12345678qwerty')
        for url, code in url_dict_staff.items():
            response = self.client.get(url)
            self.assertEqual(response.status_code, code)

        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        self.client.logout()

        # for user
        url_dict_user = url_dict.copy()
        url_dict_user[f'/staff/{self.staff_1.id}/update/'] = 403
        url_dict_user[f'/staff/{self.staff_1.id}/delete/'] = 403
        url_dict_user['/create_staff/'] = 403
        url_dict_user[f'/projects_page/{self.proj_1.id}/update/'] = 403
        url_dict_user[f'/projects_page/{self.proj_1.id}/delete/'] = 403
        url_dict_user[f'/roles_page/{self.role_1_pm.id}/update/'] = 403
        url_dict_user[f'/roles_page/{self.role_1_pm.id}/delete/'] = 403

        self.client.login(username='user', password='12345678qwerty')
        for url, code in url_dict_user.items():
            response = self.client.get(url)
            self.assertEqual(response.status_code, code)

        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        self.client.logout()
