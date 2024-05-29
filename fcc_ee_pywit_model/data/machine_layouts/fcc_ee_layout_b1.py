layout_dict = {'betas_lengths_names': ['pipe_section_1', 'resonators_1',
                                       'broadband_resonators_1'],
               'sbeg': {},
               'send': {}
               }

layout_dict['sbeg']['pipe_section_1'] = [1e4, 2e4, 3e4]
layout_dict['send']['pipe_section_1'] = [1.5e4, 2.5e4, 3.5e4]

layout_dict['sbeg']['resonators_1'] = [1e3]
layout_dict['send']['resonators_1'] = [1.001e3]

layout_dict['sbeg']['broadband_resonators_1'] = [10e3]
layout_dict['send']['broadband_resonators_1'] = [10.001e3]
