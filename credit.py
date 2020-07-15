card_number = int(input("Number: "))

card_list = [int(x) for x in str(card_number)]

#print(card_list)


def is_valid(card_list):
    sum_2_other = 0
    sum_other = 0
    for x in range(len(card_list) - 2, -1, -2):
        d = (card_list[x] * 2)
        d = [int(s) for s in str(d)]
        sum_2_other += sum(d)
    for i in range(len(card_list) - 1, -1, -2):
        sum_other += card_list[i]
    if (sum_2_other + sum_other) % 10 == 0:
        return True
    else:
        print("INVALID")
        return False


if is_valid(card_list):
    if 370000000000000 < card_number < 380000000000000:
        print("AMEX")
    elif 340000000000000 < card_number < 350000000000000:
        print("AMEX")
    elif 5100000000000000 < card_number < 5600000000000000:
        print("MASTERCARD")
    elif 4000000000000000 < card_number < 5000000000000000:
        print("VISA")
    elif 4000000000000 < card_number < 5000000000000:
        print("VISA")

    else:
        print("INVALID")  # this one just give you answer if it's not in list above, but can be card of other bank
        # if someone need more rules just add more else if
