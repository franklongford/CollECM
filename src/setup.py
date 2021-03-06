"""
ColECM: Collagen ExtraCellular Matrix Simulation
SETUP ROUTINE 

Created by: Frank Longford
Created on: 01/11/2015

Last Modified: 19/04/2018
"""

import numpy as np
from scipy import constants as con
import sys, os, pickle

import utilities as ut


def get_param_defaults():
	"""
	get_param_defaults()

	Returns default simulation and analysis parameters
	"""
	
	defaults = {	'n_dim' : 2,
		    	'dt' : 0.003,
			'n_step' : 10000,
			'save_step' : 1000,
			'mass' : 1.,
			'vdw_sigma' : 1,
			'vdw_epsilon' : 1.,
			'bond_r0' : 2.**(1./6.),
			'bond_k0' : 1.,
			'angle_theta0' : np.pi,
			'angle_k0' : 1.,
			'rc' : 3.0,
			'kBT' : 1.,
			'gamma' : 0.5,
			'sigma' : np.sqrt(0.5 * (2 - 0.5) * (1 / 1.)),
			'n_fibril_x' : 3,
			'n_fibril_y' : 3,
			'n_fibril_z' : 1,
			'n_fibril' : 9,
			'l_fibril' : 10,
			'n_bead' : 90,
			'n_cell' : 0,
			'density' : 0.3,
			'l_conv' : 1,
			'res' : 7.5,
			'sharp' : 1,
			'skip' : 1,
			'l_sample' : 100,
			'min_sample' : 25,
			'P_0' : 1,
			'lambda_p' : 5E-4,
			'bond_matrix' : None,
			'vdw_matrix' : None,
			'angle_array' : None}
	"""
	defaults = {	'n_dim' : 2,
		    	'dt' : 0.004,
			'n_step' : 10000,
			'save_step' : 500,
			'mass' : 146115, # g mol-1
			'vdw_sigma' : 0.35, # um
			'vdw_epsilon' : 1.,
			'bond_r0' : 2., # um
			#'bond_r1' : 1.5 * 2.**(1./6.),
			#'bond_rb' : 1.6 * 2.**(1./6.),
			'bond_k0' : 1.,
			#'bond_k1' : 50.,
			'angle_theta0' : np.pi,
			'angle_k0' : 1.,
			'rc' : 0.07 * 3.0, # um
			'kBT' : 5.,
			'gamma' : 0.5,
			'sigma' : np.sqrt(3.75),
			'n_fibril_x' : 2,
			'n_fibril_y' : 2,
			'n_fibril_z' : 1,
			'n_fibril' : 4,
			'l_fibril' : 50,
			'n_bead' : 200,
			'l_conv' : 1,
			'res' : 7.5,
			'sharp' : 3.0,
			'skip' : 1,
			'P_0' : 1,
			'lambda_p' : 4E-5,
			'bond_matrix' : None,
			'vdw_matrix' : None}
	"""

	return defaults


def get_file_name_defaults():
	"""
	get_file_name_defaults()

	Returns default file names
	"""
	
	defaults = {'param_file_name' : False,
			'pos_file_name' : False,
			'traj_file_name' : False,
			'restart_file_name' : False,
			'output_file_name' : False,
			'gif_file_name' : False}

	return defaults


def check_file_names(input_list, file_names=False):
	"""
	check_file_names(input_list, file_names=False)

	Checks input_list to find file names
	"""

	if not file_names: file_names = get_file_name_defaults()

	if ('-param' in input_list): file_names['param_file_name'] = input_list[input_list.index('-param') + 1]
	if ('-pos' in input_list): file_names['pos_file_name'] =  input_list[input_list.index('-pos') + 1]

	if ('-traj' in input_list): file_names['traj_file_name'] =  input_list[input_list.index('-traj') + 1]
	else: file_names['traj_file_name'] = file_names['pos_file_name']
	if ('-rst' in input_list): file_names['restart_file_name'] = input_list[input_list.index('-rst') + 1]
	else: file_names['restart_file_name'] = file_names['pos_file_name']
	if ('-out' in input_list): file_names['output_file_name'] = input_list[input_list.index('-out') + 1]
	else: file_names['output_file_name'] = file_names['traj_file_name']
	if ('-gif' in input_list): file_names['gif_file_name'] = input_list[input_list.index('-gif') + 1]
	else: file_names['gif_file_name'] = file_names['traj_file_name']

	if file_names['param_file_name']: file_names['param_file_name'] = ut.check_file_name(file_names['param_file_name'], 'param', 'pkl') + '_param'
	if file_names['pos_file_name']: file_names['pos_file_name'] = ut.check_file_name(file_names['pos_file_name'], extension='npy')
	if file_names['traj_file_name']: file_names['traj_file_name'] = ut.check_file_name(file_names['traj_file_name'], 'traj', 'npy') + '_traj'
	if file_names['restart_file_name']: file_names['restart_file_name'] = ut.check_file_name(file_names['restart_file_name'], 'rst', 'npy') + '_rst'
	if file_names['output_file_name']: file_names['output_file_name'] = ut.check_file_name(file_names['output_file_name'], 'out', 'npy') + '_out'
	if file_names['gif_file_name']: file_names['gif_file_name'] = ut.check_file_name(file_names['gif_file_name'], extension='png')

	return file_names


