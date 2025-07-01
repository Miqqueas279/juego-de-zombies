def copy_list(old_list: list) -> list:
    new_list = []

    for item in old_list:
        new_list.append(item)

    return new_list

def sort_list(unordered_list: list, key: str, limit: int) -> list:
    new_list = copy_list(unordered_list)
    length = len(new_list)
    limit_list = []

    for i in range(length):
        for j in range(0, length - i - 1):
            if new_list[j][key] < new_list[j + 1][key]:
                temp = new_list[j]
                new_list[j] = new_list[j + 1]
                new_list[j + 1] = temp

    for i in range(min(length, limit)):
        limit_list.append(new_list[i])

    return limit_list