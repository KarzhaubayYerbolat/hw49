В моем приложении я добавил модуль appuser, где описаны модели пользователей и команд, представления Login and Logout, необходимые шаблоны.
чтобы пользователи могли манипулировать над задачами:

Delete task - Может только инициатор задания или суперпользователь.

Edit task - Может только инициатор и статус задания должна быть "New"

Take task - Может только участник группы, установленной в поле responsilbe_group. Task.executor должен быть "None" и статус
не должен быть "Rejected"

Reject task - Может только тимлидер группы, установленной в поле responsilbe_group

Task solve - Может только исполнитель задания

Сhange Task Executor - Может только тимлидер группы
