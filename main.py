import json  # Pour l'export en JSON

class InventoryManager:
    def __init__(self, filename = 'Inventory.csv'):
        # On initialise le gestionnaire avec le nom du fichier d'inventaire:
        self.filename = filename

    def get_next_id(self):
        # On génère le prochain ID en lisant la dernière ligne du fichier:
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                if not lines:
                    return 1
                last_line =lines[-1].strip().split(',')
                return int(last_line[0]) +1
        except FileNotFoundError:
            return 1 # Si le fichier n'existe pas encore

    def ensure_newline(self):
        # On s'assure que la dernière ligne du csv a bien été sauté, pour éviter les
        # porblèmes de format:
    try:
        with open(self.filename, 'rb+') as file:
            file.seek(0, 2)  # Aller à la fin du fichier
            if file.tell() == 0:
                return  # Fichier vide, rien à faire
            file.seek(-1, 2)
            last_char = file.read(1)
            if last_char != b'\n':
                file.write(b'\n')  # Ajoute un saut de ligne si manquant
    except FileNotFoundError:
        pass  # Le fichier sera créé plus tard


    def add_to_inventory(self):
        # Ajoute un nouvel article à l'inventaire:
        name = str(input('Enter the name of the product:')).capitalize().strip()
        cleaned_name = ''.join(char for char in name if char.isalnum() or char.isspace()).strip().capitalize()
        try:
            quantity = int(input(f'Enter a quantity for {cleaned_name}:'))
        except ValueError:
            print('Invalid Quantity!')
            return
        try:
            price = float(input(f'Enter the price of {cleaned_name}:'))
        except ValueError:
            print('Invalid Price!')
            return
        confirm = input(f'Do you want to add {quantity} {cleaned_name} with price {price} € to the inventory? (y or n)')

        if confirm.lower() == "y":
            item_id = self.get_next_id()
            self.ensure_newline()
            with open(self.filename, 'a') as file:
                inventory_item = f'{item_id},{cleaned_name},{quantity},{price}\n'
                file.writelines(inventory_item)
                print(f'{name} successfully added to the inventory!')
        else: 
            print('Operation cancelled.')


    def view_inventory(self):
        # Affiche tous les articles de l'inventaire:
        try:
            with open(self.filename, 'r') as file:
                print("📦 INVENTAIRE ACTUEL")
                print("-" * 40)
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 4:
                            id, name, quantity, price = parts
                            print(f'Id: {id}, Item: {name}, Quantity: {quantity}, Price: {price} €')
                    else:
                            print('Wrong Format:', line.strip())
        except FileNotFoundError:
            print('Inventory file not found. Please add items first.')

    def update_inventory(self):
        # Mettre à jour la quantité ou le prix d’un article:
        item_id = input('Enter item ID to update: ').strip()
        field = input('Update (Q)uantity or (P)rice? ').lower()
        updated = False
        new_lines = []

        with open(self.filename, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 4 and parts[0] == item_id:
                    if field.lower() == 'q':
                        new_value = input('New quantity: ')
                        parts[2] = new_value
                    elif field.lower() == 'p':
                        new_value = input('New price: ')
                        parts[3] = new_value
                    else:
                        print('Invalid field.')
                        return
                    updated = True
                new_lines.append(','.join(parts) + '\n')

        if updated:
            with open(self.filename, 'w') as file:
                file.writelines(new_lines)
            print(f'Item ID {item_id} updated.')
        else:
            print('Item not found.')
        

    def delete_item(self):
        # Supprimer un article par son nom
        name = input("Item to delete: ").strip().capitalize()
        new_lines = []
        deleted = False
        with open(self.filename, 'r') as file:
            for line in file:
                if line.strip().split(',')[1].capitalize() != name:
                    new_lines.append(line)
                else:
                    deleted = True
        if deleted:
            with open(self.filename, 'w') as file:
                file.writelines(new_lines)
            print(f'{name} deleted from inventory.')
        else:
            print('Item not found.')


    def total_value(self):
        # Calcule la valeur totale de l’inventaire:
        total = 0
        try:
            with open(self.filename,'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 4:
                        quantity = int(parts[2])
                        price = float(parts[3])
                        total += quantity * price
            print(f'\n Total inventory value: {total:.2f} €')   
        except FileNotFoundError:
            print('Inventory file not found')
            
     def export_to_json(self, json_filename='inventory.json'):
        # Exporter l’inventaire au format JSON:
        inventory_list = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 4:
                        item = {
                            'id': int(parts[0]),
                            'name': parts[1],
                            'quantity': int(parts[2]),
                            'price': float(parts[3])
                        }
                        inventory_list.append(item)
            with open(json_filename, 'w') as json_file:
                json.dump(inventory_list, json_file, indent=4)
            print(f'Inventory successfully exported {json_filename}')
        except FileNotFoundError:
            print('Inventory file not found.')



def main():
    
    manager = InventoryManager()

    #Boucle principale:
    while True:
        print('-----MENU-----')
        print('1. Viewing Inventory')
        print('2. Add an Item')
        print('3. Update an Item')
        print('4. Remove an Item')
        print('5. Total value of Inventory')
        print('6. Export to json')
        print('7. Exit')

        choice = input("Your Choice: ")
        if choice == "1":
            manager.view_inventory()
        elif choice == "2":
            manager.add_to_inventory()
        elif choice == "3":
            manager.update_inventory()
        elif choice == "4":
            manager.delete_item()
        elif choice == "5":
            manager.total_value()
        elif choice == "6":
            manager.export_to_json()
        elif choice == "7":
            print('Goodbye!')
            break
        else:
            print("Invalid Option.")

if __name__ == '__main__':
    main()
