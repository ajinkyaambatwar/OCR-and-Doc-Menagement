from file_max import file_handler

Data=dict()
def doc_type(filename):
    text2=file_handler(filename)
    if text2[0]=='T':
        text2.replace('T','I')
    if text2[0]=='I':
        return 'emirates_id'
    elif text2[0]=='P':
        if text2[2:5]=='IND':
            return 'passport_ind'
        elif text2[2:5]=='PAK':
            return 'passport_pak'
        elif text2[2:5]=='ARE':
            return 'passport_uae'
        elif text2[2:5]=='JOR':
            return 'passport_jor'
    
typedoc=doc_type('s4-shripad_passport.png')
Data['doc_type']=typedoc
print(Data)