def check_sim_param(input_list, param=False):
	"""
	check_sim_param(input_list, param=False)

	Checks input_list to overwrite simulation parameters in param dictionary 
	"""

	if not param: param = get_param_defaults()

	if ('-ndim' in input_list): param['n_dim'] = int(input_list[input_list.index('-ndim') + 1])
	if ('-dt' in input_list): param['dt'] = float(input_list[input_list.index('-dt') + 1])
	if ('-mass' in input_list): param['mass'] = float(input_list[input_list.index('-mass') + 1])
	if ('-vdw_sigma' in input_list): param['vdw_sigma'] = float(input_list[input_list.index('-vdw_sigma') + 1])
	if ('-bond_r0' in input_list): param['bond_r0'] = float(input_list[input_list.index('-bond_r0') + 1])
	#param['bond_r1'] = 1.5 * param['bond_r0']
	if ('-vdw_epsilon' in input_list): param['vdw_epsilon'] = float(input_list[input_list.index('-vdw_epsilon') + 1])
	if ('-bond_k0' in input_list): param['bond_k0'] = float(input_list[input_list.index('-bond_k0') + 1])
	#if ('-bond_k1' in input_list): param['bond_k1'] = float(input_list[input_list.index('-bond_k1') + 1])
	#if param['bond_k1'] < param['bond_k0']: param['bond_k1'] = param['bond_k0']
	if ('-angle_k0' in input_list): param['angle_k0'] = float(input_list[input_list.index('-angle_k0') + 1])
	if ('-rc' in input_list): param['rc'] = float(input_list[input_list.index('-rc') + 1])
	else: param['rc'] = param['vdw_sigma'] * 3.0
	if ('-kBT' in input_list): param['kBT'] = float(input_list[input_list.index('-kBT') + 1])
	if ('-gamma' in input_list): param['gamma'] = float(input_list[input_list.index('-gamma') + 1])
	param['sigma'] = np.sqrt(param['gamma'] * (2 - param['gamma']) * (param['kBT'] / param['mass']))
	if ('-nfibx' in input_list): param['n_fibril_x'] = int(input_list[input_list.index('-nfibx') + 1])
	if ('-nfiby' in input_list): param['n_fibril_y'] = int(input_list[input_list.index('-nfiby') + 1])
	if ('-nfibz' in input_list): param['n_fibril_z'] = int(input_list[input_list.index('-nfibz') + 1])
	param['n_fibril'] = param['n_fibril_x'] * param['n_fibril_y']
	if param['n_dim'] == 3: param['n_fibril'] *= param['n_fibril_z']
	if ('-lfib' in input_list): param['l_fibril'] = int(input_list[input_list.index('-lfib') + 1])
	param['n_bead'] = param['n_fibril'] * param['l_fibril']
	if ('-density' in input_list): param['density'] = float(input_list[input_list.index('-density') + 1])

	return param


def check_analysis_param(input_list, param=False):
	"""
	check_analysis_param(input_list, param=False)

	Checks input_list to overwrite analysis parameters in param dictionary 
	"""

	if not param: param = get_param_defaults()

	if ('-res' in input_list): param['res'] = float(input_list[input_list.index('-res') + 1])
	if ('-sharp' in input_list): param['sharp'] = float(input_list[input_list.index('-sharp') + 1])
	if ('-skip' in input_list): param['skip'] = int(input_list[input_list.index('-skip') + 1])
	if ('-lsample' in input_list): param['l_sample'] = int(input_list[input_list.index('-lsample') + 1])
	if ('-min_sample' in input_list): param['min_sample'] = int(input_list[input_list.index('-min_sample') + 1])

	return param


