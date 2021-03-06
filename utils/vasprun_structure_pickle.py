from pymatgen.io.vasp.outputs import Vasprun
import os
import pickle
from multiprocessing import Pool
import sys
import argparse


def store_structures(folder, filename):
	"""
	read in vasprun files, convert to structure files and pickle them

	Args:
		folder: under with the subfolder with vasprun.xml files in it
				i.e. folder/subfolder/vasprun.xml
		filename: filename to store the pickle(in folder)
	"""
	structure_list = []
	subfolder_list = 
	for i, subfolder in enumerate(os.listdir(folder)):
		vasprun_file = os.path.join(folder, subfolder+'/vasprun.xml')
		if os.path.exists(vasprun_file):
			struc = Vasprun(vasprun_file).final_structure
			structure_list.append(struc)
		if i%10 == 0:
			print("read the {}th vasprun.xml file".format(i))

	with open(os.path.join(folder, filename), 'wb') as f:
		pickle.dump(structure_list, f, -1)


def store_structures_parallel(folder, filename, n_process):
	"""
	read in vasprun files, convert to structure objects in parallel and pickle them 

	Args:
		folder: under with the subfolder with vasprun.xml files in it
				i.e. folder/subfolder/vasprun.xml
		filename: filename to store the pickle(in folder)
		n_process: the number of processes
	"""
	vasprun_list = []
	subfolder_list = []
	for i, subfolder in enumerate(os.listdir(folder)):
		vasprun_file = os.path.join(folder, subfolder+'/vasprun.xml')
		if os.path.exists(vasprun_file):
			vasprun_list.append(vasprun_file)
			subfolder_list.append(subfolder)

	p = Pool(n_process)
	structure_list = p.map(vasp_to_struc, vasprun_list)

	structure_dict = {}
	for subfolder, structure in zip(subfolder_list, structure_list):
		structure_dict[subfolder] = structure
	#print(structure_list)

	with open(os.path.join(folder, filename), 'wb') as f:
		pickle.dump(structure_dict, f, -1)

	####TO DO: solving the encoding!!!!!!!! btw python2 and python3

def vasp_to_struc(vasprun_file):
	return Vasprun(vasprun_file).final_structure


def load_structures(filepath):
	"""
	read the pickled structure_dict in file as given by filepath

	Returns: 
		a dict of structures with folder name as keys
	"""
	with open(filepath, 'rb') as f:
		structure_dict = pickle.load(f)
	return structure_dict
	#print(structure_list)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Pickle all structures in this folder')
	parser.add_argument('folder', help='folder containing subfolder with vasprun.xml files.')
	parser.add_argument('-f', '--filename', default='structure.pkl', help='filename of the pickle file.')
	parser.add_argument('-t', '--threads', default=4, type=int, help='number of threads to use (default: 4)')
	args = parser.parse_args(sys.argv[1:])

	store_structures_parallel(args.folder, args.filename, args.threads)
	#print(load_structures('/Users/yao/Google Drive/mmtools/data/sample_vasp_calculation/structure.pkl'))
