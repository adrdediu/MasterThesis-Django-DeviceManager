# yourappname/management/commands/create_initial_instances.py
from django.core.management.base import BaseCommand
from ...models import Inventory, Subcategory,Category,Building,Room,Floor  # Import your model

class Command(BaseCommand):
    help = 'Create or update instances for Subcategory, Category, Building, Floor, and Room models'

    def handle(self, *args, **options):
        # Define predefined values for your instances
        categories_data = [
            {'id': 1, 'name': 'Computers'},
            {'id': 2, 'name': 'Labware' },
            {'id': 3, 'name': 'Network'},
            {'id': 4, 'name': 'Peripherals'},
            {'id': 5, 'name': 'Storage'},
            {'id': 6, 'name': 'IoT Device'},
            {'id': 7, 'name': 'Other'},
            # Add more categories as needed
        ]
        
        self.create_instances(Category, categories_data)

        subcategories_data = [


            # Computers
            {'id': 11, 'name': 'Laptops', 'category': Category.objects.get(id=1)},
            {'id': 12, 'name': 'Desktop PCs', 'category': Category.objects.get(id=1)},

            # Labware
            {'id': 21, 'name': 'Analyzers', 'category': Category.objects.get(id=2)},
            {'id': 22, 'name': 'Development Boards', 'category': Category.objects.get(id=2)},
            {'id': 23, 'name': 'Oscilloscopes', 'category': Category.objects.get(id=2)},
            {'id': 24, 'name': 'Multimeters', 'category': Category.objects.get(id=2)},
            {'id': 25, 'name': 'Power Supplies', 'category': Category.objects.get(id=2)},
            {'id': 26, 'name': 'Signal Generators', 'category': Category.objects.get(id=2)},


            # Networking
            {'id': 31, 'name': 'Routers', 'category': Category.objects.get(id=3)},
            {'id': 32, 'name': 'Firewalls', 'category': Category.objects.get(id=3)},
            {'id': 33, 'name': 'Servers', 'category': Category.objects.get(id=3)},
            {'id': 34, 'name': 'Switches', 'category': Category.objects.get(id=3)},
            {'id': 35, 'name': 'Racks', 'category': Category.objects.get(id=3)},
            
            # Peripherals
            {'id': 41, 'name': 'Cameras', 'category': Category.objects.get(id=4)},
            {'id': 42, 'name': 'Microphones', 'category': Category.objects.get(id=4)},
            {'id': 43, 'name': 'Printers', 'category': Category.objects.get(id=4)},
            {'id': 44, 'name': 'Projectors', 'category': Category.objects.get(id=4)},
            {'id': 45, 'name': 'Scanners', 'category': Category.objects.get(id=4)},


            #  Storage
            {'id': 51, 'name': 'Hard Drives', 'category': Category.objects.get(id=5)},
            {'id': 52, 'name': 'SSDs', 'category': Category.objects.get(id=5)},
            {'id': 53, 'name': 'NAS', 'category': Category.objects.get(id=5)},

            # Smart Devices
            {'id': 61, 'name': 'Smart Lamp', 'category': Category.objects.get(id=6)},
            
            # Other
            {'id': 71, 'name': 'Other', 'category': Category.objects.get(id=7)},

        ]

        self.create_instances(Subcategory, subcategories_data)

        buildings_data = [
            {'id': 1, 'name': 'Faculty of Electronics Telecommunications and Information Technology Iasi - Body A', 'address': 'Bd. Carol I, no. 11 A, Iaşi, 700506', 'acronym': 'ETTI - A'},
            {'id': 2, 'name': 'Faculty of Electronics Telecommunications and Information Technology Iasi - Body C', 'address': 'Strada Lascăr Catargi 38, Iași 700107', 'acronym': 'ETTI - C'},
            # Add more buildings as needed
        ]

        self.create_instances(Building, buildings_data)

        inventories_data = [
            {'id': 1, 'name': f'Inventory - {Building.objects.get(id=1).acronym}', 'building': Building.objects.get(id=1)},
            {'id': 2, 'name': f'Inventory - {Building.objects.get(id=2).acronym}', 'building': Building.objects.get(id=2)},
        ]

        self.create_instances(Inventory, inventories_data)


        # ID -  GUIDE [BF] - B Building Number, F - Floor Number
        floors_data = [
            {'id': 11, 'name': 1, 'building': Building.objects.get(id=1)},
            {'id': 12, 'name': 2, 'building': Building.objects.get(id=1)},
            {'id': 13, 'name': 3, 'building': Building.objects.get(id=1)},
            {'id': 21, 'name': 0, 'building': Building.objects.get(id=2)},
            {'id': 22, 'name': 1, 'building': Building.objects.get(id=2)},
            # Add more floors as needed
        ]
        self.create_instances(Floor, floors_data)

        # ID -  GUIDE [BFRR] - B Building Number, F - Floor Number, RR - Room Number 
        rooms_data = [
            # ETTI - A Floors levels: 1-3
                # # # Floor 1 
                {'id': 1108, 'name': '1.08', 'floor': Floor.objects.get(id=11),'building': Building.objects.get(id=1)},
                {'id': 1111, 'name': '1.11', 'floor': Floor.objects.get(id=11),'building': Building.objects.get(id=1)},
                {'id': 1115, 'name': '1.15', 'floor': Floor.objects.get(id=11),'building': Building.objects.get(id=1)},

                # # # Floor 2 
                {'id': 1203, 'name': '2.03', 'floor': Floor.objects.get(id=12),'building': Building.objects.get(id=1)},
                {'id': 1204, 'name': '2.04', 'floor': Floor.objects.get(id=12),'building': Building.objects.get(id=1)},
                {'id': 1206, 'name': '2.06', 'floor': Floor.objects.get(id=12),'building': Building.objects.get(id=1)},
                {'id': 1208, 'name': '2.08', 'floor': Floor.objects.get(id=12),'building': Building.objects.get(id=1)},

                {'id': 1210, 'name': '2.10', 'floor': Floor.objects.get(id=12),'building': Building.objects.get(id=1)},
                {'id': 1213, 'name': '2.13', 'floor': Floor.objects.get(id=12),'building': Building.objects.get(id=1)},

                {'id': 1223, 'name': '2.23', 'floor': Floor.objects.get(id=12),'building': Building.objects.get(id=1)},
                {'id': 1228, 'name': '2.28', 'floor': Floor.objects.get(id=12),'building': Building.objects.get(id=1)},
                {'id': 1229, 'name': '2.29', 'floor': Floor.objects.get(id=12),'building': Building.objects.get(id=1)},

                # # # Floor 3
                {'id': 1307, 'name': '3.07', 'floor': Floor.objects.get(id=13),'building': Building.objects.get(id=1)},
                {'id': 1309, 'name': '3.09', 'floor': Floor.objects.get(id=13),'building': Building.objects.get(id=1)},
                {'id': 1310, 'name': '3.10', 'floor': Floor.objects.get(id=13),'building': Building.objects.get(id=1)},
                {'id': 1312, 'name': '3.12', 'floor': Floor.objects.get(id=13),'building': Building.objects.get(id=1)},
                {'id': 1316, 'name': '3.16', 'floor': Floor.objects.get(id=13),'building': Building.objects.get(id=1)},
                {'id': 1319, 'name': '3.19', 'floor': Floor.objects.get(id=13),'building': Building.objects.get(id=1)},
                {'id': 1322, 'name': '3.22', 'floor': Floor.objects.get(id=13),'building': Building.objects.get(id=1)},
                {'id': 1324, 'name': '3.24', 'floor': Floor.objects.get(id=13),'building': Building.objects.get(id=1)},
                {'id': 1325, 'name': '3.25', 'floor': Floor.objects.get(id=13),'building': Building.objects.get(id=1)},
                {'id': 1326, 'name': '3.26', 'floor': Floor.objects.get(id=13),'building': Building.objects.get(id=1)},    
                {'id': 1327, 'name': '3.27', 'floor': Floor.objects.get(id=13),'building': Building.objects.get(id=1)},
                {'id': 1334, 'name': '3.34', 'floor': Floor.objects.get(id=13),'building': Building.objects.get(id=1)},
                {'id': 1337, 'name': '3.37', 'floor': Floor.objects.get(id=13),'building': Building.objects.get(id=1)},
                {'id': 1338, 'name': '3.38', 'floor': Floor.objects.get(id=13),'building': Building.objects.get(id=1)},
           
            # ETTI - C Levels: 0-1
                {'id': 2001, 'name': 'C.0.1', 'floor': Floor.objects.get(id=21),'building': Building.objects.get(id=2)},
        ]

        self.create_instances(Room, rooms_data)

    def create_instances(self, model, instances_data):
        for data in instances_data:
            # Try to get an existing instance based on the specified ID
            existing_instance = model.objects.filter(id=data['id']).first()

            if existing_instance:
                # Update existing instance
                for key, value in data.items():
                    setattr(existing_instance, key, value)
                existing_instance.save()
                self.stdout.write(self.style.SUCCESS(f'Updated {model.__name__} instance with {data}'))
            else:
                # Create a new instance
                model.objects.create(**data)
                self.stdout.write(self.style.SUCCESS(f'Created {model.__name__} instance with {data}'))