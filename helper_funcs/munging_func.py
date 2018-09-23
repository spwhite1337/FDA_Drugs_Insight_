import timeit
import os
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

def section_1(data_2, file_name):
    "year, quarter, authority_no, company_no, duplicate, expedited, occur_country"
    # Initialize the lists
    year = []
    quarter = []
    authority_no = []
    company_no = []
    duplicate = []
    expedited = []
    occur_country = []

    # 2. Convert the data
    num_entries = 0

    for i in range(0,len(data_2)):
        start_time = timeit.default_timer()
        # Generate year and quarter from file_name
        year_entry = file_name[i].split('/')[2].split('_')[0].split('q')[0]
        quarter_entry = file_name[i].split('/')[2].split('_')[0].split('q')[1]

        print('Section 1, file {} of {}...'.format(i+1, len(data_2)))

        for j in range(0, len(data_2[i]['results'])):
            num_entries += 1
            # Progress Tracker
            entry = data_2[i]['results'][j]

            # year
            year.append(year_entry)
            # quarter
            quarter.append(quarter_entry)
            # authority_no
            if 'authoritynumb' in entry.keys():
                authority_no.append(entry['authoritynumb'])
            else:
                authority_no.append('NA')
            # company_no
            if 'companynumb' in entry.keys():
                company_no.append(entry['companynumb'])
            else:
                company_no.append('NA')
            # duplicate
            if 'duplicate' in entry.keys():
                duplicate.append(entry['duplicate'])
            else:
                duplicate.append('NA')
            # expedited
            if 'fulfilledexpediteriteria' in entry.keys():
                expedited.append(entry['fulfilledexpediteriteria'])
            else:
                expedited.append('NA')
            # occurcountry
            if 'occurcountry' in entry.keys():
                occur_country.append(entry['occurcountry'])
            else:
                occur_country.append('NA')

        elapsed = timeit.default_timer() - start_time
        print('{time:0.2f} ms to complete'.format(time = elapsed*1000))

    start_time = timeit.default_timer()
    print('Converting lists to dataframe...')
    data_3 = [year, quarter, authority_no, company_no, duplicate, expedited,
              occur_country]


    # 4. Convert to dataframe
    df = pd.DataFrame(data_3).transpose()
    df.columns = ['year', 'quarter','authority_no', 'company_no', 'duplicate', 'expedited',
                 'occur_country']

    df = df.replace('', 'NA')

    elapsed = timeit.default_timer() - start_time
    print('{time:0.2f} ms to complete.\n'.format(time = elapsed*1000))

    return df


