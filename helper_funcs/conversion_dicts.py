import pickle

# Map qualification column
quals = {'1':'Physician', '2': 'Pharmacist', '3': 'Other health professional',
             '4': 'Lawyer', '5': 'Consumer or non-health professional', 'NA':'No Info'}

# Patient_sex
patientsex = {'1':'Male', '2':'Female', '0':'Unknown'}

# admin_route dict
admin_route_dict = {'001': 'Auricular', '002': 'Buccal', '003': 'Cutaneous', '004': 'Dental', '005': 'Endocervical',
                    '006': 'Endosinusal', '007': 'Endotracheal', '008':'Epidural', '009':'Extra-amniotic',
                    '010':'Hemodialysis', '011':'Intra corpus cavernosum', '012': 'Intra-amniotic', '013': 'Intra-arterial',
                   '014': 'Intra-articual', '015': 'Intra-uterine', '016': 'Intracardiac', '017': 'Intracavernous',
                   '018': 'Intracerebral', '019': 'Intracervical', '020': 'Intracisternal', '021': 'Intracorneal',
                   '022': 'Intracoronary', '023': 'Intradermal', '024': 'Intradiscal', '025': 'Intrahepatic', '026': 'Intralesional',
                   '027': 'Intralymphatic', '028': 'Intramedullar', '029': 'Intrameningeal', '030': 'Intramuscular',
                    '031': 'Intraocular', '032': 'Intrapericardial', '033': 'Intraperitoneal', '034': 'Intrapleural',
                   '035': 'Intrasynovial', '036': 'Intratumor', '037': 'Intrathecal', '038': 'Intrathoracic', '039': 'Intratracheal',
                   '040': 'Intravenous bolus', '041': 'Intravenous drip', '042':'Intravenous','043': 'Intravesical',
                   '044': 'Iontophoresis', '045': 'Nasal', '046': 'Occlusive dressing technique', '047': 'Ophthalmic',
                   '048': 'Oral', '049': 'Oropharingeal', '050': 'Other', '051':'Parenteral', '052':'Periarticular',
                   '053': 'Perineural', '054':'Rectal', '055':'Respiratory (inhalation)','056':'Retrobulbar', '057':'Sunconjunctival',
                   '058': 'Subcutaneous', '059': 'Subdermal', '060':'Sublingual', '061':'Topical', '062':'Transdermal',
                   '063':'Transmammary', '064':'Transplacental', '065':'Unknown', '066':'Urethral', '067':'Vaginal',
                   'NA':'Not Listed', '':'Not Listed'}

# drug_char dict
drug_char_dict = {'1':'Suspect', '2':'Concominant', '3': 'Interacting', '':'Unknown'}


# UNII dict
with open('./helper_funcs/UNII_dict.pkl', 'rb') as f:
    unii_dict =  pickle.load(f)


# reaction_medDRA dict
with open('./medDRA/dict_LLT_PT.pkl', 'rb') as f:
    dict_LLT_PT =  pickle.load(f)
with open('./medDRA/dict_PT_HLT.pkl', 'rb') as f:
    dict_PT_HLT =  pickle.load(f)
with open('./medDRA/dict_HLT_HLGT.pkl', 'rb') as f:
    dict_HLT_HLGT =  pickle.load(f)
with open('./medDRA/dict_HLGT_SOC.pkl', 'rb') as f:
    dict_HLGT_SOC =  pickle.load(f)
