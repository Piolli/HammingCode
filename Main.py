from tkinter import *
import ScrollFrame
import random
import math

class HammingCodeWindow:

    def __init__(self, message):
        self.root = Tk()
        # root.geometry("500x500")
        self.message = ""

        settings_frame = Frame(self.root)
        settings_frame.grid(row=0, column=0)

        Label(settings_frame, text="Количество сообщений").grid(row=0, column=0)
        self.number_messages_entry = Entry(settings_frame)
        self.number_messages_entry.grid(row=0, column=1)

        self.calculate_params_and_model_button = Button(settings_frame,
                                                        text="Рассчитать параметры и макет кода",
                                                        command=self.callback_calculate_params_and_model)
        self.calculate_params_and_model_button.grid(row=1, column=0, columnspan=2)

        self.param_count_info_bits    = Label(settings_frame, text="Nи = ")
        self.param_count_control_bits = Label(settings_frame, text="Nк = ")
        self.param_count_all_bits     = Label(settings_frame, text="N = ")

        self.param_count_info_bits.grid(row=2, column=0)
        self.param_count_control_bits.grid(row=3, column=0)
        self.param_count_all_bits.grid(row=4, column=0)

        # For message_frame
        self.messages = []
        self.entries_matrix = []
        # Parity bits entries
        self.parity_bits_labels = []
        # Hamming code return params for message
        self.hamming_code_for_message = []

        self.position_of_control_bits = []

        self.message_parent_frame = Frame(self.root)
        self.message_parent_frame.grid(row=1, column=0)

        self.root.mainloop()

    def callback_calculate_params_and_model(self):
        """DELETE ALL WIDGETS FROM FRAMES"""
        try:
            count_messages = int(self.number_messages_entry.get())
            count_reiqure_bits = int(math.ceil(math.log2(count_messages)))
            i, k, n = self.calculate_params_from_int(count_reiqure_bits)
            self.param_count_info_bits['text']    = "Nи = %d" % i
            self.param_count_control_bits['text'] = "Nк = %d" % k
            self.param_count_all_bits['text']     = "N = %d" % n

            self.create_model_frame(n, count_messages)

        except ValueError:
            print("ValueError in callback_calculate_params_and_model()")
            pass

    def create_model_frame(self, n, count_messages):
        for widget in self.message_parent_frame.winfo_children():
            widget.destroy()
        self.entries_matrix.clear()
        self.messages.clear()
        self.parity_bits_labels.clear()
        self.hamming_code_for_message.clear()
        self.position_of_control_bits.clear()

        self.messages_frame = ScrollFrame.VerticalScrolledFrame(self.message_parent_frame)
        self.messages_frame.grid(row=0, column=0)


        # Create model of hamming code
        positions_control_bits = self.get_postions_of_control_bits(n)
        self.position_of_control_bits = positions_control_bits
        # Number of line title
        Label(self.messages_frame.interior, text="№").grid(row=0, column=0)
        # Parity bit title
        Label(self.messages_frame.interior, text="БЧ").grid(row=0, column=n+1)
        # Create title for table
        for i in range(1, n + 1):
            if i in positions_control_bits:
                Label(self.messages_frame.interior, text="К%d" % i).grid(row=0, column=i, sticky="n")
            else:
                Label(self.messages_frame.interior, text="И%d" % i).grid(row=0, column=i, sticky="n")

        # Array of all entries of bits
        self.entries_matrix = [[0 for j in range(n)] for i in range(count_messages)]
        # Parity bits
        self.parity_bits_labels = [0 for i in range(count_messages)]
        # Create entries and random values for each
        for i in range(count_messages):
            Label(self.messages_frame.interior, text=str(i+1)).grid(row=i+1, column=0)
            self.parity_bits_labels[i] = Label(self.messages_frame.interior, text="-")
            self.parity_bits_labels[i].grid(row=i+1, column=n+1)
            for j in range(n):
                self.entries_matrix[i][j] = Entry(self.messages_frame.interior, width=1)
                if (j+1) not in positions_control_bits:
                    message_bit = str(random.randint(0, 1))
                    self.entries_matrix[i][j].insert(0, message_bit)
                else:
                    self.entries_matrix[i][j].insert(0, "-")
                self.entries_matrix[i][j].grid(row=i+1, column=j+1)

        self.messages_frame.update()
        # print(self.messages)


        hamming_code_button = Button(self.message_parent_frame, text="Рассчитать код",
                                     command=self.callback_calculate_hamming_code)
        hamming_code_button.grid(row=1, column=0)

        check_error_button = Button(self.message_parent_frame, text="Проверить на ошибки",
                                     command=self.callback_check_error)
        check_error_button.grid(row=2, column=0)

        # For print error messages into this
        self.out_error_message = Listbox(self.message_parent_frame, selectmode=SINGLE, width=35)
        self.out_error_message.grid(row=3, column=0)

    def callback_check_error(self):
        self.out_error_message.delete(0, END)

        messages = ["" for i in range(len(self.entries_matrix))]
        # Get messages from entries matrix
        for i in range(len(self.entries_matrix)):
            for j in range(len(self.entries_matrix[i])):
                # if (j+1) not in self.position_of_control_bits:
                value_bit = self.entries_matrix[i][j].get()
                messages[i] += value_bit

        print("second calculate", messages)

        # Calculate for each message hamming code
        new_hamming_code_entries_get = []
        for message in messages:
            int_array_message = [int(s) for s in message]
            new_hamming_code_entries_get.append(int_array_message)
        # for i in range(len(messages)):
        #     code, matrix, n, k, parity_bite = self.new_hamming_code(messages[i])
            # For check error
            # new_hamming_code_entries_get.append(code)

        for i in range(len(self.hamming_code_for_message)):
            error_position = self.new_check_error(new_hamming_code_entries_get[i],
                                                  self.hamming_code_for_message[i][1],
                                                  self.hamming_code_for_message[i][2],
                                                  self.hamming_code_for_message[i][3],
                                                  self.hamming_code_for_message[i][4])

            if error_position == -2:
                self.out_error_message.insert(END, "№{0} две ошибки\n".format(i+1))
            elif error_position > -1:
                self.out_error_message.insert(END, "№{0} ошибка в {1} бите исправлена\n".format(i+1, error_position))
                self.entries_matrix[i][error_position-1].delete(0, END)
                right_bit = 0 if new_hamming_code_entries_get[error_position-1] == 1 else 1
                self.entries_matrix[i][error_position-1].insert(0, str(right_bit))



    def callback_calculate_hamming_code(self):
        self.hamming_code_for_message.clear()
        self.messages = ["" for i in range(len(self.entries_matrix))]
        # Get messages from entries matrix
        for i in range(len(self.entries_matrix)):
            for bit_entry in self.entries_matrix[i]:
                value_bit = bit_entry.get()
                if value_bit != '-':
                    self.messages[i] += value_bit

        print("first calculate", self.messages)

        # Calculate for each message hamming code
        for i in range(len(self.messages)):
            code, matrix, n, k, parity_bite = self.new_hamming_code(self.messages[i])
            self.parity_bits_labels[i]['text'] = str(parity_bite)
            # For check error
            self.hamming_code_for_message.append((code, matrix, n, k, parity_bite))
            for j in range(len(self.entries_matrix[i])):
                self.entries_matrix[i][j].delete(0, END)
                self.entries_matrix[i][j].insert(0, str(code[j]))




    def calculate_params(self, message):
        # Control bits count
        k = 0

        # Information bits count
        i = len(message)

        # Sum of k and i
        n = 0

        message_len = i

        if message_len == 1:
            k = 2
        elif 2 <= message_len <= 4:
            k = 3
        elif 5 <= message_len <= 11:
            k = 4
        elif 12 <= message_len <= 26:
            k = 5
        elif 27 <= message_len <= 57:
            k = 6

        n = k + i

        return i, k, n

    def calculate_params_from_int(self, count):
        return self.calculate_params("".join('0' for k in range(count)))

    def get_postions_of_control_bits(self, n):
        # This is positions of control bits
        two_in_pow = []


        number_pow = 0
        calc_number = 2 ** number_pow

        while calc_number < n:
            two_in_pow.append(2**number_pow)
            number_pow += 1
            calc_number = 2 ** number_pow

        return two_in_pow

    # def hamming_code(self):
    #     positions_control_bits = self.get_postions_of_control_bits()
    #     # Message consist of int array
    #     info_bits = self.information_bits.copy()
    #     # Compute hamming code
    #     info_and_control_bits = []
    #
    #     # Create the model of hamming code
    #     for i in range(1, self.n+1):
    #         if i in positions_control_bits:
    #             info_and_control_bits.append(0)
    #         else:
    #             info_and_control_bits.append(info_bits.pop(0))
    #
    #
    #
    #     print("OLD WO:",info_and_control_bits)
    #
    #     # 1, 2, 4 -> 0, 1, 3 -> print indexes
    #     # Get positions for each control position bits for perform sum of bits on get positions
    #     positions_for_calculate = []
    #     for position_control_bit in positions_control_bits:
    #         index_control = position_control_bit - 1
    #         temp_positions = []
    #         for i in range(index_control, self.n, 2**(index_control+1)):
    #             for j in range(i, i + index_control+1):
    #                 # print(j+1, end=" ")
    #                 temp_positions.append(j+1)
    #             # print()
    #         positions_for_calculate.append(temp_positions.copy())
    #         temp_positions.clear()
    #
    #
    #     # print(positions_for_calculate)
    #
    #     # Calculate control bits [0 or 1]
    #     control_bits_result = [0 for i in range(self.k)]
    #     for i in range(len(control_bits_result)):
    #         for value_on_control_position in positions_for_calculate[i]:
    #             if value_on_control_position <= self.n:
    #                 control_bits_result[i] += info_and_control_bits[value_on_control_position-1]
    #         control_bits_result[i] %= 2
    #
    #     # print(control_bits_result)
    #
    #
    #     current_position = 0
    #     for position_control_bit in positions_control_bits:
    #         info_and_control_bits[position_control_bit-1] = control_bits_result[current_position]
    #         current_position += 1
    #
    #     # Add at the last of code bits
    #     bite_of_even = sum(info_and_control_bits) % 2
    #     # print("\t","".join(str(k) for k in info_and_control_bits))
    #     return [info_and_control_bits.copy(), control_bits_result.copy(), positions_for_calculate.copy(), bite_of_even]
    #
    # def check_error(self, code_with_params):
    #     info_and_control_bits = code_with_params[0]
    #     control_bits_result = code_with_params[1]
    #     positions_for_calculate = code_with_params[2]
    #     bite_of_even = code_with_params[3]
    #
    #     if sum(info_and_control_bits) % 2 == bite_of_even:
    #         print("Ошибки нет")
    #         return
    #
    #     without_control_result_hamming_code = info_and_control_bits.copy()
    #     for position in self.get_postions_of_control_bits():
    #         without_control_result_hamming_code[position-1] = 0
    #
    #     print("WO:", without_control_result_hamming_code)
    #
    #
    #     # Calculate NEW control bits [0 or 1]
    #     check_control_bits_result = [0 for i in range(self.k)]
    #     for i in range(len(check_control_bits_result)):
    #         for value_on_control_position in positions_for_calculate[i]:
    #             if value_on_control_position <= self.n:
    #                 check_control_bits_result[i] += without_control_result_hamming_code[value_on_control_position - 1]
    #         check_control_bits_result[i] %= 2
    #
    #     print("NEW control bits:", check_control_bits_result)
    #     print("old control bits:", control_bits_result)
    #     print()
    #     print("NEW code:", info_and_control_bits)
    #
    #     pass

    def new_hamming_code(self, message):
        self.message = message
        i, k, n = self.calculate_params(message)

        def get_binary_matrix(count, k):
            numbers_str = [str(bin(k)).replace("0b", "") for k in range(1, count+1)]
            numbers = [list(map(int, numbers_str[i])) for i in range(len(numbers_str))]
            # print(numbers)
            for i in range(len(numbers)):
                number_len = len(numbers[i])
                if number_len < k:
                    for j in range(k - number_len):
                        numbers[i].insert(0, 0)

                numbers[i].reverse()

            return numbers


        numbers_matrix = get_binary_matrix(n, k)

        # Create model of hamming code
        positions_control_bits = self.get_postions_of_control_bits(n)
        # Message consist of int array
        information_bits = [int(message[i]) for i in range(len(message))]
        # Compute hamming code
        info_and_empty_control_bits = []

        # Create the model of hamming code
        for i in range(1, n + 1):
            if i in positions_control_bits:
                info_and_empty_control_bits.append(0)
            else:
                info_and_empty_control_bits.append(information_bits.pop(0))

        # print(info_and_empty_control_bits)
        # print(numbers_matrix)

        # Calculate controls bits
        control_rows_matrix_transfrom = []
        control_bits = [0 for i in range(k)]
        for i in range(k):
            control_row = [numbers_matrix[j][i] for j in range(n)]
            control_rows_matrix_transfrom.append(control_row)
            control_bits[i] = sum([info_and_empty_control_bits[j] * control_row[j] for j in range(n)]) % 2

        control_iter = 0
        for position in positions_control_bits:
            info_and_empty_control_bits[position-1] = control_bits[control_iter]
            control_iter += 1

        print("Hamming code:", info_and_empty_control_bits)

        parity_bite = sum(info_and_empty_control_bits) % 2

        return info_and_empty_control_bits, numbers_matrix, n, k, parity_bite

    def new_check_error(self, code, transformation_matrix, n, k, parity_bite):
        sum_is_equls = False

        if sum(code) % 2 == parity_bite:
            sum_is_equls = True


        # Calculate controls bits
        control_rows_matrix_transfrom = []
        control_bits = [0 for i in range(k)]
        for i in range(k):
            control_row = [transformation_matrix[j][i] for j in range(n)]
            control_rows_matrix_transfrom.append(control_row)
            control_bits[i] = sum([code[j] * control_row[j] for j in range(n)]) % 2

        control_bits.reverse()

        print(control_bits)

        position_error_bit = int("".join(str(s) for s in control_bits), 2)
        # print("error bit postion:", position_error_bit)

        if position_error_bit == 0:
            print("Ошибок не найдено")
            return -1
        elif sum_is_equls and position_error_bit != 0:
            print("Найдено две ошибки")
            return -2
        elif not sum_is_equls and position_error_bit != 0:
            print("Найдена ошибка в", position_error_bit, "бите")
            return position_error_bit





# messages = ["0101", "0100", "1101", "0000", "1111", "0001", "0111", "1110"]
# messages = ["010101", "0100111", "11010000", "00001111", "111110101", "00011001", "01110", "11101"]
# messages = ["111011"]
# messages = ["0101"]

# for message in messages:
#     print(message, end=" ")
#     hamming = HammingCodeWindow(message)
#     code = hamming.hamming_code()
#     print("old code", code[0])
#     code[0][2] = 0 if code[0][2] == 1 else 1
#     hamming.check_error(code)
#
#     print("-----------")

hamming = HammingCodeWindow("010100")
code, matrix, n, k, parity_bite = hamming.new_hamming_code("100100101110001")
code[5] = 1
code[6] = 0
hamming.new_check_error(code, matrix, n, k, parity_bite)