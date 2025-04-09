import tkinter as tk
from tkinter import messagebox, simpledialog
import json

class TestApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Создание и тестирование")
        self.current_test = {"theory": "", "questions": []}
        self.current_question_index = 0
        self.score = 0
        self.menu()

    def clear_widgets(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def create_label(self, text):
        label = tk.Label(self.master, text=text, wraplength=500, justify="left")
        label.pack(pady=5)

    def create_button(self, text, command):
        button = tk.Button(self.master, text=text, command=command)
        button.pack(pady=5)

    def menu(self):
        self.clear_widgets()
        self.create_label("Выберите действие:")
        self.create_button("Создать тест", self.create_test)
        self.create_button("Загрузить тест", self.load_test)

    def create_test(self):
        self.clear_widgets()
        self.create_label("Создание нового теста")
        self.create_button("Добавить теорию", self.add_theory)
        self.create_button("Добавить вопрос", self.add_question)
        self.create_button("Сохранить тест", self.save_test)
        self.create_button("Назад в меню", self.menu)

    def add_theory(self):
        theory_text = simpledialog.askstring("Теория", "Введите теоретический материал:")
        if theory_text:
            self.current_test["theory"] = theory_text

    def add_question(self):
        question = simpledialog.askstring("Вопрос", "Введите текст вопроса:")
        if not question:
            return
            
        options = []
        for i in range(4):
            option = simpledialog.askstring("Вариант ответа", f"Введите вариант ответа {i+1}:")
            if option:
                options.append(option)
        
        if not options:
            return
            
        answer = simpledialog.askstring("Правильный ответ", "Введите правильный вариант ответа:")
        
        if answer in options:
            self.current_test["questions"].append({
                "question": question,
                "options": options,
                "answer": answer
            })
            messagebox.showinfo("Успех", "Вопрос добавлен!")
        else:
            messagebox.showerror("Ошибка", "Правильный ответ должен совпадать с одним из вариантов!")

    def save_test(self):
        filename = simpledialog.askstring("Сохранение", "Введите имя файла для сохранения (без расширения):")
        if filename:
            with open(f"{filename}.json", "w", encoding="utf-8") as f:
                json.dump(self.current_test, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", "Тест сохранен!")

    def load_test(self):
        filename = simpledialog.askstring("Загрузка", "Введите имя файла для загрузки (без расширения):")
        if filename:
            try:
                with open(f"{filename}.json", "r", encoding="utf-8") as f:
                    self.current_test = json.load(f)
                messagebox.showinfo("Успех", "Тест загружен!")
                self.show_theory()
            except FileNotFoundError:
                messagebox.showerror("Ошибка", "Файл не найден!")

    def show_theory(self):
        self.clear_widgets()
        if self.current_test["theory"]:
            self.create_label("Теоретическая часть:")
            self.create_label(self.current_test["theory"])
        else:
            self.create_label("Теоретическая часть отсутствует.")
        
        self.create_button("Перейти к вопросам", self.start_test)
        self.create_button("Вернуться в меню", self.menu)

    def start_test(self):
        if not self.current_test["questions"]:
            messagebox.showwarning("Внимание", "В тесте нет вопросов!")
            self.menu()
            return
            
        self.current_question_index = 0
        self.score = 0
        self.display_question()

    def display_question(self):
        if self.current_question_index < len(self.current_test["questions"]):
            question = self.current_test["questions"][self.current_question_index]

            self.clear_widgets()
            self.create_label(f"Вопрос {self.current_question_index + 1} из {len(self.current_test['questions'])}")
            self.create_label(question["question"])

            for option in question["options"]:
                self.create_button(option, lambda opt=option: self.check_answer(opt))
        else:
            self.show_result()

    def check_answer(self, selected_option):
        correct_answer = self.current_test["questions"][self.current_question_index]["answer"]
        if selected_option == correct_answer:
            self.score += 1
        self.current_question_index += 1
        self.display_question()

    def show_result(self):
        self.clear_widgets()
        self.create_label(f"Тест завершен! Правильных ответов: {self.score} из {len(self.current_test['questions'])}")
        self.create_button("Вернуться в меню", self.menu)


if __name__ == "__main__":
    root = tk.Tk()
    app = TestApp(root)
    root.mainloop()