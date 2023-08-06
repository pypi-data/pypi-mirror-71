#include "QPT.h"

namespace QPT{
    QuestionPaper::QuestionPaper(){}
    QuestionPaper::QuestionPaper(unordered_map<string, vector<int>> mark_of,
                                 vector<int> question_no)
    {
            this->mark_of = mark_of;
            for(auto &&constraint: mark_of){
                this->status_of[constraint.first].resize(constraint.second.size(), 1);
                this->allot_by_question_no[constraint.first].resize(this->mark_of["question"].size(), 0);
            }
            this->allot_by_question_no["question"] = this->mark_of["question"];
            this->allot_by_question_no["question_no"] = question_no;
    }
    QuestionPaper::~QuestionPaper(){}

    void QuestionPaper::insert_column(  int increased_size,
                                        int index ){
        for(auto &&dict : this->allot_by_question_no){
            int val = dict.second[index];
            auto pos = dict.second.begin() + index;
            dict.second.insert(pos, val);
        }
        {
            int val = this->status_of["question"][index];
            auto pos = this->status_of["question"].begin() + index;
            this->status_of["question"].insert(pos, val);
        }
        {
            int val = this->mark_of["question"][index];
            auto pos = this->mark_of["question"].begin() + index;
            this->mark_of["question"].insert(pos, val);
        }
    }
    
    void QuestionPaper::match_on(string constraint){
        for(unsigned int i=0; i<this->mark_of["question"].size(); i++){
            for(unsigned int j=0; j<this->mark_of[constraint].size(); j++){
                if( this->status_of["question"][i] == 1 &&
                    this->status_of[constraint][j] == 1 &&
                    this->mark_of["question"][i] == this->mark_of[constraint][j]){
                        this->mark_of["question"][i] = 0;
                        this->mark_of[constraint][j] = 0;
                        this->allot_by_question_no[constraint][i] = j+1;
                        this->status_of["question"][i] = -1;
                        this->status_of[constraint][j] = -1;
                }
            }
        }
    }

    void QuestionPaper::add_and_match_on(string constraint){
        for(unsigned int i=0; i<this->mark_of["question"].size(); i++){
            for(unsigned int j=0; j<this->mark_of["question"].size(); j++){
                for(unsigned int k=0; k<this->mark_of[constraint].size(); k++){
                    if( i != j &&
                        this->status_of["question"][i] == 1 &&
                        this->status_of["question"][j] == 1 &&
                        this->status_of["unit"][k] == 1 &&
                        this->mark_of["question"][i] + 
                        this->mark_of["question"][j] ==
                        this->mark_of[constraint][k]){

                            this->mark_of["question"][i] = 0;
                            this->mark_of["question"][j] = 0;
                            this->mark_of[constraint][k] = 0;
                            this->allot_by_question_no[constraint][i] = k+1;
                            this->allot_by_question_no[constraint][j] = k+1;
                            this->status_of["question"][i] = -1;
                            this->status_of["question"][j] = -1;
                            this->status_of[constraint][k] = -1;
                    }
                }
            }
        }
    }

    void QuestionPaper::final_allotment(string constraint){
        while(find(this->status_of["question"].begin(),
                   this->status_of["question"].end(), 1) != 
              this->status_of["question"].end() ){
            int max_que_mark_index = distance(this->mark_of["question"].begin(),
                                                max_element(this->mark_of["question"].begin(),
                                                            this->mark_of["question"].end()
                                                )
            );
            int max_constraint_mark_index = distance(this->mark_of[constraint].begin(),
                                                        max_element(this->mark_of[constraint].begin(),
                                                                    this->mark_of[constraint].end()
                                                        )
            );

            if(this->mark_of[constraint][max_constraint_mark_index] == 
                    this->mark_of["question"][max_que_mark_index]){
                    this->mark_of[constraint][max_constraint_mark_index] = 0;
                    this->mark_of["question"][max_que_mark_index] = 0;
                    this->allot_by_question_no[constraint][max_que_mark_index] = max_constraint_mark_index + 1;
                    this->status_of[constraint][max_constraint_mark_index] = -1;
                    this->status_of["question"][max_que_mark_index] = -1;
            }
            else if(this->mark_of[constraint][max_constraint_mark_index] > 
                        this->mark_of["question"][max_que_mark_index]){

                    this->mark_of[constraint][max_constraint_mark_index] = 
                        this->mark_of[constraint][max_constraint_mark_index] - 
                        this->mark_of["question"][max_que_mark_index];

                    this->mark_of["question"][max_que_mark_index] = 0;

                    this->allot_by_question_no[constraint][max_que_mark_index] = 
                        max_constraint_mark_index + 1;

                    this->status_of["question"][max_que_mark_index] = -1; 
            }
            else{
                    int constraint_marks = this->mark_of[constraint][max_constraint_mark_index];
                    int remaining_marks = this->mark_of["question"][max_que_mark_index] - 
                                            constraint_marks;
                    int increased_size = this->mark_of["question"].size() + 1;

                    this->insert_column(increased_size, max_que_mark_index);

                    this->allot_by_question_no["question"][max_que_mark_index] = constraint_marks;
                    this->allot_by_question_no["question"][max_que_mark_index + 1] = remaining_marks;
                    this->mark_of["question"][max_que_mark_index] = 0;
                    this->mark_of["question"][max_que_mark_index + 1] = remaining_marks;
                    this->mark_of[constraint][max_constraint_mark_index] = 0;
                    this->allot_by_question_no[constraint][max_que_mark_index] = max_constraint_mark_index + 1;
                    this->status_of["question"][max_que_mark_index] = -1;
                    this->status_of[constraint][max_constraint_mark_index] = -1;
            }
        }
    }

    void QuestionPaper::generate(){
        for(auto && constraint : mark_of){
            if(constraint.first != "question"){
                this->match_on(constraint.first);
                this->add_and_match_on(constraint.first);
                this->final_allotment(constraint.first);
            }
            fill(this->status_of["question"].begin(),
                 this->status_of["question"].end(), 1);
            
            this->mark_of["question"] = allot_by_question_no["question"];
        }
    }
} // namespace QPT