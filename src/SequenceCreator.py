from src.helper.RelationsFormatter import RelationsFormatter


class SequenceCreator:
    relations: list = []
    tableIds: list = []
    tableIdSequence: dict = {}
    level: int = 0

    def __init__(self, dictAll: dict) -> None:
        relation_formatter = RelationsFormatter(dictAll)
        self.relations = [item for item in relation_formatter.get_relations() if item["source"] != item["target"]]
        self.tableIds = [d["id"] for d in dictAll["entity"]["table"]]
        # for i in dictAll["entity"]["table"]:
        #     print(i)

        self.setSequence()

        # print(self.relations)
        # print(self.tableIds)

    def setSequence(self):
        self.setAllTablesWithoutRelations()
        self.setAllTablesWithoutTarget()

    def setAllTablesWithoutRelations(self):
        rSource = list({d["source"] for d in self.relations})
        rTarget = list({d["target"] for d in self.relations})
        allTablesWithoutRelations = list(
            set(self.tableIds) - set(rSource) - set(rTarget)
        )
        # print(allTablesWithoutRelations, 'allTablesWithoutRelations')
        self.setNextLevel(allTablesWithoutRelations)

    def setAllTablesWithoutTarget(self):
        for i in range(200):
            rTarget = list({d["target"] for d in self.relations})
            # print(rTarget, 'all relation targets')
            # print(self.tableIds, 'all tables')
            self.setNextLevel(list(set(self.tableIds) - set(rTarget)))
            # print(self.tableIds, len(self.tableIds))
            if len(self.tableIds) == 0:
                break

    def setNextLevel(self, table_ids: list):
        if len(table_ids):
            self.tableIdSequence[self.level] = table_ids
            self.tableIds = list(set(self.tableIds) - set(table_ids))
            self.relations = [d for d in self.relations if d["source"] not in table_ids]
            self.level += 1

    def getSequence(self) -> dict:
        return self.tableIdSequence
