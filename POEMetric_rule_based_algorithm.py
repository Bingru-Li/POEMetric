import nltk
from nltk.tokenize import word_tokenize
import string
import re
import pandas as pd
from nltk.corpus import cmudict
import pandas as pd
import re

# download third-party dependencies
nltk.download('cmudict')
nltk.download('punkt')
nltk.download('punkt_tab')


class METERChecker(object):
    @staticmethod
    def is_iambic_pentameter(meter_pattern):
        if len(meter_pattern) != 10:
            return False

        expected_pattern = ['u', 'S'] * 5  # 5 iambs
        matches = sum(1 for i in range(10) if meter_pattern[i] == expected_pattern[i] or meter_pattern[i] == '*')

        return matches / 10 >= 0.7  # at least 70% match

    @staticmethod
    def is_iambic_tetrameter(meter_pattern):
        if len(meter_pattern) != 8:
            return False

        expected_pattern = ['u', 'S'] * 4  # 4 iambs
        matches = sum(1 for i in range(8) if meter_pattern[i] == expected_pattern[i] or meter_pattern[i] == '*')

        return matches / 8 >= 0.7  # at least 70% match

    @staticmethod
    def is_iambic_trimeter(meter_pattern):
        if len(meter_pattern) != 6:
            return False

        expected_pattern = ['u', 'S'] * 3  # 3 iambs
        matches = sum(1 for i in range(6) if meter_pattern[i] == expected_pattern[i] or meter_pattern[i] == '*')

        return matches / 6 >= 0.7  # at least 70% match