def read_input_file(input_file_name, files=False, simulation=False, analysis=False, file_names=False, param=False):
	"""
	read_input_file(input_file_name, files=False, simulation=False, analysis=False, param=False)

	Opens input_file_name and checks contents for simulation and/or analysis parameters to overwrite param dictionary
	"""

	if not file_names: file_names = get_file_name_defaults()
	if not param: param = get_param_defaults()

	with open(input_file_name, 'r') as infile:
		lines = infile.read().splitlines()
	input_list = (' '.join(lines)).split()

	if ('-nstep' in input_list): param['n_step'] = int(input_list[input_list.index('-nstep') + 1])
	if ('-save_step' in input_list): param['save_step'] = int(input_list[input_list.index('-save_step') + 1])

	if files: file_names = check_file_names(input_list, file_names)
	if simulation: param = check_sim_param(input_list, param)
	if analysis: param = check_analysis_param(input_list, param)

	return file_names, param


def manual_input_param(param=False):
	"""
	manual_input_param(param=False)

	Manual paramter input (CURRENTLY OBSOLETE)
	"""

	if not param: param = get_param_defaults()

	param['mass'] = float(input("Enter bead mass: "))
	param['vdw_sigma'] = float(input("Enter vdw sigma radius: "))
	param['vdw_epsilon'] = float(input("Enter vdw epsilon energy: "))
	param['bond_k0'] = float(input("Enter bond k0 energy: "))
	param['bond_k1'] = float(input("Enter bond k1 energy: "))
	param['angle_k'] = float(input("Enter angle k energy: "))
	param['kBT'] = float(input("Enter kBT constant: "))
	param['gamma'] = float(input("Enter Langevin gamma constant: "))
	param['l_fibril']  = int(input("Enter length of fibril (no. of beads): "))
	param['n_fibril_x']  = int(input("Enter number of fibrils in x dimension: "))
	param['n_fibril_y']  = int(input("Enter number of fibrils in y dimension: "))
	if param['n_dim'] == 3: param['n_fibril_z'] = int(input("Enter number of fibrils in z dimension: "))
	param['res'] = float(input("Enter resolution (1-10): "))
	param['sharp'] = float(input("Enter sharpness (1-10): "))
	param['skip'] = int(input("Enter number of sampled frames between each png: "))

	return param


def read_shell_input(current_dir, sim_dir, input_file_name=False, verbosity=True):
	"""
	read_shell_input(current_dir, sim_dir)

	Reads bash shell tags to gather simulation and analysis parameters.
	Order of input methods: default_param < input_file < inline tags < param_file 

	Parameters
	----------

	current_dir:  str
		Working directory from which ColECM excecutable is called

	sim_dir:  str
		Directory in which simulation files are to be saved

	Returns
	-------

	file_names:  list (str)
		List of simulation and analysis files names

	param:  dict
		Dictionary of simulation and analysis parameters
	"""

	file_names = get_file_name_defaults()
	param = get_param_defaults()

	if input_file_name: file_names, _ = read_input_file(input_file_name, files=True, file_names=file_names)

	file_names =  check_file_names(sys.argv, file_names=file_names)

	if not file_names['param_file_name']: 
		file_names['param_file_name'] = input("Enter param_file name: ")
		check_file_names(sys.argv, file_names=file_names)
	if not file_names['pos_file_name']: 
		file_names['pos_file_name'] = input("Enter pos_file name: ")
		check_file_names(sys.argv, file_names=file_names)

	keys = ['n_dim', 'dt', 'mass', 'vdw_sigma', 'vdw_epsilon', 'bond_r0', 'bond_k0', 'angle_theta0', 
			'angle_k0', 'rc', 'kBT', 'gamma', 'sigma', 'l_fibril', 'n_fibril_x', 'n_fibril_y', 
			'n_fibril_z', 'n_fibril', 'n_bead', 'density']

	if os.path.exists(sim_dir + file_names['param_file_name'] + '.pkl'):
		if verbosity: print(" Loading parameter file {}.pkl".format(sim_dir + file_names['param_file_name']))
		param_file = ut.read_param_file(sim_dir + file_names['param_file_name'])

		"""
		if param_file['l_fibre']:
			fibre_keys = ['l_fibre', 'n_fibre_x', 'n_fibre_y', 'n_fibre_z', 'n_fibre']			
			fibril_keys = ['l_fibril', 'n_fibril_x', 'n_fibril_y', 'n_fibril_z', 'n_fibril']
			for i, key in enumerate(fibril_keys): param_file[key] = param_file.pop(fibre_keys[i])

			ut.make_param_file(sim_dir + file_names['param_file_name'])
			for key in keys: ut.update_param_file(sim_dir + file_names['param_file_name'], key, param[key])
		"""

		for key in keys: param[key] = param_file[key]		
		for key in ['bond_matrix', 'angle_array', 'vdw_matrix']: param[key] = param_file[key]

	else:
		if input_file_name: _, param = read_input_file(input_file_name, simulation=True, param=param)
		param = check_sim_param(sys.argv, param)

		if verbosity: print(" Creating parameter file {}.pkl".format(sim_dir + file_names['param_file_name'])) 
		ut.make_param_file(sim_dir + file_names['param_file_name'])
		for key in keys: ut.update_param_file(sim_dir + file_names['param_file_name'], key, param[key])
		
	assert param['n_dim'] in [2, 3]
	assert param['rc'] >= 1.5 * param['vdw_sigma']

	if ('-nstep' in sys.argv): param['n_step'] = int(sys.argv[sys.argv.index('-nstep') + 1])
	if ('-save_step' in sys.argv): param['save_step'] = int(sys.argv[sys.argv.index('-save_step') + 1])

	param = check_analysis_param(sys.argv, param)

	if verbosity: 
		print(" Parameters found:")
		for key in keys: print(" {:<15s} : {}".format(key, param[key]))	

	return file_names, param


