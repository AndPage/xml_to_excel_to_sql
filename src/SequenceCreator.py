class SequenceCreator:
    relations: list = []
    tableIds: list = []
    tableIdSequence: dict = {}
    level: int = 0

    def __init__(self, dictAll: dict) -> None:
        # TODO: relations anpassen (drei elemente in eins vereinen)
        self.relations = dictAll["relation"]['orthogonalEdgeStyle']
        self.tableIds = [d["id"] for d in dictAll["entity"]["table"]]

        # print(self.relations)
        # print(self.tableIds)
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
        for i in range(50):
        # while true:
            rTarget = list({d["target"] for d in self.relations})
            # print(rTarget)
            self.setNextLevel(list(set(self.tableIds) - set(rTarget)))
            # print(self.tableIds)
            if not len(self.tableIds):
                break

    def setNextLevel(self, tableIds: list = []):
        if len(tableIds):
            self.tableIdSequence[self.level] = tableIds
            self.tableIds = list(set(self.tableIds) - set(tableIds))
            self.relations = [d for d in self.relations if d["source"] not in tableIds]
            self.level += 1

    def getSequence(self) -> dict:
        return self.tableIdSequence
