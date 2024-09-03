class SqlCreator:
    data_list: list = []
    tab: str = "\t"

    def __init__(self, data_list):
        self.data_list = data_list

    def get_sql_list(self):
        return [
            f"CREATE TABLE orders(",
            f"{self.tab}order_id INT AUTO_INCREMENT PRIMARY KEY,",
            f"{self.tab}customer_id INT,",
            f"{self.tab}order_date DATE,",
            f"{self.tab}amount DECIMAL(10, 2),",
            f"{self.tab}FOREIGN KEY(customer_id) REFERENCES customers(customer_id)",
            ");"
        ]