def grow_cell(param, max_energy=200, max_attempt=200):
	"""
	grow_cell(param, vdw_matrix, max_energy=200, max_attempt=200)

	Grow tumour cell cluster n beads

	Parameters
	----------

	param:  dict
		Dictionary of simulation and analysis parameters

	vdw_matrix: array_like (int); shape=(n_bead, n_bead)
		Matrix determining whether a non-bonded interaction is present between two beads

	max_energy:  float (optional)
		Maximum potential energy threshold for each system configuration

	max_attempt:  int  (optional)
		Maximum number of attempts to find an acceptable configuration
		
		
	Returns
	-------

	pos:  array_like (float); shape=(n_bead, n_dim)
		Updated positions of n_bead beads in n_dim

	"""

	if param['n_dim'] == 2: 
		from sim_tools import calc_energy_forces_2D as calc_energy_forces
		pos = (np.mgrid[:n_cell,:n_cell].reshape(n_cell**2, 2) + 10) * param['vdw_sigma']
		bond_matrix = np.zeros((n_cell**2, n_cell**2))
		vdw_matrix = (np.ones((n_cell**2, n_cell**2)) - np.identity(n_cell**2)) * 10
	elif param['n_dim'] == 3: 
		from sim_tools import calc_energy_forces_3D as calc_energy_forces
		pos = (np.mgrid[:n_cell,:n_cell,:n_cell].reshape(n_cell**3, 3) + 10) * param['vdw_sigma']
		bond_matrix = np.zeros((n_cell**3, n_cell**3))
		vdw_matrix = (np.ones((n_cell**3, n_cell**3)) - np.identity(n_cell**3)) * 10

	cell_dim = np.max(pos, axis=0)

	pos, vel = equilibrate_temperature(sim_dir, pos, cell_dim, bond_matrix, vdw_matrix, param)

	return pos


def grow_fibril(index, pos, param, max_energy=200, max_attempt=200):
	"""
	grow_fibril(index, bead, pos, param, bond_matrix, vdw_matrix, max_energy=200, max_attempt=200

	Grow collagen fibril consisting of beads

	Parameters
	----------

	index:  int
		Index of bead in pos array

	bead:  int
		Bead in fibril

	pos:  array_like (float); shape=(n_bead, n_dim)
		Positions of n_bead beads in n_dim

	param:  dict
		Dictionary of simulation and analysis parameters

	bond_matrix: array_like (int); shape=(n_bead, n_bead)
		Matrix determining whether a bond is present between two beads

	vdw_matrix: array_like (int); shape=(n_bead, n_bead)
		Matrix determining whether a non-bonded interaction is present between two beads

	max_energy:  float (optional)
		Maximum potential energy threshold for each system configuration

	max_attempt:  int  (optional)
		Maximum number of attempts to find an acceptable configuration
		
		
	Returns
	-------

	pos:  array_like (float); shape=(n_bead, n_dim)
		Updated positions of n_bead beads in n_dim

	"""

	if param['n_dim'] == 2: from sim_tools import calc_energy_forces_2D as calc_energy_forces
	elif param['n_dim'] == 3: from sim_tools import calc_energy_forces_3D as calc_energy_forces

	if index == 0:
		pos[index] = np.random.random((param['n_dim'])) * param['vdw_sigma'] * 2

	else:
		bond_indices, angle_indices, angle_bond_indices = ut.update_bond_lists(param['bond_matrix'])
		param['angle_array'] = np.ones(angle_indices.shape[0]) * param['angle_k0']

		energy = max_energy + 1
		attempt = 0

		while energy > max_energy:
			new_vec = ut.rand_vector(param['n_dim']) * param['bond_r0']	
			pos[index] = pos[index-1] + new_vec
			cell_dim = np.max(pos, axis=0) + param['vdw_sigma']

			_, energy, _ = calc_energy_forces(pos, cell_dim, bond_indices, angle_indices, angle_bond_indices, param)

			attempt += 1
			if attempt > max_attempt: raise RuntimeError

	return pos[index]