def section_2(data_2):
    "action, active_substance, ... drug_treatment_duration_unit, medicinal_product"
    # 1. Initialize the lists
    action = []
    active_substance = []
    drug_additional = []
    admin_route = []
    authorization_no = []
    batch_no = []
    drug_char = []
    drug_cum_dosage = []
    drug_cum_dosage_units = []
    drug_dosage_form = []
    drug_dosage_text = []
    drug_end_date = []
    drug_end_date_format = []
    drug_indication = []
    drug_interval_dosage_def = []
    drug_interval_dosage_no = []
    drug_recurr_admin = []
    drug_sep_dosage_no = []
    drug_start_date = []
    drug_start_date_format = []
    drug_structure_dosage_no = []
    drug_structure_dosage_unit = []
    drug_treatment_duration = []
    drug_treatment_duration_unit = []
    medicinal_product = []

    # 2. Convert the data
    num_entries = 0

    for i in range(0,len(data_2)):
        start_time = timeit.default_timer()
        print('Section 2, file {} of {}...'.format(i+1, len(data_2)))
        for j in range(0, len(data_2[i]['results'])):
            num_entries += 1
            entry = data_2[i]['results'][j]

            # actiondrug
            actiondrug_tmp = ''
            # activesubstance
            activesubstance_tmp = ''
            # drugadditional
            drugadditional_tmp = ''
            # drugadministrationroute
            drugadministrationroute_tmp = ''
            # drugauthorizationnumb
            drugauthorizationnumb_tmp = ''
            # drugbatchnumb
            drugbatchnumb_tmp = ''
            # drugcharacterization
            drugcharacterization_tmp = ''
            # drugcumulativedosagenumb
            drugcumulativedosagenumb_tmp = ''
            # drugcumulativedosageunit
            drugcumulativedosageunit_tmp = ''
            # drugdosageform
            drugdosageform_tmp = ''
            # drugdosagetext
            drugdosagetext_tmp = ''
            # drugenddate
            drugenddate_tmp = ''
            # drugenddateformat
            drugenddateformat_tmp = ''
            # drugindication
            drugindication_tmp = ''
            # drugintervaldosagedefinition
            drugintervaldosagedefinition_tmp = ''
            # drugintervaldosageunitnumb
            drugintervaldosageunitnumb_tmp = ''
            # drugrecurreadministration
            drugrecurreadministration_tmp = ''
            # drugseparatedosagenumb
            drugseparatedosagenumb_tmp = ''
            # drugstartdate
            drugstartdate_tmp = ''
            # drugstartdateformat
            drugstartdateformat_tmp = ''
            # drugstructuredosagenumb
            drugstructuredosagenumb_tmp = ''
            # drugstructuredosageunit
            drugstructuredosageunit_tmp = ''
            # drugtreatmentduration
            drugtreatmentduration_tmp = ''
            # drugtreatmentdurationunit
            drugtreatmentdurationunit_tmp = ''
            # medicinalproduct
            medicinalproduct_tmp = ''

            # patient
            if 'patient' in entry.keys():
                entry_patient = entry['patient']
                # drug
                if 'drug' in entry_patient.keys():
                    entry_drug = entry_patient['drug']
                    for k in range(0, len(entry_drug)):
                        # actiondrug
                        if 'actiondrug' in entry_drug[k].keys():
                            actiondrug_tmp = actiondrug_tmp + '_' +  entry_drug[k]['actiondrug']
                        # activesubstance
                        if 'activesubstance' in entry_drug[k].keys():
                            for l in range(0, len(entry_drug[k]['activesubstance'])):
                                activesubstance_tmp = activesubstance_tmp + '_.._' + entry_drug[k]['activesubstance']['activesubstancename']
                        # drugadditional
                        if 'drugadditional' in entry_drug[k].keys():
                            drugadditional_tmp = drugadditional_tmp + '_' + entry_drug[k]['drugadditional']
                        # drugadministrationroute
                        if 'drugadministrationroute' in entry_drug[k].keys():
                            drugadministrationroute_tmp = drugadministrationroute_tmp + '_' + entry_drug[k]['drugadministrationroute']
                        # drugauthorizationnumb
                        if 'drugauthorizationnumb' in entry_drug[k].keys():
                            drugauthorizationnumb_tmp = drugauthorizationnumb_tmp + '_' + entry_drug[k]['drugauthorizationnumb']
                        # drugbatch number
                        if 'drugbatchnumb' in entry_drug[k].keys():
                            drugbatchnumb_tmp = drugbatchnumb_tmp + '_' + entry_drug[k]['drugbatchnumb']
                        # drugcharacterization
                        if 'drugcharacterization' in entry_drug[k].keys():
                            drugcharacterization_tmp = drugcharacterization_tmp + '_' + entry_drug[k]['drugcharacterization']
                        # drugcumulativedosagenumb
                        if 'drugcumulativedosagenumb' in entry_drug[k].keys():
                            drugcumulativedosagenumb_tmp = drugcumulativedosagenumb_tmp + '_' + entry_drug[k]['drugcumulativedosagenumb']
                        # drugcumulativedosageunit
                        if 'drugcumulativedosageunit' in entry_drug[k].keys():
                            drugcumulativedosageunit_tmp = drugcumulativedosageunit_tmp + '_' + entry_drug[k]['drugcumulativedosageunit']
                        # drugdosageform
                        if 'drugdosageform' in entry_drug[k].keys():
                            drugdosageform_tmp = drugdosageform_tmp + '_' + entry_drug[k]['drugdosageform']
                        # drugdosagetext
                        if 'drugdosagetext' in entry_drug[k].keys():
                            drugdosagetext_tmp = drugdosagetext_tmp + '_' + entry_drug[k]['drugdosagetext']
                        # drugenddate
                        if 'drugenddate' in entry_drug[k].keys():
                            drugenddate_tmp = drugenddate_tmp + '_' + entry_drug[k]['drugenddate']
                        # drugenddateformat
                        if 'drugenddateformat' in entry_drug[k].keys():
                            drugenddateformat_tmp = drugenddateformat_tmp + '_' + entry_drug[k]['drugenddateformat']
                        # drugindication
                        if 'drugindication' in entry_drug[k].keys():
                            drugindication_tmp = drugindication_tmp + '_' + entry_drug[k]['drugindication']
                        # drugintervaldosagedefinition
                        if 'drugintervaldosagedefinition' in entry_drug[k].keys():
                            drugintervaldosagedefinition_tmp = drugintervaldosagedefinition_tmp + '_' + entry_drug[k]['drugintervaldosagedefinition']
                        # drugintervaldosageunitnumb
                        if 'drugintervaldosageunitnumb' in entry_drug[k].keys():
                            drugintervaldosageunitnumb_tmp = drugintervaldosageunitnumb_tmp + '_' + entry_drug[k]['drugintervaldosageunitnumb']
                        # drugrecurreadministration
                        if 'drugrecurreadministration' in entry_drug[k].keys():
                            drugrecurreadministration_tmp = drugrecurreadministration_tmp + '_' + entry_drug[k]['drugrecurreadministration']
                        # drugseparatedosagenumb
                        if 'drugseparatedosagenumb' in entry_drug[k].keys():
                            drugseparatedosagenumb_tmp = drugseparatedosagenumb_tmp + '_' + entry_drug[k]['drugseparatedosagenumb']
                        # drugstartdate
                        if 'drugstartdate' in entry_drug[k].keys():
                            drugstartdate_tmp = drugstartdate_tmp + '_' + entry_drug[k]['drugstartdate']
                        # drugstartdateformat
                        if 'drugstartdateformat' in entry_drug[k].keys():
                            drugstartdateformat_tmp = drugstartdateformat_tmp + '_' + entry_drug[k]['drugstartdateformat']
                        # drugstructuredosagenumb
                        if 'drugstructuredosagenumb' in entry_drug[k].keys():
                            drugstructuredosagenumb_tmp = drugstructuredosagenumb_tmp + '_' + entry_drug[k]['drugstructuredosagenumb']
                        # drugstructuredosageunit
                        if 'drugstructuredosageunit' in entry_drug[k].keys():
                            drugstructuredosageunit_tmp = drugstructuredosageunit_tmp + '_' + entry_drug[k]['drugstructuredosageunit']
                        # drugtreatmentduration
                        if 'drugtreatmentduration' in entry_drug[k].keys():
                            drugtreatmentduration_tmp = drugtreatmentduration_tmp + '_' + entry_drug[k]['drugtreatmentduration']
                        # drugtreatmentdurationunit
                        if 'drugtreatmentdurationunit' in entry_drug[k].keys():
                            if entry_drug[k]['drugtreatmentdurationunit'] is not None:
                                drugtreatmentdurationunit_tmp = drugtreatmentdurationunit_tmp + '_' + entry_drug[k]['drugtreatmentdurationunit']
                        # medicinalproduct
                        if 'medicinalproduct' in entry_drug[k].keys():
                            if entry_drug[k]['medicinalproduct'] is not None:
                                medicinalproduct_tmp = medicinalproduct_tmp + '_' + entry_drug[k]['medicinalproduct']

                        if len(entry_drug) > 1:
                            # actiondrug
                            actiondrug_tmp = actiondrug_tmp + '_._'
                            # activesubstance
                            activesubstance_tmp = activesubstance_tmp + '_._'
                            # drugadditional
                            drugadditional_tmp = drugadditional_tmp + '_._'
                            # drugadministrationroute
                            drugadministrationroute_tmp = drugadministrationroute_tmp + '_._'
                            # drugauthorizationnumb
                            drugauthorizationnumb_tmp = drugauthorizationnumb_tmp + '_._'
                            # drugbatchnumb
                            drugbatchnumb_tmp = drugbatchnumb_tmp + '_._'
                            # drugcharacterization
                            drugcharacterization_tmp = drugcharacterization_tmp + '_._'
                            # drugcumulativedosagenumb
                            drugcumulativedosagenumb_tmp = drugcumulativedosagenumb_tmp + '_._'
                            # drugcumulativedosageunit
                            drugcumulativedosageunit_tmp = drugcumulativedosageunit_tmp + '_._'
                            # drugdosageform
                            drugdosageform_tmp = drugdosageform_tmp + '_._'
                            # drugdosagetext
                            drugdosagetext_tmp = drugdosagetext_tmp + '_._'
                            # drugenddate
                            drugenddate_tmp = drugenddate_tmp + '_._'
                            # drugenddateformat
                            drugenddateformat_tmp = drugenddateformat_tmp + '_._'
                            # drugindication
                            drugindication_tmp = drugindication_tmp + '_._'
                            # drugintervaldosagedefinition
                            drugintervaldosagedefinition_tmp = drugintervaldosagedefinition_tmp + '_._'
                            # drugintervaldosageunitnumb
                            drugintervaldosageunitnumb_tmp = drugintervaldosageunitnumb_tmp + '_._'
                            # drugrecurreadministration
                            drugrecurreadministration_tmp = drugrecurreadministration_tmp + '_._'
                            # drugseparatedosagenumb
                            drugseparatedosagenumb_tmp = drugseparatedosagenumb_tmp + '_._'
                            # drugstartdate
                            drugstartdate_tmp = drugstartdate_tmp + '_._'
                            # drugstartdateformat
                            drugstartdateformat_tmp = drugstartdateformat_tmp + '_._'
                            # drugstructuredosagenumb
                            drugstructuredosagenumb_tmp = drugstructuredosagenumb_tmp + '_._'
                            # drugstructuredosageunit
                            drugstructuredosageunit_tmp = drugstructuredosageunit_tmp + '_._'
                            # drugtreatmentduration
                            drugtreatmentduration_tmp = drugtreatmentduration_tmp + '_._'
                            # drugtreatmentdurationunit
                            drugtreatmentdurationunit_tmp = drugtreatmentdurationunit_tmp + '_._'
                            # medicinalproduct
                            medicinalproduct_tmp = medicinalproduct_tmp + '_._'

            action.append(actiondrug_tmp)
            active_substance.append(activesubstance_tmp)
            drug_additional.append(drugadditional_tmp)
            admin_route.append(drugadministrationroute_tmp)
            authorization_no.append(drugauthorizationnumb_tmp)
            batch_no.append(drugbatchnumb_tmp)
            drug_char.append(drugcharacterization_tmp)
            drug_cum_dosage.append(drugcumulativedosagenumb_tmp)
            drug_cum_dosage_units.append(drugcumulativedosageunit_tmp)
            drug_dosage_form.append(drugdosageform_tmp)
            drug_dosage_text.append(drugdosagetext_tmp)
            drug_end_date.append(drugenddate_tmp)
            drug_end_date_format.append(drugenddateformat_tmp)
            drug_indication.append(drugindication_tmp)
            drug_interval_dosage_def.append(drugintervaldosagedefinition_tmp)
            drug_interval_dosage_no.append(drugintervaldosageunitnumb_tmp)
            drug_recurr_admin.append(drugrecurreadministration_tmp)
            drug_sep_dosage_no.append(drugseparatedosagenumb_tmp)
            drug_start_date.append(drugstartdate_tmp)
            drug_start_date_format.append(drugstartdateformat_tmp)
            drug_structure_dosage_no.append(drugstructuredosagenumb_tmp)
            drug_structure_dosage_unit.append(drugstructuredosageunit_tmp)
            drug_treatment_duration.append(drugtreatmentduration_tmp)
            drug_treatment_duration_unit.append(drugtreatmentdurationunit_tmp)
            medicinal_product.append(medicinalproduct_tmp)

        elapsed = timeit.default_timer() - start_time
        print('{time:0.2f} ms to complete'.format(time = elapsed*1000))

    # 3. Generate a list of lists
    start_time = timeit.default_timer()
    print('Converting lists to dataframe...')
    data_3 = [action, active_substance, drug_additional, admin_route, authorization_no,
             batch_no, drug_char, drug_cum_dosage, drug_cum_dosage_units, drug_dosage_form, drug_dosage_text,
             drug_end_date, drug_end_date_format, drug_indication, drug_interval_dosage_def, drug_interval_dosage_no,
         drug_recurr_admin, drug_sep_dosage_no,drug_start_date, drug_start_date_format, drug_structure_dosage_no,
         drug_structure_dosage_unit, drug_treatment_duration, drug_treatment_duration_unit, medicinal_product]

    # 4. Convert to dataframe
    df = pd.DataFrame(data_3).transpose()
    df.columns = ['action', 'active_substance', 'drug_additional', 'admin_route',
                 'authorization_no', 'batch_no', 'drug_char', 'drug_cum_dosage', 'drug_cum_dosage_units',
              'drug_dosage_form', 'drug_dosage_text', 'drug_end_date', 'drug_end_date_format', 'drug_indication',
             'drug_interval_dosage_def', 'drug_interval_dosage_no', 'drug_recurr_admin', 'drug_sep_dosage_no',
             'drug_start_date', 'drug_start_date_format', 'drug_structure_dosage_no', 'drug_structure_dosage_unit',
             'drug_treatment_duration', 'drug_treatment_duration_unit', 'medicinal_product']

    df = df.replace('', 'NA')

    elapsed = timeit.default_timer() - start_time
    print('{time:0.2f} ms to complete.\n'.format(time = elapsed*1000))

    return df


