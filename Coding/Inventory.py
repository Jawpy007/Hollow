class inventory:
    def __init__(self):
        self.items_dict=dict()
    
    def add_items(self, item, item_name):
        assert item_name not in self.items_dict.keys(), "Il y a déjà un item du même nom dans l'inventaire."
        self.items_dict[item_name]= item

    def update(self):
        for item in self.items_dict.values():
            item.update()



    def get_item(self,item_name):
        return self.items_dict[item_name]
    