def create_pos_array(param):
	"""
	create_pos_array(param)

	Form initial positional array of beads

	Parameters
	----------

	param:  dict
		Dictionary of simulation and analysis parameters

		
	Returns
	-------

	pos:  array_like (float); shape=(n_bead, n_dim)
		Positions of n_bead beads in n_dim

	cell_dim:  array_like (float); shape=(n_dim)
		Simulation cell dimensions in n_dim dimensions

	bond_matrix: array_like (int); shape=(n_bead, n_bead)
		Matrix determining whether a bond is present between two beads

	vdw_matrix: array_like (int); shape=(n_bead, n_bead)
		Matrix determining whether a non-bonded interaction is present between two beads

	"""

	pos = np.zeros((param['n_bead'], param['n_dim']), dtype=float)
	bond_matrix = np.zeros((param['n_bead'], param['n_bead']), dtype=int)
	vdw_matrix = np.ones((param['n_bead'], param['n_bead']), dtype=int) * param['vdw_epsilon']
	temp_vdw = np.ones(param['n_bead'], dtype=int) * param['vdw_epsilon']

	for bead in range(param['n_bead']):
		if bead % param['l_fibril'] == 0: temp_vdw[bead] *= 10
		elif bead % param['l_fibril'] == param['l_fibril']-1: temp_vdw[bead] *= 10

	for row in range(param['n_bead']):
		if row % param['l_fibril'] == 0: vdw_matrix[row] = temp_vdw
		elif row % param['l_fibril'] == param['l_fibril']-1: vdw_matrix[row] = temp_vdw

	for bead in range(param['n_bead']): vdw_matrix[bead][bead] = 0

	for fibril in range(param['n_fibril']):
		for bead in range(1, param['l_fibril']):
			n = fibril * param['l_fibril'] + bead
			bond_matrix[n][n-1] = param['bond_k0'] 
			bond_matrix[n-1][n] = param['bond_k0'] 

	print(" Creating fibril template containing {} beads".format(param['l_fibril']))

	init_pos = np.zeros((param['l_fibril'], param['n_dim']), dtype=float)
	bead = 0

	while bead < param['l_fibril']:
		try:

			param['bond_matrix'] = bond_matrix[0:bead+1, 0:bead+1]
			param['vdw_matrix'] = vdw_matrix[0:bead+1, 0:bead+1]

			init_pos[bead] = grow_fibril(bead, init_pos[ : bead+1], param)
			bead += 1
		except RuntimeError: bead = 0

	pos[range(param['l_fibril'])] += init_pos
	pos -= np.min(pos)

	print(" Creating simulation cell containing {} fibrils".format(param['n_fibril']))

	if param['n_dim'] == 2:

		size_x = np.max(pos.T[0]) + 2 * param['vdw_sigma'] 
		size_y = np.max(pos.T[1]) + 2 * param['vdw_sigma'] 
		bead_list = np.arange(0, param['l_fibril'])

		for i in range(param['n_fibril_x']):
			for j in range(param['n_fibril_y']):
				if j + i == 0: continue
			
				fibril = (j + i * param['n_fibril_y'])

				pos_x = pos.T[0][bead_list] + size_x * i
				pos_y = pos.T[1][bead_list] + size_y * j

				pos[bead_list + param['l_fibril'] * fibril] += np.array((pos_x, pos_y)).T

		cell_dim = np.array([np.max(pos.T[0]) + param['vdw_sigma'], np.max(pos.T[1]) + param['vdw_sigma']])

	elif param['n_dim'] == 3:
		size_x = np.max(pos.T[0]) + param['vdw_sigma'] / 2
		size_y = np.max(pos.T[1]) + param['vdw_sigma'] / 2
		size_z = np.max(pos.T[2]) + param['vdw_sigma'] / 2
		bead_list = np.arange(0, param['l_fibril'])

		for k in range(param['n_fibril_z']):
			for i in range(param['n_fibril_x']):
				for j in range(param['n_fibril_y']):
					if k + j + i == 0: continue
				
					fibril = (j + i * param['n_fibril_y'] + k * param['n_fibril_x'] * param['n_fibril_y'])

					pos_x = pos.T[0][bead_list] + size_x * i
					pos_y = pos.T[1][bead_list] + size_y * j
					pos_z = pos.T[2][bead_list] + size_z * k

					pos[bead_list + param['l_fibril'] * fibril] += np.array((pos_x, pos_y, pos_z)).T

		cell_dim = np.array([np.max(pos.T[0]) + param['vdw_sigma'] / 2, np.max(pos.T[1]) + param['vdw_sigma'] / 2, np.max(pos.T[2]) + param['vdw_sigma'] / 2])

	bond_indices, angle_indices, angle_bond_indices = ut.update_bond_lists(bond_matrix)

	param['bond_matrix'] = bond_matrix
	param['angle_array'] = np.ones(angle_indices.shape[0]) * param['angle_k0']
	param['vdw_matrix'] = vdw_matrix

	return pos, cell_dim, param


