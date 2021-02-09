import typing
import math

def process_text(input: str) -> typing.List[str]:
    strip_chars = [".", "."]
    holder = input
    for char in strip_chars:
        holder = holder.strip(char)
    return [x for x in holder.split(" ") if x != ""]


def bag_of_words(input: typing.List[str]) -> typing.Mapping[str, int]:
    output = {}
    for word in input:
        if word in output.keys():
            output[word] += 1
        else:
            output[word] = 1
    return output

# N-gram is dead code for right now, was intended for use calculating window-like metrics over the sentences. Deprioritized right now due to time constraint
def n_gram(input: typing.List[str], n: int) -> typing.List[typing.List[str]]:
    if n <= 0:
        return []
    if len(input) < n:
        return []
    return [input[i : i + n] for i in range(len(input) - (n - 1))]


def kld_intersection(
    first: typing.Mapping[str, int], second: typing.Mapping[str, int]
) -> float:
    first_keys = set(first.keys())
    second_keys = set(second.keys())
    intersection = first_keys.intersection(second_keys)
    first_total = sum([first[key] for key in intersection])
    second_total = sum([second[key] for key in intersection])
    kld_sum = 0
    for key in intersection:
        first_prob = first[key] / first_total
        second_prob = second[key] / second_total
        kld_sum += first_prob * math.log(first_prob / second_prob)
    return kld_sum


def vec_helper(
    bag_of_words: typing.Mapping[str, int], union: typing.List[str]
) -> typing.List[int]:
    output = []
    keys = bag_of_words.keys()
    for key in union:
        if key in keys:
            output.append(bag_of_words[key])
        else:
            output.append(0)
    return output


def cos_bag_of_words(
    first: typing.Mapping[str, int], second: typing.Mapping[str, int]
) -> float:
    first_keys = set(first.keys())
    second_keys = set(second.keys())
    union = list(first_keys.union(second_keys))
    first_vec = vec_helper(first, union)
    second_vec = vec_helper(second, union)
    dot = sum([x * y for x, y in zip(first_vec, second_vec)])
    first_magnitude = math.sqrt(sum([x ** 2 for x in first_vec]))
    second_magnitude = math.sqrt(sum([x ** 2 for x in second_vec]))
    return round(dot / (first_magnitude * second_magnitude), 5)


def text_similarity_kld(first: str, second: str) -> float:
    kld_val = kld_intersection(
        bag_of_words(process_text(first)), bag_of_words(process_text(second))
    )
    return 1 / (1 + kld_val) * text_similarity_intersection(first, second)


def text_similarity_cos(first: str, second: str) -> float:
    if first == second:
        return 1
    elif first == "" or second == "":
        return 0
    first_bag = bag_of_words(process_text(first))
    second_bag = bag_of_words(process_text(second))
    return cos_bag_of_words(first_bag, second_bag)


def text_similarity_intersection(first: str, second: str) -> float:
    if first == second:
        return 1
    processed_first = set(process_text(first))
    processed_second = set(process_text(second))
    intersection = processed_first.intersection(processed_second)
    union = processed_first.union(processed_second)
    if len(union) == 0:
        return 0
    return len(intersection) / len(union)


if __name__ == "__main__":
    test_string_one = "The easiest way to earn points with Fetch Rewards is to just shop for the products you already love. If you have any participating brands on your receipt, you'll get points based on the cost of the products. You don't need to clip any coupons or scan individual barcodes. Just scan each grocery receipt after you shop and we'll find the savings for you."
    test_string_two = "The easiest way to earn points with Fetch Rewards is to just shop for the items you already buy. If you have any eligible brands on your receipt, you will get points based on the total cost of the products. You do not need to cut out any coupons or scan individual UPCs. Just scan your receipt after you check out and we will find the savings for you."
    test_string_three = "We are always looking for opportunities for you to earn more points, which is why we also give you a selection of Special Offers. These Special Offers are opportunities to earn bonus points on top of the regular points you earn every time you purchase a participating brand. No need to pre-select these offers, we'll give you the points whether or not you knew about the offer. We just think it is easier that way."
    print(text_similarity_cos(test_string_one, test_string_two))
    print(text_similarity_cos(test_string_one, test_string_three))
    print(text_similarity_intersection(test_string_one, test_string_two))
    print(text_similarity_intersection(test_string_one, test_string_three))
    print(text_similarity_kld(test_string_one, test_string_two))
    print(text_similarity_kld(test_string_one, test_string_three))