class POEMFormat(object):
    def __init__(self, ):
        self.valid_formats = ["limerick", "sonnet", "ballad", "ghazal", "pantoum", "villanelle", "sestina"]
        self.meter_checker = METERChecker()

    def is_limerick(self, meter_analysis, rhyme_analysis):
        lines = len(rhyme_analysis)

        if lines == 5:
            # check AABBA pattern
            if (rhyme_analysis[0][2] == rhyme_analysis[1][2] == rhyme_analysis[4][2] and
                    rhyme_analysis[2][2] == rhyme_analysis[3][2] and
                    rhyme_analysis[0][2] != rhyme_analysis[2][2]):
                return True

        elif lines == 4:
            # check AABA pattern
            if (rhyme_analysis[0][2] == rhyme_analysis[1][2] == rhyme_analysis[3][2] and
                    rhyme_analysis[0][2] != rhyme_analysis[2][2]):
                return True

        return False

    def is_sonnet(self, meter_analysis, rhyme_analysis):
        # we don't need to pre-check sonnets
        return True

    def is_ballad(self, meter_analysis, rhyme_analysis):
        sections = []
        section = []

        for line, _, rhyme_letter in rhyme_analysis:
            section.append((line, rhyme_letter))
            if len(section) == 4:
                sections.append(section)
                section = []

        if section:
            sections.append(section)

        total_sections = len(sections)
        conforming_sections = 0

        # check ABCB/ABAB rhyme patterns
        for sec in sections:
            if len(sec) != 4 or sec[1][1] != sec[3][1]:
                return False

            conforming_sections += 1

        if conforming_sections / total_sections >= 0.7:  # at least 70% match
            return True

        return False

    def is_ghazal(self, meter_analysis, rhyme_analysis):
        if not hasattr(self, 'cmu'):
            from nltk.corpus import cmudict
            self.cmu = cmudict.dict()

        import re
        import string

        # check internal rhyme patterns
        def extract_rhyme_foot(word):
            word = word.lower().strip(string.punctuation)
            if word in self.cmu:
                phones = self.cmu[word][0]
                vowels = re.compile(r'[AEIOU]')
                rhyme_parts = []
                for phone in reversed(phones):
                    if vowels.search(phone):
                        rhyme_parts.append(phone)
                        break
                    rhyme_parts.append(phone)
                return ''.join(reversed(rhyme_parts))
            return ''

        def rhymes_similar(w1, w2):
            w1 = w1.lower().strip(string.punctuation)
            w2 = w2.lower().strip(string.punctuation)
            if w1 == w2:
                return True
            foot1 = extract_rhyme_foot(w1)
            foot2 = extract_rhyme_foot(w2)
            if not foot1 or not foot2:
                return False

            f1 = re.sub(r'\d', '', foot1)
            f2 = re.sub(r'\d', '', foot2)
            if f1 == f2:
                return True

            if len(f1) == len(f2):
                if sum(1 for a, b in zip(f1, f2) if a != b) == 1:
                    return True
            if abs(len(f1) - len(f2)) == 1:
                longer, shorter = (f1, f2) if len(f1) > len(f2) else (f2, f1)
                for i in range(len(shorter) + 1):
                    if longer[:i] + longer[i + 1:] == shorter:
                        return True
            return False

        lines = [item[0] for item in meter_analysis]

        if len(lines) < 4 or len(lines) % 2 != 0:
            return False

        def get_common_suffix(list1, list2):
            suffix = []
            for w1, w2 in zip(reversed(list1), reversed(list2)):
                if w1.lower() == w2.lower():
                    suffix.insert(0, w1.lower())
                else:
                    break
            return suffix

        radif = get_common_suffix(lines[1], lines[3])
        radif_len = len(radif)

        def get_qafia(line_words):
            if radif_len == 0:
                return line_words[-1] if line_words else None
            else:
                line_suffix = [w.lower() for w in line_words[-radif_len:]]
                if line_suffix != radif:
                    return None
                if len(line_words) > radif_len:
                    return line_words[-(radif_len + 1)]
                else:
                    return None

        qafia1 = get_qafia(lines[0])
        qafia2 = get_qafia(lines[1])

        if not qafia1 or not qafia2:
            return False

        if not rhymes_similar(qafia1, qafia2):
            return False

        for i in range(3, len(lines), 2):
            current_qafia = get_qafia(lines[i])

            if not current_qafia:
                return False

            if not rhymes_similar(current_qafia, qafia1):
                return False

        return True

    def is_pantoum(self, meter_analysis, rhyme_analysis):
        if len(meter_analysis) < 8 or len(meter_analysis) % 4 != 0:
            return False

        lines = [[word.lower() for word in item[0]] for item in meter_analysis]

        stanzas = [lines[i:i + 4] for i in range(0, len(lines), 4)]

        def lines_match(line1, line2):
            if line1 == line2:
                return True

            if len(line1) == len(line2):
                diff_count = sum(1 for w1, w2 in zip(line1, line2) if w1 != w2)
                if diff_count <= 1:
                    return True

            if abs(len(line1) - len(line2)) == 1:
                longer, shorter = (line1, line2) if len(line1) > len(line2) else (line2, line1)
                for i in range(len(longer)):
                    if longer[:i] + longer[i + 1:] == shorter:
                        return True

            return False


        for i in range(len(stanzas) - 1):
            if not lines_match(stanzas[i][1], stanzas[i + 1][0]):
                return False
            if not lines_match(stanzas[i][3], stanzas[i + 1][2]):
                return False

        if not lines_match(stanzas[-1][1], stanzas[0][0]):
            return False
        if not lines_match(stanzas[-1][3], stanzas[0][2]):
            return False

        return True

    def is_villanelle(self, meter_analysis, rhyme_analysis):
        if meter_analysis is None or rhyme_analysis is None:
            return False

        if len(meter_analysis) != 19 or len(rhyme_analysis) != 19:
            return False

        lines = [[word.lower() for word in item[0]] for item in meter_analysis]

        def lines_match(line1, line2):
            if line1 == line2:
                return True
            if len(line1) == len(line2):
                if sum(1 for w1, w2 in zip(line1, line2) if w1 != w2) <= 1:
                    return True
            if abs(len(line1) - len(line2)) == 1:
                longer, shorter = (line1, line2) if len(line1) > len(line2) else (line2, line1)
                for i in range(len(longer)):
                    if longer[:i] + longer[i + 1:] == shorter:
                        return True
            return False

        rhyme_A = rhyme_analysis[0][2]
        rhyme_B = rhyme_analysis[1][2]

        if rhyme_A == rhyme_B:
            return False

        expected_rhyme_pattern = [
            0, 1, 0,  # Stanza 1
            0, 1, 0,  # Stanza 2
            0, 1, 0,  # Stanza 3
            0, 1, 0,  # Stanza 4
            0, 1, 0,  # Stanza 5
            0, 1, 0, 0  # Stanza 6 (Quatrain)
        ]

        for i, expected in enumerate(expected_rhyme_pattern):
            target_rhyme = rhyme_A if expected == 0 else rhyme_B
            if rhyme_analysis[i][2] != target_rhyme:
                return False

        refrain_1 = lines[0]
        refrain_2 = lines[2]

        if not lines_match(lines[5], refrain_1):
            return False

        if not lines_match(lines[8], refrain_2):
            return False

        if not lines_match(lines[11], refrain_1):
            return False

        if not lines_match(lines[14], refrain_2):
            return False

        if not lines_match(lines[17], refrain_1):
            return False

        if not lines_match(lines[18], refrain_2):
            return False

        return True

    def is_sestina(self, meter_analysis, rhyme_analysis):
        if meter_analysis is None or len(meter_analysis) != 39:
            return False

        lines = [[word.lower() for word in item[0]] for item in meter_analysis]

        target_end_words = [line[-1] for line in lines[0:6]]
        target_set = sorted(target_end_words)

        if len(set(target_end_words)) != 6:
            return False

        expected_permutations = [
            [5, 0, 4, 1, 3, 2],
            [2, 5, 3, 0, 1, 4],
            [4, 2, 1, 5, 0, 3],
            [3, 4, 0, 2, 5, 1],
            [1, 3, 5, 4, 2, 0]
        ]

        for i in range(1, 6):
            current_stanza = lines[i * 6: (i + 1) * 6]
            current_end_words = [line[-1] for line in current_stanza]

            if sorted(current_end_words) != target_set:
                return False

            expected_words = [target_end_words[idx] for idx in expected_permutations[i - 1]]
            if current_end_words != expected_words:
                return False

        envoi_lines = lines[36:39]
        found_in_envoi = []

        for line in envoi_lines:
            words_in_line = [w for w in target_end_words if w in line]

            if len(set(words_in_line)) != 2:
                return False

            if line[-1] not in target_end_words:
                return False

            found_in_envoi.extend(set(words_in_line))

        if sorted(list(set(found_in_envoi))) != target_set:
            return False

        return True

    def check_poem(self, meter_analysis, rhyme_analysis, meter, rhyme, form):
        def transform_string(s):
            char_map = {}
            result = []
            next_char = 'A'

            for char in s:
                if char not in char_map:
                    char_map[char] = next_char
                    next_char = chr(ord(next_char) + 1)  # Move to the next character
                result.append(char_map[char])

            return ''.join(result)

        # 1. precheck via rule-based methods
        assert form in self.valid_formats, f"invalid format {form} not in {self.valid_formats}."
        form_check_func = getattr(self, f"is_{form}")
        form_check_ret = form_check_func(meter_analysis, rhyme_analysis)

        if isinstance(form_check_ret, tuple):
            if not form_check_ret[0]:
                return False, "Fail in pre-check"
        else:
            if not form_check_ret:
                return False, f"Fail in {form} form check"

        fixed_rhyme_forms = ["limerick", "villanelle", "sestina", "pantoum", "ghazal"]
        if form in fixed_rhyme_forms:
            rhyme = None

        # 2. meter check
        if meter:
            func_name = "is_" + meter.lower().replace(" ", "_")
            meter_check_func = getattr(self.meter_checker, func_name)

            # record the number of lines that didn't satisfy the meter pattern
            non_meter_count = 0
            poem_meters = []
            for _, _, poem_meter in meter_analysis:
                poem_meters.append(poem_meter)
                if not meter_check_func(poem_meter):
                    non_meter_count += 1

            if non_meter_count / len(meter_analysis) >= 0.3:
                return False, f"False meter pattern:\npoem_meter: {poem_meters}\nmeter: {meter}"

        # 3. rhyme check
        if rhyme:
            poem_rhyme = "".join(r[-1] for r in rhyme_analysis)
            if len(poem_rhyme) % len(rhyme) != 0:
                return False, f"False number of lines. \npoem_rhyme: {poem_rhyme}\nrhyme: {rhyme}"
            n_line_per_group = len(rhyme)
            n_group = len(poem_rhyme) // len(rhyme)
            n_matched = 0
            new_poem_rhymes = ""
            for group_index in range(n_group):
                poem_rhyme_cur_group = poem_rhyme[group_index * n_line_per_group:(group_index + 1) * n_line_per_group]
                new_poem_rhymes += transform_string(poem_rhyme_cur_group)
                for pr, r in zip(transform_string(poem_rhyme_cur_group), rhyme):
                    if pr == r:
                        n_matched += 1

            if n_matched / len(poem_rhyme) > 0.7:
                return True, ""
            return False, f"False rhyme pattern. \npoem_rhyme: {new_poem_rhymes}\nrhyme: {rhyme}"

        return True, ""


