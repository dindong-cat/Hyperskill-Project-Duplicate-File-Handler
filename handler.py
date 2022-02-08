# write your code here
import sys
import os
import hashlib


def main():
    arg = sys.argv
    if len(arg) < 2:
        print("Directory is not specified")
        exit()
    else:
        print("Enter file format:")
        file_format = input()
        ordering = sorting()
        try:
            result_dict = {}
            root_directory = arg[1]

            for root, dirs, files in os.walk(root_directory, topdown=True):
                for i in files:
                    full_pathname = os.path.join(root, i)
                    size = os.path.getsize(full_pathname)
                    if not file_format:
                        result_dict[full_pathname] = size
                    else:
                        if i.endswith(file_format):
                            result_dict[full_pathname] = size
            if ordering == 1:
                byte_dict = {i: [] for i in sorted(set([i for i in result_dict.values()]), reverse=True)}
                result_dict = {i: result_dict[i] for i in sorted([i for i in result_dict], reverse=True)}
            elif ordering == 2:
                byte_dict = {i: [] for i in sorted(set([i for i in result_dict.values()]), reverse=False)}
                result_dict = {i: result_dict[i] for i in sorted([i for i in result_dict], reverse=False)}

            for i in result_dict:
                for j in byte_dict:
                    if result_dict[i] == j:
                        byte_dict[j].append(i)

            for i in byte_dict:
                print(f"{i} bytes")
                print(*byte_dict[i], sep="\n", end="\n\n")

            print("Check for duplicates?")
            answer = input()
            print()
            if answer == "yes":
                check_for_hash(result_dict, ordering)

        except FileNotFoundError:
            print("Directory is not found")


def sorting():
    print("Size sorting options:")
    print("1. Descending")
    print("2. Ascending")
    print()
    print("Enter a sorting option:")
    option = input()
    print()
    while option not in ["1", "2"]:
        print("Wrong option")
        print()
        print("Enter a sorting option:")
        option = input()
    return int(option)


def verify_selection(delete_option, files_can_del):
    try:
        delete_option = [int(i) for i in delete_option]
    except ValueError:
        return False
    if not delete_option:
        return False
    for i in delete_option:
        if i not in files_can_del:
            return False
    return True


def ask_delete(files_can_del):
    print("Delete files?")

    option = input()
    while option not in ["yes", "no"]:
        print()
        print("Wrong option")
        print()
        print("Delete files?")
        option = input()

    if option == "yes":
        print()
        print("Enter file numbers to delete:")
        delete_option = [i for i in input().split()]
        valid_option = verify_selection(delete_option, files_can_del)

        while not valid_option:
            print("Wrong format")
            print()
            print("Enter file numbers to delete:")
            delete_option = [i for i in input().split()]
            valid_option = verify_selection(delete_option, files_can_del)

        delete_option = [int(i) for i in delete_option]
        confirm_delete = [files_can_del[i] for i in delete_option]
        total_freed_up_space = sum([os.path.getsize(i) for i in confirm_delete])

        for i in confirm_delete:
            os.remove(i)

        print()
        print(f"Total freed up space: {total_freed_up_space} bytes")


def check_for_hash(result_dict, ordering):
    hash_dict = {i: {"bytes": j, "hash": i} for i, j in result_dict.items()}
    num = 1
    files_can_del = {}

    for i in hash_dict:
        with open(i, "r", encoding="utf-8") as f:
            m = hashlib.md5()
            x = "\n".join(f.readlines()).encode()
            hash_dict[i]["hash"] = m.update(x)
            hash_dict[i]["hash"] = m.hexdigest()

    hash_table = [hash_dict[i]["hash"] for i in hash_dict]

    if len(hash_table) != len(set(hash_table)):
        freq_dict = {}

        for i in hash_table:
            freq_dict.setdefault(i, 0)
            freq_dict[i] += 1
        freq_dict = {i: 0 for i in freq_dict if freq_dict[i] > 1}

        for i in freq_dict:
            for j in hash_dict.values():
                if i == j["hash"]:
                    freq_dict[i] = j["bytes"]

        output_dict = set(i for i in freq_dict.values())

        if ordering == 1:
            output_dict = sorted(list(output_dict), reverse=True)
        elif ordering == 2:
            output_dict = sorted(list(output_dict), reverse=False)

        output_dict = {i: [] for i in output_dict}

        for i in output_dict:
            for j in freq_dict:
                if i == freq_dict[j]:
                    output_dict[i].append(j)

        output_dict = {i: sorted(j) for i, j in output_dict.items()}

        for i in output_dict:
            print(f'{i} bytes')
            for j in output_dict[i]:
                print(f'Hash: {j}')
                for k in hash_dict:
                    if j == hash_dict[k]["hash"]:
                        print(f'{num}. {k}')
                        files_can_del[num] = k
                        num += 1
            print()

    if files_can_del:
        ask_delete(files_can_del)


if __name__ == "__main__":
    main()
