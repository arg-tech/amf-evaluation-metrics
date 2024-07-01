from bs4 import BeautifulSoup
import segeval
from nltk.corpus import words
class match:
    @staticmethod
    def remove_html_tags(xml_soup):
        for match in xml_soup.findAll('div'):
            match.replaceWithChildren()
        for match in xml_soup.findAll('p'):
            match.replaceWithChildren()
        for match in xml_soup.findAll('br'):
            match.replaceWithChildren()
        # for match in xml_soup.findAll('span'):
        #     match.replaceWithChildren()

        return xml_soup

    @staticmethod
    def get_segements(xml_soup):
        segment_list = []
        word_list=[]
        if xml_soup.body:
            for i, tag in enumerate(xml_soup.body):
                boundary_counter = i + 1
                tag_text = ''
                if 'span' in str(tag):
                    tag_text = tag.text
                else:
                    tag_text = str(tag)

                words = tag_text.split()
                seg_len = len(words)
                # print(seg_len)
                segment_list += seg_len * [boundary_counter]
                word_list+=words
        else:
            for i, tag in enumerate(xml_soup):
                boundary_counter = i + 1
                tag_text = ''
                if 'span' in str(tag):
                    tag_text = tag.text
                else:
                    tag_text = str(tag)

                words = tag_text.split()
                seg_len = len(words)
                # print(seg_len)
                segment_list += seg_len * [boundary_counter]
                word_list += words
        return segment_list,word_list


    # @staticmethod
    # def check_segment_length(seg_1, word_1, seg_2, word_2):
    #     # print("seg1", seg_1)
    #     # print("word_1", word_1)
    #     # print("seg2", seg_2)
    #     # print("word_2", word_2)
    #     seg_1_len = len(seg_1)
    #     print(seg_1_len)
    #     seg_2_len = len(seg_2)
    #     print(seg_2_len)
    #
    #
    #     if seg_1_len == seg_2_len:
    #         return True,seg_1,seg_2
    #     else:
    #
    #         if seg_1_len > seg_2_len:
    #             for i in range(len(word_1) - 1):
    #                 if word_1[i] + word_1[i + 1] in word_2:
    #
    #                     word_1[i:i + 2] = [word_1[i] + word_1[i + 1]]
    #                     seg_2_at_i = seg_2[i]  # Segment number at position i in seg_1
    #                     seg_1[i:i + 2] = [seg_2_at_i]
    #
    #                     # seg_2 = [seg_2[0]] * len(word_2)
    #
    #                     if len(seg_1) == len(seg_2):
    #                         return True, seg_1, seg_2
    #                     # else:
    #                     #     return False, None, None
    #             return False, None, None
    #
    #
    #         else:
    #             for i in range(len(word_2) - 1):
    #                 if word_2[i] + word_2[i + 1] in word_1:
    #
    #                     word_2[i:i + 2] = [word_2[i] + word_2[i + 1]]
    #                     seg_1_at_i = seg_1[i]  # Segment number at position i in seg_1
    #                     seg_2[i:i + 2] = [seg_1_at_i]
    #
    #                     # seg_2 = [seg_2[0]] * len(word_2)
    #
    #                     if len(seg_1) == len(seg_2):
    #                         return True,seg_1,seg_2
    #                     # else:
    #                     #     return False, None, None
    #             return False, None, None
    #
    #

    @staticmethod
    def check_segment_length(seg_1, word_1, seg_2, word_2):
        # print("seg1", seg_1)
        # print("word_1", word_1)
        # print("seg2", seg_2)
        # print("word_2", word_2)
        seg_1_len = len(seg_1)
        # print(seg_1_len)
        seg_2_len = len(seg_2)
        print(seg_2_len)

        # if seg_1_len == seg_2_len:
        #     return True, seg_1, seg_2
        # else:
        #
        #     if seg_1_len > seg_2_len:
        for i in range(len(word_1) - 1):
            if i + 1 < len(word_1) and word_1[i] + word_1[i + 1] in word_2:
                word_1[i:i + 2] = [word_1[i] + word_1[i + 1]]
                seg_1_at_i = seg_1[i]  # Segment number at position i in seg_1
                seg_1[i:i + 2] = [seg_1_at_i]
                print("new1",word_1)

                # seg_2 = [seg_2[0]] * len(word_2)


        for i in range(len(word_2) - 1):
            if i + 1 < len(word_2) and word_2[i] + word_2[i + 1] in word_1:
                        word_2[i:i + 2] = [word_2[i] + word_2[i + 1]]
                        seg_2_at_i = seg_2[i]  # Segment number at position i in seg_1
                        seg_2[i:i + 2] = [seg_2_at_i]
                        print("new2",word_2)

                        # seg_2 = [seg_2[0]] * len(word_2)

        if len(seg_1) == len(seg_2):
            return True, seg_1, seg_2
        else:
            return False, None, None


    @staticmethod
    def is_real_word(word1,word2):
        # Check if the word exists in the NLTK words corpus
        return word1.lower() in words.words()

    @staticmethod
    def get_similarity(text_1, text_2):
        aifsim = match()

        if text_1 == '' or text_2 == '':
            return 'Error: Text Input Is Empty'
        else:
            # Preprocess text to remove unwanted characters
            text_1 = aifsim.preprocess_text(text_1)
            text_2 = aifsim.preprocess_text(text_2)

            # Parse text using BeautifulSoup
            xml_soup_1 = BeautifulSoup(text_1, features="lxml")
            xml_soup_2 = BeautifulSoup(text_2, features="lxml")

            # Remove unwanted HTML tags
            xml_soup_1 = aifsim.remove_html_tags(xml_soup_1)
            # xml_soup_1 = BeautifulSoup(str(xml_soup_1), features="lxml").text

            xml_soup_2 = aifsim.remove_html_tags(xml_soup_2)
            # xml_soup_2 = BeautifulSoup(str(xml_soup_2), features="lxml").text
            # Get segments
            segments_1,words_1 = aifsim.get_segements(xml_soup_1)
            print(segments_1)


            segments_2,words_2  = aifsim.get_segements(xml_soup_2)
            print(segments_2)


            # Check segment length
            seg_check,seg1,seg2 = aifsim.check_segment_length(segments_1,words_1, segments_2,words_2)
            print(seg1)

            print(seg2)


            if not seg_check:
                error_text = 'Error: Source Text Was Different as Segmentations differ in length'
                return error_text
            else:
                if seg1 == seg2:
                    ss = 1.0  # If segmentation sequences are identical, set similarity to maximum (1.0)
                else:
                    # Convert segments to masses
                    masses_1 = segeval.convert_positions_to_masses(seg1)

                    masses_2 = segeval.convert_positions_to_masses(seg2)

                    # Calculate segmentation similarity
                    ss = segeval.segmentation_similarity(masses_1, masses_2)


                return ss

    @staticmethod
    def preprocess_text(text):
        # Remove unwanted characters
        text = text.replace("`", "").replace("’", "").replace("'", "").strip()
        text = text.replace("[", " [").replace("]", "] ").replace("...", " ").replace("…", " ")
        text = text.replace(".", " ").replace(",", " ").replace("!", " ").replace("?", " ")
        text = text.replace("  ", " ")

        return text


# Example usage
text_2 = "<span>a college degree these days is</span> equivalent to <span>high school degree in the hello </span>past bye  "
text_1 = "<span>a college degree these days i</span>s equivalent to <span>high school degree in the </span> hello past  "
similarity_score = match.get_similarity(text_1, text_2)
print("Similarity score:", similarity_score)