def section_3(data_2):
    "application_number_tmp, brand_name_tmp, ... substance_name_tmp, unii_tmp"
    # 1. Initialize lists
    app_no = []
    brand_name = []
    generic_name = []
    manufacturer_name = []
    nui = []
    package_ndc = []
    pharm_class_cs = []
    pharm_class_epc = []
    pharm_class_pe = []
    pharm_class_moa = []
    product_ndc = []
    product_type = []
    route = []
    rxcui = []
    spl_id = []
    spl_set_id = []
    substance_name = []
    unii = []

    # 2. Convert the data
    num_entries = 0

    for i in range(0,len(data_2)):
        start_time = timeit.default_timer()
        print('Section 3, file {} of {}...'.format(i+1, len(data_2)))
        for j in range(0, len(data_2[i]['results'])):
            num_entries += 1
            # application_number
            application_number_tmp = ''
            # brand_name
            brand_name_tmp  = ''
            # generic_name
            generic_name_tmp = ''
            # manufacturer_name
            manufacturer_name_tmp = ''
            # nui
            nui_tmp = ''
            # package_ndc
            package_ndc_tmp = ''
            # pharm_class_cs
            pharm_class_cs_tmp = ''
            # pharm_class_epc
            pharm_class_epc_tmp = ''
            # pharm_class_pe
            pharm_class_pe_tmp = ''
            # pharm_class_moa
            pharm_class_moa_tmp = ''
            # product_ndc
            product_ndc_tmp = ''
            # product_type
            product_type_tmp = ''
            # route
            route_tmp = ''
            # rxcui
            rxcui_tmp = ''
            # spl_id
            spl_id_tmp = ''
            # spl_set_id
            spl_set_id_tmp = ''
            # substance_name
            substance_name_tmp = ''
            # unii
            unii_tmp = ''

            entry = data_2[i]['results'][j]
            # patient
            if 'patient' in entry.keys():
                entry_patient = entry['patient']
                # drug
                if 'drug' in entry_patient.keys():
                    entry_drug = entry_patient['drug']
                    for k in range(0, len(entry_drug)):
                        # openfda
                        if 'openfda' in entry_drug[k].keys():
                            entry_openfda = entry_drug[k]['openfda']
                            keys = entry_openfda.keys()
                            # application_number
                            if 'application_number' in keys:
                                for l in range(0,len(entry_openfda['application_number'])):
                                    application_number_tmp = application_number_tmp + '_.._' + entry_openfda['application_number'][l]
                            # brand_name
                            if 'brand_name' in keys:
                                for l in range(0,len(entry_openfda['brand_name'])):
                                    brand_name_tmp = brand_name_tmp + '_.._' + entry_openfda['brand_name'][l]
                            # generic_name
                            if 'generic_name' in keys:
                                for l in range(0, len(entry_openfda['generic_name'])):
                                    generic_name_tmp = generic_name_tmp + '_.._' + entry_openfda['generic_name'][l]
                            # manufacturer_name
                            if 'manufacturer_name' in keys:
                                for l in range(0, len(entry_openfda['manufacturer_name'])):
                                    manufacturer_name_tmp = manufacturer_name_tmp + '_.._' + entry_openfda['manufacturer_name'][l]
                            # nui
                            if 'nui' in keys:
                                for l in range(0, len(entry_openfda['nui'])):
                                    nui_tmp = nui_tmp + '_.._' + entry_openfda['nui'][l]
                            # package_ndc
                            if 'package_ndc' in keys:
                                for l in range(0, len(entry_openfda['package_ndc'])):
                                    package_ndc_tmp = package_ndc_tmp + '_.._' + entry_openfda['package_ndc'][l]
                            # pharm_class_cs
                            if 'pharm_class_cs' in keys:
                                for l in range(0, len(entry_openfda['pharm_class_cs'])):
                                    pharm_class_cs_tmp = pharm_class_cs_tmp + '_.._' + entry_openfda['pharm_class_cs'][l]
                            # pharm_class_epc
                            if 'pharm_class_epc' in keys:
                                for l in range(0, len(entry_openfda['pharm_class_epc'])):
                                    pharm_class_epc_tmp = pharm_class_epc_tmp + '_.._' + entry_openfda['pharm_class_epc'][l]
                            # pharm_class_pe
                            if 'pharm_class_pe' in keys:
                                for l in range(0, len(entry_openfda['pharm_class_pe'])):
                                    pharm_class_pe_tmp = pharm_class_pe_tmp + '_.._' + entry_openfda['pharm_class_pe'][l]
                            # pharm_class_moa
                            if 'pharm_class_moa' in keys:
                                for l in range(0, len(entry_openfda['pharm_class_moa'])):
                                    pharm_class_moa_tmp = pharm_class_moa_tmp + '_.._' + entry_openfda['pharm_class_moa'][l]
                            # product_ndc
                            if 'product_ndc' in keys:
                                for l in range(0, len(entry_openfda['product_ndc'])):
                                    product_ndc_tmp = product_ndc_tmp + '_.._' + entry_openfda['product_ndc'][l]
                            # product_type
                            if 'product_type' in keys:
                                for l in range(0, len(entry_openfda['product_type'])):
                                    product_type_tmp = product_type_tmp + '_.._' + entry_openfda['product_type'][0]
                            # route
                            if 'route' in keys:
                                for l in range(0, len(entry_openfda['route'])):
                                    route_tmp = route_tmp + '_.._' + entry_openfda['route'][l]
                            # rxcui
                            if 'rxcui' in keys:
                                for l in range(0, len(entry_openfda['rxcui'])):
                                    rxcui_tmp = rxcui_tmp + '_.._' + entry_openfda['rxcui'][l]
                            # spl_id
                            if 'spl_id' in keys:
                                for l in range(0, len(entry_openfda['spl_id'])):
                                    spl_id_tmp = spl_id_tmp + '_.._' + entry_openfda['spl_id'][l]
                            # spl_set_id
                            if 'spl_set_id' in keys:
                                for l in range(0, len(entry_openfda['spl_set_id'])):
                                    spl_set_id_tmp = spl_set_id_tmp + '_.._' + entry_openfda['spl_set_id'][l]
                            # substance_name
                            if 'substance_name' in keys:
                                for l in range(0, len(entry_openfda['substance_name'])):
                                    substance_name_tmp = substance_name_tmp + '_.._' + entry_openfda['substance_name'][l]
                            # unii
                            if 'unii' in keys:
                                for l in range(0, len(entry_openfda['unii'])):
                                    unii_tmp = unii_tmp + '_.._' + entry_openfda['unii'][l]

                        if len(entry_drug) > 1:
                            # application_number
                            application_number_tmp = application_number_tmp + '_._'
                            # brand_name
                            brand_name_tmp  = brand_name_tmp + '_._'
                            # generic_name
                            generic_name_tmp = generic_name_tmp + '_._'
                            # manufacturer_name
                            manufacturer_name_tmp = manufacturer_name_tmp + '_._'
                            # nui
                            nui_tmp = nui_tmp + '_._'
                            # package_ndc
                            package_ndc_tmp = package_ndc_tmp + '_._'
                            # pharm_class_cs
                            pharm_class_cs_tmp = pharm_class_cs_tmp + '_._'
                            # pharm_class_epc
                            pharm_class_epc_tmp = pharm_class_epc_tmp + '_._'
                            # pharm_class_pe
                            pharm_class_pe_tmp = pharm_class_pe_tmp + '_._'
                            # pharm_class_moa
                            pharm_class_moa_tmp = pharm_class_moa_tmp + '_._'
                            # product_ndc
                            product_ndc_tmp = product_ndc_tmp + '_._'
                            # product_type
                            product_type_tmp = product_type_tmp + '_._'
                            # route
                            route_tmp = route_tmp + '_._'
                            # rxcui
                            rxcui_tmp = rxcui_tmp + '_._'
                            # spl_id
                            spl_id_tmp = spl_id_tmp + '_._'
                            # spl_set_id
                            spl_set_id_tmp = spl_set_id_tmp + '_._'
                            # substance_name
                            substance_name_tmp = substance_name_tmp + '_._'
                            # unii
                            unii_tmp = unii_tmp + '_._'

            app_no.append(application_number_tmp)
            brand_name.append(brand_name_tmp)
            generic_name.append(generic_name_tmp)
            manufacturer_name.append(manufacturer_name_tmp)
            nui.append(nui_tmp)
            package_ndc.append(package_ndc_tmp)
            pharm_class_cs.append(pharm_class_cs_tmp)
            pharm_class_epc.append(pharm_class_epc_tmp)
            pharm_class_pe.append(pharm_class_pe_tmp)
            pharm_class_moa.append(pharm_class_moa_tmp)
            product_ndc.append(product_ndc_tmp)
            product_type.append(product_type_tmp)
            route.append(route_tmp)
            rxcui.append(rxcui_tmp)
            spl_id.append(spl_id_tmp)
            spl_set_id.append(spl_set_id_tmp)
            substance_name.append(substance_name_tmp)
            unii.append(unii_tmp)

        elapsed = timeit.default_timer() - start_time
        print('{time:0.2f} ms to complete'.format(time = elapsed*1000))

    # 3. Generate a list of lists
    start_time = timeit.default_timer()
    print('Converting lists to dataframe...')
    data_3 = [app_no, brand_name, generic_name, manufacturer_name, nui, package_ndc, pharm_class_cs,
              pharm_class_epc, pharm_class_pe, pharm_class_moa, product_ndc, product_type, route, rxcui,
              spl_id, spl_set_id, substance_name, unii]

    # 4. Convert to dataframe
    df = pd.DataFrame(data_3).transpose()
    df.columns = ['app_no', 'brand_name','generic_name', 'manufacturer_name', 'nui', 'package_ndc',
                  'pharm_class_cs', 'pharm_class_epc', 'pharm_class_pe','pharm_class_moa',
                  'product_ndc', 'product_type', 'route', 'rxcui', 'spl_id', 'spl_set_id', 'substance_name',
             'unii']

    df = df.replace('', 'NA')

    elapsed = timeit.default_timer() - start_time
    print('{time:0.2f} ms to complete.\n'.format(time = elapsed*1000))

    return df

