#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import os
import sys
import click
from dotenv import load_dotenv


@click.group()
def cli():
    pass


@cli.command()
@click.argument('data')
@click.option("-n", "--name")
@click.option("-g", "--group")
@click.option("-gr", "--grade")
def add(data, name, group, grade):
    if os.path.exists(data):
        load_dotenv()
        dotenv_path = os.getenv("STUDENTS_DATA")
        if not dotenv_path:
            click.secho("The file is missing", fg="red")
            sys.exit(1)
        if os.path.exists(dotenv_path):
            students = load_students(dotenv_path)
        else:
            students = []
        students.append(
            {
                'name': name,
                'group': group,
                'grade': grade,
            }
        )
        with open(dotenv_path, "w", encoding="utf-8") as fout:
            json.dump(students, fout, ensure_ascii=False, indent=4)
        click.secho("Студент добавлен", fg='green')
    else:
        click.secho("The file is missing", fg="red")


@cli.command()
@click.argument('filename')
def display(filename):
    # Заголовок таблицы.
    if os.path.exists(filename):
        load_dotenv()
        dotenv_path = os.getenv("STUDENTS_DATA")
        if not dotenv_path:
            click.secho('Файла нет', fg='red')
            sys.exit(1)
        if os.path.exists(dotenv_path):
            students = load_students(dotenv_path)
        else:
            students = []
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "№",
                "Ф.И.О.",
                "Группа",
                "Успеваемость"
            )
        )
        print(line)

        # Вывести данные о всех студентах.
        for idx, student in enumerate(students, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>15} |'.format(
                    idx,
                    student.get('name', ''),
                    student.get('group', ''),
                    student.get('grade', 0)
                )
            )
        print(line)


@cli.command()
@click.argument('filename')
def select(filename):
    if os.path.exists(filename):
        load_dotenv()
        dotenv_path = os.getenv("STUDENTS_DATA")
        if not dotenv_path:
            click.secho("The file is missing", fg="red")
            sys.exit(1)
        if os.path.exists(dotenv_path):
            students = open(dotenv_path)
        else:
            students = []
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "№",
                "Ф.И.О.",
                "Группа",
                "Успеваемость"
            )
        )
        print(line)
        # Инициализировать счетчик.
        count = 0
        # Проверить сведения студентов из списка.
        for student in students:
            grade = list(map(int, student.get('grade', '').split()))
            if sum(grade) / max(len(grade), 1) >= 4.0:
                print(
                    '{:>4} {}'.format('*', student.get('name', '')),
                    '{:>1} {}'.format('группа №', student.get('group', ''))
                )
                count += 1
        print(line)


def load_students(filename):
    with open(filename, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main():
    cli()


if __name__ == '__main__':
    main()
