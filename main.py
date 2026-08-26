import flet as ft

def main(page: ft.Page):
    # Настройки экрана мобильного приложения
    page.title = "Калькулятор Перекупа"
    page.theme_mode = ft.ThemeMode.DARK # Пацанская темная тема
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    # Создаем текстовые поля для ввода данных
    sell_price = ft.TextField(label="Почем продал (руб)", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    buy_price = ft.TextField(label="Почем взял (руб)", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    repair_costs = ft.TextField(label="Че по чем ремонт (руб)", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    hidden_costs = ft.TextField(label="Заправлял или пожет пробивал авто(руб)", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    
    # Текстовые поля для вывода результатов
    result_total_costs = ft.Text(value="Всего расходов: 0 руб", size=18, color="blue")
    result_profit = ft.Text(value="Твой заработок: 0 руб", size=22, weight="bold")
    result_verdict = ft.Text(value="", size=16, italic=True)

    # Алгоритм расчета при нажатии на кнопку
    def calculate_click(e):
        try:
            # Парсим введенные значения в целые числа
            sell = int(sell_price.value)
            buy = int(buy_price.value)
            repair = int(repair_costs.value)
            hidden = int(hidden_costs.value)
            
            # Математика перекупа
            total_costs = buy + repair + hidden
            profit = sell - total_costs
            
            # Выводим цифры на экран
            result_total_costs.value = f"Всего расходов: {total_costs:,} руб"
            result_profit.value = f"Чистая прибыль: {profit:,} руб"
            
            # Логика вердиктов
            if profit > 50000:
                result_profit.color = "green"
                result_verdict.value = "Ваяяяя да ты машина, перекуп от бога 🚀"
            elif profit > 0:
                result_profit.color = "blue"
                result_verdict.value = "Ну копеечку заработал 🛠"
            else:
                result_profit.color = "red"
                result_verdict.value = "Ну ты и ведрище взял! ⚠️"
                
        except ValueError:
            result_verdict.value = "Бро, вводи только целые числа без букв и пробелов!"
            result_verdict.color = "red"
            
        page.update() # Обновляем экран смартфона

    # Кнопка расчета (ИСПРАВЛЕНО: используем content вместо text)
    calc_button = ft.ElevatedButton(
        content=ft.Text("Ну-ка сколько ты там поднял 💪"), 
        on_click=calculate_click, 
        width=250
    )

    # Собираем интерфейс на экране смартфона
    page.add(
        ft.Text("⚙️ Калькулятор перекупа ⚙️", size=30, weight="bold", color="blue"),
        ft.Container(height=10),
        buy_price,
        repair_costs,
        hidden_costs,
        sell_price,
        ft.Container(height=15),
        calc_button,
        ft.Container(height=15),
        result_total_costs,
        result_profit,
        result_verdict
    )

# Запуск приложения
ft.app(target=main)
