class IRepositoryBase:
    def get_version(self):
        raise NotImplementedError

    def add(self, data) -> None:
        raise NotImplementedError

    def delete(self, data) -> None:
        raise NotImplementedError

    def commit(self) -> None:
        raise NotImplementedError

    def get_all(self) -> list:
        raise NotImplementedError

    def get_count(self) -> int:
        raise NotImplementedError

    def get(self, *args) -> list:
        raise NotImplementedError

    def order_by_desc(self, col_map, *args) -> list:
        raise NotImplementedError

    def order_by_asc(self, col_map, *args) -> list:
        raise NotImplementedError

    def get_col(self, *args) -> list:
        raise NotImplementedError

    def max(self, col_map) -> int:
        raise NotImplementedError
