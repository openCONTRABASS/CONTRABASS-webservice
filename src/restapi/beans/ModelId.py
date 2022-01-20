class ModelId:
    def __init__(self, model, metabolites, reactions, genes, reactions_list):
        self.model_uuid = model
        self.metabolites = metabolites
        self.reactions = reactions
        self.genes = genes
        self.reactions_list = reactions_list

    @property
    def get_model_uuid(self):
        return self.model_uuid

    @get_model_uuid.setter
    def set_model_uuid(self, model):
        self.model_uuid = model

    @property
    def get_metabolites(self):
        return self.metabolites

    @get_metabolites.setter
    def set_metabolites(self, metabolites):
        self.metabolites = metabolites

    @property
    def get_reactions(self):
        return self.reactions

    @get_reactions.setter
    def set_reactions(self, reactions):
        self.reactions = reactions

    @property
    def get_genes(self):
        return self.genes

    @get_genes.setter
    def set_genes(self, genes):
        self.genes = genes

    @property
    def get_reactions_list(self):
        return self.reactions_list

    @get_reactions_list.setter
    def set_reactions_list(self, reactions_list):
        self.reactions_list = reactions_list
