import re

from word2number import w2n


def extract_age(description):
    flag = 0
    age_pattern = r"\b((\d{1,2}-\d{1,2}|\d{1,2} months old|\d{1,2}-\d{1,2}-\d{1,2}|\d{1,2}|\d{1,2}\.\d{1,2}|\d{1,2}s|\d{1,2} year old and \d{1,2} years old)|([Ff]ive|[Ss]ix|[Ss]even|[Ee]ight|[Nn]ine|[Zz]ero|[Oo]ne|[Tt]wo|[Tt]hree|[Ff]our|[Tt]en|[Ee]leven|[Tt]welve|[Tt]hirteen|[Ff]ourteen|[Ff]ifteen|[Ss]ixteen|[Ss]eventeen|[Ee]ighteen|[Nn]ineteen|[Tt]wenty|[Tt]hirty|[Ff]orty|[Ff]ifty|[Ss]ixty|[Ss]eventy|[Ee]ighty|[Nn]inety)[- ]?((?:[Oo]ne|[Tt]wo|[Tt]hree|[Ff]our|[Ff]ive|[Ss]ix|[Ss]even|[Ee]ight|[Nn]ine)?))(([- ]?[Yy]ear(s)?[- ]?[Oo]ld(s)?)|( yr old|[- ]?month(s)?[- ]?old(s)?| month old| moths year old| months year old| [Yy]ear(s)?| months years old| year(s)? (boy|girl)))\b"
    age_apttern1 = r"\d{1,2}[- ]?year[s]?[- ]?old[s]?[- ]?and[- ]?\d{1,2}[- ]?year[s]?[- ]?old[s]?"
    number_words = {
        'half': 0.5, 'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
        'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
        'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13,
        'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17,
        'eighteen': 18, 'nineteen': 19, 'twenty': 20, 'twenty-one': 21,
        'twenty-two': 22, 'twenty-three': 23, 'twenty-four': 24, 'twenty-five': 25,
        'twenty-six': 26, 'twenty-seven': 27, 'twenty-eight': 28, 'twenty-nine': 29,
        'thirty': 30, 'thirty-one': 31, 'thirty-two': 32, 'thirty-three': 33,
        'thirty-four': 34, 'thirty-five': 35, 'thirty-six': 36, 'thirty-seven': 37,
        'thirty-eight': 38, 'thirty-nine': 39, 'forty': 40, 'forty-one': 41,
        'forty-two': 42, 'forty-three': 43, 'forty-four': 44, 'forty-five': 45,
        'forty-six': 46, 'forty-seven': 47, 'forty-eight': 48, 'forty-nine': 49,
        'fifty': 50, 'fifty-one': 51, 'fifty-two': 52, 'fifty-three': 53,
        'fifty-four': 54, 'fifty-five': 55, 'fifty-six': 56, 'fifty-seven': 57,
        'fifty-eight': 58, 'fifty-nine': 59, 'sixty': 60, 'sixty-one': 61,
        'sixty-two': 62, 'sixty-three': 63, 'sixty-four': 64, 'sixty-five': 65,
        'sixty-six': 66, 'sixty-seven': 67, 'sixty-eight': 68, 'sixty-nine': 69,
        'seventy': 70, 'seventy-one': 71, 'seventy-two': 72, 'seventy-three': 73,
        'seventy-four': 74, 'seventy-five': 75, 'seventy-six': 76, 'seventy-seven': 77,
        'seventy-eight': 78, 'seventy-nine': 79, 'eighty': 80, 'eighty-one': 81,
        'eighty-two': 82, 'eighty-three': 83, 'eighty-four': 84, 'eighty-five': 85,
        'eighty-six': 86, 'eighty-seven': 87, 'eighty-eight': 88, 'eighty-nine': 89,
        'ninety': 90, 'ninety-one': 91, 'ninety-two': 92, 'ninety-three': 93,
        'ninety-four': 94, 'ninety-five': 95, 'ninety-six': 96, 'ninety-seven': 97,
        'ninety-eight': 98, 'ninety-nine': 99, 'one hundred': 100
    }

    pattern = r'\b(' + '|'.join(number_words.keys()) + r')\b'
    converted_str = re.sub(pattern, lambda match: str(number_words[match.group(0)]), description.lower())

    age = "NA"
    age_match = re.search(age_apttern1, converted_str.encode('ascii', errors='ignore').decode('ascii'))
    if age_match:
        flag = 1
        age_pattern = r"\d+"
        ages = re.findall(age_pattern, age_match.group(0))
        res = "-".join(ages)
        age = str(res)
    else:
        age_match = re.search(age_pattern, converted_str.replace("  ", " ").replace(" - ", "-").replace(" to ", "-").replace(" To ", "-").replace(
                                  " -", "-").replace(" and ", "-").encode('ascii', errors='ignore').decode('ascii'))
    # print("0000", flag)

    if flag == 0:
        if age_match:
            if "months" in age_match.group(0) or "moths" in age_match.group(0) or "month" in age_match.group(0):
                age = age_match.group(1)
                if age.isnumeric():
                    age = age
                else:
                    try:
                        age = w2n.word_to_num(str(age))
                    except:
                        age = float(age)

                years = int(age) / 12
                if years == 1.0:
                    years = 1
                    age = str(round(years, 2))
                else:
                    age = str(age) + ' Months'

            else:
                age = age_match.group(1)
                if not "-" in age:
                    if age.isnumeric():
                        age = age
                    else:
                        try:
                            age = w2n.word_to_num(str(age))
                        except:
                            if age.endswith('s'):
                                age = age.replace('s', '')
                            else:
                                age = float(age)
                else:
                    try:
                        age = w2n.word_to_num(str(age))
                    except:
                        age = age

        else:
            print("Age not found in the title", str(description))
    # print("--- ", age)
    return age
