from panda3d.core import Point3
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
import random

class SnakeGame(ShowBase):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.score_text = OnscreenText(text="Score: 0", pos=(-1.3, 0.9), scale=0.07)
        # Настройка камеры
        self.disableMouse()
        self.camera.setPos(0, -40, 30)
        self.camera.lookAt(0, 0, 0)
        
        # Инициализация змейки и еды
        self.snake = []
        self.snake_direction = (0, 0, 0)  # Начальная скорость: вправо по оси X
        self.create_snake()
        self.create_food()

        # Границы игрового поля
        self.field_boundaries = (-15, 15)  # Границы поля
        # Управление
        self.accept('arrow_up', self.change_direction, ['UP'])
        self.accept('arrow_down', self.change_direction, ['DOWN'])
        self.accept('arrow_left', self.change_direction, ['LEFT'])
        self.accept('arrow_right', self.change_direction, ['RIGHT'])

        # Создание стены из синих блоков
        self.create_wall()

        # Основной цикл игры
        self.taskMgr.add(self.move_snake, 'move_snake')
        self.food_position = self.food.getPos()

    
    def create_snake(self):
        """Создание змейки"""
        for i in range(5):
            snake_part = self.loader.loadModel("models/box")
            snake_part.setScale(1, 1, 1)
            snake_part.setColor(0, 1, 0)
            snake_part.setPos(i, 0, 0)
            snake_part.reparentTo(self.render)
            self.snake.append(snake_part)

    def create_food(self):
        """Создание еды для змейки"""
        self.food = self.loader.loadModel("models/box")
        self.food.setScale(1, 1, 1)
        self.food.setColor(1, 0, 0)
        self.food.setPos(random.randint(-15, 15), random.randint(-15, 15), 0)
        self.food.reparentTo(self.render)

    def create_wall(self):
        """Создание стены из синих блоков"""
        # Стена вдоль оси X
        for y in range(self.field_boundaries[0], self.field_boundaries[1] + 1):
            blue_block = self.loader.loadModel("models/box")
            blue_block.setScale(1, 1, 1)
            blue_block.setColor(0, 0, 1)  # Синий цвет
            blue_block.setPos(self.field_boundaries[0], y, 0)  # Левая стена
            blue_block.reparentTo(self.render)

            blue_block = self.loader.loadModel("models/box")
            blue_block.setScale(1, 1, 1)
            blue_block.setColor(0, 0, 1)  # Синий цвет
            blue_block.setPos(self.field_boundaries[1], y, 0)  # Правая стена
            blue_block.reparentTo(self.render)

        # Стена вдоль оси Y
        for x in range(self.field_boundaries[0], self.field_boundaries[1] + 1):
            blue_block = self.loader.loadModel("models/box")
            blue_block.setScale(1, 1, 1)
            blue_block.setColor(0, 0, 1)  # Синий цвет
            blue_block.setPos(x, self.field_boundaries[0], 0)  # Нижняя стена
            blue_block.reparentTo(self.render)

            blue_block = self.loader.loadModel("models/box")
            blue_block.setScale(1, 1, 1)
            blue_block.setColor(0, 0, 1)  # Синий цвет
            blue_block.setPos(x, self.field_boundaries[1], 0)  # Верхняя стена
            blue_block.reparentTo(self.render)

    def change_direction(self, direction):
        """Изменение направления движения змейки"""
        if direction == 'UP' and self.snake_direction != (0, -1, 0):
            self.snake_direction = (0, 1, 0)
        elif direction == 'DOWN' and self.snake_direction != (0, 1, 0):
            self.snake_direction = (0, -1, 0)
        elif direction == 'LEFT' and self.snake_direction != (1, 0, 0):
            self.snake_direction = (-1, 0, 0)
        elif direction == 'RIGHT' and self.snake_direction != (-1, 0, 0):
            self.snake_direction = (1, 0, 0)

    def move_snake(self, task):
        """Перемещение змейки"""
        head = self.snake[0]
        x, y, z = head.getPos()
        new_pos = Point3(x + self.snake_direction[0], y + self.snake_direction[1], z + self.snake_direction[2])

        # Проверка на выход за границы поля
        if new_pos.x < self.field_boundaries[0]:
            new_pos.x = self.field_boundaries[1]  # Возвращаем на другую сторону
        elif new_pos.x > self.field_boundaries[1]:
            new_pos.x = self.field_boundaries[0]  # Возвращаем на другую сторону

        if new_pos.y < self.field_boundaries[0]:
            new_pos.y = self.field_boundaries[1]  # Возвращаем на другую сторону
        elif new_pos.y > self.field_boundaries[1]:
            new_pos.y = self.field_boundaries[0]  # Возвращаем на другую сторону

        # Добавляем новый кусок тела змейки в начало
        new_head = self.loader.loadModel("models/box")
        new_head.setScale(1, 1, 1)
        new_head.setColor(0, 1, 0)
        new_head.setPos(new_pos)
        new_head.reparentTo(self.render)

        self.snake.insert(0, new_head)

        
        if self.snake[0].getPos() != self.food_position:
            tail = self.snake.pop()
            tail.removeNode()
        else:
            # Змейка съела еду
            self.food_position = self.food.getPos()
            self.food.setPos(random.randint(-15, 15), random.randint(-15, 15), 0)
            self.score += 1
            self.score_text.setText(f"Score: {self.score}")

        return task.cont

app = SnakeGame()
app.run()
