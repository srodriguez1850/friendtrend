import json, pprint, os, itertools, datetime

pp = pprint.PrettyPrinter(indent = 4)

data_path = "data/messages/inbox/"

all_json_data = []

all_json_files = list(
    map(
        lambda x: os.path.join(data_path, x, "message.json"),
        os.listdir(data_path)
    )
)

for json_file in all_json_files:
    with open(json_file) as f:
        json_data = json.load(f)
        json_data["my_friend_id"] = json_file.split("/")[-2]
        all_json_data.append(json_data)

# print(len(all_json_data))

# filter out group conversations
all_json_data_dm = list(filter(lambda x: x["thread_type"] == "Regular", all_json_data))
# print(len(all_json_data_dm))
all_json_data_dm = list(filter(lambda x: x["participants"] != [{'name': 'Prashant Jayannavar'}], all_json_data_dm))
# print(len(all_json_data_dm))

# processing
def process(json):
    def f(message):
        if message["sender_name"] == 'Prashant Jayannavar':
            sender_id = "me"
            recipient_id = json["my_friend_id"]
        else:
            sender_id = json["my_friend_id"]
            recipient_id = "me"

        datetime_obj = datetime.datetime.fromtimestamp(message["timestamp_ms"]/1000.0)

        transformed_msg = {
            "sender_id": sender_id,
            "recipient_id": recipient_id,
            "my_friend_id": json["my_friend_id"],
            "year": datetime_obj.year,
            "month": datetime_obj.month,
        }

        return transformed_msg

    transformed_msgs = list(map(lambda x: f(x), json["messages"]))

    return transformed_msgs

all_msgs = list(map(lambda x: process(x), all_json_data_dm))
all_msgs = list(itertools.chain.from_iterable(all_msgs))

# print(len(all_msgs))

# grouping

def process_messages_by_year(all_msgs):

    # group by year
    msgs_by_year = {}
    for year, group in itertools.groupby(sorted(all_msgs, key = lambda x: x["year"]), key = lambda x: x["year"]):
        msgs_by_year[year] = list(group)

    # pp.pprint(msgs_by_year[2019])

    for key, value in msgs_by_year.items():
        msgs_by_friend = {}
        for my_friend_id, group in itertools.groupby(sorted(value, key = lambda x: x["my_friend_id"]), key = lambda x: x["my_friend_id"]):
            msgs_by_friend[my_friend_id] = list(group)
        msgs_by_year[key] = msgs_by_friend

    # print("\n\n")
    # pp.pprint(msgs_by_year[2019])

    for key, value in msgs_by_year.items():
        for key2, value2 in value.items():
            msgs_by_year[key][key2] = len(value2)

    # print("\n\n")
    # pp.pprint(msgs_by_year[2019])

    for key, value in msgs_by_year.items():
        msgs_by_year[key] = sorted(value.items(), key = lambda x: x[1], reverse = True)

    # print("\n\n")
    # pp.pprint(msgs_by_year[2019])

    for old_key in msgs_by_year.keys():
        new_key = str(old_key) + "-01-01"
        msgs_by_year[new_key] = msgs_by_year.pop(old_key)

    print(msgs_by_year.keys())

    with open("messages_yearly_scratch.json", "w") as f:
        json.dump(msgs_by_year, f)

process_messages_by_year(all_msgs)
