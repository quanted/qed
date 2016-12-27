from __future__ import division
from collections import OrderedDict
import json
import OreCalculator


def ore(inputs, query_result_list):
    ore_class_list = []
    class_inputs = exp_duration_handler(inputs)

    for query in query_result_list:
        """
        Loop over each "row" of the spreadsheet; this is determined by the SQLite query
        from user's inputs on the Exposure Scenario tab.
        """
        # print query.keys()  #  SQLite query (row_factory.Row)

        # NonCancerInputs
        activity = query['Activity']
        formulation = query['Formulation']
        app_equip = query['AppEquip']
        app_type = query['AppType']
        crop_target = query['Category']
        crop_name = inputs['exp_crop']
        app_rate = inputs['app_rate']['app_rate_' + query['Formulation']]
        app_rate_unit = query['AppRateUnit']
        area_treated = query['TreatedVal']
        area_treated_unit = query['TreatedUnit']
        active_ingredient = inputs['activeIngredient']

        # DermalNonCancer specific inputs
        abs_frac_dermal = class_inputs['dermal']['abs_frac']
        bw_dermal = class_inputs['dermal']['bw_adult']
        pod_dermal = class_inputs['dermal']['nc_POD']
        loc_dermal = class_inputs['dermal']['nc_LOC']
        # Dermal PPE (personal protection equipment)
        dermal_unit_exp_sl_no_G = query['DUESLNoG']
        dermal_unit_exp_sl_G = query['DUESLG']
        dermal_unit_exp_dl_g = query['DUEDLG']
        dermal_unit_exp_sl_G_crh = query['DUESLGCRH']
        dermal_unit_exp_dl_G_crh = query['DUEDLGCRH']
        dermal_unit_exp_ec = query['DUEEC']

        # InhalNonCancer specific inputs
        abs_frac_inhal = class_inputs['inhal']['abs_frac']
        bw_inhal = class_inputs['inhal']['bw_adult']
        pod_inhal = class_inputs['inhal']['nc_POD']
        loc_inhal = class_inputs['inhal']['nc_LOC']
        # Inhalation PPE (personal protection equipment)
        inhal_unit_exp_no_r = query['IUENoR']
        inhal_unit_exp_pf5r = query['IUEPF5R']
        inhal_unit_exp_pf10r = query['IUEPF10R']
        inhal_unit_exp_ec = query['IUEEC']

        # Source Columns
        sources = [query['SourceCategory'], query['SourceMRID'], query['SourceDescription'], query['SourceDER']]
        # source_category = query['SourceCategory']
        # source_mrid = query['SourceMRID']
        # source_description = query['SourceDescription']
        # source_der = query['SourceDER']

        # Create DermalNonCancer class instance
        dermal = OreCalculator.DermalNonCancer(
            activity, crop_target, app_rate, app_rate_unit, crop_name,
            loc_dermal, loc_inhal, area_treated, area_treated_unit, active_ingredient,
            formulation, app_equip, app_type,
            abs_frac_dermal, bw_dermal, pod_dermal,
            dermal_unit_exp_sl_no_G, dermal_unit_exp_sl_G, dermal_unit_exp_dl_g,
            dermal_unit_exp_sl_G_crh, dermal_unit_exp_dl_G_crh, dermal_unit_exp_ec
        )

        # Create InhalNonCancer class instance
        inhal = OreCalculator.InhalNonCancer(
            activity, crop_target, app_rate, app_rate_unit, crop_name,
            loc_dermal, loc_inhal, area_treated, area_treated_unit, active_ingredient,
            formulation, app_equip, app_type,
            abs_frac_inhal, bw_inhal, pod_inhal,
            inhal_unit_exp_no_r, inhal_unit_exp_pf5r, inhal_unit_exp_pf10r, inhal_unit_exp_ec
        )

        # Combined results?
        if inputs['expComboType'] != '1':
            if inputs['expComboType'] == '2':  # Combined: Additive Dose
                combined = OreCalculator.CombinedDose(dermal, inhal).additive_dose()
            if inputs['expComboType'] == '3':  # Combined: 1/MOE Approach
                combined = OreCalculator.CombinedDose(dermal, inhal).one_over_moe()
            if inputs['expComboType'] == '4':  # Aggregate Risk Index
                combined = OreCalculator.CombinedDose(dermal, inhal).ari()
            ore_class_list.append((dermal, inhal, sources, combined))

        else:  # Not combined
            ore_class_list.append((dermal, inhal, sources))

    ore_output = OreOutputFormatter(ore_class_list)
    output_dict = ore_output.get_output_dict()
    # print output_dict

    return output_dict


