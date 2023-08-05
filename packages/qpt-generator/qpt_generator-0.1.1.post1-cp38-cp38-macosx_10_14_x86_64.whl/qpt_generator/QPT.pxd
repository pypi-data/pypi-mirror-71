# distutils: language = c++
from libcpp.string cimport string
from libcpp.unordered_map cimport unordered_map
from libcpp.vector cimport vector

cdef extern from "QPT.cpp":
    pass

cdef extern from "QPT.h" namespace "QPT":
    cdef cppclass QuestionPaper:
        QuestionPaper() except +
        QuestionPaper(unordered_map[string, vector[int]],
                      vector[int]) except +
        void generate()

        unordered_map[string, vector[int]] mark_of
        unordered_map[string, vector[int]] allot_by_question_no
