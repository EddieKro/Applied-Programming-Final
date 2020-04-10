question_blocks = {'symptoms':['Fever', 'Tiredness','Dry cough','Sore throat','Difficulty in breath','Pains','Nasal congestion','Running Nose','Diarrhea'],#select as many as possible
                   'age':['0-9','10-19','20-24','25-59','59-200'],#select only one
                   'gender':['Female','Male'],
                   'contact'['Not sure','No','Yes']
                  }
descriptions = {'symptoms':'Are you experiencing this particular symptom right now? : ',
                'age':'Select your age group:',
                'gender': 'Select your gender:',
                'contact':'Did you contact anyone lately?'
               }
initial_indices = {0:0,1:11,2:16,3:21}