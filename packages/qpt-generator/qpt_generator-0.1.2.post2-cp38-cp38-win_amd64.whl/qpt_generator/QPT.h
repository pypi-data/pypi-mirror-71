#ifndef QPT_H
#define QPT_H
#include <vector>
#include <unordered_map>
#include <string>
#include <algorithm>
#include <unordered_set>
using namespace std;
namespace QPT{
    class QuestionPaper{
        private:
        unordered_map<string, vector<int>> status_of;
        void match_on(string constraint);
        void add_and_match_on(string constraint);
        void final_allotment(string constraint);
        void insert_column(int increased_size, int index);

        public:
        unordered_map<string, vector<int>> mark_of;
        unordered_map<string, vector<int>> allot_by_question_no;

        QuestionPaper();
        QuestionPaper(unordered_map<string, vector<int>> mark_of,
                      vector<int> question_no);
        ~QuestionPaper();

        void generate();   
    };
}

#endif