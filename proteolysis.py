#! python

from PDBreader import *
import calc_sasa_for_atoms as sasa


def find_restriction_sites(residues: list, site_seq: list):
    rest_start = []
    for f in range(len(residues)):
        count = 1
        if residues[f].name == site_seq[0]:
            while count < len(site_seq):
                if residues[f + count].name != site_seq[count]:
                    break
                if count == len(site_seq) - 1:
                    rest_start.append(f)
                    break
                count += 1
    return rest_start


def check_sasa(residue):
    bb = False
    for f in residue.atoms:
        if f.sasa > 10:
            bb = True
    return bb


def check_site_sasa(sites_start, residues: list, site_seq: list):
    checked = []
    length = len(site_seq)
    for site in sites_start:
        bb = True
        for res in range(site, site + length):
            acces = check_sasa(residues[res])
            if not acces:
                bb = False
        if bb:
            checked.append(site)
    return checked


if __name__ == "__main__":
    file = PDBfile('3a1f.pdb')
    atoms_list = file.atoms
    residues = file.residues
    # print(atoms_list[1].sasa)
    sasa.compute_sasa_for_atoms(atoms_list, 1.40, 100, sasa.ATOMIC_RADII)
    # print(atoms_list[1].sasa)
    start_res= find_restriction_sites(residues, ['ILE', 'ALA'])
    start_res = check_site_sasa(start_res, residues, ['ILE', 'ALA'])
    with open('results.txt', 'a') as file:
        for f in start_res:
            file.write('id of residue with start of restriction site: ' + str(residues[f].id))
