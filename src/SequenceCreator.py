class SequenceCreator:
    relations: list = []
    tableIds: list = []
    tableIdSequence: dict = {}
    level: int = 0

    def __init__(self, dictAll: dict) -> None:
        self.relations = dictAll["relation"]
        self.tableIds = [d["id"] for d in dictAll["entity"]["table"]]
        self.setSequence()

    def setSequence(self):
        self.setAllTablesWithoutRelations()
        self.setAllTablesWithoutTarget()

    def setAllTablesWithoutRelations(self):
        rSource = list({d["source"] for d in self.relations})
        rTarget = list({d["target"] for d in self.relations})
        allTablesWithoutRelations = list(
            set(self.tableIds) - set(rSource) - set(rTarget)
        )

        self.setNextLevel(allTablesWithoutRelations)

    def setAllTablesWithoutTarget(self):
        rTarget = list({d["target"] for d in self.relations})
        self.setNextLevel(list(set(self.tableIds) - set(rTarget)))
        if len(self.tableIds):
            self.setAllTablesWithoutTarget()

    def setNextLevel(self, tableIds: list = []):
        if len(tableIds):
            self.tableIdSequence[self.level] = tableIds
            self.tableIds = list(set(self.tableIds) - set(tableIds))
            self.relations = [d for d in self.relations if d["source"] not in tableIds]
            self.level += 1

    def getSequence(self) -> dict:
        return self.tableIdSequence