class POEMetric(object):
    """
    Data format:
    id, form, meter, rhyme, model1_poem, model2_poem, ...
    """

    def __init__(self, ):
        # Parse file into standard format (list of dict)
        self.cmudict = cmudict.dict()
        self.poem_format = POEMFormat()

    @staticmethod
    def poem2words(poem: str) -> list[list[str]]:
        # Split the poem into lines
        lines = poem.strip().split('\n')
        lines = [line.strip() for line in lines if line.strip()]

        # Split each line into words and create a list of lists
        def line2words(l: str) -> list[str]:
            # Replace hyphens and possessive forms
            l = l.replace("-", " ").replace("'s ", " ")
            # Tokenize the line
            tokens = word_tokenize(l)
            # Remove the token "s" if it exists
            tokens = [token for token in tokens if token != "s" and token.isalpha()]
            return tokens

        word_lists = [line2words(line) for line in lines]
        word_lists = [words for words in word_lists if len(words) > 0]
        # for line_words in word_lists:
        #     assert len(line_words) > 0, f"Empty line in {poem}"
        return word_lists

    def poem2rhyme(self, poem_words: list[list[str]]) -> list[tuple]:

        def rhymes_similar(foot1, foot2):
            """check rhyme"""
            if foot1 == foot2:
                return True

            # ignore stress
            foot1_rhyme = re.sub(r'\d', '', foot1)
            foot2_rhyme = re.sub(r'\d', '', foot2)

            len1, len2 = len(foot1_rhyme), len(foot2_rhyme)

            # if of the same length, allow 1-letter diff
            if len1 == len2:
                diff_count = sum(1 for a, b in zip(foot1_rhyme, foot2_rhyme) if a != b)
                if diff_count == 1:
                    return True

            # if length diff =  +/- 1, allow 1-letter diff
            if abs(len1 - len2) == 1:
                longer, shorter = (foot1_rhyme, foot2_rhyme) if len1 > len2 else (foot2_rhyme, foot1_rhyme)
                for i in range(len(shorter) + 1):
                    if longer[:i] + longer[i + 1:] == shorter:
                        return True

            if foot1_rhyme == foot2_rhyme:
                return True

            return False

        def extract_rhyme_foot(word):
            if word.lower() in self.cmudict:
                phones = self.cmudict[word.lower()][0]
                vowels = re.compile(r'[AEIOU]')
                rhyme_parts = []

                for phone in reversed(phones):
                    if vowels.search(phone):
                        rhyme_parts.append(phone)
                        break
                    rhyme_parts.append(phone)

                return ''.join(reversed(rhyme_parts))
            return ''

        last_word_lists = [line_words[-1] for line_words in poem_words]
        last_word_rhyme_feet = [extract_rhyme_foot(word) for word in last_word_lists]
        rhyme_mapping = {}
        rhyme_letters = []
        rhyme_counter = 0
        for last_word_rhyme_foot in last_word_rhyme_feet:
            found_rhyme_letter = None
            for existing_foot, rhyme_letter in rhyme_mapping.items():
                if rhymes_similar(existing_foot, last_word_rhyme_foot):
                    found_rhyme_letter = rhyme_letter
                    break

            if found_rhyme_letter:
                rhyme_letter = found_rhyme_letter
            else:
                rhyme_counter += 1
                rhyme_letter = chr(64 + rhyme_counter)  # A, B, C, B, ...
                rhyme_mapping[last_word_rhyme_foot] = rhyme_letter
            rhyme_letters.append(rhyme_letter)

        return [(w, rf, rl) for w, rf, rl in zip(last_word_lists, last_word_rhyme_feet, rhyme_letters)]

    def poem2meter(self, poem_words: list[list[str]]) -> list[tuple]:

        def get_syllables(word):
            if word.lower() in self.cmudict:
                return [len(list(y for y in x if y[-1].isdigit())) for x in self.cmudict[word.lower()]]
            return [0]

        def is_monophthongal(phones):
            """check if the phone is monophthongal"""
            vowel_count = sum(1 for phone in phones if re.search(r'[AEIOU]', phone))
            return vowel_count == 1

        def get_meter_pattern(phones):
            pattern = []
            for stress in phones:
                if stress[-1].isdigit():
                    if stress[-1] in ['0', '2']:
                        pattern.append('u')  # unstressed
                    elif stress[-1] == '1':
                        pattern.append('S')  # stressed

            # monophthong can be either stressed or unstressed, marked as '*'
            if is_monophthongal(phones):
                if pattern:
                    pattern[-1] = '*'
            return pattern

        meter_analysis = []
        for words_per_line in poem_words:
            syllable_count = 0
            meter_pattern = []
            for word in words_per_line:
                syllables = get_syllables(word)
                if syllables[0] > 0:
                    syllable_count += syllables[0]
                    phones = self.cmudict[word.lower()][0]
                    meter_pattern.extend(get_meter_pattern(phones))
                else:
                    print(f"Warning: No pronunciation found for '{word}'")
                    pass
            meter_analysis.append(
                (words_per_line, syllable_count, meter_pattern))
        return meter_analysis

    def evaluate_row(self, row):
        reserved_keys = ["id", "Form", "Meter", "Rhyme", "prompt"]
        if "prompt" in row:
            form, meter, rhyme = self.extract_poem_requirements(row["prompt"])
        else:
            form = row["Form"].lower()
            meter = row["Meter"]
            rhyme = row["Rhyme"]
        form = form.lower()
        row["Form"] = form
        if rhyme:
            rhyme = "".join(letter for letter in rhyme if letter != " ")
        poems = {}
        for k, v in row.items():
            if k not in reserved_keys and "poem" in k.lower():
                poems[k] = v
        for poem_k, poem in poems.items():
            poem_words = self.poem2words(poem)
            poem_rhyme = self.poem2rhyme(poem_words)
            poem_meter = self.poem2meter(poem_words)
            is_correct, reason = self.poem_format.check_poem(poem_meter, poem_rhyme, meter, rhyme, form)
            row[f"{poem_k}_is_correct"] = is_correct
            row[f"{poem_k}_reason"] = reason
        return row

    def extract_poem_requirements(self, prompt):
        form_match = re.search(r'Form:\s*(.*?)\s*\n', prompt)
        meter_match = re.search(r'Meter:\s*(.*?)\s*\n', prompt)
        rhyme_match = re.search(r'Rhyme:\s*(.*?)\s*\n', prompt)

        form = form_match.group(1) if form_match else None
        meter = meter_match.group(1) if meter_match else None
        rhyme = rhyme_match.group(1) if rhyme_match else None

        return form, meter, rhyme

    def evaluate_file(self, file_path):
        # Load XLSX and convert to list of dict
        self.data = pd.read_excel(file_path).to_dict(orient='records')
        new_data = []
        for row in self.data:
            new_row = self.evaluate_row(row)
            new_data.append(new_row)

        # calculate the ratio of True in each row whose name contains "is_correct"
        column_names = self.data[0].keys()
        for col in column_names:
            if 'is_correct' in col:
                true_count = sum(row[col] is True for row in new_data)
                total_count = len(new_data)
                ratio = true_count / total_count if total_count > 0 else 0
                print(col, ": ", ratio)

        # Save new data to another file
        sorted_data = []
        for row in new_data:
            poem_keys = sorted(k for k in row if 'poem' in k and k != 'Form')
            other_keys = sorted(k for k in row if 'poem' not in k and k != 'Form')

            sorted_row = {'Form': row.get('Form', '')}

            for k in poem_keys + other_keys:
                sorted_row[k] = row[k]

            sorted_data.append(sorted_row)

        output_file_path = file_path.replace(".xlsx", "_result.xlsx")
        df = pd.DataFrame(sorted_data, index=range(len(sorted_data)))
        df.to_excel(output_file_path, index=False)
        print(f"Saved to {output_file_path}")


if __name__ == '__main__':
    poemetric = POEMetric()
    file_path = "./all_llm_poem_sets.xlsx"
    poemetric.evaluate_file(file_path)
