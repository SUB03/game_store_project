from faker import Faker
import random
import pandas as pd

if __name__ == "__main__":
    n = 100000
    fake = Faker()
    Faker.seed(42)
    random.seed(42)

    people = []
    for i in range(n):
        people.append({"id": i, "first_name": fake.first_name(),
            "last_name": fake.last_name()})
        
    items = []
    person_ids = [int(p["id"]) for p in people]
    for i in range(30000):
        item = random.choice(["chair", "pc", "laptop", "phone", "book", "iphone", "car"])
        person_id = random.choice(person_ids) if random.random() < 0.95 else None
        items.append({"id": i, "item_name": item, "people_id": person_id})

    courses_df = pd.read_csv("datasets/Online_Courses.csv", usecols=["Title"])
    courses_count = len(courses_df["Title"])
    enrollments_hash = set()
    for i in range(n):
        course_id = random.randint(0, courses_count-1)
        person_id = random.choice(person_ids)
        enrollments_hash.add((course_id, person_id))

    enrollments = []
    for a,b in enrollments_hash:
        enrollments.append({"course_id": a, "person_id": b})    
    
    courses_df.to_csv("datasets/onlineCourses.csv", index_label="id")
    items_df = pd.DataFrame(items)
    items_df["people_id"] = items_df["people_id"].astype("Int64") # pandas treats columns with null values as floats
    items_df.to_csv("datasets/fakeItems.csv", index=False)
    pd.DataFrame(people).to_csv("datasets/fakePeople.csv", index=False)
    pd.DataFrame(enrollments).to_csv("datasets/fakeEnrollments.csv", index=False)