def section_4(data_2):
    "patient_age_group, patient_death_date, ... patient_sex, patient_weight"
    # 1. Initialize the lists
    patient_age_group = []
    patient_death_date = []
    patient_death_date_format = []
    patient_onset_age = []
    patient_onset_age_unit = []
    patient_sex = []
    patient_weight = []

    # 2. Convert the data
    num_entries = 0

    for i in range(0,len(data_2)):
        start_time = timeit.default_timer()
        print('Section 4, file {} of {}...'.format(i+1, len(data_2)))
        for j in range(0, len(data_2[i]['results'])):
            num_entries += 1
            entry = data_2[i]['results'][j]
            # patient
            if 'patient' in entry.keys():
                entry_patient = entry['patient']
                # patientagegroup
                if 'patientagegroup' in entry_patient.keys() and entry_patient['patientagegroup'] is not None:
                    patient_age_group.append(entry_patient['patientagegroup'])
                else:
                    patient_age_group.append('NA')
                # patientdeath
                if 'patientdeath' in entry_patient.keys() and entry_patient['patientdeath'] is not None:
                    # patientdeathdate
                    if 'patientdeathdate' in entry_patient['patientdeath'].keys() and entry_patient['patientdeath']['patientdeathdate'] is not None:
                        patient_death_date.append(entry_patient['patientdeath']['patientdeathdate'])
                    else:
                        patient_death_date.append('NA')
                    # patientdeathdateformat
                    if 'patientdeathdateformat' in entry_patient['patientdeath'].keys() and entry_patient['patientdeath']['patientdeathdateformat'] is not None:
                        patient_death_date_format.append(entry_patient['patientdeath']['patientdeathdateformat'])
                    else:
                        patient_death_date_format.append('NA')
                else:
                    patient_death_date.append('NA')
                    patient_death_date_format.append('NA')
                # patientonsetage
                if 'patientonsetage' in entry_patient.keys() and entry_patient['patientonsetage'] is not None:
                    patient_onset_age.append(entry_patient['patientonsetage'])
                else:
                    patient_onset_age.append('NA')
                # patientonsetageunit
                if 'patientonsetageunit' in entry_patient.keys() and entry_patient['patientonsetageunit'] is not None:
                    patient_onset_age_unit.append(entry_patient['patientonsetageunit'])
                else:
                    patient_onset_age_unit.append('NA')
                # patientsex
                if 'patientsex' in entry_patient.keys():
                    patient_sex.append(entry_patient['patientsex'])
                else:
                    patient_sex.append('NA')
                # patientweight
                if 'patientweight' in entry_patient.keys():
                    patient_weight.append(entry_patient['patientweight'])
                else:
                    patient_weight.append('NA')

            else:
                patient_age_group.append('NA')
                patient_death_date.append('NA')
                patient_death_date_format.append('NA')
                patient_onset_age.append('NA')
                patient_onset_age_unit.append('NA')
                patient_sex.append('NA')
                patient_weight.append('NA')

        elapsed = timeit.default_timer() - start_time
        print('{time:0.2f} ms to complete'.format(time = elapsed*1000))

    # 3. Generate a list of lists
    start_time = timeit.default_timer()
    print('Converting lists to dataframe...')
    data_3 = [patient_age_group,
             patient_death_date, patient_death_date_format, patient_onset_age,
              patient_onset_age_unit, patient_sex, patient_weight]

    # 4. Convert to dataframe
    df = pd.DataFrame(data_3).transpose()
    df.columns = ['patient_age_group', 'patient_death_date', 'patient_death_date_format', 'patient_onset_age',
                 'patient_onset_age_unit', 'patient_sex', 'patient_weight']

    df = df.replace('', 'NA')

    elapsed = timeit.default_timer() - start_time
    print('{time:0.2f} ms to complete.\n'.format(time = elapsed*1000))



    return df

