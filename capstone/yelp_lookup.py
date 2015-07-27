import json

def business_dict(file_path): 
    business_lookup = {}
    with open(file_path) as data_file: 
        for line in data_file: 
            business_data = json.loads(line)
            business_id = business_data['business_id']
            state = business_data['state']
            category = business_data['categories']
            if business_lookup.get(business_id) is not None: 
                print "%s not uniuqe" % business_id
                break
            business_lookup[business_id] = (state, category)
    return business_lookup