def exp_duration_handler(inputs):
    """
    Helper method to handle the Short, Intermediate, and Long term options

    ONLY SHORT TERM IS CURRENTLY ALLOWED ON THE FRONTEND

    :param inputs: dict
    :return: float
    """

    class_inputs = {'dermal': {}, 'inhal': {}}
    type = '_st'
    if inputs['expDurationType_st']:
        print "Short term"
        type = '_st'
    if inputs['expDurationType_it']:
        print "Intermediate term"
        type = '_it'
    if inputs['expDurationType_lt']:
        print "Long term"
        type = '_lt'

    class_inputs['dermal']['abs_frac'] = float(inputs['dermal_abs_frac' + type]) / 100.
    class_inputs['dermal']['bw_adult'] = inputs['bw_dermal_NC' + type]
    class_inputs['dermal']['nc_POD'] = inputs['dermal_NC_POD' + type]
    class_inputs['dermal']['nc_LOC'] = inputs['dermal_NC_LOC' + type]

    class_inputs['inhal']['abs_frac'] = float(inputs['inhalation_abs_frac' + type]) / 100.
    class_inputs['inhal']['bw_adult'] = inputs['bw_inhalation_NC' + type]
    class_inputs['inhal']['nc_POD'] = inputs['inhalation_NC_POD' + type]
    class_inputs['inhal']['nc_LOC'] = inputs['inhalation_NC_LOC' + type]

    return class_inputs