def section_5(data_2):
    "reaction_medDRA_pt, ... reporter_country"
    # 1. Initialize the lists
    reaction_medDRA_pt = []
    reaction_medDRA_version_pt = []
    reaction_outcome = []
    summary = []
    lit_ref = []
    qualification = []
    reporter_country = []

    # 2. Convert the data
    num_entries = 0

    for i in range(0,len(data_2)):
        start_time = timeit.default_timer()
        print('Section 5, file {} of {}...'.format(i+1, len(data_2)))
        for j in range(0, len(data_2[i]['results'])):
            num_entries += 1
            entry = data_2[i]['results'][j]

            reaction_medDRA_pt_tmp = ''
            reaction_medDRA_version_pt_tmp = ''
            reaction_outcome_tmp = ''
            # patient
            if 'patient' in entry.keys():
                entry_patient = entry['patient']
                # reaction
                if 'reaction' in entry_patient.keys() and entry_patient['reaction'] is not None:
                    entry_reaction = entry_patient['reaction']
                    for l in range(0, len(entry_reaction)):
                        # reactionmeddrapt
                        if 'reactionmeddrapt' in entry_reaction[l].keys() and entry_reaction[l]['reactionmeddrapt'] is not None:
                            reaction_medDRA_pt_tmp = reaction_medDRA_pt_tmp + '_._' + entry_reaction[l]['reactionmeddrapt']
                        # reactionmeddraversionpt
                        if 'reactionmeddraversionpt' in entry_reaction[l].keys() and entry_reaction[l]['reactionmeddraversionpt'] is not None:
                            reaction_medDRA_version_pt_tmp = reaction_medDRA_version_pt_tmp + '_._' + entry_reaction[l]['reactionmeddraversionpt']
                        # reactionoutcome
                        if 'reactionoutcome' in entry_reaction[l].keys() and entry_reaction[l]['reactionoutcome'] is not None:
                            reaction_outcome_tmp = reaction_outcome_tmp + '_._' + entry_reaction[l]['reactionoutcome']

                # Summary
                if 'summary' in entry_patient.keys():
                    summary.append(entry_patient['summary']['narrativeincludeclinical'])
                else:
                    summary.append('NA')

            else:
                summary.append('NA')

            reaction_medDRA_pt.append(reaction_medDRA_pt_tmp)
            reaction_medDRA_version_pt.append(reaction_medDRA_version_pt_tmp)
            reaction_outcome.append(reaction_outcome_tmp)

            # primarysource
            if 'primarysource' in entry.keys() and entry['primarysource'] is not None:
                # literaturereference
                if 'literaturereference' in entry['primarysource'].keys():
                    lit_ref.append(entry['primarysource']['literaturereference'])
                else:
                    lit_ref.append('NA')
                # qualification
                if 'qualification' in entry['primarysource'].keys():
                    qualification.append(entry['primarysource']['qualification'])
                else:
                    qualification.append('NA')
                # reportercountry
                if 'reportercountry' in entry['primarysource'].keys():
                    reporter_country.append(entry['primarysource']['reportercountry'])
                else:
                    reporter_country.append('NA')
            else:
                lit_ref.append('NA')
                qualification.append('NA')
                reporter_country.append('NA')

        elapsed = timeit.default_timer() - start_time
        print('{time:0.2f} ms to complete'.format(time = elapsed*1000))

    # 3. Generate a list of lists
    print('Converting lists to dataframe...')
    start_time = timeit.default_timer()
    data_3 = [reaction_medDRA_pt, reaction_medDRA_version_pt, reaction_outcome, summary, lit_ref,
             qualification, reporter_country]

    # 4. Convert to dataframe
    df = pd.DataFrame(data_3).transpose()
    df.columns = ['reaction_medDRA_pt', 'reaction_medDRA_version_pt','reaction_outcome', 'summary', 'lit_ref',
                 'qualification', 'reporter_country']

    df = df.replace('', 'NA')

    elapsed = timeit.default_timer() - start_time
    print('{time:0.2f} ms to complete.\n'.format(time = elapsed*1000))

    return df

