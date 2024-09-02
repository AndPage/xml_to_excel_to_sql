class RelationsFormatter:
    tables: list = []
    tableRow: list = []
    partialRectangle: list = []
    relations: list = []

    def __init__(self, all_dict: dict):
        print(all_dict)
        self.tables = all_dict["entity"]['table']
        self.tableRow = all_dict["entity"]['tableRow']
        self.partialRectangle = all_dict["entity"]['partialRectangle']

        if len(all_dict["relation"]) == 1 and 'orthogonalEdgeStyle' in all_dict["relation"]:
            self.relations = self.get_relations(all_dict["relation"]['orthogonalEdgeStyle'])
        else:
            raw_relations = self.get_raw_relations(all_dict["relation"])
            self.relations = self.create_relations(raw_relations, all_dict["relation"]['orthogonalEdgeStyle'])

    def get_relations(self, relations: dict) -> dict:
        self.corrected_values(relations, "source")
        self.corrected_values(relations, "target")

        return relations

    @staticmethod
    def get_raw_relations(all_dict: dict) -> list:
        return [i for k, v in all_dict.items() if k != "orthogonalEdgeStyle" and isinstance(v, list) for i in v]

    def create_relations(self, raw_relations: list, orthogonal: dict) -> list:
        formatted_relations = []
        for item in raw_relations:
            all_source = [o for o in orthogonal if o.get("target") == item["id"]]
            all_target = [o for o in orthogonal if o.get("source") == item["id"]]
            if len(all_source) != 1 or len(all_target) < 1:
                print(f"ERROR: the number of arrows are not correct:\n"
                      f"to: {all_source}\nfrom: {all_target}\nitem: {item}\nrelation is skipped\n")
                continue

            self.check_cardinality(all_source[0])
            self.corrected_values(all_source, "source")
            self.corrected_values(all_target, "target")
            for target in all_target:
                formatted_relations.append(self.get_item(item, all_source, target))

        return formatted_relations

    def check_cardinality(self, item):
        if 'value' not in item or item["value"] == "1":
            print(f"ERROR: check cardinality, source has to be 1:\nitem: {item}\n")

    def corrected_values(self, items, field) -> None:
        for k, item in enumerate(items):
            id_tables = [i["id"] for i in self.tables]
            if item[field] in id_tables:
                continue

            ids_tableRow = [i["id"] for i in self.tableRow]
            if item[field] in ids_tableRow:
                item[field] = next(i["parent"] for i in self.tableRow if i.get("id") == item[field])
                continue

            id_partialRectangle = [i["id"] for i in self.partialRectangle]
            if item[field] in id_partialRectangle:
                tableRow_id = next(i["parent"] for i in self.partialRectangle if i.get("id") == item[field])
                item[field] = next(i["parent"] for i in self.tableRow if i.get("id") == tableRow_id)
                continue

            print("ERROR: the Arrow has no connection")

    def get_item(self, item, all_source, target):

        copy_item = item.copy()
        removed_value = copy_item.pop("value", None)

        copy_item["target"] = target["target"]
        copy_item["target_value"] = target.get("value", "")

        copy_item["source"] = all_source[0]["source"]
        copy_item["source_value"] = all_source[0].get("value", "")

        copy_item["value"] = removed_value

        return copy_item

    def get_formatted_relations(self):
        for i in self.relations:
            print(i)

        return self.relations
