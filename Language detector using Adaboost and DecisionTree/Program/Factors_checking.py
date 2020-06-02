class Factors:
    """
    The Following factors were taken from "https://en.wikipedia.org/wiki/Dutch_orthography"
    and "https://en.wikipedia.org/wiki/English_orthography"
    """
    def word_length(self, statement):
        """
        Check the average word length of the statement
        :param statement: Input statement
        :return: Boolean value
        """
        boolT = False
        words = statement.split()
        total_word_size = 0
        total_words = 0
        for word in words:
            total_word_size = total_word_size + len(word)
            total_words = total_words + 1
        if total_word_size / total_words < 6:
            return boolT
        else:
            boolT = True
            return boolT

    def contains_en(self, statement):
        """
        Checking for the presence of the word en in the sentence
        :param statement:Input Statement
        :return:Boolean value
        """
        bool = True
        words = statement.split()
        for word in words:
            if word.lower().replace(',', '') == 'en':
                return bool
        bool = False
        return bool

    def common_dutch_words(self, statement):
        """
        Checking if sentence contains common dutch words
        :param statement:Sentence
        :return:Boolean value
        """
        list = ['met', 'hij', 'over', 'hem', 'weten', 'jouw', 'naar', 'zijn', 'dan', 'ook', 'onze', 'deze', 'ons',
                'meest','ze', 'wij', 'ze', 'er', 'hun', 'zo', 'be', 'het', 'niet']
        bool = True
        words = statement.split()
        for word in words:
            if word.lower().replace(',', '') in list or word.lower().replace('.', '') in list:
                return bool
        bool = False
        return bool

    def common_english_words(self, statement):
        """
        Checking if the sentence contains common english words
        :param statement:Sentence
        :return: Boolean value
        """
        list = ['his', 'they', 'we', 'she', 'there', 'their', 'so', 'your', 'than', 'then', 'also', 'our', 'these',
                'about', 'me', 'him', 'know', 'to', 'be', 'I', 'it', 'for', 'not', 'with', 'he', 'us', 'most']
        bool = True
        words = statement.split()
        for word in words:
            if word.lower().replace(',', '') in list or word.lower().replace('.', '') in list:
                return bool
        bool = False
        return bool

    def contains_van(self, statement):
        """
        Check if the statement contains the string van
        :param statement:Input statement
        :return:Boolean value
        """
        words = statement.split()
        bool = True
        for word in words:
            if word.lower().replace(',', '') == 'van':
                return bool
        bool = False
        return bool

    def contains_de_het(self, statement):
        """
        Check if the statement contains the string de and het
        :param statement:Input statement
        :return:Boolean value
        """
        words = statement.split()
        bool = True
        for word in words:
            if word.lower().replace(',', '') == 'de' or word.lower().replace(',', '') == 'het':
                return bool
        bool = False
        return bool

    def contains_a_an_the(self, statement):
        """
        Check for the presence of articles a an the
        If they are present , chances are statement is in  english language
        :param statement:
        :return: Boolean value
        """
        bool = True
        words = statement.split()
        for word in words:
            if word.lower().replace(',', '') == 'a' or word.lower().replace(',', '') == 'an' or word.lower().replace(
                    ',', '') == 'the':
                return bool
        bool = False
        return bool

    def contains_een(self, statement):
        """
        Checking for the presence of the word een
        :param statement:Input 15-word statement
        :return:Boolean value
        """
        words = statement.split()
        bool = True
        for word in words:
            if word.lower().replace(',', '') == 'een' or word.lower().replace('.', '') == 'een':
                return bool
        bool = False
        return bool

    def contains_and(self, sentence):
        """
            Checking presence of 'and' in the sentence
            :param sentence:Input sentence
            :return:Boolean value
            """
        words = sentence.split()
        bool = True
        for word in words:
            if word.lower().replace(',', '') == 'and':
                return bool
        bool = False
        return bool

    def contains_X(self, sentence):
        """
            Checking occurence of Letter X
            :param sentence:Sentence
            :return: Boolean value
            """
        bool = True
        if sentence.find('x') >= 0 or sentence.find('X') >= 0:
            return bool
        else:
            bool = False
            return bool

    def contains_Q(self, sentence):
        """
            Checking occurence of Letter Q
            :param sentence:Sentence
            :return: Boolean value
            """
        bool = True
        if sentence.find('q') >= 0 or sentence.find('Q') >= 0:
            return bool
        else:
            bool = False
            return bool

    def contains_E(self, sentence):
        """
            Checking occurence of Letter E
            :param sentence:Sentence
            :return: Boolean value
            """
        bool = True
        if sentence.find('e') < 0 or sentence.find('E') < 0:
            return bool
        else:

            bool = False
            return bool
            #

    def contains_ik(self, sentence):
        """
            Checking if statement contains Dutch word ik
            :param sentence:Sentence
            :return: Boolean value
            """
        words = sentence.split()
        bool = True
        for word in words:
            if word.lower().replace(',', '') == 'ik' or word.lower().replace('.', '') == 'ik':
                return bool
        bool = False
        return bool

    def contains_voor(self, sentence):
        """
            Checking if statement contains Dutch word voor
            :param sentence:Sentence
            :return: Boolean value
            """
        words = sentence.split()
        bool = True
        for word in words:
            if word.lower().replace(',', '') == 'voor' or word.lower().replace('.', '') == 'voor':
                return bool
        bool = False
        return bool
