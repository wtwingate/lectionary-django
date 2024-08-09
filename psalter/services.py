import re


def parse_psalm_num(reference):
    return int(re.match(r"Psalm (\d+):?.*", reference)[1])


def parse_verse_nums(reference):
    ref_regex = re.compile(r":|;|,|\s|\(|\)")

    verse_nums = []
    for ref in re.split(ref_regex, reference.split(":")[1]):
        if ref == "":
            continue

        if "-" in ref:
            start = int(ref.split("-")[0])
            end = int(ref.split("-")[1])
            for v in range(start, end + 1):
                verse_nums.append(v)
        else:
            verse_nums.append(int(ref))

    return verse_nums