def calc_state(pos, cell_dim, param):
	"""
	calc_state(pos, cell_dim, bond_matrix, vdw_matrix, param)
	
	Calculate state of simulation using starting configuration and parameters provided

	Parameters
	----------

	pos:  array_like (float); shape=(n_bead, n_dim)
		Positions of n_bead beads in n_dim

	cell_dim: array_like, dtype=float
		Array with simulation cell dimensions

	bond_matrix: array_like (int); shape=(n_bead, n_bead)
		Matrix determining whether a bond is present between two beads

	vdw_matrix: array_like (int); shape=(n_bead, n_bead)
		Matrix determining whether a non-bonded interaction is present between two beads

	param:  dict
		Dictionary of simulation and analysis parameters
	
	Returns
	-------

	frc: array_like, dtype=float
		Forces acting upon each bead in all collagen fibrils

	verlet_list: array_like, dtype=int
		Matrix determining whether two beads are within rc radial distance

	pot_energy:  float
		Total potential energy of system

	virial_tensor:  array_like, (float); shape=(n_dim, n_dim)
		Virial components of pressure tensor of system

	bond_beads:  array_like, (int); shape=(n_angle, 3)
		Array containing indicies in pos array all 3-bead angular interactions

	dist_index:  array_like, (int); shape=(n_bond, 2)
		Array containing indicies in distance arrays of all bonded interactions

	r_index:  array_like, (int); shape=(n_bond, 2)
		Array containing indicies in r array of all bonded interactions
	
	"""

	import time

	if param['n_dim'] == 2: from sim_tools import calc_energy_forces_2D as calc_energy_forces
	elif param['n_dim'] == 3: from sim_tools import calc_energy_forces_3D as calc_energy_forces

	bond_indices, angle_indices, angle_bond_indices = ut.update_bond_lists(param['bond_matrix'])
	frc, pot_energy, virial_tensor = calc_energy_forces(pos, cell_dim, bond_indices, angle_indices, angle_bond_indices, param)

	return frc, pot_energy, virial_tensor, bond_indices, angle_indices, angle_bond_indices


