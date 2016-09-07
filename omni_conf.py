# Demonstration omni_conf.py file.
# Please replace all values.
from collections import OrderedDict as odict

settings = {
    'ignore_warnings': True,
}

computer_name = open('computer.txt').read().strip()
computers = {
    'zerogravitas': {
        'remote': 'rdf-comp',
        'remote_address': 'mmuetz@login.rdf.ac.uk',
        'remote_path': '/nerc/n02/n02/mmuetz/omnis/moist_profile',
        'dirs': {
            'output': '/home/markmuetz/omni_output/moist_profile/output'
        }
    },
    'rdf-comp': {
        'dirs': {
            'output': '/nerc/n02/n02/mmuetz/omni_output/moist_profile/output',
        }
    }
}

expts = ['moist_cons', 'no_moist_cons']
comp = computers['rdf-comp']
for expt in expts:
    comp['dirs']['work_' + expt] = '/nerc/n02/n02/mmuetz/um10.5_runs/2day/u-af095_64x64km2_1km_2day_moist_profile_{0}/work'.format(expt)
    comp['dirs']['results_' + expt] = '/nerc/n02/n02/mmuetz/omni_output/u-af095_64x64km2_2day_moist_profile_{}/results'.format(expt)

comp = computers['zerogravitas']
for expt in expts:
    comp['dirs']['work_' + expt] = '/home/markmuetz/omni_output/u-af095_64x64km2_1km/work_2day_moist_profile_{0}'.format(expt)
    comp['dirs']['results_' + expt] = '/home/markmuetz/omni_output/u-af095_64x64km2/results_2day_moist_profile_{}'.format(expt)


batches = odict(('batch{}'.format(i), {'index': i}) for i in range(4))
groups = odict()
ngroups = odict()
nodes = odict()
nnodes = odict()

for expt in expts:
    groups['pp5_' + expt] = {
	    'type': 'init',
	    'base_dir': 'work_' + expt,
	    'batch': 'batch0',
	    'filename_glob': '2000??????????/atmos2/atmos.pp5',
	    }

    groups['nc5_' + expt] = {
        'type': 'group_process',
        'from_group': 'pp5_' + expt,
        'base_dir': 'results_' + expt,
        'batch': 'batch1',
        'process': 'convert_pp_to_nc',
    }

    base_vars = ['q_incr_ls_rain', 'q_incr_bl_plus_cloud', 'q_incr_adv', 'q_incr_total']
    base_nodes = [bv + '_profile' for bv in base_vars]

    groups['profiles_' + expt] = {
        'type': 'nodes_process',
        'base_dir': 'results_' + expt,
        'batch': 'batch2',
        'nodes': [bn + '_' + expt for bn in base_nodes],
    }

    groups['profile_plots_' + expt] = {
        'type': 'nodes_process',
        'base_dir': 'output',
        'batch': 'batch3',
        'nodes': ['moist_profile_plots_' + expt],
    }

    for bn, bv in zip(base_nodes, base_vars):
	nodes[bn + '_' + expt] = {
	    'type': 'from_group',
	    'from_group': 'nc5_' + expt,
	    'variable': bv,
	    'process': 'domain_mean',
	}

    nodes['moist_profile_plots_' + expt] = {
        'type': 'from_nodes',
        'from_nodes': [bn + '_' + expt for bn in base_nodes],
        'process': 'plot_last_moist_profile',
    }

variables = {
    'q_incr_ls_rain': {
	'section': 4,
	'item': 182,
    },
    'q_incr_bl_plus_cloud': {
	'section': 9,
	'item': 182,
    },
    'q_incr_adv': {
	'section': 12,
	'item': 182,
    },
    'q_incr_total': {
	'section': 30,
	'item': 182,
    },
}
    
process_options = {
}
