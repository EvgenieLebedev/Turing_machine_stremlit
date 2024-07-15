import streamlit as st
def main():

    class TuringMachine:
        def __init__(self, tape, initial_state, final_states, transition_function, initial_head_position=0):
            self.tape = list(tape)
            self.head_position = initial_head_position
            self.current_state = initial_state
            self.final_states = final_states
            self.transition_function = transition_function

        def set_head_position(self, position):
            self.head_position = position

        def get_head_position(self):
            return self.head_position

        def step(self):
            if self.head_position < 0 or self.head_position >= len(self.tape):
                st.error("Ошибка: Головка вышла за границы ленты")
                return None

            current_symbol = self.tape[self.head_position]
            action = self.transition_function.get((self.current_state, current_symbol))

            st.write(f"Текущее состояние: {self.current_state}, Текущий символ: {current_symbol}")
            st.write(f"Переход: {action}")

            if action:
                new_state, new_symbol, direction = action
                st.write(f"Новое состояние: {new_state}, Новый символ: {new_symbol}, Направление: {direction}")
                self.tape[self.head_position] = new_symbol
                self.current_state = new_state
                if direction == 'R':
                    self.head_position += 1
                elif direction == 'L':
                    self.head_position -= 1
                st.write(f"Состояние обновлено на: {self.current_state}")
                st.write(f"Позиция головки обновлена на: {self.head_position}")
            else:
                st.error("Переход не найден, машина останавливается")
            
            return self.head_position

        def is_halted(self):
            return self.current_state in self.final_states

        def reset(self, tape, initial_state):
            self.tape = list(tape)
            self.current_state = initial_state
            self.head_position = 0

        def __str__(self):
            tape_str = ''.join(self.tape)
            return f"State: {self.current_state}, Tape: {tape_str}, Head: {self.head_position}"

    # Универсальная функция для отображения и редактирования таблицы переходов
    def input_transition_function(tm):
        st.subheader('Таблица переходов')

        if not tm.transition_function:
            tm.transition_function = {}
            num_transitions = st.number_input('Количество переходов', min_value=1, max_value=20, value=4, key='num_transitions')
        else:
            num_transitions = st.number_input('Количество переходов', min_value=1, max_value=20, value=4, key='num_transitions')

        for i in range(num_transitions):
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                current_state = st.text_input(f'Текущее состояние {i+1}', value=tm.transition_function.get((f'q{i}', '0'), (f'q{i}', '0', 'R'))[0])
            with col2:
                current_symbol = st.text_input(f'Текущий символ {i+1}', value=tm.transition_function.get((f'q{i}', '0'), (f'q{i}', '0', 'R'))[1])
            with col3:
                new_state = st.text_input(f'Новое состояние {i+1}', value=tm.transition_function.get((f'q{i}', '0'), (f'q{i}', '0', 'R'))[0])
            with col4:
                new_symbol = st.text_input(f'Новый символ {i+1}', value=tm.transition_function.get((f'q{i}', '0'), (f'q{i}', '0', 'R'))[1])
            with col5:
                direction = st.selectbox(f'Направление {i+1}', ['L', 'R'], index=1)

            tm.transition_function[(current_state, current_symbol)] = (new_state, new_symbol, direction)

        return tm.transition_function


    # Функция для отображения Машины Тьюринга
    def display_turing_machine(tm):
        input_transition_function(tm)
        
        # Отображение ленты с выделением текущей позиции головки

        tape_display = ""
        for i, symbol in enumerate(tm.tape):
            if i == tm.get_head_position():
                tape_display += f"<b style='color:red;'>{symbol}</b>"
            else:
                tape_display += symbol
        tape_display_element = st.empty()

        tape_display_element.write(f"Tape: {tape_display}", unsafe_allow_html=True)
        st.write(f"Состяние: {tm.current_state}")
        st.write(f"Позиция головки чтения/записи: {tm.get_head_position()}")

        if st.button('Шаг'):
            tm.step()
            if tm.is_halted():
                st.write('Машина остановилась в одном из конечных состояний.')

        new_tape = ''
        new_tape = st.text_input('Введите новую ленту', value='')
        if st.button('Применить изменения'):
            tm.reset(new_tape, tm.current_state)
            tm.head_position = 0
            tape_display = ""
            for i, symbol in enumerate(tm.tape):
                if i == tm.get_head_position():
                    tape_display += f"<b style='color:red;'>{symbol}</b>"
                else:
                    tape_display += symbol
            tape_display_element.empty()  
            tape_display_element.write(f"Tape: {tape_display}", unsafe_allow_html=True)  # Записываем новую ленту
            st.session_state['tm'] = tm

    # Интерфейс Streamlit
    st.title('Машина Тьюринга')
    st.write('Редактирование таблицы функции переходов')

    if 'tm' not in st.session_state:
        st.session_state['initial_tape'] = '000000'
        st.session_state['initial_state'] = 'q0'
        st.session_state['initial_final_states'] = 'qf'

        tape = st.session_state['initial_tape']
        initial_state =  value=st.session_state['initial_state']
        final_states_input = value=st.session_state['initial_final_states']
        final_states = set(final_states_input.split(','))

        tm = TuringMachine(tape, initial_state, final_states, None)
        st.session_state['tm'] = tm
    else:
        tm = st.session_state['tm']

    display_turing_machine(tm)

    st.session_state['tm'] = tm

if __name__ == "__main__":
    main()