# Использование

## Как запустить для своего варианта

В корне репозитория ввести:

```
python problem_x <номер_варианта>
```

#### Пример для белорусов

Запуск решения первой задачи седьмого варианта:

```
python problem_1 7
```

## Задачи с пояснительной запиской

Программы для решения задач начиная с четвертой выводят в stdout текст
пояснительной записки в формате "Markdown с формулами в формате LaTeX".
Скомпилировать его в человеко-читаемый документ можно, например, на сайте
[stackedit.io](https://stackedit.io/) или с помощью
[вот этой приложеньки](https://typora.io/). Также в рабочую директорию под
именами `~figureче-то-там.png` сохраняются построенные диаграммы. Как их
вставить в этот документ — на совести пользователя.

В седьмой задаче скорее всего еще нужно будет переписать раздел "Выводы", так
как он написан для седьмого варианта.

## Зависимости

Прога работает только на Python 2. В принципе можно легко переписать и для
работы на Python 3, но мне лень кочеврыжиться.

Предварительно следует установить следующие пакеты:

* scipy
* numpy
* matplotlib
* jinja2 (для задач 4 и выше)

Сделать это можно следующей командой:

```
pip install scipy numpy matplotlib jinja2
```
