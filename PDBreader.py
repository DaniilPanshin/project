
class Atom:
    def __init__(self, coordinates, idd, residue_name, residue_id, element):
        self.coord = coordinates
        self.id = idd
        self.residue_name = residue_name
        self.residue_id = residue_id
        self.element = element


class Residue:
    def __init__(self, idd, residue_name):
        self.atoms = []
        self.name, self.id = residue_name, idd


class PDBfile:
    def __init__(self, path_to_file):
        self.atoms, self.residues = [], []
        with open(path_to_file, "r") as f:
            current_res_id = ''
            for line in f:
                if line.startswith("ATOM"):  # ищем строку с атомом
                    idd = int(line[6:11])
                    element = line[12:16].strip()
                    residue_name = line[17:20].strip()
                    residue_id = int(line[22:26])
                    coordinates = [float(line[30:38]), float(line[38:46]), float(line[46:54])]
                    current_atom = Atom(coordinates, idd, residue_name, residue_id, element)
                    self.atoms.append(current_atom)
                    if current_res_id != residue_id:
                        current_res_id = residue_id
                        residue = Residue(residue_id, residue_name)
                        self.residues.append(residue)
                    if residue:
                        residue.atoms.append(current_atom)
