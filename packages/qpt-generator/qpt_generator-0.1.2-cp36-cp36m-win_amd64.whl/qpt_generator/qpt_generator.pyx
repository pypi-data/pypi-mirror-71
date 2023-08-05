# cython: c_string_type=str, c_string_encoding=utf8
from QPT cimport QuestionPaper

cdef class QPTGenerator:
    """ QPTGenerator is a very fast Question Paper Generator

    :argument
        mark_of: Dict[str, List[int]]:
            - A dict of constraint_name and list of mark distributions
        question_no: List[int]:
            - A list of question no. associated with list of question-wise mark distributions.
            - Repetition of same question no. indicates subquestions of that question.
    :returns
        allot_by_question_no: Dict[str, List[int]]:
            - A dict of constraint_name and list of question_no wise constraint allotment.
    Example:
        >>> from pprint import pprint
        >>> mark_distributions = {\
                "question": [5, 5, 10, 4, 6, 5, 5],\
                "unit": [8, 8, 8, 5, 11],\
                "difficulty": [13, 15, 12],\
                "cognitive": [12, 18, 10],\
            }
        >>> question_no = [1, 1, 2, 3, 3, 4, 4]
        >>> qpt = QPTGenerator(mark_distributions, question_no)
        >>> pprint(qpt.generate())
        {'cognitive': [2, 3, 2, 3, 3, 1, 3, 1, 1, 2],
         'difficulty': [3, 1, 2, 2, 1, 3, 3, 1, 2, 3],
         'question': [5, 5, 8, 2, 2, 1, 1, 6, 5, 5],
         'question_no': [1, 1, 2, 2, 3, 3, 3, 3, 4, 4],
         'unit': [4, 5, 1, 3, 2, 2, 3, 5, 2, 3]}
    """
    cdef QuestionPaper c_qpt

    def __cinit__(self, mark_of, question_no):
        self.c_qpt = QuestionPaper(mark_of, question_no)

    def generate(self):
        self.c_qpt.generate()
        return self.c_qpt.allot_by_question_no
