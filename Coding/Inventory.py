class inventory:
    def __init__(self):
        self.items_dict=dict()
        self.affected_melee_item="fist" # prend la clé qui est reelier a l'item dans self.items_dict, cette variable stock l'item de melee que le joueur a equiper
        self.affected_range_item=None # prend la clé qui est reelier a l'item dans self.items_dict, cette variable stock l'item a distance que le joueur a equiper
        self.affected__spell=None # prend la clé qui est reelier a l'item dans self.items_dict, cette variable stock le sort maqique que le joueur a equiper
    
    def add_items(self, item, item_name):
        assert item_name not in self.items_dict.keys(), "Il y a déjà un item du même nom dans l'inventaire."
        self.items_dict[item_name]= item

    def update(self):
        for item in self.items_dict.values():
            item.update()

    def affected_range_item_set(self):  
        pass

    def affected_melee_item_set(self):
        pass

    def affected__spell_set(self):
        pass

    def get_item(self,item_name):
        return self.items_dict[item_name]
    