def calc_state_mpi(pos, cell_dim, param, comm, size=1, rank=0):
	"""
	calc_state(pos, cell_dim, bond_matrix, vdw_matrix, param)
	
	Calculate state of simulation using starting configuration and parameters provided

	Parameters
	----------

	pos:  array_like (float); shape=(n_bead, n_dim)
		Positions of n_bead beads in n_dim

	cell_dim: array_like, dtype=float
		Array with simulation cell dimensions

	bond_matrix: array_like (int); shape=(n_bead, n_bead)
		Matrix determining whether a bond is present between two beads

	vdw_matrix: array_like (int); shape=(n_bead, n_bead)
		Matrix determining whether a non-bonded interaction is present between two beads

	param:  dict
		Dictionary of simulation and analysis parameters
	
	Returns
	-------

	frc: array_like, dtype=float
		Forces acting upon each bead in all collagen fibrils

	verlet_list: array_like, dtype=int
		Matrix determining whether two beads are within rc radial distance

	pot_energy:  float
		Total potential energy of system

	virial_tensor:  array_like, (float); shape=(n_dim, n_dim)
		Virial components of pressure tensor of system

	bond_beads:  array_like, (int); shape=(n_angle, 3)
		Array containing indicies in pos array all 3-bead angular interactions

	dist_index:  array_like, (int); shape=(n_bond, 2)
		Array containing indicies in distance arrays of all bonded interactions

	r_index:  array_like, (int); shape=(n_bond, 2)
		Array containing indicies in r array of all bonded interactions
	
	"""

	from mpi4py import MPI

	if param['n_dim'] == 2: from sim_tools import calc_energy_forces_2D_mpi as calc_energy_forces
	elif param['n_dim'] == 3: from sim_tools import calc_energy_forces_3D_mpi as calc_energy_forces

	bond_indices, angle_indices, angle_bond_indices = ut.update_bond_lists_mpi(param['bond_matrix'], comm, size, rank)

	pos_indices = np.array_split(np.arange(param['n_bead']), size)[rank]
	frc_indices = (bond_indices[0] + pos_indices[0], bond_indices[1])
	angle_coeff = np.array_split(param['angle_array'], size)[rank]
	vdw_coeff = np.array_split(param['vdw_matrix'], size)[rank]
	virial_indicies = ut.create_index(np.argwhere(np.array_split(np.tri(param['n_bead']).T, size)[rank]))

	#verlet_list_rb = ut.check_cutoff(r2, param['bond_rb']**2)

	frc, pot_energy, virial_tensor = calc_energy_forces(pos, cell_dim, pos_indices, bond_indices, frc_indices, 
							angle_indices, angle_bond_indices, angle_coeff, vdw_coeff, virial_indicies, param)

	pot_energy = np.sum(comm.gather(pot_energy))
	frc = comm.allreduce(frc, op=MPI.SUM)
	virial_tensor = comm.allreduce(virial_tensor, op=MPI.SUM)

	"""
	if rank == 0:
		angle_indices, angle_bond_indices, r_indices, _ = ut.update_bond_lists(bond_matrix)
		distances = ut.get_distances(pos, cell_dim)
		r2 = np.sum(distances**2, axis=0)
		verlet_list_rc = ut.check_cutoff(r2, param['rc']**2)
		pot_energy, frc, virial_tensor = calc_energy_forces(distances, r2, param, bond_matrix, vdw_matrix, verlet_list_rc, angle_indices, angle_bond_indices, r_indices)

		print((pot_energy_mpi - pot_energy) < 1E-10)
		print(np.sum(frc_mpi - frc) < 1E-10)
		print(np.sum(virial_tensor_mpi - virial_tensor) < 1E-10)

	sys.exit()
	"""

	return frc, pot_energy, virial_tensor, bond_indices, angle_indices, angle_bond_indices



def import_files(sim_dir, file_names, param, verbosity=True):
	"""
	import_files(sim_dir, file_names, param)

	Imports existing or creates new simulation files listed in file_names 

	Parameters
	----------

	sim_dir:  str
		Directory in which simulation files are to be saved

	file_names:  list (str)
		List of simulation and analysis files names

	param:  dict
		Dictionary of simulation and analysis parameters

	Returns
	-------

	pos:  array_like (float); shape=(n_bead, n_dim)
		Positions of n_bead beads in n_dim

	vel: array_like, dtype=float
		Velocity of each bead in all collagen fibrils

	cell_dim:  array_like (float); shape=(n_dim)
		Simulation cell dimensions in n_dim dimensions

	param:  dict
		Dictionary of simulation and analysis parameters
	"""

	from simulation import equilibrate_temperature, equilibrate_density

	if os.path.exists(sim_dir + file_names['restart_file_name'] + '.npy'):
		if verbosity: print(" Loading restart file {}.npy".format(sim_dir + file_names['restart_file_name']))
		restart = ut.load_npy(sim_dir + file_names['restart_file_name'])

		pos = restart[0]
		vel = restart[1]
		cell_dim = pos[-1]
		pos = pos[:-1]

	elif os.path.exists(sim_dir + file_names['pos_file_name'] + '.npy'):
		if verbosity: print(" Loading position file {}.npy".format(sim_dir + file_names['pos_file_name']))
		pos = ut.load_npy(sim_dir + file_names['pos_file_name'])

		cell_dim = pos[-1]
		pos = pos[:-1]

		pos, vel = equilibrate_temperature(sim_dir, pos, cell_dim, param)

	else:
		file_names['pos_file_name'] = ut.check_file_name(file_names['pos_file_name'], file_type='pos') + '_pos'
		if verbosity: print(" Creating input pos file {}{}.npy".format(sim_dir, file_names['pos_file_name']))
		pos, cell_dim, param = create_pos_array(param)

		#param['l_conv'] = 1. / param['vdw_sigma']

		keys = ['bond_matrix', 'angle_array', 'vdw_matrix']#, 'l_conv']
		for key in keys: ut.update_param_file(sim_dir + file_names['param_file_name'], key, param[key])

		if verbosity: print(" Saving input pos file {}{}.npy".format(sim_dir, file_names['pos_file_name']))
		ut.save_npy(sim_dir + file_names['pos_file_name'], np.vstack((pos, cell_dim)))

		pos, vel = equilibrate_temperature(sim_dir, pos, cell_dim, param)
		pos, vel, cell_dim = equilibrate_density(pos, vel, cell_dim, param)

		if verbosity: print(" Saving restart file {}".format(file_names['restart_file_name']))
		ut.save_npy(sim_dir + file_names['restart_file_name'], (np.vstack((pos, cell_dim)), vel))

	return pos, vel, cell_dim, param