def section_6(data_2):
    "primary_source_country, ... safety_report_version"
    # 1. Initialize the lists
    primary_source_country = []
    receipt_date = []
    receipt_date_format = []
    receive_date = []
    receive_date_format = []
    receiver_organization = []
    receiver_type = []
    report_duplicate = []
    report_duplicate_source = []
    report_type = []
    safety_report_id = []
    safety_report_version = []

    # 2. Convert the data
    num_entries = 0

    for i in range(0,len(data_2)):
        start_time = timeit.default_timer()
        print('Section 6, file {} of {}...'.format(i+1, len(data_2)))
        for j in range(0, len(data_2[i]['results'])):
            num_entries += 1
            entry = data_2[i]['results'][j]
            # primarysourcecountry
            if 'primarysourcecountry' in entry.keys() and entry['primarysourcecountry'] is not None:
                primary_source_country.append(entry['primarysourcecountry'])
            else:
                primary_source_country.append('NA')
            # receiptdate
            if 'receiptdate' in entry.keys() and entry['receiptdate'] is not None:
                receipt_date.append(entry['receiptdate'])
            else:
                receipt_date.append('NA')
            # receiptdateformat
            if 'receiptdateformat' in entry.keys() and entry['receiptdateformat'] is not None:
                receipt_date_format.append(entry['receiptdateformat'])
            else:
                receipt_date_format.append('NA')
            # receivedate
            if 'receivedate' in entry.keys() and entry['receivedate'] is not None:
                receive_date.append(entry['receivedate'])
            else:
                receive_date.append('NA')
            # receivedateformat
            if 'receivedateformat' in entry.keys() and entry['receivedateformat'] is not None:
                receive_date_format.append(entry['receivedateformat'])
            else:
                receive_date_format.append('NA')
            # receiver
            if 'receiver' in entry.keys() and entry['receiver'] is not None:
                # receiverorganization
                if 'receiverorganization' in entry['receiver'].keys() and entry['receiver']['receiverorganization'] is not None:
                    receiver_organization.append(entry['receiver']['receiverorganization'])
                else:
                    receiver_organization.append('NA')
                # receivertype
                if 'receivertype' in entry['receiver'].keys() and entry['receiver']['receivertype'] is not None:
                    receiver_type.append(entry['receiver']['receivertype'])
                else:
                    receiver_type.append('NA')
            else:
                receiver_organization.append('NA')
                receiver_type.append('NA')

            # reportduplicate
            if 'reportduplicate' in entry.keys() and entry['reportduplicate'] is not None:
                # duplicatenumb
                if 'duplicatenumb' in entry['reportduplicate'].keys() and entry['reportduplicate']['duplicatenumb'] is not None:
                    report_duplicate.append(entry['reportduplicate']['duplicatenumb'])
                else:
                    report_duplicate.append('NA')
                # duplicatesource
                if 'duplicatesource' in entry['reportduplicate'].keys() and entry['reportduplicate']['duplicatesource'] is not None:
                    report_duplicate_source.append(entry['reportduplicate']['duplicatesource'])
                else:
                    report_duplicate_source.append('NA')
            else:
                report_duplicate.append('NA')
                report_duplicate_source.append('NA')

            # reporttype
            if 'reporttype' in entry.keys() and entry['reporttype'] is not None:
                # reporttype
                report_type.append(entry['reporttype'])
            else:
                report_type.append('NA')

            # safetyreportid
            if 'safetyreportid' in entry.keys() and entry['safetyreportid'] is not None:
                # safetyreportid
                safety_report_id.append(entry['safetyreportid'])
            else:
                safety_report_id.append('NA')

            # safetyreportid
            if 'safetyreportversion' in entry.keys() and entry['safetyreportversion'] is not None:
                # safetyreportid
                safety_report_version.append(entry['safetyreportversion'])
            else:
                safety_report_version.append('NA')

        elapsed = timeit.default_timer() - start_time
        print('{time:0.2f} ms to complete'.format(time = elapsed*1000))

    # 3. Generate list of lists
    print('Converting lists to dataframe...')
    start_time = timeit.default_timer()
    data_3 = [primary_source_country, receipt_date, receipt_date_format, receive_date, receive_date_format,
             receive_date, receiver_organization, receiver_type, report_duplicate, report_duplicate_source, report_type,
             safety_report_id, safety_report_version]


    # 4. Convert to dataframe
    df = pd.DataFrame(data_3).transpose()
    df.columns = ['primary_source_country', 'receipt_date', 'receipt_date_format', 'receive_date', 'receive_date_format',
             'receive_date', 'receiver_organization', 'receiver_type', 'report_duplicate', 'report_duplicate_source',
                 'report_type', 'safety_report_id', 'safety_report_version']

    df = df.replace('', 'NA')

    elapsed = timeit.default_timer() - start_time
    print('{time:0.2f} ms to complete.\n'.format(time = elapsed*1000))

    return df

