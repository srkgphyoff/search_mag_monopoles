import ROOT
from array import array

class OutFunc:
    def __init__(self, name, directory, prefix, C, useVar):
        """
        name      : Name of MVA method
        directory : Path to directory containing weights file
        prefix    : Prefix of weights file
        C         : offset subtracted later from model output
        useVar    : List of 7 booleans indicating which variables to be used (0 is 'rand' not to be used)
        """
        self.reader = ROOT.TMVA.Reader()
        self.name = name
        self.C = C

        # TMVA variable names starting from index 1 in the data (index 0 is ignored)
        self.var_names = [
            "ADC_mean",      # index 1
            "nhits_min",     # index 2
            "entry_dist",    # index 3
            "exit_dist",     # index 4
            "docasqrx_max",  # index 5
            "docasqry_max"   # index 6
        ]

        self.vars = [array("f", [0.]) for _ in self.var_names]
        self.use_flags = useVar[1:]  # Skip index 0

        # Add selected variables to the TMVA reader
        for i, (var_name, use) in enumerate(zip(self.var_names, self.use_flags)):
            if use:
                self.reader.AddVariable(var_name, self.vars[i])

        # Load the trained weights
        weightfile = f"{directory}/{prefix}_{name}.weights.xml"
        self.reader.BookMVA(name, weightfile)

    def val(self, entry):
        """
        entry: A ROOT TTree entry with attributes corresponding to TMVA input variables.
        """
        for i, (var_name, use) in enumerate(zip(self.var_names, self.use_flags)):
            if use:
                self.vars[i][0] = getattr(entry, var_name)

        return self.reader.EvaluateMVA(self.name) - self.C