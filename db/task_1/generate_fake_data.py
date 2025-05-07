from faker import Faker
import random
import pandas as pd

fake = Faker()

business_fields = ["Healthcare", "Retail", "Finance", "IT Services", "E-commerce"]
locations = ["Riyadh", "Jeddah", "Dubai", "Abu Dhabi", "Cairo", "Beirut", "Doha", "Muscat", "Kuwait City", "Manama"]

def generate_fake_company():
    company_name = fake.company()  
    staff_count = random.randint(10, 1000)  
    business_field = random.choice(business_fields)  
    description = fake.sentence()  
    location = random.choice(locations)  

    return {
        "company_name": company_name,
        "staff_count": staff_count,
        "business_field": business_field,
        "description": description,
        "location": location
    }


fake_data = [generate_fake_company() for _ in range(10)]

df = pd.DataFrame(fake_data)

df.to_excel('fake_company_data.xlsx', index=False)