def section_7(data_2):
    "sender_organization, ... transmission_date_format"
    # 1. Initialize the lists
    sender_organization = []
    sender_type = []
    serious = []
    seriousness_congential_anomali = []
    seriousness_death = []
    seriousness_disabling = []
    seriousness_hospitalization = []
    seriousness_lifethreatening = []
    seriousness_other = []
    transmission_date = []
    transmission_date_format = []

    # 2. Convert the data
    num_entries = 0

    for i in range(0,len(data_2)):
        start_time = timeit.default_timer()
        print('Section 7, file {} of {}...'.format(i+1, len(data_2)))
        for j in range(0, len(data_2[i]['results'])):
            num_entries += 1
            entry = data_2[i]['results'][j]
            # sender
            if 'sender' in entry.keys() and entry['sender'] is not None:
                # senderorganization
                if 'senderorganization' in entry['sender'].keys() and entry['sender']['senderorganization'] is not None:
                    sender_organization.append(entry['sender']['senderorganization'])
                else:
                    sender_organization.append('NA')
                # sendertype
                if 'sendertype' in entry['sender'].keys() and entry['sender']['sendertype'] is not None:
                    sender_type.append(entry['sender']['sendertype'])
                else:
                    sender_type.append('0')
            else:
                sender_organization.append('NA')
                sender_type.append('0')
            # serious
            if 'serious' in entry.keys() and entry['serious'] is not None:
                serious.append(entry['serious'])
            else:
                serious.append('0')
            # seriouscongentialanomali
            if 'seriouscongentialanomali' in entry.keys() and entry['seriouscongentialanomali'] is not None:
                seriousness_congential_anomali.append(entry['seriouscongentialanomali'])
            else:
                seriousness_congential_anomali.append('0')
            # seriousnessdeath
            if 'seriousnessdeath' in entry.keys() and entry['seriousnessdeath'] is not None:
                seriousness_death.append(entry['seriousnessdeath'])
            else:
                seriousness_death.append('0')
            # seriousnessdisabling
            if 'seriousnessdisabling' in entry.keys() and entry['seriousnessdisabling'] is not None:
                seriousness_disabling.append(entry['seriousnessdisabling'])
            else:
                seriousness_disabling.append('0')
            # seriousnesshospitalization
            if 'seriousnesshospitalization' in entry.keys() and entry['seriousnesshospitalization'] is not None:
                seriousness_hospitalization.append(entry['seriousnesshospitalization'])
            else:
                seriousness_hospitalization.append('0')
            # seriousnesslifethreatening
            if 'seriousnesslifethreatening' in entry.keys() and entry['seriousnesslifethreatening'] is not None:
                seriousness_lifethreatening.append(entry['seriousnesslifethreatening'])
            else:
                seriousness_lifethreatening.append('0')
            # seriousnessother
            if 'seriousnessother' in entry.keys() and entry['seriousnessother'] is not None:
                seriousness_other.append(entry['seriousnessother'])
            else:
                seriousness_other.append('0')
            # transmissiondate
            if 'transmissiondate' in entry.keys() and entry['transmissiondate'] is not None:
                transmission_date.append(entry['transmissiondate'])
            else:
                transmission_date.append('NA')
            # transmissiondateformat
            if 'transmissiondateformat' in entry.keys() and entry['transmissiondateformat'] is not None:
                transmission_date_format.append(entry['transmissiondateformat'])
            else:
                transmission_date_format.append('NA')

        elapsed = timeit.default_timer() - start_time
        print('{time:0.2f} ms to complete'.format(time = elapsed*1000))

    # 3. Generate list of lists
    print('Converting lists to dataframe...')
    start_time = timeit.default_timer()
    data_3 = [sender_organization, sender_type, serious, seriousness_congential_anomali, seriousness_death,
              seriousness_disabling, seriousness_hospitalization, seriousness_lifethreatening, seriousness_other,
                transmission_date, transmission_date_format]

    # 4. Convert to dataframe
    df = pd.DataFrame(data_3).transpose()
    df.columns = ['sender_organization', 'sender_type', 'serious', 'seriousness_congential_anomali', 'seriousness_death',
              'seriousness_disabling', 'seriousness_hospitalization', 'seriousness_lifethreatening', 'seriousness_other',
                'transmission_date', 'transmission_date_format']

    df = df.replace('', 'NA')

    elapsed = timeit.default_timer() - start_time
    print('{time:0.2f} ms to complete.\n'.format(time = elapsed*1000))

    return df