class OreOutputFormatter(object):
    def __init__(self, ore_class_list):
        """
        [
        (<ore_rest.OreCalculator.DermalNonCancer object at ...>, <ore_rest.OreCalculator.InhalNonCancer object at ...>),
        (<ore_rest.OreCalculator.DermalNonCancer object at ...>, <ore_rest.OreCalculator.InhalNonCancer object at ...>),
        (<ore_rest.OreCalculator.DermalNonCancer object at ...>, <ore_rest.OreCalculator.InhalNonCancer object at ...>)
        ]
        """

        self.dermal_class_list = []
        self.inhal_class_list = []
        self.sources_list = []
        self.combined_list = []

        for item in ore_class_list:
            self.dermal_class_list.append(item[0])
            self.inhal_class_list.append(item[1])
            self.sources_list.append(item[2])
            try:
                self.combined_list.append(item[3])
            except IndexError:
                pass

        self.output_dict = {}

    """ Example JSON schema:
    [
        'mix_loader': {
            'activity': "M/L",
            'app_equip': 'Aerial',
            'crop_target': "Corn[field crop, high acreage]",
            'loc': {'dermal': '100', 'inhal': '100'},
            'app_rate': '2',
            'app_rate_unit': 'lb ai/A',
            'area_treated': '1200',
            'area_treated_unit': 'acre',
            'dermal_unit_exp': ['220 [SL/No G]', '37.6 [SL/G]'],
            'inhal_unit_exp': ['0.219 [No-R]', '0.219 [No-R]'],
            'dermal_dose': ['1.65', '0.282'],
            'dermal_moe': ['30', '180'],
            'inhal_dose': ['0.00658', '0.00658'],
            'inhal_moe': ['3800', '3800']
        },
        'applicator': {
            'activity': "Aerial",
            'app_equip': 'Aerial',
            'crop_target': "Corn[field crop, high acreage]",
            'loc': {'dermal': '100', 'inhal': '100'},
            'app_rate': '2',
            'app_rate_unit': 'lb ai/A',
            'area_treated': '1200',
            'area_treated_unit': 'acre',
            'dermal_unit_exp': ['2.06 [EC]'],
            'inhal_unit_exp': ['0.043 [EC]'],
            'dermal_dose': ['0.0156'],
            'dermal_moe': ['3200'],
            'inhal_dose': ['0.000148'],
            'inhal_moe': ['170000']
        },
        'flagger': {
            'activity': "Flagger",
            'app_equip': 'Aerial',
            'crop_target': "Corn[field crop, high acreage]",
            'loc': {'dermal': '100', 'inhal': '100'},
            'app_rate': '2',
            'app_rate_unit': 'lb ai/A',
            'area_treated': '350',
            'area_treated_unit': 'acre',
            'dermal_unit_exp': ['11 [EC]'],
            'inhal_unit_exp': ['0.35 [No-R]'],
            'dermal_dose': ['0.0156'],
            'dermal_moe': ['3200'],
            'inhal_dose': ['0.000148'],
            'inhal_moe': ['170000']
        }
    ]
    """

    def get_output_dict(self):
        if len(self.output_dict) > 0:
            return self.output_dict
        else:
            self.dermal_formatter()
            self.inhal_formatter()
            self.sources_formatter()
            if len(self.combined_list) > 0:
                self.combined_formatter()

            return self.output_dict

    def dermal_formatter(self):
        """
        Create shared inputs portion of output_dict for a row of results on Output page
        """
        # Loop over the DermalNonCancer instances
        i = 1
        for exp_scenario in self.dermal_class_list:  # Could be either class instances list, these are the shared inputs

            attr_dict = exp_scenario.ordered_dict(exp_scenario.get_ppe_increasing_order())
            # print attr_dict.items()

            dermal_dict = {}

            dermal_unit_exp = []
            dermal_exp = []
            dermal_dose = []
            dermal_moe = []
            for k, v in attr_dict.items():

                if isinstance(attr_dict[k], OreCalculator.OreCalculator):
                    # Attributes have been ordered by PPE to match the logic of the calculator
                    # print k, attr_dict[k], attr_dict[k].moe
                    dermal_unit_exp.append(str(attr_dict[k].unit_exp) + " [" + k.upper() + "]")
                    dermal_exp.append(str(attr_dict[k].exposure_conc))
                    dermal_dose.append(str(attr_dict[k].dose_conc))
                    dermal_moe.append(str(attr_dict[k].moe))
                elif attr_dict[k] != None and attr_dict[k] != "No Data":
                    # print k, attr_dict[k]
                    dermal_dict[k] = attr_dict[k]

            dermal_dict['dermal_unit_exp'] = dermal_unit_exp
            dermal_dict['dermal_exp'] = dermal_exp
            dermal_dict['dermal_dose'] = dermal_dose
            dermal_dict['dermal_moe'] = dermal_moe

            # self.output_dict[exp_scenario.activity] = dermal_dict
            self.output_dict[str(i)] = dermal_dict
            i += 1

    def inhal_formatter(self):

        # Loop over the InhalNonCancer instances
        i = 1
        for exp_scenario in self.inhal_class_list:

            attr_dict = exp_scenario.ordered_dict(exp_scenario.get_ppe_increasing_order())
            # print attr_dict.items()

            inhal_dict = {}

            inhal_unit_exp = []
            inhal_exp = []
            inhal_dose = []
            inhal_moe = []
            for k, v in attr_dict.items():
                if isinstance(attr_dict[k], OreCalculator.OreCalculator):
                    # Attributes have been ordered by PPE to match the logic of the calculator
                    # print k, attr_dict[k], attr_dict[k].moe
                    inhal_unit_exp.append(str(attr_dict[k].unit_exp) + " [" + k.upper() + "]")
                    inhal_exp.append(str(attr_dict[k].exposure_conc))
                    inhal_dose.append(str(attr_dict[k].dose_conc))
                    inhal_moe.append(str(attr_dict[k].moe))

            inhal_dict['inhal_unit_exp'] = inhal_unit_exp
            inhal_dict['inhal_exp'] = inhal_exp
            inhal_dict['inhal_dose'] = inhal_dose
            inhal_dict['inhal_moe'] = inhal_moe

            # self.output_dict[exp_scenario.activity].update(inhal_dict)
            self.output_dict[str(i)].update(inhal_dict)
            i += 1

    def combined_formatter(self):
        i = 1
        for combined in self.combined_list:
            print combined

            self.output_dict[str(i)].update(combined)
            i += 1

    def sources_formatter(self):
        i = 1
        for sources in self.sources_list:
            sources_dict = {
                'source': {
                    'category': sources[0],
                    'mrid': sources[1],
                    'description': sources[2],
                    'der': sources[3],
                }
            }
            self.output_dict[str(i)].update(sources_dict)
            i += 1