def import_files_mpi(sim_dir, file_names, param, comm, size=1, rank=0, verbosity=True):
	"""
	import_files(sim_dir, file_names, param)

	Imports existing or creates new simulation files listed in file_names 

	Parameters
	----------

	sim_dir:  str
		Directory in which simulation files are to be saved

	file_names:  list (str)
		List of simulation and analysis files names

	param:  dict
		Dictionary of simulation and analysis parameters

	Returns
	-------

	pos:  array_like (float); shape=(n_bead, n_dim)
		Positions of n_bead beads in n_dim

	vel: array_like, dtype=float
		Velocity of each bead in all collagen fibrils

	cell_dim:  array_like (float); shape=(n_dim)
		Simulation cell dimensions in n_dim dimensions

	param:  dict
		Dictionary of simulation and analysis parameters
	"""

	from mpi4py import MPI
	from simulation_mpi import equilibrate_temperature_mpi, equilibrate_density_mpi

	if os.path.exists(sim_dir + file_names['restart_file_name'] + '.npy'):
		if rank == 0: 
			if verbosity: print(" Loading restart file {}.npy".format(sim_dir + file_names['restart_file_name']))
			restart = ut.load_npy(sim_dir + file_names['restart_file_name'])
		else: restart = None
		restart = comm.bcast(restart, root=0)

		pos = restart[0]
		vel = restart[1]
		cell_dim = pos[-1]
		pos = pos[:-1]

	elif os.path.exists(sim_dir + file_names['pos_file_name'] + '.npy'):
		if rank == 0:
			if verbosity: print(" Loading position file {}.npy".format(sim_dir + file_names['pos_file_name']))
			pos = ut.load_npy(sim_dir + file_names['pos_file_name'])
		else: pos = None
		pos = comm.bcast(pos, root=0)
		
		cell_dim = pos[-1]
		pos = pos[:-1]

		pos, vel = equilibrate_temperature_mpi(sim_dir, pos, cell_dim, param, comm, size, rank)

	else:
		file_names['pos_file_name'] = ut.check_file_name(file_names['pos_file_name'], file_type='pos') + '_pos'

		if rank == 0: 
			if verbosity: print(" Creating input pos file {}{}.npy".format(sim_dir, file_names['pos_file_name']))
			pos, cell_dim, param = create_pos_array(param)

			#param['l_conv'] = 1. / param['vdw_sigma']

			keys = ['bond_matrix', 'angle_array', 'vdw_matrix']#, 'l_conv']
			for key in keys: ut.update_param_file(sim_dir + file_names['param_file_name'], key, param[key])

			if verbosity: print(" Saving input pos file {}{}.npy".format(sim_dir, file_names['pos_file_name']))
			ut.save_npy(sim_dir + file_names['pos_file_name'], np.vstack((pos, cell_dim)))
		else:
			pos = None
			cell_dim = None

		pos = comm.bcast(pos, root=0)
		cell_dim = comm.bcast(cell_dim, root=0)
		param = comm.bcast(param, root=0)

		pos, vel = equilibrate_temperature_mpi(sim_dir, pos, cell_dim, param, comm, size, rank)
		pos, vel, cell_dim = equilibrate_density_mpi(pos, vel, cell_dim, param, comm, size, rank)

		if rank == 0: 
			if verbosity: print(" Saving restart file {}".format(file_names['restart_file_name']))
			ut.save_npy(sim_dir + file_names['restart_file_name'], (np.vstack((pos, cell_dim)), vel))

	return pos, vel, cell_dim, param



